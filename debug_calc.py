import logging
logging.getLogger().setLevel(logging.INFO)

from sysdata.data_blob import dataBlob
from sysproduction.strategy_code.run_system_classic import runSystemClassic
from sysproduction.data.capital import dataCapital

def debug_generation():
    strategy = "custom_2026_system"
    with dataBlob(log_name="Debug-System") as data:
        # Run the system building process
        runner = runSystemClassic(data, strategy_name=strategy, backtest_config_filename="private.custom_2026_system.yaml")
        
        # Build system in memory
        system = runner.system_method()
        
        # Check Db Capital First
        cap_db = dataCapital(data)
        strat_cap = cap_db.get_current_capital_for_strategy(strategy)
        print(f"=== Capital DB: {strat_cap} ===")
        print(f"=== Notional Capital Config: {system.config.notional_trading_capital} ===")
        
        inst = "SP500_micro"
        print(f"=== Debugging Target for {inst} ===")
        
        try:
            opt_pos = system.portfolio.get_notional_position_before_risk_scaling(inst)
            print(f"Optimal raw position (pre risk scaling): {opt_pos.tail(1) if opt_pos is not None else 'None'}")
            
            sub_portfolio = system.portfolio.get_subsystem_position(inst)
            print(f"Sub-portfolio size (pre-rounding): {sub_portfolio.tail(1) if sub_portfolio is not None else 'None'}")
            
            # Check the buffer configuration:
            actual_pos = system.portfolio.get_actual_position(inst)
            print(f"Actual Position (post-rounding): {actual_pos.tail(1) if actual_pos is not None else 'None'}")
                
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_generation()
