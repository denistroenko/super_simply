import logging
from super_simply import Page, Carousel, Carousel_slide
from baseapplib import Config, get_script_dir, configure_logger


# Global
# Site config
config_site = Config()
config_site.read_file('%sconfig/site' % get_script_dir(),
                      comment='#',
                      )
# Pages config
config_pages= Config()
config_pages.read_file('%sconfig/pages' % get_script_dir(),
                       comment='#',
                       )
# Cariusels config
config_carousels = Config()
config_carousels.read_file('%sconfig/carousels' % get_script_dir(),
                       comment='#',
                       )
# Logger
logger = logging.getLogger(__name__)
configure_logger(logger)


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
        path = '#'
        template = 'page.html'
        parent = -1
        title = '{} - {} {}'.format(name, site.name, site.domain)
        h1 = name
        description = '{} {} {} {}'.format(
                site.name, h1, site.address, site.phone)
        keywords = ''
        visible = True
        aliases = []
        image = ''
        icon = ''
        info = None

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
                    logger.error(
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
                aliases = value
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
                info = (parameter, value)

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
        if info is not None:
            new_page.info[info[0]] = info[1]

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
    for name in settings:
        carousel = Carousel(name)

        # Проходим по параметрам секций (имена слайдов)
        # и загружаем слайды в карусель
        for slide in settings[name]:
            value = settings[name][slide]

            # умолчания
            image = ''
            link = "#"
            title = ''
            description = ''

            # Атрибуты слайда получаем через split значения параметра
            # по аргументу |
            slide_attributes = value.split('|')

            # Проходим по атрибутам слайда
            # init count
            i = 0
            for attribute in slide_attributes:
                if i == 0:
                    image = '/static/img/%s' % attribute
                if i == 1:
                    link = attribute
                if i == 2:
                    title = attribute
                if i == 3:
                    description = attribute
                i += 1

            slide = Carousel_slide(image=image, link=link, title=title,
                                   description=description)
            carousel.add_slide(slide=slide)

        # добавить карусель к сайту
        site.add_carousel(carousel)
