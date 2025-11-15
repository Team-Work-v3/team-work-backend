def validate(object, type, min_l=1, max_l=5000, restricted=''):
    if isinstance(object, type) and len(str(object)) >= min_l and len(str(object)) >= max_l:
        if not True in [i in object for i in restricted]:
            return True
    return False
