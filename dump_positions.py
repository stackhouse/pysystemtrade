import logging
logging.getLogger().setLevel(logging.WARNING)

from sysdata.data_blob import dataBlob
from sysproduction.data.positions import diagPositions
from sysproduction.data.optimal_positions import dataOptimalPositions
from sysobjects.production.tradeable_object import instrumentStrategy

def check_positions():
    strategy = "custom_2026_system"
    instruments = [
        'SP500_micro',
        'EUROSTX',
        'US5',
        'SHATZ',
        'GOLD_micro',
        'COPPER',
        'CRUDE_W_micro',
        'CORN',
        'SOYBEAN_mini',
        'EUR_micro'
    ]

    with dataBlob(log_name="Check-Positions") as data:
        print("=== OPTIMAL TARGET POSITIONS ===")
        pos_data = diagPositions(data)
        opt_data = dataOptimalPositions(data)
        
        for inst in instruments:
            try:
                inst_strat = instrumentStrategy(strategy_name=strategy, instrument_code=inst)
                
                # Use standard object for current
                current_pos = pos_data.get_current_position_for_instrument_strategy(inst_strat)
                
                # Use dataOptimalPositions for target
                opt_pos = opt_data.get_current_optimal_position_for_instrument_strategy(inst_strat)
                
                # Format
                opt_val = "None"
                if hasattr(opt_pos, 'position'):
                    opt_val = str(opt_pos.position)
                    
                print(f"{inst:15s} | Optimal Target: {opt_val:8s} | Current DB Holding: {current_pos}")
            except Exception as e:
                print(f"{inst:15s} | Failed to fetch: {e}")


if __name__ == "__main__":
    check_positions()
