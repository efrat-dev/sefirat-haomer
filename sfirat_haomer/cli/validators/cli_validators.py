"""
CLI validation functions for Sfirat HaOmer
"""

import os
from typing import List, Optional

from exceptions import (
    OmerCLIArgumentError,
    OmerCLIFileError,
)


def validate_cli_day_number(day_number: int) -> None:
    """Validate Omer day number (1-49)"""
    if not isinstance(day_number, int):
        raise OmerCLIArgumentError(
            f"Day number must be an integer, got {type(day_number).__name__}",
            argument="day_number",
            expected_type="int"
        )
    
    if not (1 <= day_number <= 49):
        raise OmerCLIArgumentError(
            f"Day number must be between 1-49, got {day_number}",
            argument="day_number",
            expected_type="int (1-49)"
        )


def validate_cli_week_number(week_number: int) -> None:
    """Validate Omer week number (1-7)"""
    if not isinstance(week_number, int):
        raise OmerCLIArgumentError(
            f"Week number must be an integer, got {type(week_number).__name__}",
            argument="week_number",
            expected_type="int"
        )
    
    if not (1 <= week_number <= 7):
        raise OmerCLIArgumentError(
            f"Week number must be between 1-7, got {week_number}",
            argument="week_number",
            expected_type="int (1-7)"
        )


def validate_cli_output_format(format_value: str, valid_formats: List[str]) -> None:
    """Validate output format"""
    if not isinstance(format_value, str):
        raise OmerCLIArgumentError(
            f"Format must be a string, got {type(format_value).__name__}",
            argument="format",
            expected_type="str"
        )
    
    if format_value not in valid_formats:
        raise OmerCLIArgumentError(
            f"Invalid format: {format_value}",
            argument="format",
            expected_type="one of: " + ", ".join(valid_formats)
        )


def validate_cli_file_path(file_path: str, operation: str = "read") -> None:
    """Validate file path for read/write operations"""
    if not isinstance(file_path, str):
        raise OmerCLIArgumentError(
            f"File path must be a string, got {type(file_path).__name__}",
            argument="file_path",
            expected_type="str"
        )
    
    if not file_path.strip():
        raise OmerCLIArgumentError(
            "File path cannot be empty",
            argument="file_path"
        )
    
    if operation == "read":
        if not os.path.exists(file_path):
            raise OmerCLIFileError(
                f"File does not exist: {file_path}",
                file_path=file_path,
                operation="read"
            )
        
        if not os.path.isfile(file_path):
            raise OmerCLIFileError(
                f"Path is not a file: {file_path}",
                file_path=file_path,
                operation="read"
            )
        
        if not os.access(file_path, os.R_OK):
            raise OmerCLIFileError(
                f"File is not readable: {file_path}",
                file_path=file_path,
                operation="read"
            )
    
    elif operation == "write":
        # Check if directory exists and is writable
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            raise OmerCLIFileError(
                f"Directory does not exist: {dir_path}",
                file_path=file_path,
                operation="write"
            )
        
        # Check if file exists and is writable, or directory is writable
        if os.path.exists(file_path):
            if not os.access(file_path, os.W_OK):
                raise OmerCLIFileError(
                    f"File is not writable: {file_path}",
                    file_path=file_path,
                    operation="write"
                )
        else:
            # Check if directory is writable
            check_dir = dir_path if dir_path else "."
            if not os.access(check_dir, os.W_OK):
                raise OmerCLIFileError(
                    f"Directory is not writable: {check_dir}",
                    file_path=file_path,
                    operation="write"
                )


def validate_cli_hebrew_year(hebrew_year: Optional[int]) -> None:
    """Validate Hebrew year"""
    if hebrew_year is not None:
        if not isinstance(hebrew_year, int):
            raise OmerCLIArgumentError(
                f"Hebrew year must be an integer, got {type(hebrew_year).__name__}",
                argument="hebrew_year",
                expected_type="int"
            )
        
        # Basic validation - Hebrew years should be reasonable
        if hebrew_year < 5000 or hebrew_year > 6000:
            raise OmerCLIArgumentError(
                f"Hebrew year should be between 5000-6000, got {hebrew_year}",
                argument="hebrew_year",
                expected_type="int (5000-6000)"
            )


def validate_cli_tradition(tradition: str) -> None:
    """Validate tradition parameter"""
    valid_traditions = ['ashkenazi', 'sefardi', 'chassidic']
    
    if not isinstance(tradition, str):
        raise OmerCLIArgumentError(
            f"Tradition must be a string, got {type(tradition).__name__}",
            argument="tradition",
            expected_type="str"
        )
    
    if tradition not in valid_traditions:
        raise OmerCLIArgumentError(
            f"Invalid tradition: {tradition}",
            argument="tradition",
            expected_type="one of: " + ", ".join(valid_traditions)
        )


def validate_cli_date_format(date_format: str) -> None:
    """Validate date format parameter"""
    valid_formats = ['hebrew', 'gregorian', 'both', 'iso']
    
    if not isinstance(date_format, str):
        raise OmerCLIArgumentError(
            f"Date format must be a string, got {type(date_format).__name__}",
            argument="date_format",
            expected_type="str"
        )
    
    if date_format not in valid_formats:
        raise OmerCLIArgumentError(
            f"Invalid date format: {date_format}",
            argument="date_format",
            expected_type="one of: " + ", ".join(valid_formats)
        )