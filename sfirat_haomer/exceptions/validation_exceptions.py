"""
Validation exceptions for the Sefirat HaOmer package.
"""

from typing import Optional, Dict, Any, List
from .base import OmerBaseException, OmerErrorCategory


class OmerValidationError(OmerBaseException):
    """Exception raised for general validation errors"""
    
    def __init__(
        self, 
        message: str,
        field_name: Optional[str] = None,
        field_value: Optional[Any] = None,
        expected_type: Optional[str] = None
    ):
        super().__init__(
            message,
            OmerErrorCategory.VALIDATION_ERROR,
            "שגיאה באימות נתונים",
            "VALIDATION_ERROR"
        )
        self.field_name = field_name
        self.field_value = field_value
        self.expected_type = expected_type
        if field_name:
            self.details["field_name"] = field_name
        if field_value is not None:
            self.details["field_value"] = str(field_value)
        if expected_type:
            self.details["expected_type"] = expected_type


class OmerOutOfRangeError(OmerBaseException):
    """Exception raised when Omer day number is out of valid range (1-49)"""
    
    def __init__(
        self, 
        day_number: int,
        min_day: int = 1,
        max_day: int = 49
    ):
        message = f"Omer day {day_number} is out of range. Must be between {min_day} and {max_day}."
        hebrew_message = f"יום הספירה {day_number} אינו בטווח התקין. חייב להיות בין {min_day} ל-{max_day}."
        
        super().__init__(
            message,
            OmerErrorCategory.VALIDATION_ERROR,
            hebrew_message,
            "OUT_OF_RANGE"
        )
        self.day_number = day_number
        self.min_day = min_day
        self.max_day = max_day
        self.details.update({
            "day_number": day_number,
            "min_day": min_day,
            "max_day": max_day
        })


class OmerDataIntegrityError(OmerBaseException):
    """Exception raised when data integrity validation fails"""
    
    def __init__(
        self, 
        message: str,
        missing_data: Optional[List[str]] = None,
        corrupted_data: Optional[List[str]] = None
    ):
        super().__init__(
            message,
            OmerErrorCategory.DATA_INTEGRITY_ERROR,
            "שגיאה בשלמות הנתונים",
            "DATA_INTEGRITY_ERROR"
        )
        self.missing_data = missing_data or []
        self.corrupted_data = corrupted_data or []
        self.details.update({
            "missing_data": self.missing_data,
            "corrupted_data": self.corrupted_data
        })


class OmerCalculationError(OmerBaseException):
    """Exception raised for calculation errors in Omer day computations"""
    
    def __init__(
        self, 
        message: str,
        input_values: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message,
            OmerErrorCategory.CALCULATION_ERROR,
            "שגיאה בחישוב ספירת העומר",
            "CALCULATION_ERROR"
        )
        self.input_values = input_values or {}
        self.details.update(self.input_values)