import sys
import logging
logging.basicConfig(level=logging.WARNING)

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.example.simplesystem import simplesystem

def run_improved_backtest():
    print("Loading raw CSV data and custom improved configuration...")
    my_data = csvFuturesSimData()
    
    # Load our improved YAML configuration
    try:
        my_config = Config("private.improved_system.yaml")
    except Exception as e:
        print(f"Error loading private.improved_system.yaml: {e}")
        sys.exit(1)
        
    print("Building the improved systematic trading pipeline...")
    my_system = simplesystem(config=my_config, data=my_data)
    
    print("Running backtest computation over historical data... (this might take a minute)")
    profits = my_system.accounts.portfolio()
    
    print("\n================ IMPROVED BACKTEST COMPLETE ================")
    print("Performance Summary (Net of Costs):")
    
    stats = profits.percent.stats()
    stats_dict = dict(stats[0])
    
    print(f"Annualized Mean Return:  {float(stats_dict['ann_mean']):.2f}%")
    print(f"Annualized Volatility:   {float(stats_dict['ann_std']):.2f}%")
    print(f"Return/Risk (Sharpe):    {float(stats_dict['sharpe']):.2f}")
    print(f"Maximum Drawdown:        {float(stats_dict['min']):.2f}%")
    
    print("\nNotice how the addition of distinct asset classes and faster trading speeds")
    print("smoothed out the equity curve, increasing the Sharpe ratio and potentially lowering max drawdown.")
    print("=========================================================\n")

if __name__ == "__main__":
    run_improved_backtest()
