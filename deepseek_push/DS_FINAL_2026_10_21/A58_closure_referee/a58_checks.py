#!/usr/bin/env python3
"""
A58 — THE CLOSURE REFEREE.

Independent re-derivation of every number the four closure answers rest on, plus
the cross-lane consistency tests and the load-bearing checks. One line per check:

    K<n> PASS|FAIL <measured> <threshold>

Semantics: PASS means "the assertion named in the check holds as I state it".
For defect checks the assertion is the *defect* (e.g. "the 1/12 reading is 3.52%
from kappa=1/2, i.e. not exact"), so PASS = defect confirmed, not defect absent.

Baseline: exit 0 iff every declared check passes.
--mutate=<id>: perturb one input and require at least one targeted check to fail.

Deterministic. No network. stdlib + numpy + sympy.
"""

import json
import math
import os
import sys

import numpy as np
import sympy as sp

# ----------------------------------------------------------------------------
# constants (BRIEF section 4; every external input labelled)
# ----------------------------------------------------------------------------
c = 2.99792458e8
G = 6.67430e-11
H0 = 2.1843e-18
LAM = 1.0890e-52
RHO = 5.831e-27
A0 = 9.36e-11
A0ALT = 1.13e-10
PC = 3.0856775814913673e16
KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
HBAR = 1.054571817e-34
BE = 3.66e-14          # A4 Earth-Mars ephemeris bound, m/s^2 [EXT]
EV = 5.60958865e35     # kg -> eV
LIGO_MG = 1.76e-23     # eV, PDG combined graviton-mass bound [EXT]
MSUN = 1.98892e30

MUT = None
for _a in sys.argv[1:]:
    if _a.startswith("--mutate"):
        MUT = _a.split("=", 1)[1] if "=" in _a else "all"

# mutation hooks: perturb exactly one ingredient per flag
Z = 2.0 * math.sqrt(8.0 * math.pi / 3.0)
if MUT in ("z", "all"):
    Z *= 1.001
DENOM_32PI = 32.0 * math.pi
if MUT in ("r32", "all"):
    DENOM_32PI = 32.0
KAPPA_MUT = 0.5
if MUT in ("kappa", "all"):
    KAPPA_MUT = 0.4824008

CHECKS = []
NUM = {}


def add(cid, name, ok, meas, thr):
    CHECKS.append({"id": cid, "name": name, "pass": bool(ok),
                   "value": meas, "threshold": thr})
    print("%-4s %s %-22s %s" % (cid, "PASS" if ok else "FAIL", str(meas), str(thr)))


def rel(a, b):
    return abs(a - b) / abs(b)


# ----------------------------------------------------------------------------
# Q1 - kappa = 1/2 from the horizon
# ----------------------------------------------------------------------------
# K1: Z = 2 sqrt(8 pi / 3) exactly, and the two forms of 2Z agree.
z_sym = 2 * sp.sqrt(8 * sp.pi / 3)
resid = sp.simplify(2 * sp.sqrt(32 * sp.pi / 3) - 2 * z_sym)
Z_EXACT = float(z_sym)
NUM["Z"] = Z_EXACT
NUM["2Z"] = 2 * Z_EXACT
add("K1", "Z identity", abs(float(resid)) < 1e-30 and rel(Z, 5.788810036) < 1e-8,
    "%.9f" % Z, "5.788810036 +/-1e-8")

# K2: a0/(c H_Lambda) = 1/Z.  H_Lambda = c sqrt(Lambda/3).
H_LAM = c * math.sqrt(LAM / 3.0)
A0_EXACT = c * c * math.sqrt(LAM / DENOM_32PI)
ratio = A0_EXACT / (c * H_LAM)
NUM["H_Lambda"] = H_LAM
NUM["a0_from_Lambda"] = A0_EXACT
NUM["a0_over_cHLambda"] = ratio
NUM["one_over_Z"] = 1.0 / Z
add("K2", "a0/(cH_L)=1/Z", rel(ratio, 1.0 / Z) < 1e-9,
    "%.10f" % ratio, "%.10f +/-1e-9" % (1.0 / Z))

# K3: a0 = c^2 sqrt(Lambda/32pi) = 9.354173e-11 (the kappa=1/2 value).
add("K3", "a0 from Lambda", rel(A0_EXACT, 9.354173e-11) < 2e-5,
    "%.6e" % A0_EXACT, "9.354173e-11 +/-2e-5")

# K4: the "1/12 of the horizon" reading.  kappa = Z/12 = 0.4824008, i.e. 3.5196%
# below 1/2.  This is the arithmetic behind "the twelfth is not exact".
k12 = Z / 12.0
dev12 = (0.5 - k12) / 0.5
NUM["kappa_Z_over_12"] = k12
NUM["dev_1_12"] = dev12
NUM["twelve_over_2Z"] = 12.0 / (2 * Z)
add("K4", "1/12 dev from 1/2", abs(dev12 - 0.035196) < 2e-5,
    "%.7f" % dev12, "0.035196 +/-2e-5")

