from config import TGPH_TOKEN
from telegraph import Telegraph
# from telegram.ext.updater import Bot
import requests 



def upload_media_tgph(bot, file):

    tgph = Telegraph(TGPH_TOKEN)
    print(file)

    file = bot.get_file(file_id = file.file_id)
    print(file)
    file_bytes = file.download_as_bytearray()
    

    url = requests.post(
        'https://telegra.ph/upload',
        files={'file': ('file', file_bytes, 'image/jpg')}
    ).json()
    print(url)

    return f'<a href="http://telegra.ph'+ url[0]['src'] +'">&#8203;</a>'
    


def get_method_args(string):
    print(string)
    if string == 'off':
        return 'off', None, None

    if '?' in string:
        method, args = string.split('?')
        kwargs = dict([n.split('=') for n in args.split('&')])
    else:
        method = string
        kwargs = {}
    method, action = method.split()

    return method, action, kwargs




def add_entities(text, entities):
    if text is None:
        return ''
    text = list(text)
    len_p = 0

    teg = {
        'bold'     : '<b>',
        'italic'   : '<i>',
        'code'     : '<code>',
        'pre'      : '<pre>',
        'text_link': '<a href=\"{}\">'
    }
    end_teg = {
        'bold'     : '</b>',
        'italic'   : '</i>',
        'code'     : '</code>',
        'pre'      : '</pre>',
        'text_link': '</a>'
    }
    
    for item in entities:
        start_teg = teg[item['type']]

        if item['type'] == 'text_link':
            start_teg = start_teg.format(item['url'])
        
        text.insert(item['offset'] + len_p, start_teg)
        text.insert(item['offset'] + item['length'] + 1 + len_p, end_teg[item['type']])
        len_p += 2

    return ''.join(text)

        







