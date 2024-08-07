from django.shortcuts import render, redirect
from .models import Contact
from pages.models import Topbar
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.

def contactForm(request):
    
    if request.method == "POST":
        message_name = request.POST['message-name']  # here message-name comes from contact.html file's input type name
        message_email = request.POST['message-email']
        message = request.POST['message']

        ### Send an Email Start ###
        send_mail(
            message_name, # subject
            message, # message
            message_email, # from email
            ['omarfaruk2468@gmail.com'], # To email
        )
        ### Send an Email End ###
        return render(request, 'contacts/contact-form.html', {'message_name':message_name})

    else:
        ad = Topbar.objects.get()
        tb = Topbar.objects.get()
        return render(request, 'contacts/contact-form.html', {'ad':ad, 'tb':tb})




def contact(request):

    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)

            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        # Send email
        # Go to this address - https: // myaccount.google.com / lesssecureapps  to give less secure app access
        send_mail(
            'Property Listing Inquiry',  # Subject
            'There has been an inquiry for ' + listing + '. sign into the admin panel for more info', # Body
            'sumaiyabinte580@gmail.com', # This is the from email address
            [realtor_email, 'omarfaruk2468@gmail.com'], # This is to email address means we are specifiying where should the email goes
            fail_silently=False
        )

        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')

        return redirect('/listings/'+listing_id)


        
