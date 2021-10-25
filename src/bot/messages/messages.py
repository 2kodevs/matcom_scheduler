ADMINS_ONLY     = '¡Ups! Solo los administradores del grupo pueden utilizar este comando ☹️'
ACTIVE_CANCEL   = ' 🤷 No hay ninguna votación activa en estos momentos, cree una escribiendo aquí /create.'
ACTIVE_CLOSE    = '🤷 No hay ninguna votación activa en estos momentos, cree una escribiendo aquí /create.'
CANCELED        = '❌ Votación cancelada satisfactoriamente.'
CLOSED          = '✅ Votación cerrada satisfactoriamente.'
NO_VOTES        = '🚫 Las votaciones sin votos no pueden ser cerradas. Si quiere cancelar la votación, escriba aquí /cancel.'
NO_CONFIG_PV    = "⚠️ Usted no tiene acceso a la configuración de ninguna votación en este momento. Use el comando /create en el grupo donde desea realizar la votación."
SELECT          = '📍Seleccione el grupo donde tendrá lugar la votación que desea configurar.'
OPTIONS         = '❓Escriba las opciones de la encuesta, cada una en un mensaje separado. Debe escribir al menos una opción. No repita opciones.\n\n📍Puede utilizar los siguientes comandos auxiliares durante la configuración.\n- /del para eliminar algunas opciones\n- /add para continuar añadiendo opciones luego de haber eliminado algunas.\n- /done para guardar la configuración.\n\n❗️Después de guardar la configuración, no podrá editar las opciones de la encuesta.'
WRONG_CHAT      = "⚠️ Usted no tiene acceso a la configuración de ninguna votación en el grupo que seleccionó. Escriba /config nuevamente y seleccione algún grupo válido."
INVALID_OPTION  = "🤷 Ha seleccionado una opción desconocida."
EMPTY           = "🚫 La lista de opciones de la encuesta está vacía actualmente."
CHOOSE_DEL      = '📍Selecione las opciones que desea eliminar, una por una.'
CHOOSE_ADD      = '📍Por favor, continúe añadiendo opciones.'
USELESS         = "⚠️ Su configuración ha fallado, escriba /config nuevamente para reiniciarla. Recuerde añadir al menos una opción a la encuesta."
DONE_CONFIG     = '✅ ¡Perfecto! Usted ha terminado de configurar la votación.\n\n❓Utilice /close en el grupo donde tiene lugar la votación para cerrarla. Si necesita hacer algún cambio, debe cancelar la votación escribiendo /cancel en el grupo donde tiene lugar y configurar una nueva votación repetiendo el procedimiento.'
INIT_DISCUSS    = '🎊 ¡Comienza la votación! Escriba aquí /vote para participar.\n\nLas opciones a organizar son:\n%s'
BYE             = '❌ Se ha descartado la configuración en curso.'
ACTIVE_CREATE   = '⚠️ Antes de comenzar una nueva votación en este grupo, debe cerrar la que está teniendo lugar actualmente.'
CONFIG          = '✅ La votación de este grupo está disponible ahora en su lista privada de configuración.\n\n❓Escriba /config en el chat privado con este bot para configurar las opciones de la encuesta.'
NO_ACTIVE = '🤷 No hay ninguna votación activa en este grupo actualmente.'
NO_VOTERS = '🚫 La votación activa en este grupo no tiene votantes aún.'
LIST      = '📍Los siguientes usuarios han emitido sus votos:\n%s'
STATUS    = '❗️Hasta el momento, han votado %s personas.\n\n'
LIST_MESSAGE = '📊 Los modelos son los diferentes algoritmos que el bot utiliza para determinar el resultado final de una votación.\n\n📍La lista de los modelos disponibles en este momento es:\n %s \n\n❗️Actualmente se encuentra seleccionado el modelo: %s.'
NO_REGISTER = '🤷 No se ha encontrado ninguna votación en la que se encuentre registrado. Escriba /register o /vote en el grupo donde esté teniendo lugar la votación en la que desea participar.'
NO_CONFIG = '⚠️ La votación actual aún no se ha configurado completamente.'
REGISTERED = '🙋 Usted ha sido registrado como votante. Escriba /vote en el chat privado con este bot para emitir su voto.'
START_SELECTION = '📍Seleccione el grupo donde esté ocurriendo la votación en la que desea participar.'
VOTING_IN = '🗳 Usted está votando en la encuesta del grupo "%s".\n\n❓Utilice los botones para agregar una opción al final de la lista o remover una opción ya seleccionada. Marque Cancelar para descartar su voto. Una vez agregadas todas las opciones de la encuesta a su lista en el orden deseado, marque Confirmar para emitir su voto.'
VOTING_IN_WHIT_STATE = VOTING_IN + '\n\nSu voto actual es:\n%s'
CANCEL = '❌ Se ha cancelado su voto en la votación de "%s". Escriba /vote nuevamente para participar en esta u otra votación.'
CONFIRM = '✅ Su voto en la votación de "%s" ha sido emitido satisfactoriamente. Recuerde que puede volver a ejercer su voto escribiendo /vote aquí nuevamente.\n\n❗️Su último voto válido será el único considerado en los resultados finales de la votación.\n\nSu voto actual es:\n%s'
INVALID = '⚠️ Su voto en "%s" no se ha emitido correctamente. Esto puede ocurrir por varias razones. Por favor, intente:\n\n📍Revisar que la votación en la que quiere participar no haya finalizado aún.\n📍Escribir /vote para emitir su voto nuevamente. Revise que está seleccionando la votación correcta.\n📍Registrarse nuevamente en la votación escribiendo /register en el grupo donde está teniendo lugar./n📍Contactar a un administrador del grupo en caso de haber seguido sin éxito las sugerencias anteriores.'
NO_VALID    = '⚠️ El modelo que intentó activar no es válido. Escriba /models para consultar los modelos disponibles actualmente.'
ACCEPT      = '✅ El modelo a utilizar ha sido cambiado satisfactoriamente. Escriba /models para saber más acerca de los modelos.'
INTRO_G = '''
🤖 ¡Hola! Soy eπ-2021, el asistente virtual de MatCom, y a través de este bot gestiono las encuestas que tienen lugar en los grupos de la Facultad.

😊 Puedo ayudar a alcanzar el consenso de una brigada, un año o toda la Facultad sobre cualquier cuestión. Ya tengo experiencia en generar calendarios de pruebas, seleccionar una mascota, etc.

❓Para utilizar este bot, primero agréguelo al grupo donde tendrá lugar la encuesta. Solo los administradores del grupo podrán manejar una votación.

👉Si usted es administrador, escriba en el grupo /create para iniciar una votación y luego siga las instrucciones que el bot le indicará por el chat privado. Utilice /status para seguir los resultados de la votación y /close para obtener los resultados. ¡Feliz encuesta! 😃

'''

