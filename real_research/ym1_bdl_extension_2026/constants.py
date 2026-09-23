#!/usr/bin/env python3
"""
L326 / constants.py -- explicit strong-coupling gap threshold for Hamiltonian
(Kogut-Susskind) lattice SU(N), obtained by extending Bravyi-DiVincenzo-Loss
(CMP 284 (2008) 481, arXiv:0707.1894; "BDL") Lemmas 1-5 / Appendix A to
  (i) s-body interactions (plaquette: s = 4 links; or s = 3 vertex-sites), and
 (ii) arbitrary (truncated -> infinite) on-site spaces, via SECTOR-VALUED creation
      operators whose constants do not depend on the on-site dimension.

Equation numbers (E1)-(E12) are those of DERIVATION.md in this folder; the BDL
equation each one adapts is given there.  Implemented here:
  (E3)  gamma0(s)^2  = sum_{t=1}^{s} C(s-1,t-1)/t^2                 [type-0 sector sum]
  (E4)  gammaS(s)^2  = (s+1)^2 sum_{t=0}^{s} C(s,t)/(t+1)^2         [type-j sector sum]
  (E5)  beta_0 = gamma0 ; beta_k = 2^k (gamma0 s^k + k gammaS s^(k-1)), 1<=k<=2s
                                                                     [Lemma 3', BDL eq.19]
  (E6)  q(mu) = beta_0 + sum_{k=1}^{2s} beta_k mu^k / k!             [Lemma 5', BDL eq.38-39]
  (E7)  mu*(lam) = least positive root of mu = lam q(mu)             [majorant, BDL eq.37]
  (E8)  gap criterion  2 lam q'(mu*(lam)) < 1                        [Lemma 4', BDL eq.21]
  (E9)  lam_gap:  q(mu_g) = 2 mu_g q'(mu_g),  lam_gap = mu_g/q(mu_g)
  (E10) eps_c = lam_gap Delta/(D J)   (analogue of BDL's 2 eps_0 = 2^-17 Delta/(dJ))
  (E11) X_d(N,b_N) = sqrt( (2 b_N / C_F) D / lam_cert ),  uniform: sqrt((32/3) D/lam_cert)
  (E12) theta_equiv = 2 m lam_cert / D,  door-E formula X_d = max(1, sqrt(2 A_d/theta))
The threshold is CERTIFIED with exact rational arithmetic (Fractions) using
rational upper bounds on the irrational gamma's (S4).

House rule: no fabricated constants -- every number printed is computed here from
the stated inequalities; nothing is taken from Yarotsky (2004), which remains unread.
"""
from fractions import Fraction as Fr
from math import comb, factorial, isqrt, sqrt

ok = True
def check(name, cond, detail=""):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    ok = ok and bool(cond)

