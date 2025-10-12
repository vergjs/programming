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