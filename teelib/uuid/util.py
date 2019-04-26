import hashlib
from teelib.network.constants import NETMSG_WHATIS, NETMSG_ITIS, NETMSG_IDONTKNOW, NETMSG_RCONTYPE, \
    NETMSG_MAP_DETAILS, NETMSG_TIME_SCORE

TEEWORLDS_NAMESPACE = bytearray([
    0xe0, 0x5d, 0xda, 0xaa, 0xc4, 0xe6, 0x4c, 0xfb,
    0xb6, 0x42, 0x5d, 0x48, 0xe8, 0x0c, 0x00, 0x29
])


def calculate_uuid(name: str):
    m = hashlib.md5()
    m.update(TEEWORLDS_NAMESPACE)
    m.update(name.encode())
    digest = bytearray(m.digest())

    digest[6] &= 0x0f
    digest[6] |= 0x30
    digest[8] &= 0x3f
    digest[8] &= 0x80
    return digest


def get_uuid(ID: int):
    if ID == NETMSG_WHATIS:
        return calculate_uuid("what-is@ddnet.tw")
    elif ID == NETMSG_ITIS:
        return calculate_uuid("it-is@ddnet.tw")
    elif ID == NETMSG_IDONTKNOW:
        return calculate_uuid("i-dont-know@ddnet.tw")
    elif ID == NETMSG_RCONTYPE:
        return calculate_uuid("rcon-type@ddnet.tw")
    elif ID == NETMSG_MAP_DETAILS:
        return calculate_uuid("map-details@ddnet.tw")
    elif ID == NETMSG_TIME_SCORE:
        return calculate_uuid("time-score@ddnet.tw")


def pretty_uuid(hex_str: str):
    hex_str = hex_str.upper()
    return hex_str[0:8] + "-" + hex_str[8:12] + "-" + hex_str[12:16] + "-" + hex_str[16:20] + "-" + hex_str[20:32]
