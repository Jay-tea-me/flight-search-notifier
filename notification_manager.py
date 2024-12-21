import os
from constants import *
from twilio.rest import Client

class NotificationManager:
    def send_sms(self, message_body:str):
        account_sid = os.environ[TWILIO_ACCOUNT_SID]
        auth_token = os.environ[TWILIO_AUTH_TOKEN]
        client = Client(account_sid, auth_token)
        # need to replace this to work
        from_num = os.environ[TWILIO_VIRTUAL_NUMBER]
        print(f"sending sms from {from_num} to  {from_num}")
        message = client.messages.create(
            body= message_body,
            from_= from_num,
            to= from_num
        )
