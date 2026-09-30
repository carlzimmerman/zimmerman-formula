#!/usr/bin/env python3
"""z04: is a Sciama-shaped kernel with the cutoff c^2/a0 (X3) consistent with the record's OWN regime structure and the ephemeris bound?
Uses the record's machinery verbatim: the action's Theta on circular orbits (NR: theta = 2 (v/c)|sin(Omega s/2)|), the alpha = 2 inertia function mu_2,
mu_eff = mu + (Theta/2) mu' (memory-force balance), Delta = g (1 - mu_eff) against the record's bound 3.66e-14 m/s^2, the record's short-memory
criterion lambda*Omega <= 0.1, and its structural exclusion of the long-memory branch.  Constants are the record's (mi_N_count_and_kappa_iff_2026.py)."""
import sympy as sp
import mpmath as mp
import sys

PASS = FAIL = CO = CB = 0


def chk(n, c, d=""):
    global PASS, FAIL
    if c: PASS += 1; print("  ok  ", n, d)
    else: FAIL += 1; print("  FAIL", n, d)


def ctrl(n, c, d=""):
    global CO, CB
    if not c: CO += 1; print("  ctrl-ok ", n, d)
    else: CB += 1; print("  CTRL-BAD", n, d)


mp.mp.dps = 80
C = mp.mpf("2.99792458e8"); LAM = mp.mpf("1.0908e-52"); G = mp.mpf("6.67430e-11")
RHO_L = LAM * C ** 2 / (8 * mp.pi * G); A0 = C ** 2 * mp.sqrt(LAM / (32 * mp.pi))
T_L = 1 / mp.sqrt(G * RHO_L); GM = mp.mpf("1.32712440018e20"); AU = mp.mpf("1.495978707e11")
KPC = mp.mpf("3.0856775814913673e19"); GYR = mp.mpf("3.1557e16"); YR = mp.mpf("3.1557e7"); BOUND = mp.mpf("3.66e-14")
PL = {"Mercury": (mp.mpf("0.387098"), mp.mpf("4.7362e4")), "Earth": (mp.mpf("1"), mp.mpf("2.9785e4")),
      "Mars": (mp.mpf("1.523679"), mp.mpf("2.4077e4")), "Saturn": (mp.mpf("9.53667"), mp.mpf("9.68e3"))}
T_CA0 = C / A0                                  # = 2 t_Lambda (X3's cutoff time c/a0)


def mu2(Y): return mp.sqrt((-1 + mp.sqrt(1 + 4 * Y ** 4)) / 2) / Y


def mu_eff(Y): return mu2(Y) + Y * mp.diff(mu2, Y) / 2


def Delta(g, Th): return g * (1 - mu_eff(Th))


def I_abs(Tm, k):
    """exact int_0^T s |sin(k s)| ds  (half-periods give (2j+1) pi/k^2 each)"""
    n = int(mp.floor(k * Tm / mp.pi)); a = n * mp.pi / k
    F = lambda s_: mp.sin(k * s_) / k ** 2 - s_ * mp.cos(k * s_) / k
    return n ** 2 * mp.pi / k ** 2 + (-1) ** n * (F(Tm) - F(a))


def theta_sharp(N, Tm, Om, v):
    """Theta = N int_0^T (2s/T^2) 2 v |sin(Om s/2)| ds : the sharp r dr kernel on a NR circular orbit (exact)"""
    return N * (2 / Tm ** 2) * 2 * v * I_abs(Tm, Om / 2)


print("== R1: the sharp r dr kernel: short-memory M1|a|/c, long-memory (4N/pi) v/c, with an explicit error bound ==")
ok = True
for OT in (mp.mpf("1e-3"), mp.mpf("0.1")):
    Om = mp.mpf(1); Tm = OT / Om; v = mp.mpf("1e-3")
    Dc = (mp.mpf(2) / 3) * Tm * Om * v                  # M1 |a|/c with M1 = (2/3)T (unit weight), |a| = Om v
    ok = ok and abs(theta_sharp(1, Tm, Om, v) / Dc - 1) < (OT ** 2)
chk("short memory (Omega T = 1e-3, 0.1): Theta = M1 |a|/c with M1 = (2/3) T to O((Omega T)^2)", ok)
worst = mp.mpf(0)
for OT in (mp.mpf("10.3"), mp.mpf("100.1"), mp.mpf("1000.9"), mp.mpf("1e5")):
    for frac in (0, 0.25, 0.5, 0.75, 0.999):
        kT = mp.pi * (int(OT / mp.pi) + frac); Tm = 2 * kT; Om = mp.mpf(1)
        dev = abs(theta_sharp(1, Tm, Om, mp.mpf(1)) / (4 / mp.pi) - 1) * Om * Tm
        worst = max(worst, dev)
