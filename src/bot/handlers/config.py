import re
from .filters import private_text_filter
from .utils import clean_config_data, enumerate_options, get_or_init, emoji, quiz_to_str
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Filters, ConversationHandler, MessageHandler, CallbackQueryHandler

# Messages
NO_CONFIG       = "Usted no tiene ningún chat para configurar.\nNecesita usar el comando /create en algún chat."
SELECT          = 'Seleccione el chat que desea configurar'
QUESTION        = 'Introduzca una pregunta.'
OPTIONS         = 'Comience a escribir las opciones en mensajes separados cada una. No repita opciones. Puede utilizar los siguientes 3 comandos auxiliares durante la configuración.\n- /del Para eliminar algunas opciones\n- /add Para continuar añadiendo opciones\n- /done Para terminar la pregunta actual'
WRONG_CHAT      = "Usted no tiene acceso a la configuración del chat que seleccionó :(, utilice /config nuevamente y seleccione algún chat válido."
INVALID_OPTION  = "Ha seleccionado una opción desconocida"
EMPTY           = "La lista de opciones está vacía"
CHOOSE_DEL      = 'Selecione las opciones a eliminar una por una'
CHOOSE_ADD      = 'Añada una nueva opción'
USELESS         = "Su configuración ha fallado, utilice /config nuevamente y añada algunas opciones cuando esté listo."
DONE_CONFIG     = 'Perfecto! Ha terminado la configuración.\nUtilice /close en el chat relacionado para cerrar la discusión. Si necesita hacer algún cambio debe utilizar /cancel en el chat para cancelar la discusión y repetir el procedimiento para la nueva configuración.'
INIT_DISCUSS    = 'Comienza la votación!!!\nUtiliza /register para participar.\n\n%s'
BYE             = 'Se ha cancelado la configuración'

END_QUIZ_RE         = r'END\*\*$'
END_QUIZ_PATTERN    =  'END**'
ADD_QUERY_RE        = r'ADD\*\*$'
ADD_QUERY_PATTERN   =  'ADD**'
OPT_TYPE_RE         = r'TYPE\*(.+)\*$'
OPT_TYPE_PATTERN    =  'TYPE*%d*'

# States
SELECT_STATE, QUESTION_STATE, ADD_STATE, DEL_STATE, TYPE_STATE, FINAL_STATE = range(6) 

# Handler methods
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
                QUESTION,
                reply_markup=ReplyKeyboardRemove(),
            )
            return QUESTION_STATE
    update.effective_message.reply_text(
        WRONG_CHAT,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END
    
def question(update, context):
    q = update.effective_message.text
    quiz = get_or_init(context.user_data, 'quiz', [])
    quiz.append({
        'question': q,
        'options': [],
    })
    context.user_data['cur'] = quiz[-1]
    return new_option(update.effective_user, OPTIONS)

def new_option(user, msg):
    user.send_message(msg, reply_markup=ReplyKeyboardRemove())
    return ADD_STATE

def add_options(update, context):
    context.user_data['option'] = update.effective_message.text

    update.effective_message.reply_text(
        f"Seleccione el tipo de su opción.",
        reply_markup=InlineKeyboardMarkup.from_column([
                InlineKeyboardButton(f'Correcta {emoji[1]}', callback_data=OPT_TYPE_PATTERN%1),
                InlineKeyboardButton(f'Incorrecta {emoji[0]}', callback_data=OPT_TYPE_PATTERN%0),
            ]
        )
    )
    return TYPE_STATE

def type_callback(update, context):
    query = update.callback_query
    query.answer()
    valid = int(re.findall(OPT_TYPE_RE, query.data)[0])
    query.edit_message_text(
        'Opción %s' % ['Incorrecta', 'Correcta'][valid],
        reply_markup=None,
    )
    context.user_data['cur']['options'].append((valid, context.user_data['option']))
    return new_option(query.from_user, CHOOSE_ADD)

def new_deletion(context, message, text):
    options = context.user_data.get('cur', {}).get('options', [])
    if not options:
        update.effective_user.send_message(EMPTY)
        return add_command(update, context)
    message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            [[f'{emoji[v]} {op}'] for v, op in options],
        ),
    )
    return DEL_STATE

def del_options(update, context):
    text = update.effective_message.text
    try: 
        valid = emoji.index(text[0])
        context.user_data['cur']['options'].remove((valid, text[2:]))
    except ValueError:
        update.effective_message.reply_text(INVALID_OPTION)
        return DEL_STATE
    return new_deletion(context, update.effective_message, 'Eliminado correctamente')

def add_command(update, context):
    return new_option(update.effective_user, CHOOSE_ADD)

def del_command(update, context):
    return new_deletion(context, update.effective_message, CHOOSE_DEL)
    
def done_command(update, context):
    try:
        assert context.user_data.get('quiz', [])
    except AssertionError:
        update.effective_user.send_message('Su quiz esta vacio aún.')
        update.effective_user.send_message(QUESTION)
        return QUESTION_STATE
    try:
        assert context.user_data['cur'].get('options', [])
        update.effective_user.send_message(
            '¿Qué desea hacer?',
            reply_markup=InlineKeyboardMarkup.from_column([
                InlineKeyboardButton('Terminar Quiz',   callback_data=END_QUIZ_PATTERN),
                InlineKeyboardButton('Añadir pregunta', callback_data=ADD_QUERY_PATTERN),
            ])
        )
        return FINAL_STATE
    except AssertionError:
        update.effective_user.reply_text('Su última pregunta aún no tiene opciónes')
        return add_command(update, context)

def end_quiz_callback(update, context):
    query = update.callback_query
    query.answer()
    
    update.effective_user.send_message(quiz_to_str(context.user_data['quiz'], "Preguntas del Quiz"))
    update.effective_user.send_message(DONE_CONFIG)
    chat_id = context.user_data['chat_id']
    quiz = context.user_data['quiz']
    context.dispatcher.chat_data[chat_id]['quiz'] = quiz
    context.user_data['owner'].remove(chat_id)
    text = quiz_to_str(quiz, "El quiz es:", lambda x : 2)
    context.bot.send_message(chat_id, INIT_DISCUSS % (text))
    clean_config_data(context.user_data)
    return ConversationHandler.END    

def add_query_callback(update, context):
    query = update.callback_query
    query.answer()

    update.callback_query.from_user.send_message(QUESTION)
    return QUESTION_STATE

def cancel_config(update, context):
    update.effective_message.reply_text(BYE, reply_markup=ReplyKeyboardRemove())
    clean_config_data(context.user_data)
    return ConversationHandler.END

# Handler
config_handler = ConversationHandler(
    entry_points=[CommandHandler('config', config, Filters.private)],
    states={
        SELECT_STATE:   [MessageHandler(private_text_filter, select)],
        QUESTION_STATE: [MessageHandler(private_text_filter, question)],
        ADD_STATE:      [MessageHandler(private_text_filter, add_options)],
        DEL_STATE:      [MessageHandler(private_text_filter, del_options)],
        TYPE_STATE:     [CallbackQueryHandler(type_callback, pattern=OPT_TYPE_RE)],
        FINAL_STATE:    [
            CallbackQueryHandler(end_quiz_callback, pattern=END_QUIZ_RE),
            CallbackQueryHandler(add_query_callback, pattern=ADD_QUERY_RE),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_config, Filters.private),
        CommandHandler('add', add_command, Filters.private),
        CommandHandler('del', del_command, Filters.private),
        CommandHandler('done', done_command, Filters.private),
    ],
    persistent=True,
    name='config_handler'
)
