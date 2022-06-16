__version__ = '0.0.1'


import logging
import datetime
from typing import Optional
from flask import Flask, render_template
from baseapplib import configure_logger
import super_simply
import custom


# GLOBAL
# Extra files
FLASK_RUN_EXTRA_FILES = ['./config/config_site', './config/config_pages']
# Logger
logger = logging.getLogger(__name__)
# App
app = Flask(__name__)
# Site
site = super_simply.Site()


def main():
    configure_logger(logger,
                     debug_file_name='./log/debug.log',
                     error_file_name='./log/error.log',
                     )
    logger.debug('# # # # #  Приложение запущено  # # # # #')
    super_simply.configure_site(site)
    super_simply.load_system_pages(site)
    super_simply.load_pages(site)
    super_simply.load_carousels(site)
    super_simply.load_albums(site)
    custom.load()


def run_local_app(host: Optional[str] = None,
            debug: Optional[bool] = None,
            ):
    app.run(host=host,
            debug=debug,
            extra_files = FLASK_RUN_EXTRA_FILES,
            )


@app.route('/')
def show_root():
    return show_page('')


@app.route('/<path:page_url>/')
def show_page(page_url):
    page_url = '/' + page_url
    logger.debug('Запрошена страница %s' % page_url)

    page = site.get_page(page_url)

    for key in site.system_pages:
        if site.system_pages[key].path == page_url:
            logger.debug('Возвращается специальная страница сайта.')
            page = site.system_pages[key]

    site.add_server_info(key='year', info=int(datetime.date.today().year))
    return render_template(page.template,
                           site=site,
                           page=page,
                           )


main()


if __name__ == '__main__':
    run_local_app(host='192.168.88.1',
            debug=True,
            )
