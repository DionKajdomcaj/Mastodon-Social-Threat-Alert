import calc


class TestCalculator:
    def test_addition(self):
        assert 4 == calc.add(2, 2)

    def test_subtraction(self):
        assert 2 == calc.subtract(4, 2)
        
    def test_multiplication(self):
        assert 100 == calc.multiply(10, 10)