import pandas as pd
from sysdata.csv.csv_roll_calendars import csvRollCalendarData
from sysproduction.data.prices import diagPrices
from dateutil.relativedelta import relativedelta

diag_prices = diagPrices()
r = csvRollCalendarData()
cal = r.get_roll_calendar('COPPER-micro')
all_prices = diag_prices.db_futures_contract_price_data.get_merged_prices_for_instrument('COPPER-micro').final_prices()

# We need to add rows up to the latest contract
available_contracts = sorted(list(all_prices.keys()))

# Micro Copper (MHG) typical rolls: Mar, May, Jul, Sep, Dec
# Or similar to Copper. Just roughly append forward.
last_date = pd.to_datetime(cal.index[-1])

# Extract just the last row values to increment
last_curr = str(cal.iloc[-1]['current_contract'])
last_next = str(cal.iloc[-1]['next_contract'])
last_carry = str(cal.iloc[-1]['carry_contract'])

new_rows = []
from datetime import datetime

# Build pseudo-calendar forward until 2028
current_date = last_date
import copy

import pandas as pd
from sysinit.futures.rollcalendars_from_db_prices_to_csv import build_and_write_roll_calendar

# Re-build calendar directly from the prices downloaded to capture the new ones
print("Attempting to strictly build roll calendar from recent price data...")
build_and_write_roll_calendar('COPPER-micro', write=True, check_before_writing=False)
