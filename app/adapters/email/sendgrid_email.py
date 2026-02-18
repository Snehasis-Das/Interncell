
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.adapters.email.base import EmailAdapter
from app.core.config import settings


class SendGridEmailAdapter(EmailAdapter):

    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.from_email = settings.EMAIL_FROM

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=body,
        )

        response = self.client.send(message)

        if response.status_code >= 400:
            raise Exception("Failed to send email")
