from telegram.ext import CommandHandler, Filters

from ..messages import INTRO_G, INTRO_PV, commands_pv, commands_group


def start_pv(update, context):
    cmds = "\n".join([f"/{cmd[0]} - {cmd[1]}" for cmd in commands_pv])
    update.message.reply_text(INTRO_PV + cmds)

def start_group(update, context):
    cmds = "\n".join([f"/{cmd[0]} - {cmd[1]}" for cmd in commands_group])
    update.message.reply_text(INTRO_G + cmds)

# Handler
start_group_handler = CommandHandler(['start', 'help'], start_group, Filters.group)
start_pv_handler = CommandHandler(['start', 'help'], start_pv, Filters.private)
