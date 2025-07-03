#!/usr/bin/env python3
"""
Enhanced CLI for Sfirat HaOmer with comprehensive error handling
Usage: python cli.py [OPTIONS]
"""

import click
import datetime
import json
import os
from typing import Optional, List, Dict, Any

from sfirat_haomer import (
    get_omer_text_by_date, 
    get_current_omer_status,
    get_omer_day_by_number,
    get_all_omer_days,
    get_omer_days_by_week,
    find_special_omer_days,
    find_omer_day_by_gregorian_range,
    get_omer_summary_by_sefirah,
    export_omer_calendar,
    validate_omer_configuration,
    get_ana_bekoach_text,
    get_sefirot_attributes,
    OmerTradition,
    OmerConfig,
    OutputFormat,
    DateFormat
)

# Import the new error handling system
from exceptions import (
    handle_cli_errors,
    validate_cli_day_number,
    validate_cli_week_number,
    validate_cli_output_format,
    validate_cli_file_path,
    OmerCLIError,
    OmerCLIArgumentError,
    OmerCLIOutputError,
    OmerCLIFileError
)


def format_omer_day(day_data: Dict[str, Any], compact: bool = False) -> str:
    """Format Omer day data for display"""
    try:
        if compact:
            return f"Day {day_data['day']}: {day_data['text']}"
        
        lines = []
        lines.append(f"🗓️  Day {day_data['day']} of the Omer")
        lines.append(f"📅 Week {day_data['week']}, Day {day_data['day_of_week']}")
        lines.append("")
        lines.append(f"Hebrew: {day_data['text']}")
        
        if day_data.get('transliteration'):
            lines.append(f"Transliteration: {day_data['transliteration']}")
        
        if day_data.get('english_translation'):
            lines.append(f"English: {day_data['english_translation']}")
        
        if day_data.get('week_description'):
            lines.append(f"Week Description: {day_data['week_description']}")
        
        if day_data.get('sefirah_info'):
            sefirah = day_data['sefirah_info']
            lines.append("")
            lines.append("🔮 Sefirah Combination:")
            lines.append(f"  Week: {sefirah['week_sefirah'].get('hebrew', 'N/A')}")
            lines.append(f"  Day: {sefirah['day_sefirah'].get('hebrew', 'N/A')}")
            lines.append(f"  Combination: {sefirah['combination']}")
        
        if day_data.get('is_special_day') and day_data.get('special_day_info'):
            lines.append("")
            lines.append("⭐ Special Day:")
            lines.append(f"  {day_data['special_day_info'].get('description', 'Special significance')}")
        
        if day_data.get('hebrew_date'):
            hebrew_day, hebrew_month = day_data['hebrew_date']
            lines.append("")
            lines.append(f"Hebrew Date: {hebrew_day} {hebrew_month}")
        
        if day_data.get('gregorian_date'):
            lines.append(f"Gregorian Date: {day_data['gregorian_date']}")
        
        return "\n".join(lines)
        
    except KeyError as e:
        raise OmerCLIOutputError(f"Missing required field in day data: {e}")
    except Exception as e:
        raise OmerCLIOutputError(f"Error formatting Omer day: {str(e)}")


def display_blessing(blessing_data: Dict[str, str], tradition: str = "ashkenazi") -> None:
    """Display blessing text with error handling"""
    try:
        click.echo("🙏 Blessing for Counting the Omer:")
        click.echo("")
        
        if 'intro' in blessing_data:
            click.echo(f"Intro: {blessing_data['intro']}")
            if 'intro_transliteration' in blessing_data:
                click.echo(f"Transliteration: {blessing_data['intro_transliteration']}")
            if 'intro_english' in blessing_data:
                click.echo(f"English: {blessing_data['intro_english']}")
            click.echo("")
        
        click.echo(f"Hebrew: {blessing_data.get('hebrew', 'N/A')}")
        click.echo(f"Transliteration: {blessing_data.get('transliteration', 'N/A')}")
        click.echo(f"English: {blessing_data.get('english', 'N/A')}")
        
    except Exception as e:
        raise OmerCLIOutputError(f"Error displaying blessing: {str(e)}")


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


@cli.command()
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


@cli.command()
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


@cli.command()
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


@cli.command()
@click.option('--start-date', type=click.DateTime(['%Y-%m-%d']), 
              help='Start date (YYYY-MM-DD)')
@click.option('--end-date', type=click.DateTime(['%Y-%m-%d']), 
              help='End date (YYYY-MM-DD)')
@click.option('--compact', is_flag=True, help='Compact output format')
@click.pass_context
@handle_cli_errors
def range(ctx, start_date, end_date, compact):
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


@cli.command()
@click.pass_context
@handle_cli_errors
def special(ctx):
    """Show all special days during the Omer period"""
    click.echo("⭐ Special Days during Sefirat HaOmer:")
    click.echo("=" * 60)
    
    special_days = find_special_omer_days()
    
    if not special_days:
        click.echo("No special days found.")
        return
    
    for day in special_days:
        day_data = day.to_dict()
        click.echo(f"Day {day_data['day']}: {day_data['special_day_info'].get('name', 'Special Day')}")
        click.echo(f"Description: {day_data['special_day_info'].get('description', 'N/A')}")
        click.echo(f"Hebrew: {day_data['text']}")
        click.echo("-" * 40)


@cli.command()
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


@cli.command()
@handle_cli_errors
def sefirot():
    """Show information about all Sefirot"""
    click.echo("🔮 The Ten Sefirot:")
    click.echo("=" * 60)
    
    sefirot_attrs = get_sefirot_attributes()
    
    for i, sefirah in sefirot_attrs.items():
        click.echo(f"{i}. {sefirah.get('hebrew', 'N/A')}")
        click.echo(f"   Transliteration: {sefirah.get('transliteration', 'N/A')}")
        click.echo(f"   English: {sefirah.get('english', 'N/A')}")
        click.echo(f"   Attribute: {sefirah.get('attribute', 'N/A')}")
        click.echo("")


@cli.command()
@handle_cli_errors
def ana_bekoach():
    """Show the Ana BeKoach prayer"""
    click.echo("🤲 Ana BeKoach Prayer:")
    click.echo("=" * 60)
    
    ana_bekoach_text = get_ana_bekoach_text()
    
    for key, lines in ana_bekoach_text.items():
        click.echo(f"{key.capitalize()}:")
        for line in lines:
            click.echo(f"  {line}")
        click.echo("")


@cli.command()
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


@cli.command()
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


@cli.command()
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


@cli.command()
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


@cli.command()
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


if __name__ == '__main__':
    cli()