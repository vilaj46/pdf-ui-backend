def add_page_ranges(headers, page_count):
    for i in range(len(headers)):
        header = headers[i]
        # Get header text
        header_text = header.data['text']
        header_start_page = header.data['startPage']
        page_range = ""
        try:
            # get next_header start page
            next_header = headers[i + 1]
            next_header_start_page = next_header.data['startPage']
            last_page = int(next_header_start_page) - 1

            if int(header_start_page) - int(last_page) != 0:
                page_range = ' [pages ' + str(header_start_page) + \
                    '-' + str(last_page) + ']'

        except:
            if int(header_start_page) - int(page_count) != 0:
                page_range = ' [pages ' + str(header_start_page) + \
                    ' - ' + str(page_count) + ']'

        text_with_range = header_text + page_range

        headers[i].data['text'] = text_with_range
        spaced_text = headers[i].auto_space_text(text_with_range)
        headers[i].data['autoSpaced'] = spaced_text
    return headers
