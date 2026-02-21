from sysinit.futures.seed_price_data_from_IB import seed_price_data_from_IB

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

for inst in instruments:
    print(f"Seeding {inst}...")
    try:
        seed_price_data_from_IB(inst)
    except Exception as e:
        import traceback
        traceback.print_exc()

