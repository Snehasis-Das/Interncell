from app.adapters.email.base import EmailAdapter


class ConsoleEmailAdapter(EmailAdapter):

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        print("----- EMAIL (Console Adapter) -----")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print("Body:")
        print(body)
        print("-----------------------------------")
