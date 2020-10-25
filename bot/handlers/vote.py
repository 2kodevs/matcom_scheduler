from .filters import private_text_filter
from .utils import clean_vote_data, is_chat_admin, get_or_init
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler


NO_ACTIVE = 'No hay discusiones activas en este grupo.'
REGISTERED = 'Usted a sido registrado como votante. Escribeme "/vote" por privado para emitir tu voto.'

def vote_register(update, context):
    '''
    Handler for /vote command
    '''
    user = update.effective_user.id
    user_data = update.effective_user
    chat = update.effective_chat.id
    chat_data = update.effective_chat
    try:
        assert context.chat_data.get('active'), NO_ACTIVE
        voting = get_or_init(user_data, 'voting', set())
        voters = get_or_init(chat_data, 'voters', set())
        voting.add(chat)
        voters.add(user)
        assert False, REGISTERED
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

vote_register_handler = CommandHandler(['vote', 'register'], vote_register, Filters.group)
