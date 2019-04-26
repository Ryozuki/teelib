def str_utf8_isspace(code: int):
    return not (code > 0x20 and code != 0xA0 and code != 0x034F and code != 0x2800 and
                (code < 0x2000 or code > 0x200F) and (code < 0x2028 or code > 0x202F) and
                (code < 0x205F or code > 0x2064) and (code < 0x206A or code > 0x206F) and
                (code < 0xFE00 or code > 0xFE0F) and code != 0xFEFF and
                (code < 0xFFF9 or code > 0xFFFC))


def str_sanitize(string: str):
    new_str = ""
    for x in string:
        if ord(x) < 32 or ord(x) > 255 or x in "\n\t\r":
            new_str += " "
        new_str += x
    return new_str


def str_sanitize_cc(string: str):
    new_str = ""
    for x in string:
        if ord(x) < 32:
            new_str += " "
        new_str += x
    return new_str


def str_utf8_skip_whitespaces(string: str):
    return string.rstrip()
