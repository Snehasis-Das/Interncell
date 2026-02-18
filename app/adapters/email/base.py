from abc import ABC, abstractmethod


class EmailAdapter(ABC):

    @abstractmethod
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        """
        Send an email.
        Must raise exception on failure.
        """
        pass
