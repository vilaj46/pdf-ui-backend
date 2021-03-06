import json
import fitz
import ast

from utilities.misc.get_tmp_path import get_tmp_path
from utilities.misc.allowed_file import allowed_file

from classes.Redactor import Redactor
from classes.Metadata import Metadata


class File:
    def __init__(self):
        """ fileName, filePath, pageCount """
        self.data = {}
        self.doc = {}

    def initialize_uploaded_document(self, file_name, file_path, metadata):
        open_file = fitz.open(file_path, filetype="pdf")
        self.doc = open_file
        corrected_metadata = self.create_metadata(
            metadata, self.doc.metadata)

        self.data = {
            "fileName": file_name,
            "filePath": file_path,
            "pageCount": open_file.pageCount,
            "metadata": corrected_metadata
        }
        return self.data

    def upload(self, file_storage):
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
                'pageCount': self.doc.pageCount,
                'metadata': self.doc.metadata,
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

    def create_metadata(self, new_metadata, blank_metadata):
        replaced = new_metadata.replace("None", '"None"')
        replaced_second = replaced.replace("null", '"null"')
        ast_metadata = ast.literal_eval(replaced_second)
        keywords = ast.literal_eval(ast_metadata['keywords'])
        blank_metadata['keywords'] = keywords
        return blank_metadata

    def __str__(self):
        return json.dumps(self.data)
