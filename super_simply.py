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

    # Свойства класса (чарез дескрипторы)
    name = str_value('name')
    domain = str_value('domain')
    path = str_value('path')
    pages = list_value('pages')
    system_pages = dict_value('system_pages')
    total_pages = int_value('total_pages')

    def __init__(self,
                 domain='domain.domain',
                 site_name='Super Simply',
                 ):
        logger.debug('Инициализация <Site>')
        self.pages = []  # свойство "страницы"
        self.system_pages = {}  # свойство "специальные страницы"
        self.total_pages = 0  # счетчик страниц сайта
        logger.debug('Конец инициализации')

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

    def get_page(self, id) -> object:
        """
        Возвращает объект страницы. id - идентификатор страницы, либо ее путь,
        либо алиас.
        """

        pages = self.get_pages()

        # перебрать вс страницы и найти совпадение id с path, alias или id
        for page in pages:
            print(page.name, 'ее id = ', page.id)
            if (id == page.path or
                id in page.alias_list or
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
    template = str_value('template')
    title = str_value('title')
    h1 = str_value('h1')
    description = str_value('description')
    keywords = str_value('keywords')
    subpages = list_value('subpages')
    visible = bool_value('visible')
    alias_list = list_value('alias_list')
    img = str_value('img')
    icon = str_value('icon')

    def __init__(self,
                 name: str,             # имя страницы для ссылок
                 path: str,             # url страницы относительно родителя
                 template: str,         # шаблон рендеринга
                 parent=0,              # id родителя страницы
                 title='',              # титул страницы
                 h1='',                 # заголовок страницы (для шаблонов)
                 description='',        # описание (мета-тег) страницы
                 keywords='',           # ключевые слова (мета-тег) страницы
                 visible=True,          # видимость в меню
                 alias_list=[],         # псевдонимы страницы (список path)
                 img='',
                 icon='',
                 ):
        logger.debug('Инициализация <Page>')

        self.id = -1

        self.name = name
        self.path = path
        self.template = template
        self.parent = parent
        self.title = name if title == '' else title
        self.h1 = name if h1 == '' else h1
        self.description = description
        self.keywords = keywords
        self.visible = visible
        self.alias_list = alias_list
        self.img = '/static/img/%s' % img if img != '' else ''
        self.icon = '/static/img/%s' % icon if icon != '' else ''

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
