import re

from .filters import private_text_filter
from .utils import get_or_init
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, MessageHandler


NO_ACTIVE = 'No hay una discusion activa en este grupo.'
NO_CONFIG = 'No se ha configurado completamente aun la discusion actual.'
NO_VOTERS = 'La discusion activa en este grupo no tiene votantes aun.'
LIST      = 'Los siguientes usuarios han emitido sus votos:\n%s'

def list_group_voters(update, context):
    try:
        assert context.chat_data.get('active'), NO_ACTIVE
        assert context.chat_data.get('options'), NO_CONFIG
        assert context.chat_data.get('voters'), NO_VOTERS
        voters:dict = context.chat_data['voters']
        get_user_name = lambda idx, vote: context.bot.get_chat(idx).username
        msg_list = '\n'.join([ f'@{get_user_name(voter, vote)}' for voter, vote in voters.items() ])
        assert False, LIST%msg_list
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

list_group_handler = CommandHandler( ['list', 'voters'], list_group_voters, Filters.group)
