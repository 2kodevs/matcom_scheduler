import logging
from src import Scheduler_Bot
from configparser import ConfigParser

def main(args):
    level = logging.DEBUG if args.debug else logging.INFO

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level)
    logger = logging.getLogger(__name__)

    config = ConfigParser()
    logger.log(logging.INFO, 'Loading configuration...')
    config.read(args.config)
    logger.log(logging.INFO, 'Configuration loaded.')

    token = config.get('bot', 'token', fallback=None)
    if token:
        bot = Scheduler_Bot(token)
        bot.run()
    else:
        raise Exception(f'Invalid or missing "token" in {args.config}')

def heroku(args):
    import os

    NAME = os.getenv('NAME')
    PORT = os.getenv('PORT')
    TOKEN = os.getenv('TOKEN')

    level = logging.DEBUG if args.debug else logging.INFO

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level)
    logger = logging.getLogger(__name__)

    scheduler = Scheduler_Bot(TOKEN)
    updater = scheduler.updater

    updater.start_webhook(listen='0.0.0.0', port=int(PORT), url_path=TOKEN)
    updater.bot.set_webhook('https://%s.herokuapp.com/%s' % (NAME, TOKEN))

    updater.idle()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Bot initializer')
    parser.set_defaults(command=main)

    parser.add_argument('-c', '--config', type=str, default='config.ini', help='path of the configuration file')
    parser.add_argument('--debug', help='execute in debug mode', action="store_true")

    subparsers = parser.add_subparsers()
    heroku_parser = subparsers.add_parser('heroku', help="Run a bot instance using heroku")
    heroku_parser.set_defaults(command=heroku)

    args = parser.parse_args()
    args.command(args)
