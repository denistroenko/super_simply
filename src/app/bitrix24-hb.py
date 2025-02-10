use_bitrix24 = True

# Попытаться импортировать модуль fast_bitrix24
try:
    from fast_bitrix24 import Bitrix
except ModuleNotFoundError:
    use_bitrix24 = False

web_hook = 'https://goodbass.bitrix24.ru/rest/10/g8me05jmvtq18p7z/'

b = Bitrix(web_hook)

method = 'crm.lead.add'

site_name = 'хорошиебассейны.рф'
name = 'ТЕСТ_ДЕНИС_ТРОЕНКО'
second_name = ''
last_name = ''
phone = '89034315996'
comments = ''
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
