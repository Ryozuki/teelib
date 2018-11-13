def get_int(buf, endian='little', signed=True, num_bytes=4):
    return int.from_bytes(buf[:num_bytes], endian, signed=signed)
