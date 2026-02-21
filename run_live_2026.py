import sys
import logging
import time

# PySystemTrade internals
from sysdata.data_blob import dataBlob
from sysproduction.update_multiple_adjusted_prices import update_multiple_adjusted_prices_with_data
from syscontrol.strategy_tools import strategyRunner
from sysproduction.data.control_process import get_list_of_strategies_for_process
from sysexecution.strategies.strategy_order_handling import name_of_main_generator_method
from sysexecution.stack_handler.stack_handler import stackHandler

# PySystemTrade processes run quite a bit of verbose logging through MongoDB and stdout.
# You can set this to INFO or DEBUG if you want to see everything happening under the hood.
logging.getLogger().setLevel(logging.WARNING)

def run_live_custom_portfolio():
    print("==================================================================")
    print("               PySystemTrade Live 2026 Macro Portfolio            ")
    print("==================================================================")
    print("This script orchestrates the daily trading batch sequentially.")
    print("In full production, these steps are typically run asynchronously ")
    print("and scheduled via cron with the 'run_process' wrapping logic.")
    print("==================================================================\n")
    
    # ----------------------------------------------------------------------
    # 1. Continuous Prices Construction
    # ----------------------------------------------------------------------
    print("[1/4] Calculating continuous back-adjusted prices from IB data...")
    try:
        with dataBlob(log_name="Update-Multiple-Adjusted-Prices") as data:
            update_multiple_adjusted_prices_with_data(data, instrument_code="ALL")
        print("      [SUCCESS] Adjusted prices generated!")
    except Exception as e:
        print(f"      [ERROR] Could not update adjusted prices: {e}")
        sys.exit(1)
        
    # ----------------------------------------------------------------------
    # 2. Run Trading Systems (Optimum Target Generation)
    # ----------------------------------------------------------------------
    print("\n[2/4] Running systems to calculate target positions...")
    try:
        with dataBlob(log_name="Update-System-Backtest") as data:
            strategy = "custom_2026_system"
            
            # Seed the PySystemTrade MongoDB with the 100k account size required for sizing rules
            from sysproduction.data.capital import dataCapital
            capital_db = dataCapital(data)
            capital_db.update_capital_value_for_strategy(strategy, 100000.0)

            # Use explicit runSystemClassic initialized targeting the customized yaml
            from sysproduction.strategy_code.run_system_classic import runSystemClassic
            
            print(f"      -> Executing {strategy} rules...")
            runner = runSystemClassic(data, strategy_name=strategy, backtest_config_filename="private.custom_2026_system.yaml")
            runner.run_backtest()
        print("      [SUCCESS] Expected optimal targets generated!")
    except Exception as e:
        print(f"      [ERROR] Could not run systems: {e}")
        sys.exit(1)
        
    # ----------------------------------------------------------------------
    # 3. Strategy Order Generator (Diff Targets vs Portfolio)
    # ----------------------------------------------------------------------
    print("\n[3/4] Reconciling live portfolio state and generating orders...")
    try:
        with dataBlob(log_name="Update-Strategy-Orders") as data:
            strategy = "custom_2026_system"
            
            # PySystemTrade natively uses this explicit generator for trend systems
            from sysexecution.strategies.classic_buffered_positions import orderGeneratorForBufferedPositions
            
            print(f"      -> Diffing orders for {strategy}...")
            generator = orderGeneratorForBufferedPositions(data, strategy)
            generator.get_and_place_orders()
        print("      [SUCCESS] Order diff generated successfully!")
    except Exception as e:
        print(f"      [ERROR] Could not generate orders: {e}")
        sys.exit(1)

    # ----------------------------------------------------------------------
    # 4. Execute using the Stack Handler to IBkr
    # ----------------------------------------------------------------------
    print("\n[4/4] Invoking PySystemTrade Stack Handler across IB...")
    try:
        with dataBlob(log_name="stack_handler") as data:
            handler = stackHandler(data)
            
            # The exact sequence the background cron loop runs
            print("      -> Identifying any external position breaks...")
            handler.check_external_position_break()
            
            print("      -> Processing instrument targets to contract orders...")
            handler.spawn_children_from_new_instrument_orders()
            handler.generate_force_roll_orders()
            
            print("      -> Pushing orders down to IB API...")
            handler.create_broker_orders_from_contract_orders()
            
            # Give IB API loop a second or two to accept limit/MKT orders
            time.sleep(2)
            
            print("      -> Monitoring fills and completing internal tickets...")
            handler.process_fills_stack()
            handler.handle_completed_orders()
            
        print("      [SUCCESS] Interactive Brokers transmission complete!")
    except Exception as e:
        print(f"      [ERROR] Stack Handler failed: {e}")
        
    print("\n==================================================================")
    print("   Live Execution Script Batch Complete!                          ")
    print("==================================================================")


if __name__ == "__main__":
    run_live_custom_portfolio()
