#!/usr/bin/env python
"""
Test runner script for the Bottle Shop application.

This script sets up the Python path correctly to run the tests
and handles importing the necessary modules.
"""

import os
import sys
import unittest

# Add the parent directory to the Python path so 'bottle_shop' can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_tests():
    """Run all tests in the tests directory."""
    # Set environment variable for testing
    os.environ['FLASK_ENV'] = 'testing'
    
    # Discover and run all tests
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 