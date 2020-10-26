from .create import create_handler
from .config import config_handler
from .list import list_group_handler
from .vote import vote_register_handler, vote_select_handler, vote_select_callback, vote_callback

bot_handlers = [
    create_handler, 
    config_handler,
    list_group_handler,
    vote_register_handler,
    vote_select_handler,
    vote_select_callback,
    vote_callback,
]
