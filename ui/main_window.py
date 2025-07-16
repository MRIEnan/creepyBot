import tkinter as tk
from tkinter import ttk, scrolledtext
from .settings_window import SettingsWindow

class MainWindow(tk.Tk):
    def __init__(self, bot_manager):
        super().__init__()
        self.bot_manager = bot_manager
        self.title("Creepy Bot")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.current_theme = self.bot_manager.config.THEME
        self.signal_colors = {
            "BUY": "green",
            "SELL": "red",
            "HOLD": "gray"
        }
        
        self._create_widgets()
        self._setup_layout()
        self._configure_theme()

    def _create_widgets(self):
        """Initialize all GUI widgets"""
        # Status Frame
        self.status_frame = ttk.LabelFrame(self, text="Bot Status", padding=10)
        self.status_label = ttk.Label(self.status_frame, text="Stopped", font=("Arial", 12))
        
        self.signal_var = tk.StringVar(value="Signal: None")
        self.signal_label = ttk.Label(
            self.status_frame,
            textvariable=self.signal_var,
            font=("Arial", 14, "bold"),
            foreground=self._get_signal_color("None")
        )
        
        # Control Frame
        self.control_frame = ttk.Frame(self, padding=10)
        self.start_btn = ttk.Button(self.control_frame, text="Start Bot", command=self.start_bot)
        self.stop_btn = ttk.Button(self.control_frame, text="Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.settings_btn = ttk.Button(self.control_frame, text="Settings", command=self.open_settings)
        self.theme_btn = ttk.Button(self.control_frame, text="Toggle Theme", command=self.toggle_theme)
        
        # Log Frame
        self.log_frame = ttk.LabelFrame(self, text="Logs", padding=10)
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame,
            height=20,
            font=("Consolas", 10),
            bg="white",
            fg="black"
        )
        
        # Stats Frame
        self.stats_frame = ttk.LabelFrame(self, text="Market Stats", padding=10)
        self.stats_text = tk.Text(
            self.stats_frame,
            height=8,
            font=("Consolas", 10),
            state=tk.DISABLED,
            bg="white",
            fg="black"
        )

    def _setup_layout(self):
        """Arrange widgets in the window"""
        # Status Frame
        self.status_frame.pack(fill=tk.X, padx=5, pady=5)
        self.status_label.pack(side=tk.LEFT, padx=5)
        self.signal_label.pack(side=tk.RIGHT, padx=5)
        
        # Control Frame
        self.control_frame.pack(fill=tk.X, padx=5, pady=5)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.settings_btn.pack(side=tk.LEFT, padx=5)
        self.theme_btn.pack(side=tk.RIGHT, padx=5)
        
        # Stats and Log Frames
        self.stats_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def _configure_theme(self):
        """Configure initial theme colors"""
        if self.current_theme == "dark":
            self._set_dark_theme()
        else:
            self._set_light_theme()

    def _set_dark_theme(self):
        """Apply dark theme colors"""
        self.current_theme = "dark"
        self.theme_btn.config(text="Switch to Light")
        self.configure(background="#2d2d2d")
        
        bg_color = "#3d3d3d"
        fg_color = "#ffffff"
        
        self.log_text.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.stats_text.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=bg_color, foreground=fg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TFrame", background=bg_color)
        style.configure("TButton", background="#4d4d4d", foreground=fg_color)
        style.configure("TLabelframe", background=bg_color, foreground=fg_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=fg_color)

    def _set_light_theme(self):
        """Apply light theme colors"""
        self.current_theme = "light"
        self.theme_btn.config(text="Switch to Dark")
        self.configure(background="SystemButtonFace")
        
        bg_color = "white"
        fg_color = "black"
        
        self.log_text.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.stats_text.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=bg_color, foreground=fg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TFrame", background=bg_color)
        style.configure("TButton", background="SystemButtonFace", foreground=fg_color)
        style.configure("TLabelframe", background=bg_color, foreground=fg_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=fg_color)

    def toggle_theme(self):
        """Switch between dark and light theme"""
        if self.current_theme == "light":
            self._set_dark_theme()
        else:
            self._set_light_theme()

    def _get_signal_color(self, signal):
        """Get the appropriate color for the signal"""
        signal = signal.upper() if signal else "None"
        return self.signal_colors.get(signal, "gray")

    def update_signal(self, signal):
        """Update the signal display with colored text"""
        self.signal_var.set(f"Signal: {signal}")
        self.signal_label.config(foreground=self._get_signal_color(signal))

    def start_bot(self):
        """Start the trading bot"""
        self.bot_manager.start()
        self.status_label.config(text="Running")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.log("Bot started successfully")

    def stop_bot(self):
        """Stop the trading bot"""
        if self.bot_manager.running:
            self.bot_manager.stop()
            self.status_label.config(text="Stopped")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.log("Bot stopped successfully")

    def open_settings(self):
        """Open the settings window"""
        SettingsWindow(
            parent=self,
            config=self.bot_manager.config,
            exchange=self.bot_manager.exchange,
            on_save_callback=self._on_settings_saved
        )

    def _on_settings_saved(self, new_config):
        """Handle settings changes"""
        try:
            self.bot_manager.update_config(new_config)
            self.log("Settings updated successfully")
            
            if new_config.get("THEME") != self.current_theme:
                self.current_theme = new_config["THEME"]
                self._configure_theme()
        except Exception as e:
            self.log(f"Error applying settings: {e}")

    def log(self, message):
        """Add a message to the log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.update()

    def update_stats(self, data):
        """Update market statistics display"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        stats = (
            f"Symbol: {data.get('symbol', 'N/A')}\n"
            f"Price: {data.get('close', 'N/A'):.4f}\n"
            f"RSI: {data.get('rsi', 'N/A'):.2f}\n"
            f"MA7: {data.get('ma_short', 'N/A'):.4f} | MA25: {data.get('ma_long', 'N/A'):.4f}\n"
            f"MACD: {data.get('macd', 'N/A'):.4f} | Signal: {data.get('macd_signal', 'N/A'):.4f}\n"
            f"Volume: {data.get('volume', 'N/A'):.2f} (Avg: {data.get('avg_volume', 'N/A'):.2f})\n"
            f"Bollinger Bands: {data.get('bb_lower', 'N/A'):.4f} - {data.get('bb_upper', 'N/A'):.4f}"
        )
        
        self.stats_text.insert(tk.END, stats)
        self.stats_text.config(state=tk.DISABLED)

    def on_close(self):
        """Handle window close event"""
        self.stop_bot()
        self.after(100, self.destroy)