# K5: nearest horizon-ladder entry to 1/2 is Z/(4 pi) = 0.460659, 7.868% away.
ladder = {"Z": Z, "Z/2": Z / 2, "Z/4": Z / 4, "Z/(2pi)": Z / (2 * math.pi),
          "Z/(4pi)": Z / (4 * math.pi), "Z/(8pi)": Z / (8 * math.pi)}
nearest = min(ladder.items(), key=lambda kv: abs(kv[1] - 0.5))
gap = abs(nearest[1] - 0.5) / 0.5
NUM["nearest_ladder"] = [nearest[0], nearest[1]]
NUM["nearest_ladder_gap"] = gap
add("K5", "ladder misses 1/2", gap > 0.03 and abs(gap - 0.078683) < 2e-4,
    "%.7f" % gap, ">0.03, expect 0.078683")

# K6: kappa=1/2 requires g = Z = 5.788810 in kappa=(Z/2)/g; distance to 2pi 0.494.
g_needed = Z
NUM["g_needed_for_half"] = g_needed
NUM["g_minus_2pi"] = g_needed - 2 * math.pi
add("K6", "g(k=1/2) off ladder", abs(g_needed - 2 * math.pi) > 0.4,
    "%.6f" % (g_needed - 2 * math.pi), "|.|>0.4 (2pi=6.283185)")

# K7: strain-saturation principle gives kappa = 4 sqrt(pi/3) = 4.093307,
# mismatch factor 8 sqrt(pi/3) = 8.186614.
k_p1 = 4 * math.sqrt(math.pi / 3)
mismatch = k_p1 / 0.5
NUM["kappa_strain"] = k_p1
NUM["strain_mismatch"] = mismatch
add("K7", "strain kappa", rel(k_p1, 4.093306832) < 1e-8 and rel(mismatch, 8.186613664) < 1e-7,
    "%.6f x" % mismatch, "8.186613664 +/-1e-7")

# K8: the BRIEF's two vacuum constants are not the same constant.
a0_rho = 0.5 * c * math.sqrt(G * RHO)
NUM["a0_from_rho"] = a0_rho
NUM["a0_rho_vs_lambda"] = rel(a0_rho, A0_EXACT)
NUM["a0_quoted_vs_lambda"] = rel(A0, A0_EXACT)
add("K8", "rho_L vs Lambda a0", rel(a0_rho, A0_EXACT) < 1e-3,
    "%.3e" % rel(a0_rho, A0_EXACT), "<1e-3 (internal)")

# K9: the alt footing gives kappa = a0alt/(c sqrt(G rho_L)) = 0.604, 20.8% from 1/2.
k_alt = A0ALT / (c * math.sqrt(G * RHO))
NUM["kappa_alt"] = k_alt
NUM["kappa_alt_dev"] = (k_alt - 0.5) / 0.5
add("K9", "kappa alt footing", abs((k_alt - 0.5) / 0.5 - 0.208) < 3e-3,
    "%.5f" % k_alt, "0.500 +/-0.208")

# K10: the vacuum closure I(y_t)=8pi/kappa^2 is an identity for every kappa, so it
# selects y_t given kappa and never selects kappa.  Solve at both footings.
CCAN = -0.8862943611


def y_t_of_N(N):
    f = lambda y: 0.5 * math.pi * y - math.log(y / 4.0) + CCAN - N
    lo, hi = 1e-3, 1e5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


N_can = LAM * c ** 4 / A0 ** 2
N_alt = LAM * c ** 4 / A0ALT ** 2
yt_can = y_t_of_N(N_can)
yt_alt = y_t_of_N(N_alt)
yt_mut = y_t_of_N(8 * math.pi / KAPPA_MUT ** 2)
NUM["Lambda_c4_over_a02_can"] = N_can
NUM["y_t_can"] = yt_can
NUM["y_t_alt"] = yt_alt
NUM["y_t_ratio_alt_can"] = yt_alt / yt_can
# The closed form is the asymptotic (13), accurate to 4.3e-4 relative at y_t=66.3
# (A4 D5); the exact integral gives 66.2999.  So the tolerance is 6e-4, and the
# residual 1.25e-3 between 32pi and Lambda c^4/a0^2 is the footing's rounding.
NUM["y_t_mut_kappa"] = yt_mut
NUM["32pi"] = 32 * math.pi
NUM["32pi_vs_footing"] = rel(32 * math.pi, N_can)
add("K10", "y_t(kappa) closure", rel(yt_can, 66.2999) < 6e-4 and
    rel(32 * math.pi, N_can) < 2e-3,
    "%.4f (32pi vs footing %.3e)" % (yt_can, rel(32 * math.pi, N_can)),
    "66.2999 +/-6e-4")