def sqrt_up(x, digits=15):
    """rational upper bound on sqrt(x) for a non-negative Fraction x"""
    scale = 10 ** (2 * digits)
    v = -((-x.numerator * scale) // x.denominator)       # ceil
    r = isqrt(v)
    if r * r < v:
        r += 1
    return Fr(r, 10 ** digits)

# ------------------------------------------------------------------ S1 inputs
print("== S1 INPUTS ==")
print("  repo Hamiltonian (i15/PROOF.md s.1):  H = (x/2) sum_l C_l + (b_N/x) sum_p (1 - T_p),")
print("    T_p = Re Tr U_p / N  (||T_p|| <= 1),  C_F = (N^2-1)/(2N) >= 3/4,  0 <= b_N <= 2N")
print("  normalised (E1): H/(x C_F/2) = sum_l h_l + eps sum_p V_p,  h_l = C_l/C_F (Delta = 1),")
print("    V_p = -T_p (J = 1),  eps = 2 b_N/(x^2 C_F)  <=  32/(3 x^2)  for all N >= 2, b_N <= 2N")
print("  groupings: LINK sites  s = 4, D = 2(d-1)       (plaquettes per link)")
print("             VERTEX sites s = 3, D = 3d(d-1)/2   (plaquettes touching a vertex group)")
print("  gap fraction targeted: Delta/2 (BDL Thm 1; repo uses normalized gap >= 1/2)")
# brute-force the incidence numbers D on a periodic box of side 5 (interior = infinite lattice)
import itertools
for d in (2, 3, 4):
    L = 5
    pts = list(itertools.product(range(L), repeat=d))
    def sh(x, i, sgn=1):
        y = list(x); y[i] = (y[i] + sgn) % L; return tuple(y)
    link_count, vert_count = {}, {}
    for y in pts:
        for i, j in itertools.combinations(range(d), 2):
            links = [(y, i), (sh(y, i), j), (sh(y, j), i), (y, j)]
            for l in links:
                link_count[l] = link_count.get(l, 0) + 1
            for z in {l[0] for l in links}:
                vert_count[z] = vert_count.get(z, 0) + 1
    check(f"d={d}: every link lies in {2*(d-1)} plaquettes; every vertex-site meets {3*d*(d-1)//2}",
          set(link_count.values()) == {2 * (d - 1)} and set(vert_count.values()) == {3 * d * (d - 1) // 2})

# ------------------------------------------------------------------ S2 constants
def gammas(s):
    g0sq = sum(Fr(comb(s - 1, t - 1), t * t) for t in range(1, s + 1))            # (E3)
    gSsq = (s + 1) ** 2 * sum(Fr(comb(s, t), (t + 1) ** 2) for t in range(0, s + 1))  # (E4)
    return g0sq, gSsq

def betas(s, upper=True):
    g0sq, gSsq = gammas(s)
    if upper:
        g0, gS = sqrt_up(g0sq), sqrt_up(gSsq)
    else:
        g0, gS = sqrt(g0sq), sqrt(gSsq)
    b = [g0] + [2 ** k * (g0 * s ** k + k * gS * s ** (k - 1)) for k in range(1, 2 * s + 1)]  # (E5)
    return b

def q(b, m):  return b[0] + sum(b[k] * m ** k / factorial(k) for k in range(1, len(b)))       # (E6)
def qp(b, m): return sum(b[k] * m ** (k - 1) / factorial(k - 1) for k in range(1, len(b)))

def lam_gap_float(b):                                                                           # (E9)
    f = lambda m: q(b, m) - 2 * m * qp(b, m)     # decreasing in m >= 0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return lo / q(b, lo), lo

print("\n== S2 sector constants (E3)-(E5) ==")
for s in (2, 3, 4):
    g0sq, gSsq = gammas(s)
    print(f"  s={s}: gamma0^2 = {g0sq} = {float(g0sq):.6f} (gamma0 = {sqrt(g0sq):.6f});"
          f"  gammaS^2 = {gSsq} = {float(gSsq):.6f} (gammaS = {sqrt(gSsq):.6f})")
    bl = betas(s, upper=False)
    print("        beta_k, k=0..%d: " % (2 * s) + " ".join(f"{x:.4g}" for x in bl))
# monotonicity used in (E4): ((n+s)/(n+t))^2 decreasing in n  => max over n>=1 at n=1
for s in (2, 3, 4):
    vals = [(n + s) ** 2 * sum(Fr(comb(s, t), (n + t) ** 2) for t in range(s + 1)) for n in range(1, 40)]
    check(f"s={s}: type-j sector sum is maximal at n'=1 (E4)", all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1)))

# ------------------------------------------------------------------ S3 BDL cross-checks
print("\n== S3 cross-checks against BDL (qubits, two-body, max degree d) ==")
# (a) BDL App. A with the CORRECTED ratio |M_j| <= 3|M| (their text says 2|M|; see checks.py C4)
worst = 0
for k in range(1, 5):
    Xj = k * 4 * 3 * 2 ** k * 2 ** (k - 1)      # k slots x 4 sets x 3/|M_j| x 2^k J x prod_{i!=j} 2
    X0 = 4 * 2 ** k * 2 ** k                    # 4 sets x 1/Delta x 2^k J x prod 2
    worst = max(worst, Xj + X0)
check("BDL Lemma 3 constant 2^13 survives the corrected |M_j|<=3|M|", worst <= 2 ** 13,
      f"(corrected max over k<=4: {worst} <= 8192)")
# (b) BDL's own constants (a = 2, b = 2^13 uniform, depth 4) through the exact majorant (E7)-(E9)
bBDL = [2.0] + [2.0 ** 13] * 4
lamB, _ = lam_gap_float(bBDL)
check("exact majorant with BDL's constants reproduces BDL Thm 1 (lam >= 2^-17)", lamB >= 2 ** -17,
      f"(lam_gap = {lamB:.4e} vs 2^-17 = {2**-17:.4e}; ~2^-14 = {2**-14:.4e})")
# (c) the present Lemma 3' at s = 2 is never weaker than BDL's 2^13
b2 = betas(2, upper=False)
check("sector/Cauchy-Schwarz beta_k(s=2) <= 2^13 for all k<=4", all(x <= 2 ** 13 for x in b2[1:]),
      f"(beta_4(s=2) = {b2[4]:.1f})")
print(f"  (byproduct: s=2 constants give lam_gap = {lam_gap_float(b2)[0]:.4f}, i.e. BDL's qubit"
      f" threshold improves by {lam_gap_float(b2)[0]/2**-17:.0f}x -- same proof, sharper bookkeeping)")

# ------------------------------------------------------------------ S4 certified threshold
print("\n== S4 certified lambda_gap (E7)-(E9), exact rational arithmetic ==")
cert = {}
for s in (3, 4):
    bup = betas(s, upper=True)             # rational UPPER bounds on every beta_k
    lf, mf = lam_gap_float(betas(s, upper=False))
    lam_c = Fr(int(lf * (1 - 1e-6) * 10 ** 12), 10 ** 12)
    mu_c = Fr(mf).limit_denominator(10 ** 15)
    c1 = mu_c - lam_c * q(bup, mu_c) >= 0            # => mu*(lam) <= mu_c for all lam <= lam_c
    c2 = 2 * lam_c * qp(bup, mu_c) < 1              # => gap criterion (E8) for all lam <= lam_c
    check(f"s={s}: mu_c >= lam_c q(mu_c)  [so ||C||_1 <= mu_c]", c1)
    check(f"s={s}: 2 lam_c q'(mu_c) < 1   [gap >= Delta/2]", c2,
          f"(= {float(2*lam_c*qp(bup, mu_c)):.9f})")
    cert[s] = (lam_c, mu_c)
    print(f"  s={s}: lam_gap(float) = {lf:.8f};  CERTIFIED lam_c = {float(lam_c):.8f}, mu_c = {float(mu_c):.6e}")

# ------------------------------------------------------------------ S5 crude counting (comparison)
print("\n== S5 comparison: BDL-style COUNTING constants for s = 4 (no Cauchy-Schwarz) ==")
def crude(s, ratio):
    return [2 ** (s - 1)] + [2 ** k * 2 ** s * (s ** k + k * ratio * s ** (k - 1)) for k in range(1, 2 * s + 1)]
lc5, _ = lam_gap_float(crude(4, 5))
lc4, _ = lam_gap_float(crude(4, 4))
print(f"  16 sets, |M_j|<=5|M| (correct), factor 4, depth 8:   lam_gap = {lc5:.5f}")
print(f"  16 sets, |M_j|<=4|M| (prior reader; INVALID, see C4): lam_gap = {lc4:.5f}")
print(f"  sector Cauchy-Schwarz (used, S4):                     lam_gap = {float(cert[4][0]):.5f}")

# ------------------------------------------------------------------ S6 gauge dictionary
print("\n== S6 gauge-model thresholds (E10)-(E12);  gap >= x C_F/4 >= 3x/16 for x >= X_d ==")
def CF(N): return Fr(N * N - 1, 2 * N)
rows = []
for d in (2, 3, 4):
    m = d * (d - 1) // 2
    A_d = Fr(32, 3) * m                               # door E / i15 s.4
    for name, s, D in (("link", 4, 2 * (d - 1)), ("vertex", 3, Fr(3 * d * (d - 1), 2))):
        lam_c = cert[s][0]
        eps_c = lam_c / D                              # (E10): per-plaquette normalized coupling
        Xu = sqrt(float(Fr(32, 3) * D / lam_c))        # (E11) uniform in N, b_N <= 2N
        theta = 2 * m * lam_c / D                      # (E12)
        XdoorE = max(1.0, sqrt(float(2 * A_d / theta)))
        rows.append((d, name, s, D, eps_c, Xu, theta, XdoorE))
print("  d  grouping  s  D     eps_c=2eps_0   eps_0(BDL conv.)   X_d(uniform)  theta_equiv   doorE-formula X_d")
for d, name, s, D, eps_c, Xu, theta, XE in rows:
    print(f"  {d}  {name:8s}  {s}  {float(D):4.1f}  {float(eps_c):.6e}   {float(eps_c)/2:.6e}      "
          f"{Xu:8.3f}      {float(theta):.6e}  {XE:8.3f}")
    check(f"d={d} {name}: door-E formula with theta_equiv reproduces X_d", abs(Xu - XE) < 1e-9 * Xu)
best = {}
for d in (2, 3, 4):
    best[d] = min(r[5] for r in rows if r[0] == d)
print("  BEST (min over the two rigorous groupings), N-uniform, all 0 <= b_N <= 2N:")
for d in (2, 3, 4):
    print(f"    X_{d} = {best[d]:.2f}   (gap >= 3x/16 >= {3*best[d]/16:.2f} at threshold)")

print("\n  N- and b_N-dependent thresholds X_d(N) = sqrt((2 b_N/C_F) D / lam_c), link grouping:")
print("   d   b_N    N=2      N=3      N=4      N=5      N=10     N->inf")
for d in (2, 3, 4):
    D = 2 * (d - 1); lam_c = cert[4][0]
    for bname, bfun in (("2", lambda N: 2), ("N", lambda N: N), ("2N", lambda N: 2 * N)):
        vals = []
        for N in (2, 3, 4, 5, 10):
            vals.append(sqrt(float(2 * bfun(N) / CF(N) * D / lam_c)))
        lim = {"2": 0.0, "N": sqrt(float(4 * D / lam_c)), "2N": sqrt(float(8 * D / lam_c))}[bname]
        print(f"   {d}   {bname:3s} " + " ".join(f"{v:8.2f}" for v in vals) + f" {lim:8.2f}")
# sup over N of 2 b_N / C_F with b_N = 2N is 32/3 at N = 2
check("sup_N 8N^2/(N^2-1) = 32/3 attained at N=2 (uniform constant)",
      all(Fr(8 * N * N, N * N - 1) <= Fr(32, 3) for N in range(2, 500)))

print("\n  comparison with registered expectations:")
print("   i15/PROOF.md s.4: 'No numerical value of X_d, particularly X_d<=2 or X_d<=8, is established'")
print(f"     -> this route: X_2={best[2]:.1f}, X_3={best[3]:.1f}, X_4={best[4]:.1f}; x>=2 / x>=8 windows NOT reached")
print("   door E hypothetical theta=1e-2 row: X_2~46.2, X_3~80, X_4~113 (labelled hypothetical there)")
print("   door G CONDITIONAL (on unproved (D)): X_2~53, X_3~274, X_4~1318")

print("\nALL CHECKS PASSED" if ok else "\nSOME CHECK FAILED")
