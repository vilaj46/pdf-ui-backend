import random
import math


""" PDF could have 612x792 dimensions.

The horizontal center would be: 303
Y values are 11 apart.

MAX_CHARS_PER_LINE = 90
"""


class Header():

    """
    Grab the necessary values first.

    Then set the header values we will need to set the header.

    text, startPage, endPage, idNumber, autoSpaced
    """

    def __init__(self, keys=[], values=[], headers_length=0):
        self.data = {}
        key_len = len(keys)
        value_len = len(values)
        self.MAX_CHARS_PER_LINE = 90

        if key_len > 0 or value_len > 0:
            for i in range(len(keys)):
                current_key = keys[i]
                current_value = values[i]
                self.data[current_key] = current_value

            rand_id = str(random.randint(1, 1000000000))
            self.data['idNumber'] = rand_id
            self.data['autoSpaced'] = self.auto_space_text(
                self.data['text'])
        else:
            page_range = str(headers_length + 1)
            rand_id = str(random.randint(1, 1000000000))
            self.data = {
                'text': '',
                'startPage': page_range,
                'endPage': page_range,
                'idNumber': rand_id,
                'autoSpaced': '',
                'isAutoSpaced': False
            }

    def update_values(self, keys, values):
        for i in range(len(keys)):
            current_key = keys[i]
            current_value = values[i]
            self.data[current_key] = current_value
            if current_key == 'text':
                # Update the autoSpace property.
                self.data['autoSpaced'] = self.auto_space_text(current_value)

    def auto_space_text(self, text):
        if len(text) <= self.MAX_CHARS_PER_LINE:
            return text

        lines = self.create_lines(text)
        spaced_string = ""
        for line in lines:
            spaced_string = spaced_string + line + '\n'

        if len(lines) > 0:
            return spaced_string

    def create_lines(self, text):
        lines = []
        text_len = len(text)
        iterations = math.ceil(text_len / self.MAX_CHARS_PER_LINE)
        temp_text = text

        for i in range(iterations):
            # Dont end in page range, dated, sworn to
            line = ""

            if i == 0:  # First line
                line = self.slice_no_words(temp_text, self.MAX_CHARS_PER_LINE)
            else:  # After first line
                line = self.slice_no_words(temp_text, len(lines[i - 1]))

            # Check if line ends with page range. ([pages])
            line = self.do_not_end_with_sub_string('[pages', line)
            # Check if line ends with dated.
            line = self.do_not_end_with_sub_string('dated', line)
            # Check if line ends with sworn to. This will be a multi sub_string.
            lines.append(line)
            temp_text = temp_text[len(line):]

        return lines

    def slice_no_words(self, text, range):
        temp_text_len = len(text)

        if temp_text_len > range:
            sliced = text[0:range]
            index_of_last_space = sliced.rindex(' ')
            return sliced[0:index_of_last_space].strip()
        else:
            return text

    def do_not_end_with_sub_string(self, sub_string, line):
        len_sub_string = len(sub_string)
        len_line = len(line)

        try:
            if line.rindex(sub_string) == len_line - len_sub_string:
                sliced_off_pages = line[0:len_line - len_sub_string]
                return sliced_off_pages.strip()
            else:
                return line.strip()
        except:
            return line.strip()

    def setY(self):
        return 33

    def is_multiple_page_header(self):
        if self.data['startPage'] != self.data['endPage']:
            return True
        else:
            return False

    def __str__(self):
        data_keys = list(self.data.keys())
        data_values = list(self.data.values())
        string = ""
        length = len(data_keys)
        for i in range(length):
            current_key = data_keys[i]
            current_value = str(data_values[i])
            if i == length - 1:
                string = string + '   "' + current_key + '" : ' + current_value
            else:
                string = string + '   "' + current_key + '" : ' + current_value + "\n"
        return "{{\n{strung}\n}}".format(strung=string)
