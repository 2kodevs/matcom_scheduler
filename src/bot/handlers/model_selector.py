from ...model import models, default_model
from .utils import is_chat_admin
from telegram.ext import CommandHandler, Filters


LIST_MESSAGE = 'Esta es la lista de módelos a usar para la selección del calendario:\n\n %s \n\n Actualmente se encuentra seleccionado el modelo: %s.'

def list_models(update, context):
    """
    Handle for /models

    Show all available models for calendar selection.
    """
    try:
        models_list = '\n'.join((f'{model.__name__}: "{model.__doc__}"' for model in models ))
        actual_model = context.chat_data.get('model', default_model)
        assert False, LIST_MESSAGE%(models_list, actual_model)
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

list_models_handler = CommandHandler(['models', 'list_models'], list_models, filters=Filters.group)
