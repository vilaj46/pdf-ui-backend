import json
import fitz

from utilities.misc.get_tmp_path import get_tmp_path
from utilities.misc.allowed_file import allowed_file

from classes.Redactor import Redactor
from classes.Metadata import Metadata


class File:
    def __init__(self):
        """ fileName, filePath, pageCount """
        self.data = {}
        self.doc = {}

    def upload(self, file_storage):
        # global file

        file_name = file_storage.filename

        allow_file = allowed_file(file_name)

        if allow_file == True:
            file_path = get_tmp_path()

            file_stream = file_storage.stream.read()

            self.doc = fitz.open(stream=file_stream, filetype="pdf")

            self.reset_metadata()

            self.data = {
                'fileName': file_name,
                'filePath': file_path,
                'pageCount': self.doc.pageCount
            }

            self.doc.save(file_path)
            self.doc.close()

            return self.data
        else:
            return {}

    def close(self):
        self.data = {}
        self.doc = {}

    def reset_metadata(self):
        self.doc.setMetadata({})
        metadata = self.doc.metadata
        metadata['keywords'] = "{}"
        self.doc.setMetadata(metadata)

    def add_header_to_metadata(self, is_open, text, page_number, open_file):
        if is_open:
            curr_metadata = open_file.metadata
            m_d = Metadata(curr_metadata)
            m_d.add_header(page_number, text)
            open_file.metadata = m_d.metadata
            open_file.saveIncr()
            return m_d.metadata
        else:
            # File is closed!.
            open_the = "file"

    def add_page_number_to_metadata(self, is_open, text, page_number, open_file):
        if is_open:
            curr_metadata = open_file.metadata
            m_d = Metadata(curr_metadata)
            m_d.add_page_number(page_number, text)
            open_file.metadata = m_d.metadata
            open_file.saveIncr()
            return m_d.metadata
        else:
            # File is closed!.
            open_the = "file"

    # def add_header_helper(self, metadata, text, page_number):
    #     """
    #         "${page}": {
    #             "${page_number}": int - page number || -1 if None.
    #             "header": str - header text || ""
    #         }
    #     """
    #     keywords = metadata["keywords"]
    #     page_number_to_str = str(page_number)
    #     if keywords[page_number_to_str]:
    #         keywords[page_number_to_str]["header"] = text
    #     else:
    #         keywords[page_number_to_str] = {
    #             "page_number": -1,
    #             "header": text
    #         }
    #     metadata["keywords"] = keywords

    #     return metadata

    # ---------------------------------------------------

    # def create_header_rect(self):
    #     return fitz.Rect(0, 33, 612, 100)

    # def add_header(self, header, auto_spacing, multiple):
    #     if multiple == True:
    #         start_page = int(header.data['startPage'])
    #         end_page = int(header.data['endPage'])
    #         for i in range(start_page - 1, end_page):
    #             self.add_header_meat(header, i, auto_spacing)
    #     else:
    #         start_page = int(header.data['startPage'])
    #         self.add_header_meat(header, start_page - 1, auto_spacing)

    # def add_header_meat(self, header, page_number, auto_spacing):
    #     self.doc = fitz.open(self.data['filePath'], filetype="pdf")
    #     page = self.doc.loadPage(page_number)

    #     detected = self.detect_if_header_exists(page_number)

    #     if detected == True:
    #         self.doc = fitz.open(self.data['filePath'])
    #         page = self.doc.loadPage(page_number)

    #     m_d = Metadata(self.doc.metadata)

    #     if auto_spacing == True:
    #         header_auto_spaced = header.data['autoSpaced']
    #         self.custom_insert_text_box(page, header_auto_spaced)
    #         m_d.add_header(page_number, header_auto_spaced)
    #     else:
    #         header_text = header.data['text']
    #         self.custom_insert_text_box(page, header_text)
    #         m_d.add_header(page_number, header_text)

    #     m_d.update_creator()

    #     self.doc.setMetadata(m_d.metadata)

    #     self.doc.saveIncr()
    #     self.doc.close()

    # def custom_insert_text_box(self, page, text):
    #     rect = self.create_header_rect()
    #     page.insertTextbox(
    #         rect, text, fontsize=12, fontname='Times-Bold', align=1)

    def detect_if_header_exists(self, page_number):
        # Check if header_text has a length greater than 0.
        m_d = Metadata(self.doc.metadata)
        has_header = m_d.page_has_header(page_number)

        # If header, change to new value.
        if has_header == True:
            header = m_d.get_header(page_number)
            header_text = header['header_text']
            redactor = Redactor(header_text,
                                page_number, self.data['filePath'])
            redactor.redaction()
            return True
        else:
            return False

    def __str__(self):
        return json.dumps(self.data)
