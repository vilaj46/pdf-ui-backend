# import json

# from utilities.metadata.metadata_dict_conversion import metadata_dict_conversion


# def metadata_add_header(page_number, header_text, metadata):
#     keywords = metadata_dict_conversion(metadata)

#     keywords[str(page_number)] = {
#         "page_number": int(page_number),
#         "header_text": header_text
#     }

#     metastr = json.dumps(keywords)

#     return metastr
