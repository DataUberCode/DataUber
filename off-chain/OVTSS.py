from paillier import Paillier
from shamir import recover_secret, _calc_key
from pedersen_ec import PedersenEC
from m_zkp_ui import MProof
from zkp_r_sd import ProofRsd
from zkp_r_dl import ProofRdl
from help import Counter, random_mpz
import gmpy2 as gy

security_bit = 112
paillier_n_bit = 2048

v = PedersenEC()
Z_q = gy.next_prime(2 ** (paillier_n_bit // 2))


def main():
    #n = int(input("n participants: "))
    #t = int(input("threshold t: "))
    n = 10
    t = 6
    assert t <= n, "t error"

    all_counter = Counter()
    all_m = 0

    sk = []
    pk = []
    c_m_pk = Counter()
    for i in range(n):
        pai = Paillier()

        pai.__key_gen__(n_bits=paillier_n_bit)
        pk.append(pai.pubKey)
        sk.append(pai.priKey)
    all_m += c_m_pk.cost()


    poly = [int(random_mpz(Z_q - 1)) for i in range(t)]
    secret = poly[0]
    print('Secret: ', secret)


    c = []
    r = []

    for i in range(t):
        ci, ri = v.commit(poly[i])
        c.append(ci)
        r.append(ri)


    m_u = []
    for i in range(n):
        m_u.append(i + 1)

    for i in range(1, n + 1):
        c_m_proof_u = Counter()
        mp = MProof()
        cu, cuv, cv, uiv = mp.generate_param(pk[i - 1], m_u[i - 1], t, n)
        all_m += c_m_proof_u.cost()
        assert uiv != 0, "Proof of non-zero u is valid"
        assert mp.verify_uv(), "Proof of non-zero u is invalid"
        assert mp.verify_oec(), "Proof of the validity u's ciphertext is invalid"


    y = []
    css = []
    for i in range(1, n + 1):
        pai = Paillier()
        pai.pubKey = pk[i - 1]
        n_2q = pk[i - 1][0] ** 2

        y_i = 1
        for j in range(t):
            y_i *= pow(pai.encipher(m_u[i - 1] ** j), r[j], n_2q)
        y_i %= n_2q
        y.append(y_i)

        css_i = 1
        for j in range(t):
            css_i *= pow(pai.encipher(m_u[i - 1] ** j), poly[j], n_2q)
        css_i %= n_2q
        css.append(css_i)

    S_i_s = []

    shares = []
    for i in range(1, n + 1):
        c_m_verify_commit = Counter()
        pai = Paillier()
        pai.pubKey = pk[i - 1]
        pai.priKey = sk[i - 1]
        y_i = pai.decipher(y[i - 1])
        ss_i = pai.decipher(css[i - 1])
        shares.append((m_u[i - 1], ss_i))

        alpha = c[0]
        for j in range(1, t):
            alpha += (m_u[i - 1] ** j) * c[j]


        assert v.open(ss_i, alpha, y_i), f"M_{i} is invalid"
        all_m += c_m_verify_commit.cost()

        c_m_proof_Si = Counter()
        n_2q = pk[i - 1][0] ** 2
        g = pk[i - 1][1]
        S_i = pow(g, ss_i, n_2q)
        rn = pai.extract_rn(ss_i, css[i - 1])
        proofRsd = ProofRsd()
        proof_param = proofRsd.prover_choose_param(pk[i - 1], ss_i, css[i - 1], rn, S_i)
        all_m += c_m_proof_Si.cost()
        assert proofRsd.verify(proof_param), "S_i is invalid"
        S_i_s.append(S_i)

        print(f"M_{i} check success!")


    all_reporter_cost = 0
    c_reporter_proof = Counter()
    reporter_id = 123131314111
    proofRdl = ProofRdl()
    v_pk = pk[0]
    v_s = shares[0][1]
    v_S = pow(v_pk[1], v_s, v_pk[0])
    proof_param = proofRdl.prover_choose_param(v_pk, v_s, v_S, reporter_id)
    all_reporter_cost += c_reporter_proof.cost()
    if proofRdl.verify(proof_param):
        print("one reporter complain success!!!")


    recover_secret_t = recover_secret(shares[-t:], Z_q)
    all_time = all_counter.cost()
    recover_secret_t_sub1 = recover_secret(shares[:t - 1], Z_q)
    recover_secret_t_add1 = recover_secret(shares[-(t + 1):], Z_q)

    # t-1
    print('Secret recovered from (t-1) subset of shares:         ', recover_secret_t_sub1)
    # t
    print('Secret recovered from (t) (minimum) subset of shares: ', recover_secret_t)
    # t+1
    print('Secret recovered from (t+1) subset of shares:         ', recover_secret_t_add1)


    assert recover_secret_t_sub1 != secret and recover_secret_t == recover_secret_t_add1 \
           and recover_secret_t == secret, "Reconstruction fails"


if __name__ == '__main__':
    main()