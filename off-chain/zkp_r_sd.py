from paillier import Paillier
from help import H,random_mpz

class ProofRsd(object):
    def __init__(self):
        self.pubKey = None
        self.cu = None
        self.U = None


    def prover_choose_param(self, pk, u, cu, rn, U):
        self.pubKey = pk
        self.cu = cu
        n = pk[0]
        g = pk[1]
        n_2q = n ** 2

        # random s and rs
        s = random_mpz(n, True)
        pai = Paillier()
        pai.pubKey = pk
        rs = random_mpz(n, False)
        pai.r = rs
        cs = pai.encipher(s)

        S = pow(g, s, n_2q)
        #U = pow(g, u, n_2q)
        self.U = U


        c = H(S, cs, pk[0], pk[1], cu, g, U)

        z = s + c * u % n_2q

        rzn = pow(rn, c, n_2q) * pow(rs, n, n_2q) % n_2q

        return S, cs, z, rzn



    def verify(self, proof_param):
        S, cs, z, rzn = proof_param
        pk = self.pubKey
        n = pk[0]
        g = pk[1]
        n_2q = n ** 2
        cu = self.cu
        U = self.U

        c = H(S, cs, pk[0], pk[1], cu, g, U)

        if pow(g, z, n_2q) != S * pow(U, c, n_2q) % n_2q:
            return False

        pai = Paillier()
        pai.pubKey = pk
        pai.rn = rzn
        pai.use_rn = True

        return pow(cu, c, n_2q) * cs % n_2q == pai.encipher(z % n)





def test():
    pai = Paillier()
    pai.__key_gen__(n_bits=256)
    pk = pai.pubKey

    u = 10087211
    cu = pai.encipher(u)
    rn = pai.rn

    proof = ProofRsd()
    proof_param = proof.prover_choose_param(pk, u, cu, rn)

    print(proof.verify(proof_param))



if __name__ == "__main__":
    test()









