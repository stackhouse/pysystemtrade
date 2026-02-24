import logging
logging.getLogger().setLevel(logging.WARNING)

from sysdata.data_blob import dataBlob
from sysproduction.data.orders import dataOrders

def check_orders():
    with dataBlob() as data:
        orders = dataOrders(data)
        stack = orders.get_list_of_orders_on_stack()
        
        print(f"Total orders on stack waiting for IB: {len(stack)}")
        for order in stack:
            print(f"Order: {order.instrument_code} | Size: {order.fill} / {order.trade_quantity}")

if __name__ == "__main__":
    check_orders()
