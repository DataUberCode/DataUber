from Crypto import Random
from Crypto.Random import random
from Crypto.Util import number
from math import gcd


class commitment:

    def setup(self, n):
        p = n
        print("p = ", p)

        r = 1
        while True:
            q = r * p + 1
            if number.isPrime(q):
                print("q = ", q)
                break
            r += 1

        # Since the order of G is prime, any element of G except 1 is a generator
        x = q - 1
        while True:
            g = x ** r % q
            if g != 1:
                break
            x -= 1

        print("g = ", g)

        while True:
            h = x ** r % q
            if(g != h and h != 1):
                break
            x -= 1
        print("h = ", h)

        return q, g, h

    def open(self, param, c, m, *r):
        q, g, h = param

        rSum = 0
        for rEl in r:
            rSum += rEl

        return c == (pow(g, m, q) * pow(h, rSum, q)) % q

    def add(self, param, *c):
        q = param[0]

        cSum = 1
        for cEl in c:
            cSum *= cEl
        return cSum % q

    def commit(self, param, m):
        q, g, h = param

        r = number.getRandomRange(1, q - 1)
        c = (pow(g, m, q) * pow(h, r, q)) % q
        return c, r


