import fitz
import json
import os
from api import FILE
from classes.Metadata import Metadata
from classes.Redactor import Redactor
from utilities.misc.create_header_rect import create_header_rect
from utilities.misc.get_tmp_path import get_tmp_path


class NewHeaders:
    def applyHeaders(headers):

        if FILE.data == {} or len(FILE.data.keys()) == 0:
            return

        loaded_headers = json.loads(headers)
        headers_keys = loaded_headers.keys()
        open_file = fitz.open(FILE.data["filePath"], filetype="pdf")
        metadata = open_file.metadata
        m_d = Metadata(metadata)

        for key in headers_keys:
            header = loaded_headers[key]
            page_header_appears_on = int(header["startPage"]) - 1

            if page_header_appears_on >= open_file.pageCount:
                continue

            page = open_file.loadPage(page_header_appears_on)
            text = create_text_from_lines(header["lines"])

            single_page = is_single_page_header(header)

            if single_page:
                already_has_header = m_d.page_has_header(
                    page_header_appears_on)
                if already_has_header:
                    # Redact text.
                    header = m_d.get_header(page_header_appears_on)
                    text_to_redact = header['header']

                    open_file.saveIncr()
                    open_file.close()

                    redactor = Redactor(text_to_redact,
                                        page_header_appears_on, FILE.data['filePath'])
                    redactor.redaction()

                    open_file = fitz.open(
                        FILE.data["filePath"], filetype="pdf")
                    page = open_file.loadPage(page_header_appears_on)
                    custom_insert_text_box(page, text)
                else:
                    custom_insert_text_box(page, text)

                new_metadata = FILE.add_header_to_metadata(
                    True, text, page_header_appears_on, open_file)

                open_file.setMetadata(new_metadata)
            else:
                start_page = int(header["startPage"]) - 1
                end_page = int(header["endPage"])
                for i in range(start_page, end_page):
                    already_has_header = m_d.page_has_header(i)
                    if already_has_header:
                        # Redact text.
                        header = m_d.get_header(i)
                        text_to_redact = header['header']

                        open_file.saveIncr()
                        open_file.close()

                        redactor = Redactor(text_to_redact, i,
                                            FILE.data['filePath'])
                        redactor.redaction()

                        open_file = fitz.open(
                            FILE.data["filePath"], filetype="pdf")
                        page = open_file.loadPage(i)
                        custom_insert_text_box(page, text)
                    else:
                        page = open_file.loadPage(i)
                        custom_insert_text_box(page, text)

                    new_metadata = FILE.add_header_to_metadata(
                        True, text, i, open_file)

                    open_file.setMetadata(new_metadata)

        new_file_path = get_tmp_path()
        open_file.save(new_file_path)
        open_file.close()
        FILE.data['filePath'] = new_file_path

        print("APPLIED HEADERS")
        print(FILE)
        print("----------------------")

        return {}


def create_text_from_lines(lines):
    temp = ""
    length = len(lines)
    for i in range(length):
        line = lines[i]
        if i == length - 1:
            if line == "":
                temp = temp + "\n"
            else:
                temp = temp + line
        else:
            if line == "":
                temp = temp + "\n"
            else:
                temp = temp + line + "\n"

    return temp


def header_string_to_dict(header_string):
    temp = header_string + '}'
    return json.loads(temp)


def custom_insert_text_box(page, text):
    rect = create_header_rect()
    page.insertTextbox(
        rect, text, fontsize=12, fontname='Times-Bold', align=1)


def is_single_page_header(header):
    start_page = header["startPage"]
    end_page = header["endPage"]

    if start_page != end_page:
        return False
    return True
