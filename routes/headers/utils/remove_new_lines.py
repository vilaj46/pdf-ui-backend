import re


def remove_new_lines(text):
    text = str(text)
    text_without_lines = re.sub(r'\\n', '', text)
    return text_without_lines
