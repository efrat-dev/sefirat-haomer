"""
CLI-specific exceptions for the Sefirat HaOmer package.
"""

from typing import Optional, List
from functools import wraps
import click
from .base import OmerBaseException, OmerErrorCategory
from .validation_exceptions import OmerOutOfRangeError, OmerValidationError
from .date_exceptions import OmerDateError, OmerNotInPeriodError
from .config_exceptions import OmerConfigurationError, OmerFormatError


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