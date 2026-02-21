from sysbrokers.IB.config.ib_instrument_config import get_instrument_object_from_config
from syslogging.logger import get_logger

try:
    log = get_logger("")
    for item in ['SP500_micro', 'EUROSTX', 'US5', 'SHATZ', 'GOLD_micro', 'COPPER', 'CRUDE_W_micro', 'CORN', 'SOYBEAN_mini', 'EUR_micro']:
        print(f"Testing {item}")
        get_instrument_object_from_config(item, log=log)
        print(f"Success for {item}")
except Exception as e:
    import traceback
    traceback.print_exc()

