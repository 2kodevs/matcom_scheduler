from .filters import private_text_filter
from .utils import clean_vote_data, is_chat_admin, get_or_init
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler


NO_ACTIVE = 'No hay una discusion activa en este grupo.'
NO_CONFIG = 'No se ha configurado completamente aun la discusion actual.'
REGISTERED = 'Usted a sido registrado como votante. Escribeme "/vote" por privado para emitir tu voto.'

def vote_register(update, context):
    '''
    Handler for /vote and /register command
    '''
    chat = update.effective_chat.id
    user_data = context.user_data
    try:
        assert context.chat_data.get('active'), NO_ACTIVE
        assert context.chat_data.get('options'), NO_CONFIG
        voting = get_or_init(user_data, 'voting', set())
        voting.add(chat)
        assert False, REGISTERED
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

vote_register_handler = CommandHandler(['vote', 'register'], vote_register, Filters.group)
