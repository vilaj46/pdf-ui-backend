import json


class Metadata:
    def __init__(self, metadata):
        self.metadata = metadata
        self.keywords = json.loads(self.metadata['keywords'])

    def page_has_header(self, page_number):
        try:
            page_number_str = str(page_number)
            if self.keywords[page_number_str]:
                header_text = self.keywords[page_number_str]['header']
                if len(header_text) > 0:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def page_has_number(self, page_number):
        try:
            page_number_str = str(page_number)
            if self.keywords[page_number_str]:
                page_number_text = self.keywords[page_number_str]['page_number']
                if len(page_number_text) > 0:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def get_header(self, page_number):
        page_number_str = str(page_number)
        header = self.keywords[page_number_str]
        return header

    def add_header(self, page_number, header):
        pn = str(page_number)
        try:
            if self.keywords[pn]:
                self.keywords[pn]["header"] = header
            else:
                self.keywords[pn] = {
                    "page_number": -1,
                    "header": header
                }
        except:
            self.keywords[pn] = {
                "page_number": -1,
                "header": header
            }

        self.update_keywords()

    def add_page_number(self, page_number, page_number_text):
        pn = str(page_number)
        try:
            if self.keywords[pn]:
                self.keywords[pn]["page_number"] = page_number_text
            else:
                self.keywords[pn] = {
                    "page_number": page_number_text,
                    "header": ""
                }
        except:
            self.keywords[pn] = {
                "page_number": page_number_text,
                "header": ""
            }

        self.update_keywords()

    def update_keywords(self):
        keywords = json.dumps(self.keywords)
        self.metadata['keywords'] = keywords

    # def dict_conversion(self):
    #     headers_str = self.metadata['keywords']
    #     headers_dict = json.loads(headers_str)
    #     return headers_dict

    # def update_creator(self):
    #     who_created_pdf = 'PDF-MAKER'
    #     creator = self.metadata['creator']

    #     if creator != who_created_pdf:
    #         self.metadata['creator'] = who_created_pdf

    def __str__(self):
        return json.dumps(self.metadata)
