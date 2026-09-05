import sys
import unittest

sys.path.insert(0, "src")

from arc_inspector import is_valid_address


class TestAddressValidation(unittest.TestCase):

    def test_valid_address(self):
        address = "0x0000000000000000000000000000000000000001"
        self.assertTrue(is_valid_address(address))

    def test_invalid_short_address(self):
        address = "0x1234"
        self.assertFalse(is_valid_address(address))

    def test_invalid_characters(self):
        address = "0xZZ00000000000000000000000000000000000000"
        self.assertFalse(is_valid_address(address))

    def test_missing_prefix(self):
        address = "0000000000000000000000000000000000000001"
        self.assertFalse(is_valid_address(address))


if __name__ == "__main__":
    unittest.main()