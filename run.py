import logging

import coloredlogs

import vuejs_doc
from core import cli

if __name__ == '__main__':
    logging_format = '[%(asctime)s] %(levelname)s: %(message)s'
    coloredlogs.install(level='INFO', logger=logging.getLogger(), fmt=logging_format)

    cli()
