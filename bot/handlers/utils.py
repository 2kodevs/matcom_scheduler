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

#Vote Callback helpers
AADD = 1
AREM = 2
ACAN = 3
ACOM = 4

VOTE_SEL_REGEX = r'VOTESEL\*(.+)\*$'
VOTE_SEL_PATTERN = 'VOTESEL*%s*'
VOTE_REGEX = r'VOTE\*(.+)\*$'
VOTE_PATTERN = 'VOTE*%s*'

def parse_cdata(cdata):
    idx, typex, option = re.findall('^(.+):([1|2|3|4]):(.*)$', cdata)[0]
    return int(idx), int(typex), option

def build_cdata(chat_id, option, typex):
    return VOTE_PATTERN%(f'{chat_id}:{typex}:{option}')

def parse_selected(data: str):
    parts = data.split(':')
    if len(parts) > 1:
        result = re.findall('([0-9]+) - (.*)', parts[-1])
        return [ op for _, op in result ]
    return []
