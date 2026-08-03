#!/usr/bin/env python3
r"""mi_aqual_route_a_shape_knob_2026.py -- ESCAPE A: DOES FREEING THE BARYON *SHAPE* LET ROUTE A OUT OF
LISANTI'S DILEMMA?

THE RESULT BEING ATTACKED. mi_aqual_route_a_refit_2026.py (17/17) concluded at L7a: "ROUTE A DOES NOT ESCAPE
LISANTI'S DILEMMA. ZERO cells clear the 2-sigma box on all five constraints, for either kernel, on either
footing, anywhere on the grid." Its best worst-constraint was 2.07 sigma (Route A) against 3.02 (alpha=2).

WHY THAT MIGHT NOT BE FINAL. It came from a TWO-parameter family: f_M, a COMMON multiplier on thin+thick
stellar mass, and f_R, a COMMON multiplier on the stellar scale lengths. But the dilemma is a SHAPE tension --
v_c(R0) wants radial force at R0 while Sigma_dyn(|z| < 1.1 kpc) wants little mass in the local slab -- and one
common mass scale raises both together. So this script FREES THE COMPONENTS SEPARATELY, in increasing
parameter count, and asks at each count whether the five-constraint box closes:

  (a)  3 params:  f_T (thin-disc mass), f_K (thick-disc mass), f_R (common stellar scale length)
  (b)  4 params:  + f_z, the THIN-DISC SCALE HEIGHT multiplier (300 pc -> 300 f_z pc)
  (b') 4 params:  + f_Rk, the THICK-DISC SCALE-LENGTH multiplier instead (the "release valve" reading)

THE FIVE CONSTRAINTS, verbatim from the anchor (mi_aqual_mond_refit_2026.py), NOT widened anywhere here:
    v_c(R0)  = 233.1 +- 3.0 km/s        DATA   (McMillan 2017 Table 3, his STATISTICAL error)
    K_z,1.1  = 73.9  +- 6.0 Msun/pc^2   DATA   (his fitted K_z,1.1; the +-6 is Holmberg & Flynn's)
    M_*      = 54.3  +- 5.7 e9 Msun     PRIOR  (McMillan 2017 Table 2)
    R_d,thin = 2.6   +- 0.52 kpc        PRIOR  (his adopted constraint)
    Sigma_*  = 38.0  +- 4.0 Msun/pc^2   PRIOR  (Bovy & Rix 2013, local stellar column |z| < 1.1 kpc)

WHAT IS *NOT* FREE, and why this is the honest way to run it:
  * a0 is an INPUT, never fitted, BOTH footings every time: canonical 9.3614e-11 and alt 1.13e-10.
  * gas is held at survey values and the bulge at DIRBE -- exactly as the anchor holds them.
  * NO error bar is widened anywhere. Every sigma divides by the number in the table above. The TIGHTER v_c
    convention (+-3.0) does all the deciding; the corpus's own +-4.0 is printed at the headline cell for
    information and never used to declare a pass.
  * the PREFILTER: the three PRIOR constraints are analytic -- they need no PDE -- so the search only solves
    shapes whose priors are already within 2.2 sigma. A shape beyond 2.2 sigma on a prior cannot be inside a
    2.0-sigma box, so nothing is lost for the box question, and the reported minima are checked to be INTERIOR
    to the cut. It is applied IDENTICALLY to all six kernel/footing combinations -- the prior box is
    kernel-independent, which is what makes the control in S5 like-for-like by construction.

THE EXTRACTOR. The 2026-08-02 audit measured that the anchor reads Sigma_dyn at the NEAREST GRID CELL in R
while reading v_c by INTERPOLATION, a mixed measurement biased up to +0.94 sigma ONE-SIDED UPWARD on the
vertical force. This script interpolates BOTH, everywhere, and S6b settles which extractor is right by MESH
REFINEMENT rather than by citing the audit -- because the box verdict turns on it.

  S1  VALIDATION -- the generalised builder reduces EXACTLY to the anchor's; the extractor matches the
      committed Route A script cell for cell; the analytic priors match the anchor's numerical ones
  S2  the TWO-parameter baseline re-run, all three kernels, both footings: reproduces 2.07 / 3.02 / zero
  S3  (a) THREE parameters -- the thin/thick mass split freed
  S4  (b) FOUR parameters -- the thin scale height, and (b') the thick scale length, with the response of
      each constraint to f_z measured rather than assumed
  S5  THE CONTROL: the same extended family under the superseded alpha=2 kernel and the literature's simple
      mu. If they clear too, the escape is about PARAMETERS and not about Route A, and this says so.
  S6  IS THE ESCAPE REAL? mesh refinement, extractor dependence, the JOINT (not per-constraint) prior cost,
      the parameter bill (chi2 per added dof and AIC), and what the box does not constrain.

Exit 0 = ran and every check held. No check(True), no unfalsifiable condition, and every verdict string is
built from the numbers the run produced.
"""
from __future__ import annotations

import itertools
import math
import os
import pathlib
import sys
import time

import numpy as np
from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mi_route_a_kernel import A0_ALT, A0_CANON, mu as mu_exp, mu_alpha2, mu_simple

FAST = os.environ.get("MI_FAST") == "1"          # plumbing smoke test only -- NOT the reported run
ok: list[tuple[bool, str]] = []
T0 = time.time()
NSOLVE = 0


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}", flush=True)
    return cond


def banner(t):
    print("\n" + "=" * 110, flush=True)
    print(f"  {t}")
    print("=" * 110, flush=True)


# ---------------------------------------------------------------- the anchor's definitions, verbatim
ASRC = pathlib.Path(__file__).with_name("mi_aqual_mond_refit_2026.py")
_a = ASRC.read_text()
_G: dict = {"__name__": "anchor_defs"}
exec(compile(_a[:_a.index('banner("F1')], str(ASRC), "exec"), _G)

# ------------------------------------------------- the COMMITTED Route A script's definitions, for validation
RSRC = pathlib.Path(__file__).with_name("mi_aqual_route_a_refit_2026.py")
_r = RSRC.read_text()
_R: dict = {"__name__": "routea_defs", "__file__": str(RSRC)}
exec(compile(_r[:_r.index('banner("L1')], str(RSRC), "exec"), _R)
obs_fixed_committed = _R["obs_fixed"]

G, KPC, PC, MSUN = _G["G"], _G["KPC"], _G["PC"], _G["MSUN"]
MSUN_PC2 = _G["MSUN_PC2"]
R0 = _G["R0"]
VC, VC_E, KZ, KZ_E = _G["VC"], _G["VC_E"], _G["KZ"], _G["KZ_E"]
MSTAR_P, MSTAR_E = _G["MSTAR_P"], _G["MSTAR_E"]
RDTHIN_P, RDTHIN_E = _G["RDTHIN_P"], _G["RDTHIN_E"]
SIGSTAR_P, SIGSTAR_E = _G["SIGSTAR_P"], _G["SIGSTAR_E"]
solve, densities, chi2 = _G["solve"], _G["densities"], _G["chi2"]
mass_of, sigma_of = _G["mass_of"], _G["sigma_of"]
S0T, RDT, ZDT = _G["S0_THIN0"], _G["RD_THIN0"], _G["ZD_THIN"]
S0K, RDK, ZDK = _G["S0_THICK0"], _G["RD_THICK0"], _G["ZD_THICK"]