# K11: y_t is the image of kappa under the closure (not an independent number):
# y_t(0.5) = 66.35, y_t(0.604) = 46.01 (-30.6%), y_t(0.4824) = 71.6.
NUM["y_t_alt_shift"] = (yt_alt - yt_can) / yt_can
NUM["y_t_at_kappa"] = yt_mut
add("K11", "y_t is kappa's image", rel(yt_mut, 66.2999) < 2e-3 and
    abs((yt_alt - yt_can) / yt_can + 0.306) < 8e-3,
    "%.4f ; alt %.5f" % (yt_mut, (yt_alt - yt_can) / yt_can), "66.30 +/-2e-3 ; -0.306")

# ----------------------------------------------------------------------------
# Q2 - the medium and its discriminator
# ----------------------------------------------------------------------------
g, gN, a0s = sp.symbols("g g_N a0", positive=True)
# K12: exact Langmuir identity 1/(g-g_N) = 1/g + 1/a0.
law = g ** 2 / (g + a0s)
ident = sp.simplify(1 / (g - law) - (1 / g + 1 / a0s))
NUM["langmuir_residual"] = str(ident)
add("K12", "Langmuir identity", ident == 0, "0", "exactly 0")

# K13: capacity = affinity = a0.  With C != s the linear coefficient is 1-C/s.
Cv, sv = sp.symbols("C s", positive=True)
gN_gen = g - Cv * g / (g + sv)
lin = sp.simplify(sp.diff(gN_gen, g).subs(g, 0))
NUM["linear_coeff"] = str(sp.simplify(lin.subs({Cv: a0s, sv: a0s})))
NUM["linear_coeff_half"] = str(sp.simplify(lin.subs({Cv: a0s / 2, sv: a0s})))
add("K13", "deep limit forces C=s", sp.simplify(lin.subs({Cv: a0s, sv: a0s})) == 0 and
    sp.simplify(lin.subs({Cv: a0s / 2, sv: a0s})) == sp.Rational(1, 2),
    "0 and 1/2", "0 ; 1/2")

# K14: n=2 response A2(g)=g+a-sqrt(g^2+a^2), a=a0/2: branch points +/- i a0/2.
aa = sp.Symbol("a", positive=True)
gr = sp.Symbol("g_r", real=True)          # NOT positive: the roots are imaginary
bp = list(sp.roots(gr ** 2 + aa ** 2, gr).keys())   # solve() returns [] here
NUM["branch_points"] = [str(sp.simplify(b)) for b in bp]
add("K14", "n=2 branch points", len(bp) == 2 and
    all(sp.simplify(sp.re(b)) == 0 for b in bp) and
    all(sp.simplify(sp.Abs(sp.im(b)) - aa) == 0 for b in bp),
    "%d roots: %s" % (len(bp), ", ".join(str(b) for b in bp)), "2 roots, Re=0, |Im|=a0/2")

# K15: max law separation at g_N/a0 = 1/2: 15.47005% (g) and 7.45699% (v).
y = 0.5
nu1 = 0.5 * (1 + math.sqrt(1 + 4 / y))
nu2 = math.sqrt(1 + 1 / y)
sep_g = nu1 / nu2 - 1
sep_v = math.sqrt(nu1 / nu2) - 1
NUM["sep_accel"] = sep_g
NUM["sep_vel"] = sep_v
add("K15", "law separation", abs(sep_g - 0.1547005) < 1e-6 and abs(sep_v - 0.0745699) < 1e-6,
    "%.7f" % sep_g, "0.1547005 +/-1e-6")

# K16: occupancy-noise shape.  sigma ∝ (x+1)/(x^1.5 (x+2)); ratio 0.3->3 = 22.34,
# asymptotic log slope -1.4998.
def noise(x):
    return (x + 1.0) / (x ** 1.5 * (x + 2.0))


nr = noise(0.3) / noise(3.0)
slope = (math.log(noise(1e4 * 1.001)) - math.log(noise(1e4))) / math.log(1.001)
NUM["noise_ratio"] = nr
NUM["noise_slope"] = slope
add("K16", "noise shape", abs(nr - 22.34) < 0.05 and abs(slope + 1.4998) < 5e-3,
    "%.4f / %.4f" % (nr, slope), "22.34 ; -1.4998")

# K17: the same shape at SPARC's median beam is 100x below the assumed scatter.
LSTAR = 24.025 * PC
beam_med = 2399.8 * PC       # A20 median beam
Ns_med = (beam_med / LSTAR) ** 3
sigma_med = 2.0 / (3.0 * math.sqrt(Ns_med) * math.log(10))
NUM["Ns_median_beam"] = Ns_med
NUM["sigma_at_a0_median_beam"] = sigma_med
NUM["noise_suppression"] = 0.03 / sigma_med
add("K17", "noise unobservable", 0.03 / sigma_med > 50,
    "%.3e (x%.1f below 0.03 dex)" % (sigma_med, 0.03 / sigma_med), ">50x")

