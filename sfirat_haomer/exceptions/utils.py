"""
Utility functions for Sefirat HaOmer exception handling.
Provides error handling decorators and message localization.
"""

from typing import List, Dict, Any, Optional, Callable, Union
from functools import wraps
import time
import logging
from datetime import datetime
from .base import OmerBaseException, OmerErrorCategory
from .validation_exceptions import OmerValidationError, OmerDataIntegrityError
from .date_exceptions import OmerDateError
from .config_exceptions import OmerFormatError


# Error message templates
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
    "tradition_error": "שגיאה במסורת",
    "cli_error": "שגיאה בממשק הפקודה",
    "cli_argument_error": "שגיאה בפרמטר הפקודה",
    "cli_output_error": "שגיאה בפלט הפקודה",
    "cli_file_error": "שגיאה בקובץ",
    "operation_cancelled": "הפעולה בוטלה על ידי המשתמש",
    "unexpected_error": "שגיאה בלתי צפויה",
    "validation_error": "שגיאה באימות נתונים",
    "type_error": "שגיאה בסוג הנתונים",
    "missing_data": "נתונים חסרים",
    "corrupted_data": "נתונים פגומים",
    "file_not_found": "הקובץ לא נמצא",
    "permission_denied": "אין הרשאה לגשת לקובץ",
    "network_error": "שגיאה ברשת",
    "timeout_error": "תם הזמן הקצוב לפעולה"
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
    "tradition_error": "Tradition error",
    "cli_error": "CLI error",
    "cli_argument_error": "CLI argument error",
    "cli_output_error": "CLI output error",
    "cli_file_error": "CLI file error",
    "operation_cancelled": "Operation cancelled by user",
    "unexpected_error": "Unexpected error",
    "validation_error": "Validation error",
    "type_error": "Type error",
    "missing_data": "Missing data",
    "corrupted_data": "Corrupted data",
    "file_not_found": "File not found",
    "permission_denied": "Permission denied",
    "network_error": "Network error",
    "timeout_error": "Operation timeout"
}


def get_error_message(error_key: str, language: str = "english") -> str:
    """
    Get localized error message.
    
    Args:
        error_key: Key for the error message
        language: Language for the message ("hebrew" or "english")
        
    Returns:
        Localized error message
    """
    if language.lower() in ["hebrew", "he"]:
        return ERROR_MESSAGES_HEBREW.get(error_key, "שגיאה לא ידועה")
    else:
        return ERROR_MESSAGES_ENGLISH.get(error_key, "Unknown error")


def handle_omer_exception(func: Callable) -> Callable:
    """
    Decorator to handle Omer exceptions and provide consistent error formatting.
    
    Args:
        func: Function to wrap with exception handling
        
    Returns:
        Wrapped function with exception handling
    """
    @wraps(func)
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
                from .validation_exceptions import OmerOutOfRangeError
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
        except FileNotFoundError as e:
            from .config_exceptions import OmerFileError
            raise OmerFileError(f"File not found: {str(e)}")
        except PermissionError as e:
            from .config_exceptions import OmerFileError
            raise OmerFileError(f"Permission denied: {str(e)}")
        except Exception as e:
            # Convert any other exception to a generic Omer exception
            raise OmerBaseException(
                f"Unexpected error: {str(e)}",
                category=OmerErrorCategory.VALIDATION_ERROR,
                error_code="UNEXPECTED_ERROR"
            )
    
    return wrapper


def create_error_context(
    function_name: str,
    input_params: Dict[str, Any],
    error: Exception
) -> Dict[str, Any]:
    """
    Create error context for debugging and logging.
    
    Args:
        function_name: Name of the function where error occurred
        input_params: Parameters passed to the function
        error: The exception that occurred
        
    Returns:
        Dictionary containing error context
    """
    context = {
        "function": function_name,
        "input_params": input_params,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "timestamp": datetime.now().isoformat()
    }
    
    if isinstance(error, OmerBaseException):
        context.update({
            "error_category": error.category.value,
            "error_code": error.error_code,
            "hebrew_message": error.hebrew_message,
            "details": error.details
        })
    
    return context


