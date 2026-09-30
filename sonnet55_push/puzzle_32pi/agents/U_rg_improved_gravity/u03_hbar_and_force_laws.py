#!/usr/bin/env python3
"""u03_hbar_and_force_laws.py -- lane U task item (2): the hbar issue, and what running-G force laws can and cannot give as an acceleration scale.

PART A  dimensional bookkeeping (sympy, exponents of M, L, T).  Fixed-point running is G(k) = g* c^3/(hbar k^2) with g* dimensionless (g = hbar G k^2/c^3).
   * naive force  a = G(k = xi/r) M/r^2 = g* c^3 M/(hbar xi^2): r-independent, linear in M, ~ 1/hbar  (an acceleration, but NOT mass-free, NOT hbar-free);
   * improved-action extra term (Reuter-Weyer / Rodrigues-Letelier-Shapiro: Phi = Phi_N + (c^2/2) dG/G0): a = g* c^2 r/(xi^2 l_Pl^2), l_Pl^2 = hbar G0/c^3;
   * the extra term is hbar-free iff g* = xi^2 l_Pl^2/L^2 for a classical length L, i.e. g*_IR is (xi^2 times) the hierarchy hbar G0 Lambda/c^3 ~ 1e-122, NOT an O(1) number;
   * Buckingham: every acceleration built from {G, c, Lambda, M, hbar} is  c^2 sqrt(Lambda) F(G M sqrt(Lambda)/c^2 , eps),  eps = hbar G Lambda/c^3.  A universal
     (M-free), hbar-free acceleration is c^2 sqrt(Lambda) x (pure number): the ONLY classical candidate.  No RG improvement changes that; it can only supply the number.

PART B  which (running exponent q, cutoff identification, reading) gives which force-law exponents.  G(k) = G0 (k_tr/k)^q.  Two readings:
   'naive'    a = G(k(r)) G... i.e. a = G_run M/r^2 ;   'improved-action'   a = -d/dr [ (c^2/2)(G_run/G0 - 1) ]  (Reuter-Weyer eq (5.14)/(6.10) form; the M-dependence enters only via k(r; M)).
   Identifications: k = xi/r (Reuter-Weyer) or k = zeta g_N/c^2 with g_N = G0 M/r^2 (an acceleration-based identification: my construction, NOT in the papers).
   Output: exponents (d ln a/d ln r, d ln a/d ln M).  Deep MOND is (-1, +1/2).

PART C  Reuter-Weyer IR-fixed-point crossover radius r_nc = (2 G M L^2)^(1/3), L = c/H0: the transition acceleration is M^(1/3) dependent and ~ 1e-4 a0 -- no universal scale.
Controls / mutations: dimension checker rejects a wrong formula; exponent solver returns the known RW (q, r) results; MOND needs exactly q = 1/2.  Exit 0 iff all pass.
"""
import math
import sys
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

Mu, Lu, Tu = sp.symbols('M_ L_ T_', positive=True)      # unit symbols
G, c, hbar, Lam, Mm, r, k, xi, gs = sp.symbols('G c hbar Lambda M r k xi g_star', positive=True)
DIM = {G: Mu**-1 * Lu**3 * Tu**-2, c: Lu / Tu, hbar: Mu * Lu**2 / Tu, Lam: Lu**-2, Mm: Mu, r: Lu, k: 1 / Lu, xi: 1, gs: 1}
def dim(expr):
    return sp.simplify(sp.powsimp(sp.expand_power_base(expr.subs(DIM, simultaneous=True), force=True), force=True))
ACC = Lu / Tu**2

