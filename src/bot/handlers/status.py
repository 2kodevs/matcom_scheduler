import re

from ...model import use_model
from .filters import private_text_filter
from .utils import enumerate_options, is_chat_admin
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, MessageHandler


ADMINS_ONLY     = 'Ups!!!, solo los administradores pueden usar este comando :('
NO_ACTIVE = 'No hay una votación activa en este grupo.'
NO_CONFIG = 'No se ha configurado completamente aún la votación actual.'
NO_VOTERS = 'La votación activa en este grupo no tiene votantes aún.'
LIST      = 'En estos momentos han votado: %s personas.\n\n'

def status_group_voters(update, context):
    user = update.effective_user.id
    chat = update.effective_chat.id
    try:
        assert is_chat_admin(context.bot, chat, user), ADMINS_ONLY
        assert context.chat_data.get('active'), NO_ACTIVE
        assert context.chat_data.get('options'), NO_CONFIG
        assert any(context.chat_data.get('voters', dict()).values()), NO_VOTERS
        voters: dict = context.chat_data['voters']
        cant = sum([1 for _, vote in voters.items() if vote])
        votes = [v for v in context.chat_data['voters'].values() if v]
        model = context.chat_data.get('model')
        solution = use_model(votes, model)
        sol_msg = 'Los resultados parciales de la votación son: \n'
        sol_msg += enumerate_options(solution)
        assert False, (LIST%cant) + sol_msg
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

status_group_handler = CommandHandler( ['status'], status_group_voters, Filters.group)
