import sys
import logging
logging.basicConfig(level=logging.WARNING)

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.example.simplesystem import simplesystem

def run_custom_backtest():
    print("Loading raw CSV data and custom 2026 configuration...")
    my_data = csvFuturesSimData()
    
    # Load our custom 2026 YAML configuration
    try:
        my_config = Config("private.custom_2026_system.yaml")
    except Exception as e:
        print(f"Error loading private.custom_2026_system.yaml: {e}")
        sys.exit(1)
        
    print("Building the systematic trading pipeline for the 10-instrument 2026 portfolio...")
    my_system = simplesystem(config=my_config, data=my_data)
    
    print("Running backtest computation over historical data... (this might take a minute)")
    profits = my_system.accounts.portfolio()
    
    print("\n================ CUSTOM 2026 BACKTEST COMPLETE ================")
    print("Performance Summary (Net of Costs):")
    
    stats = profits.percent.stats()
    stats_dict = dict(stats[0])
    
    print(f"Annualized Mean Return:  {float(stats_dict['ann_mean']):.2f}%")
    print(f"Annualized Volatility:   {float(stats_dict['ann_std']):.2f}%")
    print(f"Return/Risk (Sharpe):    {float(stats_dict['sharpe']):.2f}")
    print(f"Maximum Drawdown:        {float(stats_dict['min']):.2f}%")
    print("===============================================================\n")

if __name__ == "__main__":
    run_custom_backtest()
