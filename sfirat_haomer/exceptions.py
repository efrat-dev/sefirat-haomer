# exceptions.py
"""
Custom exceptions for the Sefirat HaOmer package.
Provides specialized error handling for various aspects of Omer counting,
configuration, date calculations, and data validation.
"""

from typing import Optional, Dict, Any, Union, List
from datetime import date
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


class OmerConfigurationError(OmerBaseException):
    """Exception raised for configuration-related errors"""
    
    def __init__(
        self, 
        message: str,
        config_field: Optional[str] = None,
        config_value: Optional[Any] = None
    ):
        super().__init__(
            message,
            OmerErrorCategory.CONFIGURATION_ERROR,
            None,
            "CONFIG_ERROR"
        )
        self.config_field = config_field
        self.config_value = config_value
        if config_field:
            self.details["config_field"] = config_field
        if config_value is not None:
            self.details["config_value"] = str(config_value)


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


class OmerFormatError(OmerBaseException):
    """Exception raised for formatting and output errors"""
    
    def __init__(
        self, 
        message: str,
        format_type: Optional[str] = None,
        template_error: Optional[str] = None
    ):
        super().__init__(
            message,
            OmerErrorCategory.FORMAT_ERROR,
            "שגיאה בעיצוב הפלט",
            "FORMAT_ERROR"
        )
        self.format_type = format_type
        self.template_error = template_error
        if format_type:
            self.details["format_type"] = format_type
        if template_error:
            self.details["template_error"] = template_error


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


class OmerTemplateError(OmerBaseException):
    """Exception raised for template formatting errors"""
    
    def __init__(
        self, 
        message: str,
        template_name: Optional[str] = None,
        missing_variables: Optional[List[str]] = None
    ):
        super().__init__(
            message,
            OmerErrorCategory.TEMPLATE_ERROR,
            "שגיאה בתבנית הפלט",
            "TEMPLATE_ERROR"
        )
        self.template_name = template_name
        self.missing_variables = missing_variables or []
        if template_name:
            self.details["template_name"] = template_name
        if self.missing_variables:
            self.details["missing_variables"] = self.missing_variables


class OmerFileError(OmerBaseException):
    """Exception raised for file-related errors (config loading/saving)"""
    
    def __init__(
        self, 
        message: str,
        file_path: Optional[str] = None,
        operation: Optional[str] = None
    ):
        super().__init__(
            message,
            OmerErrorCategory.CONFIGURATION_ERROR,
            "שגיאה בקובץ",
            "FILE_ERROR"
        )
        self.file_path = file_path
        self.operation = operation
        if file_path:
            self.details["file_path"] = file_path
        if operation:
            self.details["operation"] = operation


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


# Utility functions for exception handling
def validate_omer_day_number(day_number: int) -> None:
    """Validate Omer day number and raise appropriate exception if invalid"""
    if not isinstance(day_number, int):
        raise OmerValidationError(
            f"Omer day number must be an integer, got {type(day_number).__name__}",
            field_name="day_number",
            field_value=day_number,
            expected_type="int"
        )
    
    if not (1 <= day_number <= 49):
        raise OmerOutOfRangeError(day_number)


def validate_hebrew_month(month: str) -> None:
    """Validate Hebrew month name for Omer period"""
    valid_months = {"Nisan", "Iyyar", "Sivan", "nisan", "iyyar", "sivan"}
    if month not in valid_months:
        raise OmerInvalidHebrewDateError(
            0, month, 
            f"Invalid Hebrew month. Expected one of: {', '.join(sorted(valid_months))}"
        )


def validate_hebrew_day(day: int, month: str) -> None:
    """Validate Hebrew day for given month"""
    if not isinstance(day, int):
        raise OmerValidationError(
            f"Hebrew day must be an integer, got {type(day).__name__}",
            field_name="day",
            field_value=day,
            expected_type="int"
        )
    
    month_lengths = {
        "Nisan": 30, "nisan": 30,
        "Iyyar": 29, "iyyar": 29,
        "Sivan": 30, "sivan": 30
    }
    
    if month not in month_lengths:
        validate_hebrew_month(month)  # This will raise appropriate exception
    
    max_day = month_lengths[month]
    if not (1 <= day <= max_day):
        raise OmerInvalidHebrewDateError(
            day, month,
            f"Day must be between 1 and {max_day} for {month}"
        )