INTRO_PV = '''
🤖 ¡Hola! Soy eπ-2021, el asistente virtual de MatCom, y a través de este bot gestiono las encuestas que tienen lugar en los grupos de la Facultad.

😊 Puedo ayudar a alcanzar el consenso de una brigada, un año o toda la Facultad sobre cualquier cuestión. Ya tengo experiencia en generar calendarios de pruebas, seleccionar una mascota, etc.

❓Para utilizar este bot, primero agréguelo al grupo donde tendrá lugar la encuesta. Solo los administradores del grupo podrán manejar una votación.

👉Si usted es administrador, escriba en el grupo /create para iniciar una votación y luego siga las instrucciones que el bot le indicará por el chat privado. Utilice /status para seguir los resultados de la votación y /close para obtener los resultados. ¡Feliz encuesta! 😃

'''

commands_pv = [
        ('start'    , 'Inicia el bot.'),
        ('config'   , 'Inicia la configuración de las opciones de una votación.'),
        ('cancel'   , 'Cancela una acción en la configuración.'),
        ('vote'     , 'Tome parte en una votación actual.'),
        ('help'     , 'Muestra la ayuda.')
    ]

commands_group = [
        ('start'    , 'Inicia el bot.'),
        ('create'   , 'Crea una nueva votación en el grupo.'),
        ('vote'     , 'Registra al usuario para votar en la votación actual.'),
        ('register' , 'Registra al usuario para votar en la votación actual.'),
        ('close'    , 'Cierra la votación actual y arroja los resultados finales.'),
        ('cancel'   , 'Cancela la votación actual si se utiliza en el grupo.'),
        ('list'     , 'Ofrece la lista de los usuarios que han votado.'),
        ('status'   , 'Muestra la cantidad de votantes que ha participado en una votación y ofrece los resultados parciales de esta.'),
        ('models'   , 'Muestra la lista de modelos disponibles para calcular los resultados de una votación.'),
        ('list_models' , 'Muestra la lista de modelos disponibles para calcular los resultados de una votación.'),
        ('help'     , 'Muestra la ayuda.'),
    ]
