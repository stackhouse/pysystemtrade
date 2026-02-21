#!/bin/bash
# MacOS launchd executable script to run the PySystemTrade live batch
cd /Users/jacob/Documents/pysystemtrade

# Add user's python base to path
export PATH="/opt/homebrew/opt/python@3.10/bin:$PATH"

# Run the live environment wrapper
/opt/homebrew/opt/python@3.10/bin/python3.10 run_live_2026.py >> /Users/jacob/Documents/pysystemtrade/live_trading.log 2>&1
