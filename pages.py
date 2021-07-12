# Global
NAME = 'SUPER SIMPLY'

def configure_site(site: object):
    site.site_name = NAME

def load_pages(site: object):
    site.add_page(url='/',
                  template='home.html',
                  name='Главная',
                  parent=0,
                  title='Главная страница',
                  h1='Заголовок главной страницы',
                  description='Описание страницы',
                  keywords='ключевые слова',
                  access_level=3,
                  )
