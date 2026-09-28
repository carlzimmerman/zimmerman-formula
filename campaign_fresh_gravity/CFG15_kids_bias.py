#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG15 -- DOES CFG12's CANONICAL WINDOW SURVIVE A PHYSICAL 2-HALO AMPLITUDE?

WHY.  CFG12 opened CFG4's strict window on the canonical footing: KiDS floor 0.303-0.309 (2-halo amplitude A fitted in [0, 2] per
lens bin) against a budget edge 0.338-0.341 (FG001's grouping + the share at the budget's own scale).  The 2-halo template (FP1 E,
L355) is the projected MATTER correlation, so A is the lens bias.  A cap of 2 allows bias-2 lenses; KiDS's isolated lenses (no
brighter neighbour within 3 Mpc) are galaxy-mass systems whose bias is expected near or below 1.  If the floor rises above ~0.34
at a physical bias, CFG12's 'canonical conflict resolved' does not hold.

THE FRAMEWORK'S OWN LENS BIAS.  Each lens bin's profiled baryonic mass (CFG4_switch's committed log M_b = 10.4/10.9/11.05/11.25)
-> the law's turnaround mass at z_l = 0.25 (CFG4's convention: the enclosed mass at r_ta, Delta_ta(0.25) = 8.89) -> sigma(M) at
z_l (CLASS via CFG7_common, growth from its cosmology) -> the peak-background-split bias b = 1 + (nu^2 - 1)/delta, nu = delta/sigma,
for the collapse threshold (1.686) and the turnaround threshold (delta_lin,ta(0.25) = 1.208, CFG4_switch D1).  The cap per bin is
the larger of the two (generous; isolation only lowers a bias).

PRE-DECLARED (before this script's first run)
  C1  CONTROL  the exec'd KiDS machinery reproduces CFG4_switch's committed x-scan (A = 0 and A <= 2 rows, both footings, both
      kernels) to 1e-6.
  C2  CONTROL  the per-bin-cap copy of FP1's kfit equals FP1's kfit for scalar caps (0, 1, 2) exactly.
  D1  (reported) the framework's lens bias per bin, both thresholds.
  H1  [HEADLINE; MUTATE must fail] at the framework's own lens bias the canonical KiDS floor stays at or below CFG12's canonical
      budget edge (0.341 P2 / 0.338 nu_mono): the window survives.  Expectation: uncertain.
  H2  the same with unbiased lenses (A <= 1).
  R1  (reported) the floor versus the cap (0-2) on both footings; the fitted A per bin at the A <= 2 floor.
MUTATE=1: no 2-halo term (cap 0) in H1 -- the floor returns to 0.47 and H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG15_kids_bias.py   (MUTATE=1 for the control; a few minutes)
"""
import os, sys, math, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG15_kids_bias", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: no 2-halo term in H1 -- H1 must FAIL ***")
np.seterr(all="ignore")
SWJ = json.load(open(os.path.join(HERE, "CFG4_switch_results.json")))["numbers"]
C12 = json.load(open(os.path.join(HERE, "CFG12_budget_scale_results.json")))["numbers"]["H"]

# ================================================================================================ the committed KiDS machinery (exec'd slices)
SWP = os.path.join(HERE, "CFG4_switch.py")
ns = {"np": np, "math": math, "os": os, "C": C, "A0": C.A0, "time": time, "t3": time.time(), "P": lambda *a, **k: None,
      "DTA": {0.25: (SWJ["D1"]["0.25"]["one_plus_delta_ta"], SWJ["D1"]["0.25"]["delta_lin_ta"])}}
ns = C.exec_slices(SWP, [('GK = {"np": np', 'check("K3 CONTROL'),
                         ('ZL = GK["ZL"]', "def M_trunc_fixed("),
                         ("def r_bound(", "def M_trunc_bound("),
                         ("def M_trunc_xta(", "chk_full, LMB, _ = kfit_full(")], ns=ns, name="cfg4_switch_slices")[0]
GK, FIX, kids_chi2, M_trunc_xta = ns["GK"], ns["FIX"], ns["kids_chi2"], ns["M_trunc_xta"]
BASE = ns["BASE"]; LM, NPB, RPK, MPCK, MSK = GK["LM"], GK["npb"], GK["Rp"], GK["MPCm"], GK["MS"]
KERN = {"P2": C.nu_p2, "nu_mono": C.nu_mono}


def table(Mfun, foot):
    """kids_chi2's model table (the same six lines), built once per profile so every cap reuses it."""
    T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, C.A0[foot]), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    return T


