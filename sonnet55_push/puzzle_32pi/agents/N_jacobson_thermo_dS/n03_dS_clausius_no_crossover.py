#!/usr/bin/env python3
"""n03_dS_clausius_no_crossover.py -- the Clausius relation with the exact de Sitter temperature: does an acceleration scale appear?

Units c = hbar = k_B = 1, G kept.  N = sqrt(f0) is the lapse of the static patch at the observer; theta: sin(theta) = H r0, tan(theta) = a/H.
C1  a mass m held at rest at r0 has Killing energy E_K = m N; the local temperature is T_loc = T_H/N (Tolman = Deser-Levin, n01).
    The entropy it carries across the horizon is  Delta S = E_K/T_H = m/T_loc = 2 pi L m N:  the acceleration enters T and E_K with the SAME Tolman factor.
C2  exact first law of the (Schwarzschild-)de Sitter horizons with S = A/(4G), T = kappa/(2 pi):  dM = +T_b dS_b (black hole), dM = -T_c dS_c (cosmological).
    This pins the '4' independently of the '2 pi' (n02 B2d).  Controls: S = A/(2G) and T = kappa/pi fail.
C3  entropic force in exact de Sitter:  F = T_loc dS_c/dl  with S_c(r0) = S_dS - E_K(r0)/T_H  equals  m a  EXACTLY, for all a/H.
    The naive Verlinde-type F = 2 pi m T_loc = m sqrt(a^2+H^2) = m a / sin(theta) is NOT m a  (that is the mismatch).
C4  same in Schwarzschild-de Sitter: F = T_loc dS/dl = -m f'/(2 sqrt f) = the free-fall acceleration of GR (Newton + cosmological repulsion).
C5  Jacobson chain with the heat normalised by kappa_h and the temperature by kappa_T:  R_kk = 8 pi G (kappa_h/kappa_T) T_kk.
    Consistent bookkeeping (kappa_h = kappa_T, any normalisation) => G_eff = G for every theta: NO crossover.  The six mismatched pairs are tabulated with limits.
Exit 0 = all pass.
"""
import sys
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")
def must_fail(name, cond):
    ok.append(not bool(cond)); print(f"  [{'OK' if not cond else 'FAIL'}] CONTROL (wrong claim must be rejected): {name}")

H, r0, m, G, Mm, rc = sp.symbols('H r0 m G M r_c', positive=True)
L = 1 / H
N0 = sp.sqrt(1 - H**2 * r0**2)
a_st = H**2 * r0 / N0                       # proper acceleration (n01 A1)
A5 = H / N0                                 # = kappa_obs = sqrt(a^2 + H^2) (n01 A2/A5)
T_H = H / (2 * sp.pi)
T_loc = A5 / (2 * sp.pi)
sinth, costh = H * r0, N0

print("C1  Tolman cancellation")
E_K = m * N0
check("C1a T_loc = T_H / N", sp.simplify(T_loc - T_H / N0) == 0)
check("C1b Delta S = E_K/T_H = m/T_loc = 2 pi L m N   (the a-dependence cancels between energy and temperature)",
      sp.simplify(E_K / T_H - m / T_loc) == 0 and sp.simplify(E_K / T_H - 2 * sp.pi * L * m * N0) == 0)
must_fail("C1c Delta S = m/T_H (rest energy over the horizon temperature, i.e. ignoring the lapse)", sp.simplify(E_K / T_H - m / T_H) == 0)

print("C2  exact first law of the (S)dS horizons, S = A/4G, T = kappa/2pi (Killing vector d_t, f-normalisation: M is its energy)")
f = lambda rr, M_: 1 - 2 * G * M_ / rr - H**2 * rr**2
M_of_r = rc / (2 * G) * (1 - H**2 * rc**2)                    # f(r_c) = 0 solved for M
check("C2a f(r_c) = 0  <=>  M = r_c (1 - H^2 r_c^2)/(2G)", sp.simplify(f(rc, M_of_r)) == 0)
fp = sp.simplify(sp.diff(f(sp.Symbol('rho', positive=True), Mm), sp.Symbol('rho', positive=True)).subs(sp.Symbol('rho', positive=True), rc).subs(Mm, M_of_r))
kappa = fp / 2                                              # signed surface gravity f'(r_c)/2
S_c = sp.pi * rc**2 / G
# black-hole branch: dM = + T dS with T = f'/(4 pi) > 0;  cosmological branch: f' < 0, dM = - T dS with T = |f'|/(4 pi)
check("C2b  dM/dr_c = (f'/4pi) dS/dr_c   (signed: T = f'(r_c)/4pi;  f'>0 black hole, f'<0 cosmological => dM = -T_c dS_c)",
      sp.simplify(sp.diff(M_of_r, rc) - (fp / (4 * sp.pi)) * sp.diff(S_c, rc)) == 0)
