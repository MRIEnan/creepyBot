from bot.config import Config
from bot.exchange import Exchange
from bot.analyzer import Analyzer
from bot.notifier import Notifier
from ui.main_window import MainWindow
import threading
import time
from typing import Optional

class BotManager:
    def __init__(self):
        self.config = Config()
        self.exchange = Exchange(self.config.EXCHANGE)
        self.config.available_pairs = self.exchange.get_available_pairs()
        self.analyzer = Analyzer(self.config)
        self.notifier = Notifier(self.config)
        self.running = False
        # self.thread = None
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()

    def update_config(self, new_config):
        """Handle configuration updates more robustly"""
        try:
            # Save the new configuration
            self.config.save_config(new_config)
            
            # Reinitialize components if needed
            if new_config.get("EXCHANGE") != self.config.EXCHANGE:
                self.exchange = Exchange(new_config["EXCHANGE"])
                self.config.available_pairs = self.exchange.get_available_pairs()
            
            # Reinitialize analyzers with new config
            self.analyzer = Analyzer(self.config)
            self.notifier = Notifier(self.config)
            
        except Exception as e:
            if hasattr(self, 'window'):
                self.window.log(f"Error updating config: {e}")
            raise
        # self.config.save_config(new_config)
        # if new_config.get("EXCHANGE") != self.config.EXCHANGE:
        #     self.exchange = Exchange(new_config["EXCHANGE"])
        #     self.config.available_pairs = self.exchange.get_available_pairs()
        # self.analyzer = Analyzer(self.config)
        # self.notifier = Notifier(self.config)

    def start(self):
        if not self.running:
            self.running = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.stop_event.set()
            # Don't join here - that's what causes the freeze
            self.thread = None
        # if self.thread:
        #     self.thread.join()

    """ def run(self):
        while self.running:
            try:
                df = self.exchange.get_ohlcv(
                    symbol=self.config.SYMBOL,
                    timeframe=self.config.TIMEFRAME
                )
                signal, latest = self.analyzer.analyze(df)
                
                # Update UI
                if hasattr(self, 'window'):
                    self.window.update_signal(signal)
                    self.window.update_stats(latest)
                
                time.sleep(self.config.INTERVAL)
            except Exception as e:
                if hasattr(self, 'window'):
                    self.window.log(f"Error: {e}")
                time.sleep(60) """
    def run(self):
        """Main trading bot execution loop with combined features."""
        while self.running and not self.stop_event.is_set():
            try:
                start_time = time.time()
                
                # Validate pair availability
                if hasattr(self.config, 'available_pairs') and \
                  self.config.SYMBOL not in self.config.available_pairs:
                    self._log_error(f"Pair {self.config.SYMBOL} not available")
                    time.sleep(60)
                    continue
                    
                # Fetch market data
                df = self.exchange.get_ohlcv(
                    symbol=self.config.SYMBOL,
                    timeframe=self.config.TIMEFRAME
                )
                
                # Analyze data
                signal, latest_data = self.analyzer.analyze(df)
                latest_data['symbol'] = self.config.SYMBOL
                
                # # Prepare formatted message
                # message = (
                #     f"[{latest_data['timestamp']}] {self.config.SYMBOL}\n"
                #     f"Price: {latest_data['close']:.4f}\n"
                #     f"RSI: {latest_data['rsi']:.2f} | MA7: {latest_data['ma_short']:.4f} | MA25: {latest_data['ma_long']:.4f}\n"
                #     f"MACD: {latest_data['macd']:.4f} | Signal: {latest_data['macd_signal']:.4f}\n"
                #     f"Volume: {latest_data['volume']:.2f} | Signal: {signal}\n"
                # )
                # Prepare formatted message with type safety
                message = (
                    f"[{str(latest_data.get('timestamp', 'N/A'))}] {getattr(self.config, 'SYMBOL', 'N/A')} ({getattr(self.config, 'EXCHANGE', 'N/A').upper()})\n"
                    f"Timeframe: {getattr(self.config, 'TIMEFRAME', 'N/A')} | Interval: {getattr(self.config, 'INTERVAL', 'N/A')} mins\n"
                    f"RSI ({getattr(self.config, 'RSI_WINDOW', 7)}): {float(latest_data.get('rsi', 0)):.2f} | "
                    f"MA{getattr(self.config, 'SMA_SHORT', 7)}: {float(latest_data.get('ma_short', 0)):.4f} | "
                    f"MA{getattr(self.config, 'SMA_LONG', 25)}: {float(latest_data.get('ma_long', 0)):.4f}\n"
                    f"MACD: {float(latest_data.get('macd', 0)):.4f} | Signal: {float(latest_data.get('macd_signal', 0)):.4f}\n"
                    f"Volume: {float(latest_data.get('volume', 0)):.2f} | Spike Ratio: {float(getattr(self.config, 'VOLUME_SPIKE_RATIO', 1.5)):.1f}\n"
                    f"---------------------\n"
                    f"Price: {float(latest_data.get('close', 0)):.4f}\n"
                    f"Signal: {str(signal)}\n"
                    f"---------------------\n"
                    f"Theme: {getattr(self.config, 'THEME', 'light').capitalize()}"
                )
                
                # Update UI
                self._update_ui(signal, latest_data, message)
                
                # Send notifications for important signals
                if signal in ['BUY', 'SELL','HOLD'] and hasattr(self, 'notifier'):
                    self.notifier.send_telegram(message)
                
                # Precision sleep with stop_event checking
                elapsed = time.time() - start_time
                remaining_sleep = max(0, self.config.INTERVAL - elapsed)
                self._precision_sleep(remaining_sleep)
                
            except Exception as e:
                self._log_error(f"Runtime error: {e}")
                time.sleep(min(60, self.config.INTERVAL))  # Cap error delay at 60s

    def _update_ui(self, signal, latest_data, message):
        """Helper method to update user interface."""
        if hasattr(self, 'window'):
            self.window.log(message)
            self.window.update_stats(latest_data)
            self.window.update_signal(signal)
            self.window.signal_label.config(text=f"Signal: {signal}")

    def _precision_sleep(self, duration):
        """Sleep with frequent stop_event checks."""
        for _ in range(int(duration * 10)):
            if self.stop_event.is_set():
                break
            time.sleep(0.1)

    def _log_error(self, message):
        """Centralized error logging."""
        if hasattr(self, 'window'):
            self.window.log(message)
        print(message)  # Also log to console if needed
    # def run(self):
    #     while self.running and not self.stop_event.is_set():
    #         try:
    #             start_time = time.time()
                
    #             df = self.exchange.get_ohlcv(
    #                 symbol=self.config.SYMBOL,
    #                 timeframe=self.config.TIMEFRAME
    #             )
    #             signal, latest = self.analyzer.analyze(df)
                
                
    #             if hasattr(self, 'window'):
    #                 self.window.update_signal(signal)
    #                 self.window.update_stats(latest)
    #                 self.window.log(f"Signal: {signal} at {latest['timestamp']}")
                
    #             # Calculate remaining sleep time
    #             elapsed = time.time() - start_time
    #             remaining_sleep = max(0, self.config.INTERVAL - elapsed)
                
    #             # Sleep in small increments to check stop_event
    #             for _ in range(int(remaining_sleep * 10)):
    #                 if self.stop_event.is_set():
    #                     break
    #                 time.sleep(0.1)
                    
    #         except Exception as e:
    #             if hasattr(self, 'window'):
    #                 self.window.log(f"Error: {e}")
    #             time.sleep(5)  # Brief pause after error