W0 = np.zeros(len(GK["ES"])); W0[0] = 1.0


def kfit_caps(T, caps):
    """FP1's kfit with a per-bin cap on the 2-halo amplitude (the same algebra; caps a length-4 sequence)."""
    blk = np.tensordot(W0, T, axes=(0, 0))
    D = np.concatenate(GK["Ed"])
    mods, pars = [], []
    for b in range(4):
        bb = None
        for im in range(len(LM)):
            mk = blk[im, b]
            A = 0.0
            if caps[b] > 0:
                t2 = GK["T2H"][b]; wv = 1 / GK["Sd"][b] ** 2
                A = float(np.clip(np.sum(wv * t2 * (GK["Ed"][b] - mk)) / np.sum(wv * t2 * t2), 0.0, caps[b]))
                mk = mk + A * t2
            c__ = float(np.sum(((GK["Ed"][b] - mk) / GK["Sd"][b]) ** 2))
            if bb is None or c__ < bb[0]:
                bb = (c__, mk, LM[im], A)
        mods.append(bb[1]); pars.append(bb[3])
    dv = D - np.concatenate(mods)
    return float(dv @ GK["Ci"] @ dv), pars


# ================================================================================================ C1 / C2
R.banner("C1 / C2  CONTROLS: CFG4_switch's committed x-scan; the per-bin-cap kfit")
XS0 = SWJ["H2c"]["x"]
dev1, dev2 = 0.0, 0.0
TAB = {}
for f in C.FOOTS:
    for kn, kf in KERN.items():
        for x in XS0:
            T = table(M_trunc_xta(kf, x), f)
            TAB[(f, kn, x)] = T
            for A in (0.0, 2.0):
                mine = kfit_caps(T, [A] * 4)[0] - BASE[(f, kn)]
                ref = SWJ["H2c"]["scan"][f"{f}|{kn}|A{A:.0f}"][XS0.index(x)]
                dev1 = max(dev1, abs(mine - ref))
            for A in (0.0, 1.0, 2.0):
                dev2 = max(dev2, abs(kfit_caps(T, [A] * 4)[0] - GK["kfit"]({f: T}, f, W0, A)[0]))
check("C1 CONTROL: the exec'd KiDS machinery reproduces CFG4_switch's committed x-scan (A = 0 and A <= 2, both footings, both kernels)",
      f"max |d chi^2| {dev1:.1e}", dev1 <= 1e-6)
check("C2 CONTROL: the per-bin-cap kfit equals FP1's kfit for scalar caps 0 / 1 / 2", f"max |d chi^2| {dev2:.1e}", dev2 <= 1e-9)

# ================================================================================================ D1 the framework's lens bias
R.banner("D1  THE FRAMEWORK'S OWN LENS BIAS (peak-background split at each bin's turnaround mass, z_l = 0.25)")
cos = C7.LCDM
LMB = SWJ["H2c"]["lens_logMb_P2_canonical"]
DL_TA = SWJ["D1"]["0.25"]["delta_lin_ta"]
DC = 1.686
gz = float(cos.D(1.0 / 1.25) / cos.D(1.0))                                                # D(z_l)/D(0), CFG7_common's growth table
RRK = GK["rrK"]; MSUN = GK["MS"]
BIAS = {}
for f in C.FOOTS:
    for kn, kf in KERN.items():
        bs = []
        for lm in LMB:
            Mb = 10 ** lm * MSK
            M = ns["M_law"](kf)(Mb, C.A0[f])
            rta = ns["r_bound"](M, ns["DTA"][0.25][0])
            Mta = float(np.interp(rta, RRK, M)) / MSUN
            s = math.sqrt(C7.sig2(float(C7.R_lagr(Mta, cos)), float(C7.R_lagr(Mta, cos)), cos)) * gz
            bc = 1 + ((DC / s) ** 2 - 1) / DC
            bt = 1 + ((DL_TA / s) ** 2 - 1) / DL_TA
            bs.append(dict(logMb=lm, M_ta=Mta, sigma=s, b_collapse=bc, b_turnaround=bt, cap=max(bc, bt)))
        BIAS[(f, kn)] = bs
        P(f"    {f:9s} {kn:8s}: " + "; ".join(f"logMb {b['logMb']}: M_ta {b['M_ta']:.2e}, sigma {b['sigma']:.2f}, b {b['b_collapse']:.2f}/"
                                             f"{b['b_turnaround']:.2f}" for b in bs) + f"  (D(0.25)/D(0) = {gz:.4f})")
