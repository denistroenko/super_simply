import logging
from flask import url_for
from baseapplib import configure_logger
from values import int_value, str_value, list_value, dict_value, bool_value


logger = logging.getLogger(__name__)
configure_logger(logger)


class Site:
    """
    Класс объекта сайта.
    """

    # Свойства класса (через дескрипторы)
    name = str_value('name')
    domain = str_value('domain')
    path = str_value('path')
    pages = list_value('pages')
    system_pages = dict_value('system_pages')
    total_pages = int_value('total_pages')
    info = dict_value('info')
    author = str_value('author')
    phone = str_value('phone')
    address = str_value('address')

    def __init__(self,
                 domain='domain.domain',
                 site_name='Super Simply',
                 ):
        logger.debug('Инициализация <Site>')
        self.pages = []  # свойство "страницы"
        self.system_pages = {}  # свойство "специальные страницы"
        self.total_pages = 0  # счетчик страниц сайта
        self.info = {}  # словарь информации сервера
        self.author = ''
        self.phone = ''
        self.address = ''
        logger.debug('Конец инициализации')

    def __fill_page_breadcrumbs(self, page: object):
        """
        Заполняет свойство breadcrumbs переданного объекта page, исходя из
        цепочки его родителей.
        """
        if page.parent == -1:
            return

        parents = []

        def append_parent(parent_page: object):
            parents.append(parent_page)
            if parent_page.parent != -1:
                append_parent(self.get_page(parent_page.parent))

        append_parent(self.get_page(page.parent))
        page.breadcrumbs = parents[::-1]

    def add_system_page(self, page: object, key: str):
        """
        Доавляет спец. страницу на сайт (передать объект страницы и ключ).
        """
        self.system_pages[key] = page

    def get_system_page(self, key: str) -> object:
        """
        Возвращает объект спец. страницы сайта по ключу.
        """
        return self.system_pages[key]

    def get_system_pages(self) -> list:
        """
        Возвращает список объектов всех спец. страниц.
        """
        pages = []

        for key in self.system_pages:
            pages.append(self.system_pages[key])

        return pages

    def add_page(self, page: object):
        """
        Добавляет страницу либо к страницам сайта, либо к подстраницам
        конкретной страницы (в зависимости от атрибута parent передаваемого
        объекта страницы).
        """
        logger.debug('Добавление страницы...')

        page.id = self.total_pages  # присвоить id
        self.total_pages += 1  # прибавить 1 к счетчику страниц на сайте

        if page.parent == -1:
            self.pages.append(page)
            logger.debug('Страница добавлена как страница сайта.')
        else:
            self.__fill_page_breadcrumbs(page)
            parent = self.get_page(page.parent)
            parent.add_subpage(page)
            logger.debug('Страница добавлена как подстраница.')

    def get_pages(self) -> list:
        """
        Возвращает все страницы сайта и все их подстраницы (список обхектов).
        """
        pages = []  # инициализация ПОЛНОГО списка ВСЕХ страниц сайта

        def get_subpages(page):  # функция возвращает все подстраницы страницы,
                                 # а так же подстраницы ее подстраниц
            subpages = []

            def fill_subpages(page):  # рекурсивная функция заполнения списка
                                      # подстраниц (subpages)
                for subpage in page.subpages:
                    subpages.append(subpage)
                    if subpage.subpages != []:
                        fill_subpages(subpage)

            fill_subpages(page)
            return subpages

        # добавить к списку всех страниц страницы и подстраницы сайта
        for page in self.pages:
            pages.append(page)
            subpages = get_subpages(page)
            pages += subpages

        return pages

    def add_info(self, info, key) -> None:
        self.info[key] = info

    def get_page(self, id) -> object:
        """
        Возвращает объект страницы. id - идентификатор страницы, либо ее путь,
        либо алиас.
        """

        pages = self.get_pages()

        # перебрать все страницы и найти совпадение id с path, alias или id
        for page in pages:
            if (id == page.path or
                id in page.aliases or
                id == page.id):

                return page

        # Вернуть страницу 404
        return self.get_system_page('404')

class Page:
    """
    Класс страницы сайта.
    """

    # Свойства класса (чарез дескрипторы)
    id = int_value('id')
    name = str_value('name')
    path = str_value('path')
    parent = int_value('parent')
    breadcrumbs = list_value('breadcrumbs')
    template = str_value('template')
    title = str_value('title')
    h1 = str_value('h1')
    description = str_value('description')
    keywords = str_value('keywords')
    subpages = list_value('subpages')
    visible = bool_value('visible')
    aliases = list_value('aliases')
    img = str_value('img')
    icon = str_value('icon')

    def __init__(self,
                 name: str,             # имя страницы для ссылок
                 path: str,             # url страницы относительно родителя
                 template: str,         # шаблон рендеринга
                 parent: int = -1,      # id родителя страницы
                 breadcrumbs: list = [],# список объектов цепочки родителей
                 title: str = '',       # титул страницы
                 h1: str = '',          # заголовок страницы (для шаблонов)
                 description: str = '', # описание (мета-тег) страницы
                 keywords: str = '',    # ключевые слова (мета-тег) страницы
                 visible:  bool = True, # видимость в меню
                 aliases: list = [], # псевдонимы страницы (список path)
                 img: str = '',         # относительный путь к картинке
                 icon: str = '',        # относитеьный путь к иконке
                 ):
        logger.debug('Инициализация <Page>')

        self.id = -1

        self.name = name
        self.path = path
        self.template = template
        self.parent = parent
        self.breadcrumbs = breadcrumbs
        self.title = title
        self.h1 = h1
        self.description = description
        self.keywords = keywords
        self.visible = visible
        self.aliases = aliases
        self.img =  img
        self.icon = icon

        self.subpages = []

        logger.debug('Конец инициализации')


    # def __str__(self):
        # return str((self.id,
                   # self.name,
                   # self.path,
                   # self.template,
                   # self.parent,
                   # self.title,
                   # self.h1,
                   # self.description,
                   # self.keywords,
                   # )
                  # )

    def add_subpage(self, page: object):
        """
        Добавляет объект страницы к списку в атрибуте self.subpages.
        """

        if isinstance(page, object):
            self.subpages.append(page)
            return
        raise ValueError('Неверный формат данных (верный - object).')
