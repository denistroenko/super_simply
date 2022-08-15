import logging
import glob
import os.path
from baseapplib import get_script_dir, configure_logger
from config import Config
from values import int_value, str_value, list_value, dict_value, bool_value


# Global
# logger
logger = logging.getLogger(__name__)
configure_logger(logger,
                 debug_file_name='{}log/debug.log'.format(get_script_dir()),
                 error_file_name='{}log/error.log'.format(get_script_dir()),
                 )
# Site config
config_site = Config()
config_site.read_file(config_file='%sconfig/site' % get_script_dir(),
                      comment='#',
                      )
# Pages config
config_pages = Config()
config_pages.read_file(config_file='%sconfig/pages' % get_script_dir(),
                       comment='#',
                       )
# Carousels config
config_carousels = Config()
config_carousels.read_file(config_file='%sconfig/carousels' % get_script_dir(),
                           comment='#',
                           )

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
    albums = dict_value('albums')

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
        self.albums = {}        # "альбомы" - словарь имен:объектов альбомов
        self.title_rule = '{page.name} - {site.name}'  # SEO-правило title
        self.h1_rule = '{page.name}'                   # SEO-правило h1
        self.description_rule = ''                     # SEO-правило description
        self.keywords_rule = ''                        # SEO-правило keywords
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

        # Если path страницы не заполнен, заполнить исходя из ее названия
        if page.path == '':
            page.path = self.__generate_page_path(page.name)

        # Если title, h1, description и keywords не установлены,
        # заполнить их исходя из правил сайта
        if page.title == '':
            try:
                page.title = self.title_rule.format(page=page, site=self)
            except:
                logger.debug('Ошибка при заполнении из правила title_rule!')
        if page.h1 == '':
            try:
                page.h1 = self.h1_rule.format(page=page, site=self)
            except:
                logger.debug('Ошибка при заполнении из правила h1_rule!')
        if page.description == '':
            try:
                page.description = self.description_rule.format(page=page, site=self)
            except:
                logger.debug('Ошибка при заполнении из правила description_rule!')
        if page.keywords == '':
            try:
                page.keywords = self.keywords_rule.format(page=page, site=self)
            except:
                logger.debug('Ошибка при заполнении из правила keywords_rule!')

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

    def add_album(self, album: object) -> None:
        """
        Добавляет имя (строку) и альбом (объект) в словарь альбомов сайта
        """
        logger.debug('Site.add_album() Добавление альбома на сайт...')
        # присвоить ключ:значение, т.е. имя альбома:объект альбома
        if isinstance(album, Album):
            self.albums[album.name] = album
            logger.debug('Альбом добавлен.')

        else:
            logger.debug('Альбом не добавлен, поскольку не является ' \
                         + 'экземпляром класса Album')

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

    def add_server_info(self, key, info) -> None:
        """
        Добавляет ключ:значение к словарю Site.serer
        """
        self.server[key] = info

    def get_page(self, id, return_404 :bool = True):
        """
        Возвращает объект страницы. id - идентификатор страницы, либо ее путь,
        либо алиас.
        Если страница не найдена - возвращает страницу 404, либо None,
        если return_404 == False
        """

        pages = self.get_pages()

        # перебрать все страницы и найти совпадение id с path, alias или id
        for page in pages:
            if (id == page.path or
                id in page.aliases or
                id == page.id):

                return page

        # Вернуть страницу 404
        if return_404:
            return self.get_system_page('404')

        return None

    def __generate_page_path(self, path: str) -> str:
        # Rules and liters
        english_liters = '-qwertyuiopasdfghjklzxcvbnm1234567890'
        translit_rules = {'а': 'a',
                          'б': 'b',
                          'в': 'v',
                          'г': 'g',
                          'д': 'd',
                          'е': 'e',
                          'ё': 'e',
                          'ж': 'g',
                          'з': 'z',
                          'и': 'i',
                          'й': 'j',
                          'к': 'k',
                          'л': 'l',
                          'м': 'm',
                          'н': 'n',
                          'о': 'o',
                          'п': 'p',
                          'р': 'r',
                          'с': 's',
                          'т': 't',
                          'у': 'u',
                          'ф': 'f',
                          'х': 'h',
                          'ц': 'ts',
                          'ч': 'ch',
                          'ш': 'sh',
                          'щ': 'sh',
                          'ъ': '',
                          'ы': 'y',
                          'ь': '',
                          'э': 'e',
                          'ю': 'yu',
                          'я': 'ya',
                          }
        # lower
        path = path.lower()

        # init
        new_path = ''

        # change symbols from rules
        for letter in path:
            if letter in english_liters:
                new_path += letter
                continue

            if letter in translit_rules:
                new_path += translit_rules[letter]
            else:
                new_path += '-'

        # replace doubles and 0, -1 indexes
        while '--' in new_path:
            new_path = new_path.replace('--', '-')

        if len(new_path) > 1:
            if new_path[0] == '-':
                new_path = new_path[1:]

        if len(new_path) > 1:
            if new_path[-1] == '-':
                new_path = new_path[:-1]

        # double pages
        double_pages_postfix = 1
        try_path = new_path
        while self.is_page(try_path):
            double_pages_postfix += 1
            try_path = '{}-{}'.format(new_path, double_pages_postfix)
            print(try_path)

        new_path = try_path
        return '/%s' % new_path

    def is_page(self, id):
        """
        Возващает True, если искомая страница есть на сайте. False, если нет
        таковой. id - идентификатор страницы, ее путь, либо алиас.
        """
        if self.get_page(id, return_404=False) == None:
            return False

        return True


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

        logger.debug('Конец инициализации. %s' % self.__dict__.items())


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
    name = str_value('name')
    src = str_value('src')

    def __init__(self,
                 name: str, # название слайда
                 path: str,  # полный путь к изображению
                 ):

        # имя слайда без расширения
        self.name = str(name.split('.')[0])

        script_dir = get_script_dir()

        # путь к файлу - от текущей директории скрипта
        path = path[len(script_dir)-1:]
        self.src = path