check("D1 (reported) the framework's lens bias per KiDS bin (collapse / turnaround thresholds)",
      "; ".join(f"{k[0][:3]}/{k[1]}: " + "/".join(f"{b['cap']:.2f}" for b in v) for k, v in BIAS.items()), True, load_bearing=False)

# ================================================================================================ the floors
R.banner("THE KiDS FLOOR VERSUS THE 2-HALO CAP")
XF = np.round(np.arange(0.20, 0.601, 0.01), 2)


def floor_for(f, kn, caps):
    v = []
    for x in XF:
        key = (f, kn, float(x))
        if key not in TAB:
            TAB[key] = table(M_trunc_xta(KERN[kn], float(x)), f)
        v.append(kfit_caps(TAB[key], caps)[0] - BASE[(f, kn)])
    v = np.array(v)
    ok = np.where(v <= 9.0)[0]
    if not len(ok):
        return float("inf"), v
    j = ok[0]
    if j == 0:
        return float(XF[0]), v
    return float(XF[j - 1] + (9.0 - v[j - 1]) * (XF[j] - XF[j - 1]) / (v[j] - v[j - 1])), v


FL = {}
for f in C.FOOTS:
    for kn in KERN:
        for cap in (0.0, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0):
            FL[(f, kn, cap)] = floor_for(f, kn, [cap] * 4)[0]
        own = [0.0] * 4 if MUTATE else [b["cap"] for b in BIAS[(f, kn)]]
        FL[(f, kn, "own")] = floor_for(f, kn, own)[0]
        P(f"    {f:9s} {kn:8s}: floor at cap " + ", ".join(f"{c:g}: {FL[(f, kn, c)]:.3f}" for c in (0.0, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0))
          + f"; at the framework's own bias{' [MUTATE: 0]' if MUTATE else ''}: {FL[(f, kn, 'own')]:.3f}; CFG12 budget edge (FG001) "
          f"{C12[f'{f}|{kn}']['x_fg001']:.3f}")
h1 = all(FL[("canonical", kn, "own")] <= C12[f"canonical|{kn}"]["x_fg001"] for kn in KERN)
check("H1 [HEADLINE] at the framework's own lens bias the canonical KiDS floor stays at or below CFG12's canonical budget edge -- the "
      "canonical window survives" + ("  [MUTATE: no 2-halo]" if MUTATE else ""),
      "; ".join(f"{kn}: floor {FL[('canonical', kn, 'own')]:.3f} vs edge {C12[f'canonical|{kn}']['x_fg001']:.3f}" for kn in KERN), h1)
h2 = all(FL[("canonical", kn, 1.0)] <= C12[f"canonical|{kn}"]["x_fg001"] for kn in KERN)
check("H2 with unbiased lenses (A <= 1) the canonical floor stays at or below the budget edge",
      "; ".join(f"{kn}: floor {FL[('canonical', kn, 1.0)]:.3f} vs edge {C12[f'canonical|{kn}']['x_fg001']:.3f}" for kn in KERN), h2)
# fitted A per bin at the A <= 2 floor (canonical)
Afit = {}
for kn in KERN:
    x2 = FL[("canonical", kn, 2.0)]
    xs = float(np.round(max(0.2, min(0.6, x2)), 2))
    key = ("canonical", kn, xs)
    if key not in TAB:
        TAB[key] = table(M_trunc_xta(KERN[kn], xs), "canonical")
    Afit[kn] = (xs, [round(a, 2) for a in kfit_caps(TAB[key], [2.0] * 4)[1]])
check("R1 (reported) the floor versus the cap; the fitted A per bin near the A <= 2 floor (canonical)",
      "; ".join(f"{kn} at x = {v[0]}: A = {v[1]}" for kn, v in Afit.items()), True, load_bearing=False)
R.num("bias", {f"{k[0]}|{k[1]}": v for k, v in BIAS.items()})
R.num("floors", {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in FL.items()})
R.num("Afit", Afit)
nf = R.write()
sys.exit(1 if nf else 0)