def validate_sefirah_week(week: int) -> None:
    """Validate Sefirah week number"""
    if not isinstance(week, int):
        raise OmerValidationError(
            f"Sefirah week must be an integer, got {type(week).__name__}",
            field_name="week",
            field_value=week,
            expected_type="int"
        )
    
    if not (1 <= week <= 7):
        raise OmerSefiraError(
            f"Sefirah week {week} is out of range. Must be between 1 and 7.",
            sefirah_week=week
        )


def validate_sefirah_day(day: int) -> None:
    """Validate Sefirah day number within a week"""
    if not isinstance(day, int):
        raise OmerValidationError(
            f"Sefirah day must be an integer, got {type(day).__name__}",
            field_name="day",
            field_value=day,
            expected_type="int"
        )
    
    if not (1 <= day <= 7):
        raise OmerSefiraError(
            f"Sefirah day {day} is out of range. Must be between 1 and 7.",
            sefirah_day=day
        )


def validate_format_template(template_name: str, available_templates: List[str]) -> None:
    """Validate format template name"""
    if template_name not in available_templates:
        raise OmerTemplateError(
            f"Invalid template '{template_name}'. Available templates: {', '.join(available_templates)}",
            template_name=template_name
        )


def validate_tradition(tradition: str, available_traditions: List[str]) -> None:
    """Validate tradition name"""
    if tradition not in available_traditions:
        raise OmerTraditionError(
            f"Invalid tradition '{tradition}'. Available traditions: {', '.join(available_traditions)}",
            tradition=tradition,
            available_traditions=available_traditions
        )


def validate_weekday(weekday: int) -> None:
    """Validate weekday number (0-6)"""
    if not isinstance(weekday, int):
        raise OmerValidationError(
            f"Weekday must be an integer, got {type(weekday).__name__}",
            field_name="weekday",
            field_value=weekday,
            expected_type="int"
        )
    
    if not (0 <= weekday <= 6):
        raise OmerValidationError(
            f"Weekday {weekday} is out of range. Must be between 0 and 6.",
            field_name="weekday",
            field_value=weekday
        )


