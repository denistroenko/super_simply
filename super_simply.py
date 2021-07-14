import logging
from baseapplib import configure_logger
from values import int_value, str_value, list_value, dict_value


logger = logging.getLogger(__name__)
configure_logger(logger)


class Empty_page:
    def __init__(self):
        pass


class Site:
    """
    Класс объекта сайта.
    """

    # Свойства класса (чарез дескрипторы)
    name = str_value('name')
    domain = str_value('domain')
    path = str_value('path')
    pages = dict_value('pages')

    def __init__(self,
                 domain='domain.domain',
                 site_name='Super Simply',
                 ):
        logger.debug('Инициализация <Site>')
        self.pages = {}
        logger.debug('Конец инициализации')

    def add_page(self, page: object):
        id = len(self.pages)
        logger.debug('<Site>.add_page Смена id у добавляемой страницы')
        page.id = id
        self.pages[page.path] = (page)
        logger.debug('<Site>.add_page Страница добавлена.')


class Page:
    """
    Класс страницы сайта.
    """

    # Свойства класса (чарез дескрипторы)
    id = int_value('id')
    name = str_value('name')
    path = str_value('path')
    parent = int_value('parent')
    template = str_value('template')
    title = str_value('title')
    h1 = str_value('h1')
    description = str_value('description')
    keywords = str_value('keywords')
    children = list_value('children')

    def __init__(self,
                 name: str,             # имя страницы для ссылок
                 path: str,             # url страницы относительно родителя
                 template: str,         # шаблон рендеринга
                 parent=0,              # id родителя страницы
                 title='',              # титул страницы
                 h1='',                 # заголовок страницы (для шаблонов)
                 description='',        # описание (мета-тег) страницы
                 keywords='',           # ключевые слова (мета-тег) страницы
                 ):
        logger.debug('Инициализация <Page>')

        self.id = 0

        self.name = name
        self.path = path
        self.template = template
        self.parent = parent
        self.title = name if title == '' else title
        self.h1 = name if h1 == '' else h1
        self.description = description
        self.keywords = keywords

        self.children = []

        logger.debug('Конец инициализации')


    def __str__(self):
        return str((self.id,
                   self.name,
                   self.path,
                   self.template,
                   self.parent,
                   self.title,
                   self.h1,
                   self.description,
                   self.keywords,
                   )
                  )

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
