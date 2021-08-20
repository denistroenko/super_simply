import sys


APP_PATH = '/home/USER/web/DOMAIN/app_path/'


sys.path.insert(0, APP_PATH)


from main import app as application