chk("long memory: Theta = (4 N/pi) v/c up to a relative error <= 2/(Omega T) (scanned 20 phases of T, Omega T from 10 to 1e5)", worst < 2, f"max error x (Omega T) = {mp.nstr(worst, 4)}")
ctrl("control: the long-memory value is 2N/pi (a wrong limit) -- detected", abs(theta_sharp(1, 2 * mp.pi * 50, mp.mpf(1), mp.mpf(1)) / (2 / mp.pi) - 1) < 0.05)

print("\n== R2: the record's regime variable x = (kernel width) x Omega for the identified kernel T = c/a0 ==")
print(f"   T = c/a0 = {mp.nstr(T_CA0, 6)} s = {mp.nstr(T_CA0/GYR, 6)} Gyr = 2 t_Lambda")
OMEGA = {"Mercury": 2 * mp.pi / (mp.mpf("87.969") * 86400), "Earth": 2 * mp.pi / (mp.mpf("365.256") * 86400),
         "MW 1 kpc (v=100 km/s)": mp.mpf("1e5") / KPC, "MW 8 kpc (v=220 km/s)": mp.mpf("2.2e5") / (8 * KPC), "outer 30 kpc (v=180 km/s)": mp.mpf("1.8e5") / (30 * KPC)}
for nm, Om in OMEGA.items():
    print(f"   {nm:28s} Omega = {mp.nstr(Om, 4)} /s   x = T Omega = {mp.nstr(T_CA0*Om, 4)}")
lam_gal = mp.mpf("0.1") / OMEGA["MW 1 kpc (v=100 km/s)"]
chk("the record's short-memory criterion x = lambda Omega <= 0.1 across the galactic range gives lambda <= 0.98 Myr (record: 0.98 Myr) -- reproduced", abs(lam_gal / (mp.mpf("1e6") * YR) - mp.mpf("0.98")) < 0.05, f"lambda_max = {mp.nstr(lam_gal/(1e6*YR), 4)} Myr")
chk("the identified kernel (T = c/a0 = 101 Gyr) exceeds the record's galactic width bound by 1e5 (x = 2.9e3 at 8 kpc, 6e2 at 30 kpc): it sits in the LONG-memory branch in every galaxy", T_CA0 * OMEGA["MW 8 kpc (v=220 km/s)"] > 1e3 and T_CA0 * OMEGA["outer 30 kpc (v=180 km/s)"] > 1e2 and T_CA0 / lam_gal > 1e4, f"T/lambda_max = {mp.nstr(T_CA0/lam_gal, 4)}")
ctrl("control: the record's own viable kernel (exponential, lambda = 1.0e12 s) is in the LONG-memory branch in the MW (x > 1)", (mp.mpf("1.0e12") * OMEGA["MW 8 kpc (v=220 km/s)"]) > 1, f"(x = {mp.nstr(mp.mpf('1.0e12')*OMEGA['MW 8 kpc (v=220 km/s)'], 3)})")
# structural exclusion of the long-memory branch (record's D4), recomputed
r_, v_, a0s = sp.symbols("r v a_0", positive=True)
fp = sp.Function('fp')
g_bar = v_ * fp(v_) / r_                                # circular orbit with L = m f(v) - m Phi: g_bar = g_obs f'(v)/v, g_obs = v^2/r
deep = sp.Eq(v_ ** 2 / r_, sp.sqrt(g_bar * a0s))        # deep MOND g_obs = sqrt(g_bar a0)
sol = sp.solve(deep, fp(v_))[0]
chk("long-memory branch: matching deep MOND with an inertia that depends on speed alone forces f'(v) = v^3/(r a0), which depends on r at fixed v: STRUCTURALLY excluded (record D4, recomputed)", sp.simplify(sol - v_ ** 3 / (r_ * a0s)) == 0 and sp.diff(sol, r_) != 0)

print("\n== R3: the ephemeris bound for the identified kernels (record's mu_2, mu_eff, Delta = g (1 - mu_eff) <= 3.66e-14) ==")
Th_min = {nm: (GM / (aau * AU) ** 2 / (32 * BOUND)) ** mp.mpf("0.25") for nm, (aau, vp) in PL.items()}
fam = {"A: X3 (unit weight N=1, T=c/a0)": (mp.mpf(1), T_CA0),
       "B: physical Sciama strength at T=c/a0 (N=8 pi)": (8 * mp.pi, T_CA0),
       "C: physical strength + requirement (N=2.93, T=0.683 t_L)": (2 * mp.pi ** (mp.mpf(1) / 3), T_L * mp.pi ** (-mp.mpf(1) / 3)),
       "D: record's viable kernel (N=2.13e6, exp lambda=1e12 s)": (mp.mpf("2.13e6"), None)}
