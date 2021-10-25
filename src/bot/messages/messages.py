ADMINS_ONLY     = 'Ups!!!, solo los administradores pueden usar este comando :('
ACTIVE_CANCEL   = 'Para cancelar una votación, primero se debe crear una usando /create'
ACTIVE_CLOSE    = 'Para cerrar una votación, primero se debe crear una usando /create'
CANCELED        = 'Votación cancelada satisfactoriamente '
CLOSED          = 'votación cerrada satisfactoriamente '
NO_VOTES        = 'No hay votos, por tanto la votación no puede ser cerrada. Si quiere cancelarla, use /cancel'
NO_CONFIG_PV    = "Usted no tiene ningún chat para configurar.\nNecesita usar el comando /create en algún chat."
SELECT          = 'Seleccione el chat que desea configurar'
OPTIONS         = 'Comience a escribir las opciones en mensajes separados cada una. No repita opciones. Puede utilizar los siguientes 3 comandos auxiliares durante la configuración.\n- /del Para eliminar algunas opciones\n- /add Para continuar añadiendo opciones\n- /done Para guardar la configuración'
WRONG_CHAT      = "Usted no tiene acceso a la configuración del chat que seleccionó :(, utilice /config nuevamente y seleccione algún chat válido."
INVALID_OPTION  = "Ha seleccionado una opción desconocida"
EMPTY           = "La lista de opciones está vacía"
CHOOSE_DEL      = 'Selecione las opciones a eliminar una por una'
CHOOSE_ADD      = 'Continue añadiendo opciones'
USELESS         = "Su configuración ha fallado, utilice /config nuevamente y añada algunas opciones cuando esté listo."
DONE_CONFIG     = 'Perfecto! Ha terminado la configuración.\nUtilice /close en el chat relacionado para cerrar la votación. Si necesita hacer algún cambio debe utilizar /cancel en el chat para cancelar la votación y repetir el procedimiento para la nueva configuración.'
INIT_DISCUSS    = 'Comienza la votación!!!\nUtiliza /vote para participar.\n\nLas opciones a organizar son:\n%s'
BYE             = 'Se ha cancelado la configuración'
ACTIVE_CREATE   = 'Antes de comenzar una nueva votación debe cerrar la actual'
CONFIG          = 'Este chat está disponible ahora en su lista privada de configuración'
NO_ACTIVE = 'No hay una votación activa en este grupo.'
NO_VOTERS = 'La votación activa en este grupo no tiene votantes aún.'
LIST      = 'Los siguientes usuarios han emitido sus votos:\n%s'
STATUS    = 'En estos momentos han votado: %s personas.\n\n'
LIST_MESSAGE = 'Los modelos son las diferentes formas que el bot usa para determinar cúal es el resultado de una votación.\n\nLa lista de modelos disponibles ahora mismo es:\n %s \n\n Actualmente se encuentra seleccionado el modelo: %s.'
NO_REGISTER = 'No encontramos ninguna votación a la que se haya registrado. Escriba /register en el grupo donde la votación haya sido creada para registrarse.'
NO_CONFIG = 'No se ha configurado completamente aún la votación actual.'
REGISTERED = 'Usted a sido registrado como votante. Escriba /vote por privado para emitir su voto.'
START_SELECTION = 'Por favor escoja en que votación desea participar:'
VOTING_IN = 'Usted está votando en la votación del grupo "%s". Marque en las opciones para agregar al final o eliminar la opción seleccionada. Marque cancelar para finalizar su voto. Una vez seleccionadas todas las opciones marque finalizar para emitir su voto.'
VOTING_IN_WHIT_STATE = VOTING_IN + '\n\nSu voto actual es:\n%s'
CANCEL = 'Se ha cancelado su voto en la votación de "%s". Escribe /vote de nuevo para iniciar otra votación.'
CONFIRM = 'Su voto en la votación de "%s" a sido guardado satisfactoriamente. Recuerde que puede volver a ejercer su voto escribiendo /vote aquí nuevamente. Su último voto válido será el considerado al finalizar la votación.\n\nSu voto actual es:\n%s'
INVALID = 'Su voto en "%s" no se a podido emitir correctamente. Esto puede ocurrir por varias razones entre ellas que la votación a la cual hace referencia ya haya finalizado. Escriba /vote para emitir su voto de nuevo en la votación correcta o regístrese nuevamente en su chat usando /register en el grupo origen de la votación.'
NO_VALID    = 'El modelo que intentó activar no es uno válido. Use /models para verificar cuales son los modelos disponibles.'
ACCEPT      = 'El modelo a utilizar ha sido cambiado satisfactoriamente. Use /models para saber más acerca de los modelos.'
INTRO_G = '''
Hola soy un bot de Matcom para votaciones!!!

Puedo ayudar a alcanzar el consenso de un grupo sobre una votación. Especialmente sobre el calendario de pruebas( o mascotas :) ).
Para poder usar el bot, agréguelo a un grupo. Solo los administradores del grupo podrán manejar una votación.

Siendo administrador, use /create para iniciar una votación y luego siga las instrucciones del bot por el chat privado. No olvide usar /close para obtener los resultados!

'''

INTRO_PV = '''
Hola soy un bot de Matcom para votaciones!!!

Puedo ayudar a alcanzar el consenso de un grupo sobre una votación. Especialmente sobre el calendario de pruebas( o mascotas :) ).
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
