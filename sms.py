from twilio.rest import Client
import os


class SMS:
    def __init__(self):
        # SMS settings
        self.account_sid = os.environ.get('account_sid')
        self.auth_token = os.environ.get('auth_token')

    def send_text(self, msg):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages \
            .create(
            body=msg,
            to=os.environ.get('dest'),
            from_='+18643839494'
        )
