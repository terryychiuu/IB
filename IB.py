from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)

	def nextValidId(self, orderId: int):
		super().nextValidId(orderId)
		self.nextorderId = orderId
		print('The next valid order id is: ', self.nextorderId)

	def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
		print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
	
	def openOrder(self, orderId, contract, order, orderState):
		print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

	def execDetails(self, reqId, contract, execution):
		print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)


def run_loop():
	app.run()

#Function to create FX Order contract
def FX_order():
##https://interactivebrokers.github.io/tws-api/basic_contracts.html


    contract = Contract()
    contract.symbol = "700"
    contract.secType = "STK"
    contract.currency = "HKD"
    contract.exchange = "SEHK"
    return contract

    ### GOOG ###
    # contract = Contract()
    # contract.symbol = "GOOG"
    # contract.secType = "STK"
    # contract.currency = "USD"
    # contract.exchange = "SMART"
    # contract.primaryExchange = "NASDAQ"
    # return contract

app = IBapi()
app.connect('127.0.0.1', 7497, 12334)

app.nextorderId = None

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

#Check if the API is connected via orderid
while True:
	if isinstance(app.nextorderId, int):
		print('connected')
		break
	else:
		print('waiting for connection')
		time.sleep(1)

#Create order object
##http://interactivebrokers.github.io/tws-api/basic_orders.html

order = Order()
order.action = "BUY"
order.orderType = "LMT"
order.totalQuantity = 100
order.lmtPrice = 300

### GOOG ###
# order = Order()
# order.action = "BUY"
# order.orderType = "LMT"
# order.totalQuantity = 2
# order.lmtPrice = 300

#Place order
app.placeOrder(app.nextorderId, FX_order(), order)
#app.nextorderId += 1

time.sleep(3)

