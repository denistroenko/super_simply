import sys


# Path to curent app folder
APP_PATH = '/home/USER/web/DOMAIN/app_path/'


# Change dir to curent app dir
sys.path.insert(0, APP_PATH)

# Application
from main import app as application
