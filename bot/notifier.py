import requests
from typing import Optional
from requests.exceptions import RequestException

class Notifier:
    def __init__(self, config):
        self.config = config

    def send_telegram(self, message: str, parse_mode: Optional[str] = None) -> bool:
        """
        Send a message to a Telegram chat.
        
        Args:
            message: Text message to send
            parse_mode: Optional formatting mode ('HTML' or 'MarkdownV2')
        
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        # Check if config has required keys
        if not hasattr(self.config, 'TELEGRAM_TOKEN') or not hasattr(self.config, 'TELEGRAM_CHAT_ID'):
            print("❌ Telegram config missing: Need TELEGRAM_TOKEN and TELEGRAM_CHAT_ID")
            return False

        if not all([self.config.TELEGRAM_TOKEN, self.config.TELEGRAM_CHAT_ID]):
            print("❌ Telegram config empty (check .env or config file)")
            return False

        url = f"https://api.telegram.org/bot{self.config.TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": self.config.TELEGRAM_CHAT_ID,
            "text": message,
            "disable_web_page_preview": True,
        }
        
        if parse_mode and parse_mode in ['HTML', 'MarkdownV2']:
            payload['parse_mode'] = parse_mode

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            print("✅ Telegram message sent successfully")
            return True
        except RequestException as e:
            print(f"❌ Telegram API error: {e}")
            return False
# import requests
# from requests.exceptions import RequestException
# from typing import Optional

# class Notifier:
#     def __init__(self, config):
#         self.config = config


#     def send_telegram(self, message: str, parse_mode: Optional[str] = None) -> bool:
#         print("SENDING TELEGRAM MESSAGE")
#         print("Token:", self.config.TELEGRAM_TOKEN)
#         print("Chat ID:", self.config.TELEGRAM_CHAT_ID)
#         """
#         Send a message to a Telegram chat.
        
#         Args:
#             message: Text message to send
#             parse_mode: Optional formatting mode ('HTML' or 'MarkdownV2')
        
#         Returns:
#             bool: True if message was sent successfully, False otherwise
#         """
#         if not all([self.config.TELEGRAM_TOKEN, self.config.TELEGRAM_CHAT_ID]):
#             print("config not there")
#             return False

#         url = f"https://api.telegram.org/bot{self.config.TELEGRAM_TOKEN}/sendMessage"
#         payload = {
#             "chat_id": self.config.TELEGRAM_CHAT_ID,
#             "text": message,
#             "disable_web_page_preview": True,
#         }
        
#         if parse_mode and parse_mode in ['HTML', 'MarkdownV2']:
#             payload['parse_mode'] = parse_mode

#         try:
#             response = requests.post(
#                 url,
#                 json=payload,  # Using json instead of data for better formatting
#                 timeout=10  # 10 second timeout
#             )
#             print(response)
#             response.raise_for_status()  # Raises exception for 4XX/5XX responses
#             return True
#         except RequestException as e:
#             print(f"Telegram API error: {e}")
#             return False
    
#     # def send_telegram(self, message):
#     #     # print(f"TELEGRAM MESSAGE : {message}\n")
#     #     # return True
#     #     if not self.config.TELEGRAM_TOKEN or not self.config.TELEGRAM_CHAT_ID:
#     #         return False

#     #     url = f"https://api.telegram.org/bot{self.config.TELEGRAM_TOKEN}/sendMessage"
#     #     payload = {"chat_id": self.config.TELEGRAM_CHAT_ID, "text": message}
#     #     try:
#     #         response = requests.post(url, data=payload)
#     #         return response.status_code == 200
#     #     except Exception:
#     #         return False


