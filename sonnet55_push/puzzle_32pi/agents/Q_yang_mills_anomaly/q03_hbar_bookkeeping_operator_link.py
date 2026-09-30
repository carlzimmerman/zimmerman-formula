#!/usr/bin/env python3
"""q03: where hbar cancels (and where it does not) when the vacuum energy is a hidden Yang-Mills sector; principles P1, P2, P5.

  C1  Buckingham analysis of (G, rho_E, a0, hbar, c): exactly two dimensionless groups; a0 enters only Pi_A = a0^2/(G rho_E)
      (no hbar, no c), hbar enters only Pi_B = rho_E hbar G^2/c^7 = rho_E/rho_Planck.  The puzzle is Pi_A = 1/4.
  C2  rho_E = c_vac Lambda_YM^4/(hbar c)^3  =>  a0 = (sqrt(c_vac)/2) c Lambda_YM^2/(hbar E_P), a0 ~ hbar^(-3/2) at fixed
      (Lambda_YM, G, c), Pi_B = c_vac (Lambda_YM/E_P)^4, and Pi_2 = hbar G Lambda_cc/c^3 = 8 pi Pi_B.  Numbers at the observed rho_Lambda.
  C3  P1 sector independence: with a0 defined from rho the ratio Pi_A is independent of every YM datum (symbolic derivatives = 0).
      P5 control: an a0 tied to another YM operator has an N-dependent ratio; only universal numbers (trace, w, SEC) are N-free.
  C4  P2 trace reading: in a Lorentz-invariant vacuum rho, |T|/4, |rho+3p|/2 are the same number (so 1/D cannot be told from the
      others by any YM vacuum computation); off-vacuum the three readings differ.  1/sqrt(d+1) is one more function = 1/2 at d = 3.
Controls/mutations ('MUT') must fail the claim they attack.
"""
import sys, math
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ------------------------------------------------------------------ C1  Buckingham
# dimension vectors over (M, L, T)
dims = {
    'G':    (-1, 3, -2),
    'rhoE': (1, -1, -2),      # energy density
    'a0':   (0, 1, -2),
    'hbar': (1, 2, -1),
    'c':    (0, 1, -1),
}
names = list(dims)
Mx = sp.Matrix([[dims[n][i] for n in names] for i in range(3)])
ns = Mx.nullspace()
chk("C1 rank of the dimension matrix is 3, so (G, rho_E, a0, hbar, c) has exactly 5-3 = 2 dimensionless groups", Mx.rank() == 3 and len(ns) == 2)
def vec(**kw):
    return sp.Matrix([kw.get(n, 0) for n in names])
PiA = vec(a0=2, G=-1, rhoE=-1)
PiB = vec(rhoE=1, hbar=1, G=2, c=-7)
chk("C1 Pi_A = a0^2/(G rho_E) is dimensionless and contains no hbar and no c", (Mx * PiA).is_zero_matrix and PiA[names.index('hbar')] == 0 and PiA[names.index('c')] == 0)
chk("C1 Pi_B = rho_E hbar G^2/c^7 (= rho_E/rho_Planck) is dimensionless and contains no a0", (Mx * PiB).is_zero_matrix and PiB[names.index('a0')] == 0)
chk("C1 the two groups are independent and span the null space (a0 appears in Pi_A only)", sp.Matrix.hstack(PiA, PiB).rank() == 2 and sp.Matrix.hstack(PiA, PiB, *ns).rank() == 2)
# MUT: a group that mixes a0 and hbar cannot be dimensionless unless it is a combination of Pi_A, Pi_B
bad = vec(a0=2, hbar=1)
chk("MUT C1 a0^2 hbar alone is not dimensionless (a0 cannot pair with hbar without G rho_E)", not (Mx * bad).is_zero_matrix)

