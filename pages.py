import logging
from super_simply import Page
from baseapplib import Config, get_script_dir, configure_logger


# Global
config_site = Config()
config_site.read_file('%sconfig/config_site' % get_script_dir())
config_pages= Config()
config_pages.read_file('%sconfig/config_pages' % get_script_dir())
logger = logging.getLogger(__name__)
configure_logger(logger)


def configure_site(site: object):
    logger.debug('Конфигурирование сайта')

    site.name = 'Super Simply'
    site.domain = 'localhost'
    site.author = 'Super Simply'
    site.phone = ''
    site.address = ''

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

    for page_name in settings:
        logger.debug('Добавление страницы')

        path = '/'
        if 'path' in settings[page_name]:
            path = settings[page_name]['path']

        template = 'page.html'
        if 'template' in settings[page_name]:
            template = settings[page_name]['template']

        parent = -1
        if 'parent' in settings[page_name]:
            parent = int(settings[page_name]['parent'])

        title = '{} - {} {}'.format(page_name, site.name, site.domain)
        if 'title' in settings[page_name]:
            title = settings[page_name]['title']

        h1 = page_name
        if 'h1' in settings[page_name]:
            h1 = settings[page_name]['h1']

        description = '{} {} {} {}'.format(site.name,
                                           h1,
                                           site.address,
                                           site.phone,
                                           )
        if 'description' in settings[page_name]:
            description = settings[page_name]['description']

        keywords = ''
        if 'keywords' in settings[page_name]:
            keywords = settings[page_name]['keywords']

        visible = True
        if 'visible' in settings[page_name]:
            visible = settings[page_name]['visible']

        aliases = []
        if 'aliases' in settings[page_name]:
            aliases = settings[page_name]['aliases'].split(',')

        img = ''
        if 'img' in settings[page_name]:
            img = settings[page_name]['img']

        icon = ''
        if 'icon' in settings[page_name]:
            icon = settings[page_name]['icon']

        new_page = Page(name=page_name,
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
