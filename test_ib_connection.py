import logging
import sys
from ib_insync import IB, util

# Set up basic logging so we can see what ib_insync is doing
util.logToConsole(logging.INFO)

def test_ib_connection():
    print("Attempting to connect to IBKR Desktop Paper Trading...")
    
    ib = IB()
    
    try:
        # IBKR Desktop / TWS Paper Trading usually runs on port 7497
        # IB Gateway Paper Trading usually runs on port 4002
        # Let's try 7497 first since the user said they are using IBKR Desktop
        ib.connect(host='127.0.0.1', port=7497, clientId=1)
        print("✅ Successfully connected to IBKR!")
        
        # Request account summary to prove it works
        print("\nFetching Account Summary...")
        summary = ib.accountSummary()
        
        # Print a few key values
        for item in summary:
            if item.tag in ['NetLiquidation', 'TotalCashValue', 'AvailableFunds']:
                print(f"{item.account} | {item.tag}: {item.value} {item.currency}")
                
        print("\nConnection test complete. Disconnecting...")
        ib.disconnect()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nPlease check the following in your IBKR Desktop settings:")
        print("1. Go to Settings -> API -> Settings")
        print("2. 'Enable ActiveX and Socket Clients' MUST be checked.")
        print("3. Check the 'Socket port' number. If it is not 7497, you need to change the port in this script.")
        print("4. Ensure '127.0.0.1' is in the 'Trusted IPs' list.")

if __name__ == "__main__":
    test_ib_connection()
