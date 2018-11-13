from .version_header import VersionHeader
from .header import Header
from .teeworlds_map import TeeworldsMap
from .util import get_int
from .item import Item, ItemType


def load(path: str):
    with open(path, 'rb') as f:
        data = bytearray(f.read())

    version_header_buf = data[0:8]
    header_buf = data[8:8 + 28]

    version_header = VersionHeader(
        version_header_buf[0:4].decode(),
        get_int(version_header_buf[4:])
    )

    if not version_header.is_valid():
        raise ValueError("The map header is not valid.")

    if not (2 < version_header.version < 5):
        raise NotImplementedError("The map version is not complatible: {0}".format(version_header.version))

    header = Header(
        get_int(header_buf[0:]),
        get_int(header_buf[4:]),
        get_int(header_buf[4 * 2:]),
        get_int(header_buf[4 * 3:]),
        get_int(header_buf[4 * 4:]),
        get_int(header_buf[4 * 5:]),
        get_int(header_buf[4 * 6:])
    )

    current_index = 8 + 28

    # Load everything.
    item_types_buf = data[current_index:current_index + header.num_item_types]
    current_index += header.num_item_types

    item_offsets_buf = data[current_index:current_index + header.num_items]
    current_index += header.num_items

    data_offsets = data[current_index:current_index + header.num_data]
    current_index += header.num_data

    _data_sizes = None
    if version_header.version == 4:
        _data_sizes = data[current_index:current_index + header.num_data]
        current_index += header.num_items

    items_buffer = data[current_index:current_index + header.item_size]
    current_index += header.item_size

    data_buffer = data[current_index:current_index + header.data_size]
    current_index += header.data_size

    return TeeworldsMap(version_header, header)
