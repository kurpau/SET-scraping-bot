import unittest
from src import main


class TestEPSExtraction(unittest.TestCase):

    def setUp(self):
        self.parser = main.Main()  # Replace 'YourClassName' with the name of the class that contains `getEPS`

    def test_positive_eps_values(self):
        data = """... EPS (baht) 1.02 0.77 2.76 ... Remark ..."""  # Shortened for clarity
        self.assertEqual(self.parser.getEPS(data), [1.02, 0.77, 2.76])

    def test_negative_eps_values(self):
        data = """... EPS (baht) (1.02) 0.77 (2.76) ... Remark ..."""
        self.assertEqual(self.parser.getEPS(data), [-1.02, 0.77, -2.76])

    def test_no_eps_values(self):
        data = """... EPS (baht) ... Remark ..."""
        self.assertIsNone(self.parser.getEPS(data))

    def test_invalid_data(self):
        data = """... EPS (baht ... Remark ..."""
        self.assertIsNone(self.parser.getEPS(data))


if __name__ == '__main__':
    unittest.main()
