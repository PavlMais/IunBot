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