PERIOD_D = {"Mercury": "87.969", "Earth": "365.256", "Mars": "686.98", "Saturn": "10759.2"}
OM_PL = {pn: 2 * mp.pi / (mp.mpf(PERIOD_D[pn]) * 86400) for pn in PL}
# implementation check of Delta: at Theta_min (defined by the record's asymptote Delta = g/(32 Theta^4)) the exact mu_eff must give Delta/bound = 1
_e = sp.Symbol('e', positive=True); _Y = sp.Symbol('Y', positive=True)
_m = sp.sqrt((-1 + sp.sqrt(1 + 4 * _Y ** 4)) / 2) / _Y
_ser = sp.series(1 - (_m + _Y * sp.diff(_m, _Y) / 2).subs(_Y, 1 / _e), _e, 0, 8).removeO()
chk("record's residual: 1 - mu_eff = 1/(32 Theta^4) [1 + 1/(2 Theta^2) + ...] for the alpha = 2 kernel (sympy series; leading term = record eq. 15/22)", sp.simplify(_ser - (_e ** 4 / 32 + _e ** 6 / 64)) == 0)
chk("Delta implementation: with the exact mu_2 and mu_eff, Delta(g, Theta_min)/bound = 1 + 1/(2 Theta_min^2) to 1e-7 for all four planets (the record's leading asymptote plus the series correction)", all(abs(Delta(GM / (PL[pn][0] * AU) ** 2, Th_min[pn]) / BOUND - 1 - 1 / (2 * Th_min[pn] ** 2)) < 1e-7 for pn in PL))
ctrl("control: the OLD uncancelled residual g/(4 Theta^2) at Theta_min gives the bound", all(abs(GM / (PL[pn][0] * AU) ** 2 / (4 * Th_min[pn] ** 2) / BOUND - 1) < 1e-2 for pn in PL))
res = {}
for nm, (N, Tm) in fam.items():
    row = []
    for pn, (aau, vp) in PL.items():
        g = GM / (aau * AU) ** 2
        if Tm is not None:
            Th = theta_sharp(N, Tm, OM_PL[pn], vp / C)
        else:
            lam_ = mp.mpf("1.0e12"); Om = OM_PL[pn]; xx = lam_ * Om
            Th = 4 * N * (vp / C) * xx * mp.coth(mp.pi / xx) / (4 + xx ** 2)
        row.append((pn, Th, Delta(g, Th) / BOUND))
    res[nm] = row
    print(f"   {nm}")
    for pn, Th, r_ in row:
        print(f"      {pn:8s} Theta = {mp.nstr(Th, 4):>10s} (need >= {mp.nstr(Th_min[pn], 4)})  Delta/bound = {mp.nstr(r_, 4)}")
Am = {pn: r_ for pn, Th, r_ in res["A: X3 (unit weight N=1, T=c/a0)"]}
Bm = {pn: r_ for pn, Th, r_ in res["B: physical Sciama strength at T=c/a0 (N=8 pi)"]}
Cm = {pn: r_ for pn, Th, r_ in res["C: physical strength + requirement (N=2.93, T=0.683 t_L)"]}
Dm = {pn: r_ for pn, Th, r_ in res["D: record's viable kernel (N=2.13e6, exp lambda=1e12 s)"]}
chk("family A (X3's identified kernel): Theta(Mercury) = 2.0e-4 << 1, the mu-argument is deep in the MOND branch at Mercury: Delta/bound ~ 1e12 (killed)", all(v_ > 1e9 for v_ in Am.values()) and res["A: X3 (unit weight N=1, T=c/a0)"][0][1] < 1e-3, f"Mercury {mp.nstr(Am['Mercury'], 3)}, Saturn {mp.nstr(Am['Saturn'], 3)}")
chk("family B (Sciama's physical strength at T=c/a0, N = 8 pi): killed as well, by 1e11-1e12", all(v_ > 1e9 for v_ in Bm.values()), f"Mercury {mp.nstr(Bm['Mercury'], 3)}")
chk("family C (physical strength + M1 requirement): killed", all(v_ > 1e9 for v_ in Cm.values()), f"Mercury {mp.nstr(Cm['Mercury'], 3)}")
chk("Theta shortfall at Mercury: needed 428.7, identified kernel 2.0e-4 => 2.1e6 = the record's N_min (the 'six orders' the record quotes for unit weight): the Sciama-shaped kernel is the record's already-killed unit-weight candidate", abs(Th_min['Mercury'] / res["A: X3 (unit weight N=1, T=c/a0)"][0][1] / mp.mpf("2.13e6") - 1) < 0.05, f"shortfall = {mp.nstr(Th_min['Mercury']/res['A: X3 (unit weight N=1, T=c/a0)'][0][1], 4)}")
ctrl("control: the record's viable kernel D also fails the bound at Mercury by > 10x", Dm["Mercury"] > 10, f"D/bound at Mercury = {mp.nstr(Dm['Mercury'], 4)}")
chk("control that passes: D (N = 2.13e6, lambda = 1e12 s) sits at the bound at Mercury (Delta/bound within [0.5, 1.5]) and below it elsewhere: the machinery reproduces the record's surviving edge", 0.5 < Dm["Mercury"] < 1.5 and all(Dm[k] < 1.05 for k in Dm), f"Mercury {mp.nstr(Dm['Mercury'], 4)}")
ctrl("control: family A satisfies the bound", all(v_ <= 1 for v_ in Am.values()))

