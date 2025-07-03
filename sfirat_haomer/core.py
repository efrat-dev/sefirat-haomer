import datetime
from typing import Union, Tuple, Optional
from dataclasses import dataclass
from convertdate import hebrew
from .data import OMER_TEXTS, HEBREW_MONTHS, HEBREW_MONTH_LENGTHS


@dataclass
class OmerDay:
    day: int
    text: str


def get_omer_text_by_date(
    date: Union[None, datetime.date, Tuple[int, str]] = None
) -> Union[OmerDay, str]:
    """
    Get Sefirat HaOmer count and text by Hebrew or Gregorian date.
    
    Args:
        date: None (today), datetime.date (Gregorian date), or tuple (day, Hebrew month)
        
    Returns:
        OmerDay object or error message string
    """
    try:
        if date is None:
            today = datetime.date.today()
            try:
                h_year, h_month, h_day = hebrew.from_gregorian(today.year, today.month, today.day)
                return _check_and_get_text(h_day, HEBREW_MONTHS.get(h_month, ""))
            except (ValueError, OverflowError):
                return "Error converting current date to Hebrew calendar."
        
        elif isinstance(date, datetime.date):
            try:
                h_year, h_month, h_day = hebrew.from_gregorian(date.year, date.month, date.day)
                return _check_and_get_text(h_day, HEBREW_MONTHS.get(h_month, ""))
            except (ValueError, OverflowError):
                return "Error converting Gregorian date to Hebrew calendar."
        
        elif isinstance(date, tuple) and len(date) == 2:
            if not isinstance(date[0], int) or not isinstance(date[1], str):
                return "Invalid tuple format. Expected (int, str)."
            
            day, month = date
            month = month.capitalize()
            
            if month not in HEBREW_MONTH_LENGTHS:
                return "Invalid Hebrew month. Expected Nisan, Iyyar, or Sivan."
            
            if not (1 <= day <= HEBREW_MONTH_LENGTHS[month]):
                return f"Invalid day for {month}. Must be between 1 and {HEBREW_MONTH_LENGTHS[month]}."
            
            return _check_and_get_text(day, month)
        
        else:
            return "Invalid input format. Expected None, datetime.date, or (day, month) tuple."
    
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def _check_and_get_text(day: int, month: str) -> Union[OmerDay, str]:
    """Check if date is within Omer period and return appropriate text."""
    if not month:
        return "Invalid Hebrew month."
    
    month = month.capitalize()
    
    # Define the Omer period ranges
    omer_ranges = {
        "Nisan": range(16, 31),  # 16-30 Nisan
        "Iyyar": range(1, 30),   # 1-29 Iyyar  
        "Sivan": range(1, 6)     # 1-5 Sivan
    }
    
    if month not in omer_ranges:
        return "This Hebrew date is outside the Sefirat HaOmer period."
    
    if day not in omer_ranges[month]:
        return "This date is not within the Sefirat HaOmer period."
    
    try:
        omer_day = _calculate_omer_day(day, month)
        if omer_day < 1 or omer_day > 49:
            return f"Invalid Omer day calculated: {omer_day}."
        
        text = OMER_TEXTS.get(omer_day, f"Missing Omer text for day {omer_day}.")
        return OmerDay(day=omer_day, text=text)
    
    except ValueError as e:
        return str(e)


def _calculate_omer_day(day: int, month: str) -> int:
    """Calculate the Omer day number based on Hebrew date."""
    if month == "Nisan":
        # Nisan 16 = Day 1, Nisan 17 = Day 2, ..., Nisan 30 = Day 15
        return day - 15
    elif month == "Iyyar":
        # Iyyar 1 = Day 16, Iyyar 2 = Day 17, ..., Iyyar 29 = Day 44
        return 15 + day
    elif month == "Sivan":
        # Sivan 1 = Day 45, Sivan 2 = Day 46, ..., Sivan 5 = Day 49
        return 44 + day
    else:
        raise ValueError(f"Invalid Hebrew month for Omer calculation: {month}")


# Optional: Add a helper function to get all Omer days for a year
def get_all_omer_days(hebrew_year: Optional[int] = None) -> list[OmerDay]:
    """Get all 49 Omer days for a given Hebrew year."""
    if hebrew_year is None:
        today = datetime.date.today()
        hebrew_year, _, _ = hebrew.from_gregorian(today.year, today.month, today.day)
    
    omer_days = []
    
    # Add Nisan days (16-30)
    for day in range(16, 31):
        omer_day = _calculate_omer_day(day, "Nisan")
        text = OMER_TEXTS.get(omer_day, f"Missing text for day {omer_day}")
        omer_days.append(OmerDay(day=omer_day, text=text))
    
    # Add Iyyar days (1-29)
    for day in range(1, 30):
        omer_day = _calculate_omer_day(day, "Iyyar")
        text = OMER_TEXTS.get(omer_day, f"Missing text for day {omer_day}")
        omer_days.append(OmerDay(day=omer_day, text=text))
    
    # Add Sivan days (1-5)
    for day in range(1, 6):
        omer_day = _calculate_omer_day(day, "Sivan")
        text = OMER_TEXTS.get(omer_day, f"Missing text for day {omer_day}")
        omer_days.append(OmerDay(day=omer_day, text=text))
    
    return omer_days
