import datetime
from typing import Union, Tuple, Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from convertdate import hebrew
from .data import (
    OMER_TEXTS, OMER_TRANSLITERATIONS, OMER_ENGLISH_TRANSLATIONS,
    HEBREW_MONTHS, HEBREW_MONTH_LENGTHS, HEBREW_MONTH_NAMES_HEBREW,
    DAILY_SEFIROT, SEFIROT_ATTRIBUTES, SPECIAL_DAYS,
    OMER_BLESSING, OMER_PRAYER, ANA_BEKOACH,
    HEBREW_WEEKDAYS, CUSTOM_TEXTS, KAVANNOT,
    FORMAT_TEMPLATES, ERROR_MESSAGES, SUCCESS_MESSAGES,
    SPECIAL_PRAYERS, validate_data_integrity
)
from .config import get_config, OmerConfig, OutputFormat, DateFormat


class OmerMonth(Enum):
    """Enum for Hebrew months during Omer period"""
    NISAN = "Nisan"
    IYYAR = "Iyyar"
    SIVAN = "Sivan"


class OmerTradition(Enum):
    """Enum for different Jewish traditions"""
    SEFARDI = "sefardi"
    ASHKENAZI = "ashkenazi"
    CHASSIDIC = "chassidic"


@dataclass
class SefiraInfo:
    """Information about a specific Sefirah combination"""
    week_sefirah: Dict[str, str]
    day_sefirah: Dict[str, str]
    combination: str
    combination_transliteration: str
    combination_english: str
    
    def format_sefirah_text(self, include_transliteration: bool = False, include_english: bool = False) -> str:
        """Format the Sefirah information"""
        parts = [self.combination]
        if include_transliteration:
            parts.append(self.combination_transliteration)
        if include_english:
            parts.append(self.combination_english)
        return " | ".join(parts)


