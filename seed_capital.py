import logging
logging.getLogger().setLevel(logging.INFO)

from sysdata.data_blob import dataBlob
from sysproduction.data.capital import dataCapital

def seed_capital_for_live_system():
    strategy = "custom_2026_system"
    target_capital = 1000000.0  # Boosted for testing order sizing
    
    with dataBlob(log_name="Seed-Capital") as data:
        cap_db = dataCapital(data)
        
        print(f"Current recorded capital: {cap_db.get_current_capital_for_strategy(strategy)}")
        
        print(f"Setting capital for {strategy} to {target_capital}...")
        cap_db.update_capital_value_for_strategy(strategy, target_capital)
        
        print(f"Done! New capital: {cap_db.get_current_capital_for_strategy(strategy)}")

if __name__ == "__main__":
    seed_capital_for_live_system()
