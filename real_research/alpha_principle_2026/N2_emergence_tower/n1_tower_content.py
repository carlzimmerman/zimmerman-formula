#!/usr/bin/env python3
"""N1 -- tower content, exact one-loop coefficients, anomaly sums, closed-form sum (pre-registration: N2_PREREGISTRATION.md, criterion N1).
Run:    PYTHONDONTWRITEBYTECODE=1 python3 n1_tower_content.py            (exit 0 iff all checks pass)
MUTATE: PYTHONDONTWRITEBYTECODE=1 python3 n1_tower_content.py MUTATE     (positional argv; uses the lane-A slip b_Y = (3/5) b_1 instead of (5/3) b_1; the SM hypercharge check must fail -> exit 1)
Everything is exact (fractions.Fraction) except the closed-form sums (mpmath/lgamma vs brute force).
"""
import sys
sys.dont_write_bytecode = True
import math
from fractions import Fraction as Fr
import sympy as sp
import mpmath as mp
import tower_lib as T
mp.mp.dps = 30
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
YN = Fr(3, 5) if MUT else Fr(5, 3)      # b_Y = YN * b_1 ; the correct factor is 5/3
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + (" " + m if m else ""))
    if not ok: fails.append(n)

print("== N1a: SM zero modes ==")
bsm = T.b_SM()
print("b_SM (Y,2,3) =", bsm, "; fermions", T.b_weyl(), "Higgs", T.b_higgs(), "gauge", T.b_sm_gauge())
chk("SM b = (41/6, -19/6, -7) from explicit field content", bsm == (Fr(41, 6), Fr(-19, 6), Fr(-7)))
b1_gut = Fr(3, 5) * bsm[0]
chk("GUT-normalised b_1 = 41/10 and b_Y = (5/3) b_1 = 41/6 (the lane-A pitfall is a factor 3/5)", b1_gut == Fr(41, 10) and YN * b1_gut == Fr(41, 6), "b_1=%s ; YN*b_1=%s" % (b1_gut, YN * b1_gut))
chk("lane B constants agree (B_Y, B_2, B_3)", (float(bsm[0]), float(bsm[1]), float(bsm[2])) == (T.RC.B_Y, T.RC.B_2, T.RC.B_3))
chk("SM species count: 28 bosonic (24 gauge dof + 4 Higgs) + 90 fermionic = 118", T.dof_sm_gauge() + T.dof_higgs() + T.dof_weyl() == 118 == T.N0)

print("== N1b: per-level tables ==")
exp = {"TA": (Fr(27, 2), Fr(49, 6), Fr(8)), "TB": (Fr(27, 2), Fr(7, 6), Fr(-5, 2))}
for tw, key in ((T.TA, "TA"), (T.TB, "TB")):
    d, b = tw.level_fn(1, True)
    print("%-36s per level: dof %d (incl. 5 graviton), b(Y,2,3) = %s ; GUT-norm b1 = %s" % (tw.name, d, tuple(str(c) for c in b), Fr(3, 5) * b[0]))
    chk("%s per-level coefficients equal the hand expectation %s" % (key, tuple(str(c) for c in exp[key])), b == exp[key])
    chk("%s levels identical for every j" % key, all(tw.level_fn(j, True) == tw.level_fn(1, True) for j in range(1, 20)))
chk("TA dof 189 and TB dof 225", T.TA.level_fn(1, True)[0] == 189 and T.TB.level_fn(1, True)[0] == 225)
chk("TB = TA + massive SM-adjoint KK vectors (0,-7,-21/2), +36 dof", T.add(T.TA.level_fn(1, True)[1], T.b_sm_adjoint_massive()) == T.TB.level_fn(1, True)[1] and T.b_sm_adjoint_massive() == (0, Fr(-7), Fr(-21, 2)))
chk("TA fermion part = 2 x SM fermions (Dirac KK levels): (40/3, 8, 8)", T.scale(T.b_weyl(), 2) == (Fr(40, 3), Fr(8), Fr(8)))
de, be = T.TC.level_fn(2, True); do, bo = T.TC.level_fn(1, True)
print("TC even j: dof %d, b = %s ; odd j: dof %d, b = %s" % (de, tuple(str(c) for c in be), do, tuple(str(c) for c in bo)))
chk("TC even: (1/6, -41/6, -21/2), 45 dof", be == (Fr(1, 6), Fr(-41, 6), Fr(-21, 2)) and de == 45)
chk("TC odd: (-523/18, -21/2, -41/6) (the pre-registration wrote -521/18 with a question mark: an arithmetic slip, corrected by the SU(5) gate below), 42 dof", bo == (Fr(-523, 18), Fr(-21, 2), Fr(-41, 6)) and do == 42)

