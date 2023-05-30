import random
import gmpy2
import functools


_PRIME = gmpy2.next_prime(2 ** 256)


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


def Extended_Eulid(a: int, m: int) -> int:
    def extended_eulid(a: int, m: int):
        if a == 0:
            return 1, 0, m
        else:
            x, y, gcd = extended_eulid(m % a, a)
            x, y = y, (x - (m // a) * y)
            return x, y, gcd

    n = extended_eulid(a, m)
    if n[1] < 0:
        return n[1] + m
    else:
        return n[1]


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

if __name__ == '__main__':
    #n = int(input("n: "))
    #t = int(input("t: "))
    n = 10
    t = 8
    secret, shares = make_random_shares(minimum=t, shares=n)

    # print secret and shares
    print('Secret: ', secret)
    print('Shares:')
    if shares:
        for share in shares:
            print('  ', share)

    # t-1
    print('Secret recovered from (t-1) subset of shares:         ', recover_secret(shares[:t - 1]))
    # t
    print('Secret recovered from (t) (minimum) subset of shares: ', recover_secret(shares[-t:]))
    # t+1
    print('Secret recovered from (t+1) subset of shares:         ', recover_secret(shares[-(t + 1):]))

