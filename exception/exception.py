""" Custom exception definitions. """

class validationerror(Exception):
    """
    Exception raised for validation-related errors.

    :param message: The error message describing the validation issue.
    """
        
    def __init__(self, message: str) -> None:
        super().__init__(f"validation error : {message}")

class databaseconnectionerror(Exception):
    """
    Exception raised for database connection-related errors.

    :param message: The error message describing the connection issue.
    """
    
    def __init__(self, message: str) -> None:
        super().__init__(f"data connection error : {message}")

        
                