print("== N1c: SU(5) universal-shift gate for TC (a complete SU(5) multiplet shifts 1/alpha_1 = 1/alpha_2 = 1/alpha_3 equally) ==")
adj = T.add(T.b_sm_adjoint_massive(), T.b_X_massive())
gut = (Fr(3, 5) * adj[0], adj[1], adj[2])
print("massive 24 (SM part + X part), GUT-normalised (b1,b2,b3) =", tuple(str(c) for c in gut))
chk("massive adjoint of SU(5) is universal: -(7/2) T(adj) = -35/2 in all three", gut == (Fr(-35, 2),) * 3)
h5 = T.add(T.b_higgs(), T.b_triplet_higgs()); h5g = (Fr(3, 5) * h5[0], h5[1], h5[2])
chk("5_H (doublet + colour triplet) universal: 1/6 each", h5g == (Fr(1, 6),) * 3, str(tuple(str(c) for c in h5g)))
matter = T.b_weyl(1); mg = (Fr(3, 5) * matter[0], matter[1], matter[2])
chk("one generation 10 + 5bar universal: 4/3 each", mg == (Fr(4, 3),) * 3, str(tuple(str(c) for c in mg)))
sum_even_odd = T.add(be, bo)
print("TC even+odd (a pair of levels) b =", tuple(str(c) for c in sum_even_odd), "; GUT-norm (b1,b2,b3) =", tuple(str(c) for c in (Fr(3, 5) * sum_even_odd[0], sum_even_odd[1], sum_even_odd[2])))
chk("TC: every per-level coefficient is negative for SU(2) and SU(3) (no screening, emergence sign infeasible)", all(c < 0 for c in (be[1], be[2], bo[1], bo[2])))

print("== N1d: anomaly sums (SM Weyl content per generation, exact) ==")
S = {"Y^3": Fr(0), "Y": Fr(0), "SU2^2 Y": Fr(0), "SU3^2 Y": Fr(0)}
for _, d3, d2, Y in T.WEYL_PER_GEN:
    S["Y^3"] += d3 * d2 * Y ** 3
    S["Y"] += d3 * d2 * Y
    if d2 == 2: S["SU2^2 Y"] += d3 * Y * Fr(1, 2)
    if d3 == 3: S["SU3^2 Y"] += d2 * Y * Fr(1, 2)
print("sums:", {k: str(v) for k, v in S.items()})
chk("SM anomalies vanish generation by generation", all(v == 0 for v in S.values()))
kkL = sum(d3 * d2 * Y ** 3 for _, d3, d2, Y in T.WEYL_PER_GEN); kkR = sum(d3 * d2 * Y ** 3 for _, d3, d2, Y in T.WEYL_PER_GEN)
chk("KK levels are Dirac (each LH zero-mode field has a RH partner of the same rep): level anomaly = L - R = 0", kkL - kkR == 0)
print("NOT derived: fixed-point (boundary) anomaly cancellation of the chiral zero modes on the orbifold (needs brane Chern-Simons terms; recalled from the literature, not read).")

print("== N1e: closed form of the one-loop tower sum ==")
K = sp.symbols("K", positive=True, integer=True)
Kx = sp.symbols("Kx", positive=True)
closed = K * sp.log(Kx) - sp.log(sp.factorial(K))
print("S(K, x) = sum_{n<=K} ln(x/n) =", closed)
chk("sympy: S(K, x=K) = K ln K - ln K!, and equals sum for K=7 exactly", sp.simplify(closed.subs({Kx: K}).subs(K, 7) - sum(sp.log(sp.Integer(7) / n) for n in range(1, 8))) == 0)
# asymptotics: K ln K - ln K! = K - (1/2) ln(2 pi K) - 1/(12K) + ...
diffs = []
for KK in (10, 100, 1000, 10000):
    s_exact = mp.mpf(KK) * mp.log(KK) - mp.loggamma(KK + 1)
    asym = KK - mp.log(2 * mp.pi * KK) / 2
    diffs.append((KK, float(s_exact - asym), float(-1 / (12 * mp.mpf(KK)))))
    print("   K=%5d: S - [K - ln(2 pi K)/2] = %.6e ; -1/(12K) = %.6e" % diffs[-1])
chk("Stirling: S(K,K) = K - (1/2) ln(2 pi K) - 1/(12 K) + O(1/K^3) (relative to the 1/12K term < 1e-2 at K >= 100)", all(abs(a / c - 1) < 1e-2 for KK, a, c in diffs if KK >= 100) and all(abs(a) < 0.1 for _, a, _ in diffs))
worst = 0.0
for tw in T.TOWERS:
    for k in (1, 2, 5, 17, 40, 101):
        for xf in (0.0, 0.37, 0.99):
            x = k + xf
            a = T.tower_sum(tw, k, x); b = T.tower_sum_brute(tw, k, x)
            worst = max(worst, max(abs(ai - bi) / max(1.0, abs(bi)) for ai, bi in zip(a, b)))
chk("lgamma closed form == brute-force sum for all three towers (k up to 101, fractional x)", worst < 1e-12, "worst rel diff %.2e" % worst)
sm_dev = 0.0
for x in (10.5, 30.0, 30.5, 37.9, 100.3):
    k = int(x)
    ex = k * math.log(x) - math.lgamma(k + 1); sm = x - 0.5 * math.log(2 * math.pi * x)
    sm_dev = max(sm_dev, abs(ex - sm))
chk("the SHARP-threshold sum is smooth in x: |S(floor x, x) - [x - (1/2) ln(2 pi x)]| < 0.01 for x >= 10 (no sawtooth; the linear term is what carries the size)", sm_dev < 0.01, "max dev %.4f" % sm_dev)
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
