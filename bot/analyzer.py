from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD
from ta.volatility import BollingerBands
import pandas as pd

class Analyzer:
    def __init__(self, config):
        self.config = config

    def analyze(self, df):
        if df.empty:
            return "HOLD", {"symbol": df.get("symbol", "N/A"), "error": "Empty data"}
        # Calculate indicators
        df['rsi'] = RSIIndicator(close=df['close'], window=self.config.RSI_WINDOW).rsi()
        df['ma_short'] = SMAIndicator(close=df['close'], window=self.config.SMA_SHORT).sma_indicator()
        df['ma_long'] = SMAIndicator(close=df['close'], window=self.config.SMA_LONG).sma_indicator()

        macd = MACD(close=df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()

        bb = BollingerBands(close=df['close'], window=self.config.BB_WINDOW, window_dev=2)
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_lower'] = bb.bollinger_lband()

        df['avg_volume'] = df['volume'].rolling(window=10).mean()
        df['volume_spike'] = df['volume'] > (df['avg_volume'] * self.config.VOLUME_SPIKE_RATIO)

        latest = df.iloc[-1].to_dict()
        latest['symbol'] = df['symbol'].iloc[-1]  # Ensure symbol is included

        signal = self._generate_signal(latest)
        return signal, latest

    def _generate_signal(self, data):
        buy_conditions = (
            data['rsi'] < 30 and
            data['close'] > data['ma_short'] > data['ma_long'] and
            data['macd'] > data['macd_signal'] and
            data['volume_spike']
        )

        sell_conditions = (
            data['rsi'] > 70 and
            data['close'] < data['ma_short'] < data['ma_long'] and
            data['macd'] < data['macd_signal'] and
            data['volume_spike']
        )

        if buy_conditions:
            return "BUY"
        elif sell_conditions:
            return "SELL"
        return "HOLD"