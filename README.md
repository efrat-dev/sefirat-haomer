# Sfirat HaOmer

A Python package for calculating and displaying Sefirat HaOmer (Counting of the Omer) texts in Hebrew based on Hebrew or Gregorian dates.

## Installation

```bash
pip install sfirat-haomer
```

## Quick Start

```python
from sfirat_haomer import get_omer_text_by_date
import datetime

# Get today's Omer count
result = get_omer_text_by_date()
if hasattr(result, 'day'):
    print(f"Today is day {result.day} of the Omer")
    print(f"Hebrew text: {result.text}")
else:
    print(result)  # Error message if not during Omer period
```

## Features

- Calculate Omer day from Hebrew dates (Nisan, Iyyar, Sivan)
- Calculate Omer day from Gregorian dates
- Get complete Hebrew text for each day
- Get all 49 days of Sefirat HaOmer
- Comprehensive error handling
- Type hints and documentation

## Usage

### Basic Usage

```python
from sfirat_haomer import get_omer_text_by_date, OmerDay

# Get today's Omer count
today_result = get_omer_text_by_date()

# Get Omer count for specific Hebrew date
hebrew_result = get_omer_text_by_date((16, "Nisan"))  # First day of Omer

# Get Omer count for specific Gregorian date
import datetime
gregorian_result = get_omer_text_by_date(datetime.date(2024, 4, 24))
```

### Working with Results

```python
result = get_omer_text_by_date((16, "Nisan"))

if isinstance(result, OmerDay):
    print(f"Day: {result.day}")
    print(f"Hebrew text: {result.text}")
else:
    print(f"Error: {result}")
```

### Get All Omer Days

```python
from sfirat_haomer import get_all_omer_days

all_days = get_all_omer_days()
for day in all_days:
    print(f"Day {day.day}: {day.text}")
```

### Input Formats

The `get_omer_text_by_date()` function accepts:

1. **None** (default): Uses today's date
2. **datetime.date**: Any Gregorian date
3. **Tuple[int, str]**: Hebrew date as (day, month)
   - Day: 1-30 (depending on month)
   - Month: "Nisan", "Iyyar", or "Sivan"

### Hebrew Date Examples

```python
# Valid Hebrew dates during Omer period
get_omer_text_by_date((16, "Nisan"))  # Day 1
get_omer_text_by_date((30, "Nisan"))  # Day 15
get_omer_text_by_date((1, "Iyyar"))   # Day 16
get_omer_text_by_date((29, "Iyyar"))  # Day 44
get_omer_text_by_date((1, "Sivan"))   # Day 45
get_omer_text_by_date((5, "Sivan"))   # Day 49
```

### Error Handling

The function returns descriptive error messages for invalid inputs:

```python
result = get_omer_text_by_date((15, "Nisan"))  # Before Omer period
# Returns: "This date is not within the Sefirat HaOmer period."

result = get_omer_text_by_date((32, "Nisan"))  # Invalid day
# Returns: "Invalid day for Nisan. Must be between 1 and 30."

result = get_omer_text_by_date((1, "Adar"))    # Wrong month
# Returns: "Invalid Hebrew month. Expected Nisan, Iyyar, or Sivan."
```

## The Omer Period

Sefirat HaOmer is a 49-day period between Passover and Shavut:

- **Starts**: 16th of Nisan (2nd day of Passover)
- **Ends**: 5th of Sivan (day before Shavut)
- **Duration**: 49 days (7 weeks)

### Hebrew Months During Omer

- **Nisan**: Days 16-30 (Omer days 1-15)
- **Iyyar**: Days 1-29 (Omer days 16-44)
- **Sivan**: Days 1-5 (Omer days 45-49)

## Example Output

```
Day 1: הַיּוֹם יוֹם אֶחָד לָעֹמֶר
Day 7: הַיּוֹם שִׁבְעָה יָמִים, שֶׁהֵם שָׁבוּעַ אֶחָד לָעֹמֶר
Day 49: הַיּוֹם תִּשְׁעָה וְאַרְבָּעִים יוֹם, שֶׁהֵם שִׁבְעָה שָׁבוּעוֹת לָעֹמֶר
```

## API Reference

### Classes

#### `OmerDay`

A dataclass representing a day of the Omer.

**Attributes:**
- `day: int` - The Omer day number (1-49)
- `text: str` - The Hebrew text for this day

### Functions

#### `get_omer_text_by_date(date=None)`

Get the Omer count and text for a specific date.

**Parameters:**
- `date` (optional): None, datetime.date, or (day, month) tuple

**Returns:**
- `OmerDay` object if date is within Omer period
- Error message string if date is invalid or outside Omer period

#### `get_all_omer_days(hebrew_year=None)`

Get all 49 days of Sefirat HaOmer.

**Parameters:**
- `hebrew_year` (optional): Hebrew year (uses current year if None)

**Returns:**
- List of `OmerDay` objects

## Running Examples

The package includes comprehensive usage examples:

```bash
python -m sfirat_haomer.usage
```

Or run specific examples:

```python
from sfirat_haomer.usage import example_current_date, example_hebrew_dates

example_current_date()
example_hebrew_dates()
```

## Requirements

- Python 3.8+
- convertdate>=2.4.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Changelog

### Version 1.0.0
- Initial release
- Support for Hebrew and Gregorian date input
- Complete Hebrew text for all 49 days
- Comprehensive error handling
- Type hints and documentation