import unittest

from goodtypes.bytes import Bytes, Unit


class TestBytes(unittest.TestCase):

    def test_bytes(self):
        bs = Bytes("2344Ki")
        self.assertEqual("2344Ki", bs.format(Unit.KIBI_BYTES))
        self.assertEqual("2400256", bs.format(Unit.BYTES))
