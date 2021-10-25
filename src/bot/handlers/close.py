from ...model import use_model
from telegram.ext import CommandHandler, Filters
from .utils import is_chat_admin, clear_chat, enumerate_options, list_options

# Messages
ADMINS_ONLY     = 'Ups!!!, solo los administradores pueden usar este comando :('
ACTIVE          = 'Para cancelar una votación, primero se debe crear una usando /create'
CLOSED          = 'votación cerrada satisfactoriamente '
NO_VOTES        = 'No hay votos, por tanto la votación no puede ser cerrada. Si quiere cancelarla, use /cancel'

def close(update, context):
    user = update.effective_user.id
    chat = update.effective_chat.id
    try:
        assert is_chat_admin(context.bot, chat, user), ADMINS_ONLY
        assert context.chat_data.get('active'), ACTIVE
        assert any(context.chat_data.get('voters', dict()).values()), NO_VOTES

        votes = [v for v in context.chat_data['voters'].values() if v]
        model = context.chat_data.get('model')
        solution = use_model(votes, model)
        sol_msg = 'Los resultados de la votación son: \n'
        sol_msg += list_options(solution)
        context.bot.send_message(chat_id=chat, text=sol_msg)

        clear_chat(chat, context)
        assert False, CLOSED
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

# Handler
close_handler = CommandHandler('close', close, Filters.group)
