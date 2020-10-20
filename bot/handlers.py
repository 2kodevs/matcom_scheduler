from bot.filters import private_text_filter
from bot.utils import is_chat_admin, clean_config_data
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, ConversationHandler, MessageHandler

# Messages
ADMINS_ONLY     = 'Only admins can use this command, sorry :('
ACTIVE          = 'There is a discussion that needs to be closed before creating a new one'
CONFIG          = 'This chat is now available in your private configuration options'
NO_CONFIG       = "You don't have any chat to configure.\nYou need to use /create command in some chat first."
SELECT          = 'Select the chat that you want to configure'
OPTIONS         = 'Start writing the options one by one.\nAdditionally you can use /del to delete some options, or /add to continue adding.\nUse /done at the end'
WRONG_CHAT      = "You don't have any configuration active in the selected chat, sorry :(, try /config again."
INVALID_OPTION  = "I don't have this option, select a valid one"
EMPTY           = "You don't have options to delete"
CHOOSE_DEL      = 'Choose the options to delete one by one'
USELESS         = "You didn't provide any options, try /config again when you are ready"
DONE_CONFIG     = 'Perfect! The options provided by you are not editable.\nType /close in the related chat in order to close the discussion'
INIT_DISCUSS    = 'Time to vote!!!\nSend /vote to participate.\n\nThe options to organize are:\n%s'
BYE             = 'See you soon.'

# States
SELECT_STATE, ADD_STATE, DEL_STATE = range(3) 

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

def select(update, context):
    selection = update.effective_message.text
    for chat_id in context.user_data.get('owner', []):
        if context.bot.get_chat(chat_id).title == selection:
            context.user_data['chat_id'] = chat_id
            update.message.reply_text(
                OPTIONS,
                reply_markup=ReplyKeyboardRemove(),
            )
            return ADD_STATE
    update.effective_message.reply_text(
        WRONG_CHAT,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END
    
def add_options(update, context):
    option = update.effective_message.text
    if not context.user_data.get('options'):
        context.user_data['options'] = []
    context.user_data['options'].append(option)
    update.effective_message.reply_text("Added correctly.")
    return ADD_STATE

def del_options(update, context):
    option = update.effective_message.text
    try:
        idx = context.user_data['options'].index(option)
        context.user_data['options'].pop(idx)
    except ValueError:
        update.effective_message.reply_text(INVALID_OPTION)
        return DEL_STATE
    if not context.user_data['options']:
        update.effective_user.send_message(EMPTY)
        update.effective_user.send_message(
            OPTIONS, 
            reply_markup=ReplyKeyboardRemove(),
        )
        return ADD_STATE
    update.effective_message.reply_text(
        "Deleted correctly.",
        reply_markup=ReplyKeyboardMarkup(
            [[op] for op in context.user_data['options']],
        ),
    )
    return DEL_STATE

def add_command(update, context):
    update.effective_message.reply_text(
        OPTIONS,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ADD_STATE

def del_command(update, context):
    if not context.user_data.get('options'):
        update.effective_user.send_message(EMPTY)
        update.effective_user.send_message(
            OPTIONS, 
            reply_markup=ReplyKeyboardRemove(),
        )
        return ADD_STATE
    update.effective_user.send_message(
        CHOOSE_DEL,
        reply_markup=ReplyKeyboardMarkup(
            [[op] for op in context.user_data['options']],
        )
    )
    return DEL_STATE
    
def done_command(update, context):
    if not context.user_data.get('options'):
        update.effective_user.send_message(
            USELESS, 
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        update.effective_user.send_message(
            DONE_CONFIG, 
            reply_markup=ReplyKeyboardRemove()
        )
        chat_id = context.user_data['chat_id']
        options = context.user_data['options']
        context.dispatcher.chat_data[chat_id]['options'] = options
        idx = context.user_data['owner'].index(chat_id)
        context.user_data['owner'].pop(idx)
        text = '\n'.join(f'{i + 1}-) {op}' for i, op in enumerate(options))
        context.bot.send_message(chat_id, INIT_DISCUSS % (text))
    clean_config_data(context.user_data)
    return ConversationHandler.END    

def cancel_config(update, context):
    update.effective_message.reply_text(BYE, reply_markup=ReplyKeyboardRemove())
    clean_config_data(context.user_data)
    return ConversationHandler.END

# Handlers
create_handler = CommandHandler('create', create, Filters.group)

config_handler = ConversationHandler(
    entry_points=[CommandHandler('config', config, Filters.private)],
    states={
        SELECT_STATE: [MessageHandler(private_text_filter, select)],
        ADD_STATE: [MessageHandler(private_text_filter, add_options)],
        DEL_STATE: [MessageHandler(private_text_filter, del_options)],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_config, Filters.private),
        CommandHandler('add', add_command, Filters.private),
        CommandHandler('del', del_command, Filters.private),
        CommandHandler('done', done_command, Filters.private),
    ]
)

# Handlers List
bot_handlers = [
    create_handler, 
    config_handler,
]
