from Crypto.Util.number import bytes_to_long
from fastecdsa.curve import P224
from help import random_mpz

p = 2**224 - 2**96 + 1

class PedersenEC:
    def __init__(self):
        self.G = P224.G
        q = int(random_mpz(P224.p))
        self.H = q * self.G

    def commit(self, m):
        G = self.G
        H = self.H
        r = int(random_mpz(P224.p))
        c = r * H + m * G
        return c, r
        pass

    def open(self, m, c, r):
        G = self.G
        H = self.H
        r = int(r)
        m = int(m)
        # print(c)
        # print(r)
        return c == r * H + m * G
        pass

def test():
    pedersenec = PedersenEC()
    m1 = bytes_to_long("atfwus21097391837681647182177111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111".encode())
    m2 = bytes_to_long("oooaqq21097391837681647182177111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111".encode())
    m3 = bytes_to_long("oooaqq2109739183768164718217711111213131111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111".encode())
    c1, r1 = pedersenec.commit(m1)
    c2, r2 = pedersenec.commit(m2)
    c3, r3 = pedersenec.commit(m3)
    ui = 21097391837681647182177111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
    m = m1 + ui * m2 + ui**2 * m3
    r = r1 + ui * r2 + ui**2 * r3
    c = c1 + ui * c2 + ui**2 * c3
    print(pedersenec.open(m, c, r))

if __name__ == "__main__":
    test()