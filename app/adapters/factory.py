from app.core.config import settings

from app.adapters.email.console_email import ConsoleEmailAdapter
from app.adapters.email.sendgrid_email import SendGridEmailAdapter

from app.adapters.storage.local_storage import LocalStorageAdapter
from app.adapters.storage.gcp_storage import GCPStorageAdapter


def get_email_adapter():
    '''
    if settings.ENVIRONMENT == "production":
        return SendGridEmailAdapter()
    '''
    return ConsoleEmailAdapter()


def get_storage_adapter():
    if settings.STORAGE_MODE == "gcp":
        return GCPStorageAdapter()
    return LocalStorageAdapter()