print("\n== R4: what a Sciama-strength kernel would have to be to sit where the record needs it ==")
Nmin = Th_min["Mercury"] * mp.pi * C / (4 * PL["Mercury"][1])
Trec = T_CA0 / Nmin                                                # sharp shape: M1 = (2/3) N T = (2/3) c/a0 => T = (c/a0)/N
rho_req = Nmin / (2 * mp.pi * G * Trec ** 2)
ratio = rho_req / RHO_L
print(f"   record: N >= {mp.nstr(Nmin, 5)} ; with M1 = (2/3) N T = (2/3) c/a0 the sharp kernel has T = (c/a0)/N = {mp.nstr(Trec, 4)} s, R_c = c T = {mp.nstr(C*Trec/KPC, 4)} kpc")
print(f"   Sciama strength N = 2 pi G rho T^2  =>  rho_required = {mp.nstr(rho_req, 4)} kg/m^3 = {mp.nstr(ratio, 4)} x rho_Lambda ({mp.nstr(RHO_L, 4)} kg/m^3)")
chk("the record's kernel needs N/T^2 = 2 pi G rho with rho = 4e17 rho_Lambda (analytic: N^3/(8 pi) = 3.7e17): Sciama's cosmological strength is ~17 orders too weak at the required width", abs(ratio / (Nmin ** 3 / (8 * mp.pi)) - 1) < 1e-9 and ratio > 1e17, f"ratio {mp.nstr(ratio, 4)} vs N^3/(8 pi) = {mp.nstr(Nmin**3/(8*mp.pi), 4)}")
Msun = mp.mpf("1.98847e30"); pc = KPC / 1000
print(f"   context (order of magnitude, not a record number): solar-neighbourhood stellar+gas density ~ 0.1 Msun/pc^3 = {mp.nstr(mp.mpf('0.1')*Msun/pc**3, 3)} kg/m^3, i.e. still {mp.nstr(rho_req/(mp.mpf('0.1')*Msun/pc**3), 3)} x below the required rho")
ctrl("control: the required density is comparable to the cosmological matter density (rho_m ~ 0.45 rho_Lambda)", ratio < 100)

print("\n== R5: consistency of R3/R4 with the record's OWN earlier verdict on the same class ==")
# record (mi_local_source_for_K): K = (N/lambda) exp(-s/lambda), lambda = t_L, N = 4/3: excluded, long-memory. Compare Theta at Mercury with family A.
Th_rec = 4 * (mp.mpf(4) / 3) * (PL["Mercury"][1] / C) / mp.pi
Th_A = res["A: X3 (unit weight N=1, T=c/a0)"][0][1]
chk("record's own 'vacuum free-fall time at O(1) weight' kernel (exp, lambda = t_L, N = 4/3) has Theta(Mercury) = 2.7e-4: the same order as the Sciama-shaped kernel (2.0e-4) -> same verdict, same 1e6 shortfall", 0.5 < Th_rec / Th_A < 2, f"{mp.nstr(Th_rec, 4)} vs {mp.nstr(Th_A, 4)}")
print(f"\n== TOTAL: {PASS} pass, {FAIL} fail; controls rejected {CO}, not rejected {CB} ==")
sys.exit(0 if FAIL == 0 and CB == 0 else 1)
