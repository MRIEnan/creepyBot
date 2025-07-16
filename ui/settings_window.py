import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, config, exchange, on_save_callback):
        super().__init__(parent)
        self.title("Bot Settings")
        self.geometry("500x600")  # Increased height to fit all controls
        self.config = config
        self.exchange = exchange
        self.on_save_callback = on_save_callback
        
        self._create_widgets()
        self._setup_layout()
        self._load_current_settings()

    def _create_widgets(self):
        # Exchange Settings Frame
        self.exchange_frame = ttk.LabelFrame(self, text="Exchange Settings", padding=10)
        
        # Exchange Selection
        self.exchange_label = ttk.Label(self.exchange_frame, text="Exchange:")
        self.exchange_combobox = ttk.Combobox(
            self.exchange_frame,
            values=["binance", "kraken", "coinbase", "bybit"],
            state="readonly",
            width=15
        )
        
        # Trading Pair Selection
        self.pair_label = ttk.Label(self.exchange_frame, text="Trading Pair:")
        self.pair_combobox = ttk.Combobox(
            self.exchange_frame,
            state="readonly",
            width=25
        )
        self.refresh_btn = ttk.Button(
            self.exchange_frame,
            text="↻",
            width=3,
            command=self._refresh_pairs
        )
        
        # Timeframe Selection
        self.timeframe_label = ttk.Label(self.exchange_frame, text="Timeframe:")
        self.timeframe_combobox = ttk.Combobox(
            self.exchange_frame,
            values=["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"],
            state="readonly",
            width=5
        )
        
        # Indicator Settings Frame
        self.indicator_frame = ttk.LabelFrame(self, text="Indicator Settings", padding=10)
        
        # RSI Settings
        self.rsi_label = ttk.Label(self.indicator_frame, text="RSI Window:")
        self.rsi_spinbox = ttk.Spinbox(self.indicator_frame, from_=5, to=30, width=5)
        
        # Moving Average Settings
        self.ma_short_label = ttk.Label(self.indicator_frame, text="Short MA:")
        self.ma_short_spinbox = ttk.Spinbox(self.indicator_frame, from_=5, to=20, width=5)
        
        self.ma_long_label = ttk.Label(self.indicator_frame, text="Long MA:")
        self.ma_long_spinbox = ttk.Spinbox(self.indicator_frame, from_=20, to=50, width=5)
        
        # Bollinger Bands Settings
        self.bb_window_label = ttk.Label(self.indicator_frame, text="BB Window:")
        self.bb_window_spinbox = ttk.Spinbox(self.indicator_frame, from_=10, to=50, width=5)
        
        # Volume Settings
        self.volume_ratio_label = ttk.Label(self.indicator_frame, text="Volume Spike Ratio:")
        self.volume_ratio_spinbox = ttk.Spinbox(
            self.indicator_frame, 
            from_=1.0, to=3.0, increment=0.1,
            format="%.1f",
            width=5
        )
        
        # Control Buttons
        self.button_frame = ttk.Frame(self, padding=10)
        self.save_btn = ttk.Button(self.button_frame, text="Save", command=self._save_settings)
        self.cancel_btn = ttk.Button(self.button_frame, text="Cancel", command=self.destroy)

    def _setup_layout(self):
        # Exchange Frame Layout
        self.exchange_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Exchange selection row
        self.exchange_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.exchange_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Pair selection row
        self.pair_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.pair_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        self.refresh_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Timeframe row
        self.timeframe_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.timeframe_combobox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Indicator Frame Layout
        self.indicator_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # RSI row
        self.rsi_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.rsi_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # MA Short row
        self.ma_short_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.ma_short_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # MA Long row
        self.ma_long_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.ma_long_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # BB Window row
        self.bb_window_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.bb_window_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Volume Ratio row
        self.volume_ratio_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.volume_ratio_spinbox.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Buttons Frame Layout
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        self.save_btn.pack(side=tk.RIGHT, padx=5)
        self.cancel_btn.pack(side=tk.RIGHT, padx=5)

    def _load_current_settings(self):
        """Load current settings into the form"""
        # Exchange settings
        self.exchange_combobox.set(self.config.EXCHANGE)
        self.pair_combobox['values'] = self.config.available_pairs
        self.pair_combobox.set(self.config.SYMBOL)
        self.timeframe_combobox.set(self.config.TIMEFRAME)
        
        # Indicator settings
        self.rsi_spinbox.set(self.config.RSI_WINDOW)
        self.ma_short_spinbox.set(self.config.SMA_SHORT)
        self.ma_long_spinbox.set(self.config.SMA_LONG)
        self.bb_window_spinbox.set(self.config.BB_WINDOW)
        self.volume_ratio_spinbox.set(self.config.VOLUME_SPIKE_RATIO)

    def _refresh_pairs(self):
        """Reload available pairs from exchange"""
        try:
            self.exchange._load_supported_pairs()
            available_pairs = self.exchange.get_available_pairs()
            self.pair_combobox['values'] = available_pairs
            messagebox.showinfo("Success", f"Refreshed {len(available_pairs)} pairs")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh pairs: {e}")

    def _save_settings(self):
        """Save all settings to configuration"""
        new_config = {
            "EXCHANGE": self.exchange_combobox.get(),
            "SYMBOL": self.pair_combobox.get(),
            "TIMEFRAME": self.timeframe_combobox.get(),
            "RSI_WINDOW": self.rsi_spinbox.get(),
            "SMA_SHORT": self.ma_short_spinbox.get(),
            "SMA_LONG": self.ma_long_spinbox.get(),
            "BB_WINDOW": self.bb_window_spinbox.get(),
            "VOLUME_SPIKE_RATIO": self.volume_ratio_spinbox.get(),
            "THEME": self.config.THEME  # Preserve current theme
        }
        
        try:
            self.on_save_callback(new_config)
            messagebox.showinfo("Success", "Settings saved successfully")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
