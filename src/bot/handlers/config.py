from .filters import private_text_filter
from .utils import clean_config_data, enumerate_options
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Filters, ConversationHandler, MessageHandler

# Messages
NO_CONFIG       = "Usted no tiene ningún chat para configurar.\nNecesita usar el comando /create en algún chat."
SELECT          = 'Seleccione el chat que desea configurar'
OPTIONS         = 'Comience a escribir las opciones en mensajes separados cada una. No repita opciones. Puede utilizar los siguientes 3 comandos auxiliares durante la configuración.\n- /del Para eliminar algunas opciones\n- /add Para continuar añadiendo opciones\n- /done Para guardar la configuración'
WRONG_CHAT      = "Usted no tiene acceso a la configuración del chat que seleccionó :(, utilice /config nuevamente y seleccione algún chat válido."
INVALID_OPTION  = "Ha seleccionado una opción desconocida"
EMPTY           = "La lista de opciones está vacía"
CHOOSE_DEL      = 'Selecione las opciones a eliminar una por una'
CHOOSE_ADD      = 'Continue añadiendo opciones'
USELESS         = "Su configuración ha fallado, utilice /config nuevamente y añada algunas opciones cuando esté listo."
DONE_CONFIG     = 'Perfecto! Ha terminado la configuración.\nUtilice /close en el chat relacionado para cerrar la discusión. Si necesita hacer algún cambio debe utilizar /cancel en el chat para cancelar la discusión y repetir el procedimiento para la nueva configuración.'
INIT_DISCUSS    = 'Comienza la votación!!!\nUtiliza /vote para participar.\n\nLas opciones a organizar son:\n%s'
BYE             = 'Se ha cancelado la configuración'

# States
SELECT_STATE, ADD_STATE, DEL_STATE = range(3) 

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
        context.user_data['options'] = set()
    s = context.user_data['options']

    sz = len(s)
    s.add(option)
    if sz == len(s):
        update.effective_message.reply_text("La opción anterior ya fue añadida previamente")
    else:
        update.effective_message.reply_text("Añadido correctamente")
    return ADD_STATE

def del_options(update, context):
    option = update.effective_message.text
    try:
        idx = context.user_data['options'].remove(option)
    except KeyError:
        update.effective_message.reply_text(INVALID_OPTION)
        return DEL_STATE
    if not context.user_data.get('options'):
        update.effective_user.send_message(EMPTY)
        update.effective_user.send_message(
            CHOOSE_ADD, 
            reply_markup=ReplyKeyboardRemove(),
        )
        return ADD_STATE
    update.effective_message.reply_text(
        "Eliminado correctamente",
        reply_markup=ReplyKeyboardMarkup(
            [[op] for op in context.user_data['options']],
        ),
    )
    return DEL_STATE

def add_command(update, context):
    update.effective_message.reply_text(
        CHOOSE_ADD,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ADD_STATE

def del_command(update, context):
    if not context.user_data.get('options'):
        update.effective_user.send_message(EMPTY)
        update.effective_user.send_message(
            CHOOSE_ADD, 
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
        context.dispatcher.chat_data[chat_id]['options'] = list(options)
        context.user_data['owner'].remove(chat_id)
        text = enumerate_options(options)
        context.bot.send_message(chat_id, INIT_DISCUSS % (text))
    clean_config_data(context.user_data)
    return ConversationHandler.END    

def cancel_config(update, context):
    update.effective_message.reply_text(BYE, reply_markup=ReplyKeyboardRemove())
    clean_config_data(context.user_data)
    return ConversationHandler.END

# Handler
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
    ],
    persistent=True,
    name='config_handler'
)
