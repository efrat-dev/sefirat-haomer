"""
Sefirat HaOmer Custom Exceptions Package
Provides specialized error handling for various aspects of Omer counting.
"""

# Core exceptions
from .base import (
    OmerBaseException,
    OmerErrorCategory
)

# Date-related exceptions
from .date_exceptions import (
    OmerDateError,
    OmerNotInPeriodError,
    OmerInvalidHebrewDateError
)

# Validation exceptions
from .validation_exceptions import (
    OmerValidationError,
    OmerOutOfRangeError,
    OmerDataIntegrityError,
    OmerCalculationError
)

# Configuration and format exceptions
from .config_exceptions import (
    OmerConfigurationError,
    OmerFileError,
    OmerFormatError,
    OmerTemplateError
)

# Domain-specific exceptions
from .domain_exceptions import (
    OmerTraditionError,
    OmerSefiraError,
    OmerPrayerError,
    OmerLagBaOmerError,
    OmerPesachSheniError,
    OmerYomHaZikaronError,
    OmerYomHaAtzmauthError
)

# CLI exceptions
from .cli_exceptions import (
    OmerCLIError,
    OmerCLIArgumentError,
    OmerCLIOutputError,
    OmerCLIFileError,
    handle_cli_errors
)

# Validators
from .validators import (
    validate_omer_day_number,
    validate_hebrew_month,
    validate_hebrew_day,
    validate_sefirah_week,
    validate_sefirah_day,
    validate_format_template,
    validate_tradition,
    validate_weekday,
    validate_cli_day_number,
    validate_cli_week_number,
    validate_cli_output_format,
    validate_cli_file_path
)

# Utilities
from .utils import (
    handle_omer_exception,
    get_error_message
)

__all__ = [
    # Core
    'OmerBaseException',
    'OmerErrorCategory',
    
    # Date exceptions
    'OmerDateError',
    'OmerNotInPeriodError',
    'OmerInvalidHebrewDateError',
    
    # Validation exceptions
    'OmerValidationError',
    'OmerOutOfRangeError',
    'OmerDataIntegrityError',
    'OmerCalculationError',
    
    # Configuration exceptions
    'OmerConfigurationError',
    'OmerFileError',
    'OmerFormatError',
    'OmerTemplateError',
    
    # Domain exceptions
    'OmerTraditionError',
    'OmerSefiraError',
    'OmerPrayerError',
    'OmerLagBaOmerError',
    'OmerPesachSheniError',
    'OmerYomHaZikaronError',
    'OmerYomHaAtzmauthError',
    
    # CLI exceptions
    'OmerCLIError',
    'OmerCLIArgumentError',
    'OmerCLIOutputError',
    'OmerCLIFileError',
    'handle_cli_errors',
    
    # Validators
    'validate_omer_day_number',
    'validate_hebrew_month',
    'validate_hebrew_day',
    'validate_sefirah_week',
    'validate_sefirah_day',
    'validate_format_template',
    'validate_tradition',
    'validate_weekday',
    'validate_cli_day_number',
    'validate_cli_week_number',
    'validate_cli_output_format',
    'validate_cli_file_path',
    
    # Utilities
    'handle_omer_exception',
    'get_error_message'
]