VC_E_CORPUS = 4.0e3          # this corpus's own compiled v_c(R0) error; REPORTED, never used to pass a cell
A0_LIT = 1.2e-10             # the a0 the literature's simple mu is calibrated with (the anchor's own control)
BOX = 2.0
KEYS = ("vc", "sd", "mstar", "rd", "sig")
PREFILTER = 2.2              # >= this on ANY prior cannot be inside a 2.0-sigma box


def sigmas(o, vce=VC_E):
    return dict(vc=(o["vc"] - VC) / vce, sd=(o["sd"] - KZ) / KZ_E,
                mstar=(o["mstar"] - MSTAR_P) / MSTAR_E,
                rd=(o["rdt"] - RDTHIN_P) / RDTHIN_E,
                sig=(o["sigstar"] - SIGSTAR_P) / SIGSTAR_E)


def worst(o):
    s = sigmas(o)
    return max(abs(s[k]) for k in KEYS)


def worst_key(o):
    s = sigmas(o)
    return max(KEYS, key=lambda k: abs(s[k]))


# ---------------------------------------------------------------- the GENERALISED baryon model
def dens_ext(fT, fK, fR, fZ=1.0, fRK=1.0):
    """The anchor's four components with the two stellar discs freed SEPARATELY.

    fT   thin-disc surface-density multiplier      fK   thick-disc surface-density multiplier
    fR   COMMON stellar scale-length multiplier    fZ   thin-disc scale-height multiplier (300 pc baseline)
    fRK  EXTRA thick-disc scale-length multiplier on top of fR; 1.0 = the anchor's common scaling.

    At fT = fK = f_M and fZ = fRK = 1 this is the anchor's densities(f_M, f_R) IDENTICALLY -- S1a proves that
    on the density callables themselves, not on a derived number. Gas and bulge are the anchor's own objects.
    """
    s0t, rdt, zdt = S0T * fT, RDT * fR, ZDT * fZ
    s0k, rdk, zdk = S0K * fK, RDK * fR * fRK, ZDK
    base, _ = densities(1.0, 1.0)

    def thin(R, z):
        return (s0t / (2 * zdt)) * np.exp(-np.abs(z) / zdt - R / rdt)

    def thick(R, z):
        return (s0k / (2 * zdk)) * np.exp(-np.abs(z) / zdk - R / rdk)

    return dict(thin=thin, thick=thick, bulge=base["bulge"], hi=base["hi"], h2=base["h2"]), rdt


M_BULGE = mass_of(densities(1.0, 1.0)[0]["bulge"]) / MSUN


def priors_analytic(fT, fK, fR, fZ=1.0, fRK=1.0):
    """M_*, Sigma_*(R0, |z| < 1.1 kpc) and R_d,thin in CLOSED FORM -- no PDE. S1c validates them against the
    anchor's numerical mass_of/sigma_of. This is what makes a fine search affordable: three of the five
    constraints are algebra, so only the two DYNAMICAL ones ever need a solve."""
    Mt = 2 * math.pi * (S0T * fT) * (RDT * fR) ** 2 / MSUN
    Mk = 2 * math.pi * (S0K * fK) * (RDK * fR * fRK) ** 2 / MSUN
    st = (S0T * fT) * math.exp(-R0 / (RDT * fR)) * (1 - math.exp(-1.1 * KPC / (ZDT * fZ))) / MSUN_PC2
    sk = (S0K * fK) * math.exp(-R0 / (RDK * fR * fRK)) * (1 - math.exp(-1.1 * KPC / ZDK)) / MSUN_PC2
    return Mt + Mk + M_BULGE, st + sk, RDT * fR / KPC


def prior_sigmas(p):
    M, S, Rd = priors_analytic(*p)
    return (abs(M - MSTAR_P) / MSTAR_E, abs(S - SIGSTAR_P) / SIGSTAR_E,
            abs(Rd - RDTHIN_P / KPC) / (RDTHIN_E / KPC))


def passes_prefilter(p, cut=PREFILTER):
    return max(prior_sigmas(p)) <= cut


def obs_ext(fT, fK, fR, fZ, fRK, a0, mu, **kw):
    """CONSISTENT extractor: v_c AND Sigma_dyn both by INTERPOLATION in R. sd_snap is the anchor's
    nearest-cell reading, carried along so its bias can be reported rather than assumed."""
    global NSOLVE
    comp, rdt = dens_ext(fT, fK, fR, fZ, fRK)
    rho = lambda R, z: sum(f(R, z) for f in comp.values())
    Rc, zc, P = solve(rho, a0, mu, **kw)
    NSOLVE += 1
    vc = math.sqrt(abs(np.interp(R0, Rc, np.gradient(P[:, 0], Rc))) * R0)
    dPdz = np.gradient(P, zc, axis=1)
    gz11 = np.array([np.interp(1.1 * KPC, zc, dPdz[j, :]) for j in range(len(Rc))])
    sd = abs(np.interp(R0, Rc, gz11)) / (2 * math.pi * G) / MSUN_PC2
    i0 = int(np.argmin(np.abs(Rc - R0)))
    sd_snap = abs(np.interp(1.1 * KPC, zc, dPdz[i0, :])) / (2 * math.pi * G) / MSUN_PC2
    st = sigma_of(comp["thin"], R0, 1.1 * KPC) / MSUN_PC2
    sk = sigma_of(comp["thick"], R0, 1.1 * KPC) / MSUN_PC2
    mstar = (mass_of(comp["thin"]) + mass_of(comp["thick"]) + mass_of(comp["bulge"])) / MSUN
    return dict(vc=vc, sd=sd, sd_snap=sd_snap, mstar=mstar, sigstar=st + sk, rdt=rdt,
                fk_loc=sk / (st + sk), zd=ZDT * fZ / PC, rdk=RDK * fR * fRK / KPC,
                p=(fT, fK, fR, fZ, fRK))


CACHE: dict = {}


def cell(tag, p, a0, mu):
    k = (tag,) + tuple(round(v, 5) for v in p)
    if k not in CACHE:
        CACHE[k] = obs_ext(*p, a0, mu)
    return CACHE[k]


COMBOS = [("Route A exp, canon", "exc", mu_exp, A0_CANON),
          ("Route A exp, ALT", "exa", mu_exp, A0_ALT),
          ("alpha=2 superseded, canon", "a2c", mu_alpha2, A0_CANON),
          ("alpha=2 superseded, ALT", "a2a", mu_alpha2, A0_ALT),
          ("literature simple, a0=1.2e-10", "smL", mu_simple, A0_LIT),
          ("literature simple, canon a0", "smc", mu_simple, A0_CANON)]
CMB = {t: (lab, mu, a0) for lab, t, mu, a0 in COMBOS}
TAGS = [t for _l, t, _m, _a in COMBOS]
STAGE: dict = {t: {} for t in TAGS}


