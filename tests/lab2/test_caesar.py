import unittest
from src.lab2.caesar import encrypt_caesar, decrypt_caesar

class CaesarCipherTest(unittest.TestCase):

    def test_encrypt_basic_uppercase(self):
        self.assertEqual(encrypt_caesar("PYTHON"), "SBWKRQ")

    def test_encrypt_basic_lowercase(self):
        self.assertEqual(encrypt_caesar("python"), "sbwkrq")

    def test_encrypt_mixed(self):
        self.assertEqual(encrypt_caesar("Python3.6"), "Sbwkrq3.6")

    def test_encrypt_empty(self):
        self.assertEqual(encrypt_caesar(""), "")

    def test_decrypt_basic_uppercase(self):
        self.assertEqual(decrypt_caesar("SBWKRQ"), "PYTHON")

    def test_decrypt_basic_lowercase(self):
        self.assertEqual(decrypt_caesar("sbwkrq"), "python")

    def test_decrypt_mixed(self):
        self.assertEqual(decrypt_caesar("Sbwkrq3.6"), "Python3.6")

    def test_decrypt_empty(self):
        self.assertEqual(decrypt_caesar(""), "")

    def test_shift_zero(self):
        self.assertEqual(encrypt_caesar("Hello", shift=0), "Hello")
        self.assertEqual(decrypt_caesar("Hello", shift=0), "Hello")

    def test_custom_shift(self):
        self.assertEqual(encrypt_caesar("ABC", shift=1), "BCD")
        self.assertEqual(decrypt_caesar("BCD", shift=1), "ABC")


if __name__ == "__main__":
    unittest.main()