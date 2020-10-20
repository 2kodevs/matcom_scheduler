from bot.utils import is_chat_admin
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, ConversationHandler, MessageHandler

# Messages
ADMINS_ONLY     = 'Only admins can use this command, sorry :('
ACTIVE          = 'There is a discussion that needs to be closed before creating a new one'
CONFIG          = 'This chat is now available in your private configuration options'
NO_CONFIG       = "You don't have any chat to configure.\nYou need to use /create command in some chat first."
SELECT          = 'Select the chat that you want to configure'

# States
SELECT_STATE, ADD_STATE, DEL_STATE = range(3) 

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

def config(update, context):
    if not context.user_data.get('owner'):
        update.message.reply_text(NO_CONFIG)
        return ConversationHandler.END
    
    keyboard = []
    for chat_id in context.user_data['owner']:
        keyboard.append([context.bot.get_chat(chat_id).title])
    update.message.reply_text(
        SELECT, 
        reply_markup=ReplyKeyboardMarkup(
            keyboard, 
            one_time_keyboard=True,
        ),
    )
    return SELECT_STATE

create_handler = CommandHandler('create', create, Filters.group)

bot_handlers = [
    create_handler
]
