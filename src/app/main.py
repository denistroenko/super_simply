__version__ = '0.0.1'


import datetime
from typing import Optional

from flask import (Flask, render_template, session, redirect,
        send_from_directory, request)

from tools import (get_logger, configure_logger, get_app_dir,
        PasswordGenerator, Config)

import super_simply
import custom
from custom import web_forms, view


# GLOBAL
app = Flask(__name__)                 # app
app_dir = get_app_dir(False)
logger = get_logger(__name__)  # logger
site = super_simply.Site()            # site
app_config = Config()                 # app_config


def main():
    configure_logger(logger,
                     debug_file=f'{app_dir}log/debug.log',
                     error_file_name=f'{app_dir}log/error.log',
                     )

    load_app_config()
    mapping_view()
    super_simply.configure_site(site)
    super_simply.load_system_pages(site)
    super_simply.load_pages(site)
    super_simply.load_albums(site)
    custom.load()


def load_app_config():
    # прочитать настройки приложения из файла
    app_config.read_file(f'{app_dir}config/app')
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
        app_config.write_file(f'{app_dir}config/app')
    app.config['SECRET_KEY'] = secret_key
    app.config['SRF_ENABLED'] = True


def run_local_app(host: Optional[str]=None, debug: Optional[bool]=None):
    FLASK_RUN_EXTRA_FILES = ['./config/site', './config/pages']
    main()
    app.run(host=host, debug=debug, extra_files = FLASK_RUN_EXTRA_FILES)


def mapping_view():
    # custom views in ./custom/views
    view.mapping_view(app, site)

    @app.route('/robots.txt')
    def show_static():
        return send_from_directory(app.static_folder, request.path[1:])

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

        # получить страницу сайта
        page = site.get_page(page_url)

        # получить системную страницу
        for key in site.system_pages:
            if site.system_pages[key].path == page_url:
                logger.debug('Возвращается специальная страница сайта.')
                page = site.system_pages[key]

        if site.is_page(page.path):
            session['page.name'] = page.name

        # получить формы (контекст запроса)
        forms = web_forms.get_forms()

        # Добавить информацию сервера
        site.add_server_info(key='year', info=int(datetime.date.today().year))

        for form in forms:
            try:
                forms[form].page_url.data = page_url
                forms[form].page_name.data = page.name
            except Exception:
                pass

        # если запрошен path алиаса страницы, сделать 301-й редирект на ее path
        if page_url in page.aliases:
            return redirect(page.path, 301)

        try:
            # вернуть html-рендер нужной страницы
            return render_template(page.template, site=site, page=page,
                session=session, forms=forms), page.code
        except Exception as e:
            e = str(e)
            return f'Ошибка в шаблоне {page.template}:<br> {e}'


if __name__ == '__main__':
    run_local_app(host='192.168.88.1', debug=True, )
