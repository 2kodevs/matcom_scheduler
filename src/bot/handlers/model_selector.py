import re

from ..messages import ACCEPT, ADMINS_ONLY, LIST_MESSAGE, NO_VALID

from ...model import models, default_model, use_model, ModelError
from .utils import is_chat_admin
from telegram.ext import CommandHandler, MessageHandler, Filters


SET_MODEL_REGEX = r'^/set(\w+)'


def build_option(model):
    name = model.__name__
    doc = model.__doc__
    return f'- {name} /set{name}:\n {doc}'

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


def set_model(update, context):
    """
    Handle for /set<model>

    Set chat current used model to <model>
    """
    selected_model = ''
    user = update.effective_user.id
    chat = update.effective_chat.id
    try:
        selected_model = re.findall( SET_MODEL_REGEX, update.effective_message.text)[0]
    except:
        pass
    try:
        assert is_chat_admin(context.bot, chat, user), ADMINS_ONLY
        try:
            use_model(None, selected_model)
        except ModelError:
            assert False, NO_VALID

        context.chat_data['model'] = selected_model
        assert False, ACCEPT
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

    

list_models_handler = CommandHandler(['models', 'list_models'], list_models, filters=Filters.group)
set_model_handler = MessageHandler(Filters.group & Filters.regex(SET_MODEL_REGEX) & Filters.command, set_model)
