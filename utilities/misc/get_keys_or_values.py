def get_keys_or_values(property, form):
    if property == "keys":
        keys = form.keys()
        keys = list(keys)
        return keys
    else:
        values = form.values()
        values = list(values)
        return values
