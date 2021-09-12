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
    pages = list_value('pages')
    system_pages = dict_value('system_pages')
    total_pages = int_value('total_pages')
    server = dict_value('server')
    company = str_value('company')
    author = str_value('author')
    phone = str_value('phone')
    tel = str_value('tel')
    email = str_value('email')
    address = str_value('address')
    info = dict_value('info')
    carousels = list_value('carousels')
    galleries = list_value('galleries')

    def __init__(self):
        logger.debug('Инициализация <Site>')
        self.name = ''          # Имя сайта
        self.domain = ''        # домен сайта
        self.pages = []         # "страницы" - список объектов страниц
        self.system_pages = {}  # "спец. страницы" - объекты страниц (словарь)
        self.total_pages = 0    # счетчик страниц сайта
        self.server = {}        # словарь информации сервера
        self.company = ''       # название компании
        self.author = ''        # авторство
        self.phone = ''         # телефон сайта
        self.tel = ''           # телефон сайта для href ссылки
        self.email = ''         # адрес электронной почты
        self.address = ''       # адрес офиса
        self.info = {}          # любая прочая информация (словарь)
        self.carousels = []     # "карусели" - список объектов карусель
        self.galleries = []     # "галереи" - список объектов галерей
        logger.debug('Конец инициализации')

    def __fill_page_breadcrumbs(self, page: object) -> None:
        """
        Заполняет свойство breadcrumbs переданного объекта page, исходя из
        цепочки его родителей.
        """
        if page.parent == -1:
            return

        parents = []

        def append_parent(parent_page: object) -> None:
            parents.append(parent_page)
            if parent_page.parent != -1:
                append_parent(self.get_page(parent_page.parent))

        append_parent(self.get_page(page.parent))
        page.breadcrumbs = parents[::-1]

    def add_system_page(self, page: object, key: str) -> None:
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

    def add_page(self, page: object) -> None:
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

    def add_carousel(self, carousel: object) -> None:
        """
        Добавляет карусель к коллекции каруселей сайта
        """
        self.carousels.append(carousel)

    def add_gallery(self, gallery: object) -> None:
        """
        Добавляет галерею (объект) в список галерей сайта
        """
        self.galleries.append(gallery)

    def get_pages(self) -> list:
        """
        Возвращает все страницы сайта и все их подстраницы (список обхектов).
        """
        pages = []  # инициализация ПОЛНОГО списка ВСЕХ страниц сайта

        def __get_subpages(page) -> list:
            """
            функция возвращает всe подстраницы страницы,
            а так же подстраницы ее подстраниц
            """
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
            subpages = __get_subpages(page)
            pages += subpages

        return pages

    def add_server_info(self, info, key) -> None:
        """
        Добавляет ключ:значение к словарю Site.serer
        """
        self.server[key] = info

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
    image = str_value('image')
    icon = str_value('icon')
    info = dict_value('info')

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
                 aliases: list = [],    # псевдонимы страницы (список path)
                 image: str = '',       # относительный путь к картинке
                 icon: str = '',        # относитеьный путь к иконке
                 info: dict = {},       # любая прочая информация (словарь)
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
        self.image =  image
        self.icon = icon
        self.info = info

        self.subpages = []

        logger.debug('Конец инициализации')

    def add_subpage(self, page: object) -> None:
        """
        Добавляет объект страницы к списку в атрибуте self.subpages.
        """
        if isinstance(page, object):
            self.subpages.append(page)
            return
        raise ValueError('Неверный формат данных (верный - object).')


class Slide:
    """
    Базовый класс слайда
    """
    image = str_value('image')

    def __init__(self,
                 image: str,  # путь к изображению
                 ):
        self.image = image


class Carousel_slide(Slide):
    """
    Слайд карусели
    """
    link = str_value('link')
    title = str_value('title')
    description = str_value('description')
    info = dict_value('carousel_slide_info')

    def __init__(self,
                 image: str,            # путь к изображению
                 link: str = '#',       # ссылка (url Для клика)
                 title: str = '',       # заголовок слайда
                 description: str = '', # описание слайда
                 info = {},             # прочая информация (словарь)
                 ):
        # __init__ базового класса
        Slide.__init__(self, image=image)

        self.link = link
        self.title = title
        self.description = description
        self.info = info


class Carousel:
    """
    Класс карусели
    """
    slides = list_value('slides')
    name = str_value('name')

    def __init__(self,
                 name: str,
                 ):
        self.slides = []  # слайды карусели
        self.name = name  # имя карусели

    def add_slide(self, slide: object) -> None:
        """
        Добавляет слайд к слайдам карусели
        """
        self.slides.append(slide)


class Gallery:
    """
    Класс галереи
    """
    name = str_value('name')
    __folder = str_value('folder')
    slides = list_value('slides')

    def add_slide(self, slide: object) -> None:
        """
        Добавляет слайд к галерее
        """
        self.slides.append(slide)

    def __load_slides(self):
        """
        Загружает слайды из папки (информацию о файлах)
        """
        folder = self.__folder
        pass

    def __init__(self, name: str,           # имя галереи
                 folder: str,               # папка с  файлами для галереи
                 auto_load: bool = True,    # автозагрузка галереи при создании
                 ):
        self.name = name
        self.__folder = folder
        self.slides =[]
        # загрузить слайды
        if auto_load:
            self.__load_slides()


class Promo_card:
    pass
