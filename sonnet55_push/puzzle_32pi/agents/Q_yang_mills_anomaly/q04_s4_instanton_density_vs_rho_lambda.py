#!/usr/bin/env python3
"""q04: classical Yang-Mills action/energy density of the BPST instanton and of the S^4 spin-connection instanton against
rho_Lambda = 3/(8 pi G L^2)  (c = 1, hbar explicit), and what the gauge-gravity identification 1/g^2 = L^2/(16 pi hbar G) implies.

  D1  S^4(L) in stereographic coordinates e^a = Omega dx^a, Omega = 2L/(1+r^2): spin connection omega^{ab} = d_b ln Omega dx^a - d_a ln Omega dx^b,
      torsion-free, R^{ab} = e^a e^b/L^2 (256 components).  SU(2)_pm connection A^i = -(1/2) eta^i_{ab} omega^{ab} (eta / eta-bar) IS the BPST
      field of size 1 in the stereographic chart, F^i = -4 eta^i/(1+r^2)^2, and |F|^2_phys = g^{mr}g^{ns}F F = 12/L^4 (constant), Int = 32 pi^2.
  D2  Euclidean action density (hbar/(4 g^2))|F|^2 over rho_Lambda:  R_pm = 8 pi hbar G/(g^2 L^2) per chirality.
      With 1/g^2 = k_g L^2/(16 pi hbar G):  R_pm = k_g/2, pair R = k_g.  k_g = 1 (the matching of S_dS = 2 x 8 pi^2/g^2) gives R_pm = 1/2, R_pair = 1.
  D3  flat-space BPST core density over rho_Lambda = 128 pi hbar G L^2/(g^2 rho^4) -> 8 (L/rho)^4 (k_g = 1); rho = 2L (the S^4 centre) gives 1/2 again.
  D4  The Euclidean stress tensor of the (anti)self-dual S^4 field vanishes (conformal covariance): the 'energy density' T_00 is ZERO; the comparable
      quantity is the action density.  The anomaly (one-loop) vacuum energy of the SAME instanton pair is |eps|/rho_L = b0 Pi_2/(6 pi) ~ 1e-123 b0.
  D5  Where a '4' can appear: hbar(|F_+|^2+|F_-|^2)/g^2 = 4 rho_Lambda (pair) exactly if the Lagrangian's 1/4 is omitted -- a convention, not a result.
Controls/mutations ('MUT') must fail the claim they attack.
"""
import sys, math, itertools
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

pi = sp.pi
L = sp.symbols('L', positive=True)
x = sp.symbols('x1:5', real=True)
r2 = sum(xi**2 for xi in x)
Om = 2 * L / (1 + r2)
phi = sp.log(Om)
dphi = [sp.diff(phi, xi) for xi in x]

# ------------------------------------------------------------------ D1: spin connection of S^4 and its curvature
# omega^{ab}_mu = d_b phi delta^a_mu - d_a phi delta^b_mu
def omega(a, b, m):
    return dphi[b] * (1 if a == m else 0) - dphi[a] * (1 if b == m else 0)
W = [[[sp.simplify(omega(a, b, m)) for m in range(4)] for b in range(4)] for a in range(4)]
# torsion-free: d e^a + omega^a_b ^ e^b = 0 in components: (d e^a)_{mn} = d_m e^a_n - d_n e^a_m ; (omega^a_b ^ e^b)_{mn} = omega^{ab}_m e^b_n - omega^{ab}_n e^b_m
e = lambda a, m: Om * (1 if a == m else 0)
tors = 0
for a in range(4):
    for m in range(4):
        for n in range(4):
            val = sp.diff(e(a, n), x[m]) - sp.diff(e(a, m), x[n]) + sum(W[a][b][m] * e(b, n) - W[a][b][n] * e(b, m) for b in range(4))
            tors += sp.simplify(val) != 0
