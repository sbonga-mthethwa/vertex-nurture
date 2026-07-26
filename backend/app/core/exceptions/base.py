class ApplicationError(Exception):
    """
    Base application exception.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "APPLICATION_ERROR",
        status_code: int = 400,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

        super().__init__(message)

class ValidationError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
        )


class NotFoundError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=404,
        )


class ConflictError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="CONFLICT",
            status_code=409,
        )


class AuthenticationError(ApplicationError):
    def __init__(self, message: str = "Authentication required."):
        super().__init__(
            message=message,
            error_code="UNAUTHORIZED",
            status_code=401,
        )


class AuthorizationError(ApplicationError):
    def __init__(self, message: str = "Permission denied."):
        super().__init__(
            message=message,
            error_code="FORBIDDEN",
            status_code=403,
        )


class BusinessRuleViolation(ApplicationError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="BUSINESS_RULE_VIOLATION",
            status_code=422,
        )