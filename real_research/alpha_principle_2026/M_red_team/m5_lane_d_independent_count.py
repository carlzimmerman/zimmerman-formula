#!/usr/bin/env python3
"""M5 -- independent re-implementation (numpy, from lane D's DECLARED grammar in D_PREREGISTRATION.md, not from D's code) of the grammar sizes and hit counts.
Compares E1(12) and E2(6) with D's printed d1_grammar_sizes.out:
   E1(12): 38,948 distinct, 19 within 1e-2 of T, 1 within 1e-3;   E2(6): 8,820,869 distinct, 3,047 within 1e-2, 289 within 1e-3, 1 within 1e-5.
Run:    python3 m5_lane_d_independent_count.py
MUTATE: python3 m5_lane_d_independent_count.py MUTATE   (removes the sqrt operation; the 'matches D' checks must fail -> exit 1)
Grammar (as declared by D): atoms {1..N, pi, e, Z=2 sqrt(8 pi/3)}; unary {sqrt, sq, inv, ln}; binary {+,-,*,/,pow}; positive finite values in [1e-30,1e30] only,
ln(1)=0 dropped, distinct = relative 1e-12.  L1 = atoms u U(atoms); B1 = B(L1,L1); T1 = B1 u U(B1); E1 = L1 u T1; B2 = B(L1,T1) u B(T1,L1); E2 = E1 u B2 u U(B2).
"""
import sys
import numpy as np
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
T = 137.035999177
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + " " + m)
    if not ok: fails.append(n)

def clean(v):
    v = v[np.isfinite(v)]
    return v[(v >= 1e-30) & (v <= 1e30)]
def dedup(v):
    v = clean(np.asarray(v, dtype=np.float64))
    if v.size == 0: return v
    lv = np.sort(np.log(v))
    keep = np.concatenate(([True], np.diff(lv) > 1e-12))
    return np.exp(lv[keep])
def unary(v):
    with np.errstate(all='ignore'):
        outs = [v**2, 1.0/v, np.log(v)]
        if not MUT: outs.append(np.sqrt(v))
    outs = [o[o > 0] for o in outs]           # ln(v) <= 0 dropped (ln 1 = 0, negatives twin-covered)
    return np.concatenate(outs)
def binary(a, b):
    """all pairs a[i] op b[j] for + - * / pow, positive results only"""
    A = a[:, None]; B = b[None, :]
    outs = []
    with np.errstate(all='ignore'):
        outs.append((A + B).ravel()); outs.append((A - B).ravel()); outs.append((A * B).ravel()); outs.append((A / B).ravel()); outs.append((A ** B).ravel())
    v = np.concatenate(outs)
    return v[np.isfinite(v) & (v > 0)]
def binary_chunked(a, b, chunk=400):
    res = []
    for i in range(0, len(a), chunk):
        res.append(dedup(binary(a[i:i+chunk], b)))
    return dedup(np.concatenate(res))

def grammar(N):
    Z = 2*np.sqrt(8*np.pi/3)
    atoms = np.array(list(range(1, N+1)) + [np.pi, np.e, Z], dtype=np.float64)
    L1 = dedup(np.concatenate([atoms, unary(atoms)]))
    B1 = binary_chunked(L1, L1)
    T1 = dedup(np.concatenate([B1, unary(B1)]))
    E1 = dedup(np.concatenate([L1, T1]))
    return L1, B1, T1, E1
def hits(v, tol):
    return int(np.sum(np.abs(v/T - 1) < tol))

# ---- E1(12)
L1, B1, T1, E1 = grammar(12)
print("N=12: L1 %d  B1 %d  T1 %d  E1 %d" % (len(L1), len(B1), len(T1), len(E1)))
print("E1(12): within 1e-2: %d ; 1e-3: %d ; 1e-5: %d" % (hits(E1, 1e-2), hits(E1, 1e-3), hits(E1, 1e-5)))
chk("E1(12) distinct count within 2 % of D's 38,948", abs(len(E1)/38948 - 1) < 0.02, "mine %d" % len(E1))
chk("E1(12) hits: 19 within 1e-2 (+-3) and 1 within 1e-3 (D)", abs(hits(E1, 1e-2) - 19) <= 3 and hits(E1, 1e-3) == 1)
# ---- E2(6)
L1, B1, T1, E1 = grammar(6)
print("N=6: L1 %d  B1 %d  T1 %d  E1 %d   (D: 38 / 3748 / 13337 / 13337)" % (len(L1), len(B1), len(T1), len(E1)))
chk("L1, B1, T1 distinct counts within 2 % of D's (38, 3748, 13337)", abs(len(L1)/38-1) < .02 and abs(len(B1)/3748-1) < .02 and abs(len(T1)/13337-1) < .02)
B2 = np.concatenate([binary_chunked(L1, T1, 2), binary_chunked(T1, L1, 200)])
B2 = dedup(B2)
E2 = dedup(np.concatenate([E1, B2, dedup(unary(B2))]))
print("E2(6): distinct %d (D: 8,820,869)" % len(E2))
h2, h3, h5 = hits(E2, 1e-2), hits(E2, 1e-3), hits(E2, 1e-5)
print("E2(6): within 1e-2: %d ; 1e-3: %d ; 1e-5: %d   (D: 3047 / 289 / 1)" % (h2, h3, h5))
chk("E2(6) distinct count within 2 % of D's 8,820,869", abs(len(E2)/8820869 - 1) < 0.02)
chk("E2(6) hits within 1e-2 (D 3047) and 1e-3 (D 289) agree within 5 %", abs(h2/3047 - 1) < .05 and abs(h3/289 - 1) < .05)
chk("E2(6) hits within 1e-5 equal D's 1 (+-1)", abs(h5 - 1) <= 1)
rho = h2 / len(E2) / 2e-2
print("independent density rho = fraction per unit relative deviation = %.4f (D: 0.0173)" % rho)
chk("independent rho within 10 % of D's 0.0173", abs(rho/0.0173 - 1) < 0.10)
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
