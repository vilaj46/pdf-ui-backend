import fitz


def create_page_number_rect():
    return fitz.Rect(0, 22, 612, 100)
