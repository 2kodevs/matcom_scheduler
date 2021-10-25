from .create import create_handler
from .config import config_handler
from .list import list_group_handler
from .vote import vote_register_handler, vote_select_handler, vote_select_callback, vote_callback
from .start import start_group_handler, start_pv_handler
from .cancel import cancel_handler
from .close import close_handler
from .model_selector import list_models_handler, set_model_handler
from .status import status_group_handler

bot_handlers = [
    create_handler, 
    config_handler,
    # list_group_handler,
    vote_register_handler,
    vote_select_handler,
    vote_select_callback,
    vote_callback,
    start_group_handler,
    start_pv_handler,
    cancel_handler,
    close_handler,
    list_models_handler,
    set_model_handler,
    status_group_handler,
]
