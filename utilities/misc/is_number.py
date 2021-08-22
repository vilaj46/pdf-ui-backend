# def is_number(potential_number):
#     try:
#         int(potential_number)
#         return True
#     except:
#         return False
def is_number(potential_number):
    try:
        number = int(potential_number)
        type_of = type(number)
        if str(type_of) == "<class 'int'>":
            return True
        else:
            return False
    except:
        return False
