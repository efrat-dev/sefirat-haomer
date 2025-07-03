
import datetime
from typing import Union, Tuple
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
    try:
        if date is None:
            today = datetime.date.today()
            h_year, h_month, h_day = hebrew.from_gregorian(today.year, today.month, today.day)
            return _check_and_get_text(h_day, HEBREW_MONTHS.get(h_month, ""))

        elif isinstance(date, datetime.date):
            try:
                datetime.date(date.year, date.month, date.day)
            except ValueError:
                return "Invalid Gregorian date."

            h_year, h_month, h_day = hebrew.from_gregorian(date.year, date.month, date.day)
            return _check_and_get_text(h_day, HEBREW_MONTHS.get(h_month, ""))

        elif isinstance(date, tuple) and isinstance(date[0], int) and isinstance(date[1], str):
            day, month = date
            month = month.capitalize()
            if month not in {"Nisan", "Iyyar", "Sivan"}:
                return "This Hebrew date is outside the Sefirat HaOmer period."
            if not (1 <= day <= HEBREW_MONTH_LENGTHS[month]):
                return "Invalid Hebrew date."
            return _check_and_get_text(day, month)

        else:
            return "Invalid input format."

    except Exception as e:
        return f"Unexpected error: {str(e)}"

def _check_and_get_text(day: int, month: str) -> Union[OmerDay, str]:
    month = month.capitalize()
    omer_range = {
        "Nisan": range(16, 31),
        "Iyyar": range(1, 30),
        "Sivan": range(1, 6)
    }

    if month in omer_range and day in omer_range[month]:
        day_num = _calculate_omer_day(day, month)
        text = OMER_TEXTS.get(day_num, f"Missing Omer text for day {day_num}.")
        return OmerDay(day=day_num, text=text)
    else:
        return "This date is not within the Sefirat HaOmer."

def _calculate_omer_day(day: int, month: str) -> int:
    if month == "Nisan":
        return day - 15
    elif month == "Iyyar":
        return 15 + day
    elif month == "Sivan":
        return 44 + day
    else:
        raise ValueError("Invalid Hebrew month in calculation.")