# import tkinter as tk
# from tkinter import ttk, messagebox
# from typing import Dict

# class SettingsWindow(tk.Toplevel):
#     def __init__(self, parent, config, exchange, on_save_callback):
#         super().__init__(parent)
#         self.title("Bot Settings")
#         self.geometry("500x500")
#         self.config = config
#         self.exchange = exchange
#         self.on_save_callback = on_save_callback
        
#         self._create_widgets()
#         self._setup_layout()
#         self._load_current_settings()

#     def _create_widgets(self):
#         # Exchange Settings
#         self.exchange_frame = ttk.LabelFrame(self, text="Exchange Settings", padding=10)
        
#         self.pair_label = ttk.Label(self.exchange_frame, text="Trading Pair:")
#         self.pair_combobox = ttk.Combobox(
#             self.exchange_frame,
#             state="readonly",
#             width=25
#         )
#         self.refresh_btn = ttk.Button(
#             self.exchange_frame,
#             text="↻",
#             width=3,
#             command=self._refresh_pairs
#         )
        
#         self.timeframe_label = ttk.Label(self.exchange_frame, text="Timeframe:")
#         self.timeframe_combobox = ttk.Combobox(
#             self.exchange_frame,
#             values=["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"],
#             state="readonly",
#             width=5
#         )
        
#         # Indicator Settings
#         self.indicator_frame = ttk.LabelFrame(self, text="Indicator Settings", padding=10)
        
#         self.rsi_label = ttk.Label(self.indicator_frame, text="RSI Window:")
#         self.rsi_spinbox = ttk.Spinbox(self.indicator_frame, from_=5, to=30, width=5)
        
#         self.ma_short_label = ttk.Label(self.indicator_frame, text="Short MA:")
#         self.ma_short_spinbox = ttk.Spinbox(self.indicator_frame, from_=5, to=20, width=5)
        
#         self.ma_long_label = ttk.Label(self.indicator_frame, text="Long MA:")
#         self.ma_long_spinbox = ttk.Spinbox(self.indicator_frame, from_=20, to=50, width=5)
        
#         # Control Buttons
#         self.button_frame = ttk.Frame(self, padding=10)
#         self.save_btn = ttk.Button(self.button_frame, text="Save", command=self._save_settings)
#         self.cancel_btn = ttk.Button(self.button_frame, text="Cancel", command=self.destroy)

