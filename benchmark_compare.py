import sys
import logging
import pandas as pd
logging.basicConfig(level=logging.WARNING)

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.example.simplesystem import simplesystem

def run_benchmark():
    print("Loading data and initializing system to get exact backtest date range...")
    my_data = csvFuturesSimData()
    my_config = Config("private.improved_system.yaml")
    my_system = simplesystem(config=my_config, data=my_data)
    
    # We need to know the exact dates the backtest ran to do an apples-to-apples comparison
    profits = my_system.accounts.portfolio()
    start_date = profits.index[0]
    end_date = profits.index[-1]
    
    print(f"Backtest Date Range: {start_date.date()} to {end_date.date()}")
    print("\nCalculating Buy & Hold metrics for SP500_micro...")
    
    # Get the raw daily prices for SP500_micro (Adjusted for rolls)
    # csvFuturesSimData provides .get_raw_price()
    try:
         sp500_prices = my_data.get_raw_price("SP500_micro")
    except Exception as e:
         print(f"Error fetching SP500_micro raw prices: {e}")
         return
         
    if sp500_prices is None or sp500_prices.empty:
         print("Missing data for SP500_micro")
         return
         
    # Align the price series to the exact system backtest dates
    aligned_prices = sp500_prices.loc[start_date:end_date]
    
    # Calculate daily percentage returns
    daily_returns = aligned_prices.pct_change(fill_method=None).dropna()
    
    import numpy as np
    
    ann_mean = daily_returns.mean() * 256 * 100
    ann_std = daily_returns.std() * np.sqrt(256) * 100
    sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(256)
    
    cum_returns = (1 + daily_returns).cumprod()
    peak = cum_returns.cummax()
    drawdown = (cum_returns - peak) / peak
    max_dd = drawdown.min() * 100
    
    print("\n================ BENCHMARK: BUY & HOLD SP500 ================")
    print(f"Performance Summary ({start_date.date()} to {end_date.date()}):")
    print(f"Annualized Mean Return:  {ann_mean:.2f}%")
    print(f"Annualized Volatility:   {ann_std:.2f}%")
    print(f"Return/Risk (Sharpe):    {sharpe:.2f}")
    print(f"Maximum Drawdown:        {max_dd:.2f}%")
    print("=============================================================\n")
    
if __name__ == "__main__":
    run_benchmark()
