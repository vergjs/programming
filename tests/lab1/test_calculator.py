import unittest
from src.lab1.calculator import calculate

class CalculatorTestCase(unittest.TestCase):

    def test_one(self):
        self.assertEqual(calculate("2+2"), 4)

    def test_two(self):
        self.assertEqual(calculate("10-5"), 5)

    def test_three(self):
        self.assertEqual(calculate("3*4"), 12)

    def test_four(self):
        self.assertEqual(calculate("8/2"), 4)

    def test_five(self):
        self.assertEqual(calculate("5/0"), "Ошибка: деление на ноль!")

    def test_six(self):
        self.assertEqual(calculate("2^2"), "Ошибка: операция не распознана!")

    def test_seven(self):
        self.assertEqual(calculate("5"), "Ошибка: операция не распознана!")


if __name__ == "__main__":
    unittest.main()


