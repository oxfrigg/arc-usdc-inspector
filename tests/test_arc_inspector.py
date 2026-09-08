import sys
import unittest

sys.path.insert(0, "src")

from arc_inspector import (
    build_balance_of_call,
    format_usdc,
    is_valid_address,
)


class TestAddressValidation(unittest.TestCase):

    def test_valid_address(self):
        address = "0x0000000000000000000000000000000000000001"
        self.assertTrue(is_valid_address(address))

    def test_invalid_short_address(self):
        self.assertFalse(is_valid_address("0x1234"))

    def test_invalid_characters(self):
        address = "0xZZ00000000000000000000000000000000000000"
        self.assertFalse(is_valid_address(address))

    def test_missing_prefix(self):
        address = "0000000000000000000000000000000000000001"
        self.assertFalse(is_valid_address(address))


class TestERC20Encoding(unittest.TestCase):

    def test_balance_of_call_selector(self):
        address = "0x0000000000000000000000000000000000000001"
        call_data = build_balance_of_call(address)

        self.assertTrue(call_data.startswith("0x70a08231"))
        self.assertEqual(len(call_data), 74)

    def test_balance_of_call_contains_address(self):
        address = "0x1234567890abcdef1234567890abcdef12345678"
        call_data = build_balance_of_call(address)

        self.assertTrue(
            call_data.endswith(
                "1234567890abcdef1234567890abcdef12345678"
            )
        )


class TestUSDCFormatting(unittest.TestCase):

    def test_format_usdc(self):
        self.assertEqual(
            format_usdc(12345678),
            "12.345678",
        )

    def test_format_zero(self):
        self.assertEqual(
            format_usdc(0),
            "0.000000",
        )


if __name__ == "__main__":
    unittest.main()