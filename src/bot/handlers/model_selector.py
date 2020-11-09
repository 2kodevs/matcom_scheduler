import re

from ...model import models, default_model
from .utils import is_chat_admin
from telegram.ext import CommandHandler, MessageHandler, Filters


SET_MODEL_REGEX = r'^/set_(\w+)'
LIST_MESSAGE = 'Los modelos son las diferentes formas que el bot usa para determinar cual es el calendario resultante de una votación. La lista de modelos disponibles ahora mismo es:\n\n %s \n\n Actualmente se encuentra seleccionado el modelo: %s.'

def build_option(model):
    name = model.__name__
    doc = model.__doc__.replace('\n', ' ')
    return f' {name}: {doc}'

def list_models(update, context):
    """
    Handle for /models

    Show all available models for calendar selection.
    """
    try:
        models_list = '\n'.join([ build_option(model) for model in models ])
        actual_model = context.chat_data.get('model', default_model)
        assert False, LIST_MESSAGE%(models_list, actual_model)
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

ADMINS_ONLY = 'Ups!!!, solo los administradores pueden usar este comando :('
NO_VALID    = 'El modelo que intentó activar no es uno válido. Use /models para verificar cuales son los modelos disponibles.'
ACCEPT      = 'El modelo a utilizar a sido cambiado satisfactoriamente. Use /models para saber mas acerca de los modelos.'

def set_model(update, context):
    """
    Handle for /set_<model>

    Set chat current used model to <model>
    """
    selected_model = ''
    user = update.effective_user.id
    chat = update.effective_chat.id
    try:
        selected_model = re.findall( SET_MODEL_REGEX,update.effective_message.text)[0]
    except:
        pass
    try:
        assert is_chat_admin(context.bot, chat, user), ADMINS_ONLY
        assert not selected_model in [model.__name__ for model in models], NO_VALID
        context.chat_data['model'] = selected_model
        assert False, ACCEPT
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

    

list_models_handler = CommandHandler(['models', 'list_models'], list_models, filters=Filters.group)
set_model_handler = MessageHandler(Filters.group & Filters.regex(SET_MODEL_REGEX), set_model)