print("=" * 100); print("PART A  dimensions and hbar"); print("=" * 100)
check("g = hbar G k^2/c^3 is dimensionless", sp.simplify(dim(hbar * G * k**2 / c**3) - 1) == 0)
check("MUTATION: hbar G k^2/c^2 is NOT dimensionless (checker has power)", sp.simplify(dim(hbar * G * k**2 / c**2) - 1) != 0)
check("G(k) = g* c^3/(hbar k^2) has the dimension of G", sp.simplify(dim(gs * c**3 / (hbar * k**2)) / dim(G) - 1) == 0)
a_naive = sp.simplify((gs * c**3 / (hbar * (xi / r)**2)) * Mm / r**2)
print("  naive force  a = G(k=xi/r) M/r^2 =", a_naive)
check("naive force is an acceleration", sp.simplify(dim(a_naive) / ACC - 1) == 0)
check("naive force is independent of r", sp.diff(a_naive, r) == 0)
check("naive force is linear in M and proportional to 1/hbar", sp.simplify(sp.diff(sp.log(a_naive), Mm) * Mm - 1) == 0 and sp.simplify(sp.diff(sp.log(a_naive), hbar) * hbar + 1) == 0)
dG = gs * c**3 * r**2 / (hbar * xi**2)                    # fixed-point piece of G(k = xi/r)
Phi_extra = c**2 / 2 * dG / G
a_IR = sp.simplify(sp.diff(Phi_extra, r))
print("  improved-action extra acceleration =", a_IR, "  (= g* c^2 r/(xi^2 l_Pl^2) with l_Pl^2 = hbar G/c^3)")
check("improved-action extra term is an acceleration, M-independent, linear in r", sp.simplify(dim(a_IR) / ACC - 1) == 0 and sp.diff(a_IR, Mm) == 0 and sp.simplify(sp.diff(a_IR, r) * r / a_IR - 1) == 0)
Lc = sp.symbols('L_c', positive=True)                      # a classical length
gs_needed = sp.solve(sp.Eq(a_IR, c**2 * r / Lc**2), gs)[0]
print("  hbar-free requirement  a = c^2 r/L^2  =>  g* =", gs_needed)
check("g*_needed = xi^2 hbar G/(c^3 L^2) = xi^2 l_Pl^2/L^2  (proportional to hbar)", sp.simplify(gs_needed - xi**2 * hbar * G / (c**3 * Lc**2)) == 0 and sp.simplify(sp.diff(sp.log(gs_needed), hbar) * hbar - 1) == 0)
# numbers (CODATA-level constants, SI)
Gn, cn, hn = 6.67430e-11, 2.99792458e8, 1.054571817e-34
H0 = 67.4e3 / 3.0856775814913673e22                       # s^-1
lPl = math.sqrt(hn * Gn / cn**3)
eps = (lPl * H0 / cn)**2
print(f"  l_Pl = {lPl:.4e} m;  (l_Pl H0/c)^2 = {eps:.3e};  Reuter-Weyer eq (5.25) with xi_hat = 1, z_tr = 1: g*_IR = (9/16)(2^(3/2)) eps = {9/16 * 2**1.5 * eps:.2e}")
check("the required g*_IR is ~1e-122 (not O(1)): (l_Pl H0/c)^2 in [1e-123, 1e-121]", 1e-123 < eps < 1e-121)
# Buckingham: acceleration monomials G^a c^b Lam^d M^e hbar^f
a_, b_, d_, e_, f_ = sp.symbols('a b d e f')
mono = G**a_ * c**b_ * Lam**d_ * Mm**e_ * hbar**f_
expr = dim(mono)
eqs = []
for U, target in ((Mu, 0), (Lu, 1), (Tu, -2)):
    eqs.append(sp.Eq(sp.powsimp(expr).as_powers_dict().get(U, 0), target))
sol = sp.solve(eqs, [a_, b_, d_], dict=True)[0]
print("  acceleration monomials (free exponents e, f):", sol)
sol_hbar_free = {kk: vv.subs(f_, 0) for kk, vv in sol.items()}
sol_M_free = {kk: vv.subs({e_: 0, f_: 0}) for kk, vv in sol.items()}
print("  hbar-free and M-free:", sol_M_free)
check("hbar-free, M-free acceleration is UNIQUE: c^2 Lambda^(1/2)  (G^0)", sol_M_free == {a_: 0, b_: 2, d_: sp.Rational(1, 2)})
check("with M allowed (hbar-free): exponent of G equals exponent of M (family c^2 sqrt(Lambda) (G M sqrt(Lambda)/c^2)^e)", sp.simplify(sol_hbar_free[a_] - e_) == 0)
check("hbar enters only through the dimensionless eps = hbar G Lambda/c^3:  f multiplies (a,b,d) by (f, -3f, f)", sp.simplify(sol[a_] - sol_hbar_free[a_] - f_) == 0 and sp.simplify(sol[b_] - sol_hbar_free[b_] + 3 * f_) == 0 and sp.simplify(sol[d_] - sol_hbar_free[d_] - f_) == 0)
print("  => the RG (which supplies hbar only through g = hbar G k^2/c^3) can change a0 = c^2 sqrt(Lambda) x number only by a number; g*_IR is not that number: it IS eps up to O(1).")


