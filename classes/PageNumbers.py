import json
import fitz

from api import FILE
from classes.Metadata import Metadata
from classes.Redactor import Redactor
from utilities.misc.create_page_number_rect import create_page_number_rect


class PageNumbers:
    def apply_page_numbers(page_numbers):
        if FILE.data == {} or len(FILE.data.keys()) == 0:
            return

        loaded_options = json.loads(page_numbers)
        page_range = loaded_options["range"]
        template = loaded_options["text"]
        start_page = int(loaded_options["startPage"])
        end_page = int(loaded_options["endPage"])
        open_file = fitz.open(FILE.data["filePath"], filetype="pdf")

        metadata = open_file.metadata
        m_d = Metadata(metadata)

        if page_range == "all":
            page_count = open_file.pageCount
            start_page = 1
            end_page = page_count + 1
        else:
            end_page = end_page + 1

        for i in range(start_page, end_page):
            page_number_appears_on = i - 1

            if page_number_appears_on >= open_file.pageCount:
                continue

            already_has_page_number = m_d.page_has_number(
                page_number_appears_on)

            rect = create_page_number_rect()
            if already_has_page_number:
                page = open_file.loadPage(page_number_appears_on)
                page.addRedactAnnot(rect, fill=(255, 255, 255))
                page.apply_redactions()

            templated_page_number = use_template(template, str(i))

            page = open_file.loadPage(page_number_appears_on)

            page.insertTextbox(rect, templated_page_number, fontsize=12,
                               fontname='Times-Bold', align=1)

            new_metadata = FILE.add_page_number_to_metadata(
                True, templated_page_number, page_number_appears_on, open_file)

            open_file.setMetadata(new_metadata)

        open_file.saveIncr()
        open_file.close()


def use_template(template, number):
    try:
        before_brackets = template.index("<<")
        after_brackets = template.index(">>")

        if before_brackets != -1 and after_brackets != -1:
            return template[0:before_brackets] + str(number) + template[after_brackets + 2:len(template)]
        else:
            return template
    except:
        return template
