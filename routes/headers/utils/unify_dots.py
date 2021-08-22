import re

def unify_dots(text):
    dots_removed = re.sub(r'\.{2,}', ' > ', text)
    dots_removed = check_if_dots_remain(dots_removed)
    return dots_removed

def check_if_dots_remain(string_without_dots):
    search = re.search(r'\.{2,}', string_without_dots)
    if search == None:
        return string_without_dots
    else:
        print('We have to remove the rest of the dots!')
        return string_without_dots