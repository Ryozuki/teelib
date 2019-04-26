import unittest
from .util import get_uuid, calculate_uuid, pretty_uuid
from teelib.network.constants import NETMSG_RCONTYPE


class UuidUtilTestCase(unittest.TestCase):
    def test_util(self):
        self.assertEqual(b'\xd1\x05\x95\x14\x19^4o\x00\x85\xa3[\x08\xa4\xe7i', calculate_uuid("test"))
        self.assertEqual('12810e1fa1db337800fb164ed6505926', get_uuid(NETMSG_RCONTYPE).hex())
        self.assertEqual('12810E1F-A1DB-3378-00FB-164ED6505926', pretty_uuid('12810e1fa1db337800fb164ed6505926'))


if __name__ == '__main__':
    unittest.main()
