from help import H, random_mpz
from paillier import Paillier

class ProofRdl(object):
    def __init__(self):
        self.pubKey = None
        self.S = None

    def prover_choose_param(self, pk, s, S, ID):
        self.pubKey = pk
        n = pk[0]
        g = pk[1]
        self.S = S

        r = random_mpz(n)

        R = pow(g, r, n)

        c = H(S, R, ID)

        z = r + s * c % n

        return R, z, ID


    def verify(self, proof_param):
        R, z, ID = proof_param
        pk = self.pubKey
        n = pk[0]
        g = pk[1]
        S = self.S

        c = H(S, R, ID)

        return R * pow(S, c, n) % n == pow(g, z, n)


def test():
    pai = Paillier()
    pai.__key_gen__()
    pk = pai.pubKey
    n = pk[0]
    g = pk[1]

    s = 129417418974281218111111111111111111
    S = pow(g, s, n)

    ID = 104812941421412455250991881911

    proof = ProofRdl()

    proof_param = proof.prover_choose_param(pk, s, S, ID)

    print(proof.verify(proof_param))


if __name__ == "__main__":
    test()




