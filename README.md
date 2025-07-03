# sfirat-haomer

Get Sefirat HaOmer count and text by Hebrew or Gregorian date.

## Installation

```bash
pip install sfirat-haomer
```

## Usage

```python
from sfirat_haomer import get_omer_text_by_date

print(get_omer_text_by_date())  # today
print(get_omer_text_by_date((18, "Iyyar")))  # Hebrew date
```