def record(tag, stage, cells):
    """Reduce a solved set to its minimax cell, its chi2 cell, and its box membership. The sets for the
    different parameter counts are kept DISJOINT where the nesting is being tested, so S3a can fail."""
    seen, uniq = set(), []
    for o in cells:
        k = tuple(round(v, 5) for v in o["p"])
        if k not in seen:
            seen.add(k)
            uniq.append(o)
    bw = min(uniq, key=worst)
    bc = min(uniq, key=lambda o: chi2(o)[0])
    box = sorted((o for o in uniq if worst(o) <= BOX), key=lambda o: chi2(o)[0])
    STAGE[tag][stage] = dict(w=worst(bw), w_cell=bw, c=chi2(bc)[0], c_cell=bc,
                             nbox=len(box), box=box, n=len(uniq))
    return STAGE[tag][stage]


def pstr(p, nd=3):
    return "(" + ", ".join(f"{v:.{nd}f}" for v in p) + ")"


def row(o):
    s = sigmas(o)
    return (f"{o['vc']/1e3:>7.1f}{s['vc']:>+7.2f}{o['sd']:>8.1f}{s['sd']:>+7.2f}{o['mstar']:>10.3e}"
            f"{s['mstar']:>+7.2f}{o['sigstar']:>7.1f}{s['sig']:>+7.2f}{o['rdt']/KPC:>6.2f}{s['rd']:>+7.2f}"
            f"{worst(o):>7.2f}{chi2(o)[0]:>8.1f}")


HDR = ("  " + f"{'v_c':>7}{'s_vc':>7}{'Sig_dyn':>8}{'s_sd':>7}{'M_*':>10}{'s_M':>7}{'Sig_*':>7}{'s_Sg':>7}"
       f"{'R_d':>6}{'s_Rd':>7}{'WORST':>7}{'chi2':>8}")


def pattern_refine(tag, p0, steps, budget=26):
    """Local minimax refinement: walk to the best neighbour on a shrinking pattern, capped in solves.
    Returns (best cell, solves used, every cell visited) so the visited set can be recorded honestly."""
    lab, mu, a0 = CMB[tag]
    p = tuple(p0)
    best = cell(tag, p, a0, mu)
    vis = [best]
    used, st = 0, list(steps)
    for _ in range(2):
        moved = True
        while moved and used < budget:
            moved = False
            for i, h in enumerate(st):
                if h == 0.0:
                    continue
                for sgn in (-1.0, +1.0):
                    q = list(p)
                    q[i] = round(q[i] + sgn * h, 5)
                    if q[i] <= 0.0 or used >= budget:
                        continue
                    o = cell(tag, tuple(q), a0, mu)
                    vis.append(o)
                    used += 1
                    if worst(o) < worst(best) - 1e-9:
                        best, p, moved = o, tuple(q), True
        st = [h / 2.0 for h in st]
    return best, used, vis


# ======================================================================================================
banner("S1  VALIDATION -- the generalised builder, the analytic priors, and the extractor")
if FAST:
    print("  *** MI_FAST=1: SMOKE MODE, grids shrunk. THIS IS NOT THE REPORTED RUN. ***")

c_anchor, rd_anchor = densities(1.30, 0.90)
c_mine, rd_mine = dens_ext(1.30, 1.30, 0.90, 1.0, 1.0)
Rg = np.array([0.1, 0.5, 1.0, 2.0, 4.0, 8.21, 12.0, 20.0]) * KPC
zg = np.array([0.0, 0.05, 0.3, 0.9, 1.1, 2.0, 5.0]) * KPC
RRg, ZZg = np.meshgrid(Rg, zg, indexing="ij")
dmax = 0.0
for k in ("thin", "thick", "bulge", "hi", "h2"):
    dmax = max(dmax, float(np.max(np.abs(c_mine[k](RRg, ZZg) / c_anchor[k](RRg, ZZg) - 1.0))))
check(dmax == 0.0 and rd_mine == rd_anchor,
      f"S1a the generalised builder REDUCES EXACTLY to the anchor's: at f_T = f_K = 1.30, f_R = 0.90, "
      f"f_z = f_Rk = 1 all five component density callables agree to {dmax:.1e} (bit-identical) on a "
      f"{len(Rg)}x{len(zg)} grid spanning 0.1-20 kpc and 0-5 kpc, and R_d,thin matches. Every difference "
      f"below is the freed SHAPE, not a re-implemented mass model")

o_mine = cell("exc", (1.30, 1.30, 0.90, 1.0, 1.0), A0_CANON, mu_exp)
o_comm = obs_fixed_committed(1.30, 0.90, A0_CANON, mu_exp)
dv = abs(o_mine["vc"] / o_comm["vc"] - 1.0)
ds = abs(o_mine["sd"] / o_comm["sd"] - 1.0)
print(f"  committed obs_fixed(1.30, 0.90):  v_c = {o_comm['vc']/1e3:.4f} km/s   "
      f"Sigma_dyn = {o_comm['sd']:.4f}")
print(f"  this script obs_ext(1.30, 1.30, 0.90):  v_c = {o_mine['vc']/1e3:.4f} km/s   "
      f"Sigma_dyn = {o_mine['sd']:.4f}")
check(dv < 1e-12 and ds < 1e-12,
      f"S1b and the EXTRACTOR is the committed one: obs_ext agrees with mi_aqual_route_a_refit_2026's own "
      f"obs_fixed to {dv:.1e} in v_c and {ds:.1e} in Sigma_dyn at the same cell, both interpolated in R as the "
      f"2026-08-02 audit requires. The +2.11 sigma vertical force quoted for Route A at fixed baryons is "
      f"reproduced: {sigmas(o_mine)['sd']:+.2f} sigma")

worst_ana = 0.0
for p in [(1.30, 1.30, 0.90, 1.0, 1.0), (2.40, 1.00, 0.76, 1.0, 1.0), (1.80, 2.50, 1.04, 1.6, 1.0),
          (2.00, 0.50, 0.88, 0.7, 1.4)]:
    comp, rdt = dens_ext(*p)
    Mn = (mass_of(comp["thin"]) + mass_of(comp["thick"]) + mass_of(comp["bulge"])) / MSUN
    Sn = (sigma_of(comp["thin"], R0, 1.1 * KPC) + sigma_of(comp["thick"], R0, 1.1 * KPC)) / MSUN_PC2
    Ma, Sa, Rda = priors_analytic(*p)
    worst_ana = max(worst_ana, abs(Mn / Ma - 1.0), abs(Sn / Sa - 1.0), abs(rdt / KPC / Rda - 1.0))
check(worst_ana < 2e-3,
      f"S1c the analytic priors the PREFILTER uses match the anchor's numerical mass_of / sigma_of to "
      f"{worst_ana:.2e} relative over four widely separated shapes (the residual is the anchor's own 60 kpc x "
      f"20 kpc integration truncation, i.e. well inside 0.01 sigma). So skipping the PDE for the three prior "
      f"constraints is exact for the search, and every REPORTED prior number below is still the numerical one")

sd_bias = (o_mine["sd_snap"] - o_mine["sd"]) / KZ_E
print(f"\n  extractor at (1.30, 1.30, 0.90): Sigma_dyn interpolated {o_mine['sd']:.2f} "
      f"({sigmas(o_mine)['sd']:+.2f} s) vs nearest-cell {o_mine['sd_snap']:.2f} "
      f"({(o_mine['sd_snap']-KZ)/KZ_E:+.2f} s)  ->  {sd_bias:+.2f} sigma of one-sided upward bias")
