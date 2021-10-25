import re

from ..messages import ADMINS_ONLY, NO_ACTIVE, NO_CONFIG, NO_VOTERS, STATUS

from ...model import use_model
from .filters import private_text_filter
from .utils import enumerate_options, is_chat_admin, list_options
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, MessageHandler


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
        sol_msg += list_options(solution)
        assert False, (STATUS%cant) + sol_msg
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

status_group_handler = CommandHandler( ['status'], status_group_voters, Filters.group)
