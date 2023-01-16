from paillier import Paillier
from shamir import *
from pedersen_use import *
import random
import gmpy2 as gy
import functools
from phe import paillier
from m_zkp_ui import MProof
import datetime


_PRIME = gy.next_prime(2 ** 256)


_rand_int = functools.partial(random.SystemRandom().randint, 0)


def _extended_gcd(a, b):
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y


def _divmod(num, den, p):
    inv, _ = _extended_gcd(den, p)
    return num * inv


def _calc_key(poly, x, prime):
    accum = 0
    for p in reversed(poly):
        accum *= x
        accum += p
        accum %= prime
    return accum


def make_random_shares(minimum, shares, prime=_PRIME):
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")

    poly = [_rand_int(prime - 1) for i in range(minimum)]
    shares = [(i, _calc_key(poly, i, prime))
              for i in range(1, shares + 1)]
    return poly[0], shares


def lagrange_interpolate(x, x_s, y_s, p):
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"


    def PI(vals):
        accum = 1
        for v in vals:
            accum *= v
        return accum


    nums = []
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
    return (_divmod(num, den, p) + p) % p


def recover_secret(shares: list, prime=_PRIME):
    if len(shares) < 2:
        raise ValueError("need at least two shares")

    x_s, y_s = zip(*shares)

    return lagrange_interpolate(0, x_s, y_s, prime)

def main():
    n = int(input("n participants: "))
    t = int(input("threshold t: "))


    sk=[]
    pk=[]
    for i in range(n):
        # paillier.DEFAULT_KEYSIZE = 256
        # public_key, private_key = paillier.generate_paillier_keypair()
        # pk.append(public_key)
        # sk.append(private_key)
        pai = Paillier()
        pai.__key_gen__()
        pk.append(pai.pubKey)
        sk.append(pai.priKey)


    poly = [_rand_int(_PRIME - 1) for i in range(t)]
    secret = poly[0]
    print('Secret: ', secret)


    c = [] 
    r = [] 
    v = commitment()
    param = v.setup(_PRIME)
    for i in range(t):
        ci, ri = v.commit(param, poly[i])
        c.append(ci)
        r.append(ri)


    for i in range(1, n + 1):
        mp = MProof()
        cu, cuv, cv, uiv = mp.generate_param(pk[i - 1], i, t, n)
        assert uiv != 0
        assert mp.verify_uv(gy.mpz_random(gy.random_state(datetime.datetime.now().microsecond), n))
        assert mp.verify_oec(gy.mpz_random(gy.random_state(datetime.datetime.now().microsecond), n))



    y = []
    css = []
    for i in range(1, n + 1):

        cr = 0
        for j in range(1, t + 1):
            cr += r[j - 1] * (i ** (j - 1))
        pai = Paillier()
        pai.pubKey = pk[i - 1]
        #y.append(pk[i - 1].encrypt(cr))
        y.append(pai.encipher(cr))


        ss_i = int(_calc_key(poly, i, _PRIME))
        print(i, "ss_i", ss_i)
        #css.append(pk[i - 1].encrypt(ss_i))
        css.append(pai.encipher(ss_i))


    shares = []
    for i in range(1, n + 1):
        # y_i = sk[i- 1].decrypt(y[i - 1])
        # ss_i = sk[i- 1].decrypt(css[i - 1])
        pai = Paillier()
        pai.pubKey = pk[i - 1]
        pai.priKey = sk[i - 1]
        y_i = pai.decipher(y[i - 1])
        ss_i = pai.decipher(css[i - 1])
        shares.append((i, ss_i))

        q, g, h = param
        alpha = 1
        for j in range(1, t + 1):
            alpha *= pow(c[j - 1], i ** (j - 1))
        alpha %= q
        print("ss_" + str(i) + ":" + str(ss_i) + " y_" + str(i) + ":" + str(y_i) + " pi-alpha_" + str(i) + ":" + str(alpha))


        print("u_" + str(i) + "VerificationResult: " + str(pow(g, ss_i, q) * pow(h, y_i, q) % q == alpha))
        print()


    print('Secret recovered from (t-1) subset of shares:         ', recover_secret(shares[:t - 1]))

    print('Secret recovered from (t) (minimum) subset of shares: ', recover_secret(shares[-t:]))

    print('Secret recovered from (t+1) subset of shares:         ', recover_secret(shares[-(t + 1):]))


if __name__ == '__main__':
    main()