check(o_mine["sd_snap"] > o_mine["sd"],
      f"S1d the anchor's nearest-cell reading is HIGH here by {o_mine['sd_snap']-o_mine['sd']:.2f} Msun/pc^2 = "
      f"{sd_bias:+.2f} sigma, the one-sided upward bias the audit measured. S6b decides which extractor is "
      f"right by MESH REFINEMENT instead of taking the audit on trust, because the box verdict turns on it")


# ======================================================================================================
banner("S2  THE TWO-PARAMETER BASELINE, re-run here so the extra parameters can be priced")

FM = [1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8] if not FAST else [1.3, 1.9]
FR2 = [0.7, 0.8, 0.9, 1.0, 1.1] if not FAST else [0.8, 0.9]
print(f"  the committed grid: f_M in {FM}, f_R in {FR2}   (f_T = f_K = f_M, f_z = f_Rk = 1)\n")
print(f"  {'kernel / footing':<32}{'best (f_M, f_R)':>18}{'WORST':>7}{'binding':>9}{'chi2':>8}{'in box':>8}")
print("  " + "-" * 86)
for lab, tag, mu_k, a0 in COMBOS:
    cells = [cell(tag, (fm, fm, fr, 1.0, 1.0), a0, mu_k) for fm in FM for fr in FR2]
    r = record(tag, "2par", cells)
    bw = r["w_cell"]
    print(f"  {lab:<32}{pstr((bw['p'][0], bw['p'][2]), 2):>18}{r['w']:>7.2f}{worst_key(bw):>9}"
          f"{r['c']:>8.1f}{r['nbox']:>8d}   [{time.time()-T0:.0f}s]", flush=True)

w2 = {t: STAGE[t]["2par"]["w"] for t in TAGS}
w2_ex, w2_a2 = min(w2["exc"], w2["exa"]), min(w2["a2c"], w2["a2a"])
w2_sm = min(w2["smL"], w2["smc"])
n2_ex = STAGE["exc"]["2par"]["nbox"] + STAGE["exa"]["2par"]["nbox"]
n2_a2 = STAGE["a2c"]["2par"]["nbox"] + STAGE["a2a"]["2par"]["nbox"]
print(f"\n  best worst-constraint over both footings:  Route A {w2_ex:.2f}   alpha=2 {w2_a2:.2f}   "
      f"simple mu {w2_sm:.2f}")
check(abs(w2_ex - 2.07) < 0.10 and abs(w2_a2 - 3.02) < 0.10 and n2_ex == 0 and n2_a2 == 0,
      f"S2a the committed baseline REPRODUCES through this script's own code path: Route A's best "
      f"worst-constraint is {w2_ex:.2f} sigma against the published 2.07, alpha=2's is {w2_a2:.2f} against "
      f"3.02, with {n2_ex} and {n2_a2} cells in the {BOX:.0f}-sigma box. L7a's 'ZERO cells clear the box' is "
      f"reproduced, so the extended families below are measured against the real baseline")


# ======================================================================================================
banner("S3  (a) THREE PARAMETERS -- f_T, f_K, f_R.  The thin/thick mass split freed")

FT = list(np.round(np.arange(1.00, 3.76, 0.25), 4)) if not FAST else [2.25, 2.50]
FK = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0] if not FAST else [1.0, 2.0]
FR3 = list(np.round(np.arange(0.62, 1.25, 0.06), 4)) if not FAST else [0.74, 0.80]
GRID3 = [(t, k, r, 1.0, 1.0) for t, k, r in itertools.product(FT, FK, FR3)]
PASS3 = [p for p in GRID3 if passes_prefilter(p)]
print(f"""  f_T in [{min(FT)}, {max(FT)}] step 0.25   f_K in {FK}   f_R in [{min(FR3)}, {max(FR3)}] step 0.06
  {len(GRID3)} shapes enumerated, {len(PASS3)} survive the {PREFILTER} sigma prefilter on the three analytic
  priors and are solved. The {len(GRID3)-len(PASS3)} skipped shapes are beyond {PREFILTER} sigma on M_*, R_d
  or Sigma_* and so cannot be inside a {BOX:.0f}-sigma box. The 2-parameter cells of S2 are deliberately NOT
  pooled into this set, so the nesting test in S3a can actually fail.\n""")
print(f"  {'kernel / footing':<32}{'best (f_T, f_K, f_R)':>26}{'WORST':>7}{'binding':>9}{'chi2':>8}"
      f"{'in box':>8}{'refine':>8}")
print("  " + "-" * 102)
for lab, tag, mu_k, a0 in COMBOS:
    cells = [cell(tag, p, a0, mu_k) for p in PASS3]
    r = record(tag, "3par", cells)
    bw, used, vis = pattern_refine(tag, r["w_cell"]["p"], (0.125, 0.25, 0.03, 0.0, 0.0),
                                   budget=6 if FAST else 26)
    r = record(tag, "3par", cells + vis)
    bw = r["w_cell"]
    print(f"  {lab:<32}{pstr(bw['p'][:3]):>26}{r['w']:>7.2f}{worst_key(bw):>9}{r['c']:>8.1f}"
          f"{r['nbox']:>8d}{used:>8d}   [{time.time()-T0:.0f}s]", flush=True)

b3 = STAGE["exc"]["3par"]["w_cell"]
print(f"\n  the Route A CANONICAL best 3-parameter cell in full:")
print(HDR)
print("  " + row(b3))
print(f"  f_T = {b3['p'][0]:.3f}  f_K = {b3['p'][1]:.3f}  f_R = {b3['p'][2]:.3f}  ->  R_d,thin = "
      f"{b3['rdt']/KPC:.2f} kpc, R_d,thick = {b3['rdk']:.2f} kpc, thick disc = "
      f"{100*b3['fk_loc']:.0f}% of the local stellar column")
w3 = {t: STAGE[t]["3par"]["w"] for t in TAGS}
w3_ex, w3_a2 = min(w3["exc"], w3["exa"]), min(w3["a2c"], w3["a2a"])
n3_ex = STAGE["exc"]["3par"]["nbox"] + STAGE["exa"]["3par"]["nbox"]
n3_a2 = STAGE["a2c"]["3par"]["nbox"] + STAGE["a2a"]["3par"]["nbox"]
check(w3_ex < w2_ex and all(w3[t] <= w2[t] + 1e-9 for t in TAGS),
      f"S3a the third parameter does real work, and the two searches are mutually consistent: Route A's best "
      f"worst-constraint falls from {w2_ex:.2f} sigma (2 params) to {w3_ex:.2f} sigma (3 params), and no "
      f"kernel gets WORSE when its mass split is freed (alpha=2 {w2_a2:.2f} -> {w3_a2:.2f}). The 3-parameter "
      f"family CONTAINS the 2-parameter one but the two sets are searched separately here, so a rise would "
      f"mean the finer search misses a region the coarse one found -- this fails on that defect")
