import logging
logging.getLogger().setLevel(logging.WARNING)

from sysdata.data_blob import dataBlob
from sysproduction.data.prices import diagPrices

def check_data_availability():
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

    with dataBlob(log_name="Check-Data") as data:
        print("=== HISTORICAL PRICE DATA IN MONGODB ===")
        price_db = diagPrices(data)
        
        for inst in instruments:
            try:
                adj_prices = price_db.get_adjusted_prices(inst)
                
                if adj_prices is None or adj_prices.empty:
                    print(f"{inst:15s} | 0 days | No data found")
                else:
                    num_days = len(adj_prices)
                    first_date = adj_prices.index[0].strftime('%Y-%m-%d')
                    last_date = adj_prices.index[-1].strftime('%Y-%m-%d')
                    
                    status = "✅ OK" if num_days > 250 else "❌ WARMUP REQUIRED (~250+ days ideal)"
                    print(f"{inst:15s} | {num_days:4d} days | {first_date} to {last_date} | {status}")
            except Exception as e:
                print(f"{inst:15s} | Failed to fetch: {e}")

if __name__ == "__main__":
    check_data_availability()
