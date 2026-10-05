class InvalidIdentifierError(ValueError):
    """Raised when an identifier has an invalid format."""

class InvalidRecordError(ValueError):
    """Raised when a CSV record cannot be accepted."""