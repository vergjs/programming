import unittest
from src.lab2.rsa import is_prime, gcd, multiplicative_inverse, generate_keypair, encrypt, decrypt

class RSATest(unittest.TestCase):
    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(11))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(0))

    def test_gcd(self):
        self.assertEqual(gcd(12, 15), 3)
        self.assertEqual(gcd(3, 7), 1)
        self.assertEqual(gcd(100, 10), 10)

    def test_multiplicative_inverse(self):
        self.assertEqual(multiplicative_inverse(7, 40), 23)

    def test_generate_keypair_and_encrypt_decrypt(self):
        p, q = 17, 23
        public, private = generate_keypair(p, q)

        message = "hello"
        encrypted = encrypt(public, message)
        decrypted = decrypt(private, encrypted)

        self.assertEqual(decrypted, message)

    def test_invalid_primes(self):
        with self.assertRaises(ValueError):
            generate_keypair(4, 9)
        with self.assertRaises(ValueError):
            generate_keypair(7, 7)


if __name__ == "__main__":
    unittest.main()