class Carousel_slide(Slide):
    """
    Слайд карусели
    """
    link = str_value('link')
    title = str_value('title')
    description = str_value('description')
    info = dict_value('carousel_slide_info')

    def __init__(self,
                 name: str,             # имя слайда
                 image: str,            # путь к изображению
                 link: str = '#',       # ссылка (url Для клика)
                 title: str = '',       # заголовок слайда
                 description: str = '', # описание слайда
                 info = {},             # прочая информация (словарь)
                 ):
        # __init__ базового класса
        Slide.__init__(self, name=name, path=image)

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


class Album:
    """
    Класс альбома
    """
    name = str_value('name')
    __path = str_value('folder')
    slides = list_value('slides')

    def add_slide(self, slide: object) -> None:
        """
        Добавляет слайд к галерее
        """
        self.slides.append(slide)

    def __load_slides(self, sort_slides: bool = True):
        """
        Загружает слайды из папки (информацию о файлах)
        """
        folder = self.__path

        jpg_files = glob.glob(f'{folder}/**/*.jpg', recursive=True)
        jpeg_files = glob.glob(f'{folder}/**/*.jpeg', recursive=True)
        png_files = glob.glob(f'{folder}/**/*.png', recursive=True)

        files = jpg_files + jpeg_files + png_files
        if sort_slides:
            files = sorted(files)

        for file_path in files:
            slide=Slide(os.path.basename(file_path),
                        file_path)

            self.add_slide(slide)

    def __init__(self, name: str,           # имя альбома
                 path: str,                 # полный путь альбома в ФС
                 auto_load: bool = True,    # автозагрузка при создании
                 sort_slides: bool = True,  # сортировать слайды в альбоме
                 ):
        self.slides =[]                     # слайды альбома (список)
        self.name = name
        self.__path = path

        # загрузить слайды
        if auto_load:
            self.__load_slides(sort_slides=sort_slides)

    def get_path(self):
        """
        Метод возвращает полный путь к альбому в рамках ФС
        """
        return(self.__path)


class Promo_card:
    pass


def configure_site(site: object) -> None:
    """
    Загружает конфигурацию сайта (передать объект сайта)
    """
    logger.debug('Конфигурирование сайта')

    # умолчания
    site.name = 'Super Simply'
    site.domain = 'localhost'

    try:
        settings = config_site.get_section_dict('main')
    except KeyError:
        return

    for key in settings:
        if key == 'name':
            site.name = settings[key]
        elif key == 'domain':
            site.domain = settings[key]
        elif key == 'author':
            site.author = settings[key]
        elif key == 'company':
            site.company = settings[key]
        elif key == 'phone':
            site.phone = settings[key]
        elif key == 'tel':
            site.tel = settings[key]
        elif key == 'email':
            site.email = settings[key]
        elif key == 'address':
            site.address = settings[key]
        elif key == 'title_rule':
            site.title_rule = settings[key]
        elif key == 'h1_rule':
            site.h1_rule = settings[key]
        elif key == 'description_rule':
            site.description_rule = settings[key]
        elif key == 'keywords_rule':
            site.keywords_rule = settings[key]
        else:
            site.info[key] = settings[key]


