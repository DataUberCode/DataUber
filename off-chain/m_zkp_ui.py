from paillier_zkp import Proof
from paillier import Paillier
import datetime
import gmpy2 as gy

class MProof(object):
    def __init__(self):
        self.pubKey = None
        self.cu = None
        self.ru = None
        self.ui = None
        self.t = None
        self.n = None
        self.rv = None
        self.ruv = None
        self.cv = None
        self.cuv = None
        self.v = None

    def generate_param(self, pk, ui, t, n):
        cu = []
        ru = []
        pai = Paillier()
        pai.pubKey = pk
        for j in range(1, t):
            cu.append(pai.encipher(ui ** j))
            ru.append(pai.r)
            pai.r = None
        v = gy.mpz_random(gy.random_state(datetime.datetime.now().microsecond), n)
        while v == 0:
            v = gy.mpz_random(gy.random_state(datetime.datetime.now().microsecond), n)
        cv = pai.encipher(v)
        self.rv = pai.r
        pai.r = None
        cuv = pai.encipher(ui * v)
        self.ruv = pai.r
        self.cv = cv
        self.cuv = cuv
        self.v = v

        self.pubKey = pk
        self.cu = cu
        self.ru = ru
        self.ui = ui
        self.t = t
        self.n = n
        return cu, cuv, cv, ui * v

    def verify_uv(self):
        #a = random_a
        #  c1, c2, c3, m1, m2, r1, r2, r3,
        proof = Proof()
        proof.setup(self.pubKey, self.cu[0], self.cv, self.cuv, self.ui, self.v, self.ru[0], self.rv, self.ruv)

        c4, c24 = proof.random_m4()
        #proof.set_random_a(a)
        return proof.verify()

    def verify_oec(self):
        for i in range(2, self.t - 1):
            c1 = self.cu[0]
            c2 = self.cu[i - 1]
            c3 = self.cu[i]
            m1 = self.ui
            m2 = self.ui ** i
            r1 = self.ru[0]
            r2 = self.ru[i - 1]
            r3 = self.ru[i]
            #a = random_a

            proof = Proof()
            proof.setup(self.pubKey, c1, c2, c3, m1, m2, r1, r2, r3)

            c4, c24 = proof.random_m4()
            #proof.set_random_a(a)

            if not proof.verify():
                return False
        return True




def test():
    pai = Paillier()
    pai.__key_gen__()
    pk = pai.pubKey

    mf = MProof()
    cu, cuv, cv, uiv = mf.generate_param(pk, 4, 6, 10)
    mf.verify_uv(214143)
    print(mf.verify_oec(214143))

if __name__ == "__main__":
    test()