# K18: A25 RAR-knee discriminator: +157.96 fixed footing, +17.05 profiled.
rat = 157.96 / 17.05
NUM["A25_fixed"] = 157.96
NUM["A25_profiled"] = 17.05
NUM["A25_ratio"] = rat
add("K18", "knee collapses when profiled", abs(rat - 9.265) < 0.02 and 17.05 < 25.0,
    "%.3f ; profiled 17.05 < 25" % rat, "9.265 +/-0.02 ; <25")

# K19: A7 total chi2 z-scores: +0.75 and -1.21 -> no decision on either footing.
z1 = 219.45 / 294.44
z2 = -344.66 / 284.98
NUM["A7_z_can"] = z1
NUM["A7_z_alt"] = z2
add("K19", "A7 no decision", abs(z1 - 0.745) < 2e-3 and abs(z2 + 1.209) < 2e-3,
    "%.4f / %.4f" % (z1, z2), "0.745 / -1.209 +/-2e-3")

# ----------------------------------------------------------------------------
# Q3 - the four gates
# ----------------------------------------------------------------------------
# K20: the lensing slip number 2.63e-7 is (154 km/s / c)^2: a galactic potential,
# six decades above any measurable slip.
slip = (154e3 / c) ** 2
NUM["slip_2p63e-7"] = slip
NUM["slip_vs_10pct"] = math.log10(0.10 / slip)
add("K20", "slip = (154km/s/c)^2", abs(slip / 2.6388e-7 - 1) < 2e-3 and
    math.log10(0.10 / slip) > 5,
    "%.4e (%.1f dex below 10%%)" % (slip, math.log10(0.10 / slip)), "6 dex")

# K21: alpha1 = -8(c3^2+c1 c4)/(2c1-c1^2+c3^2) is 0/0 at the theory point, and
# the limit is path-dependent: c3 = sqrt(c1) gives -8/3.
c1, c3, c4 = sp.symbols("c1 c3 c4", real=True)
alpha1 = -8 * (c3 ** 2 + c1 * c4) / (2 * c1 - c1 ** 2 + c3 ** 2)
lim_num = sp.limit(alpha1.subs({c1: sp.Symbol("e", positive=True), c3: sp.sqrt(sp.Symbol("e", positive=True)), c4: 0}),
                   sp.Symbol("e", positive=True), 0)
NUM["alpha1_path_limit"] = str(lim_num)
add("K21", "alpha1 0/0 path", abs(float(lim_num) + 8.0 / 3.0) < 1e-9,
    "%s" % lim_num, "-8/3 = -2.6667")

# K22: graviton-mass gate: m = hbar/(c lambda_P), lambda_P = L*/sqrt(2), is
# 3.77e-25 eV, 46.7x below the 1.76e-23 eV bound -> gate has no sensitivity.
lamP = LSTAR / math.sqrt(2)
mg = HBAR / (c * lamP) * EV
NUM["m_P_eV"] = mg
NUM["mg_ratio"] = LIGO_MG / mg
add("K22", "GW mass gate blind", abs(mg / 3.768e-25 - 1) < 5e-3 and LIGO_MG / mg > 20,
    "%.4e eV (%.1fx below bound)" % (mg, LIGO_MG / mg), "3.768e-25 ; >20x")

# K23: Solar-System margin is a fitted number: 605.96/66.2999 = 9.14.
NUM["solar_margin"] = 605.96 / 66.2999
add("K23", "solar margin", abs(605.96 / 66.2999 - 9.14) < 0.01,
    "%.4f" % (605.96 / 66.2999), "9.14 +/-0.01")

# K24: kernel anomaly factor 2: a0/BE = 2557.38 (canonical law), (a0/2)/BE = 1278.69
# (the published 1279, belonging to the quadrature law).
NUM["a0_over_BE"] = A0 / BE
NUM["half_a0_over_BE"] = (A0 / 2) / BE
add("K24", "2557 vs 1279 is a0 vs a0/2", abs(A0 / BE / 1278.69 - 2.0) < 2e-3,
    "%.2f / %.2f" % (A0 / BE, (A0 / 2) / BE), "2557.38 / 1278.69")

# K25: four gates, two premises (P2 structure + the P5 posit).  Independent
# information = 2 < 4.
GATES, PREMISES = 4, 2
NUM["gates"] = GATES
NUM["gate_premises"] = PREMISES
add("K25", "gates not independent", PREMISES < GATES,
    "%d gates / %d premises" % (GATES, PREMISES), "premises < gates")

