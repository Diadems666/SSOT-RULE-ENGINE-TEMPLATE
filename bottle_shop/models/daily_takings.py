from datetime import date
import json
from bottle_shop import db

class DailyTakings(db.Model):
    """
    Model representing the daily takings records for the bottle shop.
    
    This model stores all financial data for a single day's operation,
    including all payment methods, safe and till float details, and
    reconciliation information. It is the primary data structure for the
    end-of-trade reconciliation process.
    
    The safe float should maintain a target value of $1,500 and the till float
    should maintain a target value of $500. Denomination counts for both floats
    are stored as JSON strings to allow flexibility in recording various
    denominations of Australian currency.
    
    The settled flag indicates whether the day's records have been finalized
    and should not be modified further without special permissions.
    """
    
    __tablename__ = 'daily_takings'
    
    # Primary key - date of the takings record
    date = db.Column(db.Date, primary_key=True, default=date.today)
    
    # Daily totals from POS and payment methods
    till_read = db.Column(db.Float, nullable=True)  # Total from point-of-sale system
    eftpos_total = db.Column(db.Float, nullable=True)  # Fixed EFTPOS terminal
    portable_eftpos_total = db.Column(db.Float, nullable=True)  # Portable EFTPOS devices
    amex = db.Column(db.Float, nullable=True)  # American Express transactions
    diners = db.Column(db.Float, nullable=True)  # Diners Club transactions
    account_charges = db.Column(db.Float, nullable=True)  # Charges to customer accounts
    total_cash = db.Column(db.Float, nullable=True)  # Total cash takings
    points_redeemed = db.Column(db.Float, nullable=True)  # Loyalty points redeemed
    customer_count = db.Column(db.Integer, nullable=True)  # Number of customers served
    
    # Safe float data (stored as JSON strings for denomination counts)
    safe_float_open = db.Column(db.Text, nullable=True)  # JSON string with opening counts
    safe_float_close = db.Column(db.Text, nullable=True)  # JSON string with closing counts
    
    # Till float data (stored as JSON strings for denomination counts)
    till_float_open = db.Column(db.Text, nullable=True)  # JSON string with opening counts
    till_float_close_before_makeup = db.Column(db.Text, nullable=True)  # Counts before makeup to $500
    till_float_makeup = db.Column(db.Text, nullable=True)  # Counts used for makeup to $500
    
    # Calculated variance
    variance = db.Column(db.Float, nullable=True)  # Difference between till read and payment methods
    
    # Settled status (whether daily takings have been finalized)
    settled = db.Column(db.Boolean, default=False)  # True if records are finalized
    
    def __repr__(self):
        """String representation of the DailyTakings object."""
        return f'<DailyTakings {self.date}>'
    
    # Helper methods for handling denomination JSON
    def get_safe_float_open(self):
        """
        Get the safe float opening balances as a dictionary.
        
        Returns:
            dict: Dictionary mapping denomination names to counts,
                 or empty dict if no data is available
        """
        if self.safe_float_open:
            return json.loads(self.safe_float_open)
        return {}
    
    def set_safe_float_open(self, data):
        """
        Set the safe float opening balances from a dictionary.
        
        Args:
            data (dict): Dictionary mapping denomination names to counts
        """
        self.safe_float_open = json.dumps(data)
    
    def get_safe_float_close(self):
        """
        Get the safe float closing balances as a dictionary.
        
        Returns:
            dict: Dictionary mapping denomination names to counts,
                 or empty dict if no data is available
        """
        if self.safe_float_close:
            return json.loads(self.safe_float_close)
        return {}
    
    def set_safe_float_close(self, data):
        """
        Set the safe float closing balances from a dictionary.
        
        Args:
            data (dict): Dictionary mapping denomination names to counts
        """
        self.safe_float_close = json.dumps(data)
    
    def get_till_float_open(self):
        """
        Get the till float opening balances as a dictionary.
        
        Returns:
            dict: Dictionary mapping denomination names to counts,
                 or empty dict if no data is available
        """
        if self.till_float_open:
            return json.loads(self.till_float_open)
        return {}
    
    def set_till_float_open(self, data):
        """
        Set the till float opening balances from a dictionary.
        
        Args:
            data (dict): Dictionary mapping denomination names to counts
        """
        self.till_float_open = json.dumps(data)
    
    def get_till_float_close_before_makeup(self):
        """
        Get the till float closing balances (before makeup) as a dictionary.
        
        These represent the denomination counts in the till at the end of
        trading, before making up the float to the target value of $500.
        
        Returns:
            dict: Dictionary mapping denomination names to counts,
                 or empty dict if no data is available
        """
        if self.till_float_close_before_makeup:
            return json.loads(self.till_float_close_before_makeup)
        return {}
    
    def set_till_float_close_before_makeup(self, data):
        """
        Set the till float closing balances (before makeup) from a dictionary.
        
        Args:
            data (dict): Dictionary mapping denomination names to counts
        """
        self.till_float_close_before_makeup = json.dumps(data)
    
    def get_till_float_makeup(self):
        """
        Get the till float makeup balances as a dictionary.
        
        These represent the denomination counts used to make up the till float
        to the target value of $500 after trading.
        
        Returns:
            dict: Dictionary mapping denomination names to counts,
                 or empty dict if no data is available
        """
        if self.till_float_makeup:
            return json.loads(self.till_float_makeup)
        return {}
    
    def set_till_float_makeup(self, data):
        """
        Set the till float makeup balances from a dictionary.
        
        Args:
            data (dict): Dictionary mapping denomination names to counts
        """
        self.till_float_makeup = json.dumps(data)
    
    def calculate_variance(self):
        """
        Calculate the variance between till read and payment methods.
        
        The variance is the difference between the till read (from the POS system)
        and the sum of all payment methods. A positive variance indicates
        more money in the till than recorded in payment methods, while a
        negative variance indicates a shortage.
        
        Returns:
            float or None: The calculated variance, or None if till_read is None
        """
        if self.till_read is None:
            return None
        
        # Sum all payment methods
        payment_methods_sum = 0
        for value in [self.eftpos_total, self.portable_eftpos_total, 
                     self.amex, self.diners, self.account_charges, 
                     self.total_cash]:
            if value is not None:
                payment_methods_sum += value
        
        # Calculate variance
        return self.till_read - payment_methods_sum 