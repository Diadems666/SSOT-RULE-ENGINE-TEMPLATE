import unittest
from bottle_shop.services.currency_service import CurrencyService


class TestCurrencyService(unittest.TestCase):
    """Test cases for the CurrencyService class."""

    def test_all_denominations(self):
        """Test that all denominations are correctly defined."""
        # Test coin denominations
        self.assertEqual(CurrencyService.COIN_DENOMINATIONS['5c'], 0.05)
        self.assertEqual(CurrencyService.COIN_DENOMINATIONS['10c'], 0.10)
        self.assertEqual(CurrencyService.COIN_DENOMINATIONS['20c'], 0.20)
        self.assertEqual(CurrencyService.COIN_DENOMINATIONS['50c'], 0.50)
        self.assertEqual(CurrencyService.COIN_DENOMINATIONS['$1'], 1.00)
        self.assertEqual(CurrencyService.COIN_DENOMINATIONS['$2'], 2.00)
        
        # Test note denominations
        self.assertEqual(CurrencyService.NOTE_DENOMINATIONS['$5'], 5.00)
        self.assertEqual(CurrencyService.NOTE_DENOMINATIONS['$10'], 10.00)
        self.assertEqual(CurrencyService.NOTE_DENOMINATIONS['$20'], 20.00)
        self.assertEqual(CurrencyService.NOTE_DENOMINATIONS['$50'], 50.00)
        self.assertEqual(CurrencyService.NOTE_DENOMINATIONS['$100'], 100.00)
        
        # Test combined denominations
        self.assertEqual(len(CurrencyService.ALL_DENOMINATIONS), 11)
        for denom in CurrencyService.COIN_DENOMINATIONS:
            self.assertIn(denom, CurrencyService.ALL_DENOMINATIONS)
        for denom in CurrencyService.NOTE_DENOMINATIONS:
            self.assertIn(denom, CurrencyService.ALL_DENOMINATIONS)
            
        # Test denomination order
        expected_order = ['5c', '10c', '20c', '50c', '$1', '$2', '$5', '$10', '$20', '$50', '$100']
        self.assertEqual(CurrencyService.DENOMINATION_ORDER, expected_order)

    def test_create_empty_denomination_dict(self):
        """Test creating an empty denomination dictionary."""
        empty_dict = CurrencyService.create_empty_denomination_dict()
        
        # Verify all denominations are in the dictionary with value 0
        self.assertEqual(len(empty_dict), 11)
        for denom in CurrencyService.ALL_DENOMINATIONS:
            self.assertIn(denom, empty_dict)
            self.assertEqual(empty_dict[denom], 0)

    def test_calculate_total_value(self):
        """Test calculating total value from denomination counts."""
        # Test with a mix of denominations
        denominations = {
            '5c': 10,    # $0.50
            '10c': 20,   # $2.00
            '20c': 5,    # $1.00
            '50c': 6,    # $3.00
            '$1': 15,    # $15.00
            '$2': 8,     # $16.00
            '$5': 4,     # $20.00
            '$10': 3,    # $30.00
            '$20': 2,    # $40.00
            '$50': 1,    # $50.00
            '$100': 1    # $100.00
        }
        total = CurrencyService.calculate_total_value(denominations)
        expected_total = 0.50 + 2.00 + 1.00 + 3.00 + 15.00 + 16.00 + 20.00 + 30.00 + 40.00 + 50.00 + 100.00
        self.assertEqual(total, expected_total)
        
        # Test with empty dictionary
        self.assertEqual(CurrencyService.calculate_total_value({}), 0.0)
        
        # Test with None values
        denominations_with_none = {
            '5c': None,
            '$10': 5,
            '$50': None
        }
        self.assertEqual(CurrencyService.calculate_total_value(denominations_with_none), 50.0)
        
        # Test with invalid denominations
        invalid_denominations = {
            '5c': 10,
            '25c': 5,  # Invalid denomination
            '$10': 5
        }
        # Should ignore invalid denomination and only count valid ones
        self.assertEqual(CurrencyService.calculate_total_value(invalid_denominations), 0.5 + 50.0)

    def test_calculate_optimal_float_exact_match(self):
        """Test calculating optimal till float with exact match to target."""
        # Test case where we have exactly the right denominations for $500 float
        available_denominations = {
            '5c': 10,     # $0.50
            '10c': 15,    # $1.50
            '20c': 10,    # $2.00
            '50c': 20,    # $10.00
            '$1': 50,     # $50.00
            '$2': 40,     # $80.00
            '$5': 30,     # $150.00
            '$10': 10,    # $100.00
            '$20': 5,     # $100.00
            '$50': 10,    # $500.00 (should avoid using)
            '$100': 5     # $500.00 (should avoid using)
        }
        
        # Expected denominations used for float (should not use $50 and $100)
        expected_result = {
            '5c': 10,     # $0.50
            '10c': 15,    # $1.50
            '20c': 10,    # $2.00
            '50c': 20,    # $10.00
            '$1': 50,     # $50.00
            '$2': 40,     # $80.00
            '$5': 30,     # $150.00
            '$10': 10,    # $100.00
            '$20': 5,     # $100.00
            '$50': 1,     # $50.00 (using one $50 to get to exactly $500)
            '$100': 0     # $0.00 (should avoid using)
        }
        
        result = CurrencyService.calculate_optimal_float(available_denominations)
        
        # Verify result matches expected denominations
        self.assertEqual(result, expected_result)
        
        # Verify total value is exactly $500
        self.assertEqual(CurrencyService.calculate_total_value(result), 500.0)

    def test_calculate_optimal_float_insufficient_funds(self):
        """Test calculating optimal till float with insufficient funds."""
        # Test case where we don't have enough for $500 float
        available_denominations = {
            '5c': 10,     # $0.50
            '10c': 15,    # $1.50
            '20c': 10,    # $2.00
            '50c': 20,    # $10.00
            '$1': 50,     # $50.00
            '$2': 40,     # $80.00
            '$5': 20,     # $100.00
            '$10': 10,    # $100.00
            '$20': 5,     # $100.00
            '$50': 0,     # $0.00
            '$100': 0     # $0.00
        }
        # Total available is $444.00, which is less than $500 target
        
        result = CurrencyService.calculate_optimal_float(available_denominations)
        
        # Should return None as we can't make exact $500
        self.assertIsNone(result)

    def test_calculate_optimal_float_custom_target(self):
        """Test calculating optimal till float with custom target value."""
        # Test with custom target of $300
        available_denominations = {
            '5c': 10,     # $0.50
            '10c': 15,    # $1.50
            '20c': 10,    # $2.00
            '50c': 20,    # $10.00
            '$1': 50,     # $50.00
            '$2': 40,     # $80.00
            '$5': 20,     # $100.00
            '$10': 10,    # $100.00
            '$20': 5,     # $100.00
            '$50': 0,     # $0.00
            '$100': 0     # $0.00
        }
        
        result = CurrencyService.calculate_optimal_float(available_denominations, target_value=300.0)
        
        # Verify total value is exactly $300
        self.assertEqual(CurrencyService.calculate_total_value(result), 300.0)

    def test_format_currency(self):
        """Test formatting currency values."""
        # Test formatting various values
        self.assertEqual(CurrencyService.format_currency(0), "$0.00")
        self.assertEqual(CurrencyService.format_currency(1), "$1.00")
        self.assertEqual(CurrencyService.format_currency(10.5), "$10.50")
        self.assertEqual(CurrencyService.format_currency(100.25), "$100.25")
        self.assertEqual(CurrencyService.format_currency(1234.56), "$1234.56")
        
        # Test with None value
        self.assertEqual(CurrencyService.format_currency(None), "$0.00")


if __name__ == '__main__':
    unittest.main() 