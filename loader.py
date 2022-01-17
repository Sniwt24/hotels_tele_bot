import telebot
import os
from dotenv import load_dotenv
from models import Req


class FinderBot:
    """
    Telegram bot
    """
    def __init__(self) -> None:
        load_dotenv()
        TOKEN = os.getenv('BOT_TOKEN')
        self._bot = telebot.TeleBot(TOKEN, parse_mode=None)

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, bot_id):
        self._bot = bot_id


class API:
    """
    API
    """
    def __init__(self) -> None:
        load_dotenv()
        self._api_key = os.getenv('x-rapidapi-key')

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, bot_id):
        self._api_key = bot_id


"""
Initializing dict for headers, telegram bot and API
"""
query_headers = dict()  # Dict for headers of queries
bot = FinderBot().bot
key = API().api_key

"""
Initializing DataBase and create table 'req' if not exist
"""
Req.create_table(safe=True)
