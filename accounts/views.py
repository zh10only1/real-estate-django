from django.shortcuts import render, redirect
from django.contrib import messages, auth ## For message
from django.contrib.auth.models import User  ## Django User model (Built in)
from contacts.models import Contact
from .models import Agent, OTPVerification
from django.contrib.auth import logout, login, authenticate
from pages.models import Topbar
import re, random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.template.loader import render_to_string
import json
from django.contrib.auth.decorators import login_required
from django.utils import translation



def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        country = request.POST.get('country')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # company data
        company_name = request.POST.get('company_name')
        # logo is a image file
        company_logo = request.FILES.get('company_logo')
        portrait_photo = request.FILES.get('portrait_photo')
        oib_number = request.POST.get('oib_number')
        domain = request.POST.get('domain')

        # check if first name and lastname contains numbers
        if any(char.isdigit() for char in first_name) or any(char.isdigit() for char in last_name):
            messages.error(request, 'First name and last name cannot contain numbers')
            return render(request, 'account/signup.html')

        # check valid email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email):
            messages.error(request, 'Invalid email')
            return render(request, 'account/signup.html')

        username = email.split('@')[0]
        if User.objects.filter(username=username).exists():
            username = username + \
                str(User.objects.filter(username=username).count())

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'account/signup.html')
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return render(request, 'account/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'account/signup.html')

        user = User.objects.create_user(username, email, password)
        
        user.save()

        userProfile = Agent.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            city=city,
            country=country,
            company_name=company_name,
            company_logo=company_logo,
            portrait_photo=portrait_photo,
            oib_number=oib_number,
            domain=domain,
        )
        userProfile.save()

        # login user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            otp = random.randint(100000, 999999)

            otpVerification = OTPVerification.objects.get_or_create(user=request.user)[0]
            otpVerification.otp = otp
            otpVerification.sent_at = timezone.now()
            otpVerification.save()

            # send otp to email
            name = request.user.first_name
            template = render_to_string(
                'account/otpEmail.html', {'name': name, 'otp': otp, 'action': 'Verify Email'})
            send_mail(
                'OTP for Email Verification',
                template,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=template,
            )
            message = 'OTP sent to ' + email
            messages.success(request, message)
            context = {
                'verifyEmailPage': True,
                'title': 'Verify Email',
            }
            return render(request, 'account/verifyEmail.html', context)
        return redirect('account:login')
    return render(request, 'account/signup.html')


def login_view(request):
    site_language = request.session.get('site_language')
    if not site_language:
        request.session['site_language'] = 'ge'
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is None:
            # try to authenticate with email
            try:
                user = User.objects.get(email=username)
                user = authenticate(
                    request, username=user.username, password=password)
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password')
                return render(request, 'account/login.html')
            
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are successfully logged in')
            return redirect('main:home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('account:login')

    else:
        tb = Topbar.objects.get()
        return render(request, 'account/login.html', {'tb':tb})


def logout_view(request):

    logout(request)

    return redirect('account:login')


def dashboard(request):

    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id) # request.user means current logged in user
    tb = Topbar.objects.get()
    context = {
        'contacts':user_contacts,
        'tb':tb,
    }

    return render(request, 'accounts/dashboard.html', context)


def agents(request, pk):

    agents = Agent.objects.get(id=pk)
    tb = Topbar.objects.get()

    context = {
        'agents':agents,
        'tb':tb,
    }

    return render(request, 'accounts/agents.html', context)