# ------------------------------------------------------------------ C2  YM substitution
G, hb, cc, Lam, cvac = sp.symbols('G hbar c Lambda c_vac', positive=True)
rhoE = cvac * Lam**4 / (hb * cc)**3
E_P = sp.sqrt(hb * cc**5 / G)
a0 = sp.sqrt(G * rhoE) / 2
a0_form = sp.sqrt(cvac) / 2 * cc * Lam**2 / (hb * E_P)
chk("C2 a0 = (1/2) sqrt(G rho_E) = (sqrt(c_vac)/2) c Lambda_YM^2/(hbar E_P)  (symbolic)", sp.simplify(a0 - a0_form) == 0)
chk("C2 a0 ~ hbar^(-3/2) at fixed (Lambda_YM, G, c)", sp.simplify(sp.diff(sp.log(a0), hb) * hb + sp.Rational(3, 2)) == 0)
rho_P = cc**7 / (hb * G**2)
Pi2 = hb * G * (8 * sp.pi * G * rhoE / cc**4) / cc**3          # Pi_2 = hbar G Lambda_cc / c^3 with Lambda_cc = 8 pi G rho_E/c^4
chk("C2 Pi_2 = hbar G Lambda_cc/c^3 = 8 pi rho_E/rho_P = 8 pi c_vac (Lambda_YM/E_P)^4", sp.simplify(Pi2 - 8 * sp.pi * cvac * (Lam / E_P)**4) == 0 and sp.simplify(Pi2 - 8 * sp.pi * rhoE / rho_P) == 0)
Pi1 = a0**2 / (cc**4 * (8 * sp.pi * G * rhoE / cc**4))         # a0^2/(c^4 Lambda_cc)
chk("C2 Pi_1 = a0^2/(c^4 Lambda_cc) = 1/(32 pi) for every c_vac, Lambda_YM, hbar (the hbar-free classical coefficient)", sp.simplify(Pi1 - 1 / (32 * sp.pi)) == 0)

# numbers (SI): Planck-2018-like  H0 = 67.4 km/s/Mpc, Omega_L = 0.685
Gv, hv, cv = 6.67430e-11, 1.054571817e-34, 299792458.0
Mpc = 3.0856775814913673e22
def numbers(H0kms, OL):
    H0 = H0kms * 1e3 / Mpc
    rho = OL * 3 * H0**2 * cv**2 / (8 * math.pi * Gv)            # J/m^3
    a0v = 0.5 * math.sqrt(Gv * rho)
    rhoP = cv**7 / (hv * Gv**2)
    EP = math.sqrt(hv * cv**5 / Gv)
    Lam_J = (rho * (hv * cv)**3)**0.25                            # c_vac = 1
    return rho, a0v, rho / rhoP, 8 * math.pi * rho / rhoP, Lam_J / 1.602176634e-19, EP / 1.602176634e-19
for H0kms, OL in ((67.4, 0.685), (73.0, 0.70)):
    rho, a0v, PB, P2, Lam_eV, EP_eV = numbers(H0kms, OL)
    print("     H0=%.1f Omega_L=%.3f: rho_E = %.3e J/m^3, a0 = 0.5 sqrt(G rho) = %.3e m/s^2, Pi_B = rho/rho_P = %.2e, Pi_2 = 8 pi Pi_B = %.2e, Lambda_YM(c_vac=1) = %.2e eV, E_P = %.3e eV"
          % (H0kms, OL, rho, a0v, PB, P2, Lam_eV, EP_eV))
    a0_YM = 0.5 * cv * (Lam_eV * 1.602176634e-19)**2 / (hv * (EP_eV * 1.602176634e-19))     # (1/2) c Lambda^2/(hbar E_P), c_vac = 1
    chk("C2 numbers H0=%.1f: a0 = (1/2) c Lambda_YM^2/(hbar E_P) reproduces 0.5 sqrt(G rho) to 1e-12 (c_vac = 1)" % H0kms, abs(a0_YM / a0v - 1) < 1e-12)
    chk("C2 numbers H0=%.1f: Lambda_YM ~ sqrt(H M_P)-type seesaw scale, 2-3 meV; Pi_2 ~ 3e-122 (agrees with lane A)" % H0kms, 1e-3 < Lam_eV < 5e-3 and 1e-122 < P2 < 1e-121)

