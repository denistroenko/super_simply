"""
This import custom plugins
"""


import sys
sys.path.append('./custom/')
import glob
import logging
from baseapplib import configure_logger, get_script_dir


logger = logging.getLogger(__name__)
configure_logger(logger,
                 debug_file_name='{}log/debug.log'.format(get_script_dir()),
                 error_file_name='{}log/error.log'.format(get_script_dir()),
                 )


def load():
    plugins_list = (glob.glob('./custom/*.py'))

    with open(f'{get_script_dir()}custom/imports.py', 'w') as import_file:
        for plugin in plugins_list:
            plugin = plugin.split('/')[-1]
            if plugin != '__init__.py' and \
                plugin != 'imports.py':
                    import_file.write(
                        'import ' + plugin[:-3] + '\n')
                    logger.debug('Будет импортирован ' + plugin)
    logger.debug('Импорт custom-модулей...')
    from . import imports
