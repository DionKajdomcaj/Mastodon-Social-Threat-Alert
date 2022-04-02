"""
Unit tests for the calculator library
"""
#We add all the files in the app directory so that they can be found
##from sys import path
##from database import calculator

from database import calculator

class TestCalculator:

    def test_addition(self):
        assert 4 == calculator.add(2, 2)

    def test_subtraction(self):
        assert 2 == calculator.subtract(4, 2)

    def test_multiplication(self):
        assert 100 == calculator.multiply(10, 10)