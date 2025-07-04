"""
Base exception classes for the Sefirat HaOmer package.
"""

from typing import Optional, Dict, Any
from enum import Enum


class OmerErrorCategory(Enum):
    """Categories of Omer-related errors"""
    DATE_ERROR = "date_error"
    VALIDATION_ERROR = "validation_error"
    CONFIGURATION_ERROR = "configuration_error"
    DATA_INTEGRITY_ERROR = "data_integrity_error"
    CALCULATION_ERROR = "calculation_error"
    FORMAT_ERROR = "format_error"
    TRADITION_ERROR = "tradition_error"
    SEFIRAH_ERROR = "sefirah_error"
    PRAYER_ERROR = "prayer_error"
    TEMPLATE_ERROR = "template_error"


class OmerBaseException(Exception):
    """Base exception class for all Omer-related errors"""
    
    def __init__(
        self, 
        message: str, 
        category: OmerErrorCategory = OmerErrorCategory.VALIDATION_ERROR,
        hebrew_message: Optional[str] = None,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.category = category
        self.hebrew_message = hebrew_message
        self.error_code = error_code
        self.details = details or {}
        
    def __str__(self) -> str:
        """String representation of the exception"""
        base_msg = super().__str__()
        if self.hebrew_message:
            return f"{base_msg} | {self.hebrew_message}"
        return base_msg
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for JSON serialization"""
        return {
            "error_type": self.__class__.__name__,
            "category": self.category.value,
            "message": str(self),
            "hebrew_message": self.hebrew_message,
            "error_code": self.error_code,
            "details": self.details
        }