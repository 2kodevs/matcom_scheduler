import re

from .filters import private_text_filter
from .utils import get_or_init, build_cdata, parse_cdata, parse_selected,\
    VOTE_PATTERN, VOTE_REGEX, VOTE_SEL_PATTERN, VOTE_SEL_REGEX,AADD, ACAN, ACOM, AREM
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, MessageHandler


NO_ACTIVE = 'No hay una discusion activa en este grupo.'
NO_REGISTER = 'No encontramos ninguna discusion a la que se haya registrado. Escriba /register en el grupo donde la discusion haya sido creada para registrarse.'
NO_CONFIG = 'No se ha configurado completamente aun la discusion actual.'
REGISTERED = 'Usted a sido registrado como votante. Escriba /vote por privado para emitir su voto.'
START_SELECTION = 'Por favor escoja en que discusion desea participar:'
VOTING_IN = 'Usted esta votando en la discusion del grupo "%s". Marque en las opciones para agregar al final o eliminar la opcion seleccionada. Marque cancelar para finalizar su voto. Una vez seleccionadas todas las opciones marque finalizar para emitir su voto.'
VOTING_IN_WHIT_STATE = VOTING_IN + '\n\nSu voto actual es:\n%s'
CANCEL = 'Se ha cancelado su voto en la discusion de "%s". Escribe /vote de nuevo para iniciar otra votacion.'
CONFIRM = 'Su voto en la discusion de "%s" a sido guardado satisfactoriamente. Recuerde que puede volver a ejercer su voto escribiendo /vote aqui nuevamente. Su ultimo voto valido sera el considerado al finalizar la discusion.'
INVALID = 'Su voto no se a podido emitir correctamente. Esto puede ocurrir por varias razones entre ellas que la votacion a la cual hace referencia ya haya finalizado. Escriba /vote para emitir su voto de nuevo en la votacion correcta o registrese nuevamente en su chat usando /register en el grupo origen de la discusion.'


def vote_register(update, context):
    '''
    Handler for /vote and /register command
    '''
    chat = update.effective_chat.id
    user_data = context.user_data
    try:
        assert context.chat_data.get('active'), NO_ACTIVE
        assert context.chat_data.get('options'), NO_CONFIG
        voting = get_or_init(user_data, 'voting_in', set())
        voting.add(chat)
        assert False, REGISTERED
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

def vote_selection_handler(update, context):
    user_data = context.user_data
    chats = user_data.get('voting_in', set())
    if not chats:
        update.effective_message.reply_text(NO_REGISTER)
        return

    keyboard = []

    for chat in chats:
        keyboard.append([InlineKeyboardButton(context.bot.get_chat(chat).title, callback_data=VOTE_SEL_PATTERN%chat)])

    update.effective_message.reply_text(START_SELECTION, reply_markup=InlineKeyboardMarkup(keyboard))
    
def vote_selection_callback(update, context):
    query = update.callback_query
    query.answer()
    chat_id = int(re.findall(VOTE_SEL_REGEX, query.data)[0])
    chat_title = context.bot.get_chat(chat_id).title
    options = context.dispatcher.chat_data[chat_id]['options']
    keyboard = []
    for option in options:
        cdata = build_cdata(chat_id, option, AADD)
        keyboard.append([InlineKeyboardButton(f'Agregar "{option}"', 
                callback_data=cdata)])
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data=build_cdata(chat_id, '', ACAN))])

    query.edit_message_text(text=VOTING_IN%chat_title)
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))


def voting_callback(update, context):
    query: CallbackQuery = update.callback_query
    query.answer()
    chat_id, operation, option =  parse_cdata(re.findall(VOTE_REGEX, query.data)[0])
    selected = parse_selected(query.message.text)
    chat_title = context.bot.get_chat(chat_id).title
    
    if operation == AADD:
        selected.append(option)

    if operation == AREM:
        try:
            selected.remove(option)
        except ValueError:
            try:
                context.user_data['voting_in'].remove(chat_id)
            except KeyError:
                pass
            query.edit_message_text(text=INVALID%chat_title)
            return

    options = context.dispatcher.chat_data[chat_id].get('options', [])
    if any([not op in options for op in selected ]):
        try:
            context.user_data['voting_in'].remove(chat_id)
        except KeyError:
            pass
        query.edit_message_text(text=INVALID%chat_title)
        return
    left = [op for op in options if not op in selected]

    if operation == ACAN:
        query.edit_message_text(text=CANCEL%chat_title)
        return

    if operation == ACOM:
        voters = get_or_init(context.dispatcher.chat_data[chat_id], 'voters', dict())
        user_id = update.effective_user.id
        voters[user_id] = selected
        context.user_data['voting_in'][chat_id] = None
        query.edit_message_text(text=CONFIRM%chat_title)
        return

    keyboard = []
    
    for to_add in left:
        keyboard.append([InlineKeyboardButton(f'Agregar "{to_add}"', 
                callback_data=build_cdata(chat_id, to_add, AADD))])
    
    for to_quit in selected:
        keyboard.append([InlineKeyboardButton(f'Remover "{to_quit}"', 
                callback_data=build_cdata(chat_id, to_quit, AREM))])
    
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data=build_cdata(chat_id, '', ACAN))] + ([] if left else [InlineKeyboardButton('Confirmar', callback_data=build_cdata(chat_id, '', ACOM))]))

    state = '\n'.join([ f'{idx+1} - {option}' for idx, option in enumerate(selected) ])
    msg = VOTING_IN_WHIT_STATE%(chat_title, state) if selected else VOTING_IN%chat_title

    query.edit_message_text(text=msg)
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))



vote_register_handler = CommandHandler(['register', 'vote'], vote_register, Filters.group)
vote_select_callback = CallbackQueryHandler(vote_selection_callback, pattern=VOTE_SEL_REGEX)
vote_select_handler = CommandHandler('vote', vote_selection_handler, Filters.text & Filters.private)
vote_callback = CallbackQueryHandler(voting_callback, pattern=VOTE_REGEX)
