"""
Variable integer compression.
"""


def compress(num: int) -> bytes:
    sign = num < 0
    out = bytearray(1)

    if sign:
        # Swap all bits.
        num = ~num
        # Set sign bit
        out[0] = 0b1000000

    # Pack 6 bits
    out[0] |= num & 0b111111
    num >>= 6

    if num != 0:
        out[0] = 0b10000000  # Set extend bit

    byte_index = 1
    while num != 0:
        byte_index += 1
        current = 0
        if byte_index == 5:
            # Last byte has a zeroed 4 bit padding.
            current |= num & 0b00001111
            num >>= 4
        else:
            current |= num & 0b10000000  # Extend bit
            current |= num & 0b01111111  # Actual bits
            num >>= 7
        out.append(current)
    return out


def decompress(buf: bytes) -> int:
    pass
