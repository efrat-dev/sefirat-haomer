from sfirat_haomer import get_omer_text_by_date

print(get_omer_text_by_date())  # Today
print(get_omer_text_by_date((18, "Iyyar")))  # Hebrew date
print(get_omer_text_by_date((30, "Nisan")))  # Hebrew date
import datetime
print(get_omer_text_by_date(datetime.date(2025, 5, 14)))  # Gregorian
