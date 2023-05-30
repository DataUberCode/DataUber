import gmpy2 as gy
import time
import datetime


class Paillier(object):
    def __init__(self, pubKey=None, priKey=None, r = None, n_bits=256):
        self.pubKey = pubKey
        self.priKey = priKey
        self.r = r
        self.n_bits = n_bits
        self.rn = None
        self.use_rn = False

    def __gen_prime__(self, rs, n_bits):
        p = gy.mpz_urandomb(rs, n_bits)
        while not gy.is_prime(p):
            p += 1
        return p

    def __L__(self, x, n):
        return (x - 1) // n

    def __key_gen__(self, n_bits=256):
        assert n_bits % 2 == 0
        self.n_bits = n_bits
        while True:
            rs = gy.random_state(int(time.time()))
            p = self.__gen_prime__(rs, n_bits // 2)
            q = self.__gen_prime__(rs, n_bits // 2)
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
        if m >= n:
            raise Exception("out of plaintext space")
        if self.r is None:
            # r = gy.mpz_random(gy.random_state(int(time.time())), n)
            r = gy.mpz_random(gy.random_state(datetime.datetime.now().microsecond), n)
            while gy.gcd(n, r) != 1:
                r += 1
            self.r = r
        else:
            r = self.r
        if self.rn is not None and self.use_rn:
            ciphertext = gy.powmod(g, m, n ** 2) * self.rn % (n ** 2)
        else:
            ciphertext = gy.powmod(g, m, n ** 2) * gy.powmod(r, n, n ** 2) % (n ** 2)
            self.rn = gy.powmod(r, n, n ** 2)
        return ciphertext

    def extract_rn(self, m ,c):
        n, g = self.pubKey
        n_2q = n ** 2

        rn = gy.invert(gy.powmod(g, m, n_2q), n_2q) * c % n_2q
        return rn



if __name__ == "__main__":
    pai = Paillier()
    pai.__key_gen__()
    m = 2408914721985720503165136
    c = pai.encipher(m)
    #print(c)
    r = pai.r

    rn = pai.extract_rn(m, c)
    print(rn == pai.rn)


