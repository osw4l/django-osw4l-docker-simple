from twilio.rest import Client
from django.conf import settings


def send_sms(phone, sms):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_=settings.TWILIO_FROM_NUMBER,
        to='{}'.format(phone),
        body=sms
    )
