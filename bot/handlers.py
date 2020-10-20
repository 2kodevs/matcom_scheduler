from bot.utils import is_chat_admin
from telegram.ext import CommandHandler, Filters

ADMINS_ONLY = 'Only admins can use this command, sorry :('
ACTIVE      = 'There is a discussion that needs to be closed before create a new one'
CONFIG      = 'This chat is now available in your private configuration options'

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

create_handler = CommandHandler('create', create, Filters.group)

bot_handlers = [
    create_handler
]
