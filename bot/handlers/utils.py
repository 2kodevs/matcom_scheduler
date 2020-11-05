import re


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
        del data['options']
    except KeyError:
        pass

def clear_chat(chat, context):
    context.chat_data['active'] = False
    if context.user_data.get('owner'):
        context.user_data['owner'] = [x for x in context.user_data['owner'] if x != chat]
    if context.chat_data.get('voters'):
        users_data = context.dispatcher.user_data
        for idx in context.chat_data['voters'].keys():
            users_data[idx]['voting_in'].remove(chat)
        del context.chat_data['voters']
    if context.chat_data.get('options'):
        del context.chat_data['options']
    del context.chat_data['manager']