def format_error_for_display(
    error: Exception,
    include_hebrew: bool = False,
    include_details: bool = False
) -> str:
    """
    Format an error for user display.
    
    Args:
        error: The exception to format
        include_hebrew: Whether to include Hebrew translation
        include_details: Whether to include detailed error information
        
    Returns:
        Formatted error string
    """
    if isinstance(error, OmerBaseException):
        message = str(error)
        
        if include_hebrew and error.hebrew_message:
            message += f"\n{error.hebrew_message}"
        
        if include_details and error.details:
            details_str = ", ".join(f"{k}: {v}" for k, v in error.details.items())
            message += f"\nDetails: {details_str}"
        
        return message
    else:
        return str(error)


def validate_error_recovery_params(
    max_retries: int = 3,
    retry_delay: float = 1.0,
    allowed_exceptions: Optional[List[type]] = None
) -> Dict[str, Any]:
    """
    Validate parameters for error recovery mechanisms.
    
    Args:
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retry attempts in seconds
        allowed_exceptions: List of exception types to retry on
        
    Returns:
        Validated parameters dictionary
        
    Raises:
        OmerValidationError: If parameters are invalid
    """
    if not isinstance(max_retries, int) or max_retries < 0:
        raise OmerValidationError(
            "max_retries must be a non-negative integer",
            field_name="max_retries",
            field_value=max_retries,
            expected_type="int"
        )
    
    if not isinstance(retry_delay, (int, float)) or retry_delay < 0:
        raise OmerValidationError(
            "retry_delay must be a non-negative number",
            field_name="retry_delay",
            field_value=retry_delay,
            expected_type="float"
        )
    
    if allowed_exceptions is not None:
        if not isinstance(allowed_exceptions, list):
            raise OmerValidationError(
                "allowed_exceptions must be a list",
                field_name="allowed_exceptions",
                field_value=allowed_exceptions,
                expected_type="list"
            )
        
        for exc_type in allowed_exceptions:
            if not isinstance(exc_type, type) or not issubclass(exc_type, Exception):
                raise OmerValidationError(
                    f"allowed_exceptions must contain exception types, got {type(exc_type)}",
                    field_name="allowed_exceptions",
                    field_value=exc_type
                )
    
    return {
        "max_retries": max_retries,
        "retry_delay": retry_delay,
        "allowed_exceptions": allowed_exceptions or [OmerBaseException]
    }


def retry_on_error(
    max_retries: int = 3,
    retry_delay: float = 1.0,
    allowed_exceptions: Optional[List[type]] = None
) -> Callable:
    """
    Decorator to retry function execution on specific exceptions.
    
    Args:
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retry attempts in seconds
        allowed_exceptions: List of exception types to retry on
        
    Returns:
        Decorator function
    """
    params = validate_error_recovery_params(max_retries, retry_delay, allowed_exceptions)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(params["max_retries"] + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    # Check if this exception type should be retried
                    should_retry = any(
                        isinstance(e, exc_type) for exc_type in params["allowed_exceptions"]
                    )
                    
                    if not should_retry or attempt == params["max_retries"]:
                        raise
                    
                    # Wait before retry
                    time.sleep(params["retry_delay"])
            
            # This should never be reached, but just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def safe_execute(
    func: Callable,
    *args,
    default_return: Any = None,
    log_errors: bool = True,
    reraise_omer_exceptions: bool = True,
    **kwargs
) -> Any:
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        *args: Arguments to pass to function
        default_return: Value to return if function fails
        log_errors: Whether to log errors
        reraise_omer_exceptions: Whether to re-raise Omer exceptions
        **kwargs: Keyword arguments to pass to function
        
    Returns:
        Function result or default_return on error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_errors:
            # Create error context for logging
            context = create_error_context(
                func.__name__,
                {"args": args, "kwargs": kwargs},
                e
            )
            # In a real implementation, this would log to a proper logger
            logging.error(f"Error in {func.__name__}: {e}", extra=context)
        
        if isinstance(e, OmerBaseException) and reraise_omer_exceptions:
            # Re-raise Omer exceptions unless explicitly suppressed
            raise
        
        return default_return