check("C2c small-M cosmological horizon: dS_c/dM = -2 pi L = -1/T_H at M -> 0 (r_c -> L)",
      sp.simplify((sp.diff(S_c, rc) / sp.diff(M_of_r, rc)).subs(rc, L) + 2 * sp.pi * L) == 0)
check("C2d flat limit H -> 0: Schwarzschild dM = T dS with T = 1/(8 pi G M), S = 4 pi G M^2",
      sp.simplify((sp.diff(4 * sp.pi * G * Mm**2, Mm) / (8 * sp.pi * G * Mm)) - 1) == 0)
must_fail("C2e S = A/(2G) (wrong quarter):  dM = T dS", sp.simplify(sp.diff(M_of_r, rc) - (fp / (4 * sp.pi)) * sp.diff(2 * sp.pi * rc**2 / G, rc)) == 0)
must_fail("C2f T = kappa/pi (wrong Unruh 2 pi): dM = T dS", sp.simplify(sp.diff(M_of_r, rc) - (fp / (2 * sp.pi)) * sp.diff(S_c, rc)) == 0)

print("C3  entropic force in exact de Sitter with the exact temperature")
S_dS = sp.pi * L**2 / G
S_c_of_r0 = S_dS - E_K / T_H                                 # linear response, coefficient fixed by C2c
dS_dl = N0 * sp.diff(S_c_of_r0, r0)                          # dl = dr0 / N
F_ent = T_loc * dS_dl
check("C3a F = T_loc dS_c/dl = m a   for every r0 (every a/H)", sp.simplify(F_ent - m * a_st) == 0)
check("C3b in angle form: F = m kappa_obs sin(theta) = m a", sp.simplify(F_ent - m * A5 * sinth) == 0)
F_naive = 2 * sp.pi * m * T_loc                              # Verlinde-type: DeltaS = 2 pi m Delta x with the DL temperature
check("C3c naive F = 2 pi m T_loc = m sqrt(a^2+H^2) = m a / sin(theta) (>= m H even for a = 0)", sp.simplify(F_naive - m * A5) == 0 and sp.simplify(F_naive * sinth - m * a_st) == 0)
must_fail("C3d naive F equals m a", sp.simplify(F_naive - m * a_st) == 0)
xx = sp.symbols('x', positive=True)
check("C3e ratio F_naive/F = sqrt(1 + (H/a)^2) -> 1 for a >> H, -> infinity for a << H (a geodesic observer would feel a force m H)",
      sp.simplify((F_naive / F_ent).subs(r0, sp.solve(sp.Eq(a_st, xx * H), r0)[0]) - sp.sqrt(1 + 1 / xx**2)) == 0)

print("C4  same in Schwarzschild-de Sitter (Tolman with the cosmological-horizon temperature)")
rr, Tc = sp.symbols('rr T_c', positive=True)
fS = 1 - 2 * G * Mm / rr - H**2 * rr**2
NS = sp.sqrt(fS)
T_loc_S = Tc / NS
dS_dl_S = NS * sp.diff(-m * NS / Tc, rr)
F_S = T_loc_S * dS_dl_S
freefall = -sp.diff(fS, rr) / (2 * NS)                        # d^2 l/d tau^2 of a geodesic released at rest (from the geodesic equation), signed outward
check("C4a T_loc dS/dl = m * (free-fall proper acceleration, = -f'/(2 sqrt f))", sp.simplify(F_S - m * freefall) == 0)
check("C4b = m (H^2 r - GM/r^2)/sqrt(f): Newton + cosmological repulsion, no other term", sp.simplify(F_S - m * (H**2 * rr - G * Mm / rr**2) / NS) == 0)
must_fail("C4c T_loc dS/dl = m G M/r^2 only (drop the cosmological piece)", sp.simplify(F_S - m * (-G * Mm / rr**2)) == 0)

