"""
Variable integer compression.
"""

from typing import Tuple


def compress(num: int) -> bytearray:
    """
    Compresses a integer into a variable integer inside a bytearray.

    :param num: The integer to compress.
    :return: A bytearray containing the variable integer.
    """
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


def decompress(buf: bytearray) -> Tuple[int, int]:
    """
    Decompresses a single variable int from a buffer.

    :param buf: The buffer sliced so that index 0 is the start of the variable int.
    :return: The integer and the length in the bytearray
    """
    index = 0
    sign = (buf[index] >> 6) & 1
    extended = (buf[index] >> 7) == 1
    out = buf[index] & 0b00111111
    while extended:
        index += 1
        if index > 4:
            break
        extended = (buf[index] >> 7) == 1
        out |= (buf[index] & 0b01111111) << (6 + 7 * (index - 1))

    out ^= - sign
    return out, index + 1
