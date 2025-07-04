"""
Utility CLI commands for Sfirat HaOmer
"""

import click
import json
from typing import Dict, Any

from sfirat_haomer import (
    export_omer_calendar,
    validate_omer_configuration,
)

from exceptions import (
    handle_cli_errors,
    OmerCLIFileError,
)

from ..validators.cli_validators import (
    validate_cli_output_format,
    validate_cli_file_path,
)


@click.group()
def util_commands():
    """Utility commands"""
    pass


@util_commands.command('export')
@click.option('--format', 'export_format', type=click.Choice(['json', 'text']),
              default='json', help='Export format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--hebrew-year', type=int, help='Hebrew year (default: current year)')
@click.pass_context
@handle_cli_errors
def export(ctx, export_format, output, hebrew_year):
    """Export complete Omer calendar"""
    # Validate export format
    valid_formats = ['json', 'text']
    validate_cli_output_format(export_format, valid_formats)
    
    # Validate output file path if provided
    if output:
        validate_cli_file_path(output, operation="write")
    
    calendar_data = export_omer_calendar(
        hebrew_year=hebrew_year,
        format_type=export_format
    )
    
    if output:
        try:
            with open(output, 'w', encoding='utf-8') as f:
                if export_format == 'json':
                    json.dump(calendar_data, f, ensure_ascii=False, indent=2)
                else:
                    f.write(calendar_data)
            click.echo(f"✅ Calendar exported to {output}")
        except IOError as e:
            raise OmerCLIFileError(
                f"Error writing to file: {str(e)}",
                file_path=output,
                operation="write"
            )
    else:
        if export_format == 'json':
            click.echo(json.dumps(calendar_data, ensure_ascii=False, indent=2))
        else:
            click.echo(calendar_data)


@util_commands.command('validate')
@handle_cli_errors
def validate():
    """Validate Omer configuration and data integrity"""
    click.echo("🔍 Validating Omer configuration...")
    
    errors = validate_omer_configuration()
    
    if not errors:
        click.echo("✅ All validations passed successfully!")
    else:
        click.echo("❌ Validation errors found:")
        for error in errors:
            click.echo(f"  • {error}")
        
        # This is a validation error, not a CLI error
        raise click.ClickException("Configuration validation failed")


@util_commands.command('process-file')
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.pass_context
@handle_cli_errors
def process_file(ctx, input_file, output):
    """Process a file containing Omer data"""
    # Validate input file
    validate_cli_file_path(input_file, operation="read")
    
    # Validate output file if provided
    if output:
        validate_cli_file_path(output, operation="write")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = f.read()
            
        # Process the data (example processing)
        processed_data = f"Processed Omer data from {input_file}\n{data}"
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(processed_data)
            click.echo(f"✅ Processed data saved to {output}")
        else:
            click.echo(processed_data)
            
    except IOError as e:
        raise OmerCLIFileError(
            f"Error processing file: {str(e)}",
            file_path=input_file,
            operation="read"
        )