from .create import create_handler
from .config import config_handler

bot_handlers = [
    create_handler, 
    config_handler,
]
