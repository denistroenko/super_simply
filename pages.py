import logging
from super_simply import Page, Empty_page
from baseapplib import Config, get_script_dir, configure_logger


# Global
config_site = Config()
config_site.read_file('%sconfig_site' % get_script_dir())
config_pages= Config()
config_pages.read_file('%sconfig_pages' % get_script_dir())
logger = logging.getLogger(__name__)
configure_logger(logger)


def configure_shadow_site(site: object):
    site.name = 'Shadow Site'
    site.path = ''
    site.domain = 'shadow site'

    site.pages['error 404'] = Page('Error 404',
                                   '404.html',
                                   '404.html',
                                   )


def configure_site(site: object):
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

    site.pages[domain] = Empty_page()


def load_pages(site: object):
    settings = config_pages.settings  # dict

    for page in settings:
        name = 'PAGE NAME'
        if 'name' in settings[page]:
            name = settings[page]['name']

        path = '/'
        if 'path' in settings[page]:
            path = settings[page]['path']

        template = 'page.html'
        if 'template' in settings[page]:
            template = settings[page]['template']

        parent = 0
        if 'parent' in settings[page]:
            parent = settings[page]['parent']

        title = ''
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

        site.add_page(Page(name=name,
                           path=path,
                           template=template,
                           parent=parent,
                           title=title,
                           h1=h1,
                           description=description,
                           keywords=keywords
                           )
                      )
