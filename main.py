__version__ = '0.0.1'


import logging
from flask import Flask, url_for, render_template
from baseapplib import configure_logger
from super_simply import Site, Page
import pages


logger = logging.getLogger(__name__)
app = Flask(__name__)
site = Site()


def main():
    configure_logger(logger)
    logger.debug('# # # # #  Приложение запущено  # # # # #')
    pages.configure_site(site)
    pages.load_pages(site)
    pages.load_system_pages(site)


@app.route('/')
def show_root():
    return show_page('')

@app.route('/<page_url>/')
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
    app.run(debug=True,
            host='192.168.88.1',
            port=80,
            )
