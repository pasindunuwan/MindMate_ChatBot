# test_twilio.py
from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()
client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'))
try:
    message = client.messages.create(
        from_=os.getenv('TWILIO_PHONE'),
        to=os.getenv('RESPONSIBLE_PHONE'),
        body="Test SMS from RASA chatbot"
    )
    print(f"SMS sent: {message.sid}")
except Exception as e:
    print(f"Error: {e}")