_int3 = all(min(FT) < STAGE[t]["3par"]["w_cell"]["p"][0] < max(FT)
            and min(FR3) < STAGE[t]["3par"]["w_cell"]["p"][2] < max(FR3) for t in TAGS)
_intc = all(max(prior_sigmas(STAGE[t]["3par"]["c_cell"]["p"])) < PREFILTER - 1e-9 for t in TAGS)
check(_int3 and _intc,
      f"S3b every one of the six minimax cells is INTERIOR in f_T and f_R, and every one of the six chi2 minima "
      f"is interior to the {PREFILTER} sigma prefilter, so no reported best is an unexplored edge and no "
      f"reported chi2 minimum is sitting against the prefilter boundary (f_K's lower edge is the physical "
      f"0 = no thick disc, which is why f_K is excluded from the interiority test)")


# ======================================================================================================
banner("S4  (b) FOUR PARAMETERS -- the thin SCALE HEIGHT, and (b') the thick SCALE LENGTH")

FZ = [0.7, 0.85, 1.2, 1.5, 2.0] if not FAST else [0.85, 1.5]
FRK = [0.6, 0.8, 1.25, 1.6] if not FAST else [0.8, 1.25]
NTOP = 3 if not FAST else 1
print(f"""  (b)  f_z multiplies the thin disc's 300 pc scale height: f_z in {FZ}. The brief's hypothesis is that
       this is "a nearly pure knob on the binding constraint" because Sigma_dyn(|z| < 1.1 kpc) is directly
       sensitive to how much disc sits inside the slab. S4a MEASURES that instead of assuming it.
  (b') f_Rk multiplies the THICK disc scale length on top of f_R: f_Rk in {FRK} -- the "release valve"
       reading, mass carried at height and at large R.
  Each is scanned on the top {NTOP} three-parameter cells per kernel (ranked by worst constraint), then
  minimax-refined in all four parameters.\n""")
print(f"  {'kernel / footing':<28}{'stage':>7}{'best (f_T,f_K,f_R,f_z,f_Rk)':>34}{'WORST':>7}{'binding':>9}"
      f"{'chi2':>8}{'in box':>8}")
print("  " + "-" * 104)
for lab, tag, mu_k, a0 in COMBOS:
    seeds = sorted(STAGE[tag]["3par"]["box"] or [STAGE[tag]["3par"]["w_cell"]], key=worst)[:NTOP]
    if len(seeds) < NTOP:
        seeds = sorted((o for k, o in CACHE.items() if k[0] == tag and o["p"][3] == 1.0
                        and o["p"][4] == 1.0), key=worst)[:NTOP]
    for stg, vals, slot, steps in (("4par_z", FZ, 3, (0.125, 0.25, 0.03, 0.10, 0.0)),
                                   ("4par_Rk", FRK, 4, (0.125, 0.25, 0.03, 0.0, 0.10))):
        cells = list(seeds)
        for o in seeds:
            for v in vals:
                q = list(o["p"])
                q[slot] = v
                if passes_prefilter(tuple(q)):
                    cells.append(cell(tag, tuple(q), a0, mu_k))
        r = record(tag, stg, cells)
        bw, used, vis = pattern_refine(tag, r["w_cell"]["p"], steps, budget=4 if FAST else 18)
        r = record(tag, stg, cells + vis)
        bw = r["w_cell"]
        print(f"  {lab:<28}{stg.replace('4par_', ''):>7}{pstr(bw['p'], 2):>34}{r['w']:>7.2f}"
              f"{worst_key(bw):>9}{r['c']:>8.1f}{r['nbox']:>8d}   [{time.time()-T0:.0f}s]", flush=True)

# --- S4a  the f_z RESPONSE, measured: is the scale height really a knob on the BINDING constraint alone?
print(f"\n  f_z RESPONSE at the Route A canonical 3-parameter best {pstr(b3['p'][:3])}, prefilter suspended so "
      f"the response is\n  measured over the full range rather than only where it stays inside the prior box:")
print(f"  {'f_z':>6}{'z_d [pc]':>10}{'Sig_dyn':>9}{'s_sd':>8}{'Sig_*':>8}{'s_Sg':>8}{'v_c':>8}{'s_vc':>8}"
      f"{'WORST':>7}")
print("  " + "-" * 72)
RESP = []
for fz in (0.7, 1.0, 1.5, 2.0, 2.8):
    q = (b3["p"][0], b3["p"][1], b3["p"][2], fz, 1.0)
    o = cell("exc", q, A0_CANON, mu_exp)
    s = sigmas(o)
    RESP.append((fz, s["sd"], s["sig"], s["vc"], worst(o)))
    print(f"  {fz:>6.2f}{o['zd']:>10.0f}{o['sd']:>9.1f}{s['sd']:>+8.2f}{o['sigstar']:>8.1f}{s['sig']:>+8.2f}"
          f"{o['vc']/1e3:>8.1f}{s['vc']:>+8.2f}{worst(o):>7.2f}")
d_sd = RESP[-1][1] - RESP[0][1]
d_sg = RESP[-1][2] - RESP[0][2]
check(d_sd * d_sg > 0 and abs(d_sg / d_sd) > 0.5,
      f"S4a *** THE BRIEF'S HYPOTHESIS IS WRONG, and this is the single most useful thing in S4: the thin-disc "
      f"scale height is NOT a nearly pure knob on the binding constraint. Over f_z = 0.7 -> 2.8 the vertical "
      f"force moves {d_sd:+.2f} sigma and Bovy & Rix's Sigma_* moves {d_sg:+.2f} sigma -- the SAME sign and a "
      f"ratio of {abs(d_sg/d_sd):.2f}. *** The reason is structural: Sigma_dyn and Sigma_* are both columns "
      f"through the SAME |z| < 1.1 kpc slab, so lifting mass out of the slab spends the star-count prior at "
      f"almost exactly the rate it buys the vertical force. The scale height moves ALONG the degeneracy, not "
      f"across it")
g3 = w2_ex - w3_ex
w4z_ex = min(STAGE[t]["4par_z"]["w"] for t in ("exc", "exa"))
w4k_ex = min(STAGE[t]["4par_Rk"]["w"] for t in ("exc", "exa"))
w4_ex = min(w4z_ex, w4k_ex)
w4_a2 = min(min(STAGE[t][s]["w"] for s in ("4par_z", "4par_Rk")) for t in ("a2c", "a2a"))
g4 = w3_ex - w4_ex
check(g4 < g3,
      f"S4b DIMINISHING RETURNS, and it is sharp: the THIRD parameter bought {g3:.3f} sigma of worst "
      f"constraint ({w2_ex:.2f} -> {w3_ex:.2f}); the FOURTH buys {g4:.3f} ({w3_ex:.2f} -> {w4_ex:.2f}), from "
      f"the scale height {w3_ex-w4z_ex:.3f} and from the thick scale length {w3_ex-w4k_ex:.3f}. The brief's "
      f"'the thick disc is the natural release valve' is therefore "
      f"{'the better of the two fourth parameters but still marginal' if w4k_ex < w4z_ex else 'NOT borne out -- the scale height is the better of two weak knobs' if w4z_ex < w4k_ex else 'exactly as (in)effective as the scale height'}. "
      f"This check fails if the fourth parameter ever buys more than the third did")


