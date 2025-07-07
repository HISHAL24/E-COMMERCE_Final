"""
Utility module for input validation functions
"""

import logging
from datetime import datetime
import re

logger = logging.getLogger(__name__)

def validate_date(prompt: str) -> str:
    """
    Prompt the user for a date input in YYYY-MM-DD format and validate it.
    """
    while True:
        date_input = input(prompt).strip()
        logger.debug(f"User entered date: {date_input}")
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            logger.info(f"Valid date input received: {date_input}")
            return date_input
        except ValueError:
            logger.warning(f"Invalid date format entered: {date_input}")
            print("Invalid date format. Use YYYY-MM-DD.")

def validate_int(prompt: str) -> int:
    """
    Prompt the user for an integer input and validate it.
    """
    while True:
        user_input = input(prompt).strip()
        logger.debug(f"User entered integer: {user_input}")
        try:
            value = int(user_input)
            logger.info(f"Valid integer input received: {value}")
            return value
        except ValueError:
            logger.warning(f"Invalid integer input: {user_input}")
            print("Invalid input. Please enter a valid integer.")

def validate_alpha_string(prompt: str, field_name: str = "Field") -> str:
    """
    Prompt the user for an alphabetic string and validate it.
    """
    while True:
        value = input(prompt).strip()
        logger.debug(f"User entered string for {field_name}: {value}")
        if not value:
            logger.warning(f"{field_name} is empty.")
            print(f"{field_name} cannot be empty.")
        elif not re.match(r'^[A-Za-z ]+$', value):
            logger.warning(f"{field_name} contains invalid characters: {value}")
            print(f"{field_name} must contain only letters.")
        else:
            logger.info(f"Valid alphabetic string for {field_name}: {value}")
            return value

def validate_status(prompt: str) -> str:
    """
    Prompt the user to enter a status and validate it against allowed values.
    """
    valid_status = ['active', 'inactive', 'upcoming', 'expired']
    while True:
        status = input(prompt).strip().lower()
        logger.debug(f"User entered status: {status}")
        if status in valid_status:
            logger.info(f"Valid status received: {status}")
            return status
        else:
            logger.warning(f"Invalid status entered: {status}")
            print(f"Status must be one of: {', '.join(valid_status)}")