@dataclass
class OmerDay:
    """Represents a day in the Omer counting period"""
    day: int
    text: str
    transliteration: str = ""
    english_translation: str = ""
    hebrew_date: Optional[Tuple[int, str]] = None
    gregorian_date: Optional[datetime.date] = None
    sefirah_info: Optional[SefiraInfo] = None
    is_special_day: bool = False
    special_day_info: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        """Validate day and populate missing information"""
        if not (1 <= self.day <= 49):
            raise ValueError(ERROR_MESSAGES["out_of_range"]["english"])
        
        # Populate missing text information
        if not self.text:
            self.text = OMER_TEXTS.get(self.day, f"Missing text for day {self.day}")
        if not self.transliteration:
            self.transliteration = OMER_TRANSLITERATIONS.get(self.day, "")
        if not self.english_translation:
            self.english_translation = OMER_ENGLISH_TRANSLATIONS.get(self.day, "")
        
        # Populate Sefirah information
        if not self.sefirah_info and self.day in DAILY_SEFIROT:
            sefirah_data = DAILY_SEFIROT[self.day]
            self.sefirah_info = SefiraInfo(**sefirah_data)
        
        # Check for special days
        if self.day in SPECIAL_DAYS:
            self.is_special_day = True
            self.special_day_info = SPECIAL_DAYS[self.day]
    
    @property
    def week(self) -> int:
        """Get the week number (1-7) for this Omer day"""
        return (self.day - 1) // 7 + 1
    
    @property
    def day_of_week(self) -> int:
        """Get the day within the week (1-7) for this Omer day"""
        return (self.day - 1) % 7 + 1
    
    @property
    def is_complete_week(self) -> bool:
        """Check if this day completes a week"""
        return self.day % 7 == 0
    
    @property
    def days_remaining(self) -> int:
        """Get number of days remaining in Omer period"""
        return 49 - self.day
    
    def get_week_description(self, in_hebrew: bool = True) -> str:
        """Get description of weeks and days"""
        if self.day < 7:
            return ""
        
        weeks = self.week - 1 if self.day % 7 == 0 else self.week
        days = self.day_of_week if self.day % 7 != 0 else 7
        
        if in_hebrew:
            if weeks == 1:
                week_text = "שבוע אחד"
            else:
                week_text = f"{weeks} שבועות"
            
            if days == 1:
                day_text = "יום אחד"
            elif days > 1:
                day_text = f"{days} ימים"
            else:
                day_text = ""
            
            if day_text:
                return f"שהם {week_text} ו{day_text}"
            else:
                return f"שהם {week_text}"
        else:
            week_text = "week" if weeks == 1 else "weeks"
            day_text = "day" if days == 1 else "days"
            
            if days > 0:
                return f"which are {weeks} {week_text} and {days} {day_text}"
            else:
                return f"which are {weeks} {week_text}"
    
    def format_output(self, config: Optional[OmerConfig] = None, tradition: OmerTradition = OmerTradition.ASHKENAZI) -> str:
        """Format output according to configuration and tradition"""
        if config is None:
            config = get_config()
        
        # Use format template if available
        if config.output_format == OutputFormat.DETAILED:
            template = FORMAT_TEMPLATES.get("detailed", FORMAT_TEMPLATES["full"])
        elif config.compact_output:
            template = FORMAT_TEMPLATES.get("compact", FORMAT_TEMPLATES["simple"])
        else:
            template = FORMAT_TEMPLATES.get("full", "{hebrew_text}\n{transliteration}\n{english_translation}")
        
        # Prepare format variables
        format_vars = {
            "day_number": self.day,
            "hebrew_text": self.text,
            "transliteration": self.transliteration,
            "english_translation": self.english_translation,
            "sefirah_info": self.sefirah_info.format_sefirah_text(True, True) if self.sefirah_info else "",
            "week_description": self.get_week_description(),
            "special_day_info": self.special_day_info.get("description", "") if self.is_special_day else "",
            "date_info": self._format_date_info(config)
        }
        
        # Add tradition-specific intro if needed
        if tradition != OmerTradition.ASHKENAZI and tradition.value in CUSTOM_TEXTS:
            intro = CUSTOM_TEXTS[tradition.value].get("omer_intro", "")
            if intro:
                format_vars["tradition_intro"] = intro
        
        try:
            return template.format(**format_vars)
        except KeyError:
            # Fallback to simple format if template has issues
            return f"{self.text}\n{self.transliteration}\n{self.english_translation}"
    
    def _format_date_info(self, config: OmerConfig) -> str:
        """Format date information according to configuration"""
        date_parts = []
        
        # Hebrew date
        if config.date_format in [DateFormat.HEBREW_ONLY, DateFormat.BOTH]:
            if self.hebrew_date:
                day, month = self.hebrew_date
                hebrew_month = HEBREW_MONTH_NAMES_HEBREW.get(month, month)
                date_parts.append(f"{day} {hebrew_month}")
        
        # Gregorian date
        if config.date_format in [DateFormat.GREGORIAN_ONLY, DateFormat.BOTH] and self.gregorian_date:
            if config.date_format == DateFormat.ISO:
                date_parts.append(self.gregorian_date.strftime("%Y-%m-%d"))
            else:
                date_parts.append(self.gregorian_date.strftime(config.gregorian_format))
        
        return " / ".join(date_parts)
    
    def get_blessing_text(self, tradition: OmerTradition = OmerTradition.ASHKENAZI) -> Dict[str, str]:
        """Get the blessing text for this day"""
        blessing = OMER_BLESSING.copy()
        
        # Add tradition-specific intro if available
        if tradition.value in CUSTOM_TEXTS:
            intro = CUSTOM_TEXTS[tradition.value].get("omer_intro", "")
            if intro:
                blessing["intro"] = intro
                blessing["intro_transliteration"] = CUSTOM_TEXTS[tradition.value].get("omer_intro_transliteration", "")
                blessing["intro_english"] = CUSTOM_TEXTS[tradition.value].get("omer_intro_english", "")
        
        return blessing
    
    def get_prayer_text(self) -> Dict[str, str]:
        """Get the prayer text said after counting"""
        return OMER_PRAYER.copy()
    
    def get_kavana_text(self) -> Dict[str, str]:
        """Get the Kabbalistic intention text"""
        return KAVANNOT.get("general", {})
    
    def get_special_day_blessing(self) -> Optional[Dict[str, str]]:
        """Get special blessing for special days like Lag BaOmer"""
        if self.is_special_day and self.day == 33:  # Lag BaOmer
            return SPECIAL_PRAYERS.get("lag_baomer", {})
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "day": self.day,
            "text": self.text,
            "transliteration": self.transliteration,
            "english_translation": self.english_translation,
            "week": self.week,
            "day_of_week": self.day_of_week,
            "is_complete_week": self.is_complete_week,
            "days_remaining": self.days_remaining,
            "hebrew_date": self.hebrew_date,
            "gregorian_date": self.gregorian_date.isoformat() if self.gregorian_date else None,
            "sefirah_info": {
                "week_sefirah": self.sefirah_info.week_sefirah,
                "day_sefirah": self.sefirah_info.day_sefirah,
                "combination": self.sefirah_info.combination,
                "combination_transliteration": self.sefirah_info.combination_transliteration,
                "combination_english": self.sefirah_info.combination_english
            } if self.sefirah_info else None,
            "is_special_day": self.is_special_day,
            "special_day_info": self.special_day_info,
            "week_description": self.get_week_description()
        }
    
    def __str__(self) -> str:
        return self.format_output()


