import re

from .filters import private_text_filter
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, MessageHandler


NO_ACTIVE = 'No hay una discusión activa en este grupo.'
NO_CONFIG = 'No se ha configurado completamente aún la discusión actual.'
NO_VOTERS = 'La discusión activa en este grupo no tiene votantes aún.'
LIST      = 'En estos momentos han votado: %s personas.'

def status_group_voters(update, context):
    try:
        assert context.chat_data.get('active'), NO_ACTIVE
        assert context.chat_data.get('options'), NO_CONFIG
        assert any(context.chat_data.get('voters', dict()).values()), NO_VOTERS
        voters: dict = context.chat_data['voters']
        cant = sum([1 for _, vote in voters.items() if vote])
        assert False, LIST%cant
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

status_group_handler = CommandHandler( ['status'], status_group_voters, Filters.group)
