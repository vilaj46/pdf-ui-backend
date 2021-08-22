def find_5531_index(entries):
    for i in range(len(entries)):
        entry = entries[i]
        if 'CPLR Rule 5531' in entry:
            return i
    return None
