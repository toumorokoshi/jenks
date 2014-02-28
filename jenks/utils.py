RANGES = (('0', '9'), ('a', 'z'), ('A', 'Z'))


class JenksException(Exception):
    """ an exception to notify that the exception arrives from jenks """
    pass


def generate_valid_keys():
    """ create a list of valid keys """
    valid_keys = []
    for minimum, maximum in RANGES:
        for i in range(ord(minimum), ord(maximum) + 1):
            valid_keys.append(chr(i))
    return valid_keys
