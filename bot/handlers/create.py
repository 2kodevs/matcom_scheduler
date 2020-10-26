from .filters import private_text_filter
from .utils import is_chat_admin, get_or_init
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler

# Messages
ADMINS_ONLY     = 'Only admins can use this command, sorry :('
ACTIVE          = 'There is a discussion that needs to be closed before creating a new one'
CONFIG          = 'This chat is now available in your private configuration options'

# Handler methods
def create(update, context):
    '''
    Handler for /create command
    '''
    user = update.effective_user.id
    chat = update.effective_chat.id
    try:
        assert is_chat_admin(context.bot, chat, user), ADMINS_ONLY
        assert not context.chat_data.get('active'), ACTIVE
        context.chat_data['active'] = True
        context.chat_data['manager'] = user
        if not context.user_data.get('owner'):
            context.user_data['owner'] = []
        context.user_data['owner'].append(chat)
        assert False, CONFIG
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

# Handler
create_handler = CommandHandler('create', create, Filters.group)
