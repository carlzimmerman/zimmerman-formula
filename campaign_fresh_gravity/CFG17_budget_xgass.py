#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG17 -- THE COLD BUDGET WITH A STELLAR-MASS-SELECTED GAS RELATION (xGASS).  Does CFG4's minimal conflict close once the budget's
gas is measured on a stellar-mass-selected sample instead of HI-selected SPARC?

WHY.  CFG16 left CFG4's minimal conflict at the margin: the self-consistent KiDS floor (0.3409 P2 / 0.3476 nu_mono canonical;
0.3402 / 0.3453 alt) sits above CFG12's strict budget edge (0.3406 / 0.3380 canonical; 0.2932 / 0.2910 alt).  The budget turns the
GAMA stellar mass function into baryons with SPARC's gas fractions, log(M_gas/M_*) = -0.456 log M_* + 4.19 -- and SPARC is HI-selected,
so it over-weights gas-rich galaxies (CFG4 already noted a stars-only budget relaxes by ~30%).  The xGASS representative sample
(Catinella et al. 2018; 1179 galaxies, 10^9-10^11.5 Msun, stellar-mass-selected, HI detections and upper limits, weights recovering
the GAMA stellar mass function -- the same function CFG4 integrates) measures the gas at fixed stellar mass without that selection.
Data: real_research/data/xgass/ (the team's public release, provenance recorded).

THE MEASUREMENT (CFG12's method, gas swapped).  For each xGASS galaxy, its phantom inside x r_ta (CFG4's isolated law, Delta_ta(0)) with
its own gas (M_gas = 1.33 M_HI, SPARC's convention; upper limits bracketed: at the limit -- conservative -- or zero) is divided by the
phantom with SPARC's gas relation at the same stellar mass; the weighted mean ratio in 0.1-dex stellar-mass bins rescales the budget's
integrand (SPARC's relation kept below 10^9, the last bin's ratio above 10^11.5).  FG001's grouping ratio R (CFG11, the most
conservative D <= 15 Mpc sample) is recomputed at x = 0.31 and 0.40 with the xGASS mean gas relation and interpolated exactly as
CFG12 did; the share at the budget's own scale is CFG12's (0.672 / 0.667).  CFG11's functions are exec'd read-only.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  with SPARC's gas the lane reproduces CFG11's committed R(0.31), R(0.40) (D <= 15, all four rows) and CFG12's committed
      FG001 strict edges (0.34062 / 0.33803 / 0.29318 / 0.29099) exactly.
  C2  CONTROL  the xGASS catalogue: 1179 galaxies; its weighted log M_* histogram (0.25-dex bins, 9.0-11.5) follows the GAMA (Baldry+12)
      stellar mass function CFG4 uses within 15% per bin after normalisation (the weights are read right).
  H1  [HEADLINE; MUTATE must fail] with xGASS's gas (non-detections at their limits) the canonical FG001 strict edge reaches CFG16's
      self-consistent KiDS floor for both kernels: the canonical window opens.  Expectation: uncertain.
  H2  the same on the alt footing.
  R1  (reported) the zero-gas bracket for non-detections; the per-bin phantom ratio xGASS/SPARC; R with xGASS's gas.
MUTATE=1: SPARC's gas relation is kept (the xGASS swap switched off) -- the edges return to CFG12's and H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG17_budget_xgass.py   (MUTATE=1 for the control; ~1 min)
"""
import os, sys, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG17_budget_xgass", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: SPARC's gas relation kept -- H1 must FAIL ***")
np.seterr(all="ignore")


class _Q:
    def banner(self, *a, **k):
        pass


# ================================================================================================ CFG11's committed functions (read-only)
C11P = os.path.join(HERE, "CFG11_budget_hierarchy.py")
ns = {"np": np, "math": math, "os": os, "json": json, "C": C, "C7": C7, "HERE": HERE, "MUTATE": False, "P": lambda *a, **k: None,
      "R": _Q()}
ns = C.exec_slices(C11P, [("SW = json.load(", 'R.banner("C1  CONTROL: CFG4_target'),
                          ("def read_vizier(", 'check("C2 CONTROL'),
                          ("def baryons(", 'R.banner("THE SAMPLES')], ns=ns, name="cfg11_slices")[0]
C11 = json.load(open(os.path.join(HERE, "CFG11_budget_hierarchy_results.json")))["numbers"]["RES"]
C12 = json.load(open(os.path.join(HERE, "CFG12_budget_scale_results.json")))["numbers"]
C16 = json.load(open(os.path.join(HERE, "CFG16_selfconsistent_floor_results.json")))["numbers"]["floors"]
A0 = C.A0; KERN = {"P2": C.nu_p2, "nu_mono": C.nu_mono}
UPSK = 0.6
OC0 = ns["OC0"]; lmg = ns["lmg"]; phi_h = ns["phi_h"]; RHOC0_MSUN = ns["RHOC0_MSUN"]; Mst_h = ns["Mst_h"]
MB_SMF = ns["_MB_SMF"]; mph_of = ns["mph_of"]; cfit = ns["cfit"]
m15, L15 = ns["sample"](15.0)
MLIM = math.log10(UPSK * L15)
sparc_baryons = ns["baryons"]

# ================================================================================================ the xGASS catalogue
XD = os.path.join(C.REPO, "real_research", "data", "xgass", "xGASS_representative_sample.ascii")
hdr = open(XD).readline().lstrip("#").split()
tab = np.genfromtxt(XD, comments="#", dtype=None, encoding=None, names=hdr)
lms = np.asarray(tab["lgMstar"], float); lgHI = np.asarray(tab["lgMHI"], float); src = np.asarray(tab["HIsrc"], int)
wts = np.asarray(tab["weight"], float)
DET = src != 4
MS_X = 10 ** lms
GAS_A = 1.33 * 10 ** lgHI                                                             # non-detections at their upper limits
GAS_B = np.where(DET, GAS_A, 0.0)                                                    # non-detections as zero gas
BINS = np.round(np.arange(9.0, 11.501, 0.1), 2)


def fgas_sparc(ms):
    return 10 ** np.polyval(cfit, np.log10(ms))


def binned(vals, w):
    out = []
    for lo, hi in zip(BINS[:-1], BINS[1:]):
        m = (lms >= lo) & (lms < hi) & np.isfinite(vals)
        out.append(np.sum(w[m] * vals[m]) / np.sum(w[m]) if m.sum() >= 3 else np.nan)
    return np.array(out)


BC = 0.5 * (BINS[:-1] + BINS[1:])

# ================================================================================================ C2 the weights
R.banner("C2  CONTROL: the xGASS weights recover the GAMA stellar mass function")
edges = np.arange(9.0, 11.501, 0.25)
hw = np.array([wts[(lms >= a) & (lms < b)].sum() for a, b in zip(edges[:-1], edges[1:])])
LMS_, PHI1, AL1, PHI2, AL2 = 10.66, 3.96e-3, -0.35, 0.79e-3, -1.47
phi_b = lambda l: math.log(10) * np.exp(-10 ** (l - LMS_)) * (PHI1 * 10 ** ((l - LMS_) * (AL1 + 1)) + PHI2 * 10 ** ((l - LMS_) * (AL2 + 1)))
hs = np.array([np.mean(phi_b(np.linspace(a, b, 21))) for a, b in zip(edges[:-1], edges[1:])])
rel = (hw / hw.sum()) / (hs / hs.sum()) - 1
P(f"    {len(lms)} galaxies ({int((~DET).sum())} HI non-detections); weighted histogram / Baldry SMF - 1 per 0.25-dex bin: "
  + ", ".join(f"{a:.2f}: {r_:+.2f}" for a, r_ in zip(edges[:-1], rel)))
check("C2 CONTROL: 1179 galaxies; the weighted log M_* histogram follows the GAMA (Baldry+12) SMF within 15% per 0.25-dex bin",
      f"N = {len(lms)}; max |dev| {np.max(np.abs(rel)):.3f}", len(lms) == 1179 and np.max(np.abs(rel)) <= 0.15)


# ================================================================================================ the gas swap
def ratio_curve(f, kn, x, gas):
    """the weighted mean phantom ratio (own gas / SPARC's relation) in 0.1-dex stellar-mass bins, mapped onto the SMF grid."""
    kf = KERN[kn]
    own = mph_of(MS_X * (1 + gas / MS_X) * C.MSUN, kf, A0[f], 0.0, x)
    spc = mph_of(MS_X * (1 + fgas_sparc(MS_X)) * C.MSUN, kf, A0[f], 0.0, x)
    rb = binned(own / spc, wts)
    ok = np.isfinite(rb)
    r = np.interp(lmg, BC[ok], rb[ok])
    return np.where(lmg < 9.0, 1.0, r), rb


_OM = {}


def omega_x(f, kn, x, mcut, gas):
    key = (f, kn, x, gas)
    if key not in _OM:
        mph = mph_of(MB_SMF, KERN[kn], A0[f], 0.0, x)
        r = np.ones_like(lmg) if gas == "sparc" else ratio_curve(f, kn, x, GAS_A if gas == "A" else GAS_B)[0]
        _OM[key] = phi_h * mph * r
    m = np.log10(Mst_h) >= mcut
    return float(np.trapz(_OM[key][m], lmg[m]) / RHOC0_MSUN)


def xgass_baryons_factory(gas):
    fb = binned((gas if gas is not None else fgas_sparc(MS_X) * MS_X) / MS_X, wts)
    ok = np.isfinite(fb)

    def baryons(Lk, upsK):
        Ms = upsK * Lk
        lg = np.log10(Ms)
        fg = np.where(lg < 9.0, 10 ** np.polyval(cfit, lg), np.interp(lg, BC[ok], fb[ok]))
        return Ms * (1 + fg), Ms
    return baryons


def R_at(f, kn, x, gas):
    ns["baryons"] = sparc_baryons if gas == "sparc" else xgass_baryons_factory(GAS_A if gas == "A" else GAS_B)
    ns["_RC"].clear()
    return ns["ratio"](m15, UPSK, KERN[kn], A0[f], x)


XS = np.round(np.arange(0.20, 0.801, 0.005), 3)


def edge(f, kn, gas):
    r31, r40 = R_at(f, kn, 0.31, gas), R_at(f, kn, 0.40, gas)
    Rf = lambda x: float(np.interp(x, [0.31, 0.40], [r31, r40]))
    lim = OC0 * C12["D1"][f"{f}|{kn}"]["f_ta"]
    om = np.array([omega_x(f, kn, float(x), 7.0, gas) - (1.0 - Rf(float(x))) * omega_x(f, kn, float(x), MLIM, gas) for x in XS])
    if om[0] > lim:
        return 0.0, r31, r40
    if om[-1] <= lim:
        return float(XS[-1]), r31, r40
    return float(np.interp(lim, om, XS)), r31, r40


# ================================================================================================ C1
R.banner("C1  CONTROL: SPARC's gas reproduces CFG11's R and CFG12's FG001 edges")
dev_r, dev_e = 0.0, 0.0
for f in C.FOOTS:
    for kn in KERN:
        e, r31, r40 = edge(f, kn, "sparc")
        v = C11[f"D<=15|{f}|{kn}"]
        dev_r = max(dev_r, abs(r31 - v["R031"]), abs(r40 - v["R04"]))
        dev_e = max(dev_e, abs(e - C12["H"][f"{f}|{kn}"]["x_fg001"]))
        P(f"    {f:9s} {kn:8s}: R(0.31) {r31:.5f} (CFG11 {v['R031']:.5f}), R(0.40) {r40:.5f} ({v['R04']:.5f}); edge {e:.5f} "
          f"(CFG12 {C12['H'][f'{f}|{kn}']['x_fg001']:.5f})")
check("C1 CONTROL: with SPARC's gas the lane reproduces CFG11's committed R (D <= 15) and CFG12's committed FG001 strict edges",
      f"max |d R| {dev_r:.1e}, max |d edge| {dev_e:.1e}", dev_r <= 1e-9 and dev_e <= 1e-9)

# ================================================================================================ H1 / H2
R.banner("H1 / H2  THE FG001 STRICT EDGE WITH xGASS's GAS, AGAINST CFG16's SELF-CONSISTENT KiDS FLOOR")
RES = {}
for f in C.FOOTS:
    for kn in KERN:
        eA, rA31, rA40 = edge(f, kn, "sparc" if MUTATE else "A")
        eB, rB31, _ = edge(f, kn, "B")
        _, rb = ratio_curve(f, kn, 0.34, GAS_A)
        fl = C16[f"{f}|{kn}"]
        RES[(f, kn)] = dict(edge_A=eA, edge_B=eB, R031_A=rA31, R040_A=rA40, R031_B=rB31, floor=fl, gap_A=fl - eA, gap_B=fl - eB,
                            ratio_bins=[None if not np.isfinite(v) else float(v) for v in rb])
        P(f"    {f:9s} {kn:8s}: edge (limits kept) {eA:.4f}, (limits as zero) {eB:.4f}; KiDS floor {fl:.4f}; gap {fl - eA:+.4f} / "
          f"{fl - eB:+.4f}; R(0.31) {rA31:.4f}; phantom ratio xGASS/SPARC at log M_* 9.5 / 10.0 / 10.5 / 11.0: "
          + "/".join(f"{np.interp(v, BC[np.isfinite(rb)], rb[np.isfinite(rb)]):.3f}" for v in (9.5, 10.0, 10.5, 11.0)))
h1 = all(RES[("canonical", kn)]["edge_A"] >= RES[("canonical", kn)]["floor"] for kn in KERN)
check("H1 [HEADLINE] with xGASS's gas (non-detections at their limits) the canonical FG001 strict edge reaches CFG16's self-consistent "
      "KiDS floor for both kernels" + ("  [MUTATE: SPARC's gas]" if MUTATE else ""),
      "; ".join(f"{kn}: edge {RES[('canonical', kn)]['edge_A']:.4f} vs floor {RES[('canonical', kn)]['floor']:.4f}" for kn in KERN), h1)
h2 = all(RES[("alt", kn)]["edge_A"] >= RES[("alt", kn)]["floor"] for kn in KERN)
check("H2 the same on the alt footing",
      "; ".join(f"{kn}: edge {RES[('alt', kn)]['edge_A']:.4f} vs floor {RES[('alt', kn)]['floor']:.4f}" for kn in KERN), h2)
check("R1 (reported) the zero-gas bracket for non-detections",
      "; ".join(f"{k[0][:3]}/{k[1]}: edge {v['edge_B']:.4f} vs floor {v['floor']:.4f}" for k, v in RES.items()), True, load_bearing=False)
R.num("RES", {f"{k[0]}|{k[1]}": v for k, v in RES.items()})
R.num("weights_vs_smf", dict(edges=list(edges), rel=list(rel)))
nf = R.write()
sys.exit(1 if nf else 0)