@login_required(login_url='account:login')
def verifyEmail(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otpVerification = OTPVerification.objects.get(user=request.user)
        now = timezone.now()
        if now - otpVerification.sent_at > timedelta(minutes=5):
            messages.error(request, 'OTP expired')
            context = {
                'verifyEmailPage': True,
                'title': 'Verify Email',
                'resend_button': True
            }
            return render(request, 'account/verifyEmail.html', context)

        if str(otpVerification.otp) == otp:
            messages.success(request, 'Email verified successfully')
            otpVerification.is_verified = True
            otpVerification.save()
            user = request.user
            userProfile = Agent.objects.get_or_create(user=user)[0]
            userProfile.save()
            return redirect('main:home')
        else:
            messages.error(request, 'Invalid OTP')
            context = {
                'verifyEmailPage': True,
                'title': 'Verify Email',
            }
            return render(request, 'account/verifyEmail.html', context)

    email = request.user.email
    otp = random.randint(100000, 999999)

    otpVerification = OTPVerification.objects.get_or_create(user=request.user)[
        0]
    now = timezone.now()
    if now - otpVerification.sent_at < timedelta(minutes=2):
        try_after = 2 - (now - otpVerification.sent_at).seconds // 60
        messages.error(request, f'Otp already sent. Try after {try_after} minutes')
        context = {
            'verifyEmailPage': True,
            'title': 'Verify Email',
            'resend_button': True,
        }
        return render(request, 'account/verifyEmail.html', context)
    otpVerification.otp = otp
    otpVerification.sent_at = timezone.now()
    otpVerification.save()

    # send otp to email
    name = request.user.first_name
    template = render_to_string(
        'account/otpEmail.html', {'name': name, 'otp': otp, 'action': 'Verify Email'})
    send_mail(
        'OTP for Email Verification',
        template,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        html_message=template,
    )
    message = 'OTP sent to ' + email
    messages.success(request, message)
    context = {
        'verifyEmailPage': True,
        'title': 'Verify Email',
    }
    return render(request, 'account/verifyEmail.html', context)


def verifyOTP(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')
        forget_password = request.POST.get('forget_password')
        otpVerification = OTPVerification.objects.get(
            user=User.objects.get(email=email))
        now = timezone.now()
        otp_sent_at = otpVerification.sent_at
        if now - otp_sent_at > timedelta(minutes=5):
            messages.error(request, 'OTP expired. Please try again.')
            return render(request, 'account/forgetPassword.html')

        if otp == str(otpVerification.otp):
            otpVerification.verified = True
            otpVerification.save()
            if forget_password:
                context = {
                    'resetPasswordPage': True,
                    'title': 'Reset Password',
                    'email': email,
                }
                return render(request, 'account/resetPassword.html', context)
            return redirect('main:home')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            context = {
                'verifyEmailPage': True,
                'title': 'Verify Email',
                'email': email,
            }
            return render(request, 'account/verifyOTP.html', context)

    return render(request, 'account/forgetPassword.html')


def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            otpVerification = OTPVerification.objects.get_or_create(user=user)[
                0]
            prev_otp_sent_at = otpVerification.sent_at
            now = timezone.now()
            if now - prev_otp_sent_at < timedelta(minutes=2):
                try_again_in = 2 - (now - prev_otp_sent_at).seconds // 60
                messages.error(request, f'OTP already sent. Try again in {try_again_in} minutes')
                context = {
                    'verifyEmailPage': True,
                    'title': 'Forget Password',
                    'email': email,
                    'otp_already_sent': True,
                }
                return render(request, 'account/verifyOTP.html', context)
            otp = random.randint(100000, 999999)
            otpVerification.otp = otp
            otpVerification.sent_at = now
            otpVerification.save()

            # send otp to email
            name = user.first_name
            template = render_to_string(
                'account/otpEmail.html', {'name': name, 'otp': otp})
            send_mail(
                'OTP for password reset',
                template,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=template,
            )

            message = f'OTP sent to {email}'
            messages.success(request, message)
            context = {
                'verifyEmailPage': True,
                'title': 'Verify Email',
                'email': email,
                'forget_password': True,
            }
            return render(request, 'account/verifyOTP.html', context)
        else:
            messages.error(request, 'Email does not exists')
            return render(request, 'account/forgetPassword.html')

    return render(request, 'account/forgetPassword.html')


def resetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'Password does not match')
            context = {
                'resetPasswordPage': True,
                'title': 'Reset Password',
                'email': email,
            }
            return render(request, 'account/resetPassword.html', context)

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return redirect('account:login')

    return redirect("account:forget_password")

