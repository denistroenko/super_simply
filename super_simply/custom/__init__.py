"""
This import custom plugins
"""


import glob
import sys
sys.path.append('..')
sys.path.append('./custom/')
import logging
from baseapplib import configure_logger


logger = logging.getLogger(__name__)


def __init__():
    configure_logger(logger,
                     debug_file_name='../log/debug.log',
                     error_file_name='../log/error.log',
                     screen_logging=True,
                     )

def load():
    plugins_list = (glob.glob('./custom/*.py'))

    with open('./custom/imports.py', 'w') as import_file:
        for plugin in plugins_list:
            plugin = plugin.split('/')[-1]
            if plugin != '__init__.py' and \
                plugin != 'imports.py':
                    import_file.write(
                        'import ' + plugin[:-3] + '\n')
                    logger.info("Будет импортирован " + plugin)
    from . import imports
