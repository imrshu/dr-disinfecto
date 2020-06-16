from django.core.mail import send_mail
from django.conf import settings
from .models import Order


def saveOrder(*args, **kwargs):
    Order.objects.create(**kwargs)


def sendOrderEmail(msg, email):
    send_mail('Dr Disinfecto Order Placed', msg, email, [settings.EMAIL_HOST_USER])
