from .util import get_int


class Item:
    def __init__(self, buffer: bytearray):
        itemtype = get_int(buffer)
        self.size = get_int(buffer[4:])
        self.item_data = get_int(buffer[8:8 + self.size])
        # type_id might not be accurate, TODO: make uuid
        # datafile.cppL445
        self.type_id = (itemtype >> 16) & 0xffff
        self.id = itemtype & 0xffff

    def _get_size(self):
        """
        Used internally to know the next index.

        :return: The index of the next object in the buffer
        """
        return 4 + 4 + self.size


class ItemType:
    def __init__(self, buffer: bytearray):
        self.type_id = get_int(buffer)
        self.start = get_int(buffer[4:])
        self.num = get_int(buffer[8:])
