from alpaca.trading.client import TradingClient
import os

os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'


def connect_to_alpaca(api_key: str, api_secret: str, paper: bool) -> TradingClient:
    try:
        trading_client = TradingClient(api_key, api_secret, paper=paper)
        account = trading_client.get_account()

        print('Connected to ALPACA.')
        print(f'${account.buying_power} is available as buying power.')
        return trading_client
    except Exception:
        print("Issue connecting to ALPACA.")


