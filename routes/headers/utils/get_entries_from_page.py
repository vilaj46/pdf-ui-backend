import re

from routes.headers.utils.find_5531_index import find_5531_index
from routes.headers.utils.find_cert_index import find_cert_index
from routes.headers.utils.contains_2105 import contains_2105

from utilities.misc.get_romans import get_romans
from utilities.misc.is_number import is_number


def get_entries_from_page(page_text, page_num, headers):
    page_text = page_text.strip()

    split_text_entries = re.split(r'\s{1,}>\s{1,}\d+ ', page_text)
    split_text_numbers = re.split(r'\s{1,}>', page_text)

    page_numbers = find_page_numbers(split_text_numbers)

    ff31_index = find_5531_index(split_text_entries)

    if ff31_index != None and ff31_index == 0:
        split_text_entries[ff31_index] = 'Statement Pursuant to CPLR Rule 5531'

    cert_index = find_cert_index(split_text_entries)
    split_text_entries.reverse()

    if cert_index != None and cert_index > 0:
        twenty_105 = contains_2105(split_text_entries[cert_index])
        split_text_entries = split_text_entries[0:cert_index]
        if twenty_105 == True:
            split_text_entries.append(
                'Certification Pursuant to CPLR Rule 2105')

    fixed_entries = []
    for i in range(len(split_text_entries)):
        entry = split_text_entries[i]
        entry = entry.strip()

        if i == 0:
            entry = remove_roman_numeral(entry, page_num)

        if len(entry) > 0 and entry != "'":
            fixed_entries.append(entry)

    for i in range(len(fixed_entries)):
        entry = fixed_entries[i]

        page_number_in_pdf = page_numbers[i]
        headers.create_and_add(entry, page_number_in_pdf)

    return headers


def remove_roman_numeral(entry, page):
    romans = get_romans()
    roman = romans[page]

    entry = str(entry)

    if 'Table of Contents' in entry:
        index_of_toc = entry.index('Contents') + len('Contents')
        sliced_entry = entry[index_of_toc:len(entry)].strip()

        index_of_roman = sliced_entry.index(roman) + len(roman)
        entry_wo_roman = sliced_entry[index_of_roman: len(sliced_entry)]
        return entry_wo_roman
    else:
        return entry


def find_page_numbers(entries):
    page_numbers = []
    for entry in entries:
        entry = entry.strip()
        first_white_space = entry.index(' ')
        potential_number = entry[0:first_white_space]

        if is_number(potential_number) == True:
            page_numbers.append(potential_number)

    return page_numbers
