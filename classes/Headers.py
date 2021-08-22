import json
from routes.headers.utils.add_page_ranges import add_page_ranges

from utilities.misc.get_keys_or_values import get_keys_or_values
from utilities.misc.is_number import is_number

from routes.headers.utils.find_header_with_id import find_header_with_id
from routes.headers.utils.add_page_ranges import add_page_ranges
from routes.headers.utils.remove_page_ranges import remove_page_ranges

from classes.Header import Header


class Headers():

    """
    Will contain a list of Header(s).
    """

    def __init__(self):
        self.data = []
        self.have_page_ranges = False
        self.auto_spacing = False

    # Used in the reset route to normalize the data.
    def reset(self):
        self.data = []
        self.have_page_ranges = False
        self.auto_spacing = False

    def default_settings(self):
        self.have_page_ranges = False
        self.auto_spacing = False

    # Add blank header to the list.
    # Create it in the backend and update the front end.
    def add_header(self):
        # Used to determine the startPage and endPage.
        len_of_headers = len(self.data)
        new_header = Header(headers_length=len_of_headers)
        self.data.append(new_header)

    def create_and_add(self, text, page_num):
        keys = ['text', 'startPage', 'endPage', 'autoSpaced']
        values = [text, str(page_num), str(page_num), text]
        new_header = Header(keys, values, page_num)
        self.data.append(new_header)

    # Get the index of the header we are looking for.
    def get_header(self, id_number):
        index = find_header_with_id(id_number, self.data)
        return self.data[index].data

    def update_header(self, form):
        id_number = form["idNumber"]
        index = find_header_with_id(id_number, self.data)

        if index != -1:
            keys = get_keys_or_values("keys", form)
            values = get_keys_or_values("values", form)

            found_header = self.data[index]
            found_header.update_values(keys, values)
            self.data[index] = found_header

    def remove_header(self, id_number):
        index = find_header_with_id(id_number, self.data)
        self.data = self.data[0:index] + self.data[index + 1: len(self.data)]

    def swap_headers(self, id_number, direction):
        index = find_header_with_id(id_number, self.data)

        if direction == "up":
            if index != 0:
                header_pushed = self.data[index]
                header_temp = self.data[index - 1]
                self.data[index] = header_temp
                self.data[index - 1] = header_pushed
        else:
            if index != len(self.data) - 1:
                header_pushed = self.data[index]
                header_temp = self.data[index + 1]
                self.data[index] = header_temp
                self.data[index + 1] = header_pushed

    def toggle_page_ranges(self, status, file):
        headers = self.data
        page_count = file.data['pageCount']

        temp_headers = []

        if status == 'on':
            self.have_page_ranges = True
            temp_headers = add_page_ranges(headers, page_count)
        else:
            self.have_page_ranges = False
            temp_headers = remove_page_ranges(headers)

        self.data = temp_headers

    def toggle_auto_spacing(self, status):
        if status == 'on':
            self.auto_spacing = True
            self.toggle_header_auto_spacing(True)
        else:
            self.auto_spacing = False
            self.toggle_header_auto_spacing(False)

    def toggle_header_auto_spacing(self, status):
        for i in range(len(self.data)):
            header = self.data[i]
            header.data['isAutoSpaced'] = status
            self.data[i] = header

    def to_dict_list(self):
        headers = self.data
        temp_list = []
        for header in headers:
            temp_list.append(header.data)

        return temp_list

    def check_headers(self):
        """ endPage, startPage, text """
        headers = self.data
        for header in headers:
            text = header.data['text'].strip()
            end_page = header.data['endPage'].strip()
            start_page = header.data['startPage'].strip()
            text_len = len(text)
            end_len = len(end_page)
            start_len = len(start_page)

            if text_len <= 0 or end_len <= 0 or start_len <= 0:
                return False

            start_is_number = is_number(start_page)
            end_is_number = is_number(end_page)

            if start_is_number == False or end_is_number == False:
                return False

        return True

    def __str__(self):
        strung = '[\n'
        data_len = len(self.data)

        if data_len == 0:
            return '[]'

        for i in range(0, data_len):
            header = self.data[i]
            header_string = header.__str__()

            strung = strung + header_string + ', '
            if i == data_len - 1:
                strung = strung + '\n]'
        return strung
