"""
Domain-specific exceptions for the Sefirat HaOmer package.
"""

from typing import Optional, List
from .base import OmerBaseException, OmerErrorCategory


class OmerTraditionError(OmerBaseException):
    """Exception raised for tradition-related errors"""
    
    def __init__(
        self, 
        message: str,
        tradition: Optional[str] = None,
        available_traditions: Optional[List[str]] = None
    ):
        super().__init__(
            message,
            OmerErrorCategory.TRADITION_ERROR,
            "שגיאה במסורת",
            "TRADITION_ERROR"
        )
        self.tradition = tradition
        self.available_traditions = available_traditions or []
        if tradition:
            self.details["tradition"] = tradition
        if self.available_traditions:
            self.details["available_traditions"] = self.available_traditions


class OmerSefiraError(OmerBaseException):
    """Exception raised for Sefirah-related errors"""
    
    def __init__(
        self, 
        message: str,
        sefirah_week: Optional[int] = None,
        sefirah_day: Optional[int] = None,
        sefirah_name: Optional[str] = None
    ):
        super().__init__(
            message,
            OmerErrorCategory.SEFIRAH_ERROR,
            "שגיאה בספירות",
            "SEFIRAH_ERROR"
        )
        self.sefirah_week = sefirah_week
        self.sefirah_day = sefirah_day
        self.sefirah_name = sefirah_name
        if sefirah_week:
            self.details["sefirah_week"] = sefirah_week
        if sefirah_day:
            self.details["sefirah_day"] = sefirah_day
        if sefirah_name:
            self.details["sefirah_name"] = sefirah_name


class OmerPrayerError(OmerBaseException):
    """Exception raised for prayer-related errors"""
    
    def __init__(
        self, 
        message: str,
        prayer_type: Optional[str] = None
    ):
        super().__init__(
            message,
            OmerErrorCategory.PRAYER_ERROR,
            "שגיאה בתפילה",
            "PRAYER_ERROR"
        )
        self.prayer_type = prayer_type
        if prayer_type:
            self.details["prayer_type"] = prayer_type


class OmerLagBaOmerError(OmerBaseException):
    """Exception for Lag BaOmer specific errors"""
    
    def __init__(self, message: str):
        super().__init__(
            message,
            OmerErrorCategory.SEFIRAH_ERROR,
            "שגיאה בל\"ג בעומר",
            "LAG_BAOMER_ERROR"
        )


class OmerPesachSheniError(OmerBaseException):
    """Exception for Pesach Sheni specific errors"""
    
    def __init__(self, message: str):
        super().__init__(
            message,
            OmerErrorCategory.SEFIRAH_ERROR,
            "שגיאה בפסח שני",
            "PESACH_SHENI_ERROR"
        )


class OmerYomHaZikaronError(OmerBaseException):
    """Exception for Yom HaZikaron specific errors"""
    
    def __init__(self, message: str):
        super().__init__(
            message,
            OmerErrorCategory.SEFIRAH_ERROR,
            "שגיאה ביום הזיכרון",
            "YOM_HAZIKARON_ERROR"
        )


class OmerYomHaAtzmauthError(OmerBaseException):
    """Exception for Yom Ha'Atzmauth specific errors"""
    
    def __init__(self, message: str):
        super().__init__(
            message,
            OmerErrorCategory.SEFIRAH_ERROR,
            "שגיאה ביום העצמאות",
            "YOM_HAATZMAUTH_ERROR"
        )