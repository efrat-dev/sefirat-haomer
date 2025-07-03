"""
Sefirat HaOmer Counter Library
=============================

A comprehensive Python library for calculating and displaying Sefirat HaOmer 
(Counting of the Omer) with support for Hebrew dates, multiple traditions, 
and Kabbalistic Sefirot information.

Basic Usage:
-----------
    from omer_counter import get_omer_text_by_date, get_current_omer_status
    
    # Get today's Omer count
    today_omer = get_current_omer_status()
    
    # Get specific Omer day
    day_33 = get_omer_day_by_number(33)  # Lag BaOmer

Advanced Features:
-----------------
    # Get all 49 days
    all_days = get_all_omer_days()
    
    # Export calendar
    calendar = export_omer_calendar(format_type="json")
    
    # Configure output
    from omer_counter.config import OmerConfig, OutputFormat
    config = OmerConfig(output_format=OutputFormat.DETAILED)

Quick Access:
------------
    from omer_counter import today, day, week
    
    # Get today's Omer
    today_status = today()
    
    # Get specific day
    lag_baomer = day(33)
    
    # Get specific week
    first_week = week(1)

CLI Usage:
---------
    # Command line interface available via cli.py
    # python cli.py today --blessing
    # python cli.py day 33
    # python cli.py week 1
    # python cli.py export --format json
"""

# Core imports from the new modular structure
from .models.omer_day import OmerDay
from .models.sefirah import SefiraInfo
from .models.enums import OmerMonth, OmerTradition
from .calculators.omer_calculator import OmerCalculator
from .services.omer_service import (
    get_omer_text_by_date,
    get_all_omer_days,
    get_omer_days_by_week,
    get_current_omer_status,
    get_omer_day_by_number,
    find_special_omer_days,
    find_omer_day_by_gregorian_range,
    get_omer_summary_by_sefirah
)
from .services.export_service import export_omer_calendar
from .utils.validation import validate_omer_configuration
from .config import get_config, set_config, OmerConfig, OutputFormat, DateFormat

# Additional services that may exist
try:
    from .services.sefirot_service import (
        get_sefirot_attributes,
        get_ana_bekoach_text
    )
except ImportError:
    # If sefirot service doesn't exist, create placeholder functions
    def get_sefirot_attributes(*args, **kwargs):
        return {"error": "Sefirot service not available"}
    
    def get_ana_bekoach_text(*args, **kwargs):
        return {"error": "Ana BeKoach service not available"}

# Try to import CLI-related exceptions if available
try:
    from .exceptions import (
        OmerCLIError,
        OmerCLIArgumentError,
        OmerCLIOutputError,
        OmerCLIFileError,
        handle_cli_errors,
        validate_cli_day_number,
        validate_cli_week_number,
        validate_cli_output_format,
        validate_cli_file_path
    )
    _CLI_AVAILABLE = True
except ImportError:
    _CLI_AVAILABLE = False

# Version info
__version__ = "1.0.0"
__author__ = "Omer Package Team"
__email__ = "info@omer-package.com"
__description__ = "A comprehensive library for Sefirat HaOmer calculations and display"
__url__ = "https://github.com/yourusername/omer-counter"
__license__ = "MIT"

# Package metadata
__package_name__ = "omer-counter"
__python_requires__ = ">=3.7"
__dependencies__ = [
    "convertdate>=2.0.0",
    "typing-extensions>=3.7.4;python_version<'3.8'"
]

# CLI dependencies (optional)
__cli_dependencies__ = [
    "click>=8.0.0"
]

# Define what gets imported with "from omer_counter import *"
__all__ = [
    # Core classes
    "OmerDay",
    "OmerCalculator", 
    "OmerMonth",
    "OmerTradition",
    "SefiraInfo",
    
    # Main functions
    "get_omer_text_by_date",
    "get_current_omer_status", 
    "get_omer_day_by_number",
    "get_all_omer_days",
    
    # Week and range functions
    "get_omer_days_by_week",
    "find_omer_day_by_gregorian_range", 
    "find_special_omer_days",
    
    # Sefirot functions
    "get_sefirot_attributes",
    "get_omer_summary_by_sefirah",
    "get_ana_bekoach_text",
    
    # Utility functions
    "export_omer_calendar",
    "validate_omer_configuration",
    
    # Configuration
    "OmerConfig",
    "OutputFormat", 
    "DateFormat",
    "get_config",
    "set_config",
    
    # Convenience functions
    "today",
    "day", 
    "week",
    
    # Version info
    "__version__"
]

# Add CLI exceptions to __all__ if available
if _CLI_AVAILABLE:
    __all__.extend([
        "OmerCLIError",
        "OmerCLIArgumentError", 
        "OmerCLIOutputError",
        "OmerCLIFileError",
        "handle_cli_errors",
        "validate_cli_day_number",
        "validate_cli_week_number",
        "validate_cli_output_format",
        "validate_cli_file_path"
    ])

# Convenience functions for common use cases
def today(config=None, tradition=None):
    """
    Quick access to today's Omer status
    
    Args:
        config: Optional OmerConfig object
        tradition: Optional OmerTradition enum
        
    Returns:
        dict: Current Omer status
    """
    if tradition is None:
        tradition = OmerTradition.ASHKENAZI
    return get_current_omer_status(config, tradition)


