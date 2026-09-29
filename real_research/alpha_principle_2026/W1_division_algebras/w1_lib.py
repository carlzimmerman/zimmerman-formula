"""w1_lib -- shared machinery of lane W1 (declared in W1_PREREGISTRATION.md).  Not a script; imported by w1_1 ... w1_5.

Contents: the octonion product table (Furey-Hughes convention e_i e_j = e_k for ijk in {124,235,346,457,561,672,713}, optionally corrupted for MUTATE controls), left- and
right-multiplication matrices (numpy and sympy), quaternion multiplication, and the PASS/FAIL bookkeeping with the lane's exit-code convention.
Exit codes: real run 0 if every check passes, 2 otherwise; MUTATE run 1 if the control bites (some check fails), 3 if the control is broken (all checks pass).
Writes nothing; no bytecode.
"""
import sys
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp

TRIPLES = [(1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7), (5, 6, 1), (6, 7, 2), (7, 1, 3)]


def octonion_table(corrupt=False):
    """c[i][j] = (k, sign) with e_i e_j = sign e_k for i, j in 1..7 (i != j); e_i e_i = -1.  corrupt: flip the sign of the triple (5,6,1) only (non-alternative table)."""
    tab = {}
    for (a, b, c) in TRIPLES:
        s = -1 if (corrupt and (a, b, c) == (5, 6, 1)) else 1
        for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
            tab[(x, y)] = (z, s)
            tab[(y, x)] = (z, -s)
    return tab


def oct_left_np(corrupt=False):
    """list L[0..7] of real 8x8 numpy matrices: (L[a] f)_k = coefficient of e_k in e_a f."""
    tab = octonion_table(corrupt)
    L = [np.eye(8)]
    for a in range(1, 8):
        M = np.zeros((8, 8))
        M[a, 0] = 1.0                      # e_a * 1 = e_a
        for b in range(1, 8):
            if a == b:
                M[0, b] = -1.0             # e_a e_a = -1
            else:
                k, s = tab[(a, b)]
                M[k, b] = float(s)
        L.append(M)
    return L


def oct_left_sp(corrupt=False):
    return [sp.Matrix(np.rint(M).astype(int).tolist()) for M in oct_left_np(corrupt)]


def oct_right_np(corrupt=False):
    """R[a] f = f e_a as real 8x8 matrices."""
    tab = octonion_table(corrupt)
    R = [np.eye(8)]
    for a in range(1, 8):
        M = np.zeros((8, 8))
        M[a, 0] = 1.0
        for b in range(1, 8):
            if a == b:
                M[0, b] = -1.0
            else:
                k, s = tab[(b, a)]          # e_b e_a
                M[k, b] = float(s)
        R.append(M)
    return R


def quat_left_np():
    """quaternion left multiplication matrices Q[0..3] (basis 1, eps1, eps2, eps3; eps_i eps_j = -delta + eps_ijk eps_k)."""
    def prod(i, j):
        if i == 0:
            return (j, 1)
        if j == 0:
            return (i, 1)
        if i == j:
            return (0, -1)
        k = 6 - i - j
        eps = 1 if (i, j, k) in ((1, 2, 3), (2, 3, 1), (3, 1, 2)) else -1
        return (k, eps)
    L = []
    R = []
    for a in range(4):
        ML = np.zeros((4, 4))
        MR = np.zeros((4, 4))
        for b in range(4):
            k, s = prod(a, b)
            ML[k, b] = s
            k2, s2 = prod(b, a)
            MR[k2, b] = s2
        L.append(ML)
        R.append(MR)
    return L, R


class Checks:
    def __init__(self, mutate=False):
        self.mut = mutate
        self.items = []

    def __call__(self, name, ok, info=""):
        ok = bool(ok)
        self.items.append((name, ok))
        print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")
        return ok

    def finish(self, title=""):
        nfail = sum(1 for _, ok in self.items if not ok)
        n = len(self.items)
        print(f"\nSUMMARY{' ' + title if title else ''}: {n - nfail}/{n} checks pass" + (" [MUTATE]" if self.mut else ""))
        if self.mut:
            code = 1 if nfail else 3
            print(f"MUTATE control {'bites (exit 1)' if nfail else 'is BROKEN: every check still passes (exit 3)'}")
            sys.exit(code)
        sys.exit(2 if nfail else 0)
