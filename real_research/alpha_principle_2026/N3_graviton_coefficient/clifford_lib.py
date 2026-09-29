"""Exact Clifford algebra Cl(p,q) on blades (bitmask representation), rational coefficients.
Used by n1 and n2 of lane N3.  No file I/O, no randomness.  Scalar part = coefficient of the empty blade.
Signature: sig[i] = e_i^2 = +1 or -1.
"""
from fractions import Fraction

class Cl:
    def __init__(self, sig):
        self.sig = list(sig)
        self.d = len(sig)

    def blade_mul(self, a, b):
        """product of basis blades a,b (bitmasks): returns (sign, mask)."""
        s = 1
        # sign from reordering: count pairs (i in a, j in b) with i > j
        aa = a >> 1
        cnt = 0
        while aa:
            cnt += bin(aa & b).count("1")
            aa >>= 1
        if cnt & 1:
            s = -s
        common = a & b
        i = 0
        while common:
            if common & 1:
                s *= self.sig[i]
            common >>= 1
            i += 1
        return s, a ^ b

    def mul(self, x, y):
        out = {}
        for ma, ca in x.items():
            for mb, cb in y.items():
                s, m = self.blade_mul(ma, mb)
                c = out.get(m, 0) + s * ca * cb
                if c == 0:
                    out.pop(m, None)
                else:
                    out[m] = c
        return out

    def gen(self, i):
        return {1 << i: Fraction(1)}

    def word(self, idx, coeff=Fraction(1)):
        """product e_{idx[0]} e_{idx[1]} ... times coeff"""
        x = {0: Fraction(coeff)}
        for i in idx:
            x = self.mul(x, self.gen(i))
        return x

    def scalar(self, x):
        return x.get(0, Fraction(0))

    @staticmethod
    def add(x, y, cy=1):
        out = dict(x)
        for m, c in y.items():
            v = out.get(m, 0) + cy * c
            if v == 0:
                out.pop(m, None)
            else:
                out[m] = v
        return out

def lorentz_plus_internal(N):
    """Cl(1+N,3): index 0 -> +1 (time), 1..3 -> -1, 4..3+N -> +1 (internal)."""
    return Cl([1, -1, -1, -1] + [1] * N)
