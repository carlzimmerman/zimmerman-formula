#!/usr/bin/env python3
"""PIK1 row 0: exact certification of L_K(Q, Pi) = F(Q) S(Pi).

    Q = sqrt(-g^{mn} d_m tau d_n tau);  n_m = -d_m tau / Q;  h_mn = g_mn + n_m n_n
    l = ln Q;  A_m = -h_m^n d_n l;  Pi = D_m P^m = (Q sqrt(-g))^{-1} d_m (Q sqrt(-g) P^m) [n.P = 0]

The Lagrangian density sqrt(-g) L_K is assembled on jet symbols for (g^{mn}, tau, P_m) in 2+1;
the Euler-Lagrange densities and the tau current follow from the total derivative D_a; the
claimed closed forms are subtracted and evaluated to 50 digits on exact configurations.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import sys
import time

import sympy as sp

NC = 3
IDX = [0, 1, 2]
_tt, _xx, _yy = sp.symbols('tt xx yy')
CO = (_tt, _xx, _yy)
MUT = '--mutate' in sys.argv
T0 = time.time()
OUT = []


def P_(s):
    print(s, flush=True)
    OUT.append(s)


def _o(*a):
    o = [0, 0, 0]
    for i in a:
        o[i] = o[i] + 1
    return tuple(o)


class Bag(object):
    pass


def sym(tag, *ix):
    nm = tag
    for k in ix:
        nm = nm + str(k)
    return sp.Symbol(nm)


def kn(i, j):
    a = min(i, j)
    b = max(i, j)
    return str(a) + str(b)


def build_jets():
    J = Bag()
    J.G = [[sp.Symbol('G' + kn(i, j)) for j in IDX] for i in IDX]
    J.Gc = [[[sp.Symbol('Gc' + kn(i, j) + '_' + str(a)) for a in IDX] for j in IDX] for i in IDX]]
    J.Gcc = [[[[sp.Symbol('Gcc' + kn(i, j) + '_' + kn(a, b)))] for b in IDX] for a in IDX] for j in IDX] for i in IDX]]]]
    J.T = [sp.Symbol('T' + str(i)) for i in IDX]
    J.Tc = [[sp.Symbol('Tc' + kn(i, j))) for j in IDX] for i in IDX]
    J.Tcc = [[[spSymbol('Tcc' + str(i) + '_' + kn(j, k)))) for k in IDX]]]
    return J
