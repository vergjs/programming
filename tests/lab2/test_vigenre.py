import unittest
from src.lab2.vigenre import encrypt_vigenere, decrypt_vigenere


class VigenereCipherTest(unittest.TestCase):

    def test_encrypt_simple(self):
        self.assertEqual(encrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(encrypt_vigenere("python", "a"), "python")

    def test_encrypt_lemon(self):
        self.assertEqual(encrypt_vigenere("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")