class OmerCalculator:
    """Calculator for Omer dates and texts"""
    
    # Define the Omer period ranges
    OMER_RANGES = {
        OmerMonth.NISAN.value: range(16, 31),  # 16-30 Nisan
        OmerMonth.IYYAR.value: range(1, 30),   # 1-29 Iyyar  
        OmerMonth.SIVAN.value: range(1, 6)     # 1-5 Sivan
    }
    
    def __init__(self):
        """Initialize calculator and validate data integrity"""
        validation_errors = validate_data_integrity()
        if validation_errors:
            print(f"Warning: Data integrity issues found: {validation_errors}")
    
    @staticmethod
    def is_omer_period(day: int, month: str) -> bool:
        """Check if a Hebrew date is within the Omer period"""
        month = month.capitalize()
        return month in OmerCalculator.OMER_RANGES and day in OmerCalculator.OMER_RANGES[month]
    
    @staticmethod
    def calculate_omer_day(day: int, month: str) -> int:
        """Calculate the Omer day number based on Hebrew date"""
        month = month.capitalize()
        
        if month == OmerMonth.NISAN.value:
            return day - 15
        elif month == OmerMonth.IYYAR.value:
            return 15 + day
        elif month == OmerMonth.SIVAN.value:
            return 44 + day
        else:
            raise ValueError(f"Invalid Hebrew month for Omer calculation: {month}")
    
    @staticmethod
    def get_hebrew_date_from_omer_day(omer_day: int) -> Tuple[int, str]:
        """Get Hebrew date from Omer day number"""
        if not (1 <= omer_day <= 49):
            raise ValueError(ERROR_MESSAGES["out_of_range"]["english"])
        
        if omer_day <= 15:
            return (omer_day + 15, OmerMonth.NISAN.value)
        elif omer_day <= 44:
            return (omer_day - 15, OmerMonth.IYYAR.value)
        else:
            return (omer_day - 44, OmerMonth.SIVAN.value)
    
    @staticmethod
    def get_weekday_info(date: datetime.date) -> Dict[str, str]:
        """Get Hebrew weekday information for a given date"""
        weekday = date.weekday()
        # Convert Python weekday (0=Monday) to Hebrew weekday (0=Sunday)
        hebrew_weekday = (weekday + 1) % 7
        return HEBREW_WEEKDAYS.get(hebrew_weekday, {})