# ======================================================================================================
banner("S5  THE CONTROL -- the SAME extended family under alpha=2 and the literature's simple mu")

print("""  This is the load-bearing table of the lane. If the extended family lets the SUPERSEDED alpha=2
  kernel clear the box too, then the escape is about PARAMETERS and not about Route A, and that has to be
  said plainly. Identical grid, identical prefilter, identical extractor, identical priors.\n""")
print(f"  {'kernel / footing':<32}{'2par':>7}{'3par':>7}{'4par z':>8}{'4par Rk':>9}{'box@2':>7}{'box@3':>7}"
      f"{'box@4':>7}{'best chi2':>10}")
print("  " + "-" * 96)
for lab, tag, mu_k, a0 in COMBOS:
    S = STAGE[tag]
    nb4 = max(S["4par_z"]["nbox"], S["4par_Rk"]["nbox"])
    print(f"  {lab:<32}{S['2par']['w']:>7.2f}{S['3par']['w']:>7.2f}{S['4par_z']['w']:>8.2f}"
          f"{S['4par_Rk']['w']:>9.2f}{S['2par']['nbox']:>7d}{S['3par']['nbox']:>7d}{nb4:>7d}"
          f"{min(S[s]['c'] for s in S):>10.1f}")

BOXED = {t: max(STAGE[t][s]["nbox"] for s in STAGE[t]) for t in TAGS}
n_ex, n_a2, n_sm = BOXED["exc"] + BOXED["exa"], BOXED["a2c"] + BOXED["a2a"], BOXED["smL"] + BOXED["smc"]
wx_ex, wx_a2 = min(w3_ex, w4_ex), min(w3_a2, w4_a2)
wx_sm = min(min(STAGE[t][s]["w"] for s in STAGE[t]) for t in ("smL", "smc"))
print(f"\n  cells inside the {BOX:.0f}-sigma box anywhere in the extended search:  Route A {n_ex}, "
      f"alpha=2 {n_a2}, literature simple {n_sm}")
print(f"  best worst-constraint reached at ANY parameter count:  Route A {wx_ex:.2f}, alpha=2 {wx_a2:.2f}, "
      f"literature simple {wx_sm:.2f} sigma")
check(n_ex > 0 and wx_ex <= BOX,
      f"S5a *** THE BOX CLOSES FOR ROUTE A ONCE THE MASS SPLIT IS FREED: {n_ex} cell(s) hold all five "
      f"constraints inside {BOX:.0f} sigma simultaneously, against {n2_ex} for the 2-parameter family, and the "
      f"best worst-constraint goes {w2_ex:.2f} -> {wx_ex:.2f} sigma. *** No error bar was widened to get "
      f"there; S6c prices what WAS spent. This check fails if no cell clears")
check(wx_a2 > BOX,
      f"S5b *** THE CONTROL HOLDS: the superseded alpha=2 kernel, given the IDENTICAL extended family, the "
      f"identical prefilter and the identical extractor, reaches only {wx_a2:.2f} sigma and puts {n_a2} cells "
      f"in the box. *** So the box-clearing is NOT bought by the extra parameters -- alpha=2 has exactly the "
      f"same extra parameters and stays outside. If this check ever fails, the shape knob is the whole story "
      f"and Route A is not")
check(wx_a2 > w2_ex,
      f"S5c and the sharpest form of that control: TWO EXTRA PARAMETERS do not buy alpha=2 what the kernel "
      f"switch bought Route A for free. alpha=2 with a freed thin/thick split AND a freed scale height still "
      f"reaches only {wx_a2:.2f} sigma, worse than the 2-parameter Route A baseline's {w2_ex:.2f}. The reason "
      f"is that Route A's boost at the Galaxy's own y is ~10% stronger in g, i.e. ~1.5x in the mass needed for "
      f"the same v_c, and no reshaping of a fixed baryon budget substitutes for that")
check(abs(STAGE["exc"]["3par"]["w"] - STAGE["exa"]["3par"]["w"]) > 0.01,
      f"S5d the two a0 footings are NOT degenerate on this front under the extended family either: canonical "
      f"reaches {STAGE['exc']['3par']['w']:.2f} sigma and alt {STAGE['exa']['3par']['w']:.2f} at three "
      f"parameters ({'canonical' if STAGE['exc']['3par']['w'] < STAGE['exa']['3par']['w'] else 'alt'} ahead), "
      f"so the footing fork is a real part of the answer and both are carried everywhere above")


# ======================================================================================================
banner("S6  IS THE ESCAPE REAL?  mesh, extractor, the JOINT prior cost, and the parameter bill")

HEAD = None
for stg, k in (("3par", 3), ("4par_z", 4), ("4par_Rk", 4)):
    for tag in ("exc", "exa"):
        if HEAD is None and STAGE[tag][stg]["nbox"] > 0:
            HEAD = (tag, stg, k, STAGE[tag][stg]["box"][0])
if HEAD is None:
    tag = min(("exc", "exa"), key=lambda t: STAGE[t]["3par"]["w"])
    stg = min(("3par", "4par_z", "4par_Rk"), key=lambda s: STAGE[tag][s]["w"])
    HEAD = (tag, stg, 3 if stg == "3par" else 4, STAGE[tag][stg]["w_cell"])
htag, hstg, hk, H = HEAD
hlab, hmu, ha0 = CMB[htag]
sH, sH4 = sigmas(H), sigmas(H, VC_E_CORPUS)
print(f"  THE HEADLINE CELL -- {hlab}, stage {hstg}, minimal clearing parameter count k = {hk}")
print(f"      f_T = {H['p'][0]:.3f}   f_K = {H['p'][1]:.3f}   f_R = {H['p'][2]:.3f}   f_z = {H['p'][3]:.3f}"
      f"   f_Rk = {H['p'][4]:.3f}")
print(f"      v_c(R0)   = {H['vc']/1e3:7.1f} km/s      ({sH['vc']:+.2f} s on McMillan's +-3.0, "
      f"{sH4['vc']:+.2f} on this corpus's +-4.0)")
print(f"      K_z,1.1   = {H['sd']:7.1f} Msun/pc^2 ({sH['sd']:+.2f} s vs 73.9 +- 6.0)")
print(f"      M_*       = {H['mstar']:.3e} Msun ({sH['mstar']:+.2f} s vs 54.3e9 +- 5.7e9)")
print(f"      R_d,thin  = {H['rdt']/KPC:7.2f} kpc       ({sH['rd']:+.2f} s vs 2.6 +- 0.52)")
print(f"      Sigma_*   = {H['sigstar']:7.1f} Msun/pc^2 ({sH['sig']:+.2f} s vs Bovy & Rix 38 +- 4)")
print(f"      worst constraint {worst(H):.2f} sigma on {worst_key(H)};   chi2 = {chi2(H)[0]:.2f}")

o_fine = obs_ext(*H["p"], ha0, hmu, n=130, growth=1.0715)
sF = sigmas(o_fine)
print(f"\n  MESH: the anchor's n = 110 / growth 1.085 vs n = 130 / growth 1.0715 (same outer radius, "
      f"finer spacing)")
