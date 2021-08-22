from utilities.misc.allowed_file import allowed_file

from routes.headers.utils.get_headers_from_toc import get_headers_from_toc


def upload_toc(file_storage, headers):
    file_name = file_storage.filename
    # Read lines and create headers off them.
    # Use the other file
    allow_file = allowed_file(file_name)

    if allow_file == True:
        new_headers = get_headers_from_toc(file_storage, headers)
        # print(new_headers)
        return new_headers
    else:
        return {}
