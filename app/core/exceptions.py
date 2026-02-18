class AppException(Exception):
    """Base application exception."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppException):
    pass


class ConflictError(AppException):
    pass


class PermissionDenied(AppException):
    pass


class AuthenticationError(AppException):
    pass