def load_pages(site: object) -> None:
    """
    Загружает конфигурацию страниц сайта (передать объект сайта)
    """
    logger.debug('Добавление страниц в сайт')
    settings = config_pages.settings  # dict

    # проходим по именам секций (имена страниц)
    for name in settings:
        logger.debug('Добавление страницы %s' % name)

        # Умолчания
        path = ''
        template = 'page.html'
        parent = -1

        title = ''
        h1 = ''
        description = ''
        keywords = ''

        visible = True
        aliases = []
        image = ''
        icon = ''
        info = {}

        # проходим по параметрам секций (свойства страниц)
        for parameter in settings[name]:
            value = settings[name][parameter]
            if parameter == 'path':
                if value != '':
                    path = value
                continue
            elif parameter == 'template':
                template = value
                continue
            elif parameter == 'parent':
                try:
                    parent = int(value)
                except ValueError:
                    logger.erroer(
                            'В файле конфигурации страниц parent - не число!')
                continue
            elif parameter == 'title':
                title = value
                continue
            elif parameter == 'h1':
                h1 = value
                continue
            elif parameter == 'description':
                description = value
                continue
            elif parameter == 'keywords':
                keywords = value
                continue
            elif parameter == 'visible':
                visible = value
                continue
            elif parameter == 'aliases':
                aliases = value.replace(' ','').split(',')
                continue
            elif parameter == 'image':
                image = value
                continue
            elif parameter == 'icon':
                icon = value
                continue
            elif parameter == 'name':
                name = value
                continue
            else:
                info[parameter] = value

        new_page = Page(name=name,
                        path=path,
                        template=template,
                        parent=parent,
                        title=title,
                        h1=h1,
                        description=description,
                        keywords=keywords,
                        visible=visible,
                        aliases=aliases,
                        image=image,
                        icon=icon,
                        )
        if len(info)>0:
            new_page.info = info

        site.add_page(page=new_page)


def load_system_pages(site: object) -> None:
    """
    Создает системные страницы сайта (передать объект сайта)
    """
    logger.debug('Добавление страницы 404')

    new_page = Page(name='error 404',
                    path='/404',
                    template='404.html',
                    )
    site.add_system_page(page=new_page, key='404')

    new_page = Page(name='seo test',
                    path='/_seo',
                    template='seo.html',
                    )
    site.add_system_page(page=new_page, key='_seo')


def load_carousels(site: object) -> None:
    """
    Загружает конфигурацию каруселей сайта (передать объект сайта)
    """
    settings = config_carousels.settings
    # Проходим по именам секций (имена каруселей)
    for carousel_name in settings:
        carousel = Carousel(carousel_name)

        # Проходим по параметрам секций (имена слайдов)
        # и загружаем слайды в карусель
        for slide_name in settings[carousel_name]:
            value = settings[carousel_name][slide_name]

            # умолчания
            image = ''
            link = "#"
            title = ''
            description = ''
            info = {}

            # Атрибуты слайда получаем через split значения параметра
            # по аргументу |
            slide_attributes = value.split('|')

            # Проходим по атрибутам слайда
            # init count
            i = 0
            for attribute in slide_attributes:
                if i == 0:
                    image = '/static/img/%s' % attribute
                elif i == 1:
                    if attribute:
                        link = attribute
                elif i == 2:
                    title = attribute
                elif i == 3:
                    description = attribute
                else:
                    # разделить attribute по знаку =
                    attribute = attribute.split('=')
                    # отдельно сохраняем разделенные части
                    info_name = attribute[0]
                    info_value = attribute[1]
                    # добавляем в локальный словарь info эти значения как key,
                    # value
                    info[info_name] = info_value
                i += 1

            slide = Carousel_slide(name=slide_name,
                                   image=image,
                                   link=link,
                                   title=title,
                                   description=description,
                                   )
            # заполнить словарь slide.info, если есть, чем
            if info != {}:
                slide.info = info

            # Добавить слайд к карусели
            carousel.add_slide(slide=slide)

        # добавить карусель к сайту
        site.add_carousel(carousel)


def load_albums(site: object) -> None:
    """
    Функция создает альбомы и подключает к сайту в свойство site.albums,
    заполняет альбомы найденными фотографиями
    """
    script_dir = get_script_dir()

    albums_folders = {}  # словарь, содержащий значения названий папок альбомов
                         # и их полных путей

    # получить список всех элементов файловой системы в папке static/albums
    elements = glob.glob('{}static/albums/*'.format(script_dir))

    # пройти по элементам ФС и включить в словарь album_filder только папки
    for element in elements:
        if os.path.isdir(element):
            # полный путь к альбому в файловой системе
            full_path = element
            # имя папки (последний элемент в пути)
            base_name = os.path.basename(element)

            # создать ключ и значение
            albums_folders[base_name] = full_path

    # пройти по словарю, создаьть объекты альбомов, подключить альбомы к сайту
    for album_name in albums_folders:
        album = Album(name=album_name,
                      path=albums_folders[album_name],
                      auto_load=True,
                      sort_slides=True,
                      )

        logger.debug(f"Добавление к сайту альбома '{album_name}'" + \
                     f", полный путь {albums_folders[album_name]}"
                     )

        site.add_album(album)
