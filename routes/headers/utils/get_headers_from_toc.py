import fitz
import re

from routes.headers.utils.unify_dots import unify_dots
from routes.headers.utils.remove_new_lines import remove_new_lines
from routes.headers.utils.remove_new_lines import remove_new_lines
from routes.headers.utils.get_entries_from_page import get_entries_from_page


def get_headers_from_toc(file_storage, headers):
    file_stream = file_storage.stream.read()
    toc_doc = fitz.open(stream=file_stream, filetype="pdf")

    for i in range(toc_doc.pageCount):
        page = toc_doc.loadPage(i)
        text = page.getText()

        text = text.encode("utf-8")

        text = str(text)
        text_without_dots = unify_dots(text)
        text_without_new_lines = remove_new_lines(text_without_dots)

        # Right QUOTATION MARK taken out.
        text_without_utf = re.sub(
            r'\\xe2\\x80\\x99', "'", text_without_new_lines)

        get_entries_from_page(
            text_without_utf, i, headers)

    return headers