def log_exception_details(
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    logger: Optional[logging.Logger] = None
) -> None:
    """
    Log detailed exception information.
    
    Args:
        error: The exception to log
        context: Additional context information
        logger: Logger instance to use (creates default if None)
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    
    error_info = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "timestamp": datetime.now().isoformat()
    }
    
    if isinstance(error, OmerBaseException):
        error_info.update({
            "error_category": error.category.value,
            "error_code": error.error_code,
            "hebrew_message": error.hebrew_message,
            "details": error.details
        })
    
    if context:
        error_info["context"] = context
    
    logger.error(f"Exception details: {error_info}")


def create_error_summary(
    errors: List[Exception],
    include_counts: bool = True,
    include_messages: bool = False
) -> Dict[str, Any]:
    """
    Create a summary of multiple errors.
    
    Args:
        errors: List of exceptions to summarize
        include_counts: Whether to include error counts by type
        include_messages: Whether to include error messages
        
    Returns:
        Dictionary containing error summary
    """
    summary = {
        "total_errors": len(errors),
        "error_types": {}
    }
    
    if include_counts:
        for error in errors:
            error_type = type(error).__name__
            summary["error_types"][error_type] = summary["error_types"].get(error_type, 0) + 1
    
    if include_messages:
        summary["messages"] = [str(error) for error in errors]
    
    # Add Omer-specific information if present
    omer_errors = [e for e in errors if isinstance(e, OmerBaseException)]
    if omer_errors:
        summary["omer_errors"] = {
            "count": len(omer_errors),
            "categories": {}
        }
        
        for error in omer_errors:
            category = error.category.value
            summary["omer_errors"]["categories"][category] = \
                summary["omer_errors"]["categories"].get(category, 0) + 1
    
    return summary


def batch_validate(
    validators: List[Callable],
    data: Any,
    stop_on_first_error: bool = False
) -> List[Exception]:
    """
    Run multiple validators on data and collect errors.
    
    Args:
        validators: List of validator functions
        data: Data to validate
        stop_on_first_error: Whether to stop after first validation error
        
    Returns:
        List of validation errors
    """
    errors = []
    
    for validator in validators:
        try:
            validator(data)
        except Exception as e:
            errors.append(e)
            if stop_on_first_error:
                break
    
    return errors


def exception_to_dict(error: Exception) -> Dict[str, Any]:
    """
    Convert an exception to a dictionary representation.
    
    Args:
        error: Exception to convert
        
    Returns:
        Dictionary representation of the exception
    """
    if isinstance(error, OmerBaseException):
        return error.to_dict()
    else:
        return {
            "error_type": type(error).__name__,
            "message": str(error),
            "category": "unknown",
            "error_code": None,
            "hebrew_message": None,
            "details": {}
        }


def dict_to_exception(error_dict: Dict[str, Any]) -> Exception:
    """
    Convert a dictionary back to an exception.
    
    Args:
        error_dict: Dictionary representation of an exception
        
    Returns:
        Exception instance
    """
    error_type = error_dict.get("error_type")
    message = error_dict.get("message", "Unknown error")
    
    # Try to recreate the original exception type
    if error_type and error_type.startswith("Omer"):
        try:
            # Import the exception classes from their specific modules
            from .base import OmerBaseException
            from .date_exceptions import OmerDateError
            from .validation_exceptions import OmerValidationError, OmerOutOfRangeError
            from .config_exceptions import OmerConfigurationError
            
            exception_classes = {
                "OmerBaseException": OmerBaseException,
                "OmerDateError": OmerDateError,
                "OmerValidationError": OmerValidationError,
                "OmerOutOfRangeError": OmerOutOfRangeError,
                "OmerConfigurationError": OmerConfigurationError
            }
            
            if error_type in exception_classes:
                exc_class = exception_classes[error_type]
                if error_type == "OmerOutOfRangeError":
                    # Special handling for OmerOutOfRangeError
                    day_number = error_dict.get("details", {}).get("day_number", 0)
                    return exc_class(day_number)
                else:
                    return exc_class(
                        message,
                        hebrew_message=error_dict.get("hebrew_message"),
                        error_code=error_dict.get("error_code"),
                        details=error_dict.get("details", {})
                    )
        except ImportError:
            pass
    
    # Fallback to generic exception
    return Exception(message)


def filter_exceptions_by_type(
    errors: List[Exception],
    exception_types: Union[type, List[type]]
) -> List[Exception]:
    """
    Filter exceptions by type.
    
    Args:
        errors: List of exceptions to filter
        exception_types: Exception type or list of types to filter by
        
    Returns:
        List of exceptions matching the specified types
    """
    if not isinstance(exception_types, list):
        exception_types = [exception_types]
    
    return [
        error for error in errors
        if any(isinstance(error, exc_type) for exc_type in exception_types)
    ]


def group_exceptions_by_category(
    errors: List[Exception]
) -> Dict[str, List[Exception]]:
    """
    Group exceptions by their category.
    
    Args:
        errors: List of exceptions to group
        
    Returns:
        Dictionary mapping categories to lists of exceptions
    """
    grouped = {}
    
    for error in errors:
        if isinstance(error, OmerBaseException):
            category = error.category.value
        else:
            category = "unknown"
        
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(error)
    
    return grouped


def get_error_severity(error: Exception) -> str:
    """
    Determine the severity level of an error.
    
    Args:
        error: Exception to evaluate
        
    Returns:
        Severity level string ('low', 'medium', 'high', 'critical')
    """
    if isinstance(error, OmerBaseException):
        # Map error categories to severity levels
        category_severity = {
            OmerErrorCategory.VALIDATION_ERROR: "medium",
            OmerErrorCategory.DATE_ERROR: "medium",
            OmerErrorCategory.CONFIGURATION_ERROR: "high",
            OmerErrorCategory.DATA_INTEGRITY_ERROR: "high",
            OmerErrorCategory.CALCULATION_ERROR: "high",
            OmerErrorCategory.FORMAT_ERROR: "low",
            OmerErrorCategory.TEMPLATE_ERROR: "low",
            OmerErrorCategory.TRADITION_ERROR: "medium",
            OmerErrorCategory.SEFIRAH_ERROR: "medium",
            OmerErrorCategory.PRAYER_ERROR: "medium"
        }
        
        return category_severity.get(error.category, "medium")
    else:
        # For non-Omer exceptions, provide basic severity assessment
        if isinstance(error, (ValueError, TypeError)):
            return "medium"
        elif isinstance(error, (FileNotFoundError, PermissionError)):
            return "high"
        elif isinstance(error, KeyError):
            return "high"
        else:
            return "medium"


# Export all utility functions
__all__ = [
    "get_error_message",
    "handle_omer_exception",
    "create_error_context",
    "format_error_for_display",
    "validate_error_recovery_params",
    "retry_on_error",
    "safe_execute",
    "log_exception_details",
    "create_error_summary",
    "batch_validate",
    "exception_to_dict",
    "dict_to_exception",
    "filter_exceptions_by_type",
    "group_exceptions_by_category",
    "get_error_severity",
    "ERROR_MESSAGES_HEBREW",
    "ERROR_MESSAGES_ENGLISH"
]