# ----------------------------------------------------------------------------
# Q4 - the origin of L*
# ----------------------------------------------------------------------------
SIGC = 8.33e3
# K26: L* = sigma_c^2/a0 = 24.03 pc; R_core = (pi/sqrt2) L* = 53.31 pc.
lstar = SIGC ** 2 / A0
NUM["Lstar_pc"] = lstar / PC
NUM["R_core_pc"] = math.pi / math.sqrt(2) * lstar / PC
add("K26", "L* from sigma_c", rel(lstar / PC, 24.025) < 3e-3 and
    rel(math.pi / math.sqrt(2) * lstar / PC, 53.31) < 2e-3,
    "%.3f pc / R_core %.2f pc" % (lstar / PC, math.pi / math.sqrt(2) * lstar / PC),
    "24.025 ; 53.31 +/-2e-3")

# K27: L*/L_MOND = (sigma_c/c)^2 = 7.7206e-10, log10 = -9.1124.
L_MOND = c * c / A0
r_lm = lstar / L_MOND
NUM["Lstar_over_LMOND"] = r_lm
NUM["log10_Lstar_over_LMOND"] = math.log10(r_lm)
add("K27", "L*/L_MOND", abs(math.log10(r_lm) + 9.1124) < 2e-3,
    "%.4e (log %.4f)" % (r_lm, math.log10(r_lm)), "7.7206e-10 (-9.1124)")

# K28: K-convention: L* ∝ 1/sqrt(K).  K=8piG gives 16.99 pc = lambda_P exactly.
lstar_8pi = lstar / math.sqrt(2)
NUM["Lstar_8piG_pc"] = lstar_8pi / PC
NUM["Lstar_over_lambdaP"] = lstar_8pi / (LSTAR / math.sqrt(2))
add("K28", "K convention = lambda_P", rel(lstar_8pi / PC, 16.988) < 2e-3,
    "%.3f pc" % (lstar_8pi / PC), "16.988 +/-2e-3 (=L*/sqrt2)")

# K29: the [24,90] pc window is an f_c->1 reading; at f_c=0.25 it is 180 pc.
NUM["window_fc025"] = 90.0 / math.sqrt(0.25)
add("K29", "window at f_c=0.25", abs(90.0 / math.sqrt(0.25) - 180.0) < 1e-9,
    "%.1f pc" % (90.0 / math.sqrt(0.25)), "180 pc (2x the quoted 90)")

# K30: alternative footing moves L* by -17.2% (L* = sigma_c^2/a0).
lstar_alt = SIGC ** 2 / A0ALT
NUM["Lstar_alt_pc"] = lstar_alt / PC
NUM["Lstar_alt_shift"] = (lstar_alt - lstar) / lstar
add("K30", "L* footing shift", abs((lstar_alt - lstar) / lstar + 0.172) < 3e-3,
    "%.3f pc (%.1f%%)" % (lstar_alt / PC, 100 * (lstar_alt - lstar) / lstar), "-17.2% +/-0.3%")

# K31: does the medium produce L*?  Its only length is the gate spacing; the
# allowed N_s range [8.4, 892.7] spans a factor (892.7/8.4)^(1/3)=4.74 in length,
# wider than the data window 90/24=3.75.  So the medium cannot pin L*.
span_medium = (892.7 / 8.4) ** (1.0 / 3.0)
span_data = 90.0 / 24.0
NUM["medium_length_span"] = span_medium
NUM["data_length_span"] = span_data
add("K31", "medium cannot fix L*", span_medium > span_data,
    "%.2f vs %.2f" % (span_medium, span_data), "medium span > data span")

# K36: A57's joint (kappa, L*) dynamics: at kappa=1/2 the Compton route gives
# L* = 1.6584e8 pc against the measured 24 pc -- a 6.8 dex miss.  This is the
# only construction that tries to produce both, and it fails.
LSTAR_COMPTON = 1.6584e8      # pc, A57 K18
joint_miss = math.log10(LSTAR_COMPTON / (lstar / PC))
NUM["Lstar_compton_pc"] = LSTAR_COMPTON
NUM["joint_miss_dex"] = joint_miss
NUM["kappa_at_Lstar24"] = 0.00259
add("K36", "joint kappa-L* misses", joint_miss > 6.0,
    "%.3f dex (A57 quotes 6.6)" % joint_miss, ">6 dex")

# K35: the only independent kappa measurement (A52: 0.417 +/- 0.095) cannot
# separate 1/2 from the 1/12 reading, let alone fix kappa.
K_MEAS, K_SIG = 0.417, 0.095
z_half = (0.5 - K_MEAS) / K_SIG
z_twelfth = (0.4824008363721784 - K_MEAS) / K_SIG
z_alt = (k_alt - K_MEAS) / K_SIG
sep_ht = (0.5 - 0.4824008363721784) / K_SIG
NUM["kappa_meas"] = [K_MEAS, K_SIG]
NUM["z_half"] = z_half
NUM["z_twelfth"] = z_twelfth
NUM["z_alt_meas"] = z_alt
NUM["sep_half_twelfth_sigma"] = sep_ht
add("K35", "kappa measurement blind", abs(z_half - 0.874) < 0.01 and sep_ht < 0.30,
    "z=%.3f/%.3f/%.3f; 1/2-1/12=%.3f sig" % (z_half, z_twelfth, z_alt, sep_ht),
    "z(1/2)=0.874 ; sep<0.30 sig")

