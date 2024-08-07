from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Agent
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

# if is_active is changed to True, then send email to the user
@receiver(pre_save, sender=Agent)
def agent_pre_save(sender, instance, **kwargs):
    try:
        old_agent = Agent.objects.get(pk=instance.pk)
        if instance.is_active and not old_agent.is_active:
            # send email to the user
            name = instance.first_name + ' ' + instance.last_name
            email = instance.user.email
            template = render_to_string(
                'account/accountActiveEmail.html', {'name': name})
            send_mail(
                'Account Activated',
                template,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=template,
            )
            
    except:
        pass


# if an agent is created, then send email to admin
@receiver(post_save, sender=Agent)
def agent_post_save(sender, instance, created, **kwargs):
    if created:
        # send email to admin
        superusers = User.objects.filter(is_superuser=True)
        for superuser in superusers:
            email = superuser.email
            template = render_to_string(
                'account/accountCreatedEmail.html')
            send_mail(
                'Account Created',
                template,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=template,
            )
