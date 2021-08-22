import re
import fitz

# https://www.geeksforgeeks.org/pdf-redaction-using-python/


class Redactor:

    # static methods work independent of class object
    @staticmethod
    def get_sensitive_data(text_for_redaction, lines):
        """ Function to get all the lines """
        for line in lines:
            # This is for when we add page ranges. Our search cannot find them.
            if line == text_for_redaction:
                yield line
            elif re.search(text_for_redaction, line, re.IGNORECASE):
                search = re.search(text_for_redaction, line, re.IGNORECASE)
                yield search.group(0)
            else:
                split_text = text_for_redaction.split('\n')
                for i in split_text:
                    yield i

    # constructor

    def __init__(self, text_for_redaction, page_number, file_path):
        # self.doc = doc
        self.doc = fitz.open(file_path, filetype="pdf")
        self.page_number = page_number
        self.file_path = file_path
        self.text_for_redaction = text_for_redaction

    def redaction(self):
        """ main redactor code """
        self.page = self.doc.loadPage(self.page_number)

        # _wrapContents is needed for fixing
        # alignment issues with rect boxes in some
        # cases where there is alignment issue
        self.page._wrapContents()

        # geting the rect boxes which consists the matching email regex
        sensitive = self.get_sensitive_data(self.text_for_redaction, self.page.getText("text")
                                            .split('\n'))

        for data in sensitive:
            areas = self.page.searchFor(data)
            for area in areas:
                difference = abs(33 - area.y0)
                if difference <= 10:
                    self.page.addRedactAnnot(area, fill=(255, 255, 255))
                elif len(self.text_for_redaction) == 1:
                    # Same as NewHeaders function.
                    rect = fitz.Rect(0, 33, 612, 100)
                    self.page.addRedactAnnot(rect, fill=(255, 255, 255))

        # applying the redaction
        self.page.apply_redactions()

        self.doc.saveIncr()
        self.doc.close()
