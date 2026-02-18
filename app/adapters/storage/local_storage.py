import os
from uuid import uuid4
from typing import BinaryIO

from app.adapters.storage.base import BaseStorageAdapter


class LocalStorageAdapter(BaseStorageAdapter):

    def __init__(self, base_dir: str = "uploads"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def upload_file(
        self,
        file: BinaryIO,
        destination_path: str,
        content_type: str | None = None,
    ) -> str:
        unique_name = f"{uuid4()}_{destination_path}"
        full_path = os.path.join(self.base_dir, unique_name)

        # Reset pointer to start (important for safety)
        file.seek(0)

        with open(full_path, "wb") as buffer:
            buffer.write(file.read())

        return unique_name

    def delete_file(self, path: str) -> None:
        full_path = os.path.join(self.base_dir, path)
        if os.path.exists(full_path):
            os.remove(full_path)

    def generate_signed_url(self, blob_name: str) -> str:
        return f"/uploads/{blob_name}"
