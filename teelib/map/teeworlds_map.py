from .version_header import VersionHeader
from .header import Header
from .items import InfoItem, VersionItem


class TeeworldsMap:
    def __init__(self, version_header: VersionHeader, header: Header,
                 version_item: VersionItem, info_item: InfoItem):
        self.version_header = version_header
        self.header = header
        self.version = version_item.version
        self.map_info = info_item
