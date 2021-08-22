def auto_space_text(MAX_CHARS_PER_LINE, temp_text):
    # Find the last word less than or equal to 90 chars in length.
    # Slice text up until that point and add a new line.
    spaced = ""
    # Continue to do the same thing until our main text is no more.
    # Figure out how to space page ranges at the end.
    while len(temp_text) > 0:
        sliced = slice_words_until_max_chars(MAX_CHARS_PER_LINE, temp_text)
        sliced_len = len(sliced)
        temp_text = temp_text[sliced_len: len(temp_text)].strip()

        if len(temp_text) > 0:
            spaced = spaced + sliced + '\n'
        else:
            spaced = spaced + sliced
    return spaced


def slice_words_until_max_chars(MAX_CHARS_PER_LINE, temp_text):
    temp_text_len = len(temp_text)

    if temp_text_len > MAX_CHARS_PER_LINE:
        sliced = temp_text[0:MAX_CHARS_PER_LINE]
        index_of_last_space = sliced.rindex(' ')
        return sliced[0:index_of_last_space].strip()
    else:
        return temp_text
