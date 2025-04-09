import requests
from django.conf import settings

def send_resend_email(to_email, subject, html_content):
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {settings.EMAIL_HOST_PASSWORD}",
        "Content-Type": "application/json"
    }
    data = {
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
