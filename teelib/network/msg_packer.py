from .packer import Packer
from .constants import OFFSET_UUID
from teelib.uuid.util import get_uuid


class MsgPacker(Packer):
    def __init__(self, packet_type: int):
        super().__init__()
        if packet_type < OFFSET_UUID:
            self.add_int(packet_type)
        else:
            self.add_int(0)  # NETMSG_EX, NETMSGTYPE_EX
            self.add_raw(get_uuid(packet_type))
