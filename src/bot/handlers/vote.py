import re

from ..messages import CANCEL, CONFIRM, INVALID, NO_ACTIVE, NO_CONFIG, NO_REGISTER, REGISTERED, START_SELECTION, VOTING_IN, VOTING_IN_WHIT_STATE

from .filters import private_text_filter
from .utils import get_or_init, enumerate_options
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, MessageHandler


#Vote Callback helpers
AADD = 1
AREM = 2
ACAN = 3
ACOM = 4

VOTE_SEL_REGEX = r'VOTESEL\*(.+)\*$'
VOTE_SEL_PATTERN = 'VOTESEL*%s*'
VOTE_REGEX = r'VOTE\*(.+)\*$'
VOTE_PATTERN = 'VOTE*%s*'

def vote_parse_cdata(cdata):
    idx, typex, option = re.findall('^(.+):([1|2|3|4]):(.*)$', cdata)[0]
    return int(idx), int(typex), option

def vote_build_cdata(chat_id, option, typex):
    return VOTE_PATTERN%(f'{chat_id}:{typex}:{option}')

def vote_parse_selected(data: str):
    parts = data.split(':')
    if len(parts) > 1:
        result = re.findall('([0-9]+)-\) (.*)', parts[-1])
        return [ op for _, op in result ]
    return []

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
        voters = get_or_init(context.chat_data, 'voters', dict())
        user_id = update.effective_user.id
        if not user_id in voters:
            voters[user_id] = None
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
        cdata = vote_build_cdata(chat_id, option, AADD)
        keyboard.append([InlineKeyboardButton(f'Agregar "{option}"', 
                callback_data=cdata)])
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data=vote_build_cdata(chat_id, '', ACAN))])

    query.edit_message_text(text=VOTING_IN%chat_title)
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))

def voting_callback(update, context):
    query: CallbackQuery = update.callback_query
    query.answer()
    chat_id, operation, option =  vote_parse_cdata(re.findall(VOTE_REGEX, query.data)[0])
    selected = vote_parse_selected(query.message.text)
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
        query.edit_message_text(text=CONFIRM%(chat_title, enumerate_options(selected)))
        return

    keyboard = []
    
    for to_add in left:
        keyboard.append([InlineKeyboardButton(f'Agregar "{to_add}"', 
                callback_data=vote_build_cdata(chat_id, to_add, AADD))])
    
    for to_quit in selected:
        keyboard.append([InlineKeyboardButton(f'Remover "{to_quit}"', 
                callback_data=vote_build_cdata(chat_id, to_quit, AREM))])
    
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data=vote_build_cdata(chat_id, '', ACAN))] + ([] if left else [InlineKeyboardButton('Confirmar', callback_data=vote_build_cdata(chat_id, '', ACOM))]))

    state = enumerate_options(selected)
    msg = VOTING_IN_WHIT_STATE%(chat_title, state) if selected else VOTING_IN%chat_title

    query.edit_message_text(text=msg)
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))



vote_register_handler = CommandHandler(['register', 'vote'], vote_register, Filters.group)
vote_select_callback = CallbackQueryHandler(vote_selection_callback, pattern=VOTE_SEL_REGEX)
vote_select_handler = CommandHandler('vote', vote_selection_handler, Filters.text & Filters.private)
vote_callback = CallbackQueryHandler(voting_callback, pattern=VOTE_REGEX)