def handle_omer_exception(func):
    """Decorator to handle Omer exceptions and provide consistent error formatting"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OmerBaseException:
            # Re-raise Omer exceptions as-is
            raise
        except ValueError as e:
            # Convert ValueError to appropriate Omer exception
            error_msg = str(e)
            if "day" in error_msg.lower() and "range" in error_msg.lower():
                raise OmerOutOfRangeError(0)  # Default invalid day
            elif "date" in error_msg.lower():
                raise OmerDateError(error_msg)
            elif "format" in error_msg.lower():
                raise OmerFormatError(error_msg)
            else:
                raise OmerValidationError(error_msg)
        except KeyError as e:
            # Convert KeyError to data integrity error
            raise OmerDataIntegrityError(f"Missing required data: {str(e)}")
        except TypeError as e:
            raise OmerValidationError(f"Type error: {str(e)}")
        except Exception as e:
            # Convert any other exception to a generic Omer exception
            raise OmerBaseException(
                f"Unexpected error: {str(e)}",
                category=OmerErrorCategory.VALIDATION_ERROR,
                error_code="UNEXPECTED_ERROR"
            )
    
    return wrapper


# Error message templates - integrating with data.py ERROR_MESSAGES
ERROR_MESSAGES_HEBREW = {
    "out_of_range": "יום הספירה חייב להיות בין 1 ל-49",
    "invalid_date": "תאריך לא תקין",
    "not_in_period": "התאריך אינו בתוך תקופת ספירת העומר",
    "invalid_month": "חודש עברי לא תקין",
    "config_error": "שגיאה בהגדרות",
    "data_integrity": "שגיאה בשלמות הנתונים",
    "calculation_error": "שגיאה בחישוב",
    "format_error": "שגיאה בעיצוב הפלט",
    "template_error": "שגיאה בתבנית",
    "prayer_error": "שגיאה בתפילה",
    "sefirah_error": "שגיאה בספירות",
    "tradition_error": "שגיאה במסורת"
}

ERROR_MESSAGES_ENGLISH = {
    "out_of_range": "Omer day must be between 1 and 49",
    "invalid_date": "Invalid date",
    "not_in_period": "Date is not within the Omer counting period",
    "invalid_month": "Invalid Hebrew month",
    "config_error": "Configuration error",
    "data_integrity": "Data integrity error",
    "calculation_error": "Calculation error",
    "format_error": "Format error",
    "template_error": "Template error",
    "prayer_error": "Prayer error",
    "sefirah_error": "Sefirah error",
    "tradition_error": "Tradition error"
}


def get_error_message(error_key: str, language: str = "english") -> str:
    """Get localized error message"""
    if language.lower() == "hebrew":
        return ERROR_MESSAGES_HEBREW.get(error_key, "שגיאה לא ידועה")
    else:
        return ERROR_MESSAGES_ENGLISH.get(error_key, "Unknown error")


# Custom exception for specific Omer scenarios
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

# הוספות לקובץ exceptions.py הקיים
# להוסיף בסוף הקובץ לפני __all__

import click
from functools import wraps


class OmerCLIError(OmerBaseException):
    """Exception raised for CLI-specific errors"""
    
    def __init__(
        self, 
        message: str,
        command: Optional[str] = None,
        exit_code: int = 1
    ):
        super().__init__(
            message,
            OmerErrorCategory.VALIDATION_ERROR,
            "שגיאה בממשק הפקודה",
            "CLI_ERROR"
        )
        self.command = command
        self.exit_code = exit_code
        if command:
            self.details["command"] = command
        self.details["exit_code"] = exit_code


class OmerCLIArgumentError(OmerCLIError):
    """Exception raised for CLI argument errors"""
    
    def __init__(
        self, 
        message: str,
        argument: Optional[str] = None,
        expected_type: Optional[str] = None
    ):
        super().__init__(
            message,
            command=argument,
            exit_code=2
        )
        self.argument = argument
        self.expected_type = expected_type
        if argument:
            self.details["argument"] = argument
        if expected_type:
            self.details["expected_type"] = expected_type


class OmerCLIOutputError(OmerCLIError):
    """Exception raised for CLI output formatting errors"""
    
    def __init__(
        self, 
        message: str,
        output_format: Optional[str] = None
    ):
        super().__init__(message, exit_code=3)
        self.output_format = output_format
        if output_format:
            self.details["output_format"] = output_format


class OmerCLIFileError(OmerCLIError):
    """Exception raised for CLI file operations"""
    
    def __init__(
        self, 
        message: str,
        file_path: Optional[str] = None,
        operation: Optional[str] = None
    ):
        super().__init__(message, exit_code=4)
        self.file_path = file_path
        self.operation = operation
        if file_path:
            self.details["file_path"] = file_path
        if operation:
            self.details["operation"] = operation


def handle_cli_errors(func):
    """
    Decorator to handle CLI errors and provide user-friendly output
    Usage: @handle_cli_errors above CLI command functions
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OmerOutOfRangeError as e:
            click.echo(f"❌ {str(e)}", err=True)
            if e.hebrew_message:
                click.echo(f"   {e.hebrew_message}", err=True)
            raise click.ClickException(f"Day {e.day_number} is out of range")
        
        except OmerNotInPeriodError as e:
            click.echo(f"❌ {str(e)}", err=True)
            if e.hebrew_message:
                click.echo(f"   {e.hebrew_message}", err=True)
            raise click.ClickException("Date not in Omer period")
        
        except OmerDateError as e:
            click.echo(f"❌ {str(e)}", err=True)
            if e.hebrew_message:
                click.echo(f"   {e.hebrew_message}", err=True)
            raise click.ClickException("Invalid date")
        
        except OmerValidationError as e:
            click.echo(f"❌ {str(e)}", err=True)
            if e.hebrew_message:
                click.echo(f"   {e.hebrew_message}", err=True)
            if e.field_name:
                click.echo(f"   Field: {e.field_name}", err=True)
            raise click.ClickException("Validation error")
        
        except OmerConfigurationError as e:
            click.echo(f"❌ {str(e)}", err=True)
            if e.config_field:
                click.echo(f"   Configuration field: {e.config_field}", err=True)
            raise click.ClickException("Configuration error")
        
        except OmerFormatError as e:
            click.echo(f"❌ {str(e)}", err=True)
            if e.format_type:
                click.echo(f"   Format type: {e.format_type}", err=True)
            raise click.ClickException("Output formatting error")
        
        except OmerCLIError as e:
            click.echo(f"❌ CLI Error: {str(e)}", err=True)
            if e.hebrew_message:
                click.echo(f"   {e.hebrew_message}", err=True)
            raise click.ClickException(str(e))
        
        except OmerBaseException as e:
            click.echo(f"❌ {str(e)}", err=True)
            if e.hebrew_message:
                click.echo(f"   {e.hebrew_message}", err=True)
            raise click.ClickException("Omer calculation error")
        
        except click.ClickException:
            # Re-raise Click exceptions as-is
            raise
        
        except KeyboardInterrupt:
            click.echo("\n⚠️  Operation cancelled by user", err=True)
            raise click.Abort()
        
        except Exception as e:
            click.echo(f"❌ Unexpected error: {str(e)}", err=True)
            raise click.ClickException(f"Unexpected error: {str(e)}")
    
    return wrapper


