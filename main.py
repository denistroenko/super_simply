__version__ = '0.0.1'


import logging
import datetime
from typing import Optional
from flask import Flask, render_template, session
from baseapplib import configure_logger, get_script_dir, PasswordGenerator
from config import Config
import super_simply
import custom
from custom import web_forms, view


# GLOBAL
logger = logging.getLogger(__name__)  # logger
app = Flask(__name__)                 # app
site = super_simply.Site()            # site
app_config = Config()                 # app_config


def main():
    configure_logger(logger,
                     debug_file_name=f'{get_script_dir()}log/debug.log',
                     error_file_name=f'{get_script_dir()}log/error.log',
                     start_msg='\n\n#  Приложение запущено  #')

    load_app_config()
    mapping_view()

    super_simply.configure_site(site)
    super_simply.load_system_pages(site)
    super_simply.load_pages(site)
    super_simply.load_carousels(site)
    super_simply.load_albums(site)
    custom.load()


def load_app_config():
    # прочитать настройки приложения из файла
    app_config.read_file(f'{get_script_dir()}config/app')
    # найти параметр секретного ключа
    try:
        secret_key = app_config.get('app', 'secret_key')
    except:
        # если исключение - создать ключ, добавить его в app_config,
        # перезаписать настройки приложения в файл
        password_generator = PasswordGenerator()
        password_generator.password_len = 24
        secret_key = password_generator.get_new_password()

        app_config.set('app', 'secret_key', secret_key)
        app_config.write_file(f'{get_script_dir()}config/app')
    app.config['SECRET_KEY'] = secret_key


def run_local_app(host: Optional[str]=None, debug: Optional[bool]=None):
    FLASK_RUN_EXTRA_FILES = ['./config/site', './config/pages']
    main()
    app.run(host=host, debug=debug, extra_files = FLASK_RUN_EXTRA_FILES)


def mapping_view():
    # custom views in ./custom/views
    view.mapping_view(app, site)

    # standard views for all pages
    @app.route('/')
    @app.route('/<path:page_url>')
    def show_page(page_url=''):
        # убрать / в конце относительного url
        if len(page_url) > 1 and page_url[-1] == '/':
            page_url = page_url[:-1]

        # поставить / в начало относительного url
        page_url = '/%s' % page_url

        logger.debug('Запрошена страница %s' % page_url)

        # получить формы (контекст запроса)
        forms = web_forms.get_forms()

        # получить страницу сайта
        page = site.get_page(page_url)

        # получить системную страницу
        for key in site.system_pages:
            if site.system_pages[key].path == page_url:
                logger.debug('Возвращается специальная страница сайта.')
                page = site.system_pages[key]

        # Добавить шташрмацию сервера
        site.add_server_info(key='year', info=int(datetime.date.today().year))

        # вернуть html-рендер нужной страницы
        return render_template(page.template, site=site, page=page,
                session=session, forms=forms)


if __name__ == '__main__':
    run_local_app(host='192.168.88.1', debug=True, )
