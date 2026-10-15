#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
short_numbers.py -- every number quoted in `mnras_a0_lambda_short.tex`.

Three kinds of check, each printed with its kind (only the first two can fail on the data):
  [algebra]  recomputed here from the formulas printed in the paper (dimensional analysis, the unit chain, the series
             expansion, the error-amplification derivation, the odds formulas).  A numerical differentiation / solve is
             used wherever the paper does a derivation by hand, so a slip in the hand algebra shows up as a FAIL.
  [data]     read from the committed output of the longer analysis, ../mnras_submission_2026_v3/paper_numbers.json
             (SPARC fits, estimators A/B/C, RC100, the design Monte Carlo) and compared with what the short paper quotes.
  [lit]      a value taken from a cited paper (not computed here); listed so that nothing in the text is unaccounted for.

Then every quote string registered below must occur in the .tex, and EVERY number with two or more decimals in the .tex
must be registered (so no figure can be added to the text without being checked here).
Run:  python3 short_numbers.py       (exit 1 on any FAIL)
"""
import os, re, sys, json, math
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.join(HERE, "..", "mnras_submission_2026_v3")
PN = json.load(open(os.path.join(V3, "paper_numbers.json")))
TEX = open(os.path.join(HERE, "mnras_a0_lambda_short.tex")).read()

FAILS, ROWS, QUOTES = [], [], set()


def check(kind, label, ok, detail, quotes=()):
    """kind: algebra | data | lit.  quotes: strings that must appear verbatim in the .tex."""
    miss = [q for q in quotes if q not in TEX]
    good = bool(ok) and not miss
    ROWS.append((kind, label, good, detail, miss))
    QUOTES.update(quotes)
    if not good:
        FAILS.append(label)


def close(a, b, rel=1e-3, ab=0.0):
    return abs(a - b) <= max(rel * abs(b), ab)


# =====================================================================================================================
# 1. Dimensional analysis, equation (2):  kg: -b+g=0 ; m: a+3b-3g=1 ; s: -a-2b=-2
A = np.array([[0, -1, 1], [1, 3, -3], [-1, -2, 0]], float)      # unknowns (alpha, beta, gamma)
sol = np.linalg.solve(A, np.array([0, 1, -2], float))
check("algebra", "S1 dimensional analysis gives alpha=1, beta=gamma=1/2", np.allclose(sol, [1, .5, .5]),
      f"(alpha,beta,gamma) = {sol.round(12).tolist()}", [r"\alpha=1", r"\beta=1/2", r"\gamma=\beta"])

# 2. The unit chain (the aligned block in Section 2), Planck 2020 H0 = 67.4, Omega_L = 0.685
c, G, MPC = 2.99792458e8, 6.6743e-11, 3.08568e22
H0 = 67.4e3 / MPC
rho_crit = 3 * H0**2 / (8 * math.pi * G)
rho_L = 0.685 * rho_crit
Grho = G * rho_L
sq = math.sqrt(Grho)
csq = c * sq
a0_L = 0.5 * csq
a0_C = 0.5 * c * math.sqrt(G * rho_crit)
S1 = PN["S1"]
check("algebra", "S2 unit chain H0, rho_crit, rho_L, sqrt(G rho_L), c sqrt(G rho_L)",
      close(H0, 2.184e-18, 5e-4) and close(rho_crit, 8.533e-27, 5e-4) and close(rho_L, 5.845e-27, 5e-4)
      and close(sq, 6.246e-19, 5e-4) and close(csq, 1.872e-10, 5e-4),
      f"H0={H0:.4e} rho_crit={rho_crit:.4e} rho_L={rho_L:.4e} sqrt={sq:.4e} c*sqrt={csq:.4e}",
      ["2.184\\times10^{-18}", "8.533\\times10^{-27}", "5.845\\times10^{-27}", "6.246\\times10^{-19}", "1.872\\times10^{-10}",
       "3.08568\\times10^{22}", "67.4", "0.685"])
check("algebra", "S3 a0 = 9.36e-11 (rho_L), 1.13e-10 (rho_crit), ratio Omega_L^-1/2 = 1.208",
      close(a0_L, 9.36e-11, 5e-4) and close(a0_C, 1.13e-10, 3e-3) and close(a0_C / a0_L, 0.685**-0.5, 1e-9)
      and close(0.685**-0.5, 1.208, 1e-3),
      f"{a0_L:.4e}, {a0_C:.4e}, ratio {a0_C/a0_L:.4f}", ["9.36\\times10^{-11}", "1.13\\times10^{-10}", "1.208"])
check("data", "S3b same chain as the committed v3 S1 block (relative 1e-5; the v3 script uses the exact Mpc)",
      close(S1["a0_L"], a0_L, 1e-5) and close(S1["a0_C"], a0_C, 1e-5), f"v3: {S1['a0_L']:.5e}, {S1['a0_C']:.5e}")
check("lit", "S3c usual value (1.20 +- 0.02 +- 0.24)e-10 (McGaugh+2016)", True, "quoted from the cited paper",
      ["(1.20\\pm0.02\\pm0.24)"])
check("lit", "S3d constants used in the text: c = 2.99792e8, G = 6.6743e-11 (CODATA)", True, "c in the chain",
      ["6.674\\times10^{-11}"])

# 3. Deep-limit series, equations (5)-(6)
for y in (1e-6, 1e-4, 1e-2):
    s = math.sqrt(y)
    nu = 1 / (1 - math.exp(-s))
    lead = (1 / s) * (1 + s / 2)
    # next term is O(s) relative: nu*s = 1 + s/2 + s^2/12 + ...
    err = abs(nu * s - (1 + s / 2 + s * s / 12)) / (nu * s)
    assert err < 1e-3 * s * s + 1e-12, (y, err)
check("algebra", "S4 nu(y)*sqrt(y) = 1 + sqrt(y)/2 + y/12 + ...  (so g_obs = sqrt(g_bar a0)(1 + sqrt(y)/2))", True,
      "series verified at y = 1e-6, 1e-4, 1e-2", ["s=\\sqrt y", "1-e^{-s}=s-s^2/2"])
# g_bar/sqrt(y) = sqrt(g_bar a0)
gb, a0t = 3.3e-12, 1.0e-10
check("algebra", "S5 g_bar/sqrt(y) = sqrt(g_bar a0)", close(gb / math.sqrt(gb / a0t), math.sqrt(gb * a0t), 1e-12),
      "identity checked numerically")

# 4. SPARC fit vs mass-to-light ratio (data)
tab = {round(r["UD"], 1): r for r in PN["S2"]["table"]}
check("data", "S6 kappa and a0 at Upsilon = 0.5/0.6/0.7 (Planck-consistent distances, bulge 0.7)",
      close(tab[0.5]["kappa_L"], 0.560, 1e-3) and close(tab[0.6]["kappa_L"], 0.457, 1e-3) and close(tab[0.7]["kappa_L"], 0.381, 1e-3)
      and close(tab[0.5]["a0"], 1.05e-10, 5e-3) and close(tab[0.6]["a0"], 0.86e-10, 5e-3) and close(tab[0.7]["a0"], 0.71e-10, 5e-3),
      f"kappa {[round(tab[u]['kappa_L'],3) for u in (.5,.6,.7)]}, a0 {[round(tab[u]['a0']*1e10,3) for u in (.5,.6,.7)]}",
      ["$a_0=1.05$, $0.86$ and $0.71\\times10^{-10}$", "$\\kappa=0.560$, $0.457$ and $0.381$"])
check("data", "S6b rms scatter 0.143-0.145 dex at Upsilon 0.5-0.7",
      all(0.1425 <= tab[u]["rms"] <= 0.1455 for u in (0.5, 0.6, 0.7)),
      f"rms {[round(tab[u]['rms'],4) for u in (.5,.6,.7)]}", ["0.143--0.145"])
r1 = tab[0.6]["kappa_L"] / tab[0.5]["kappa_L"]
check("algebra", "S6c kappa(0.6)/kappa(0.5) = 0.82 close to 0.5/0.6 = 0.83 (a0 proportional to 1/Upsilon)",
      close(r1, 0.82, 5e-3) and close(0.5 / 0.6, 0.83, 5e-3), f"{r1:.4f} vs {0.5/0.6:.4f}", ["$0.457/0.560=0.82$", "$0.5/0.6=0.83$"])
check("data", "S6d kappa = 1/2 needs Upsilon = 0.555", close(PN["S2"]["ud_for_half_L"], 0.555, 1e-3), f"{PN['S2']['ud_for_half_L']:.4f}", ["0.555"])
check("data", "S6e SPARC counts: 2803 points in 164 galaxies", PN["S2"]["n_pts"] == 2803 and PN["S2"]["n_gal"] == 164, "", ["2803", "164 galaxies"])
check("lit", "S6f SPARC has 175 galaxies; 97 on Hubble-flow distances at H0 = 73; Upsilon 0.5-0.7 at 3.6 um (Meidt+14)", True, "", ["175 disc galaxies", "97 galaxies", "73"])

# 5. Estimators A, B, C and the pulls (data)
meas = {m[0][0]: (m[1], m[2]) for m in PN["S3"]["meas"]}
kA, sA = meas["A"]; kB, sB = meas["B"]; kC, sC = meas["C"]
check("data", "S7 kappa_A = 0.450 +- 0.073, kappa_B = 0.58 +- 0.18, kappa_C = 0.43 +- 0.08",
      close(kA, 0.450, 2e-3) and close(sA, 0.073, 5e-3) and close(kB, 0.58, 1e-2) and close(sB, 0.18, 3e-2)
      and close(kC, 0.43, 1e-2) and close(sC, 0.08, 4e-2),
      f"A {kA:.4f}+-{sA:.4f}  B {kB:.4f}+-{sB:.4f}  C {kC:.4f}+-{sC:.4f}",
      ["$\\kappa=0.450\\pm0.073$, $0.58\\pm0.18$ and $0.43\\pm0.08$", "$0.45\\pm0.07$, $0.58\\pm0.18$ and $0.43\\pm0.08$"])
kap_h = PN["S3"]["kappa_horizon"]                         # c H_Lambda / 2 pi
check("algebra", "S7b c H_Lambda/(2 pi) has kappa = sqrt(8 pi/3)/(2 pi) = 0.461",
      close(math.sqrt(8 * math.pi / 3) / (2 * math.pi), 0.461, 1e-3) and close(kap_h, 0.461, 1e-3), f"{kap_h:.4f}", ["0.461"])
p_half = [abs(0.5 - k) / s for k, s in ((kA, sA), (kB, sB), (kC, sC))]
p_hor = [abs(kap_h - k) / s for k, s in ((kA, sA), (kB, sB), (kC, sC))]
check("data", "S7c distance from kappa = 1/2: 0.7, 0.5, 0.9 sigma; from 0.461: 0.1, 0.7, 0.4 sigma",
      [round(x, 1) for x in p_half] == [0.7, 0.5, 0.9] and [round(x, 1) for x in p_hor] == [0.1, 0.7, 0.4],
      f"{[round(x,2) for x in p_half]}, {[round(x,2) for x in p_hor]}",
      ["(0.7, 0.5 and $0.9\\sigma$ away)", "(0.1, 0.7 and $0.4\\sigma$)"])
des = [p for p in PN["S3"]["published"] if p["paper"] == "Desmond 2023"][0]
check("data", "S7d Desmond (2023): kappa = 0.636 +- 0.053, 2.6 sigma above 1/2",
      close(des["kappa_L"], 0.636, 2e-3) and close(des["s_L"], 0.053, 1e-2) and round(des["pull_half_L"], 1) == 2.6,
      f"{des['kappa_L']:.4f} +- {des['s_L']:.4f}, pull {des['pull_half_L']:.2f}", ["$\\kappa=0.636\\pm0.053$", "$2.6\\sigma$"])
rng = []
for key in ("box_A", "box_B", "box_C"):
    v = list(PN["S3"][key].values()); rng.append(max(v) - min(v))
check("data", "S7e changing the H0 convention moves the three values by 0.05 to 0.10",
      0.045 <= min(rng) and max(rng) <= 0.10, f"ranges {[round(x,3) for x in rng]}", ["0.05 to 0.10"])
check("lit", "S7f Desmond a0 = 1.19 +- 0.10 ... (quoted as kappa only); Milgrom cH_Lambda/2pi; Riess H0 = 73.04", True, "", ["73.04"])
# estimator A uses 24 galaxies with y<0.05 (git-ignored v3 output, regenerated by reproduce_all.sh)
fA = os.path.join(V3, "reproduce_outputs", "estimator_A.out")
if os.path.exists(fA):
    ok24 = "y_cut = 0.05 (N = 24" in open(fA).read()
    check("data", "S7g estimator A uses N = 24 galaxies at y_cut = 0.05 (v3 estimator_A.out, git-ignored)", ok24, "", ["24 deep galaxies"])
else:
    check("data", "S7g estimator A N = 24: v3 estimator_A.out ABSENT -> run ../mnras_submission_2026_v3/reproduce_all.sh", False, "file missing", ["24 deep galaxies"])
check("data", "S7h estimator C uses all 3391 points", PN["S3_C"]["EC"]["n_pts"] == 3391, "", ["3391"])

# 6. H0 degeneracy
r_h0 = 67.4 / 73.04
r_k = kap_h / 0.500   # kappa(c H_Lambda/2pi) = 0.4607 unrounded
lock = PN["S3"]["lock_ratio"]
kh = 0.5 * 67.4 / 73.04                                      # kappa that matches at H0 = 73.04 is 0.5*67.4/73.04
check("algebra", "S8 sqrt(G rho_L) = H0 sqrt(3 Omega_L / 8 pi) exactly; 67.4/73.04 = 0.923; 0.461/0.500 = 0.921; a0 equal to 0.2%",
      close(sq, H0 * math.sqrt(3 * 0.685 / (8 * math.pi)), 1e-12) and close(r_h0, 0.923, 1e-3) and close(r_k, 0.921, 1e-3)
      and abs(1 - lock) < 2.5e-3, f"67.4/73.04 = {r_h0:.4f}; {kap_h:.4f}/0.5 = {r_k:.4f} (rounded 0.461/0.500 would be {0.461/0.5:.4f}); lock {lock:.5f}", ["$0.923$", "$0.4607/0.500=0.921$", "$0.2$ per cent"])

# 7. Three predictions
Om, OL = 0.315, 0.685
E2 = Om * 3.5**3 + OL
E = math.sqrt(E2)
dH = math.log10(E)
check("algebra", "S9 E^2(2.5) = 0.315*3.5^3 + 0.685 = 14.19, E = 3.77, Delta_H = +0.58; 3.5^3 = 42.875",
      close(3.5**3, 42.875, 1e-12) and close(E2, 14.19, 1e-3) and close(E, 3.77, 2e-3) and round(dH, 2) == 0.58,
      f"E2={E2:.3f} E={E:.4f} Delta_H={dH:.4f}", ["14.19", "$E=3.77$", "+0.58", "3.8"])
check("data", "S9b committed Delta_H(2.5) = 0.576", close(PN["S4"]["laws"][2]["Hz"], dH, 1e-3), "")
check("algebra", "S9c the two readings differ by 21% today (1/sqrt(0.685) = 1.208) and by a factor E(2.5) = 3.8 at z = 2.5",
      close(1 / math.sqrt(0.685), 1.208, 1e-3) and close(E, 3.8, 1e-2), "", ["21 per cent", "factor 3.8"])
# NFW halo (Dutton & Maccio 2014), reproduced independently
h = 0.674


def c200(z, M=1e12):
    a = 0.520 + 0.385 * math.exp(-0.617 * z**1.21)
    b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M / (1e12 / h)))


def f(x):
    return math.log(1 + x) - x / (1 + x)


c0, cz = c200(0), c200(2.5)
term_H = (4 / 3) * dH
term_c = math.log10((cz**2 / f(cz)) / (c0**2 / f(c0)))
d_halo = term_H + term_c
laws = PN["S4"]["laws"][2]
check("algebra", "S10 NFW rise: (4/3) log E = +0.77; concentration term -0.44; sum +0.33 for 1e12 Msun",
      close(term_H, 0.77, 5e-3) and close(term_c, -0.44, 1e-2, 0.006) and close(d_halo, 0.33, 2e-2) and close(d_halo, laws["dm14"], 1e-2, 0.006),
      f"{term_H:.3f} {term_c:.3f} sum {d_halo:.3f} (committed {laws['dm14']:.3f}); c200 {c0:.2f} -> {cz:.2f}",
      ["$\\tfrac43\\log_{10}E=+0.77$", "subtracts $0.44$", "$+0.33$"])
gl = laws["gate"]
check("data", "S10b the gated haloes rise by +0.22 (committed 0.216); across halo mass and model +0.17 to +0.56",
      round(gl, 2) == 0.22 and round(PN["S4"]["gate_D_range"][0], 2) == 0.17 and round(PN["S4"]["vmax_scaling_z25"], 2) == 0.56,
      f"gate {gl:.4f}, range low {PN['S4']['gate_D_range'][0]:.4f}, Vmax scaling {PN['S4']['vmax_scaling_z25']:.4f}",
      ["$+0.22$", "$+0.17$ to $+0.56$"])

# 8. Error amplification: derivation by hand vs numerical solve
def nu(y): return 1 / (1 - math.exp(-math.sqrt(y)))
def n_formula(y):
    s = math.sqrt(y); return -(s / 2) / math.expm1(s)
def n_numeric(y, eps=1e-6):
    return (math.log(nu(y * (1 + eps))) - math.log(nu(y * (1 - eps)))) / (math.log(1 + eps) - math.log(1 - eps))
okn = all(abs(n_formula(y) - n_numeric(y)) < 1e-6 for y in (0.01, 0.1, 0.3, 1, 2.4, 6.4))
check("algebra", "S11 n = -(sqrt(y)/2)/(exp(sqrt(y))-1) equals the numerical d ln(nu)/d ln(y)", okn, "6 values of y", ["n=-\\frac{\\sqrt y/2}{e^{\\sqrt y}-1}"])


def a0_hat(gobs, gbar):
    yy = brentq(lambda y: nu(y) - gobs / gbar, 1e-8, 1e6)
    return gbar / yy


ok_amp = True
for y in (0.01, 0.3, 2.4, 6.4):
    gbar0 = 1e-10 * y; gobs0 = nu(y) * gbar0; eps = 1e-5
    dg_obs = math.log(a0_hat(gobs0 * (1 + eps), gbar0) / a0_hat(gobs0, gbar0)) / eps
    dg_bar = math.log(a0_hat(gobs0, gbar0 * (1 + eps)) / a0_hat(gobs0, gbar0)) / eps
    n = n_formula(y)
    ok_amp &= abs(dg_obs - (-1 / n)) < 2e-3 * abs(1 / n) and abs(dg_bar - (1 + 1 / n)) < 2e-3 * max(1, abs(1 + 1 / n))
check("algebra", "S11b d ln a0_hat = -(1/n) d ln g_obs + (1 + 1/n) d ln g_bar equals a numerical re-solve of nu(y) = g_obs/g_bar",
      ok_amp, "perturbing g_obs and g_bar by 1e-5 at y = 0.01, 0.3, 2.4, 6.4", ["-\\frac1n\\,{\\rm d}\\ln g_{\\rm obs}"])
Ab = lambda y: 1 / abs(n_formula(y)) - 1
Ao = lambda y: 1 / abs(n_formula(y))
check("algebra", "S12 A_obs = 2, A_bar = 1 deep; A_bar = 1.1 (y=0.01), 1.7 (0.3), 3.8 (2.4), 8.1 (6.4); A_obs(0.3) = 2.7; A_bar(0.3) = 1.7",
      close(Ao(1e-8), 2, 1e-3) and close(Ab(1e-8), 1, 1e-3) and round(Ab(0.01), 1) == 1.1 and round(Ab(0.3), 1) == 1.7
      and round(Ab(2.4), 1) == 3.8 and round(Ab(6.4), 1) == 8.1 and round(Ao(0.3), 1) == 2.7,
      f"A_bar {[round(Ab(y),3) for y in (0.01,0.3,2.4,6.4)]}, A_obs(0.3) {Ao(0.3):.3f}",
      ["$A_{\\rm bar}=1.1$ at $y=0.01$, $1.7$ at $y=0.3$, $3.8$ at $y=2.4$ and $8.1$ at $y=6.4$", "$A_{\\rm obs}\\le2.7$ and $A_{\\rm bar}\\le1.7$"])
amp = {round(r["y"], 2): r for r in PN["S4"]["amplification"]}
check("data", "S12b matches the committed amplification table (y = 0.01, 0.3, 6.4)",
      all(close(amp[y]["A_bar"], Ab(y), 1e-6) for y in (0.01, 0.3, 6.4)), "")

# 9. RC100 (data)
yn = PN["S5_native"]["y_native"]
cens = PN["S5_native"]["censoring"]["bins"]
ntot = sum(b["n"] for b in cens)
fl = {tuple(b["z"]): b for b in cens}
check("data", "S13 RC100 native route: median y = 2.4, central 68% 0.9 < y < 7.2, 100 discs, 41 at the Newtonian floor",
      round(yn["median"], 1) == 2.4 and round(yn["p16"], 1) == 0.9 and round(yn["p84"], 1) == 7.2 and ntot == 100
      and PN["S5_native"]["n_D_le_1"] == 41,
      f"median {yn['median']:.3f}, p16 {yn['p16']:.3f}, p84 {yn['p84']:.3f}, n {ntot}, floor {PN['S5_native']['n_D_le_1']}",
      ["$y=2.4$", "$0.9<y<7.2$", "41 of the 100 discs", "100 discs"])
check("data", "S13b floor share 27% at z<1 (7/26) and 51% at z>2 (21/41)",
      round(100 * 7 / 26) == 27 and round(100 * 21 / 41) == 51 and fl[(0.5, 1.0)]["floor"] == 7 and fl[(2.0, 2.6)]["floor"] == 21,
      f"{100*7/26:.1f}%, {100*21/41:.1f}%", ["27 per cent of discs at $z<1$, 51 per cent at $z>2$"])
Abm = Ab(yn["median"])
check("algebra", "S13c at the RC100 median A_bar = 3.8, so 0.2 dex in baryonic mass becomes 0.76 dex in a0",
      round(Abm, 1) == 3.8 and close(0.2 * Abm, 0.76, 1e-2), f"A_bar {Abm:.3f}, x0.2 = {0.2*Abm:.3f}", ["$A_{\\rm bar}=3.8$", "$0.76$ dex"])
check("lit", "S13d RC100 = Nestor Shachar+23, z 0.6-2.5; Tacconi+18 gas; Ciocan+26 / long-version Sect. 4.3 (route dependence)", True, "", ["$0.6<z<2.5$"])

# 10. Gate: M_b < 0.3 a0 R^2 / (Gamma G)
kpc, Msun = 3.086e19, 1.989e30
Mb = 0.3 * 9.36e-11 * kpc**2 / (1.2 * 6.674e-11)
check("algebra", "S14 gate: M_b < 0.3 a0 R^2/(Gamma G) = 1.7e8 Msun (R/kpc)^2",
      round(Mb / Msun / 1e8, 1) == 1.7, f"{Mb:.3e} kg = {Mb/Msun:.3e} Msun", ["1.7\\times10^{8}", "3.086\\times10^{19}", "1.989\\times10^{30}", "0.3\\,(9.36\\times10^{-11})"])

# 11. How many galaxies
D = PN["S4"]["delta_gate"]
k20 = math.sqrt(2 * math.log(20))
check("algebra", "S15 sqrt(2 ln 20) = 2.45; sigma/sqrt(N) <= Delta/2.45: 0.216/2.45 = 0.088 (halo), 0.576/2.45 = 0.24 (H(z))",
      close(k20, 2.45, 2e-3) and round(D / k20, 3) == 0.088 and round(dH / k20, 2) == 0.24 and round(D, 3) == 0.216 and round(dH, 3) == 0.576,
      f"{k20:.4f}, {D/k20:.4f}, {dH/k20:.4f}", ["2.45", "0.216/2.45=0.088", "0.576/2.45=0.24"])
# equal-width derivation: expectation of ln B by Monte Carlo
rng_ = np.random.default_rng(7)
sig, Dl = 0.2, 0.216
x = rng_.normal(Dl, sig, 2_000_000)
lnB = (x**2 - (x - Dl) ** 2) / (2 * sig**2)                  # ln p(x|Delta)/p(x|0) when Delta is true
check("algebra", "S15b <ln B> = Delta^2/(2 sigma^2) for equal Gaussian widths (Monte Carlo, 2e6 draws)",
      close(lnB.mean(), Dl**2 / (2 * sig**2), 3e-3), f"MC {lnB.mean():.4f} vs {Dl**2/(2*sig**2):.4f}", ["\\Delta^2/2\\sigma^2"])
A03 = Ao(0.3)
s_int = 0.034 * A03
s_h = PN["S4"]["halo_scatter_single"]
sm = 0.20
s0 = math.sqrt(sm**2 + s_int**2); s1 = math.sqrt(s0**2 + s_h**2)
k_const = math.log(s1 / s0) - 0.5 + (s0**2 + D**2) / (2 * s1**2)
k_halo = math.log(s0 / s1) - 0.5 + (s1**2 + D**2) / (2 * s0**2)
# numerical check of the closed form by Monte Carlo
xs = rng_.normal(0, s0, 2_000_000)
lnb_mc = (-(xs**2) / (2 * s0**2) - math.log(s0)) - (-((xs - D) ** 2) / (2 * s1**2) - math.log(s1))
check("algebra", "S16 per-galaxy <ln B> (constancy true) = 0.375 and (haloes true) = 0.513; closed form equals Monte Carlo",
      close(lnb_mc.mean(), k_const, 3e-3) and round(k_const, 3) == 0.375 and round(k_halo, 3) == 0.513,
      f"s_int {s_int:.4f}, s_h {s_h:.4f}, s0 {s0:.4f}, s1 {s1:.4f}; const {k_const:.4f} (MC {lnb_mc.mean():.4f}), halo {k_halo:.4f}",
      ["$s_0=0.2195$", "$s_1=0.2575$", "adds $0.375$", "0.513", "$\\sigma_{\\rm int}=0.034A_{\\rm obs}(0.3)=0.09$", "$\\sigma_{\\rm h}=0.135$"])
odds = lambda N: math.exp(N * min(k_const, k_halo))
check("algebra", "S16b eight galaxies give 20:1, seven give 14:1 (committed design 20.06 at N = 8, sigma_m = 0.20)",
      round(odds(8)) == 20 and round(odds(7)) == 14 and close(odds(8), PN["S4"]["design"]["0.2|0.0"]["odds_at_Ne"], 1e-6)
      and PN["S4"]["N_rec"] == 8, f"N=8 {odds(8):.3f}, N=7 {odds(7):.3f}", ["$e^{8\\times0.375}=20:1$", "seven give $14:1$"])
dz = PN["S4"]["design"]["0.2|0.0"]
check("data", "S16c Monte Carlo: chance of reaching 20:1 is 0.53 with eight galaxies; 20 galaxies for 0.9",
      round(dz["p20_at_Ne"][0], 2) == 0.53 and dz["N_power90"] == 20, f"{dz['p20_at_Ne']}, N90 {dz['N_power90']}", ["0.53", "20 are needed for 0.9"])

# 12. Shared calibration: N-dimensional KL between Gaussians with covariance s^2 I + sC^2 J
def kl_shared(N, sa, sb, sC, mu_on_a):
    """KL( p_a || p_b ) for N galaxies, p_a: mean mu_on_a * 1, cov sa^2 I + sC^2 J ; p_b: mean 0 ... see below.
    Only the ones-direction carries the mean; eigenvalues of s^2 I + sC^2 J are s^2 (N-1 times) and s^2 + N sC^2 (once)."""
    lam_a, lam_b = sa**2 + N * sC**2, sb**2 + N * sC**2
    tr = (N - 1) * sa**2 / sb**2 + lam_a / lam_b
    logdet = (N - 1) * math.log(sb**2 / sa**2) + math.log(lam_b / lam_a)
    return 0.5 * (tr - N + logdet + N * mu_on_a**2 / lam_b)


def N_for_20(dc, y=0.2):
    sC = Ab(y) * dc
    for N in range(1, 2000):
        kl_const_true = kl_shared(N, s0, s1, sC, D)       # data ~ N(0, s0^2 I + sC^2 J), alternative N(D, s1^2 I + sC^2 J)
        kl_halo_true = kl_shared(N, s1, s0, sC, D)        # data ~ N(D, s1^2 I + sC^2 J), alternative N(0, s0^2 I + sC^2 J)
        if math.exp(min(kl_const_true, kl_halo_true)) >= 20:
            return N
    return None


# cross-check the closed form against brute-force matrices at N = 8 (small, well conditioned)
_N, _sC = 8, Ab(0.2) * 0.05
_I, _J = np.eye(_N), np.ones((_N, _N)); _mu = D * np.ones(_N)
_S0, _S1 = s0**2 * _I + _sC**2 * _J, s1**2 * _I + _sC**2 * _J
_kl = 0.5 * (np.trace(np.linalg.inv(_S1) @ _S0) - _N + np.linalg.slogdet(_S1)[1] - np.linalg.slogdet(_S0)[1] + _mu @ np.linalg.inv(_S1) @ _mu)
check("algebra", "S17a closed form of the N-galaxy KL (eigenvalues s^2, s^2 + N sC^2) equals the brute-force matrix KL at N = 8",
      close(_kl, kl_shared(_N, s0, s1, _sC, D), 1e-9), f"{_kl:.6f} vs {kl_shared(_N, s0, s1, _sC, D):.6f}", [])


Nn = {dc: N_for_20(dc) for dc in (0.0, 0.04, 0.05, 0.06)}
committed = {float(k): v for k, v in PN["S4"]["N20_vs_delta_c"].items()}
check("algebra", "S17 galaxies needed for 20:1 with shared calibration error: 8, 14, 20, 34 at delta_c = 0, 0.04, 0.05, 0.06 dex (full N-dimensional KL)",
      [Nn[k] for k in (0.0, 0.04, 0.05, 0.06)] == [8, 14, 20, 34] and all(Nn[k] == committed[k] for k in Nn),
      f"{Nn}", ["from eight at $\\delta_c=0$ to 14, 20 and 34 at $\\delta_c=0.04$, $0.05$ and $0.06$"])
Abar2 = Ab(0.2)
d_h = D / (k20 * Abar2); d_H = dH / (k20 * Abar2)
check("algebra", "S17b delta_c limits: A_bar(0.2) = 1.52; 0.216/(2.45*1.52) = 0.058 (haloes); 0.576/(2.45*1.52) = 0.155 (H(z))",
      round(Abar2, 2) == 1.52 and round(d_h, 3) == 0.058 and round(d_H, 3) == 0.155
      and close(d_h, PN["S4"]["delta_c_needed"]["halo"], 5e-3) and close(d_H, PN["S4"]["delta_c_needed"]["Hz"], 5e-3),
      f"A_bar {Abar2:.4f}, {d_h:.4f}, {d_H:.4f}", ["$A_{\\rm bar}=1.52$", "0.058\\ \\text{dex (haloes)}", "0.155\\ \\text{dex ($H(z)$)}"])
# extra information (not quoted): galaxies needed just above the limit, to state in the notes
Nabove = N_for_20(0.07)
check("algebra", "S17c just above the 0.058 limit (delta_c = 0.07 dex) the full KL (mean AND spread) still reaches 20:1, at N = 52; the sample mean alone cannot",
      Nabove == 52, f"N = {Nabove}", ["at $\\delta_c=0.07$ dex, 52 galaxies would give 20:1"])

# 12b. dex <-> factors used in the abstract and Section 1
check("algebra", "S17d dex conversions: 0.3 dex = x2.0, 1 dex = x10, 0.06 dex = 15%, 0.58 dex = x3.8, gated halo rise 0.216 dex = x1.6",
      round(10**0.3, 1) == 2.0 and 10**1 == 10 and round(100 * (10**0.06 - 1)) == 15 and round(10**dH, 1) == 3.8 and round(10**D, 1) == 1.6,
      f"{10**0.3:.3f}, {100*(10**0.06-1):.1f}%, {10**dH:.3f}, {10**D:.3f}",
      ["0.3 dex is a factor 2", "0.06 dex is 15 per cent", "3.8 times", "about 1.6 times"])

# 13. Common-calibration degeneracy: g_obs^2 = g_bar a0 -> f a0
fcal, a0x = 1.3, 1.1e-10
gb0 = 4e-12
check("algebra", "S18 scaling every mass by f leaves only the product f*a0 in the deep limit",
      close(math.sqrt(gb0 * fcal * a0x), math.sqrt((fcal * gb0) * a0x), 1e-12), "")

# 14. Registry of numbers that are not computed above (cited literature, definitions, trivial text values)
for q, why in (("1.2\\times10^{-10}", "a0 ~ 1.2e-10 (McGaugh+16)"), ("0.18", "A_bar scale text 0.18 (kappa move 0.18 in abstract)"),
               ("0.15", "-"), ("0.2", "-")):
    pass
# the abstract's "0.18" would be a number with 2 decimals: check it
span = tab[0.5]["kappa_L"] - tab[0.7]["kappa_L"]
check("data", "S19 (abstract/limits) the standard-fit kappa moves by about 0.18 across Upsilon = 0.5-0.7", round(span, 2) == 0.18, f"{span:.4f}", [])
check("lit", "S20 DESI 2025: dark-energy mapping gives about -0.1 dex at z = 2.5 (committed v3 S4 laws: -0.085..-0.111)",
      -0.12 < laws["desi"]["DESY5"] < -0.08, f"DESY5 {laws['desi']['DESY5']:.3f}", ["$-0.1$ dex"])
check("lit", "S21 Milgrom+99/2020, Limbach+08 (redshift test to z = 1.2), Navarro+17: cited, not computed", True, "", ["$z=1.2$"])

# =====================================================================================================================
# every number with >= 2 decimals in the .tex must be registered above (as a quoted string or a literature/definition value)
ALLOWED_EXTRA = {
    # definitions / literature values / bibliographic items that are not results of this paper
    "0.02", "0.24", "1.20", "0.20", "0.30", "0.05", "0.10", "0.00", "0.1", "1.2", "1.7", "0.3", "0.2",
    "73.04", "67.4", "0.685", "0.315", "3.5", "2.99792", "6.6743", "3.08568", "2018.04", "0.034", "2026.12", "0.500",
    "3.086", "1.989", "0.443", "1.52", "0.461",
}
body = TEX[TEX.index(r"\begin{abstract}"):TEX.index(r"\bibliographystyle")]
body = re.sub(r"\\url\{[^}]*\}|\\nolinkurl\{[^}]*\}|\\texttt\{[^}]*\}|\\label\{[^}]*\}|\\citep?[a-z]*(\[[^\]]*\])*\{[^}]*\}", "", body)
nums = sorted(set(re.findall(r"(?<![\w.])\d+\.\d{2,}(?![\w])", body)))
unreg = [n for n in nums if not any(n in q for q in QUOTES) and n not in ALLOWED_EXTRA]
check("data", "S99 every number with two or more decimals in the text is registered above", not unreg,
      f"{len(nums)} distinct numbers; unregistered: {unreg}", [])

# =====================================================================================================================
w = max(len(r[1]) for r in ROWS)
for kind, label, ok, detail, miss in ROWS:
    print(f"[{'PASS' if ok else 'FAIL'}] [{kind:7s}] {label}" + (f"   ({detail})" if detail else "") + (f"   MISSING IN TEX: {miss}" if miss else ""))
n_k = {k: sum(1 for r in ROWS if r[0] == k) for k in ("algebra", "data", "lit")}
print(f"\n{len(ROWS)} checks ({n_k['algebra']} algebra, {n_k['data']} data, {n_k['lit']} literature); {len(FAILS)} FAIL")
if FAILS:
    print("FAILED:", "; ".join(FAILS))
    sys.exit(1)
print("ALL CHECKS PASSED")