def get_omer_text_by_date(
    date: Union[None, datetime.date, Tuple[int, str]] = None,
    config: Optional[OmerConfig] = None,
    tradition: OmerTradition = OmerTradition.ASHKENAZI
) -> Union[OmerDay, str]:
    """
    Get Sefirat HaOmer count and text by Hebrew or Gregorian date.
    
    Args:
        date: None (today), datetime.date (Gregorian date), or tuple (day, Hebrew month)
        config: Configuration object (uses global config if None)
        tradition: Jewish tradition for customization
        
    Returns:
        OmerDay object or error message string
    """
    if config is None:
        config = get_config()
    
    try:
        if date is None:
            today = datetime.date.today()
            return _get_omer_from_gregorian(today, config, tradition)
        
        elif isinstance(date, datetime.date):
            return _get_omer_from_gregorian(date, config, tradition)
        
        elif isinstance(date, tuple) and len(date) == 2:
            if not isinstance(date[0], int) or not isinstance(date[1], str):
                return ERROR_MESSAGES["invalid_day"]["english"]
            
            day, month = date
            return _get_omer_from_hebrew(day, month, config, tradition)
        
        else:
            return ERROR_MESSAGES["invalid_day"]["english"]
    
    except Exception as e:
        return ERROR_MESSAGES["date_error"]["english"] + f": {str(e)}"


def _get_omer_from_gregorian(
    date: datetime.date, 
    config: OmerConfig, 
    tradition: OmerTradition
) -> Union[OmerDay, str]:
    """Get Omer day from Gregorian date"""
    try:
        h_year, h_month, h_day = hebrew.from_gregorian(date.year, date.month, date.day)
        month_name = HEBREW_MONTHS.get(h_month, "")
        
        if not month_name:
            return "This date is outside the Sefirat HaOmer period."
        
        return _create_omer_day(h_day, month_name, config, tradition, gregorian_date=date)
    
    except (ValueError, OverflowError):
        return ERROR_MESSAGES["date_error"]["english"]


def _get_omer_from_hebrew(
    day: int, 
    month: str, 
    config: OmerConfig, 
    tradition: OmerTradition
) -> Union[OmerDay, str]:
    """Get Omer day from Hebrew date"""
    month = month.capitalize()
    
    if month not in HEBREW_MONTH_LENGTHS:
        return "Invalid Hebrew month. Expected Nisan, Iyyar, or Sivan."
    
    if not (1 <= day <= HEBREW_MONTH_LENGTHS[month]):
        return f"Invalid day for {month}. Must be between 1 and {HEBREW_MONTH_LENGTHS[month]}."
    
    return _create_omer_day(day, month, config, tradition, hebrew_date=(day, month))


def _create_omer_day(
    day: int, 
    month: str, 
    config: OmerConfig,
    tradition: OmerTradition,
    hebrew_date: Optional[Tuple[int, str]] = None,
    gregorian_date: Optional[datetime.date] = None
) -> Union[OmerDay, str]:
    """Create an OmerDay object with full data integration"""
    if not OmerCalculator.is_omer_period(day, month):
        return "This date is not within the Sefirat HaOmer period."
    
    try:
        omer_day = OmerCalculator.calculate_omer_day(day, month)
        
        # Get all text information
        text = OMER_TEXTS.get(omer_day, f"Missing Omer text for day {omer_day}.")
        transliteration = OMER_TRANSLITERATIONS.get(omer_day, "")
        english_translation = OMER_ENGLISH_TRANSLATIONS.get(omer_day, "")
        
        return OmerDay(
            day=omer_day,
            text=text,
            transliteration=transliteration,
            english_translation=english_translation,
            hebrew_date=hebrew_date or (day, month),
            gregorian_date=gregorian_date
        )
    
    except ValueError as e:
        return str(e)


