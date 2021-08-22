import re


def remove_page_ranges(headers):
    for i in range(len(headers)):
        current_text = headers[i].data['text']

        new_text = re.sub(r'\s\[\w+\s\d+\-\d+\]', '', current_text)
        headers[i].data['text'] = new_text

    return headers
