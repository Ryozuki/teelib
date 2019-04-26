import unittest
from .packer import Packer, Unpacker


class PackerTestCase(unittest.TestCase):
    def test_packer(self):
        packer = Packer()
        packer.add_int(64)
        packer.add_str("hello world!")
        packer.add_raw(bytearray([2, 7, 9, 2, 4]))

        print(packer.buffer)
        unpacker = Unpacker(packer.buffer)

        self.assertEqual(64, unpacker.get_int())
        self.assertEqual("hello world!", unpacker.get_str(0))
        self.assertEqual(bytearray([2, 7, 9, 2, 4]), unpacker.get_raw(5))


if __name__ == '__main__':
    unittest.main()