chk("D1 omega^{ab} is torsion-free for e^a = Omega dx^a, Omega = 2L/(1+r^2) (mismatches %d of 64)" % tors, tors == 0)
Rcurv = [[[[None]*4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
bad = 0
for a in range(4):
    for b in range(4):
        for m in range(4):
            for n in range(4):
                val = sp.diff(W[a][b][n], x[m]) - sp.diff(W[a][b][m], x[n]) + sum(W[a][c][m] * W[c][b][n] - W[a][c][n] * W[c][b][m] for c in range(4))
                Rcurv[a][b][m][n] = sp.simplify(val)
                target = (Om**2 / L**2) * ((1 if (a == m and b == n) else 0) - (1 if (a == n and b == m) else 0))
                bad += sp.simplify(Rcurv[a][b][m][n] - target) != 0
chk("D1 R^{ab} = e^a e^b/L^2 on all 256 components (mismatches %d): the round S^4 of radius L" % bad, bad == 0)

def eta(i, a, b, bar=False):
    if a <= 2 and b <= 2:
        return sp.LeviCivita(i + 1, a + 1, b + 1)
    s = -1 if bar else 1
    if b == 3 and a <= 2:
        return s * (1 if a == i else 0)
    if a == 3 and b <= 2:
        return -s * (1 if b == i else 0)
    return 0

def su2_connection(bar):
    return [[sp.simplify(-sp.Rational(1, 2) * sum(eta(i, a, b, bar) * W[a][b][m] for a in range(4) for b in range(4))) for m in range(4)] for i in range(3)]
def su2_curv(A):
    F = [[[None]*4 for _ in range(4)] for _ in range(3)]
    for i in range(3):
        for m in range(4):
            for n in range(4):
                val = sp.diff(A[i][n], x[m]) - sp.diff(A[i][m], x[n])
                for j in range(3):
                    for k in range(3):
                        ee = sp.LeviCivita(i + 1, j + 1, k + 1)
                        if ee != 0:
                            val += ee * A[j][m] * A[k][n]
                F[i][m][n] = sp.simplify(val)
    return F
res = {}
for bar in (False, True):
    A = su2_connection(bar)
    # BPST regular gauge: A = 2 eta x/(1+r^2)   (rho = 1)
    bpst = [[2 * sum(eta(i, m, n, bar) * x[n] for n in range(4)) / (1 + r2) for m in range(4)] for i in range(3)]
    same = all(sp.simplify(A[i][m] - bpst[i][m]) == 0 for i in range(3) for m in range(4))
    F = su2_curv(A)
    cur_ok = all(sp.simplify(F[i][m][n] + 4 * eta(i, m, n, bar) / (1 + r2)**2) == 0 for i in range(3) for m in range(4) for n in range(4))
    F2phys = sp.simplify(sum(F[i][m][n]**2 for i in range(3) for m in range(4) for n in range(4)) / Om**4)   # g^{mr}g^{ns} = Omega^-4 delta delta
    # comparison with the SU(2) part of the Riemann curvature: F^i = -(1/2) eta^i_{ab} R^{ab}
    Rproj = all(sp.simplify(F[i][m][n] + sp.Rational(1, 2) * sum(eta(i, a, b, bar) * Rcurv[a][b][m][n] for a in range(4) for b in range(4))) == 0 for i in range(3) for m in range(4) for n in range(4))
    res[bar] = (same, cur_ok, F2phys, Rproj)
    lab = "SU(2)_-" if bar else "SU(2)_+"
    chk("D1 %s: A^i = -(1/2) eta^i_{ab} omega^{ab} equals the BPST regular-gauge field 2 eta x/(1+r^2) (size 1 in the chart)" % lab, same)
    chk("D1 %s: F^i = -4 eta^i/(1+r^2)^2 = -(1/2) eta^i_{ab} R^{ab} (curvature of the projected connection = projection of the Riemann curvature)" % lab, cur_ok and Rproj)
    chk("D1 %s: |F|^2_phys = g^{mr}g^{ns} F^i_mn F^i_rs = 12/L^4 (constant on S^4)" % lab, sp.simplify(F2phys - 12 / L**4) == 0)
rr = sp.symbols('rr', positive=True)
vol4 = sp.simplify(2 * pi**2 * sp.integrate((2 * L / (1 + rr**2))**4 * rr**3, (rr, 0, sp.oo)))
chk("D1 Vol(S^4_L) = 8 pi^2 L^4/3", sp.simplify(vol4 - sp.Rational(8, 3) * pi**2 * L**4) == 0)
chk("D1 Int |F|^2 sqrt(g) d^4x = (12/L^4)(8 pi^2 L^4/3) = 32 pi^2 per chirality (k = 1, same unit as R^4)", sp.simplify(12 / L**4 * vol4 - 32 * pi**2) == 0)
# MUT: a wrong projection normalisation (A = -eta omega, no 1/2) is not the BPST field
Amut = [[sp.simplify(-sum(eta(i, a, b, False) * W[a][b][m] for a in range(4) for b in range(4))) for m in range(4)] for i in range(3)]
bpst0 = [[2 * sum(eta(i, m, n, False) * x[n] for n in range(4)) / (1 + r2) for m in range(4)] for i in range(3)]
chk("MUT D1 without the 1/2 in A = -(1/2) eta omega the connection is NOT BPST (factor 2), rejected", not all(sp.simplify(Amut[i][m] - bpst0[i][m]) == 0 for i in range(3) for m in range(4)))

# ------------------------------------------------------------------ D2: density ratios
g, hb, G, kg = sp.symbols('g hbar G k_g', positive=True)
s_pm = hb / (4 * g**2) * 12 / L**4                      # Euclidean action density per chirality
rho_L = 3 / (8 * pi * G * L**2)                          # c = 1
R_pm = sp.simplify(s_pm / rho_L)
chk("D2 per-chirality YM action density over rho_Lambda:  R_pm = 8 pi hbar G/(g^2 L^2)", sp.simplify(R_pm - 8 * pi * hb * G / (g**2 * L**2)) == 0)
MM = {g: sp.sqrt(16 * pi * hb * G / (kg * L**2))}        # 1/g^2 = k_g L^2/(16 pi hbar G)
R_pm_k = sp.simplify(R_pm.subs(MM)); R_pair_k = sp.simplify(2 * R_pm_k)
chk("D2 with 1/g^2 = k_g L^2/(16 pi hbar G):  R_pm = k_g/2 and R_pair = k_g (hbar and G cancel)", sp.simplify(R_pm_k - kg / 2) == 0 and sp.simplify(R_pair_k - kg) == 0)
chk("D2 lane-A matching (k_g = 1: total instanton action 2 x 8 pi^2/g^2 = S_dS/hbar = pi L^2/(hbar G)):  R_pm = 1/2, R_pair = 1",
    sp.simplify(2 * sp.Rational(1, 4) * 32 * pi**2 / g**2 - pi * L**2 / (hb * G)).subs(MM).subs(kg, 1) == 0 and R_pm_k.subs(kg, 1) == sp.Rational(1, 2) and R_pair_k.subs(kg, 1) == 1)
# the Euclidean EH on-shell Lagrangian density is exactly rho_Lambda: -(R-2Lambda)/(16 pi G), R = 12/L^2, Lambda = 3/L^2
Rsc, Lmb = 12 / L**2, 3 / L**2
chk("D2 EH on-shell action density |(R-2 Lambda)|/(16 pi G) = Lambda/(8 pi G) = rho_Lambda on S^4  (so R_pair = 1 is S_dS = 2 x 8 pi^2/g^2 restated: an identity)", sp.simplify((Rsc - 2 * Lmb) / (16 * pi * G) - rho_L) == 0)
print("     -> the ratio is NOT an independent number: k_g is CHOSEN so that the instanton action equals S_dS; R_pair = k_g = 1 by that choice (lane A: chi = 2).")
# MUT: one-chirality matching (k_g = 2) gives R_pm = 1, R_pair = 2 -- a different convention, different number
chk("MUT D2 matching only ONE chirality's action to S_dS (k_g = 2) gives R_pm = 1, R_pair = 2: the ratio is convention, not physics", R_pm_k.subs(kg, 2) == 1 and R_pair_k.subs(kg, 2) == 2)
chk("D2 the ratio never equals 4 or 1/4 for the natural matchings k_g in {1, 2}: values (1/2, 1, 1, 2)", {R_pm_k.subs(kg, 1), R_pair_k.subs(kg, 1), R_pm_k.subs(kg, 2), R_pair_k.subs(kg, 2)} == {sp.Rational(1, 2), 1, 2} and all(v not in (4, sp.Rational(1, 4)) for v in (R_pm_k.subs(kg, 1), R_pair_k.subs(kg, 1), R_pm_k.subs(kg, 2), R_pair_k.subs(kg, 2))))
# generic coupling: hbar-full and ~1e-121
Pi2 = 2.85e-122          # hbar G Lambda_cc/c^3 (q03, H0 = 67.4)
g2_MM = 16 * math.pi / 3 * Pi2
print("     Pi_2 = 3 hbar G/L^2 = %.2e ; MM coupling g^2 = (16 pi/3) Pi_2 = %.2e ; for a generic g^2 = 0.1 the same S^4 field has R_pm = (8 pi/3) Pi_2/g^2 = %.2e" % (Pi2, g2_MM, 8 * math.pi / 3 * Pi2 / 0.1))
chk("D2 for an ordinary O(0.1-1) gauge coupling the classical instanton density is ~1e-121 to 1e-120 of rho_Lambda (hbar-full ratio 8 pi hbar G/(g^2 L^2)); only g^2 ~ hbar G/L^2 makes it O(1)  [first version of this bound was mis-set by me: 2.4e-120 vs 1e-120]", 1e-122 < 8 * math.pi / 3 * Pi2 / 1.0 < 1e-120 < 8 * math.pi / 3 * Pi2 / 0.1 < 1e-119 and g2_MM < 1e-119)
# D2': the energy of the running: b0 g^2/(8 pi^2) at the MM coupling
chk("D2 at the MM coupling the one-loop running b0 g^2/(8 pi^2) is ~1e-122 b0: no dimensional transmutation, exp(-8 pi^2/(b0 g^2)) = exp(-1e121)", 8 * math.pi**2 / g2_MM > 1e120)

# ------------------------------------------------------------------ D3: flat-space BPST core density
rho_, rr2 = sp.symbols('rho_inst rr2', positive=True)
s_core = hb / (4 * g**2) * 192 * rho_**4 / (0 + rho_**2)**4          # at x = 0
ratio_core = sp.simplify(s_core / rho_L)
chk("D3 BPST (flat R^4, size rho) action density at the centre 48 hbar/(g^2 rho^4); over rho_Lambda:  128 pi hbar G L^2/(g^2 rho^4)", sp.simplify(ratio_core - 128 * pi * hb * G * L**2 / (g**2 * rho_**4)) == 0)
core_MM = sp.simplify(ratio_core.subs(MM).subs(kg, 1))
chk("D3 with k_g = 1: core ratio = 8 (L/rho)^4", sp.simplify(core_MM - 8 * (L / rho_)**4) == 0)
chk("D3 rho = 2L (the size that matches the S^4 centre: physical scale factor Omega(0) = 2L) gives 1/2 = R_pm (consistency between the flat BPST and the S^4 field)", sp.simplify(core_MM.subs(rho_, 2 * L)) == sp.Rational(1, 2))
sol4 = sp.solve(sp.Eq(core_MM.subs(L, 1), 4), rho_); sol14 = sp.solve(sp.Eq(core_MM.subs(L, 1), sp.Rational(1, 4)), rho_)
print("     core ratio = 4 needs rho = %s L ; = 1/4 needs rho = %s L (no symmetry marks either: lane A a03)" % (sol4, sol14))
chk("MUT D3 rho = L (instead of 2L) would give 8, not the S^4 value: the size matching is rejected by the check", sp.simplify(core_MM.subs(rho_, L)) == 8)

# ------------------------------------------------------------------ D4: stress tensor and the one-loop energy of the same instanton
F_plus = su2_curv(su2_connection(False))
gmet = Om**2
T = [[sp.simplify(sum(F_plus[i][m][p] * F_plus[i][n][p] for i in range(3) for p in range(4)) / Om**2 - (sp.Rational(1, 4) * Om**2 * sum(F_plus[i][a][b]**2 for i in range(3) for a in range(4) for b in range(4)) / Om**4 if m == n else 0)) for n in range(4)] for m in range(4)]
chk("D4 Euclidean stress tensor of the S^4 SU(2)_+ field, T_mn = g^{rs}F_mr F_ns - (1/4) g_mn |F|^2, vanishes identically (all 16 components): zero energy density, no back-reaction", all(t == 0 for row in T for t in row))
b0 = sp.symbols('b0', positive=True)
eps_anom = -(b0 / (128 * pi**2)) * hb * 24 / L**4        # eps = -(b0/(128 pi^2)) <F^2_geo>, pair: 12 + 12 per L^4
Pi2s = sp.symbols('Pi_2', positive=True)
rat = sp.simplify(sp.Abs(eps_anom) / rho_L)
chk("D4 the one-loop anomaly vacuum energy of the same S^4 instanton pair: |eps|/rho_Lambda = b0 hbar G/(2 pi L^2) = b0 Pi_2/(6 pi)  (Pi_2 = 3 hbar G/L^2)", sp.simplify(rat - b0 * hb * G / (2 * pi * L**2)) == 0 and sp.simplify(rat.subs(hb, Pi2s * L**2 / (3 * G)) - b0 * Pi2s / (6 * pi)) == 0)
print("     |eps_anom|/rho_Lambda = b0 Pi_2/(6 pi) = %.2e b0 (loop order hbar^1 relative to the classical hbar^0 identity; lane A's classicality theorem)" % (Pi2 / (6 * math.pi)))
chk("D4 that ratio is ~1e-123 b0, nowhere near 1/4 or 4 unless b0 ~ 1e122", Pi2 / (6 * math.pi) < 1e-122)

# ------------------------------------------------------------------ D5: where a 4 can appear
noquarter = hb / g**2 * 24 / L**4 / rho_L              # both chiralities, Lagrangian WITHOUT the 1/4
chk("D5 hbar(|F_+|^2+|F_-|^2)/g^2 (Lagrangian 1/4 omitted) = 4 rho_Lambda exactly at k_g = 1: a '4' from a normalisation convention", sp.simplify(noquarter.subs(MM).subs(kg, 1)) == 4)
chk("MUT D5 with the correct 1/4 the same comparison gives 1, so the '4' is the inverse Lagrangian normalisation, not a derived ratio", sp.simplify(noquarter.subs(MM).subs(kg, 1) / 4) == 1)
print("\nsummary: same instanton for gauge and gravity: YM action density/rho_Lambda = 1/2 per chirality, 1 for the pair, by the definition of 1/g^2 (S_dS = 2 x 8 pi^2/g^2).")
print("         It is not 4 or 1/4. The puzzle's a0^2/(G rho_Lambda) = 1/4 = a0^2/(G s_pair) has no place in it: a0 is not in the gauge theory.")
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
