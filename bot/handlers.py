from .filters import private_text_filter
from .utils import clean_vote_data, is_chat_admin, get_or_init
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler

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

## Vote Conversational Handler

VOTE_START, VOTE_ADD = range(2)

def vote_start(update, context):
    '''
    Handler for /vote command
    '''
    source_id = 0
    try:
        source_id = int(context.args[0])
    except IndexError:
        update.effective_message.reply_text(
            'No se pudo determinar la votación.',
            reply_markup = ReplyKeyboardRemove() 
        )
        return ConversationHandler.END
    source_chat = update.bot.get_chat(source_id)
    source_chat_data = context.dispatcher.chat_data[source_id]
    voter_data = context.user_data

    options = source_chat_data.get('options', [])
    if not options:
        update.effective_message.reply_text(
            'No hay votación activa en %s.'%(source_chat.title),
            reply_markup = ReplyKeyboardRemove() 
        )
        return ConversationHandler.END

    voter_data['source_id'] = source_id
    voter_data['options'] = options
    voter_selected = get_or_init(voter_data, 'selected', [])

    update.effective_message.reply_text(
        'Usted esta votando para la votación del grupo %s. Seleccione a continuacion las opciones \
        en el orden que desee. Use el comando "/list" para ver su seleccion actual.Use el comandos\
         "/remove" si desea desacher su ultima selección. Use le comando "/cancel" para cancelar su voto.\
        Use el comando "/done" para finalizar su votacion.'%(source_chat.title),
        reply_markup=ReplyKeyboardMarkup(
            [[op] for op in options if not op in voter_selected],
            one_time_keyboard=True
        )
    )
    return VOTE_ADD

def vote_add(update, context):
    option = update.effective_message.text
    options = context.user_data['options']
    voter_selected = context.user_data['selected']

    ret_txt = 'Use el comando "/done" para finalizar.'

    if not option in options or option in voter_selected:
        ret_txt = 'La opcion introducida es invalida.'
    elif len(options) > len(voter_selected):
        ret_txt = 'Opcion agregada correctamente.'
        voter_selected.append(option)
    
    update.effective_message.reply_text(
            ret_txt,
            reply_markup=ReplyKeyboardMarkup(
                [[op] for op in options if not op in voter_selected],
                one_time_keyboard=True
            )
        )
    return VOTE_ADD
    
def list_command(update, context):
    options = context.user_data['options']
    voter_selected = context.user_data['selected']
    actual_state = 'Sus opciones seleccionadas en orden son:\n' + '\n'.join([ f'{idx+1} - {op}' for idx, op in enumerate(voter_selected) ])
    update.effective_message.reply_text(
        actual_state,
        reply_markup=ReplyKeyboardMarkup(
                [[op] for op in options if not op in voter_selected],
                one_time_keyboard=True
            )
    )
    return VOTE_ADD

def remove_command(update, context):
    options = context.user_data['options']
    voter_selected = context.user_data['selected']
    ret_txt = 'No hay opciones a eliminar.'
    if voter_selected:
        ret_txt = 'La opcion "%s" fue eliminada.'%voter_selected.pop()
    update.effective_message.reply_text(
        ret_txt,
        reply_markup=ReplyKeyboardMarkup(
                [[op] for op in options if not op in voter_selected],
                one_time_keyboard=True
            )
    )
    return VOTE_ADD

def cancel_command(update, context):
    clean_vote_data(context.user_data)
    update.effective_message.reply_text(
        'Su voto a sido cancelado.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def done_command(update, context):
    source_id = context.user_data['source_id']
    options = context.user_data['options']
    voter_selected = context.user_data['selected']

    if len(voter_selected) == len(options):
        user_id = update.effective_user.id
        context.user_data[source_id] = voter_selected.copy()
        voters = get_or_init(context.dispatcher.chat_data[source_id], 'voters', set())
        voters.add(user_id)
        update.effective_message.reply_text(
        'Su voto a sido guardado.',
        reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    update.effective_message.reply_text(
        'Aun faltan opciones por seleccionar.',
        reply_markup=ReplyKeyboardMarkup(
                [[op] for op in options if not op in voter_selected],
                one_time_keyboard=True
            )
    )
    return VOTE_ADD

vote_handler = ConversationHandler(
    entry_points=[CommandHandler('vote', vote_start, Filters.private)],
    states={
        VOTE_START: [MessageHandler(private_text_filter, vote_start)],
        VOTE_ADD: [MessageHandler(private_text_filter, vote_add)]
    },
    fallbacks=[
        CommandHandler('list', list_command, Filters.private),
        CommandHandler('remove', remove_command, Filters.private),
        CommandHandler('cancel', cancel_command, Filters.private),
        CommandHandler('done', done_command, Filters.private),
    ]
)

bot_handlers = [
    create_handler,
    vote_handler
]
