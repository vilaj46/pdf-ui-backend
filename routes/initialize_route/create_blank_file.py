def create_blank_file():
    return {
        # Name of file.
        'name': '',
        # We cannot recreate a File object from JavaScript
        # so just use a blank object.
        'file': {
            'name': ''
        },
        # Data which helps us display the pdf on the front end.
        'blob': '',
        # Number of pages in the document.
        'pageCount': 0,

        # KEEP IT THE SAME AS THE ABOVE OBJECT.
        # This will be used to reset the front end state
        # if we close the file or when starting the program up.
        'template': {
            'name': '',
            'file': {},
            'blob': '',
            'pageCount': 0,
        }
    }
