__version__ = '0.0.1'


import logging
from flask import Flask, url_for
from baseapplib import configure_logger
from super_simply import Site, Page
import pages


logger = logging.getLogger(__name__)
configure_logger(logger)
logger.debug('# # # # #  Приложение запущено  # # # # #')
app = Flask(__name__)
site = Site()


def main():
    pages.configure_site(site)
    page = Page('/', 0 , 'home')


main()


# @app.route('<page_url>')
# def render_site(page_url):
    # pass


# if __name__ == '__main__':
    # app.run(
        # debug=True,
        # host='192.168.88.1',
        # port=80,
    # )
