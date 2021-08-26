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

    site.name='Super Simply'
    site.domain=''

    try:
        settings = config_site.get_section_dict('main')
    except KeyError:
        return

    if 'name' in settings:
        site.name = settings['name']

    if 'path' in settings:
        site.path = settings['path']

    if 'domain' in settings:
        site.domain = settings['domain']


def load_pages(site: object):
    logger.debug('Добавление страниц в сайт')
    settings = config_pages.settings  # dict

    for page_name in settings:
        logger.debug('Добавление страницы')
        name = page_name

        path = '/'
        if 'path' in settings[page_name]:
            path = settings[page_name]['path']

        template = 'page_name.html'
        if 'template' in settings[page_name]:
            template = settings[page_name]['template']

        parent = -1
        if 'parent' in settings[page_name]:
            parent = int(settings[page_name]['parent'])

        title = '{} - {} {}'.format(name, site.name, site.domain)
        if 'title' in settings[page_name]:
            title = settings[page_name]['title']

        h1 = ''
        if 'h1' in settings[page_name]:
            h1 = settings[page_name]['h1']

        description = ''
        if 'description' in settings[page_name]:
            description = settings[page_name]['description']

        keywords = ''
        if 'keywords' in settings[page_name]:
            keywords = settings[page_name]['keywords']

        visible = True
        if 'visible' in settings[page_name]:
            visible = settings[page_name]['visible']

        alias_list = []
        if 'alias_list' in settings[page_name]:
            alias_list = settings[page_name]['alias_list'].split(',')

        img = ''
        if 'img' in settings[page_name]:
            img = settings[page_name]['img']

        icon = ''
        if 'icon' in settings[page_name]:
            icon = settings[page_name]['icon']

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