#     def _setup_layout(self):
#         # Exchange Frame
#         self.exchange_frame.pack(fill=tk.X, padx=5, pady=5)
#         self.pair_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
#         self.pair_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
#         self.refresh_btn.grid(row=0, column=2, padx=5, pady=5)
        
#         self.timeframe_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
#         self.timeframe_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
#         # Indicator Frame
#         self.indicator_frame.pack(fill=tk.X, padx=5, pady=5)
#         self.rsi_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
#         self.rsi_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
#         self.ma_short_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
#         self.ma_short_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
#         self.ma_long_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
#         self.ma_long_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
#         # Buttons
#         self.button_frame.pack(fill=tk.X, padx=5, pady=5)
#         self.save_btn.pack(side=tk.RIGHT, padx=5)
#         self.cancel_btn.pack(side=tk.RIGHT, padx=5)

#     def _load_current_settings(self):
#         self.pair_combobox['values'] = self.config.available_pairs
#         self.pair_combobox.set(self.config.SYMBOL)
#         self.timeframe_combobox.set(self.config.TIMEFRAME)
#         self.rsi_spinbox.set(self.config.RSI_WINDOW)
#         self.ma_short_spinbox.set(self.config.SMA_SHORT)
#         self.ma_long_spinbox.set(self.config.SMA_LONG)

#     def _refresh_pairs(self):
#         try:
#             self.exchange._load_supported_pairs()
#             self.pair_combobox['values'] = self.exchange.get_available_pairs()
#             messagebox.showinfo("Success", "Pairs refreshed successfully")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to refresh pairs: {e}")

#     def _save_settings(self):
#         """Save all settings including previously missing ones"""
#         new_config = {
#             "SYMBOL": self.pair_combobox.get(),
#             "TIMEFRAME": self.timeframe_combobox.get(),
#             "RSI_WINDOW": self.rsi_spinbox.get(),
#             "SMA_SHORT": self.ma_short_spinbox.get(),
#             "SMA_LONG": self.ma_long_spinbox.get(),
#             "BB_WINDOW": "20",  # Make sure this is included
#             "VOLUME_SPIKE_RATIO": "1.5",  # Make sure this is included
#             "EXCHANGE": self.exchange_combobox.get(),  # Make sure this is included
#             "THEME": self.config.THEME  # Preserve current theme
#         }
        
#         try:
#             self.on_save_callback(new_config)
#             messagebox.showinfo("Success", "Settings saved successfully")
#             self.destroy()
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to save settings: {e}")
#         # new_config = {
#         #     "SYMBOL": self.pair_combobox.get(),
#         #     "TIMEFRAME": self.timeframe_combobox.get(),
#         #     "RSI_WINDOW": self.rsi_spinbox.get(),
#         #     "SMA_SHORT": self.ma_short_spinbox.get(),
#         #     "SMA_LONG": self.ma_long_spinbox.get()
#         # }
        
#         # try:
#         #     self.on_save_callback(new_config)
#         #     self.destroy()
#         # except Exception as e:
#         #     messagebox.showerror("Error", f"Failed to save settings: {e}")
# # import tkinter as tk
# # from tkinter import ttk
# # from tkinter import messagebox
# # from typing import Dict

# # class SettingsWindow(tk.Toplevel):
# #     def __init__(self, parent, config, exchange, on_save_callback):
# #         super().__init__(parent)
# #         self.title("Bot Settings")
# #         self.geometry("500x500")
# #         self.config = config
# #         self.exchange = exchange
# #         self.on_save_callback = on_save_callback
        
# #         self._create_widgets()
# #         self._setup_layout()
# #         self._load_current_settings()

# #     def _create_widgets(self):
# #         # # Exchange Settings
# #         # self.exchange_frame = ttk.LabelFrame(self, text="Exchange Settings", padding=10)
        
# #         # self.symbol_label = ttk.Label(self.exchange_frame, text="Trading Pair:")
# #         # self.symbol_entry = ttk.Entry(self.exchange_frame, width=20)
        
# #         # self.timeframe_label = ttk.Label(self.exchange_frame, text="Timeframe:")
# #         # self.timeframe_combobox = ttk.Combobox(
# #         #     self.exchange_frame, 
# #         #     values=["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"],
# #         #     width=5
# #         # )
        
