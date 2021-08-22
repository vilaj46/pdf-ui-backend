def find_header_with_id(id_number, headers):
    for i in range(0, len(headers)):
        current_header = headers[i].data
        if current_header["idNumber"] == id_number:
            return i

    return -1
