from paillier import Paillier
import gmpy2 as gy
import datetime
from help import H

class Proof(object):
    def __init__(self, pubKey=None, n_bits=256):
        self.pubKey = pubKey
        self.n_bits = n_bits
        self.zkp_pro = None
        self.random_m4_param = None
        self.a = None

    def setup(self, pk, c1, c2, c3, m1, m2, r1, r2, r3, n_bits=256):
        self.pubKey = pk
        self.n_bits = n_bits
        self.zkp_pro = [c1, c2, c3, m1, m2, r1, r2, r3]


    def random_m4(self):
        c1, c2, c3, m1, m2, r1, r2, r3 = self.zkp_pro
        m4 = gy.mpz_random(gy.random_state(datetime.datetime.now().microsecond), self.pubKey[0])

        pai = Paillier()
        pai.pubKey = self.pubKey
        n = self.pubKey[0]
        c4 = pai.encipher(m4)
        r4 = pai.r
        pai.r = None

        c24 = pai.encipher(m2 * m4 % n)
        r24 = pai.r
        pai.r = None

        self.random_m4_param = [c4, m4, r4, c24, r24]
        return c4, c24

    # def set_random_a(self, a):
    #     self.a = a

    def verify(self):
        n_2q = self.pubKey[0] ** 2
        c1, c2, c3, m1, m2, r1, r2, r3 = self.zkp_pro
        c4, m4, r4, c24, r24 = self.random_m4_param
        #a = self.a
        a = H(c2, c24, c1, c3)

        b = a * m1 + m4
        #print("b", b)
        z1 = pow(r1, a, n_2q) * r4 % n_2q
        #print("z1", z1)
        r243a = r24 * pow(r3, a, n_2q) % n_2q
        z2 = pow(r2, b, n_2q) * gy.invert(r243a, n_2q) % n_2q
        #print("z2", z2)
        c24c3a = pow(c3, a, n_2q) * c24 % n_2q

        pai = Paillier()
        pai.pubKey = self.pubKey
        pai.r = pow(r1, a, n_2q) * r4 % n_2q
        if pow(c1, a, n_2q) * c4 % n_2q != pai.encipher(a * m1 + m4):
            return False
        pai.r = z2
        return pow(c2, b, n_2q) * gy.invert(c24c3a, n_2q) % n_2q == pai.encipher(0)

def test():
    pai = Paillier()
    pai.__key_gen__(n_bits=256)
    pk = pai.pubKey
    m1 = 520
    m2 = 1314
    c1 = pai.encipher(m1)
    r1 = pai.r
    pai.r = None
    c2 = pai.encipher(m2)
    r2 = pai.r
    pai.r = None
    c3 = pai.encipher(m1 * m2)
    r3 = pai.r

    proof = Proof()
    proof.setup(pk, c1, c2, c3, m1, m2, r1, r2, r3)

    c4, c24 = proof.random_m4()
    print("c4", c4)
    print("c24", c24)

    #a = proof.set_random_a(13214)

    print(proof.verify())

if __name__ == "__main__":
    test()




