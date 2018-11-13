from .util import get_int
from typing import List

MAPITEMTYPE_VERSION = 0
MAPITEMTYPE_INFO = 1
MAPITEMTYPE_IMAGE = 2
MAPITEMTYPE_ENVELOPE = 3
MAPITEMTYPE_GROUP = 4
MAPITEMTYPE_LAYER = 5
MAPITEMTYPE_ENVPOINTS = 6
MAPITEMTYPE_SOUND = 7


class VersionItem:
    def __init__(self, buffer: bytearray):
        self.version = get_int(buffer)


class InfoItem:
    def __init__(self, buffer: bytearray, data: List[bytes]):
        self.version = get_int(buffer)
        self.author = data[get_int(buffer[4:])][:-1] if get_int(buffer[4:]) > -1 else None
        self.map_version = data[get_int(buffer[4*2:])][:-1] if get_int(buffer[4*2:]) > -1 else None
        self.credits = data[get_int(buffer[4*3:])][:-1] if get_int(buffer[4*3:]) > -1 else None
        self.license = data[get_int(buffer[4*4:])][:-1] if get_int(buffer[4*4:]) > -1 else None
        self.settings: List[str] = []

        settings = get_int(buffer[4*5:])

        if settings > -1:
            self.settings = [x.decode() for x in filter(None, data[settings].split(b'\0'))]
