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

def clean_vote_data(data):
    try:
        del data['source_id']
        del data['options']
        del data['selected']
    except KeyError:
        pass
