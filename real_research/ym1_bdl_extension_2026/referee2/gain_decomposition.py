#!/usr/bin/env python3
"""
Tasks 3+4: independent recomputation (mpmath, 40 digits) of lam_c and X_d, and a decomposition of the
factor ~3 between this lane (L326) and the space-time polymer method (ym1_hamiltonian, X_3 = 185.3).
Both lanes condition on the SAME quantity  r := 2 b_N /(x^2 C_F)  (= lane eps = other lambda/C_F)
and conclude the SAME gap  x C_F/4.  So X ratios = sqrt of ratios of the admissible r.
"""
import mpmath as mp
from math import comb
mp.mp.dps = 40

def betas(s, mode):
    g0 = mp.sqrt(sum(mp.mpf(comb(s - 1, t - 1)) / t ** 2 for t in range(1, s + 1)))
    gS = (s + 1) * mp.sqrt(sum(mp.mpf(comb(s, t)) / (t + 1) ** 2 for t in range(0, s + 1)))
    if mode == "CS":        # lane (E3)-(E5)
        return [g0] + [2 ** k * (g0 * s ** k + k * gS * s ** (k - 1)) for k in range(1, 2 * s + 1)]
    if mode == "count":     # BDL-style counting, correct |M_j| <= (s+1)|M|  (lane S5)
        return [mp.mpf(2 ** (s - 1))] + [2 ** k * 2 ** s * (s ** k + k * (s + 1) * s ** (k - 1)) for k in range(1, 2 * s + 1)]

def q(b, m):  return b[0] + sum(b[k] * m ** k / mp.factorial(k) for k in range(1, len(b)))
def qp(b, m): return sum(b[k] * m ** (k - 1) / mp.factorial(k - 1) for k in range(1, len(b)))

def lam_exact_root(b):
    mu = mp.findroot(lambda m: q(b, m) - 2 * m * qp(b, m), 0.01)
    return mu / q(b, mu), mu

def lam_disc(b):
    """BDL Claim-2 style: a = b0, uniform B = max_k beta_k; disc radius r with |Q| >= a/2 ; lam = r/(2*(a+...))
    reproduce BDL's recipe: |Q(mu)-a| <= B*(e^{|mu|}-1) ; choose |mu| <= r where B(e^r-1) <= a/2, then
    lam_conv = (r/2)/(a + B(e^{r/2}-1)) on the circle of radius r/2; gap criterion 2*lam*B*e^{mu} < 1 with mu = r/2."""
    a = b[0]; B = max(b[1:])
    r = mp.log(1 + a / (2 * B))
    lam1 = (r / 2) / (a + B * (mp.e ** (r / 2) - 1))
    lam2 = 1 / (2 * B * mp.e ** (r / 2))
    return min(lam1, lam2)

X = lambda r_adm, pref=mp.mpf(32) / 3: mp.sqrt(pref / r_adm)
print("s=4 link grouping, D = 2(d-1); admissible r = lam_c / D ; X_d(uniform) = sqrt((32/3)/r)")
rows = {}
for mode in ("CS", "count"):
    b = betas(4, mode)
    lr, mu = lam_exact_root(b)
    ld = lam_disc(b)
    rows[mode] = (lr, ld)
    print(f"  {mode:5s}: beta_1={mp.nstr(b[1],6)}  beta_8={mp.nstr(b[8],6)}  lam(exact root)={mp.nstr(lr,8)}  (mu_c={mp.nstr(mu,8)})"
          f"   lam(BDL disc-type)={mp.nstr(ld,6)}")
print()
other = {2: mp.mpf("6.2137e-4") / 1, 3: mp.mpf("6.2137e-4") / 2, 4: mp.mpf("6.2137e-4") / 3}
print("  d   X_d uniform:  lane(CS,root)  lane-count(root)  CS+disc  count+disc  |  other method   | SU(2),b=2: lane  other")
for d in (2, 3, 4):
    D = 2 * (d - 1)
    xs = [X(rows["CS"][0] / D), X(rows["count"][0] / D), X(rows["CS"][1] / D), X(rows["count"][1] / D)]
    xo = X(other[d])
    su2 = lambda r: mp.sqrt((mp.mpf(2 * 2) / mp.mpf(3) * 4) / r)   # 2 b_N / C_F = 4/(3/4) = 16/3
    print(f"  {d}   " + "  ".join(f"{mp.nstr(v,6):>10s}" for v in xs) + f"   |   {mp.nstr(xo,6):>8s}      |  {mp.nstr(su2(rows['CS'][0]/D),5):>6s}  {mp.nstr(su2(other[d]),5):>6s}")
print()
d = 3; D = 4
print(f"  d=3 factor lane/other in X: {mp.nstr(X(other[3]) / X(rows['CS'][0]/D), 5)} ;"
      f" of which sector Cauchy-Schwarz alone (CS vs count, both exact root): {mp.nstr(mp.sqrt(rows['CS'][0]/rows['count'][0]),5)} ;"
      f" count(root) vs other: {mp.nstr(X(other[3]) / X(rows['count'][0]/D),5)}")
print(f"  exact root vs disc (CS constants): x{mp.nstr(mp.sqrt(rows['CS'][0]/rows['CS'][1]),4)} in X")
