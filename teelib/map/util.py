def get_int(buf, endian='little', signed=True):
    return int.from_bytes(buf[:4], endian, signed=signed)
