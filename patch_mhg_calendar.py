import pandas as pd
from sysdata.csv.csv_roll_calendars import csvRollCalendarData
from sysproduction.data.prices import diagPrices

diag_prices = diagPrices()
r = csvRollCalendarData()
cal = r.get_roll_calendar('COPPER-micro')

# Fill backward any empty carry contract fields missing from PySystemTrade's generation algorithm
cal['carry_contract'] = cal['carry_contract'].fillna(method='bfill')
# In case extreme ends don't backfill, forward fill them
cal['carry_contract'] = cal['carry_contract'].fillna(method='ffill')

# Verify and override the broken calendar into the CSV database
print("Sanitized Calendar Head:\n", cal.head())

# Output
r.add_roll_calendar('COPPER-micro', cal, ignore_duplication=True)
print("Saved patched roll calendar for COPPER-micro!")