print(f"      v_c        {H['vc']/1e3:8.2f} -> {o_fine['vc']/1e3:8.2f} km/s   ({sH['vc']:+.2f} -> "
      f"{sF['vc']:+.2f} s)")
print(f"      Sigma_dyn  {H['sd']:8.2f} -> {o_fine['sd']:8.2f}          ({sH['sd']:+.2f} -> {sF['sd']:+.2f} s)")
print(f"      worst      {worst(H):8.2f} -> {worst(o_fine):8.2f} sigma")
check((worst(o_fine) <= BOX) == (worst(H) <= BOX) and abs(worst(o_fine) - worst(H)) < 0.30,
      f"S6a the headline verdict SURVIVES mesh refinement: on a 130-cell mesh at the same outer radius the "
      f"worst constraint moves {worst(H):.2f} -> {worst(o_fine):.2f} sigma and the cell is "
      f"{'still inside' if worst(o_fine) <= BOX else 'still outside'} the box. Both halves are asserted, so "
      f"this fails if box membership is a discretisation artefact")

snap_shift = abs(o_fine["sd_snap"] - H["sd_snap"])
int_shift = abs(o_fine["sd"] - H["sd"])
s_snap = max([abs((H["sd_snap"] - KZ) / KZ_E)] + [abs(sH[k]) for k in KEYS if k != "sd"])
print(f"\n  EXTRACTOR, settled by refinement rather than by citing the audit:")
print(f"      interpolated   {H['sd']:.2f} -> {o_fine['sd']:.2f}  (moves {int_shift:.2f} Msun/pc^2)")
print(f"      nearest cell   {H['sd_snap']:.2f} -> {o_fine['sd_snap']:.2f}  (moves {snap_shift:.2f})")
print(f"      on the anchor's nearest-cell extractor this cell reads {(H['sd_snap']-KZ)/KZ_E:+.2f} sigma "
      f"instead of {sH['sd']:+.2f}, i.e. worst = {s_snap:.2f} and it would "
      f"{'STILL clear' if s_snap <= BOX else 'NOT clear'} the box")
check(int_shift < snap_shift and abs(o_fine["sd_snap"] - o_fine["sd"]) < abs(H["sd_snap"] - H["sd"]),
      f"S6b the INTERPOLATED extractor is the convergent one, measured: refining the mesh moves it by "
      f"{int_shift:.2f} Msun/pc^2 against {snap_shift:.2f} for the nearest-cell reading "
      f"({snap_shift/max(int_shift,1e-9):.1f}x more), and the gap between the two extractors SHRINKS from "
      f"{abs(H['sd_snap']-H['sd']):.2f} to {abs(o_fine['sd_snap']-o_fine['sd']):.2f} as the mesh refines -- "
      f"i.e. the nearest-cell value converges TOWARD the interpolated one, which is the evidence that the "
      f"audit's fix is a fix. Stated against interest: the box verdict therefore depends on a 2026-08-02 "
      f"methodological correction as well as on the kernel")

chi2_pri = sH["mstar"] ** 2 + sH["rd"] ** 2 + sH["sig"] ** 2
chi2_dat = sH["vc"] ** 2 + sH["sd"] ** 2
p_pri = float(stats.chi2.sf(chi2_pri, 3))
sig_pri = float(stats.norm.isf(max(p_pri, 1e-16) / 2.0))
w_pri = max(abs(sH[k]) for k in ("mstar", "rd", "sig"))
print(f"\n  THE JOINT COST, which a per-constraint box hides. The three star-count priors sit at "
      f"({sH['mstar']:+.2f}, {sH['rd']:+.2f}, {sH['sig']:+.2f}) sigma:")
print(f"      chi2_prior = {chi2_pri:.2f} on 3 priors  ->  p = {p_pri:.3f}, a {sig_pri:.2f} sigma JOINT "
      f"departure from the star counts")
print(f"      chi2_data  = {chi2_dat:.2f}      total chi2 = {chi2(H)[0]:.2f} on 5 constraints, k = {hk}, "
      f"{5-hk} dof")
check(sig_pri > w_pri,
      f"S6c AGAINST INTEREST, and this caveat must travel with the headline: the escape lives in a CORNER of "
      f"the prior box. No single prior is off by more than {w_pri:.2f} sigma, but JOINTLY the three star-count "
      f"priors are {sig_pri:.2f} sigma away (chi2 = {chi2_pri:.2f} on 3 dof, p = {p_pri:.3f}). 'All five "
      f"constraints inside {BOX:.0f} sigma' -- the corpus's own operationalisation of the dilemma, which is "
      f"why it is answered on its own terms -- is a WEAKER statement than 'consistent with the star counts at "
      f"{BOX:.0f} sigma', and this cell satisfies the first and not the second. The check is not automatic: a "
      f"cell with one prior off and two on the nose would fail it")

print(f"\n  THE PARAMETER BILL (5 constraints throughout, AIC = chi2 + 2k, lower is better):")
print(f"  {'family':<46}{'k':>3}{'dof':>5}{'chi2':>9}{'chi2/dof':>10}{'AIC':>9}{'d chi2':>9}")
print("  " + "-" * 92)
BILL = {}
for tag in ("exc", "a2c"):
    prev = None
    for stg, k, cum in (("2par", 2, ("2par",)), ("3par", 3, ("2par", "3par")),
                        ("4par_z", 4, ("2par", "3par", "4par_z", "4par_Rk"))):
        c_ = min(STAGE[tag][s]["c"] for s in cum)
        d = "--" if prev is None else f"{prev-c_:.2f}"
        print(f"  {CMB[tag][0] + '  k=' + str(k):<46}{k:>3}{5-k:>5}{c_:>9.2f}{c_/max(5-k,1):>10.2f}"
              f"{c_+2*k:>9.2f}{d:>9}")
        BILL[(tag, k)] = c_
        prev = c_
cE = [BILL[("exc", k)] for k in (2, 3, 4)]
aic = [cE[i] + 2 * k for i, k in enumerate((2, 3, 4))]
check(cE[1] < cE[0] and cE[2] <= cE[1] + 1e-9,
      f"S6d the chi2 improvement is monotone in the parameter count, as a nested family requires: Route A "
      f"canonical goes {cE[0]:.2f} (k=2) -> {cE[1]:.2f} (k=3) -> {cE[2]:.2f} (k=4), so the third parameter "
      f"buys {cE[0]-cE[1]:.2f} of chi2 for 1 dof and the fourth {cE[1]-cE[2]:.2f}. AIC prefers k = "
      f"{(2, 3, 4)[int(np.argmin(aic))]} ({min(aic):.2f}); by the usual Delta chi2 > 1 per parameter reading "
      f"the third parameter is EARNED and the fourth is "
      f"{'earned too' if cE[1]-cE[2] > 1.0 else 'NOT earned'}. A rise here would mean the wider search missed "
      f"the narrower one's optimum")

o_mc = cell("exc", (1.0, 1.0, 1.0, 1.0, 1.0), A0_CANON, mu_exp)
print(f"\n  WHAT THE BOX DOES NOT CONSTRAIN, and what the escape does to it anyway:")
print(f"      thin-disc scale height          {H['zd']:6.0f} pc   (McMillan adopts 300 pc; factor "
      f"{H['zd']/300:.2f})")
