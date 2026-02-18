from google.cloud import storage
from uuid import uuid4
from typing import BinaryIO
from datetime import timedelta

from app.adapters.storage.base import BaseStorageAdapter
from app.core.config import settings


class GCPStorageAdapter(BaseStorageAdapter):

    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(settings.GCP_BUCKET_NAME)

    def upload_file(
        self,
        file: BinaryIO,
        destination_path: str,
        content_type: str | None = None,
    ) -> str:
        unique_name = f"{uuid4()}_{destination_path}"
        blob = self.bucket.blob(unique_name)

        blob.upload_from_file(
            file,
            content_type=content_type,
        )

        return unique_name

    def delete_file(self, path: str) -> None:
        blob = self.bucket.blob(path)
        blob.delete()

    def generate_signed_url(self, path: str) -> str:
        blob = self.bucket.blob(path)
        return blob.generate_signed_url(
            version="v4",
            expiration=timedelta(hours=1),
            method="GET",
        )