# ------------------------------------------------------------------ C3  P1 sector independence and the P5 control
N_, nf_, gg, LamYM, cv_, b0s, mu_ = sp.symbols('N nf g Lambda_YM c_vac b0 mu', positive=True)
Gs = sp.symbols('G', positive=True)
rho_sector = cv_ * LamYM**4
a0_grav = sp.sqrt(Gs * rho_sector) / 2                         # a0 defined gravity-side from rho (the puzzle)
ratio_A = sp.simplify(a0_grav**2 / (Gs * rho_sector))
chk("C3 P1: with a0 defined from rho the ratio Pi_A = 1/4 and d/dLambda_YM = d/dc_vac = d/dN = d/db0 = d/dg = 0", ratio_A == sp.Rational(1, 4) and all(sp.diff(ratio_A, v) == 0 for v in (LamYM, cv_, N_, b0s, gg)))
print("     (P1 is true by construction: it is the statement that the sector enters only through rho; the content is what would HAVE to differ.)")
# P5 control: a0^2 = C G <O> with O another YM operator; <O>/eps from B3/B4: O = (alpha/pi)G^2: eps = -(b0/32) <O>; O = n: eps = -(b0/4) n
def b0_pure(N):
    return sp.Rational(11, 3) * N
Cs = sp.symbols('C')
vals = {}
for Nc in (2, 3, 4, 5):
    b0v = b0_pure(Nc)
    # a0^2/(G eps) = C * <O>/eps  (magnitudes)
    vals[Nc] = (sp.Rational(32) / b0v, sp.Rational(4) / b0v)      # |<(alpha/pi)G^2>/eps|, |n/eps|
Cneeded = {Nc: (sp.Rational(1, 4) / v[0], sp.Rational(1, 4) / v[1]) for Nc, v in vals.items()}
print("     C needed for Pi_A = 1/4:  O=(alpha/pi)G^2: " + ", ".join("N=%d: %s" % (n_, str(c[0])) for n_, c in Cneeded.items()) + " ; O=n: " + ", ".join("N=%d: %s" % (n_, str(c[1])) for n_, c in Cneeded.items()))
chk("C3 P5 control: tying a0^2 to <(alpha/pi)G^2> or to the instanton density n needs an N-dependent coefficient C (b0/128 resp. b0/16); a universal C cannot give Pi_A = 1/4 for all N",
    len({c[0] for c in Cneeded.values()}) == 4 and len({c[1] for c in Cneeded.values()}) == 4)
chk("C3 P5: those needed coefficients are b0/128 and b0/16 (rational multiples of the anomaly's own numbers, so still 'inserted')", all(Cneeded[N] == (b0_pure(N) / 128, b0_pure(N) / 16) for N in Cneeded))
# universal numbers of a Lorentz-invariant vacuum
rho_ = sp.symbols('rho', positive=True)
eta = sp.diag(-1, 1, 1, 1)                                   # mostly-plus metric
Tvac = -rho_ * eta
p_ = Tvac[1, 1]
trT = sum((eta.inv() * Tvac)[i, i] for i in range(4))
chk("C3 vacuum T_mn = -rho g_mn: p = -rho, T = -4 rho, rho+p = 0, rho+3p = -2 rho (all pure numbers, none YM-specific)",
    sp.simplify(p_ + rho_) == 0 and sp.simplify(trT + 4 * rho_) == 0 and sp.simplify(rho_ + 3 * p_ + 2 * rho_) == 0)

