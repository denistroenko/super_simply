import logging
from super_simply import Page
from baseapplib import Config, get_script_dir, configure_logger


# Global
config_site = Config()
config_site.read_file('%sconfig/config_site' % get_script_dir(),
                      comment='//',
                      )
config_pages= Config()
config_pages.read_file('%sconfig/config_pages' % get_script_dir(),
                       comment='//',
                       )
logger = logging.getLogger(__name__)
configure_logger(logger)


def configure_site(site: object):
    logger.debug('Конфигурирование сайта')

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


def load_pages(site: object):
    logger.debug('Добавление страниц в сайт')
    settings = config_pages.settings  # dict

    # Умолчания
    path = '/'
    template = 'page.html'
    parent = -1
    title = '{} - {} {}'.format(name, site.name, site.domain)
    h1 = name
    description = '{} {} {} {}'.format(site.name, h1, site.address, site.phone)
    keywords = ''
    visible = True
    aliases = []
    img = ''
    icon = ''

    # проходим по именам секций
    for name in settings:
        logger.debug('Добавление страницы %s' % name)
        # проходим по параметрам секций
        for parameter in settings[name]:
            value = settings[name][parameter]

            if value == 'path':
                path = value
                continue
            elif value == 'template':
                template = value
                continue
            elif value == 'parent':
                try:
                    parent = int(value)
                except ValueError:
                    logger.error('В файле конфигурации страниц parent - не число!')
                continue
            elif value == 'title':
                title = value
                continue
            elif value == 'h1'
                h1 = value
                continue
            elif value == 'description'
                description = value
                continue
            elif value == 'keywords'
                keywords = value
                continue
            elif value == 'visible'
                visible = value
                continue
            elif value == 'aliases'
                aliases = value
                continue
            elif value == 'image'
                img = value
                continue
            elif value ==
                icon = value
                continue
            elif value ==
                name = value
                continue

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
                        img=img,
                        icon=icon,
                        )

        site.add_page(page=new_page)


def load_system_pages(site: object):
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
