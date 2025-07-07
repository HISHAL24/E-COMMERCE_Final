"""Custom exception definitions with logging."""

import logging

logger = logging.getLogger(__name__)

class validationerror(Exception):
    """
    Exception raised for validation-related errors.

    :param message: The error message describing the validation issue.
    """

    def __init__(self, message: str) -> None:
        full_message = f"Validation Error: {message}"
        logger.error(full_message)
        super().__init__(full_message)

class databaseconnectionerror(Exception):
    """
    Exception raised for database connection-related errors.

    :param message: The error message describing the connection issue.
    """

    def __init__(self, message: str) -> None:
        full_message = f"Database Connection Error: {message}"
        logger.error(full_message)
        super().__init__(full_message)

                