def validate_object(object, object_type, min_l=1, max_l=5000, restricted=''):
    if object_type == int and isinstance(type(object), str) and object.isdigit():
        object = int(object)
    if object_type == float and isinstance(type(object), str) and object.isdigit():
        object = float(object)
    if min_l == 0 and (object is None or object == 0 or object == ''):
        return True
    if isinstance(object, object_type) and min_l <= len(str(object)) <= max_l:
        if True not in [i in object for i in restricted]:
            return True
    return False


def validate_greedy(to_check, dict_object, cant_be_empty=True):
    return False not in [i[0] in dict_object.keys() and validate_object(dict_object[i[0]], i[1], int(cant_be_empty))
                         for i in to_check]
