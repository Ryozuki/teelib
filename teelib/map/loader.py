from .version_header import VersionHeader
from .header import Header
from .teeworlds_map import TeeworldsMap
from .util import get_int
from .item import Item, ItemType
from typing import List
from .items import *
import zlib


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
        raise NotImplementedError("The map version is not compatible: {0}".format(version_header.version))

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

    # ------------------------
    # Load buffers.
    # ------------------------
    item_types_buf = data[current_index:current_index + 12 * header.num_item_types]
    current_index += 12 * header.num_item_types

    item_offsets_buf = data[current_index:current_index + 4 * header.num_items]
    current_index += 4 * header.num_items

    data_offsets_buf = data[current_index:current_index + 4 * header.num_data]
    current_index += 4 * header.num_data

    data_sizes_buf = bytearray()
    if version_header.version == 4:
        data_sizes_buf = data[current_index:current_index + 4 * header.num_data]
        current_index += 4 * header.num_data

    items_buffer = data[current_index:current_index + header.item_size]
    current_index += header.item_size

    data_buffer = data[current_index:current_index + header.data_size]
    current_index += header.data_size
    # ------------------------
    # End loading buffers.
    # ------------------------

    # ------------------------
    # Parse offsets and sizes.
    # ------------------------
    item_offsets: List[int] = []
    for x in range(header.num_items):
        item_offsets.append(get_int(item_offsets_buf[x * 4:]))

    data_offsets: List[int] = []
    for x in range(header.num_data):
        data_offsets.append(get_int(data_offsets_buf[x * 4:]))

    data_sizes: List[int] = []
    if version_header.version == 4:
        for x in range(header.num_data):
            data_sizes.append(get_int(data_sizes_buf[x * 4:]))
    # ------------------------
    # End parsing offsets and sizes.
    # ------------------------

    item_types: List[ItemType] = []
    for x in range(header.num_item_types):
        item_types.append(ItemType(item_types_buf[x * 12:]))

    assert len(item_types) == header.num_item_types, "Error parsing: Length of item_types is not " \
                                                     "equal to header.num_item_types"

    items: List[Item] = []
    for x in range(header.num_items):
        items.append(Item(items_buffer[item_offsets[x]:]))

    assert len(items) == header.num_items, "Error parsing: Length of items is not equal to header.num_items"

    map_data: List[bytes] = []
    for x in range(header.num_data):
        if len(data_offsets) >= x:
            buffer = data_buffer[data_offsets[x]:]
        else:
            buffer = data_buffer[data_offsets[x]:data_offsets[x] + data_offsets[x + 1]]

        if version_header.version == 4:
            result = zlib.decompress(buffer)
        else:
            result = bytes(buffer)
        map_data.append(result)

    if __debug__:
        for x in range(len(map_data)):
            assert len(map_data[x]) == data_sizes[x], "Data length not equal to data_sizes on index: {0}".format(x)

    def get_type(_type: int):
        for i in item_types:
            if i.type_id == _type:
                return i

    def find_item_index(_type: int, id: int):
        itemtype = get_type(_type)
        for i in range(itemtype.num):
            if items[itemtype.start + i].id == id:
                return itemtype.start + i

    def find_item(_type: int, id: int):
        index = find_item_index(_type, id)
        return items[index]

    # Load Version Item
    version_item = VersionItem(find_item(MAPITEMTYPE_VERSION, 0).item_data)

    # Load stuff
    map_info = None

    if version_item.version == 1:
        info_type = get_type(MAPITEMTYPE_INFO)
        for x in range(info_type.start, info_type.start + info_type.num):
            if items[x].id != 0:
                continue

            map_info = InfoItem(items[x].item_data, map_data)

    return TeeworldsMap(version_header, header, version_item, map_info)
