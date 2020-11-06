import re

from .filters import private_text_filter
from .utils import get_or_init, enumerate_options
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, MessageHandler


NO_ACTIVE = 'No hay una discusión activa en este grupo.'
NO_CONFIG = 'No se ha configurado completamente aún la discusión actual.'
NO_VOTERS = 'La discusión activa en este grupo no tiene votantes aún.'
LIST      = 'Los siguientes usuarios han emitido sus votos:\n%s'

def list_group_voters(update, context):
    try:
        assert context.chat_data.get('active'), NO_ACTIVE
        assert context.chat_data.get('options'), NO_CONFIG
        assert any(context.chat_data.get('voters', dict()).values()), NO_VOTERS
        voters:dict = context.chat_data['voters']
        get_user_name = lambda idx: update.effective_chat.get_member(idx).user.full_name
        msg_list = enumerate_options([f'{get_user_name(voter)}' for voter, vote in voters.items() if vote])
        assert False, LIST%msg_list
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

list_group_handler = CommandHandler( ['list', 'voters'], list_group_voters, Filters.group)