# ------------------------------------------------------------------ C4  P2 trace reading and the equation-of-state discriminator
Gs2 = sp.symbols('G', positive=True)
rd = lambda w: rho_                                         # reading R1: a0^2 = G rho/4
r1 = lambda w: Gs2 * rho_ / 4
r2 = lambda w: Gs2 * sp.Abs(rho_ * (3 * w - 1)) / 16       # reading R2: a0^2 = G |T|/16,  T = -(rho - 3p) = -rho(1-3w)
r3 = lambda w: Gs2 * sp.Abs(rho_ * (1 + 3 * w)) / 8         # reading R3: a0^2 = G |rho+3p|/8
vac = {r(-1) for r in (r1, r2, r3)}
chk("C4 in the vacuum (w = -1) the three readings coincide:  G rho/4 = G |T|/16 = G |rho+3p|/8", len({sp.simplify(r(-1)) for r in (r1, r2, r3)}) == 1)
tab = {}
for w, lab in ((0, 'dust'), (sp.Rational(1, 3), 'radiation'), (-1, 'vacuum')):
    tab[lab] = tuple(sp.simplify(r(w) / (Gs2 * rho_)) for r in (r1, r2, r3))
print("     a0^2/(G rho) under the three readings (R1: rho/4, R2: |T|/16, R3: |rho+3p|/8): " + "; ".join("%s: %s" % (k, tuple(str(x) for x in v)) for k, v in tab.items()))
chk("C4 off the vacuum the readings differ: dust (1/4, 1/16, 1/8), radiation (1/4, 0, 1/4)", tab['dust'] == (sp.Rational(1, 4), sp.Rational(1, 16), sp.Rational(1, 8)) and tab['radiation'] == (sp.Rational(1, 4), 0, sp.Rational(1, 4)))
chk("MUT C4 a wrong trace normalisation (|T|/8) does NOT coincide with R1 in the vacuum", sp.simplify(Gs2 * 4 * rho_ / 8 - r1(-1)) != 0)
# if a reading were applied to the TOTAL content (dust + vacuum) a0 would evolve: z = 2.5, Omega_m = 0.315, Omega_L = 0.685
Om, OL_, z = 0.315, 0.685, 2.5
rm = lambda zz: Om * (1 + zz)**3
R1z = OL_ / 4 / (OL_ / 4)                                   # vacuum only: flat
R2z = ((rm(z) * 1 / 16 + OL_ * 4 / 16) / (Om / 16 + OL_ * 4 / 16))
R3z = abs(rm(z) - 2 * OL_) / abs(Om - 2 * OL_)            # rho+3p: dust +rho_m, vacuum -2 rho_L (opposite signs; my first version added magnitudes: fixed)
print("     a0^2(z=2.5)/a0^2(0): R1 (vacuum only) %.3f ; R2 total trace %.3f ; R3 total SEC %.3f  [illustration of the discriminator, not a data comparison]" % (R1z, R2z, R3z))
chk("C4 applied to the total content the trace/SEC readings make a0 grow with z (x%.1f, x%.1f in a0^2 at z=2.5), the opposite of the flat law: so the 1/D reading would have to be restricted to the vacuum sector by hand" % (R2z, R3z), R2z > 2 and R3z > 2)
# the d-dependence
d = sp.symbols('d', positive=True)
kap = 1 / sp.sqrt(d + 1)
chk("C4 the trace reading kappa(d) = 1/sqrt(d+1) equals 1/2 at d = 3 and only there (one more function through (3, 1/2))", sp.solve(sp.Eq(kap, sp.Rational(1, 2)), d) == [3])
print("     kappa_trace(d=2,3,4,5) = " + ", ".join("%.4f" % float(kap.subs(d, k)) for k in (2, 3, 4, 5)))
chk("MUT C4 kappa = 1/d equals 1/2 at d = 2, not 3: the mutated formula is rejected by the d=3 anchor", sp.solve(sp.Eq(1 / d, sp.Rational(1, 2)), d) != [3])

print("\nsummary: hbar cancels in Pi_A exactly because rho_E is an energy density (G rho_E = acceleration^2); the YM sector lives in Pi_B (hbar-full, ~1e-123).")
print("         The sector cannot reach Pi_A (P1). The only sector-independent numbers it can pass are vacuum numbers (trace 4, w, SEC): P2 is a rewriting.")
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
