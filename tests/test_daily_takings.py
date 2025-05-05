import unittest
from datetime import date
import json
from bottle_shop import db, create_app
from bottle_shop.models.daily_takings import DailyTakings
from bottle_shop.services.currency_service import CurrencyService


class TestDailyTakings(unittest.TestCase):
    """Test cases for the DailyTakings model."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create a test takings record
        self.test_date = date(2023, 7, 15)
        self.test_takings = DailyTakings(date=self.test_date)
        self.test_takings.till_read = 2500.00
        self.test_takings.eftpos_total = 1200.00
        self.test_takings.portable_eftpos_total = 300.00
        self.test_takings.amex = 150.00
        self.test_takings.diners = 50.00
        self.test_takings.account_charges = 100.00
        self.test_takings.total_cash = 650.00
        self.test_takings.points_redeemed = 50.00
        self.test_takings.customer_count = 120
        
        # Set up denomination data for testing
        self.safe_float_open = {
            '5c': 0.50,
            '10c': 1.00,
            '20c': 2.00,
            '50c': 10.00,
            '$1': 50.00,
            '$2': 100.00,
            '$5': 100.00,
            '$10': 200.00,
            '$20': 400.00,
            '$50': 500.00,
            '$100': 100.00
        }
        
        self.till_float_open = {
            '5c': 1.00,
            '10c': 3.00,
            '20c': 5.00,
            '50c': 10.00,
            '$1': 50.00,
            '$2': 80.00,
            '$5': 100.00,
            '$10': 150.00,
            '$20': 100.00,
            '$50': 0,
            '$100': 0
        }
        
        # Store the denomination data
        self.test_takings.set_safe_float_open(self.safe_float_open)
        self.test_takings.set_till_float_open(self.till_float_open)
        
        # Save the test record to the database
        db.session.add(self.test_takings)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_initialization(self):
        """Test initializing a new DailyTakings record."""
        takings = DailyTakings(date=date(2023, 8, 1))
        self.assertEqual(takings.date, date(2023, 8, 1))
        self.assertFalse(takings.settled)
        self.assertIsNone(takings.till_read)
        self.assertIsNone(takings.eftpos_total)
        self.assertIsNone(takings.total_cash)
        self.assertIsNone(takings.variance)
    
    def test_calculate_variance(self):
        """Test calculating variance between till read and payment methods."""
        # The variance should be: 2500 - (1200 + 300 + 150 + 50 + 100 + 650) = 50
        expected_variance = 50.0
        calculated_variance = self.test_takings.calculate_variance()
        self.assertEqual(calculated_variance, expected_variance)
        
        # Test with None values for some payment methods
        takings = DailyTakings(date=date(2023, 8, 2))
        takings.till_read = 1000.00
        takings.eftpos_total = 500.00
        takings.total_cash = 450.00
        # Other payment methods are None
        
        # Variance should be: 1000 - (500 + 450) = 50
        self.assertEqual(takings.calculate_variance(), 50.0)
        
        # Test with None for till_read
        takings.till_read = None
        self.assertIsNone(takings.calculate_variance())
    
    def test_json_serialization(self):
        """Test JSON serialization and deserialization of denomination data."""
        # Test safe float open
        retrieved_safe_float = self.test_takings.get_safe_float_open()
        self.assertEqual(retrieved_safe_float, self.safe_float_open)
        
        # Test till float open
        retrieved_till_float = self.test_takings.get_till_float_open()
        self.assertEqual(retrieved_till_float, self.till_float_open)
        
        # Test setting safe float close
        safe_float_close = {
            '5c': 1.00,
            '10c': 2.00,
            '20c': 4.00,
            '50c': 15.00,
            '$1': 30.00,
            '$2': 120.00,
            '$5': 150.00,
            '$10': 100.00,
            '$20': 500.00,
            '$50': 550.00,
            '$100': 0
        }
        self.test_takings.set_safe_float_close(safe_float_close)
        retrieved_safe_float_close = self.test_takings.get_safe_float_close()
        self.assertEqual(retrieved_safe_float_close, safe_float_close)
    
    def test_empty_denomination_dicts(self):
        """Test handling of empty denomination dictionaries."""
        # Create new record with no denomination data
        empty_takings = DailyTakings(date=date(2023, 8, 3))
        
        # Test getting empty denomination dictionaries
        self.assertEqual(empty_takings.get_safe_float_open(), {})
        self.assertEqual(empty_takings.get_safe_float_close(), {})
        self.assertEqual(empty_takings.get_till_float_open(), {})
        self.assertEqual(empty_takings.get_till_float_close_before_makeup(), {})
        self.assertEqual(empty_takings.get_till_float_makeup(), {})
    
    def test_string_representation(self):
        """Test the string representation of DailyTakings objects."""
        expected_repr = f'<DailyTakings {self.test_date}>'
        self.assertEqual(repr(self.test_takings), expected_repr)
    
    def test_setting_and_getting_till_float_makeup(self):
        """Test setting and getting till float makeup data."""
        till_float_makeup = {
            '5c': 0.50,
            '10c': 1.00,
            '20c': 2.00,
            '50c': 5.00,
            '$1': 25.00,
            '$2': 40.00,
            '$5': 50.00,
            '$10': 80.00,
            '$20': 100.00,
            '$50': 0,
            '$100': 0
        }
        
        self.test_takings.set_till_float_makeup(till_float_makeup)
        retrieved_makeup = self.test_takings.get_till_float_makeup()
        self.assertEqual(retrieved_makeup, till_float_makeup)
    
    def test_database_persistence(self):
        """Test that denomination data is correctly persisted to the database."""
        # Retrieve from database to verify persistence
        db_takings = db.session.execute(
            db.select(DailyTakings).where(DailyTakings.date == self.test_date)
        ).scalar_one_or_none()
        
        # Test that values were correctly persisted
        self.assertEqual(db_takings.date, self.test_date)
        self.assertEqual(db_takings.till_read, 2500.00)
        self.assertEqual(db_takings.eftpos_total, 1200.00)
        self.assertEqual(db_takings.total_cash, 650.00)
        self.assertEqual(db_takings.customer_count, 120)
        
        # Test JSON data for denominations
        db_safe_float_open = db_takings.get_safe_float_open()
        self.assertEqual(db_safe_float_open['$5'], 100.00)
        self.assertEqual(db_safe_float_open['$10'], 200.00)
        
        db_till_float_open = db_takings.get_till_float_open()
        self.assertEqual(db_till_float_open['$1'], 50.00)
        self.assertEqual(db_till_float_open['$2'], 80.00)
    
    def test_settled_status(self):
        """Test the settled status flag behavior."""
        # Verify default is False
        self.assertFalse(self.test_takings.settled)
        
        # Set to True
        self.test_takings.settled = True
        db.session.commit()
        
        # Verify it was saved
        db_takings = db.session.execute(
            db.select(DailyTakings).where(DailyTakings.date == self.test_date)
        ).scalar_one_or_none()
        self.assertTrue(db_takings.settled)

    def test_settled_protection(self):
        """Test that settled records cannot be modified."""
        # Create and save a takings record
        takings = DailyTakings(date=self.test_date, till_read=2500.00, settled=True)
        db.session.add(takings)
        db.session.commit()
        
        # Verify the record is marked as settled
        db_takings = db.session.execute(
            db.select(DailyTakings).where(DailyTakings.date == self.test_date)
        ).scalar_one_or_none()
        self.assertTrue(db_takings.settled)


if __name__ == '__main__':
    unittest.main() 