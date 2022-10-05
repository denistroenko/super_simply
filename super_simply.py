import logging
import glob
import os.path

from PIL import Image, ImageEnhance

from baseapplib import get_script_dir, configure_logger
from config import Config
from values import int_value, str_value, list_value, dict_value, bool_value


# Global
# logger
logger = logging.getLogger(__name__)
configure_logger(logger,
                 debug_file_name='{}log/debug.log'.format(get_script_dir()),
                 error_file_name='{}log/error.log'.format(get_script_dir()))
# Site config
config_site = Config()
config_site.read_file(config_file='%sconfig/site' % get_script_dir(),
                      comment='#')
# Pages config
config_pages = Config()
config_pages.read_file(config_file='%sconfig/pages' % get_script_dir(),
                       comment='#')


class Site:
    """
    Класс сайта
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
    albums = dict_value('albums')
    title_rule = str_value('title_rule')
    h1_rule = str_value('h1_rule')
    description_rule = str_value('description_rule')
    keywords_rule = str_value('keywords_rule')
    thumbnail_sizes = dict_value('thumbnail_sizes')

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

        self.albums = {}        # "альбомы" - словарь имен:объектов альбомов
        self.thumbnail_sizes = {}  # размеры эскизов для альбомов:
                                   # имя:строка в формате 'width,height'

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
            return self.get_system_page('_404')

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
    Класс страницы сайта
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


class Thumbnail:
    name = str_value('name')
    src = str_value('src')
    slide_path = str_value('slide_path')

    def __init__(self,
                 path: str,         # путь к эскизу
                 slide_src: str,    # путь к оригинальному слайду от /static/
                 width: int=0,      # ширина эскиза в пикселях
                 height: int=0,     # высота эскиза в пикселях
                 ):
        self.path = path
        self.slide_src = slide_src
        self.width = width
        self.height = height

    @property
    def src(self):
        thumbnail_full_dir = f'{get_script_dir()[:-1]}{os.path.dirname(self.path)}'
        thumbnail_full_name = f'{get_script_dir()[:-1]}{self.path}'
        slide_full_name = f'{get_script_dir()[:-1]}{self.slide_src}'

        # Create folder if not exist
        if not os.path.exists(thumbnail_full_dir):
            os.mkdir(thumbnail_full_dir)

        # Create thumbnail if file not exist
        if not os.path.exists(thumbnail_full_name):
            try:
                with Image.open(slide_full_name) as im:
                    if self.height == 0:
                        width, height = im.size
                        self.height = int(self.width * height / width)

                    if self.width == 0:
                        width, height = im.size
                        self.width = int(self.height * width / height)

                    print(self.height)

                    resized_im = im.resize((self.width, self.height), Image.ANTIALIAS)
                    resized_im = ImageEnhance.Sharpness(resized_im).enhance(1.5)
                    resized_im.save(thumbnail_full_name, "JPEG", quality=80)
                    logger.debug(f'{thumbnail_full_name} {self.width}x{self.height}')
            except Exception as e:
                logger.error(f'Не удалось создать thumbnail {self.slide_src}: {e}')

        return self.path


class Slide:
    """
    Базовый класс слайда
    """
    name = str_value('name')
    src = str_value('src')
    thumbnails = dict_value('thumbnails')
    thumbnail_sizes = dict_value('thumbnail_sizes')

    def __init__(self,
                 name: str,  # название слайда
                 path: str,  # полный путь к изображению
                 thumbnail_sizes: dict={}, # словарь размеров эскиза
                                           # 'имя':(width: int, height: int)
                 ):


        # имя слайда - без расширения
        self.name = str(name.split('.')[0])

        # путь к файлу - от текущей директории скрипта
        script_dir = get_script_dir()
        path = path[len(script_dir)-1:]
        self.src = path
        self.thumbnail_sizes = thumbnail_sizes

        self.thumbnails = {}

        self.load_thumbnails()

    def load_thumbnails(self):
        # заполнить свойство thimbnails обхектами эскизов
        for size_name in self.thumbnail_sizes:
            width = self.thumbnail_sizes[size_name][0]
            height = self.thumbnail_sizes[size_name][1]
            # имя создать по правилу widh x height имя_слайда
            file_name = os.path.basename(self.src)
            dir_name = os.path.dirname(self.src)
            path = f'{dir_name}/_thumbnail_{width}x{height}_{file_name}'

            self.thumbnails[size_name] = Thumbnail(path=path,
                                                   slide_src=self.src,
                                                   width=width,
                                                   height=height,
                                                   )


class Album:
    """
    Класс альбома
    """
    name = str_value('name')
    __path = str_value('folder')
    slides = list_value('slides')
    thumbnail_sizes = dict_value('thumbnail_sizes')

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
            name = os.path.basename(file_path)

            if name[:10] != '_thumbnail':
                slide = Slide(name=name,
                            path=file_path,
                            thumbnail_sizes=self.thumbnail_sizes,
                            )

                self.add_slide(slide)

    def __init__(self, name: str,           # имя альбома
                 path: str,                 # полный путь альбома в ФС
                 auto_load: bool = True,    # автозагрузка при создании
                 sort_slides: bool = True,  # сортировать слайды в альбоме
                 thumbnail_sizes: tuple=(), # размеры слайдов
                 ):
        self.slides =[]                     # слайды альбома (список)
        self.name = name
        self.__path = path
        self.thumbnail_sizes = thumbnail_sizes

        # загрузить слайды
        if auto_load:
            self.__load_slides(sort_slides=sort_slides)

    def get_path(self):
        """
        Метод возвращает полный путь к альбому в рамках ФС
        """
        return(self.__path)


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

    # Заполнить свойство сайта (словарь) thumbnail_sizes
    try:
        thumbnail_sizes = config_site.get_section_dict('thumbnails')
    except KeyError:
        return
    # Преобразуем строку в кортеж int
    new_thumbnail_sizes = {}
    for size in thumbnail_sizes:
        # из строки делаем список размеров
        sizes = thumbnail_sizes[size].split(',')
        if len(sizes) > 1:  # берем только, если длина списка не менее 2-х
            # обрезать до 2-х элементов
            sizes = sizes[:2]
            try:
                new_thumbnail_sizes[size] = (int(sizes[0].strip()),
                                             int(sizes[1].strip()),
                                             )
            except Exception:
                logger.debug('Ошибка преобразования в кортеж int настройки ' \
                             + 'размера альбома: ' + size)

    site.thumbnail_sizes = new_thumbnail_sizes


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

    new_page = Page(name='error 404',
                    path='/_404',
                    template='_404.html',
                    )
    site.add_system_page(page=new_page, key='_404')

    new_page = Page(name='seo test',
                    path='/_seo',
                    template='_seo.html',
                    )
    site.add_system_page(page=new_page, key='_seo')


    new_page = Page(name='form completed',
                    path='/_form_completed',
                    template='_form_completed.html',
                    )
    site.add_system_page(page=new_page, key='_form_completed')


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
                      thumbnail_sizes=site.thumbnail_sizes,
                      )

        logger.debug(f"Добавление к сайту альбома '{album_name}'" + \
                     f", полный путь {albums_folders[album_name]}"
                     )

        site.add_album(album)