# RESTATEMENT (identity, not a result): the puzzle in fixed-point variables.  P := g* lambda* = hbar G Lambda/c^3 is the dimensionless product that a fixed point
# fixes (u01: ~0.1 for the UV point; Bonanno-Reuter: an undetermined ~1e-120 for the IR point).  With a_Pl = c^2/l_Pl and a0^2 = c^4 Lambda/(32 pi):
a0s, aPl = sp.symbols('a0 a_Pl', positive=True)
a0_expr = c**2 * sp.sqrt(Lam / (32 * sp.pi)); aPl_expr = c**2 / sp.sqrt(hbar * G / c**3)
check("IDENTITY (restatement only): 32 pi (a0/a_Pl)^2 = hbar G Lambda/c^3 = g*_IR lambda*_IR", sp.simplify(32 * sp.pi * (a0_expr / aPl_expr)**2 - hbar * G * Lam / c**3) == 0)
t_Pl = math.sqrt(hn * Gn / cn**5); aPl_n = cn / t_Pl
P_from_a0 = 32 * math.pi * (1.2e-10 / aPl_n)**2
P_from_Lam = 3 * 0.7 * eps
print(f"  a_Pl = {aPl_n:.3e} m/s^2;  32 pi (a0/a_Pl)^2 = {P_from_a0:.2e} (a0 = 1.2e-10);  3 Omega_L (l_Pl H0/c)^2 = {P_from_Lam:.2e} (Omega_L = 0.7)  -- Bonanno-Reuter quote 'O(1e-120)' for g*_IR lambda*_IR and say it is NOT computed")
check("both are ~1e-122: the RG converts the puzzle into a statement about the undetermined IR fixed-point product g*lambda*, nothing more", 1e-123 < P_from_a0 < 1e-121 and 1e-123 < P_from_Lam < 1e-121)

# How hbar-free is the observed a0?  If a0 = c^2 sqrt(Lambda) x eps^f x O(1), what exponent f is allowed?
Lam_n = 3 * 0.7 * H0**2 / cn**2
ratio = 1.2e-10 / (cn**2 * math.sqrt(Lam_n))
eps_act = hn * Gn * Lam_n / cn**3
f_fit = math.log(ratio) / math.log(eps_act); f_max = math.log(10.0) / abs(math.log(eps_act))
print(f"  a0/(c^2 sqrt(Lambda)) = {ratio:.3f};  eps = hbar G Lambda/c^3 = {eps_act:.2e};  a0 = c^2 sqrt(Lambda) eps^f (no coefficient) needs f = {f_fit:.4f};  allowing an O(1)-to-10 coefficient, |f| < {f_max:.4f}")
check("the observed a0 leaves an hbar-dependence exponent |f| < 0.01: it is hbar-free to ~1 part in 10^2 of the exponent (a0 ~ c^2 sqrt(Lambda), not a Planck-suppressed quantity)", f_max < 0.01 and abs(f_fit) < 0.01)

print(); print("=" * 100); print("PART B  force-law exponents for G(k) = G0 (k_tr/k)^q"); print("=" * 100)
q, ktr, zeta, G0, Rr = sp.symbols('q k_tr zeta G0 R', positive=True)
def exps(a):
    a = sp.simplify(a)
    er = sp.simplify(sp.diff(sp.log(a), Rr) * Rr); eM = sp.simplify(sp.diff(sp.log(a), Mm) * Mm)
    return er, eM
Grun = lambda kk: G0 * (ktr / kk)**q
rows = []
k_r = xi / Rr; k_g = zeta * G0 * Mm / (c**2 * Rr**2)
for ident_name, kk in (("k = xi/r", k_r), ("k = zeta g_N/c^2", k_g)):
    a_naive_ = Grun(kk) * Mm / Rr**2
    a_impr = sp.simplify(-sp.diff(c**2 / 2 * (Grun(kk) / G0 - 1), Rr))   # -dPhi/dr with Phi_extra = (c^2/2)(G_run/G0 - 1); sign: attractive = positive
    rows.append((ident_name, "naive  G(k(r)) M/r^2", exps(a_naive_)))
    rows.append((ident_name, "improved-action", exps(a_impr)))
