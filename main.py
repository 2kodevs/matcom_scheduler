import logging

from configparser import ConfigParser

from src.bot import Scheduler_Bot


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
    

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Bot initializer')
    parser.add_argument('-c', '--config', type=str, default='config.ini', help='path of the configuration file')
    parser.add_argument('--debug', help='execute in debug mode', action="store_true")

    args = parser.parse_args()
    main(args)
