from binance.client import Client
from binance.enums import *
import time

# Replace with your Binance API key and secret
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# Replace with your trading parameters
symbol = 'BTCUSDT'
quantity = 0.001
stop_loss_percent = 0.02  # 2% stop loss
take_profit_percent = 0.05  # 5% take profit

# Create a Binance API client
client = Client(api_key, api_secret)

def place_order(symbol, side, quantity, order_type):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity,
            timeInForce=TIME_IN_FORCE_GTC
        )
        return order
    except Exception as e:
        print("Error placing order:", e)
        return None

def monitor_price():
    last_price = None
    stop_loss_price = None
    take_profit_price = None

    while True:
        try:
            # Fetch the current price
            ticker = client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker['price'])

            # Initialize the stop loss and take profit prices
            if last_price is None:
                last_price = current_price
                stop_loss_price = last_price - (last_price * stop_loss_percent)
                take_profit_price = last_price + (last_price * take_profit_percent)

            # Check if the price reaches the stop loss or take profit levels
            if current_price <= stop_loss_price or current_price >= take_profit_price:
                side = SIDE_SELL if current_price >= take_profit_price else SIDE_SELL
                order = place_order(symbol, side, quantity, ORDER_TYPE_MARKET)
                if order is not None:
                    print("Order executed:", order)
                    break

            print("Current Price:", current_price)
            time.sleep(5)  # Adjust the interval based on your requirements

        except Exception as e:
            print("Error monitoring price:", e)
            time.sleep(10)  # Retry after a delay in case of an error

monitor_price()
