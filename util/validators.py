"""
Utility module for input validation function
"""

from datetime import datetime
import re


def validate_date(prompt: str) -> str:
    """
    Prompt the user for a date input in YYYY-MM-DD format and validate it.

    Args:
        prompt (str): The prompt message to display to the user.

    Returns:
        str: A valid date string in YYYY-MM-DD format.
    """

    while True:
        date_input = input(prompt).strip()
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")


def validate_int(prompt: str) -> int:
    """
    Prompt the user for an integer input and validate it.

    Args:
        prompt (str): The prompt message to display to the user.

    Returns:
        int: A valid integer input.
    """

    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def validate_alpha_string(prompt: str, field_name: str = "Field") -> str:
    """
    Prompt the user for an alphabetic string and validate it.

    Args:
        prompt (str): The prompt message to display to the user.
        field_name (str, optional): The name of the field for display in error messages. Defaults to "Field".

    Returns:
        str: A valid alphabetic string input.
    """


    while True:
        value = input(prompt).strip()
        if not value:
            print(f"{field_name} cannot be empty.")
        elif not re.match(r'^[A-Za-z ]+$', value):
            print(f"{field_name} must contain only letters .")
        else:
            return value

def validate_status(prompt: str) -> str:
    """
    Prompt the user to enter a status and validate it against allowed values.

    Args:
        prompt (str): The prompt message to display to the user.

    Returns:
        str: A valid status value (active, inactive, upcoming, expired).
    """

    valid_status = ['active', 'inactive', 'upcoming', 'expired']
    while True:
        status = input(prompt).strip().lower()
        if status in valid_status:
            return status
        else:
            print(f"Status must be one of: {', '.join(valid_status)}")



