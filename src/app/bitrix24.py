import logging
#from baseapplib import configure_logger, get_script_dir



#script_dir = get_script_dir(False)

use_bitrix24 = True
#logger = logging.getLogger(__name__)
#configure_logger(logger,
#                 debug_file_name=f'{script_dir}log/debug.log',
#                 error_file_name=f'{script_dir}log/error.log')

# Попытаться импортировать модуль fast_bitrix24
try:
    from fast_bitrix24 import Bitrix
except ModuleNotFoundError:
#    logger.error('Не найден модуль fast_bitrix24. Загрузка и использование ' \
#                 + 'возможностей Битрикс24 отключена.')
    use_bitrix24 = False


web_hook = 'https://algorithmcomputers.bitrix24.ru/rest/1/1lafck1icg1yw470/'


b = Bitrix(web_hook)

method = 'crm.deal.add'

site_name = 'a-computers.ru'
name = 'Денис'
second_name = ''
last_name = ''
phone = '89034311122'
comments = 'Страница: a-computers.ru/test'
source_id = None

title = 'Заполнена форма на сайте %s:' % site_name
form_fields = [name, second_name, last_name, phone]

for field in form_fields:
    if field:
        title += ' %s' % field

params = {
        'fields': {
                "TITLE": title,
                "NAME": name,
                "SECOND_NAME": second_name,
                "LAST_NAME": last_name,
                "STATUS_ID": "NEW",
                "PHONE": [{"VALUE": phone, "VALUE_TYPE": "WORK"}],
                "COMMENTS": comments,
        }
}

# Если указан id источника лида, добавляем в словарь
if source_id:
    params['fields']['SOURCE_ID'] = source_id
print(params['fields'].items())

b.call(method, params)
