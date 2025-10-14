import unittest
from src.lab2.vigenre import encrypt_vigenere, decrypt_vigenere


class VigenereCipherTest(unittest.TestCase):

    def test_encrypt_simple(self):
        self.assertEqual(encrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(encrypt_vigenere("python", "a"), "python")

    def test_encrypt_lemon(self):
        self.assertEqual(encrypt_vigenere("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")

    def test_decrypt_simple(self):
        self.assertEqual(decrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(decrypt_vigenere("python", "a"), "python")

    def test_decrypt_lemon(self):
        self.assertEqual(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")

    def test_case_sensitivity(self):
        self.assertEqual(encrypt_vigenere("Python", "a"), "Python")
        self.assertEqual(decrypt_vigenere("Python", "a"), "Python")

if __name__ == "__main__":
    unittest.main()