__version__ = '0.0.1'


import logging
from typing import Optional
from flask import Flask, url_for, render_template
from baseapplib import configure_logger
from super_simply import Site, Page
import pages


# GLOBAL
# Extra files
FLASK_RUN_EXTRA_FILES = ['./config_site',
                         './config_pages',
                        ]


# Logger
logger = logging.getLogger(__name__)
# App
app = Flask(__name__)

# Site
site = Site()


def main():
    configure_logger(logger)
    logger.debug('# # # # #  Приложение запущено  # # # # #')
    pages.configure_site(site)
    pages.load_pages(site)
    pages.load_system_pages(site)


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


    return render_template(page.template,
                           site=site,
                           page=page,
                           )


main()

if __name__ == '__main__':
    run_local_app(host='192.168.88.1',
            debug=True,
            )
