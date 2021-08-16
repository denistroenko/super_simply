import logging
from super_simply import Page
from baseapplib import Config, get_script_dir, configure_logger


# Global
config_site = Config()
config_site.read_file('%sconfig_site' % get_script_dir())
config_pages= Config()
config_pages.read_file('%sconfig_pages' % get_script_dir())
logger = logging.getLogger(__name__)
configure_logger(logger)


def configure_site(site: object):
    logger.debug('Конфигурирование сайта')
    settings = config_site.get_section_dict('main')

    name = 'SUPER SIMPLY'
    if 'name' in settings:
        name = settings['name']

    path = ''
    if 'path' in settings:
        path = settings['path']

    domain = ''
    if 'domain' in settings:
        domain = settings['domain']

    site.name = name
    site.path = path
    site.domain = domain


def load_pages(site: object):
    logger.debug('Добавление страниц в сайт')
    settings = config_pages.settings  # dict

    for page in settings:
        logger.debug('Добавление страницы')
        name = 'NAME'
        if 'name' in settings[page]:
            name = settings[page]['name']

        path = '/'
        if 'path' in settings[page]:
            path = settings[page]['path']

        template = 'page.html'
        if 'template' in settings[page]:
            template = settings[page]['template']

        parent = -1
        if 'parent' in settings[page]:
            parent = int(settings[page]['parent'])

        title=''
        if 'title' in settings[page]:
            title = settings[page]['title']

        h1 = ''
        if 'h1' in settings[page]:
            h1 = settings[page]['h1']

        description = ''
        if 'description' in settings[page]:
            description = settings[page]['description']

        keywords = ''
        if 'keywords' in settings[page]:
            keywords = settings[page]['keywords']

        visible = True
        if 'visible' in settings[page]:
            visible = settings[page]['visible']

        alias_list = []
        if 'alias_list' in settings[page]:
            alias_list = settings[page]['alias_list'].split(',')

        img = ''
        if 'img' in settings[page]:
            img = settings[page]['img']

        icon = ''
        if 'icon' in settings[page]:
            icon = settings[page]['icon']

        new_page = Page(name=name,
                        path=path,
                        template=template,
                        parent=parent,
                        title=title,
                        h1=h1,
                        description=description,
                        keywords=keywords,
                        visible=visible,
                        alias_list=alias_list,
                        img=img,
                        icon=icon,
                        )

        site.add_page(page=new_page)


def load_system_pages(site: object):
    logger.debug('Добавление страницы 404')

    new_page = Page(name='error 404',
                path='/404',
                template='404.html',
                visible=False,
                )
    site.add_system_page(page=new_page, key='404')

    new_page = Page(name='seo test',
                path='/_seo',
                template='seo.html',
                visible=False,
                )
    site.add_system_page(page=new_page, key='seo')
