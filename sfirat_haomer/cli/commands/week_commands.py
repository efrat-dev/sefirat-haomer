"""
Week-related CLI commands for Sfirat HaOmer
"""

import click
from typing import Dict, Any

from sfirat_haomer import (
    get_omer_days_by_week,
    get_omer_summary_by_sefirah,
)

from exceptions import (
    handle_cli_errors,
)

from ..validators.cli_validators import (
    validate_cli_week_number,
)

from ..formatters.output_formatters import (
    format_omer_day,
)


@click.group()
def week_commands():
    """Week-related commands"""
    pass


@week_commands.command('week')
@click.argument('week_number', type=int)
@click.option('--compact', is_flag=True, help='Compact output format')
@click.pass_context
@handle_cli_errors
def week(ctx, week_number, compact):
    """Get all days for a specific week (1-7)"""
    # Validate week number using our custom validator
    validate_cli_week_number(week_number)
    
    tradition = ctx.obj['tradition']
    
    week_days = get_omer_days_by_week(week_number, tradition=tradition)
    
    if not compact:
        # Show week summary first
        summary = get_omer_summary_by_sefirah(week_number)
        sefirah_info = summary['sefirah']
        
        click.echo(f"📅 Week {week_number} of the Omer")
        click.echo(f"🔮 Sefirah: {sefirah_info.get('hebrew', 'N/A')}")
        click.echo(f"Transliteration: {sefirah_info.get('transliteration', 'N/A')}")
        click.echo(f"English: {sefirah_info.get('english', 'N/A')}")
        click.echo(f"Attribute: {sefirah_info.get('attribute', 'N/A')}")
        click.echo("=" * 60)
    
    for day in week_days:
        if compact:
            click.echo(format_omer_day(day.to_dict(), compact=True))
        else:
            click.echo(format_omer_day(day.to_dict()))
            click.echo("-" * 40)