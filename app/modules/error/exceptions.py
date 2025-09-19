from .codes import ErrorCode


class DomainException(Exception):
    def __init__(
        self,
        error: str = "Error",
        code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR,
        details: dict | None = None,
    ):
        super().__init__(error)
        self.success = False
        self.error = error
        self.code = code
        self.details = details or {}

    def __str__(self):
        return f"{self.code.name}: {self.error} - Details: {self.details}"

    def to_dict(self):
        return {
            "success": self.success,
            "error": self.error,
            "code": self.code.name,
            "details": self.details,
        }


class UniqueConstraintException(DomainException):
    """Exception raised for unique constraint violations."""

    def __init__(self, error: str = "Item already exists", details=None):
        super().__init__(error, ErrorCode.UNIQUE_CONSTRAINT_VIOLATION, details)

    pass
