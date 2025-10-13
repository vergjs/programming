import unittest
from src.lab2.rsa import is_prime, gcd, multiplicative_inverse, generate_keypair

class RSATest(unittest.TestCase):
    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(11))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(0))