def validate_cli_day_number(day_number: int) -> None:
    """Validate day number for CLI with enhanced error messages"""
    if not isinstance(day_number, int):
        raise OmerCLIArgumentError(
            f"Day number must be an integer, got {type(day_number).__name__}",
            argument="day_number",
            expected_type="int"
        )
    
    if not (1 <= day_number <= 49):
        raise OmerOutOfRangeError(day_number)


def validate_cli_week_number(week_number: int) -> None:
    """Validate week number for CLI with enhanced error messages"""
    if not isinstance(week_number, int):
        raise OmerCLIArgumentError(
            f"Week number must be an integer, got {type(week_number).__name__}",
            argument="week_number",
            expected_type="int"
        )
    
    if not (1 <= week_number <= 7):
        raise OmerOutOfRangeError(week_number, 1, 7)


def validate_cli_output_format(output_format: str, valid_formats: List[str]) -> None:
    """Validate output format for CLI"""
    if output_format not in valid_formats:
        raise OmerCLIOutputError(
            f"Invalid output format '{output_format}'. Valid formats: {', '.join(valid_formats)}",
            output_format=output_format
        )


def validate_cli_file_path(file_path: str, operation: str = "read") -> None:
    """Validate file path for CLI operations"""
    import os
    
    if not file_path:
        raise OmerCLIFileError(
            "File path cannot be empty",
            file_path=file_path,
            operation=operation
        )
    
    if operation == "read":
        if not os.path.exists(file_path):
            raise OmerCLIFileError(
                f"File does not exist: {file_path}",
                file_path=file_path,
                operation=operation
            )
        if not os.path.isfile(file_path):
            raise OmerCLIFileError(
                f"Path is not a file: {file_path}",
                file_path=file_path,
                operation=operation
            )
    elif operation == "write":
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            raise OmerCLIFileError(
                f"Directory does not exist: {directory}",
                file_path=file_path,
                operation=operation
            )


# הוספה לרשימת ERROR_MESSAGES_HEBREW
ERROR_MESSAGES_HEBREW.update({
    "cli_error": "שגיאה בממשק הפקודה",
    "cli_argument_error": "שגיאה בפרמטר הפקודה",
    "cli_output_error": "שגיאה בפלט הפקודה",
    "cli_file_error": "שגיאה בקובץ",
    "operation_cancelled": "הפעולה בוטלה על ידי המשתמש"
})

# הוספה לרשימת ERROR_MESSAGES_ENGLISH
ERROR_MESSAGES_ENGLISH.update({
    "cli_error": "CLI error",
    "cli_argument_error": "CLI argument error", 
    "cli_output_error": "CLI output error",
    "cli_file_error": "CLI file error",
    "operation_cancelled": "Operation cancelled by user"
})

# Export all exceptions for easy importing
__all__ = [
    'OmerBaseException',
    'OmerDateError',
    'OmerOutOfRangeError',
    'OmerNotInPeriodError',
    'OmerInvalidHebrewDateError',
    'OmerConfigurationError',
    'OmerDataIntegrityError',
    'OmerCalculationError',
    'OmerFormatError',
    'OmerTraditionError',
    'OmerSefiraError',
    'OmerPrayerError',
    'OmerTemplateError',
    'OmerFileError',
    'OmerValidationError',
    'OmerLagBaOmerError',
    'OmerPesachSheniError',
    'OmerYomHaZikaronError',
    'OmerYomHaAtzmauthError',
    'OmerErrorCategory',
    'validate_omer_day_number',
    'validate_hebrew_month',
    'validate_hebrew_day',
    'validate_sefirah_week',
    'validate_sefirah_day',
    'validate_format_template',
    'validate_tradition',
    'validate_weekday',
    'handle_omer_exception',
    'get_error_message'
]

# הוספה לרשימת __all__
__all__.extend([
    'OmerCLIError',
    'OmerCLIArgumentError',
    'OmerCLIOutputError', 
    'OmerCLIFileError',
    'handle_cli_errors',
    'validate_cli_day_number',
    'validate_cli_week_number',
    'validate_cli_output_format',
    'validate_cli_file_path'
])