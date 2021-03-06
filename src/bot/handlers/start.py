from telegram.ext import CommandHandler, Filters

INTRO_G = '''
Hola soy el bot Matcom Trivia!!!

Puedo ayudar a crear quiz dinámicos y ponerlos en práctica en un grupo.
Para poder usar el bot, agréguelo a un grupo. Solo los administradores del grupo podrán manejar un quiz.

Siendo administrador, use /create para iniciar un quiz y luego siga las instrucciones del bot por el chat privado. No olvide usar /close para obtener los resultados!

'''

INTRO_PV = '''
Hola soy el bot Matcom Trivia!!!

Puedo ayudar a crear quiz dinámicos y ponerlos en práctica en un grupo.
Para poder usar el bot, agréguelo a un grupo. Solo los administradores del grupo podrán manejar un quiz.

Siendo administrador, use /create en un grupo para iniciar un quiz y luego /config para configurar sus opciones. Una vez configurada un quiz, los miembros del grupo correspondiente podrán tomar parte. No olvide usar /close para obtener los resultados!

'''

commands_pv = [
        ('start'    , 'Inicia el bot.'),
        ('config'   , 'Configura las opciones del quiz.'),
        ('play'     , 'Toma parte en el quiz actual.'),
        ('cancel'   , 'Cancela una acción en la configuración o el quiz actual si se usa en el grupo.'),
        ('help'     , 'Muestra la ayuda.')
    ]

commands_group = [
        ('start'    , 'Inicia el bot.'),
        ('create'   , 'Crea un nuevo quiz.'),
        ('register' , 'Registrarse para participar en el quiz actual.'),
        ('close'    , 'Cierra el quiz actual.'),
        ('cancel'   , 'Cancela una acción en la configuración o el quiz actual si se usa en el grupo.'),
        ('list'     , 'Lista los usuarios que han terminado el quiz.'),
        ('help'     , 'Muestra la ayuda.'),
    ]

def start_pv(update, context):
    cmds = "\n".join([f"/{cmd[0]} - {cmd[1]}" for cmd in commands_pv])
    update.message.reply_text(INTRO_PV + cmds)

def start_group(update, context):
    cmds = "\n".join([f"/{cmd[0]} - {cmd[1]}" for cmd in commands_group])
    update.message.reply_text(INTRO_G + cmds)

# Handler
start_group_handler = CommandHandler(['start', 'help'], start_group, Filters.group)
start_pv_handler = CommandHandler(['start', 'help'], start_pv, Filters.private)
