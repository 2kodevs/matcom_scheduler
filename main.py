import logging

from configparser import ConfigParser
from sys import argv
from telegram.ext import Updater

debug = argv[1] == 'debug' if len(argv) > 1 else False

level = logging.INFO if not debug else logging.DEBUG

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level)
logger = logging.getLogger(__name__)

def main():
    logger.log(logging.INFO, 'Setting up bot...')
    
    config = ConfigParser()
    logger.log(logging.INFO, 'Loading configuration...')
    config.read('config.ini')
    logger.log(logging.INFO, 'Configuration loaded.')

    updater = Updater(config['bot']['HTTP_API'], use_context=True)

    logger.log(logging.INFO, 'Running bot...')
    try:
        updater.start_polling()
    except Exception as e:
        logger.log(logging.ERROR, e)
        return
    logger.log(logging.INFO, 'Bot sucessfully started.')

    updater.idle()
    

if __name__ == '__main__':
    main()
