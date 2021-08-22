def find_cert_index(entries):
    temp = entries
    temp.reverse()
    for i in range(len(temp)):
        entry = temp[i]
        if 'Certification' in entry:
            return len(temp) - i - 1
    return None