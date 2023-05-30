import hashlib
import datetime
import gmpy2 as gy
import time

def H(*c):
    o = ""
    for i in c:
        o += str(int(i))
        o += "_"
    o = o[:-1]

    return int(hashlib.sha256(o.encode()).digest().hex(), 16)


def random_mpz(n, zero=False):
    time.sleep(0.00000000000000001)
    r = gy.mpz_random(gy.random_state(datetime.datetime.now().microsecond), n)
    while zero and r == 0:
        r = gy.mpz_random(gy.random_state(datetime.datetime.now().microsecond), n)
    return r

def random_bit_mpz(n_bits):
    rs = gy.random_state(datetime.datetime.now().microsecond)
    p = gy.mpz_urandomb(rs, n_bits)
    return p

class Counter(object):
    def __init__(self):
        self.start_t = time.perf_counter()

    # def start(self):
    #     self.start_t = time.perf_counter()

    def cost(self):
        return time.perf_counter() - self.start_t



if __name__ == "__main__":
    a = 111111111111111111111111111
    b = 1352153134
    c = 31514143
    print(H(a, b, c))
    print(random_mpz(10000, True))
    print(random_mpz(10000, False))

    c = Counter()

    print(c.cost())



