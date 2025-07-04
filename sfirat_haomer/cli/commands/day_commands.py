"""
Day-related CLI commands for Sfirat HaOmer
"""

import click
import datetime
from typing import Dict, Any

from sfirat_haomer import (
    get_omer_text_by_date, 
    get_current_omer_status,
    get_omer_day_by_number,
    find_omer_day_by_gregorian_range,
)

from exceptions import (
    handle_cli_errors,
    OmerCLIError,
    OmerCLIArgumentError,
)

from ..validators.cli_validators import (
    validate_cli_day_number,
)

from ..formatters.output_formatters import (
    format_omer_day,
    display_blessing,
)


@click.group()
def day_commands():
    """Day-related commands"""
    pass


@day_commands.command('today')
@click.option('--blessing', is_flag=True, help='Include blessing text')
@click.option('--prayer', is_flag=True, help='Include prayer text')
@click.option('--sefirah', is_flag=True, help='Show Sefirah information')
@click.pass_context
@handle_cli_errors
def today(ctx, blessing, prayer, sefirah):
    """Get today's Omer count and information"""
    tradition = ctx.obj['tradition']
    
    status = get_current_omer_status(tradition=tradition)
    
    if not status['is_omer_period']:
        click.echo(f"❌ {status['message']}")
        click.echo("We are not currently in the Sefirat HaOmer period.")
        return
    
    click.echo(format_omer_day(status))
    
    if blessing and 'blessing' in status:
        click.echo("\n" + "="*60)
        display_blessing(status['blessing'], tradition.value)
    
    if prayer and 'prayer' in status:
        click.echo("\n" + "="*60)
        click.echo("🤲 Prayer after counting:")
        prayer_text = status['prayer']
        click.echo(f"Hebrew: {prayer_text.get('hebrew', 'N/A')}")
        click.echo(f"Transliteration: {prayer_text.get('transliteration', 'N/A')}")
        click.echo(f"English: {prayer_text.get('english', 'N/A')}")
    
    if sefirah and status.get('sefirah_info'):
        click.echo("\n" + "="*60)
        click.echo("🔮 Detailed Sefirah Information:")
        sefirah_info = status['sefirah_info']
        click.echo(f"Week Sefirah: {sefirah_info['week_sefirah'].get('hebrew', 'N/A')}")
        click.echo(f"Day Sefirah: {sefirah_info['day_sefirah'].get('hebrew', 'N/A')}")
        click.echo(f"Combination: {sefirah_info['combination']}")
        click.echo(f"English: {sefirah_info['combination_english']}")


@day_commands.command('day')
@click.argument('day_number', type=int)
@click.option('--blessing', is_flag=True, help='Include blessing text')
@click.pass_context
@handle_cli_errors
def day(ctx, day_number, blessing):
    """Get information for a specific Omer day (1-49)"""
    # Validate day number using our custom validator
    validate_cli_day_number(day_number)
    
    tradition = ctx.obj['tradition']
    
    result = get_omer_day_by_number(day_number, tradition=tradition)
    
    if isinstance(result, str):
        raise OmerCLIError(f"Error getting day {day_number}: {result}")
    
    click.echo(format_omer_day(result.to_dict()))
    
    if blessing:
        click.echo("\n" + "="*60)
        display_blessing(result.get_blessing_text(tradition))


@day_commands.command('range')
@click.option('--start-date', type=click.DateTime(['%Y-%m-%d']), 
              help='Start date (YYYY-MM-DD)')
@click.option('--end-date', type=click.DateTime(['%Y-%m-%d']), 
              help='End date (YYYY-MM-DD)')
@click.option('--compact', is_flag=True, help='Compact output format')
@click.pass_context
@handle_cli_errors
def range_command(ctx, start_date, end_date, compact):
    """Get Omer days within a date range"""
    if not start_date or not end_date:
        raise OmerCLIArgumentError(
            "Both start-date and end-date are required",
            argument="date_range"
        )
    
    if start_date > end_date:
        raise OmerCLIArgumentError(
            "Start date must be before end date",
            argument="date_range"
        )
    
    tradition = ctx.obj['tradition']
    
    omer_days = find_omer_day_by_gregorian_range(
        start_date.date(), 
        end_date.date(), 
        tradition=tradition
    )
    
    if not omer_days:
        click.echo("❌ No Omer days found in the specified date range")
        return
    
    click.echo(f"📅 Found {len(omer_days)} Omer days between {start_date.date()} and {end_date.date()}")
    click.echo("=" * 60)
    
    for day in omer_days:
        if compact:
            click.echo(format_omer_day(day.to_dict(), compact=True))
        else:
            click.echo(format_omer_day(day.to_dict()))
            click.echo("-" * 40)


@day_commands.command('hebrew-date')
@click.argument('hebrew_day', type=int)
@click.argument('hebrew_month', type=str)
@click.pass_context
@handle_cli_errors
def hebrew_date(ctx, hebrew_day, hebrew_month):
    """Get Omer day by Hebrew date (e.g., 18 Iyyar)"""
    # Validate Hebrew day
    if not (1 <= hebrew_day <= 30):
        raise OmerCLIArgumentError(
            f"Hebrew day must be between 1-30, got {hebrew_day}",
            argument="hebrew_day",
            expected_type="int (1-30)"
        )
    
    # Validate Hebrew month (basic check)
    if not hebrew_month or not isinstance(hebrew_month, str):
        raise OmerCLIArgumentError(
            "Hebrew month must be a non-empty string",
            argument="hebrew_month",
            expected_type="str"
        )
    
    tradition = ctx.obj['tradition']
    
    result = get_omer_text_by_date(
        date=(hebrew_day, hebrew_month),
        tradition=tradition
    )
    
    if isinstance(result, str):
        raise OmerCLIError(f"Error for Hebrew date {hebrew_day} {hebrew_month}: {result}")
    
    click.echo(format_omer_day(result.to_dict()))


@day_commands.command('gregorian-date')
@click.argument('gregorian_date', type=click.DateTime(['%Y-%m-%d']))
@click.pass_context
@handle_cli_errors
def gregorian_date(ctx, gregorian_date):
    """Get Omer day by Gregorian date (YYYY-MM-DD)"""
    tradition = ctx.obj['tradition']
    
    result = get_omer_text_by_date(
        date=gregorian_date.date(),
        tradition=tradition
    )
    
    if isinstance(result, str):
        raise OmerCLIError(f"Error for Gregorian date {gregorian_date.date()}: {result}")
    
    click.echo(format_omer_day(result.to_dict()))


@day_commands.command('status')
@click.pass_context
@handle_cli_errors
def status(ctx):
    """Get comprehensive status of current Omer period"""
    tradition = ctx.obj['tradition']
    
    status = get_current_omer_status(tradition=tradition)
    
    if status['is_omer_period']:
        click.echo("📈 Current Omer Status:")
        click.echo("=" * 60)
        click.echo(format_omer_day(status))
        
        click.echo("\n📊 Additional Information:")
        click.echo(f"Days remaining: {status.get('days_remaining', 'N/A')}")
        click.echo(f"Complete weeks: {status.get('is_complete_week', 'N/A')}")
        
        if status.get('weekday_info'):
            weekday = status['weekday_info']
            click.echo(f"Hebrew weekday: {weekday.get('hebrew', 'N/A')}")
    else:
        click.echo("❌ Not currently in Omer period")
        click.echo(f"Status: {status['message']}")