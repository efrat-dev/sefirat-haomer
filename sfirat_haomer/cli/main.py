#!/usr/bin/env python3
"""
Enhanced CLI for Sfirat HaOmer with comprehensive error handling
Usage: python main.py [OPTIONS]
"""

import click
from typing import Dict, Any

from sfirat_haomer import (
    OmerTradition,
    OmerConfig,
    OutputFormat,
    DateFormat
)

# Import the new error handling system
from exceptions import (
    OmerCLIError,
    OmerCLIArgumentError,
)

# Import command groups
from .commands.day_commands import day_commands
from .commands.week_commands import week_commands
from .commands.info_commands import info_commands
from .commands.util_commands import util_commands

# Import validators
from .validators.cli_validators import (
    validate_cli_output_format,
)


@click.group()
@click.option('--tradition', type=click.Choice(['ashkenazi', 'sefardi', 'chassidic']), 
              default='ashkenazi', help='Jewish tradition for customization')
@click.option('--format', 'output_format', type=click.Choice(['simple', 'detailed', 'compact']),
              default='detailed', help='Output format')
@click.option('--dates', type=click.Choice(['hebrew', 'gregorian', 'both', 'iso']),
              default='both', help='Date format to display')
@click.pass_context
def cli(ctx, tradition, output_format, dates):
    """Enhanced CLI for Sfirat HaOmer counting and information"""
    try:
        # Validate input parameters
        valid_traditions = ['ashkenazi', 'sefardi', 'chassidic']
        if tradition not in valid_traditions:
            raise OmerCLIArgumentError(
                f"Invalid tradition: {tradition}",
                argument="tradition",
                expected_type="one of: " + ", ".join(valid_traditions)
            )
        
        valid_formats = ['simple', 'detailed', 'compact']
        validate_cli_output_format(output_format, valid_formats)
        
        valid_dates = ['hebrew', 'gregorian', 'both', 'iso']
        if dates not in valid_dates:
            raise OmerCLIArgumentError(
                f"Invalid date format: {dates}",
                argument="dates",
                expected_type="one of: " + ", ".join(valid_dates)
            )
        
        # Initialize context
        ctx.ensure_object(dict)
        ctx.obj['tradition'] = OmerTradition(tradition)
        ctx.obj['output_format'] = OutputFormat.DETAILED if output_format == 'detailed' else OutputFormat.SIMPLE
        ctx.obj['date_format'] = {
            'hebrew': DateFormat.HEBREW_ONLY,
            'gregorian': DateFormat.GREGORIAN_ONLY,
            'both': DateFormat.BOTH,
            'iso': DateFormat.ISO
        }[dates]
        
    except Exception as e:
        if not isinstance(e, (OmerCLIArgumentError, OmerCLIError)):
            raise OmerCLIError(f"Error initializing CLI: {str(e)}")
        raise


# Register command groups
cli.add_command(day_commands)
cli.add_command(week_commands)
cli.add_command(info_commands)
cli.add_command(util_commands)


if __name__ == '__main__':
    cli()