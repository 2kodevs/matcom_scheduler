import json
import re

from .filters import private_text_filter
from .utils import clean_vote_data, is_chat_admin, get_or_init
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, MessageHandler

VOTE_SEL_REGEX = r'VOTESEL\*(.+)\*$'
VOTE_SEL_PATTERN = 'VOTESEL*%s*'
VOTE_REGEX = r'VOTE\*(.+)\*$'
VOTE_PATTERN = 'VOTE*%s*'
NO_ACTIVE = 'No hay una discusion activa en este grupo.'
NO_REGISTER = 'No encontramos ninguna discusion a la que se haya registrado. Escriba /register en el grupo donde la discusion haya sido creada para registrarse.'
NO_CONFIG = 'No se ha configurado completamente aun la discusion actual.'
REGISTERED = 'Usted a sido registrado como votante. Escribeme /vote por privado para emitir tu voto.'
START_SELECTION = 'Por favor escoja en que discusion desea participar:'
VOTING_IN = 'Usted esta votando en la discusion del grupo "%s". Marque en las opciones para agregar al final o eliminar la opcion seleccionada. Marque cancelar para finalizar su voto. Una vez seleccionadas todas las opciones marque finalizar para emitir su voto.'
VOTING_IN_WHIT_STATE = VOTING_IN + '\n\nSu voto actual es:\n%s'
CANCEL = 'Se ha cancelado su voto en la discusion de "%s". Escribe /vote de nuevo para iniciar otra votacion.'
CONFIRM = 'Su voto en la discusion de "%s" a sido guardado satisfactoriamente. Recuerde que puede volver a ejercer su voto escribiendo /vote aqui nuevamente. Su ultimo voto valido sera el considerado al finalizar la discusion.'

#Callback helpers
AADD = 1
AREM = 2
ACAN = 3
ACOM = 4

def parse_cdata(cdata):
    idx, typex, option = re.findall('^(.+):([1|2|3|4]):(.*)$', cdata)[0]
    return int(idx), int(typex), option

def build_cdata(chat_id, option, typex):
    return VOTE_PATTERN%(f'{chat_id}:{typex}:{option}')

def vote_register(update, context):
    '''
    Handler for /vote and /register command
    '''
    chat = update.effective_chat.id
    user_data = context.user_data
    try:
        assert context.chat_data.get('active'), NO_ACTIVE
        assert context.chat_data.get('options'), NO_CONFIG
        voting = get_or_init(user_data, 'voting_in', dict())
        voting[chat] = None
        assert False, REGISTERED
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

def vote_selection_handler(update, context):
    user_data = context.user_data
    chats = user_data.get('voting_in', dict())
    if not chats:
        update.effective_message.reply_text(NO_REGISTER)
        return

    keyboard = []
    for chat in chats:
        if chats[chat] is None:
            keyboard.append([InlineKeyboardButton(context.bot.get_chat(chat).title, callback_data=VOTE_SEL_PATTERN%chat)])

    update.effective_message.reply_text(START_SELECTION, reply_markup=InlineKeyboardMarkup(keyboard))


def vote_selection_callback(update, context):
    query = update.callback_query
    query.answer()
    chat_id = json.loads(re.findall(VOTE_SEL_REGEX, query.data)[0])
    chat_title = context.bot.get_chat(chat_id).title
    options = context.dispatcher.chat_data[chat_id]['options']
    context.user_data['voting_in'][chat_id] = []
    keyboard = []
    for option in options:
        cdata = build_cdata(chat_id, option, AADD)
        keyboard.append([InlineKeyboardButton(f'Agregar "{option}"', 
                callback_data=cdata)])
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data=build_cdata(chat_id, '', ACAN))])

    query.edit_message_text(text=VOTING_IN%chat_title)
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))


def voting_callback(update, context):
    query = update.callback_query
    query.answer()
    chat_id, operation, option =  parse_cdata(re.findall(VOTE_REGEX, query.data)[0])
    selected = context.user_data['voting_in'][chat_id]
    
    if operation == AADD:
        selected.append(option)

    if operation == AREM:
        selected.remove(option)
    
    options = context.dispatcher.chat_data[chat_id]['options']
    left = [op for op in options if not op in selected]
    chat_title = context.bot.get_chat(chat_id).title

    if operation == ACAN:
        query.edit_message_text(text=CANCEL%chat_title)
        # query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        return

    if operation == ACOM:
        voters = get_or_init(context.dispatcher.chat_data[chat_id], 'voters', dict())
        user_id = update.effective_user.id
        voters[user_id] = selected
        clean_vote_data(context.user_data['voting_in'][chat_id])
        query.edit_message_text(text=CONFIRM%chat_title)
        # query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        return

    keyboard = []
    
    for to_add in left:
        keyboard.append([InlineKeyboardButton(f'Agregar "{to_add}"', 
                callback_data=build_cdata(chat_id, to_add, AADD))])
    
    for to_quit in selected:
        keyboard.append([InlineKeyboardButton(f'Remover "{to_quit}"', 
                callback_data=build_cdata(chat_id, to_quit, AREM))])
    
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data=build_cdata(chat_id, '', ACAN))] + ([] if left else [InlineKeyboardButton('Confirmar', callback_data=build_cdata(chat_id, '', ACOM))]))

    state = '\n'.join([ f'{idx} - {option}' for idx, option in enumerate(selected) ])
    msg = VOTING_IN_WHIT_STATE%(chat_title, state) if selected else VOTING_IN%chat_title

    query.edit_message_text(text=msg)
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))



vote_register_handler = CommandHandler(['register', 'vote'], vote_register, Filters.group)
vote_select_callback = CallbackQueryHandler(vote_selection_callback, pattern=VOTE_SEL_REGEX)
vote_select_handler = CommandHandler('vote', vote_selection_handler, Filters.text & Filters.private)
vote_callback = CallbackQueryHandler(voting_callback, pattern=VOTE_REGEX)
