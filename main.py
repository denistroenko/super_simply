__version__ = '0.0.1'


import logging
from flask import Flask, url_for
from baseapplib import configure_logger
from super_simply import Site, Page
import pages


logger = logging.getLogger(__name__)
app = Flask(__name__)
site = Site()
shadow_site = Site()


def main():
    configure_logger(logger)
    logger.debug('# # # # #  Приложение запущено  # # # # #')
    pages.configure_shadow_site(shadow_site)
    pages.configure_site(site)
    pages.load_pages(site)

    app.run(
        debug=True,
        host='192.168.88.1',
        port=80,
    )


@app.route('/')
def show_root():
    page_url = '/'

    logger.debug('Запрошена страница %s' % page_url)

    if page_url in site.pages:
        logger.debug('ЕСТЬ ТАКАЯ')
        return page_url

    logger.debug('НЕТ ТАКОЙ')
    return shadow_site.pages['error 404'].name


@app.route('/<page_url>/')
def show_page(page_url):
    page_url += '/'

    logger.debug('Запрошена страница %s' % page_url)

    if page_url in site.pages:
        logger.debug('ЕСТЬ ТАКАЯ')
        return page_url

    logger.debug('НЕТ ТАКОЙ')
    return shadow_site.pages['404/'].name


if __name__ == '__main__':
    main()
