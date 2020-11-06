from telegram.ext import CommandHandler

INTRO = '''
Hola soy el bot Matcom Scheduler!!!

Puedo ayudar a alcanzar el concenso de un grupo sobre una planificación. Especialmente sobre el calendario de pruebas.
Para poder usar el bot, agréguelo a un grupo. Solo los administradores del grupo podrán manejar una votación.

Siendo administrador, use /create para iniciar una discusión y luego /config para configurar sus opciones. No olvide usar /close para obtener los resultados!

'''

def start(update, context):
    cmds = "\n".join([f"/{cmd.command} - {cmd.description}" for cmd in context.bot.get_my_commands()])
    update.message.reply_text(INTRO + cmds)

# Handler
start_handler = CommandHandler(['start', 'help'], start)
