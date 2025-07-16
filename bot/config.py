import csv
import os
from pathlib import Path
from typing import List, Dict, Any

class Config:
    def __init__(self):
        self.config_path = Path(__file__).parent.parent / "config.csv"
        self.default_config = {
            "TELEGRAM_TOKEN": "",
            "TELEGRAM_CHAT_ID": "",
            "SYMBOL": "BTC/USDT",
            "TIMEFRAME": "1h",
            "INTERVAL": "3600",
            "RSI_WINDOW": "14",
            "SMA_SHORT": "7",
            "SMA_LONG": "25",
            "BB_WINDOW": "20",
            "VOLUME_SPIKE_RATIO": "1.5",
            "EXCHANGE": "binance",
            "THEME": "light"
        }
        self.config = self.default_config.copy()
        self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            self._create_default_config()
        
        try:
            with open(self.config_path, mode='r') as file:
                reader = csv.reader(file)
                loaded_config = {rows[0]: rows[1] for rows in reader if len(rows) == 2}
                
                # Only update with valid keys from default config
                for key in self.default_config:
                    if key in loaded_config:
                        self.config[key] = loaded_config[key]
        except Exception as e:
            print(f"Error loading config: {e}")
            self._create_default_config()

    def _create_default_config(self):
        try:
            with open(self.config_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                for key, value in self.default_config.items():
                    writer.writerow([key, value])
            self.config = self.default_config.copy()
        except Exception as e:
            print(f"Error creating default config: {e}")

    def save_config(self, new_config: Dict[str, Any]):
        """Save configuration ensuring all required keys are present"""
        # Merge new config with existing, keeping any missing keys from current config
        full_config = {**self.config, **new_config}
        
        try:
            with open(self.config_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                for key, value in full_config.items():
                    writer.writerow([key, value])
            self.config = full_config
        except Exception as e:
            print(f"Error saving config: {e}")
            raise

    @property
    def available_pairs(self) -> List[str]:
        return getattr(self, '_available_pairs', ["BTC/USDT"])

    @available_pairs.setter
    def available_pairs(self, pairs: List[str]):
        self._available_pairs = sorted(pairs)

    def __getattr__(self, name):
        if name in self.config:
            # Convert numeric values to appropriate types
            if name in ["INTERVAL", "RSI_WINDOW", "SMA_SHORT", "SMA_LONG", "BB_WINDOW"]:
                return int(self.config[name])
            elif name in ["VOLUME_SPIKE_RATIO"]:
                return float(self.config[name])
            return self.config[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
# import csv
# import os
# from pathlib import Path
# from typing import List

# class Config:
#     def __init__(self):
#         self.config_path = Path(__file__).parent.parent / "config.csv"
#         self.default_config = {
#             "TELEGRAM_TOKEN": "",
#             "TELEGRAM_CHAT_ID": "",
#             "SYMBOL": "BTC/USDT",
#             "TIMEFRAME": "1h",
#             "INTERVAL": "3600",
#             "RSI_WINDOW": "14",
#             "SMA_SHORT": "7",
#             "SMA_LONG": "25",
#             "BB_WINDOW": "20",
#             "VOLUME_SPIKE_RATIO": "1.5",
#             "EXCHANGE": "binance",
#             "THEME": "light"
#         }
#         self._load_config()

#     def _load_config(self):
#         if not os.path.exists(self.config_path):
#             self._create_default_config()
        
#         with open(self.config_path, mode='r') as file:
#             reader = csv.reader(file)
#             self.config = {rows[0]: rows[1] for rows in reader if len(rows) == 2}

#     def _create_default_config(self):
#         with open(self.config_path, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             for key, value in self.default_config.items():
#                 writer.writerow([key, value])
#         self.config = self.default_config.copy()

#     def save_config(self, new_config):
#         with open(self.config_path, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             for key, value in new_config.items():
#                 writer.writerow([key, value])
#         self.config = new_config.copy()

#     @property
#     def available_pairs(self) -> List[str]:
#         return getattr(self, '_available_pairs', ["BTC/USDT"])

#     @available_pairs.setter
#     def available_pairs(self, pairs: List[str]):
#         self._available_pairs = sorted(pairs)

#     def __getattr__(self, name):
#         if name in self.config:
#             if name in ["INTERVAL", "RSI_WINDOW", "SMA_SHORT", "SMA_LONG", "BB_WINDOW"]:
#                 return int(self.config[name])
#             elif name in ["VOLUME_SPIKE_RATIO"]:
#                 return float(self.config[name])
#             return self.config[name]
#         raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
# # # # class Config:
# # # #     TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
# # # #     TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'
# # # #     SYMBOL = 'BTC/USDT'
# # # #     TIMEFRAME = '1h'
# # # #     INTERVAL = 10  # seconds between checks
# # # #     RSI_WINDOW = 14
# # # #     SMA_SHORT = 7
# # # #     SMA_LONG = 25
# # # #     BB_WINDOW = 20
# # # #     VOLUME_SPIKE_RATIO = 1.5

# # # import csv
# # # import os
# # # from pathlib import Path

# # # class Config:
# # #     def __init__(self):
# # #         self.config_path = Path(__file__).parent.parent / "config.csv"
# # #         self.default_config = {
# # #             "TELEGRAM_TOKEN": "",
# # #             "TELEGRAM_CHAT_ID": "",
# # #             "SYMBOL": "BTC/USDT",
# # #             "AVAILABLE_PAIRS": "BTC/USDT,USUAL/USDT,SOL/USDT,XRP/USDT,TON/USDT",
# # #             "TIMEFRAME": "1h",
# # #             "INTERVAL": "3600",
# # #             "RSI_WINDOW": "14",
# # #             "SMA_SHORT": "7",
# # #             "SMA_LONG": "25",
# # #             "BB_WINDOW": "20",
# # #             "VOLUME_SPIKE_RATIO": "1.5",
# # #             "EXCHANGE": "binance",
# # #             "THEME": "light"
# # #         }
# # #         self._load_config()

# # #     def _load_config(self):
# # #         if not os.path.exists(self.config_path):
# # #             self._create_default_config()
        
# # #         with open(self.config_path, mode='r') as file:
# # #             reader = csv.reader(file)
# # #             self.config = {rows[0]: rows[1] for rows in reader if len(rows) == 2}

# # #     def _create_default_config(self):
# # #         with open(self.config_path, mode='w', newline='') as file:
# # #             writer = csv.writer(file)
# # #             for key, value in self.default_config.items():
# # #                 writer.writerow([key, value])
# # #         self.config = self.default_config.copy()

# # #     def save_config(self, new_config):
# # #         with open(self.config_path, mode='w', newline='') as file:
# # #             writer = csv.writer(file)
# # #             for key, value in new_config.items():
# # #                 writer.writerow([key, value])
# # #         self.config = new_config.copy()

# # #     def __getattr__(self, name):
# # #         if name in self.config:
# # #             # Convert numeric values to appropriate types
# # #             if name in ["INTERVAL", "RSI_WINDOW", "SMA_SHORT", "SMA_LONG", "BB_WINDOW"]:
# # #                 return int(self.config[name])
# # #             elif name in ["VOLUME_SPIKE_RATIO"]:
# # #                 return float(self.config[name])
# # #             return self.config[name]
# # #         raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
# # #     @property
# # #     def available_pairs(self):
# # #         return [pair.strip() for pair in self.config.get("AVAILABLE_PAIRS", "").split(",") if pair.strip()]

# # import csv
# # import os
# # from pathlib import Path
# # from typing import List

# # class Config:
# #     def __init__(self):
# #         self.config_path = Path(__file__).parent.parent / "config.csv"
# #         self.default_config = {
# #             "TELEGRAM_TOKEN": "",
# #             "TELEGRAM_CHAT_ID": "",
# #             "SYMBOL": "BTC/USDT",
# #             "TIMEFRAME": "1h",
# #             "INTERVAL": "3600",
# #             "RSI_WINDOW": "14",
# #             "SMA_SHORT": "7",
# #             "SMA_LONG": "25",
# #             "BB_WINDOW": "20",
# #             "VOLUME_SPIKE_RATIO": "1.5",
# #             "EXCHANGE": "binance",
# #             "THEME": "light"
# #         }
# #         self._load_config()

# #     def _load_config(self):
# #         if not os.path.exists(self.config_path):
# #             self._create_default_config()
        
# #         with open(self.config_path, mode='r') as file:
# #             reader = csv.reader(file)
# #             self.config = {rows[0]: rows[1] for rows in reader if len(rows) == 2}

# #     def _create_default_config(self):
# #         with open(self.config_path, mode='w', newline='') as file:
# #             writer = csv.writer(file)
# #             for key, value in self.default_config.items():
# #                 writer.writerow([key, value])
# #         self.config = self.default_config.copy()

# #     def save_config(self, new_config):
# #         with open(self.config_path, mode='w', newline='') as file:
# #             writer = csv.writer(file)
# #             for key, value in new_config.items():
# #                 writer.writerow([key, value])
# #         self.config = new_config.copy()

# #     @property
# #     def available_pairs(self) -> List[str]:
# #         """Get available pairs from exchange (loaded dynamically)"""
# #         # This will be set by the bot manager after exchange initialization
# #         return getattr(self, '_available_pairs', ["BTC/USDT"])

# #     @available_pairs.setter
# #     def available_pairs(self, pairs: List[str]):
# #         """Set available pairs from exchange"""
# #         self._available_pairs = pairs

# #     def __getattr__(self, name):
# #         if name in self.config:
# #             if name in ["INTERVAL", "RSI_WINDOW", "SMA_SHORT", "SMA_LONG", "BB_WINDOW"]:
# #                 return int(self.config[name])
# #             elif name in ["VOLUME_SPIKE_RATIO"]:
# #                 return float(self.config[name])
# #             return self.config[name]
# #         raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")