def get_all_omer_days(
    hebrew_year: Optional[int] = None,
    config: Optional[OmerConfig] = None,
    tradition: OmerTradition = OmerTradition.ASHKENAZI
) -> List[OmerDay]:
    """Get all 49 Omer days for a given Hebrew year"""
    if config is None:
        config = get_config()
    
    if hebrew_year is None:
        today = datetime.date.today()
        hebrew_year, _, _ = hebrew.from_gregorian(today.year, today.month, today.day)
    
    omer_days = []
    
    # Add Nisan days (16-30)
    for day in range(16, 31):
        omer_day = OmerCalculator.calculate_omer_day(day, OmerMonth.NISAN.value)
        omer_days.append(OmerDay(
            day=omer_day,
            text=OMER_TEXTS.get(omer_day, f"Missing text for day {omer_day}"),
            transliteration=OMER_TRANSLITERATIONS.get(omer_day, ""),
            english_translation=OMER_ENGLISH_TRANSLATIONS.get(omer_day, ""),
            hebrew_date=(day, OmerMonth.NISAN.value)
        ))
    
    # Add Iyyar days (1-29)
    for day in range(1, 30):
        omer_day = OmerCalculator.calculate_omer_day(day, OmerMonth.IYYAR.value)
        omer_days.append(OmerDay(
            day=omer_day,
            text=OMER_TEXTS.get(omer_day, f"Missing text for day {omer_day}"),
            transliteration=OMER_TRANSLITERATIONS.get(omer_day, ""),
            english_translation=OMER_ENGLISH_TRANSLATIONS.get(omer_day, ""),
            hebrew_date=(day, OmerMonth.IYYAR.value)
        ))
    
    # Add Sivan days (1-5)
    for day in range(1, 6):
        omer_day = OmerCalculator.calculate_omer_day(day, OmerMonth.SIVAN.value)
        omer_days.append(OmerDay(
            day=omer_day,
            text=OMER_TEXTS.get(omer_day, f"Missing text for day {omer_day}"),
            transliteration=OMER_TRANSLITERATIONS.get(omer_day, ""),
            english_translation=OMER_ENGLISH_TRANSLATIONS.get(omer_day, ""),
            hebrew_date=(day, OmerMonth.SIVAN.value)
        ))
    
    return omer_days


def get_omer_days_by_week(
    week: int, 
    hebrew_year: Optional[int] = None,
    config: Optional[OmerConfig] = None,
    tradition: OmerTradition = OmerTradition.ASHKENAZI
) -> List[OmerDay]:
    """Get all Omer days for a specific week (1-7)"""
    if not (1 <= week <= 7):
        raise ValueError(f"Week must be between 1 and 7, got {week}")
    
    all_days = get_all_omer_days(hebrew_year, config, tradition)
    start_day = (week - 1) * 7 + 1
    end_day = min(week * 7, 49)
    
    return [day for day in all_days if start_day <= day.day <= end_day]


def get_current_omer_status(
    config: Optional[OmerConfig] = None,
    tradition: OmerTradition = OmerTradition.ASHKENAZI
) -> Dict[str, Any]:
    """Get comprehensive status of current Omer period"""
    if config is None:
        config = get_config()
    
    today = datetime.date.today()
    result = get_omer_text_by_date(today, config, tradition)
    
    if isinstance(result, OmerDay):
        status = {
            "is_omer_period": True,
            "day": result.day,
            "text": result.text,
            "transliteration": result.transliteration,
            "english_translation": result.english_translation,
            "formatted_text": result.format_output(config, tradition),
            "week": result.week,
            "day_of_week": result.day_of_week,
            "is_complete_week": result.is_complete_week,
            "hebrew_date": result.hebrew_date,
            "gregorian_date": result.gregorian_date or today,
            "days_remaining": result.days_remaining,
            "week_description": result.get_week_description(),
            "sefirah_info": result.sefirah_info.to_dict() if result.sefirah_info else None,
            "is_special_day": result.is_special_day,
            "special_day_info": result.special_day_info,
            "blessing": result.get_blessing_text(tradition),
            "prayer": result.get_prayer_text(),
            "kavana": result.get_kavana_text(),
            "weekday_info": OmerCalculator.get_weekday_info(today)
        }
        
        # Add special day blessing if applicable
        special_blessing = result.get_special_day_blessing()
        if special_blessing:
            status["special_blessing"] = special_blessing
        
        return status
    else:
        return {
            "is_omer_period": False,
            "message": result
        }