print(f"  {'identification':22s} {'reading':24s} {'dln a/dln r':>14s} {'dln a/dln M':>14s}")
for name, reading, (er, eM) in rows:
    print(f"  {name:22s} {reading:24s} {str(er):>14s} {str(eM):>14s}")
E = {(n, rd): (er, eM) for n, rd, (er, eM) in rows}
# known Reuter-Weyer results, recovered:
er, eM = E[("k = xi/r", "improved-action")]
check("RW: k = xi/r, improved action: force exponent q-1 in r, M-independent (their plateau v^2 = q/2, universal, no Tully-Fisher)", sp.simplify(er - (q - 1)) == 0 and eM == 0)
a_lim = sp.limit(sp.diff(c**2 / 2 * (Grun(k_r) / G0 - 1), Rr) * Rr / q, q, 0)      # inward acceleration times r, over q
check("RW: q -> 0 limit: v^2 = a r = c^2 q/2 (a r / q -> c^2/2)", sp.simplify(a_lim - c**2 / 2) == 0)
er, eM = E[("k = xi/r", "improved-action")]
er2 = sp.simplify(er.subs(q, 2))
check("RW IR fixed point q = 2, k = xi/r: force ~ r^1 and M-independent (their eq 5.14, linear 'confinement' force)", er2 == 1 and eM == 0)
er, eM = E[("k = zeta g_N/c^2", "naive  G(k(r)) M/r^2")]
sol_q = sp.solve([sp.Eq(er, -1), sp.Eq(eM, sp.Rational(1, 2))], q, dict=True)
print("  acceleration identification, naive reading: solve (r-exponent, M-exponent) = (-1, 1/2) for q ->", sol_q)
check("deep-MOND scaling a ~ sqrt(M)/r arises here ONLY for q = 1/2 (both exponents consistent)", sol_q == [{q: sp.Rational(1, 2)}])
a_m = sp.simplify((Grun(k_g) * Mm / Rr**2).subs(q, sp.Rational(1, 2)))
a0_id = sp.symbols('a0', positive=True)
sol_a0 = sp.solve(sp.Eq(a_m**2, a0_id * G0 * Mm / Rr**2), a0_id)[0]
print("  q = 1/2, k = zeta g_N/c^2:  a^2 = a0 G M/r^2  with  a0 =", sol_a0)
check("a0 = c^2 k_tr/zeta  (hbar-free: k_tr is a wavenumber, zeta a pure number)", sp.simplify(sol_a0 - c**2 * ktr / zeta) == 0)
er, eM = E[("k = zeta g_N/c^2", "naive  G(k(r)) M/r^2")]
check("fixed-point exponent q = 2 with this identification: force ~ r^2/M (grows with r, DEcreases with M): not gravity-like", sp.simplify(er.subs(q, 2)) == 2 and sp.simplify(eM.subs(q, 2)) == -1)
er, eM = E[("k = zeta g_N/c^2", "improved-action")]
print("  acceleration identification, improved-action reading: exponents (r, M) =", (er, eM), "  -> extra force ~ M^(-q): no BTFR either")
check("acceleration identification + improved-action reading: M-exponent is -q (never +1/2 for q > 0)", sp.simplify(eM + q) == 0)
print("  So: a0 = c^2 k_tr/zeta needs THREE inserted ingredients: q = 1/2 (eta_N = -1/2: neither Gaussian (0) nor UV/IR fixed-point (-2)), the identification k ~ g/c^2 (RW: 'critical acceleration, not distance', beyond their scheme), and k_tr, zeta.")

print(); print("=" * 100); print("PART C  Reuter-Weyer IR fixed point: crossover radius and transition acceleration"); print("=" * 100)
Msun = 1.98847e30; kpc = 3.0856775814913673e19
def r_nc(M):     # (r_S L^2)^(1/3), r_S = 2 G M/c^2, L = c/H0   (RW 5.15, 5.27: kappa = H0)
    L = cn / H0
    return (2 * Gn * M / cn**2 * L**2)**(1 / 3)