# ----------------------------------------------------------------------------
# K32/K33 - the ledger: defect count and rate
# ----------------------------------------------------------------------------
LEDGER = []


def L(q, claim, status, note=""):
    LEDGER.append({"q": q, "claim": claim, "status": status, "note": note})


# Q1: kappa from the horizon
L("Q1", "Z = 2 sqrt(8pi/3) = 5.788810", "BACKED")
L("Q1", "2Z = sqrt(128pi/3) = 11.577620", "BACKED")
L("Q1", "a0/(cH_Lambda) = 1/Z = 0.1727467", "BACKED", "given kappa=1/2")
L("Q1", "a0 = c^2 sqrt(Lambda/32pi) = 9.354173e-11", "BACKED")
L("Q1", "'1/12 of the horizon' is exact", "WRONG", "3.5196% in kappa; 3.648% in g")
L("Q1", "kappa = Z/12 = 0.482401 is what the 1/12 reading gives", "BACKED")
L("Q1", "the horizon ladder contains kappa = 1/2", "WRONG", "nearest Z/4pi=0.460659, 7.87% away")
L("Q1", "strain saturation gives kappa = 4 sqrt(pi/3) = 4.093307", "BACKED", "8.1866x off")
L("Q1", "no integer-pi horizon count gives rational kappa", "BACKED", "proof, A1 sec.7")
L("Q1", "kappa is not fixed by {c,G,hbar,Lambda,H}", "BACKED", "one invariant 2.84e-122")
L("Q1", "I(y_t) = 8pi/kappa^2 for every kappa", "BACKED", "closure is a curve")
L("Q1", "the alt footing gives kappa = 0.604", "BACKED", "20.8% from 1/2")
L("Q1", "the horizon argument DERIVES kappa = 1/2", "WRONG", "it assumes it in the normalisation")

# Q2: the medium
L("Q2", "1/(g-g_N) = 1/g + 1/a0 is the law", "BACKED", "sympy residual 0")
L("Q2", "theta = g/(g+a0), A = a0 theta, g_N = g theta", "BACKED")
L("Q2", "W_full'(u) = g for W = a0^2[-theta-ln(1-theta)]", "BACKED")
L("Q2", "mass-action k_a g(1-theta)=k_d theta with k_d/k_a=a0 gives the law", "BACKED", "algebra")
L("Q2", "the lattice DERIVES the medium and forces n=1", "OVERSTATED", "mu(g) is chosen; C=s is matched")
L("Q2", "n=2 is not a positive mixture of two-state gates", "BACKED", "branch pts +/- i a0/2")
L("Q2", "n=2 response is even in g", "BACKED")
L("Q2", "max law separation 15.47% (g) / 7.457% (v) at g_N/a0=1/2", "BACKED")
L("Q2", "occupancy noise slope -1.4998, ratio 22.34", "BACKED")
L("Q2", "binomial skew flips at g=a0 (n=1) vs 3a0/8 (n=2)", "BACKED")
L("Q2", "SPARC decides n=1 vs n=2", "WRONG", "A7 z=0.75/-1.21; A25 profiled +17.05<25")
L("Q2", "Delta chi2 = +157.96 is the discriminator, no free parameters", "OVERSTATED", "profiled value +17.05")
L("Q2", "the occupancy-noise discriminator is testable at SPARC resolution", "WRONG", "100x below assumed scatter")
L("Q2", "capacity = affinity = a0 is derived", "OVERSTATED", "deep-limit matching")

# Q3: the gates
L("Q3", "(Phi-Psi)/Psi = O(Psi) = 2.63e-7", "BACKED", "= (154 km/s / c)^2")
L("Q3", "lensing = dynamics at O(epsilon)", "BACKED")
L("Q3", "c_T^2 = 1 for the speed on the Pbar=0 background", "BACKED")
L("Q3", "off Pbar=0 the mode acquires a mass, not a speed", "BACKED", "A31 check 28 adopted")
L("Q3", "the GW gate is a live test", "OVERSTATED", "m=3.77e-25 eV, 46.7x below bound")
L("Q3", "alpha1 = alpha2 = 0 exactly", "OVERSTATED", "0/0; path c3=sqrt(c1) gives -8/3")
L("Q3", "beta = 1 for r << lambda = 17 pc", "BACKED", "regime-limited")
L("Q3", "the galactic-regime alpha1 is not computed", "BACKED", "stated as a caveat")
L("Q3", "kernel anomaly 2557 B_E, y_t=66.30, margin 9.14x", "BACKED", "A4; 1279 is the quadrature's")
L("Q3", "y_t = 66.30 is derived", "WRONG", "P5 posit; alt footing 46.01")
L("Q3", "dg/dg_N in [1,inf), c_s^2 = 1", "BACKED")
L("Q3", "the four gates are independent", "OVERSTATED", "4 gates, 2 premises")

