import gmpy2 as gy
import random
import time
import libnum
import datetime


class Paillier(object):
    def __init__(self, pubKey=None, priKey=None, r = None, n_bits=256):
        self.pubKey = pubKey
        self.priKey = priKey
        self.r = r
        self.n_bits = n_bits

    def __gen_prime__(self, rs, n_bits):
        p = gy.mpz_urandomb(rs, n_bits)
        while not gy.is_prime(p):
            p += 1
        return p

    def __L__(self, x, n):
        return (x - 1) // n

    def __key_gen__(self, n_bits=256):
        self.n_bits = n_bits
        while True:
            rs = gy.random_state(int(time.time()))
            p = self.__gen_prime__(rs, n_bits)
            q = self.__gen_prime__(rs, n_bits)
            n = p * q
            lmd = (p - 1) * (q - 1)
            if gy.gcd(n, lmd) == 1:
                break

        g = n + 1
        mu = gy.invert(lmd, n)
        self.pubKey = [n, g]
        self.priKey = [lmd, mu]
        return

    def decipher(self, ciphertext):
        n, g = self.pubKey
        lmd, mu = self.priKey
        m = self.__L__(gy.powmod(ciphertext, lmd, n ** 2), n) * mu % n
        return m

    def encipher(self, plaintext):
        m = plaintext
        n, g = self.pubKey
        if self.r is None:
            # r = gy.mpz_random(gy.random_state(int(time.time())), n)
            r = gy.mpz_random(gy.random_state(datetime.datetime.now().microsecond), n)
            while gy.gcd(n, r) != 1:
                r += 1
            self.r = r
        else:
            r = self.r
        ciphertext = gy.powmod(g, m, n ** 2) * gy.powmod(r, n, n ** 2) % (n ** 2)
        return ciphertext


if __name__ == "__main__":
    pai = Paillier()
    pai.__key_gen__()
    c = pai.encipher(2408914721985720503165136)
    print(c)
    m = pai.decipher(c)
    print(m)


