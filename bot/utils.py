def is_chat_admin(bot, chat_id, user_id):
    '''
    Check if the given user is
    admin in the given chat
    '''
    for member in bot.get_chat_administrators(chat_id):
        if member.user.id == user_id:
            return True
    return False
