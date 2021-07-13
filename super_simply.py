import logging
from baseapplib import configure_logger
from values import int_value, str_value, list_value


logger = logging.getLogger(__name__)
configure_logger(logger)


class Site:
    """
    Класс объекта сайта.
    """

    # Свойства класса (чарез дескрипторы)
    site_name = str_value('site_name')

    def __init__(self, site_name='Super Simply'):
        logger.debug('Инициализация Site')
        self.site_name = site_name


class Page:
    """
    Класс страницы сайта.
    """

    # Свойства класса (чарез дескрипторы)
    id = int_value('id')
    path = str_value('path')
    name = str_value('name')
    parent = int_value('parent')
    children = list_value('children')
    template = str_value('template')
    title = str_value('title')
    h1 = str_value('h1')
    description = str_value('description')
    keywords = str_value('keywords')

    def __init__(self,
                 id: int,               # id страницы
                 path: str,             # url страницы относительно родителя
                 name: str,             # имя страницы для ссылок
                 parent=0,              # id родителя страницы
                 children=[],           # список id дочерних страниц
                 template='page.html',  # шаблон рендеринга
                 title='',              # титул страницы
                 h1='',                 # заголовок страницы (для шаблонов)
                 description='',        # описание (мета-тег) страницы
                 keywords='',           # ключевые слова (мета-тег) страницы
                 ):
        logger.debug('Инициализация Page')

        self.id = id
        self.path = path
        self.name = name
        self.parent = parent
        self.children = children
        self.template = template
        self.title = name if title == '' else title
        self.h1 = name if h1 == '' else h1
        self.description = description
        self.keywords = keywords

    def render_page():
        """
        Рендерит страницу по ее шаблону и возвращает html.
        """
        pass

    def add_child(self, page_id: int):
        """
        Добавляет принятый page_id к списку в атрибуте self.children,
        но проверяет изначально тип данных, должен быть int.
        """

        if isinstance(page_id, int):
            self.children.append(page_id)
            return
        raise ValueError('Неверный формат данных (верный - int).')
