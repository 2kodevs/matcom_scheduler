from telegram.ext import CommandHandler, Filters

INTRO_G = '''
Hola soy el bot Matcom Scheduler!!!

Puedo ayudar a alcanzar el concenso de un grupo sobre una votación. Especialmente sobre el calendario de pruebas( o mascotas :) ).
Para poder usar el bot, agréguelo a un grupo. Solo los administradores del grupo podrán manejar una votación.

Siendo administrador, use /create para iniciar una votación y luego siga las instrucciones del bot por el chat privado. No olvide usar /close para obtener los resultados!

'''

INTRO_PV = '''
Hola soy el bot Matcom Scheduler!!!

Puedo ayudar a alcanzar el concenso de un grupo sobre una votación. Especialmente sobre el calendario de pruebas( o mascotas :) ).
Para poder usar el bot, agréguelo a un grupo. Solo los administradores del grupo podrán manejar una votación.

Siendo administrador, use /create en un grupo para iniciar una votación y luego /config para configurar sus opciones. Una vez configurada una votación, los miembros del grupo correspondiente podrán tomar parte. No olvide usar /close para obtener los resultados!

'''

commands_pv = [
        ('start'    , 'Inicia el bot.'),
        ('config'   , 'Configura las opciones de la discución.'),
        ('vote'     , 'Toma parte en la votación actual.'),
        ('cancel'   , 'Cancela una acción en la configuración o la votación actual si se usa en el grupo.'),
        ('help'     , 'Muestra la ayuda.')
    ]

commands_group = [
        ('start'    , 'Inicia el bot.'),
        ('create'   , 'Crea una nueva votación del calendario.'),
        ('vote'     , 'Registrarse para votar en la votación actual.'),
        ('register' , 'Registrarse para votar en la votación actual.'),
        ('close'    , 'Cierra la votación actual.'),
        ('cancel'   , 'Cancela una acción en la configuración o la votación actual si se usa en el grupo.'),
        ('list'     , 'Lista los usuarios que han votado.'),
        ('status'   , 'Muestra la cantidad de votantes y resultados parciales'),
        ('models'   , 'Lista los modelos disponibles para usar.'),
        ('list_models' , 'Lista los modelos disponibles para usar.'),
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
