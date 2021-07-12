import logging
from baseapplib import configure_logger
from values import int_value, str_value, list_value


logger = logging.getLogger(__name__)
configure_logger(logger)

class Site:
    """
    Класс объекта сайта.
    """

    site_name = str_value('site_name')

    def __init__(self,
                    site_name: str ='Super Simply',
                    ):
        logger.debug('Инициализация Site')

        self.site_name = site_name


class Page:
    """
    Класс страницы сайта.
    """

    url = str_value('url')
    page_id = int_value('page_id')
    page_name = str_value('page_name')
    parent = int_value('parent')
    children = list_value('children')
    template = str_value('template')
    title = str_value('title')
    h1 = str_value('h1')
    description = str_value('description')
    keywords = str_value('keywords')

    def __init__(self,
                 url: str,
                 page_id: int,
                 page_name: str,
                 parent: int=0,
                 children: list=[],
                 template: str='page.html',
                 title: str='',
                 h1: str='',
                 description: str='',
                 keywords: str='',
                 ):
        logger.debug('Инициализация Page')

        self.url = url
        self.page_id = page_id
        self.page_name = page_name
        self.parent = parent
        self.children = children
        self.template = template
        self.title = title
        self.h1 = h1
        self.description = description
        self.keywords = keywords

    def render_page():
        pass

    def add_child(self, page_id: int):
        if isinstance(page_id, int):
            self.children.append(page_id)
            return
        raise ValueError('Неверный формат данных (верный - int).')
