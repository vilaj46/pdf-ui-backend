def has_page_range_error(start, end):
    if end < start:
        return True
    elif start > end:
        return True
    else:
        return False
