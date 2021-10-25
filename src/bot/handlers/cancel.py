from ..messages import ACTIVE_CANCEL, ADMINS_ONLY, CANCELED
from .utils import is_chat_admin, clear_chat
from telegram.ext import CommandHandler, Filters


def cancel(update, context):
    user = update.effective_user.id
    chat = update.effective_chat.id
    try:
        assert is_chat_admin(context.bot, chat, user), ADMINS_ONLY
        assert context.chat_data.get('active'), ACTIVE_CANCEL
        clear_chat(chat, context)
        assert False, CANCELED
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

# Handler
cancel_handler = CommandHandler('cancel', cancel, Filters.group)
