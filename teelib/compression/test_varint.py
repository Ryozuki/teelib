import unittest
from .varint import compress, decompress


class VariableIntTestCase(unittest.TestCase):
    def test_compression(self):
        self.assertEqual(bytearray([0b00000000]), compress(0))
        self.assertEqual(bytearray([0b10000000, 0b00000001]), compress(64))
        self.assertEqual(bytearray([0b01000000]), compress(-1))

    def test_decompression(self):
        self.assertEqual((64, 2), decompress(bytearray([0b10000000, 0b00000001])))
        self.assertEqual((-1, 1), decompress(bytearray([0b01000000])))
        self.assertEqual((0, 1), decompress(bytearray([0b00000000])))


if __name__ == '__main__':
    unittest.main()
