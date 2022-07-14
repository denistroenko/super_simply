import sys
import inspect
import os


def get_script_dir(follow_symlinks=True):
    """
        Возвращает путь к скрипту __main__ (папку)
    """
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return '{}/'.format(os.path.dirname(path))


# Change dir to curent app dir
sys.path.insert(0, get_script_dir())

# Application
from view import app as application