def day(number, config=None, tradition=None):
    """
    Quick access to specific Omer day
    
    Args:
        number: Omer day number (1-49)
        config: Optional OmerConfig object
        tradition: Optional OmerTradition enum
        
    Returns:
        OmerDay: Omer day object or error string
    """
    if tradition is None:
        tradition = OmerTradition.ASHKENAZI
    return get_omer_day_by_number(number, config, tradition)


def week(number, hebrew_year=None, config=None, tradition=None):
    """
    Quick access to specific Omer week
    
    Args:
        number: Week number (1-7)
        hebrew_year: Optional Hebrew year
        config: Optional OmerConfig object
        tradition: Optional OmerTradition enum
        
    Returns:
        list: List of OmerDay objects for the week
    """
    if tradition is None:
        tradition = OmerTradition.ASHKENAZI
    return get_omer_days_by_week(number, hebrew_year, config, tradition)


def is_omer_today():
    """
    Check if today is during the Omer period
    
    Returns:
        bool: True if today is during Omer period
    """
    status = today()
    return status.get("is_omer_period", False)


def days_until_shavuot():
    """
    Get number of days until Shavuot (end of Omer period)
    
    Returns:
        int or None: Days remaining if in Omer period, None otherwise
    """
    status = today()
    if status.get("is_omer_period", False):
        return status.get("days_remaining", None)
    return None


def current_sefirah():
    """
    Get current Sefirah information
    
    Returns:
        dict or None: Current Sefirah info if in Omer period
    """
    status = today()
    if status.get("is_omer_period", False):
        return status.get("sefirah_info", None)
    return None


def format_omer_display(day_data, compact=False):
    """
    Format Omer day data for display (useful for CLI integration)
    
    Args:
        day_data: Dictionary with Omer day data
        compact: Boolean for compact display format
        
    Returns:
        str: Formatted display string
    """
    try:
        if compact:
            return f"Day {day_data['day']}: {day_data['text']}"
        
        lines = []
        lines.append(f"Day {day_data['day']} of the Omer")
        lines.append(f"Week {day_data['week']}, Day {day_data['day_of_week']}")
        lines.append("")
        lines.append(f"Hebrew: {day_data['text']}")
        
        if day_data.get('transliteration'):
            lines.append(f"Transliteration: {day_data['transliteration']}")
        
        if day_data.get('english_translation'):
            lines.append(f"English: {day_data['english_translation']}")
        
        return "\n".join(lines)
        
    except KeyError as e:
        return f"Error formatting Omer day: Missing field {e}"
    except Exception as e:
        return f"Error formatting Omer day: {str(e)}"


def get_cli_status():
    """
    Check if CLI dependencies are available
    
    Returns:
        dict: Status of CLI availability
    """
    status = {
        "cli_available": _CLI_AVAILABLE,
        "exceptions_available": _CLI_AVAILABLE,
        "click_available": False
    }
    
    try:
        import click
        status["click_available"] = True
    except ImportError:
        pass
    
    return status


def check_cli_setup():
    """
    Check if CLI is properly set up and provide setup instructions
    
    Returns:
        dict: Setup status and instructions
    """
    status = get_cli_status()
    
    result = {
        "ready": False,
        "missing_dependencies": [],
        "instructions": []
    }
    
    if not status["click_available"]:
        result["missing_dependencies"].append("click")
        result["instructions"].append("Install click: pip install click>=8.0.0")
    
    if not status["exceptions_available"]:
        result["missing_dependencies"].append("exceptions module")
        result["instructions"].append("Ensure exceptions.py is in the same directory as cli.py")
    
    result["ready"] = len(result["missing_dependencies"]) == 0
    
    if result["ready"]:
        result["instructions"].append("CLI is ready to use: python cli.py --help")
    
    return result


# Add new convenience functions to __all__
__all__.extend([
    "is_omer_today",
    "days_until_shavuot", 
    "current_sefirah",
    "format_omer_display",
    "get_cli_status",
    "check_cli_setup"
])

# Optional: Validate configuration on import with better error handling
def _validate_on_import():
    """Validate configuration on import"""
    try:
        validation_errors = validate_omer_configuration()
        if validation_errors:
            import warnings
            warnings.warn(
                f"Omer Counter configuration validation found issues: {validation_errors}",
                UserWarning,
                stacklevel=2
            )
    except ImportError:
        # If dependencies are missing, warn but don't fail
        import warnings
        warnings.warn(
            "Some dependencies may be missing. Please install with: pip install omer-counter[full]",
            UserWarning,
            stacklevel=2
        )
    except Exception as e:
        # Don't fail import if validation fails
        import warnings
        warnings.warn(
            f"Configuration validation failed: {e}",
            UserWarning,
            stacklevel=2
        )

# Run validation
_validate_on_import()

# Package-level constants that might be useful
OMER_PERIOD_DAYS = 49
OMER_WEEKS = 7
SEFIROT_COUNT = 7

# CLI-related constants
CLI_SUPPORTED_FORMATS = ['json', 'text', 'simple', 'detailed', 'compact']
CLI_SUPPORTED_TRADITIONS = ['ashkenazi', 'sefardi', 'chassidic']
CLI_SUPPORTED_DATE_FORMATS = ['hebrew', 'gregorian', 'both', 'iso']

# Export constants
__all__.extend([
    "OMER_PERIOD_DAYS",
    "OMER_WEEKS", 
    "SEFIROT_COUNT",
    "CLI_SUPPORTED_FORMATS",
    "CLI_SUPPORTED_TRADITIONS",
    "CLI_SUPPORTED_DATE_FORMATS"
])