from abc import ABC, abstractmethod
from typing import BinaryIO


class BaseStorageAdapter(ABC):

    @abstractmethod
    def upload_file(
        self,
        file: BinaryIO,
        destination_path: str,
        content_type: str | None = None,
    ) -> str:
        """
        Upload file and return storage path.
        """
        pass

    @abstractmethod
    def delete_file(self, path: str) -> None:
        pass

    @abstractmethod
    def generate_signed_url(self, path: str) -> str:
        pass