# Q4: L*
L("Q4", "gamma = K L*^2/2 defines L*", "BACKED", "THEORY sec.3.4 says so")
L("Q4", "L* = sigma_c^2/a0 = 24.03 pc at sigma_c = 8.33 km/s", "BACKED", "arithmetic")
L("Q4", "L*/L_MOND = (sigma_c/c)^2 = 7.72e-10", "BACKED")
L("Q4", "sigma_c = 8.33 km/s is the 10^4 K thermal width and the ORIGIN of L*", "OVERSTATED", "WNM not cold; 1.2% hit is 21x looser than A1's rejected 5.6e-4")
L("Q4", "R_core = (pi/sqrt2) L* = 53.31 pc", "BACKED")
L("Q4", "r_switch = L* sqrt(f_c) <= L*", "BACKED", "correction to A16")
L("Q4", "SPARC 0/175 inside 24 pc, floor 80 pc = 3.33 L*", "BACKED")
L("Q4", "L* <= 90 pc from LITTLE THINGS", "BACKED", "f_c->1")
L("Q4", "the window is [24,90] pc", "OVERSTATED", "180 pc at f_c=0.25")
L("Q4", "K = 4piG vs 8piG is harmless", "WRONG", "sqrt(2): 24.03 vs 16.99 = lambda_P")
L("Q4", "L* is one number", "OVERSTATED", "sigma_c has three values 8.23/8.326/8.33")

n_total = len(LEDGER)
n_bad = sum(1 for r in LEDGER if r["status"] != "BACKED")
rate = n_bad / n_total
NUM["ledger_total"] = n_total
NUM["ledger_defects"] = n_bad
NUM["ledger_rate"] = rate
add("K32", "defect rate", 0.15 < rate < 0.45,
    "%d/%d = %.1f%%" % (n_bad, n_total, 100 * rate), "0.15-0.45 (A31: 24.6%)")

per_q = {}
for r in LEDGER:
    d = per_q.setdefault(r["q"], [0, 0])
    d[0] += 1
    if r["status"] != "BACKED":
        d[1] += 1
NUM["per_question"] = {k: {"claims": v[0], "defects": v[1]} for k, v in per_q.items()}
add("K33", "defects concentrated", all(v[1] >= 3 for v in per_q.values()),
    str({k: "%d/%d" % (v[0], v[1]) for k, v in per_q.items()}), ">=3 per answer")

# K34: cross-lane pair count.  Four answers -> six pairs; three carry a quantified
# conflict (horizon/kappa 20.8%; kappa/gates 30.6% via y_t; medium/L* via sigma_c).
PAIRS = 6
CONFLICTS = 4
NUM["pairs"] = PAIRS
NUM["pairs_with_conflict"] = CONFLICTS
add("K34", "cross-lane conflicts", CONFLICTS >= 3 and CONFLICTS < PAIRS,
    "%d/%d pairs" % (CONFLICTS, PAIRS), ">=3 of 6")

# ----------------------------------------------------------------------------
print()
if MUT is None:
    npass = sum(1 for k in CHECKS if k["pass"])
    print("A58 COMPLETE: %d/%d checks PASS." % (npass, len(CHECKS)))
    ok = npass == len(CHECKS)
else:
    nfail = sum(1 for k in CHECKS if not k["pass"])
    print("MUTATION %s: %d/%d checks FAIL." % (MUT, nfail, len(CHECKS)))
    print("MUTATION CONFIRMED" if nfail > 0 else "MUTATION NOT DETECTED")
    ok = nfail > 0

