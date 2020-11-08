import logging

from telegram.ext import Updater, PicklePersistence

from .handlers import bot_handlers

logger = logging.getLogger(__name__)

def set_commands(bot):
    bot.set_my_commands([
        ('create'   , 'Crea una nueva discusión del calendario.'),
        ('config'   , 'Configura las opciones de la discución.'),
        ('vote'     , 'Toma parte en la discusión actual.'),
        ('close'    , 'Cierra la discusión actual.'),
        ('cancel'   , 'Cancela una acción en la configuración o la votación actual si se usa en el grupo.'),
        ('start'    , 'Inicia el bot.'),
        ('help'     , 'Muestra la ayuda.'),
        ('list'     , 'Lista los usuarios que han votado.'),
    ])

class Scheduler_Bot:
    def __init__(self, token:str):
        self.token = token

        logger.log(logging.INFO, 'Setting up bot...')

        persistance = PicklePersistence('scheduler.data')

        self.updater = Updater(self.token, persistence=persistance, use_context=True)
        dispatcher = self.updater.dispatcher

        logger.log(logging.INFO, 'Adding handlers...')
        set_commands(self.updater.bot)

        for handler in bot_handlers:
            dispatcher.add_handler(handler)

        logger.log(logging.INFO, 'Bot setted up.')
        
            

    def run(self):
        logger.log(logging.INFO, 'Running bot...')
        try:
            self.updater.start_polling()
        except Exception as e:
            logger.log(logging.ERROR, e)
            return
        logger.log(logging.INFO, 'Bot sucessfully started.')

        self.updater.idle()
