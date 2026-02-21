import sys
import logging
logging.basicConfig(level=logging.DEBUG)
print("Importing configdata...")
from sysdata.config.configdata import Config
print("Importing csvFuturesSimData...")
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
print("Importing simplesystem...")
from systems.provided.example.simplesystem import simplesystem

def run_starter_backtest():
    print("Loading raw CSV data and custom starter configuration...")
    # Load the mock data that comes with pysystemtrade
    my_data = csvFuturesSimData()
    
    # Load our custom YAML configuration
    try:
        my_config = Config("private.starter_system.yaml")
    except Exception as e:
        print(f"Error loading private.starter_system.yaml: {e}")
        sys.exit(1)
        
    # Build the system
    # This automatically strings together Rules, Scaling, Position Sizing, 
    # Portfolios, and Accounting based on our configuration.
    print("Building the systematic trading pipeline...")
    my_system = simplesystem(config=my_config, data=my_data)
    
    # Run the backtest and calculate profits
    print("Running backtest computation over historical data... (this may take a few seconds)")
    profits = my_system.accounts.portfolio()
    
    print("\n================ BACKTEST COMPLETE ================")
    print("Performance Summary (Net of Costs):")
    
    # Fetch Sharpe, Drawdown, etc.
    stats = profits.percent.stats()
    stats_dict = dict(stats[0])
    
    print(f"Annualized Mean Return:  {float(stats_dict['ann_mean']):.2f}%")
    print(f"Annualized Volatility:   {float(stats_dict['ann_std']):.2f}%")
    print(f"Return/Risk (Sharpe):    {float(stats_dict['sharpe']):.2f}")
    print(f"Maximum Drawdown:        {float(stats_dict['min']):.2f}%")
    
    print("\n(Note: A Sharpe ratio above 0.5 for a simple, non-optimised trend following")
    print("system over a broad macro basket is considered a solid, robust baseline).")
    print("===================================================\n")

if __name__ == "__main__":
    run_starter_backtest()
