from ...model import use_model
from telegram.ext import CommandHandler, Filters
from .utils import is_chat_admin, clear_chat, enumerate_options, quiz_to_str, custom_quiz_to_str

# Messages
ADMINS_ONLY = 'Ups!!!, solo los administradores pueden usar este comando :('
ACTIVE      = 'Para cancelar un quiz, primero se debe crear uno usando /create'
CLOSED      = 'Quiz cerrado satisfactoriamente '
NO_VOTES    = 'No hay respuestas, por tanto el quiz no puede ser cerrado. Si quiere cancelarlo, use /cancel'

def close(update, context):
    user = update.effective_user.id
    chat = update.effective_chat.id
    try:
        assert is_chat_admin(context.bot, chat, user), ADMINS_ONLY
        assert context.chat_data.get('active'), ACTIVE
        assert any(context.chat_data.get('voters', dict()).values()), NO_VOTES

        get_user_name = lambda idx: update.effective_chat.get_member(idx).user.full_name
        
        quiz : list                   = context.chat_data['quiz']
        participants : list           = [(k, get_user_name(k), v) for k, v in context.chat_data['voters'].items()] #if not any(v)]
        participants_scores           = {}
        quiz_count                    = len(quiz)
        correct_responses_by_question = [[opt[1] for opt in quiz[qi]['options'] if opt[0]] for qi in range(quiz_count)]
        for idx, uname, responses in participants:
            correct = 0
            for qi in range(quiz_count):
                if len(responses[qi]) != len(correct_responses_by_question[qi]): 
                    continue
                correct += all(uresp in correct_responses_by_question[qi] for uresp in responses[qi])
            participants_scores[uname] = correct

        participants_scores_sorted = sorted([(name, score) for name, score in participants_scores.items()], key=lambda e: e[1], reverse=True)
        solution = [f'{name} - {score}' for name, score in participants_scores_sorted]
        sol_msg = 'Los resultados de la ronda es: \n'
        sol_msg += enumerate_options(solution)
        context.bot.send_message(chat_id=chat, text=sol_msg)
        context.bot.send_message(chat_id=chat, text=quiz_to_str(quiz, 'Quiz resuelto:'))

        voters = context.dispatcher.chat_data[chat]['voters']
        for user_id, ans in voters.items():
            new_quiz = custom_quiz_to_str(quiz, ans, validate=True)
            context.bot.send_message(chat_id=user_id, text=quiz_to_str(new_quiz, 'Sus respuestas revisadas:'))

        clear_chat(chat, context)
        assert False, CLOSED
    except AssertionError as e:
        update.effective_message.reply_text(str(e))

# Handler
close_handler = CommandHandler('close', close, Filters.group)