print(f"      thick-disc scale length         {H['rdk']:6.2f} kpc  (his 3.02 kpc times f_R f_Rk = "
      f"{H['p'][2]*H['p'][4]:.3f})")
print(f"      thick share of local stellar column {100*H['fk_loc']:5.0f}%   (his own model: "
      f"{100*o_mc['fk_loc']:.0f}%)")
print(f"      f_T / f_K                       {H['p'][0]/max(H['p'][1], 1e-9):6.2f}   (1.00 = the anchor's "
      f"common scaling, which is the parameter this lane freed)")
check(abs(H["p"][0] / max(H["p"][1], 1e-9) - 1.0) > 0.15 and (H["zd"] == 300.0) == (hstg != "4par_z"),
      f"S6e the escape genuinely NEEDS the split freed rather than relabelled: the clearing cell has "
      f"f_T/f_K = {H['p'][0]/max(H['p'][1],1e-9):.2f}, i.e. {abs(100*(H['p'][0]/max(H['p'][1],1e-9)-1)):.0f}% "
      f"away from the common scaling that any 2-parameter fit is forced into, with a "
      f"{'thin-heavy' if H['p'][0] > H['p'][1] else 'thick-heavy'} disc. Second half of the check: the "
      f"reported thin scale height is {H['zd']:.0f} pc and the headline stage is {hstg}, so a 4-parameter cell "
      f"can never be reported under a 3-parameter headline")


# ======================================================================================================
banner("THE ANSWER")

_ctrl = ("does NOT clear it even with the same extra freedom" if n_a2 == 0
         else "clears it as well once given the same extra freedom, which would make this a parameter result")
print(f"""  ESCAPE A -- THE SHAPE KNOB -- {'WORKS' if n_ex > 0 else 'DOES NOT WORK'}, on the corpus's own
  operationalisation of Lisanti's dilemma, and here is the whole of it in numbers:

    * the 2-parameter family reaches {w2_ex:.2f} sigma on its worst constraint with {n2_ex} cells in the
      {BOX:.0f}-sigma box -- L7a's published 2.07 and zero, reproduced in S2a.
    * freeing the thin and thick disc MASSES separately -- 3 parameters, no widened error bar anywhere, a0
      still an input on both footings -- reaches {wx_ex:.2f} sigma with {n_ex} cell(s) in the box. The MINIMAL
      clearing parameter count is {hk}; the fourth parameter buys {g4:.3f} sigma more (S4b) and by AIC is
      {'worth it' if aic[2] < aic[1] else 'not worth it'}.
    * THE CONTROL, the single most important line here: the superseded alpha=2 kernel with the IDENTICAL
      family, prefilter, extractor and priors {_ctrl} -- it reaches {wx_a2:.2f} sigma with {n_a2} cells. The
      literature's simple mu reaches {wx_sm:.2f} sigma with {n_sm} cell(s). So the escape is attributable to
      the KERNEL and not to the parameter count.
    * WHAT IT COSTS, stated as plainly as the win: the clearing cell sits in a CORNER of the prior box --
      M_* {sH['mstar']:+.2f}, R_d {sH['rd']:+.2f}, Sigma_* {sH['sig']:+.2f} sigma -- which is {sig_pri:.2f}
      sigma JOINTLY (S6c), with total chi2 = {chi2(H)[0]:.2f} on {5-hk} dof. And box membership depends on the
      2026-08-02 interpolated extractor: on the anchor's nearest-cell reading the same cell's vertical force
      is {(H['sd_snap']-KZ)/KZ_E:+.2f} sigma and its worst constraint {s_snap:.2f}, i.e. it would
      {'still clear' if s_snap <= BOX else 'NOT clear'} (S6b).

  THE PHYSICS, which is the transferable part. v_c(R0) is set by the radial force at R0, i.e. by mass INSIDE
  R0, while Sigma_dyn is set by the local slab column at R0. A single common mass scale cannot separate those
  -- it raises both -- which is exactly why the 2-parameter family stalled at {w2_ex:.2f} sigma. Freeing the
  thin/thick split lets the fit buy enclosed mass while spending the local stellar column DOWN toward the low
  end of Bovy & Rix, and the vertical constraint is then met by having LESS baryonic column in the slab rather
  than by a weaker kernel. The scale height, which the brief expected to be the pure knob, is NOT one: it
  moves Sigma_* and Sigma_dyn together at a ratio of {abs(d_sg/d_sd):.2f} because they are columns through the
  same slab (S4a). And Route A's ~10% stronger boost in g at the Galaxy's own y is what makes v_c reachable
  inside the mass prior at all -- alpha=2 needs ~1.5x the mass for the same v_c and cannot get it (S5c).""")


banner("SCOPE AND CAVEATS")
print(f"""   * NO error bar was widened anywhere. Every sigma divides by the anchor's own published uncertainty,
     with the TIGHTER v_c convention (+-3.0 km/s, McMillan's statistical) doing all the deciding; +-4.0 is
     printed at the headline cell for information only. Required widening for the box to close: NONE.
   * The box is max |sigma| <= {BOX:.0f} on five constraints ONE AT A TIME. That is the corpus's own
     operationalisation (L7's BOX) and it is answered on its own terms -- but S6c prices the JOINT departure,
     which is larger, and no reader should convert "clears the box" into "consistent with the star counts".
   * a0 was an INPUT throughout, both footings, never fitted: canonical {A0_CANON:.4e} and alt {A0_ALT:.4e}.
   * The PREFILTER solves only shapes already within {PREFILTER} sigma on all three analytic priors -- exact
     for the box question, applied identically to all six combinations. chi2 minima are therefore minima
     WITHIN that region and, like the anchor's, are UPPER bounds on what the family could reach.
   * Gas held at survey values, bulge at DIRBE, R0 = 8.21 kpc fixed, and the vertical constraint compressed
     to the single number K_z,1.1. The real data constrain more than that number: Holmberg & Flynn's K_z(z)
     PROFILE and Bovy & Rix's Sigma(R) profile bear on the vertical and radial distribution, so a fit that
     moves the scale height or the thin/thick split is exploiting freedom the five-constraint box grants and
     the underlying observations do not. Read anything here about f_z, f_Rk or the thick-disc fraction as
     "the box permits it", never as "the data permit it". THE SAME APPLIES TO THE HEADLINE CELL: its
     thin/thick mass split is not itself confronted with star counts anywhere in this script.
   * Still not tested: the full rotation curve rather than v_c(R0) alone, R0, the gas, the external-field
     effect, and the MI (as opposed to AQUAL) realisation of the same kernel -- a DIFFERENT theory outside
     spherical symmetry, and not what this solver integrates.
   * {NSOLVE} AQUAL solves on the anchor mesh (n = 110, growth 1.085, 400 Picard) except the S6a refinement.""")

banner("RESULT")
n = sum(1 for t, _ in ok if t)
print(f"  {n}/{len(ok)} checks held.   {NSOLVE} solves, {time.time()-T0:.0f}s"
      f"{'   *** MI_FAST SMOKE RUN -- NOT THE REPORTED NUMBERS ***' if FAST else ''}")
if n != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the shape knob measured, the control run under the identical family, the cost priced.")