a0_obs = 1.2e-10
print(f"  {'M [Msun]':>10s} {'r_nc [kpc]':>12s} {'G M/r_nc^2 [m/s^2]':>20s} {'/a0':>10s}")
vals = []
for M in (1e8 * Msun, 1e10 * Msun, 1e11 * Msun, 1e12 * Msun):
    rr = r_nc(M); an = Gn * M / rr**2; vals.append(an)
    print(f"  {M / Msun:10.0e} {rr / kpc:12.1f} {an:20.3e} {an / a0_obs:10.2e}")
slope = math.log(vals[-1] / vals[0]) / math.log(1e4)
print(f"  d ln a_nc / d ln M = {slope:.4f}  (exact 1/3)")
check("transition acceleration scales as M^(1/3): no universal a0 from the IR fixed point", abs(slope - 1 / 3) < 1e-9)
check("for M = 1e11 Msun (H0 = 67.4): r_nc ~ 500-600 kpc (Reuter-Weyer quote 560 kpc at H0 = 70)", 450 < r_nc(1e11 * Msun) / kpc < 650)
check("... and the transition acceleration is < 1e-3 a0 (they themselves call the hierarchy 2 orders of magnitude too small)", vals[2] / a0_obs < 1e-3)


print(); print("=" * 100); print("PART D  a 2025 'marginal IR running' proposal (Kumar, arXiv:2509.05246, opened): G(k) = G_N (1 + k*/k), k = 1/r -> q = 1 row of Part B"); print("=" * 100)
# their Table I (opened): baryonic mass, outer velocity, derived k* (per kpc) for three galaxies; relation k* = pi V0^2/(2 G M)
tab = [(1.01e12, 271.4, 2.66e-2), (5.85e11, 210.4, 2.76e-2), (3.55e11, 158.9, 2.60e-2)]
Gk = 4.30091e-6          # kpc km^2 s^-2 Msun^-1
a0_kms2_per_kpc = 1.2e-10 / 1e6 * 3.0856775814913673e19    # a0 = 1.2e-10 m/s^2 in km^2 s^-2 kpc^-1
print(f"  {'M_bar [Msun]':>14s} {'V0 [km/s]':>10s} {'k* (paper)':>11s} {'pi V0^2/(2GM)':>14s} {'V0^4/(G M) / a0':>16s}")
effs = []
for M, V, ks in tab:
    kcalc = math.pi * V**2 / (2 * Gk * M); eff = V**4 / (Gk * M) / a0_kms2_per_kpc; effs.append(eff)
    print(f"  {M:14.3e} {V:10.1f} {ks:11.3e} {kcalc:14.3e} {eff:16.3f}")
check("the paper's tabulated k* equals pi V0^2/(2 G M) for all three galaxies (2%)", all(abs(math.pi * V**2 / (2 * Gk * M) / ks - 1) < 0.02 for M, V, ks in tab))
slope = math.log(tab[0][1] / tab[2][1]) / math.log(tab[0][0] / tab[2][0])
print(f"  d ln V0 / d ln M over the three galaxies = {slope:.3f}   (v^2 ~ M means 0.5; the baryonic Tully-Fisher relation v^4 ~ M means 0.25)")
check("a universal k* (the 'single crossover parameter') means V0^2 ~ M (slope 0.5), not BTFR (0.25): this is the naive-reading q = 1 row of Part B (v^2 = G M/r_tr)", abs(slope - 0.5) < 0.05)
print(f"  V0^4/(G M a0) for the three galaxies: {[round(e, 2) for e in effs]}  (BTFR/MOND would give the same number for all)")
check("the implied MOND-like a0_eff varies by a factor > 2.5 across only a 3x mass range", max(effs) / min(effs) > 2.5)
print("  k* is fitted (their words: predicting it 'from first principles' is left to future work); it is a wavenumber, so no hbar enters -- but then nothing ties it to Lambda or a0.")

print()
fails = ok.count(False)
print(f"RESULT: {ok.count(True)} checks passed, {fails} failed")
sys.exit(1 if fails else 0)
