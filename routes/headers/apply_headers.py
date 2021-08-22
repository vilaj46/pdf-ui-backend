import fitz


# from routes.headers.utils.is_multiple_page_header import is_multiple_page_header
# from routes.headers.utils.detect_if_header_exists import detect_if_header_exists

from utilities.misc.get_tmp_path import get_tmp_path
from utilities.misc.has_page_range_error import has_page_range_error

# from utilities.metadata.metadata_add_header import metadata_add_header
# from utilities.metadata.metadata_update_creator import metadata_update_creator

from api import file
from api import headers

from classes.Metadata import Metadata


def apply_headers():
    headers_data = headers.data
    auto_spacing = headers.auto_spacing

    headers_are_good = headers.check_headers()

    if headers_are_good == True:
        for header in headers_data:
            try:
                header_start = int(header.data['startPage'])
                header_end = int(header.data['endPage'])
                pr_error = has_page_range_error(header_start, header_end)

                if pr_error == False:
                    multiple_pages = header.is_multiple_page_header()

                    if multiple_pages == True:
                        file.add_header(
                            header=header, auto_spacing=auto_spacing, multiple=True)
                    else:
                        file.add_header(
                            header=header, auto_spacing=auto_spacing, multiple=False)
            except:
                print("ERROR APPLYING HEADERS")
                continue

        headers.reset()
    return headers