# #         # self.exchange_label = ttk.Label(self.exchange_frame, text="Exchange:")
# #         # self.exchange_combobox = ttk.Combobox(
# #         #     self.exchange_frame, 
# #         #     values=["binance", "kraken", "coinbase", "ftx"],
# #         #     width=10
# #         # )
# #          # Exchange Settings Frame
# #         self.exchange_frame = ttk.LabelFrame(self, text="Exchange Settings", padding=10)
        
# #         # Trading Pair Selection
# #         self.pair_label = ttk.Label(self.exchange_frame, text="Trading Pair:")
# #         self.pair_combobox = ttk.Combobox(
# #             self.exchange_frame,
# #             state="readonly",
# #             width=25
# #         )
# #         self.refresh_pairs_btn = ttk.Button(
# #             self.exchange_frame,
# #             text="↻",
# #             width=3,
# #             command=self._refresh_pairs
# #         )
        
# #         # Timeframe Selection
# #         self.timeframe_label = ttk.Label(self.exchange_frame, text="Timeframe:")
# #         self.timeframe_combobox = ttk.Combobox(
# #             self.exchange_frame,
# #             values=["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"],
# #             state="readonly",
# #             width=5
# #         )
        
# #         # Exchange Selection
# #         self.exchange_label = ttk.Label(self.exchange_frame, text="Exchange:")
# #         self.exchange_combobox = ttk.Combobox(
# #             self.exchange_frame,
# #             values=["binance", "kraken", "coinbase", "bybit"],
# #             state="readonly",
# #             width=10
# #         )
        
        
# #         # Indicator Settings
        
# #         self.indicator_frame = ttk.LabelFrame(self, text="Indicator Settings", padding=10)
        
# #         self.rsi_label = ttk.Label(self.indicator_frame, text="RSI Window:")
# #         self.rsi_spinbox = ttk.Spinbox(self.indicator_frame, from_=5, to=30, width=5)
        
# #         self.ma_short_label = ttk.Label(self.indicator_frame, text="Short MA:")
# #         self.ma_short_spinbox = ttk.Spinbox(self.indicator_frame, from_=5, to=20, width=5)
        
# #         self.ma_long_label = ttk.Label(self.indicator_frame, text="Long MA:")
# #         self.ma_long_spinbox = ttk.Spinbox(self.indicator_frame, from_=20, to=50, width=5)
        
# #         self.volume_ratio_label = ttk.Label(self.indicator_frame, text="Volume Spike Ratio:")
# #         self.volume_ratio_spinbox = ttk.Spinbox(
# #             self.indicator_frame, 
# #             from_=1.0, to=3.0, increment=0.1, 
# #             width=5
# #         )
        
# #         # Notification Settings
# #         self.notification_frame = ttk.LabelFrame(self, text="Notification Settings", padding=10)
        
# #         self.telegram_token_label = ttk.Label(self.notification_frame, text="Telegram Token:")
# #         self.telegram_token_entry = ttk.Entry(self.notification_frame, width=40)
        
# #         self.telegram_chat_label = ttk.Label(self.notification_frame, text="Chat ID:")
# #         self.telegram_chat_entry = ttk.Entry(self.notification_frame, width=20)
        
# #         # Control Buttons
# #         self.button_frame = ttk.Frame(self, padding=10)
# #         self.save_btn = ttk.Button(self.button_frame, text="Save", command=self._save_settings)
# #         self.cancel_btn = ttk.Button(self.button_frame, text="Cancel", command=self.destroy)
# #         # # Control Buttons
# #         # self.button_frame = ttk.Frame(self, padding=10)
# #         # self.save_btn = ttk.Button(self.button_frame, text="Save", command=self.save_settings)
# #         # self.cancel_btn = ttk.Button(self.button_frame, text="Cancel", command=self.destroy)

# #     def _setup_layout(self):
# #         # Exchange Settings Layout
# #         self.exchange_frame.pack(fill=tk.X, padx=5, pady=5)
        
# #         # Pair selection row
# #         self.pair_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.pair_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
# #         self.refresh_pairs_btn.grid(row=0, column=2, padx=5, pady=5)
        
