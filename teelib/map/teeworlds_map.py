from .version_header import VersionHeader
from .header import Header


class TeeworldsMap:
    def __init__(self, version_header: VersionHeader, header: Header):
        self.version_header = version_header
        self.header = header
