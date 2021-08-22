# import json

# from utilities.metadata.metadata_dict_conversion import metadata_dict_conversion


# def metadata_page_has_header(page_number, metadata):
#     keywords = metadata_dict_conversion(metadata)
#     try:
#         page_number_str = str(page_number)
#         if keywords[page_number_str]:
#             header_text = keywords[page_number_str]['header_text']
#             if len(header_text) > 0:
#                 return True
#             else:
#                 return False
#         else:
#             return False
#     except:
#         return False
