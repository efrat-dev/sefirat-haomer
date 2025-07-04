"""
Date-related exceptions for the Sefirat HaOmer package.
"""

from typing import Optional, Union
from datetime import date
from .base import OmerBaseException, OmerErrorCategory


class OmerDateError(OmerBaseException):
    """Exception raised for date-related errors in Omer calculations"""
    
    def __init__(
        self, 
        message: str, 
        date_value: Optional[Union[date, tuple]] = None,
        hebrew_message: Optional[str] = None
    ):
        super().__init__(
            message, 
            OmerErrorCategory.DATE_ERROR,
            hebrew_message,
            "DATE_ERROR"
        )
        self.date_value = date_value
        if date_value:
            self.details["date_value"] = str(date_value)


class OmerNotInPeriodError(OmerBaseException):
    """Exception raised when date is not within the Omer counting period"""
    
    def __init__(
        self, 
        date_value: Union[date, tuple],
        message: Optional[str] = None
    ):
        if message is None:
            message = f"Date {date_value} is not within the Sefirat HaOmer period."
        
        hebrew_message = f"התאריך {date_value} אינו בתוך תקופת ספירת העומר."
        
        super().__init__(
            message,
            OmerErrorCategory.DATE_ERROR,
            hebrew_message,
            "NOT_IN_PERIOD"
        )
        self.date_value = date_value
        self.details["date_value"] = str(date_value)


class OmerInvalidHebrewDateError(OmerBaseException):
    """Exception raised for invalid Hebrew date inputs"""
    
    def __init__(
        self, 
        day: int, 
        month: str,
        reason: Optional[str] = None
    ):
        base_message = f"Invalid Hebrew date: {day} {month}"
        if reason:
            base_message += f" ({reason})"
        
        hebrew_message = f"תאריך עברי לא תקין: {day} {month}"
        if reason:
            hebrew_message += f" ({reason})"
        
        super().__init__(
            base_message,
            OmerErrorCategory.DATE_ERROR,
            hebrew_message,
            "INVALID_HEBREW_DATE"
        )
        self.day = day
        self.month = month
        self.reason = reason
        self.details.update({
            "day": day,
            "month": month,
            "reason": reason
        })