print("C5  Jacobson chain with separate normalisations for the heat (kappa_h) and the temperature (kappa_T)")
kh, kT, lam, lam0, Tkk, Rkk, Ap, hb = sp.symbols('kappa_h kappa_T lambda lambda_0 T_kk R_kk A_p hbar', positive=True)
dQ = sp.integrate(-kh * lam * Tkk, (lam, -lam0, 0)) * Ap
dA = sp.integrate(-lam * Rkk, (lam, -lam0, 0)) * Ap
Rsol = sp.solve(sp.Eq(dQ, (hb * kT / (2 * sp.pi)) * (1 / (4 * G * hb)) * dA), Rkk)[0]
Geff_over_G = sp.simplify(Rsol / (8 * sp.pi * G * Tkk))
check("C5a R_kk = 8 pi G (kappa_h/kappa_T) T_kk", sp.simplify(Geff_over_G - kh / kT) == 0)
th = sp.symbols('theta', positive=True)
kap = {'a': sp.tan(th), 'kobs': 1 / sp.cos(th), 'H': sp.Integer(1)}          # in units of H: a = tan(theta), kappa_obs = 1/cos(theta), kappa_xi = 1
check("C5b kappa_obs = a/sin(theta) in these units", sp.simplify(kap['kobs'] - kap['a'] / sp.sin(th)) == 0)
for nm in kap:
    check(f"C5c consistent bookkeeping kappa_h = kappa_T = kappa_{nm}: G_eff/G = 1 for ALL theta", sp.simplify(Geff_over_G.subs({kh: kap[nm], kT: kap[nm]}) - 1) == 0)
print("     mismatched pairs (heat normalisation, temperature normalisation): G_eff/G as a function of theta, limits at a >> H (theta->pi/2) and a << H (theta->0)")
rows = []
for h_, t_ in [('a', 'kobs'), ('a', 'H'), ('kobs', 'a'), ('kobs', 'H'), ('H', 'a'), ('H', 'kobs')]:
    expr = sp.simplify(Geff_over_G.subs({kh: kap[h_], kT: kap[t_]}))
    hi = sp.limit(expr, th, sp.pi / 2, '-'); lo = sp.limit(expr, th, 0, '+')
    newton = (hi == 1); enhanced = (lo == sp.oo)
    rows.append((h_, t_, expr, hi, lo, newton, enhanced))
    print(f"     ({h_:>4},{t_:>4}): G_eff/G = {str(expr):>16}   theta->pi/2: {str(hi):>3}   theta->0: {str(lo):>3}   Newton at a>>H: {newton}   enhanced at a<<H: {enhanced}")
passing = [(r_[0], r_[1]) for r_ in rows if r_[5] and r_[6]]
check("C5d exactly ONE mismatched pair has both a Newtonian limit (G_eff -> G at a >> H) and an enhancement at a << H: (kobs, a)", passing == [('kobs', 'a')])
check("C5e that pair is G_eff/G = 1/sin(theta) = sqrt(1 + H^2/a^2) (heat with the FULL kappa_obs, temperature with the acceleration part only, T_U = a/2pi)",
      sp.simplify(rows[2][2] - 1 / sp.sin(th)) == 0)
check("C5f the pair (a, kobs) is the opposite: G_eff/G = sin(theta) < 1, weaker gravity at low a (wrong direction for MOND)", sp.simplify(rows[0][2] - sp.sin(th)) == 0)
check("C5g (H, a): G_eff/G = cot(theta): a = g_N cot(theta) => a^2 = g_N H for ALL g_N: no Newtonian regime at all",
      sp.simplify(rows[4][2] - sp.cot(th)) == 0)
must_fail("C5h claim 'every mismatched pair has a Newtonian limit'", all(r_[5] for r_ in rows))
print("     NOTE: the selection in C5d is by OUTCOME (Newton limit + MOND direction). Nothing in the Clausius chain selects the pair; it is an INPUT.")

n, npass = len(ok), sum(ok)
print(f"\nn03: {npass}/{n} checks passed")
sys.exit(0 if npass == n else 1)
