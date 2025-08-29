# test_sms.py
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path=r"C:\Users\User\Desktop\test_rasa3\.env")
client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
message = client.messages.create(
    body="Test SMS: User test DASS-21 Results: Anxiety - Extremely Severe (20.0)",
    from_=os.getenv('TWILIO_PHONE_NUMBER'),
    to=os.getenv('RESPONSIBLE_PERSON_PHONE')
)
print(f"SMS sent: {message.sid}")