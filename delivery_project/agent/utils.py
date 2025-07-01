import random
import string
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp):
    subject = "Your Password Reset OTP"
    message = f"Your OTP for password reset is: {otp}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
