import ccxt
import pandas as pd
from typing import List

class Exchange:
    def __init__(self, exchange_name='binance'):
        self.exchange = getattr(ccxt, exchange_name)({
            'enableRateLimit': True
        })
        self.supported_pairs = []
        self._load_supported_pairs()

    def _load_supported_pairs(self):
        try:
            markets = self.exchange.load_markets()
            self.supported_pairs = sorted([
                symbol for symbol in markets.keys() 
                if symbol.endswith('/USDT') and markets[symbol]['active']
            ])
        except Exception as e:
            print(f"Error loading markets: {e}")

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
        if not self.is_pair_supported(symbol):
            raise ValueError(f"Pair {symbol} not supported")
        
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["symbol"] = symbol  # Add symbol column
            return df
        except Exception as e:
            raise Exception(f"Error fetching data: {e}")

    def is_pair_supported(self, symbol: str) -> bool:
        return symbol in self.supported_pairs

    def get_available_pairs(self) -> List[str]:
        return self.supported_pairs
# # # import ccxt
# # # import pandas as pd

# # # class Exchange:
# # #     def __init__(self, exchange_name='binance'):
# # #         self.exchange = getattr(ccxt, exchange_name)()
# # #         self.supported_pairs = None
# # #         self._load_supported_pairs()

# # #     def _load_supported_pairs(self):
# # #         try:
# # #             markets = self.exchange.load_markets()
# # #             self.supported_pairs = list(markets.keys())
# # #         except Exception as e:
# # #             print(f"Warning: Could not load supported pairs: {e}")
# # #             self.supported_pairs = []

# # #     def get_ohlcv(self, symbol, timeframe, limit=100):
# # #         if symbol not in self.supported_pairs:
# # #             raise ValueError(f"Pair {symbol} not supported by exchange")
# # #         try:
# # #             ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
# # #             df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
# # #             df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
# # #             return df
# # #         except Exception as e:
# # #             raise Exception(f"Error fetching OHLCV data: {e}")

# # import ccxt
# # import pandas as pd
# # from typing import List, Optional

# # class Exchange:
# #     def __init__(self, exchange_name: str = 'binance'):
# #         """
# #         Initialize the exchange connector.
        
# #         Args:
# #             exchange_name (str): Name of the exchange (default: 'binance')
# #         """
# #         self.exchange = getattr(ccxt, exchange_name)()
# #         self.supported_pairs: Optional[List[str]] = None
# #         self._load_supported_pairs()

# #     def _load_supported_pairs(self) -> None:
# #         """
# #         Load all supported trading pairs from the exchange.
# #         """
# #         try:
# #             markets = self.exchange.load_markets()
# #             self.supported_pairs = [pair for pair in markets.keys() if pair.endswith('/USDT')]
# #             print(f"Loaded {len(self.supported_pairs)} USDT trading pairs")
# #         except Exception as e:
# #             print(f"Warning: Could not load supported pairs: {e}")
# #             self.supported_pairs = []

# #     def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
# #         """
# #         Fetch OHLCV data from the exchange.
        
# #         Args:
# #             symbol (str): Trading pair symbol (e.g., 'BTC/USDT')
# #             timeframe (str): Timeframe for candles (e.g., '1h')
# #             limit (int): Number of candles to fetch
            
# #         Returns:
# #             pd.DataFrame: DataFrame containing OHLCV data
            
# #         Raises:
# #             ValueError: If the pair is not supported
# #             Exception: If there's an error fetching data
# #         """
# #         # Validate the pair format
# #         if not isinstance(symbol, str) or '/' not in symbol:
# #             raise ValueError(f"Invalid symbol format: {symbol}. Expected format: 'BASE/QUOTE'")
            
# #         # Check if pair is supported
# #         if self.supported_pairs and symbol not in self.supported_pairs:
# #             raise ValueError(f"Pair {symbol} not supported by exchange. Available USDT pairs: {len(self.supported_pairs)}")
            
# #         # Validate timeframe
# #         valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']
# #         if timeframe not in valid_timeframes:
# #             raise ValueError(f"Invalid timeframe: {timeframe}. Valid options: {valid_timeframes}")

# #         try:
# #             # Fetch data from exchange
# #             ohlcv = self.exchange.fetch_ohlcv(
# #                 symbol=symbol,
# #                 timeframe=timeframe,
# #                 limit=limit
# #             )
            
# #             # Create DataFrame
# #             df = pd.DataFrame(
# #                 ohlcv, 
# #                 columns=["timestamp", "open", "high", "low", "close", "volume"]
# #             )
            
# #             # Convert timestamp to datetime
# #             df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            
# #             # Add symbol column for reference
# #             df["symbol"] = symbol
            
# #             return df
            
# #         except ccxt.NetworkError as e:
# #             raise Exception(f"Network error fetching data: {e}")
# #         except ccxt.ExchangeError as e:
# #             raise Exception(f"Exchange error fetching data: {e}")
# #         except Exception as e:
# #             raise Exception(f"Unexpected error fetching OHLCV data: {e}")

# #     def is_pair_supported(self, symbol: str) -> bool:
# #         """
# #         Check if a trading pair is supported by the exchange.
        
# #         Args:
# #             symbol (str): Trading pair symbol
            
# #         Returns:
# #             bool: True if supported, False otherwise
# #         """
# #         if not self.supported_pairs:
# #             return False
# #         return symbol in self.supported_pairs

# import ccxt
# import pandas as pd
# from typing import List, Optional

# class Exchange:
#     def __init__(self, exchange_name: str = 'binance'):
#         self.exchange = getattr(ccxt, exchange_name)({
#             'enableRateLimit': True  # Important for API rate limiting
#         })
#         self.supported_pairs = []
#         self._load_supported_pairs()

#     def _load_supported_pairs(self) -> None:
#         """Load and filter only USDT trading pairs"""
#         try:
#             markets = self.exchange.load_markets()
#             self.supported_pairs = sorted([
#                 symbol for symbol in markets.keys() 
#                 if symbol.endswith('/USDT') and markets[symbol]['active']
#             ])
#             print(f"Loaded {len(self.supported_pairs)} active USDT pairs")
#         except Exception as e:
#             print(f"Error loading markets: {e}")
#             self.supported_pairs = []

#     def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
#         """Fetch OHLCV data with validation"""
#         if not self.is_pair_supported(symbol):
#             raise ValueError(f"Pair {symbol} not supported")
        
#         try:
#             ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
#             df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
#             df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
#             return df
#         except Exception as e:
#             raise Exception(f"Error fetching data: {e}")

#     def is_pair_supported(self, symbol: str) -> bool:
#         """Check if pair is supported"""
#         return symbol in self.supported_pairs

#     def get_available_pairs(self) -> List[str]:
#         """Get sorted list of available USDT pairs"""
#         return self.supported_pairs