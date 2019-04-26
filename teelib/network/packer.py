from teelib.compression import compress, decompress
from .constants import PACKER_BUFFER_SIZE, SANITIZE, SANITIZE_CC, SKIP_START_WHITESPACES
from teelib.base.system import str_sanitize, str_sanitize_cc, str_utf8_skip_whitespaces


class Packer:
    def __init__(self):
        self.buffer = bytearray()
        self.error = False

    def _check_error(self):
        if len(self.buffer) > PACKER_BUFFER_SIZE:
            self.error = True

    def reset(self):
        self.buffer = bytearray()
        self.error = False

    def add_int(self, num: int):
        compressed = compress(num)
        self.buffer += compressed

        self._check_error()

    def add_str(self, string: str, limit=0):
        if limit > 0:
            if limit > len(string):
                limit = len(string)
        else:
            limit = len(string)

        self.buffer += string[0:limit].encode()
        self.buffer.append(0)

        self._check_error()

    def add_raw(self, raw: bytearray):
        self.buffer += raw

        self._check_error()


class Unpacker:
    def __init__(self, data: bytearray):
        self.buffer = data
        self.error = False
        self.index = 0

    def _check_error(self):
        if len(self.buffer) > PACKER_BUFFER_SIZE:
            self.error = True

    def reset(self, data: bytearray):
        self.buffer = data
        self.error = False
        self.index = 0

    def get_int(self):
        num, self.index = decompress(self.buffer[self.index:])
        return num

    def get_str(self, sanitize_type: int):
        length = 0
        for x in range(self.index, len(self.buffer)):
            if self.buffer[x] == 0:
                break
            length += 1
        string = self.buffer[self.index:self.index + length].decode()
        # Remember null char at end of str.
        self.index += length + 1
        if sanitize_type & SANITIZE:
            return str_sanitize(string)
        elif sanitize_type & SANITIZE_CC:
            return str_sanitize_cc(string)
        elif sanitize_type & SKIP_START_WHITESPACES:
            return str_utf8_skip_whitespaces(string)
        return string

    def get_raw(self, size: int):
        raw = self.buffer[self.index:self.index + size]
        self.index += size
        return raw
