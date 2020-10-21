import logging

from telegram.ext import Updater

from .handlers import bot_handlers

logger = logging.getLogger(__name__)

def set_commands(bot):
    bot.set_my_commands([
        ('create'   , 'New schedule discuss'),
        ('config'   , 'Set the schedule options'),
        ('vote'     , 'Take part in the current discussion'),
        ('close'    , 'Close the current discussion'),
        ('cancel'   , 'Cancel the current action'),
        ('start'    , 'Start the bot'),
        ('help'     , 'Show the bot help'),
    ])

class Scheduler_Bot:
    def __init__(self, token:str):
        self.token = token

        logger.log(logging.INFO, 'Setting up bot...')

        self.updater = Updater(self.token, use_context=True)
        dispatcher = self.updater.dispatcher

        logger.log(logging.INFO, 'Adding handlers...')
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
