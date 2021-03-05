import re

emoji = ['❌', '✅']

def is_chat_admin(bot, chat_id, user_id):
    '''
    Check if the given user is
    admin in the given chat
    '''
    for member in bot.get_chat_administrators(chat_id):
        if member.user.id == user_id:
            return True
    return False

def get_or_init(d: dict, key, default):
    result = None
    try:
        result = d[key]
    except KeyError:
        result = d[key] = default
    return result

def clean_config_data(data):
    try:
        del data['chat_id']
        del data['quiz']
        del data['cur']
        del data['option']
    except KeyError:
        pass

def clear_chat(chat, context):
    context.chat_data['active'] = False
    manager = context.chat_data['manager']
    manager_data = context.dispatcher.user_data[manager]
    if manager_data.get('owner'):
        manager_data['owner'] = [x for x in manager_data['owner'] if x != chat]
    if context.chat_data.get('voters'):
        users_data = context.dispatcher.user_data
        for idx in context.chat_data['voters'].keys():
            users_data[idx]['voting_in'].remove(chat)
        del context.chat_data['voters']
    if context.chat_data.get('options'):
        del context.chat_data['options']
    del context.chat_data['manager']

def enumerate_options(options):
    return '\n'.join(f'{i + 1}-) {op}' for i, op in enumerate(options))

def question_to_str(question, options):
    return "%s:\n%s\n" % (question, '\n'.join(f'{emoji[v]} {op}' for v, op in options))

def quiz_to_str(quiz):
    text = ["Preguntas del Quiz\n"]
    for query in quiz:
        text.append(question_to_str(**query))
    return '\n'.join(text)