# #         # Timeframe row
# #         self.timeframe_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.timeframe_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
# #         # Exchange row
# #         self.exchange_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.exchange_combobox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
# #         # Exchange Settings
# #         self.exchange_frame.pack(fill=tk.X, padx=5, pady=5)
# #         self.symbol_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.symbol_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
# #         self.timeframe_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.timeframe_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
# #         self.exchange_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.exchange_combobox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
# #         # Indicator Settings
# #         self.indicator_frame.pack(fill=tk.X, padx=5, pady=5)
# #         self.rsi_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.rsi_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
# #         self.ma_short_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.ma_short_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
# #         self.ma_long_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.ma_long_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
# #         self.volume_ratio_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.volume_ratio_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
# #         # Notification Settings
# #         self.notification_frame.pack(fill=tk.X, padx=5, pady=5)
# #         self.telegram_token_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.telegram_token_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W, columnspan=3)
        
# #         self.telegram_chat_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
# #         self.telegram_chat_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
# #         # Control Buttons
# #         self.button_frame.pack(fill=tk.X, padx=5, pady=5)
# #         self.save_btn.pack(side=tk.RIGHT, padx=5)
# #         self.cancel_btn.pack(side=tk.RIGHT, padx=5)


# #     def _refresh_pairs(self):
# #         """Reload available pairs from exchange"""
# #         try:
# #             self.exchange._load_supported_pairs()
# #             available_pairs = self.exchange.get_available_pairs()
# #             self.pair_combobox['values'] = available_pairs
# #             messagebox.showinfo("Success", f"Refreshed {len(available_pairs)} pairs")
# #         except Exception as e:
# #             messagebox.showerror("Error", f"Failed to refresh pairs: {e}")

# #     def _load_current_settings(self):
        
# #         """Load current settings into the form"""
# #         # Load available pairs
# #         available_pairs = self.config.available_pairs
# #         self.pair_combobox['values'] = available_pairs
# #         self.pair_combobox.set(self.config.SYMBOL)
        

# #         """Load current configuration into the form"""
# #         # self.symbol_entry.insert(0, self.config.SYMBOL)
# #         self.timeframe_combobox.set(self.config.TIMEFRAME)
# #         self.exchange_combobox.set(self.config.EXCHANGE)
        
# #         self.rsi_spinbox.set(self.config.RSI_WINDOW)
# #         self.ma_short_spinbox.set(self.config.SMA_SHORT)
# #         self.ma_long_spinbox.set(self.config.SMA_LONG)
# #         self.volume_ratio_spinbox.set(self.config.VOLUME_SPIKE_RATIO)
        
# #         self.telegram_token_entry.insert(0, self.config.TELEGRAM_TOKEN)
# #         self.telegram_chat_entry.insert(0, self.config.TELEGRAM_CHAT_ID)

# #     def _save_settings(self):
# #         """Save settings to config file"""
# #         new_config = {
# #             "SYMBOL": self.pair_combobox.get(),
# #             "TIMEFRAME": self.timeframe_combobox.get(),
# #             "EXCHANGE": self.exchange_combobox.get(),
# #             "TELEGRAM_TOKEN": self.telegram_token_entry.get(),
# #             "TELEGRAM_CHAT_ID": self.telegram_chat_entry.get(),
# #             "INTERVAL": str(self.config.INTERVAL),  # Keep original for now
# #             "RSI_WINDOW": self.rsi_spinbox.get(),
# #             "SMA_SHORT": self.ma_short_spinbox.get(),
# #             "SMA_LONG": self.ma_long_spinbox.get(),
# #             "BB_WINDOW": str(self.config.BB_WINDOW),  # Keep original for now
# #             "VOLUME_SPIKE_RATIO": self.volume_ratio_spinbox.get(),
# #             "THEME": self.config.THEME  # Keep original for now
# #         }
        
# #         try:
# #             self.config.save_config(new_config)
# #             self.on_save_callback(new_config)
# #             messagebox.showinfo("Success", "Settings saved successfully!")
# #             self.destroy()
# #         except Exception as e:
# #             messagebox.showerror("Error", f"Failed to save settings: {str(e)}")