if __name__ == "__main__":
    bot_manager = BotManager()
    window = MainWindow(bot_manager)
    bot_manager.window = window
    window.mainloop()
# from bot.config import Config
# from bot.exchange import Exchange
# from bot.analyzer import Analyzer
# from bot.notifier import Notifier
# from ui.main_window import MainWindow
# import threading
# import time

# class BotManager:
#     def __init__(self):
#         self.config = Config()
#         self.exchange = Exchange(self.config.EXCHANGE)

#         # Set available pairs in config
#         self.config.available_pairs = self.exchange.get_available_pairs()

#         self.analyzer = Analyzer(self.config)
#         self.notifier = Notifier(self.config)
#         self.running = False
#         self.thread = None

#     def update_config(self, new_config):
#         """Handle config updates"""
#         # Reinitialize exchange if changed
#         if new_config.get("EXCHANGE") != self.config.EXCHANGE:
#             self.exchange = Exchange(new_config["EXCHANGE"])
#             self.config.available_pairs = self.exchange.get_available_pairs()
        
#         # Update other components
#         self.analyzer = Analyzer(self.config)
#         self.notifier = Notifier(self.config)
        
#         # Save and reload config
#         self.config.save_config(new_config)
#         self.config = Config()  # Reload config

#     def start(self):
#         if not self.running:
#             self.running = True
#             self.thread = threading.Thread(target=self.run, daemon=True)
#             self.thread.start()

#     def stop(self):
#         self.running = False
#         if self.thread:
#             self.thread.join()

#     def run(self):
#         while self.running:
#             try:
#                 # Validate pair is available
#                 if self.config.SYMBOL not in self.config.available_pairs:
#                     self.window.log(f"Error: Pair {self.config.SYMBOL} not in available pairs")
#                     time.sleep(60)
#                     continue
                    
#                 df = self.exchange.get_ohlcv(
#                     symbol=self.config.SYMBOL,
#                     timeframe=self.config.TIMEFRAME
#                 )
#                 # df = self.exchange.get_ohlcv(
#                 #     symbol=self.config.SYMBOL,
#                 #     timeframe=self.config.TIMEFRAME
#                 # )
                
#                 signal, latest_data = self.analyzer.analyze(df)
#                 latest_data['symbol'] = self.config.SYMBOL
                
#                 # Format message
#                 message = (
#                     f"[{latest_data['timestamp']}] {self.config.SYMBOL}\n"
#                     f"Price: {latest_data['close']:.4f}\n"
#                     f"RSI: {latest_data['rsi']:.2f} | MA7: {latest_data['ma_short']:.4f} | MA25: {latest_data['ma_long']:.4f}\n"
#                     f"MACD: {latest_data['macd']:.4f} | Signal: {latest_data['macd_signal']:.4f}\n"
#                     f"Volume: {latest_data['volume']:.2f} | Signal: {signal}\n"
#                 )
                
#                 # Update UI
#                 if hasattr(self, 'window'):
#                     self.window.log(message)
#                     self.window.update_stats(latest_data)
#                     self.window.signal_label.config(text=f"Signal: {signal}")
                
#                 # Send notification if needed
#                 if signal in ['BUY', 'SELL']:
#                     self.notifier.send_telegram(message)
                
#                 # Sleep for interval
#                 for _ in range(self.config.INTERVAL):
#                     if not self.running:
#                         break
#                     time.sleep(1)
                    
#             except Exception as e:
#                 if hasattr(self, 'window'):
#                     self.window.log(f"Error: {e}")
#                 time.sleep(60)

# if __name__ == "__main__":
#     bot_manager = BotManager()
#     window = MainWindow(bot_manager)
#     bot_manager.window = window  # Connect the window to the bot manager
    
#     # Apply dark theme if available
#     try:
#         from ttkthemes import ThemedTk
#         window.tk.call("source", "azure.tcl")
#         window.tk.call("set_theme", "light")
#     except:
#         pass
    
#     window.mainloop()