def get_omer_day_by_number(
    day_number: int,
    config: Optional[OmerConfig] = None,
    tradition: OmerTradition = OmerTradition.ASHKENAZI
) -> Union[OmerDay, str]:
    """Get Omer day by day number (1-49)"""
    if not (1 <= day_number <= 49):
        return ERROR_MESSAGES["out_of_range"]["english"]
    
    try:
        hebrew_date = OmerCalculator.get_hebrew_date_from_omer_day(day_number)
        return _create_omer_day(hebrew_date[0], hebrew_date[1], config or get_config(), tradition)
    except Exception as e:
        return ERROR_MESSAGES["date_error"]["english"] + f": {str(e)}"


def get_ana_bekoach_text() -> Dict[str, List[str]]:
    """Get Ana BeKoach prayer text"""
    return ANA_BEKOACH.copy()


def get_sefirot_attributes() -> Dict[int, Dict[str, str]]:
    """Get all Sefirot attributes"""
    return SEFIROT_ATTRIBUTES.copy()


def find_special_omer_days() -> List[OmerDay]:
    """Find all special days during the Omer period"""
    special_days = []
    config = get_config()
    
    for day_num in SPECIAL_DAYS.keys():
        omer_day = get_omer_day_by_number(day_num, config)
        if isinstance(omer_day, OmerDay):
            special_days.append(omer_day)
    
    return special_days


def find_omer_day_by_gregorian_range(
    start_date: datetime.date,
    end_date: datetime.date,
    config: Optional[OmerConfig] = None,
    tradition: OmerTradition = OmerTradition.ASHKENAZI
) -> List[OmerDay]:
    """Find all Omer days within a Gregorian date range"""
    if config is None:
        config = get_config()
    
    omer_days = []
    current_date = start_date
    
    while current_date <= end_date:
        result = get_omer_text_by_date(current_date, config, tradition)
        if isinstance(result, OmerDay):
            omer_days.append(result)
        current_date += datetime.timedelta(days=1)
    
    return omer_days


def get_omer_summary_by_sefirah(
    sefirah_week: int,
    config: Optional[OmerConfig] = None
) -> Dict[str, Any]:
    """Get summary of Omer days for a specific Sefirah week"""
    if not (1 <= sefirah_week <= 7):
        raise ValueError("Sefirah week must be between 1 and 7")
    
    week_sefirah = SEFIROT_ATTRIBUTES.get(sefirah_week, {})
    week_days = get_omer_days_by_week(sefirah_week, config=config)
    
    return {
        "week": sefirah_week,
        "sefirah": week_sefirah,
        "days": [day.to_dict() for day in week_days],
        "total_days": len(week_days)
    }


# Utility functions for advanced features
def export_omer_calendar(
    hebrew_year: Optional[int] = None,
    format_type: str = "json",
    config: Optional[OmerConfig] = None
) -> Union[str, Dict[str, Any]]:
    """Export complete Omer calendar in specified format"""
    all_days = get_all_omer_days(hebrew_year, config)
    
    if format_type.lower() == "json":
        return {
            "hebrew_year": hebrew_year,
            "total_days": len(all_days),
            "days": [day.to_dict() for day in all_days],
            "special_days": [day.to_dict() for day in all_days if day.is_special_day],
            "sefirot_attributes": SEFIROT_ATTRIBUTES
        }
    
    elif format_type.lower() == "text":
        lines = []
        for day in all_days:
            lines.append(day.format_output(config))
            lines.append("-" * 50)
        return "\n".join(lines)
    
    else:
        raise ValueError("Unsupported format type. Use 'json' or 'text'")


def validate_omer_configuration() -> List[str]:
    """Validate the current Omer configuration and data"""
    errors = []
    
    # Check data integrity
    data_errors = validate_data_integrity()
    errors.extend(data_errors)
    
    # Check that we can create all 49 days
    try:
        all_days = get_all_omer_days()
        if len(all_days) != 49:
            errors.append(f"Expected 49 days, got {len(all_days)}")
    except Exception as e:
        errors.append(f"Error creating all Omer days: {str(e)}")
    
    return errors