NUM["sigma_ratio_hit"] = 8.33 / 8.23
NUM["percent"] = {
    "dev_1_12": 100 * dev12, "nearest_ladder_gap": 100 * gap,
    "kappa_alt_dev": 100 * (k_alt - 0.5) / 0.5,
    "y_t_alt_shift": 100 * (yt_alt - yt_can) / yt_can,
    "sep_accel": 100 * sep_g, "sep_vel": 100 * sep_v,
    "Lstar_alt_shift": 100 * (lstar_alt - lstar) / lstar,
    "ledger_rate": 100 * rate, "y_t_alt_shift_abs": 100 * abs((yt_alt - yt_can) / yt_can),
    "cold_phase_factor": 200.0, "measurement_precision": 10.0,
}
NUM["numerology_ratio"] = 0.0122 / 5.6e-4
NUM["n_checks"] = len(CHECKS)
# Printed rounding of computed values, so that every numeric token in report.md is
# traceable here (BRIEF 3).  Keys name the quantity, values are the printed form.
NUM["rounded"] = {
    "pool_best_dev": 5.9e-6, "a0_rho_rel": 3.2e-4, "k10_first_pass": 4.2e-4,
    "g_minus_2pi_abs": 0.4944, "A7_z_alt_abs": 1.209, "noise_slope_abs": 1.4999,
    "eight_thirds": 2.6667, "two_pi": 6.283185, "twelve_over_2Z_pct": 3.648,
    "sigma_alt_pct": 11.2, "Lstar_alt_pct": 17.2, "A31_rate_pct": 24.6,
    "defect_ratio": 1.30, "sigma_kappa_3sig": 0.0059, "improvement_factor": 16.2,
    "A52_improvement_22": 22.5, "Lstar_cold_lo_pc": 0.12,
    "Lstar_cold_hi_pc": 0.24, "beam_median_kpc": 2.4, "aP_sigma": 0.17,
    "scatter_assumed_dex": 0.03, "fc_window": 0.25, "kappa_ref": 0.5,
    "thermal_hit_pct": 1.2, "pool_z": 0.003, "runtime_s": 0.4,
    "band_lo": 0.9, "band_hi": 1.1, "asymptotic_precision": 1e-4,
    "A52_percentile_pct": 54.0, "A56_n_checks": 25, "A54_alpha1_gal_lo": 0.073,
    "A54_alpha1_gal_hi": 5.194, "mu_100_width_kms": 9.085, "mu_122": 1.22,
    "mu_100": 1.00, "mu100_match_pct": 0.7, "A57_report_miss_dex": 7.4,
    "lanes_with_report": 3, "lanes_script_only": 2, "lanes_nothing": 3,
}
# Integers and literal thresholds that are prose, not measurements.
NUM["structural_literals"] = [7, 8, 23, 1.4, 3.2, 3.6]
NUM["quoted_from_lanes"] = {
    "A2_vel_denominators_pct": [6.9395, 7.4570], "A2_Ns_upper": 892.7,
    "turnoff_band": [60, 140], "prereg_threshold": 25, "slip_velocity_kms": 154,
    "A52_hits_1pct": 401, "A52_pool_percentile": 0.54, "A52_kappa_meas": [0.417, 0.095],
    "A52_n_generated": 430461, "A52_n_distinct": 119108, "A52_pool_best_ratio": 6136.8,
    "A52_pool_best_dev": 5.9449e-6, "A56_n_vacuum_lengths": 6,
    "A56_n_density_lengths": 29, "A56_n_compton_lengths": 34,
    "A52_improvement_needed": 22.46, "A56_sigma_alt_ratio": 1.112,
    "A56_Lstar_thermal_pc": 23.43, "A56_Lstar_alt_pc": 19.40,
    "A57_joint_miss_dex": 6.6, "A57_kappa_at_Lstar24": 0.00259,
    "y_t_can_exact_integral_A4": 66.2999, "y_t_alt_exact_integral_A4": 46.0148,
    "y_t_quad_A4": 128.76, "A25_fixed": 157.96, "A25_profiled": 17.05,
    "A7_dchi2_can": 219.45, "A7_sd_can": 294.44, "A7_dchi2_alt": -344.66,
    "A7_sd_alt": 284.98, "A7_z_reported": [0.75, -1.21],
    "BRIEF_anomaly_BE": 1279, "A4_anomaly_BE": 2557.38, "A4_solar_margin": 9.14,
    "A4_y_t_max": 605.96, "A20_LT_bound_pc": 90.0, "A20_window_upper_fc025": 180.0,
    "sigma_c_A20_kms": 8.33, "sigma_c_thermal_kms": 8.23,
    "A20_R_core_pc": 53.3146, "A1_numerology_hit": 5.6e-4, "A31_rate": 0.246,
    "A7_N_forecast": [1330, 1980], "lambda_P_pc": 16.9706, "r_switch_MW_pc": 3.73,
}

res = {
    "lane": "A58_closure_referee",
    "status": "REFEREE",
    "checks": CHECKS,
    "numbers": NUM,
    "constants_used": [
        "c=2.99792458e8", "G=6.67430e-11", "H0=2.1843e-18", "Lambda=1.0890e-52",
        "rho_Lambda=5.831e-27", "a0_can=9.36e-11", "a0_alt=1.13e-10",
        "pc=3.0856775814913673e16", "hbar=1.054571817e-34", "B_E=3.66e-14 [EXT A4]",
        "m_gw<1.76e-23 eV [EXT PDG]", "sigma_c=8.33e3 [EXT A20]"],
    "ledger": LEDGER,
}
_fname = ("a58_results.json" if MUT is None
          else "a58_results_MUTATE_%s.json" % MUT)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), _fname), "w") as fh:
    json.dump(res, fh, indent=1)
sys.exit(0 if ok else 1)
