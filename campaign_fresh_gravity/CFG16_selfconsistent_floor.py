#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG16 -- THE SELF-CONSISTENT KiDS FLOOR: the lens bias taken from the TRUNCATED profile's own turnaround mass.

WHY.  CFG15 found CFG12's canonical window open at the framework's peak-background lens bias (1.1-1.6) and closed for unbiased lenses.
But that bias was computed at the law's UNTRUNCATED turnaround mass.  With the phantom cut at x r_ta (CFG4's density edge), the
system's actual enclosed mass beyond the edge stays M_e = M_law(x r_ta), so its actual turnaround mass is smaller and its bias lower.
The floor depends on the bias and the bias on x: the zero-parameter closure is the self-consistent floor, where at every x the 2-halo
cap of each lens bin is the peak-background bias of that bin's truncated turnaround mass.  The bias used is an UPPER estimate (KiDS's
isolation criterion selects low-density environments and lowers it), so a closed window here is robust; an open one is not.

THE CLOSURE (CFG4's conventions throughout).  At each x: the truncated profile (CFG4_switch's M_trunc_xta, exec'd read-only) -> its
turnaround radius with CFG4_switch's r_bound at Delta_ta(0.25) = 8.89 -> M_ta'(x) = the truncated profile's enclosed mass there ->
sigma(M_ta') at z_l = 0.25 (CLASS via CFG7_common) -> b = max of the collapse (1.686) and turnaround (1.208) peak-background biases.
The floor is the smallest x with d chi^2 <= +9 against the untruncated law (CFG4's KIDS_TOL) with those caps.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  CFG15's committed floors at scalar caps (0, 1, 2) and at its untruncated-mass bias are reproduced exactly.
  D1  (reported) the truncated turnaround masses and biases per bin at x = 0.30 / 0.34, against CFG15's untruncated ones.
  H1  [HEADLINE; MUTATE must fail] the self-consistent canonical floor stays at or below CFG12's canonical budget edge (0.341 P2 /
      0.338 nu_mono): the canonical window survives self-consistently.  Expectation: uncertain (a rough estimate puts it at the edge).
  R1  (reported) the alt footing's self-consistent floor against its edge (0.293 / 0.291).
MUTATE=1: caps held at 0 (no 2-halo) -- the floor returns to 0.47 and H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG16_selfconsistent_floor.py   (MUTATE=1 for the control; ~10 s)
"""
import os, sys, math, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG16_selfconsistent_floor", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: caps held at 0 -- H1 must FAIL ***")
np.seterr(all="ignore")
SWJ = json.load(open(os.path.join(HERE, "CFG4_switch_results.json")))["numbers"]
C12 = json.load(open(os.path.join(HERE, "CFG12_budget_scale_results.json")))["numbers"]["H"]
C15 = json.load(open(os.path.join(HERE, "CFG15_kids_bias_results.json")))["numbers"]

SWP = os.path.join(HERE, "CFG4_switch.py")
ns = {"np": np, "math": math, "os": os, "C": C, "A0": C.A0, "time": time, "t3": time.time(), "P": lambda *a, **k: None,
      "DTA": {0.25: (SWJ["D1"]["0.25"]["one_plus_delta_ta"], SWJ["D1"]["0.25"]["delta_lin_ta"])}}
ns = C.exec_slices(SWP, [('GK = {"np": np', 'check("K3 CONTROL'),
                         ('ZL = GK["ZL"]', "def M_trunc_fixed("),
                         ("def r_bound(", "def M_trunc_bound("),
                         ("def M_trunc_xta(", "chk_full, LMB, _ = kfit_full(")], ns=ns, name="cfg4_switch_slices")[0]
GK, FIX, M_trunc_xta, r_bound, M_law = ns["GK"], ns["FIX"], ns["M_trunc_xta"], ns["r_bound"], ns["M_law"]
BASE = ns["BASE"]; LM, NPB, RPK, MPCK, MSK, RRK = GK["LM"], GK["npb"], GK["Rp"], GK["MPCm"], GK["MS"], GK["rrK"]
KERN = {"P2": C.nu_p2, "nu_mono": C.nu_mono}
W0 = np.zeros(len(GK["ES"])); W0[0] = 1.0
DTA25 = ns["DTA"][0.25][0]; DL_TA = SWJ["D1"]["0.25"]["delta_lin_ta"]; DC = 1.686
cos = C7.LCDM
GZ = float(cos.D(1.0 / 1.25) / cos.D(1.0))
LMB = SWJ["H2c"]["lens_logMb_P2_canonical"]


def table(Mfun, foot):
    T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, C.A0[foot]), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    return T


def kfit_caps(T, caps):
    blk = np.tensordot(W0, T, axes=(0, 0))
    D = np.concatenate(GK["Ed"])
    mods = []
    for b in range(4):
        bb = None
        for im in range(len(LM)):
            mk = blk[im, b]
            if caps[b] > 0:
                t2 = GK["T2H"][b]; wv = 1 / GK["Sd"][b] ** 2
                A = float(np.clip(np.sum(wv * t2 * (GK["Ed"][b] - mk)) / np.sum(wv * t2 * t2), 0.0, caps[b]))
                mk = mk + A * t2
            c__ = float(np.sum(((GK["Ed"][b] - mk) / GK["Sd"][b]) ** 2))
            if bb is None or c__ < bb[0]:
                bb = (c__, mk)
        mods.append(bb[1])
    dv = D - np.concatenate(mods)
    return float(dv @ GK["Ci"] @ dv)


def bias_of(M_msun):
    s = math.sqrt(C7.sig2(float(C7.R_lagr(M_msun, cos)), float(C7.R_lagr(M_msun, cos)), cos)) * GZ
    return max(1 + ((DC / s) ** 2 - 1) / DC, 1 + ((DL_TA / s) ** 2 - 1) / DL_TA), s


def caps_at(f, kn, x, truncated=True):
    out = []
    for lm in LMB:
        Mb = 10 ** lm * MSK
        Mfun = M_trunc_xta(KERN[kn], x) if truncated else M_law(KERN[kn])
        M = Mfun(Mb, C.A0[f])
        rta = r_bound(M, DTA25)
        out.append(bias_of(float(np.interp(rta, RRK, M)) / GK["MS"])[0])
    return out


XF = np.round(np.arange(0.20, 0.601, 0.01), 2)
TAB = {}


def floor(f, kn, capfun):
    v = []
    for x in XF:
        key = (f, kn, float(x))
        if key not in TAB:
            TAB[key] = table(M_trunc_xta(KERN[kn], float(x)), f)
        v.append(kfit_caps(TAB[key], capfun(float(x))) - BASE[(f, kn)])
    v = np.array(v)
    ok = np.where(v <= 9.0)[0]
    if not len(ok):
        return float("inf")
    j = ok[0]
    return float(XF[0]) if j == 0 else float(XF[j - 1] + (9.0 - v[j - 1]) * (XF[j] - XF[j - 1]) / (v[j] - v[j - 1]))


# ================================================================================================ C1
R.banner("C1  CONTROL: CFG15's committed floors")
dev = 0.0
for f in C.FOOTS:
    for kn in KERN:
        for cap in (0.0, 1.0, 2.0):
            dev = max(dev, abs(floor(f, kn, lambda x, c=cap: [c] * 4) - C15["floors"][f"{f}|{kn}|{cap}"]))
        own = caps_at(f, kn, 1.0, truncated=False)
        dev = max(dev, abs(floor(f, kn, lambda x, o=own: o) - C15["floors"][f"{f}|{kn}|own"]))
check("C1 CONTROL: CFG15's committed floors at caps 0 / 1 / 2 and at its untruncated-mass bias reproduced exactly",
      f"max |d x| {dev:.1e}", dev <= 1e-9)

# ================================================================================================ D1
R.banner("D1  THE TRUNCATED TURNAROUND MASSES AND THEIR BIAS")
for f in C.FOOTS:
    for kn in ("P2",):
        un = caps_at(f, kn, 1.0, truncated=False)
        t30 = caps_at(f, kn, 0.30); t34 = caps_at(f, kn, 0.34)
        P(f"    {f:9s} {kn}: bias per bin untruncated {[round(b, 2) for b in un]}; truncated at x = 0.30 {[round(b, 2) for b in t30]}; "
          f"at x = 0.34 {[round(b, 2) for b in t34]}")
check("D1 (reported) the truncated turnaround masses' bias against CFG15's untruncated one (canonical and alt, P2)",
      "printed above", True, load_bearing=False)

# ================================================================================================ H1
R.banner("H1  THE SELF-CONSISTENT FLOOR")
SC = {}
for f in C.FOOTS:
    for kn in KERN:
        capfun = (lambda x: [0.0] * 4) if MUTATE else (lambda x, _f=f, _k=kn: caps_at(_f, _k, x))
        SC[(f, kn)] = floor(f, kn, capfun)
        P(f"    {f:9s} {kn:8s}: self-consistent floor {SC[(f, kn)]:.3f} (CFG15 untruncated-bias floor {C15['floors'][f'{f}|{kn}|own']:.3f}, "
          f"unbiased {C15['floors'][f'{f}|{kn}|1.0']:.3f}); CFG12 budget edge {C12[f'{f}|{kn}']['x_fg001']:.3f}")
h1 = all(SC[("canonical", kn)] <= C12[f"canonical|{kn}"]["x_fg001"] for kn in KERN)
check("H1 [HEADLINE] the self-consistent canonical floor stays at or below CFG12's canonical budget edge -- the window survives "
      "self-consistently" + ("  [MUTATE: no 2-halo]" if MUTATE else ""),
      "; ".join(f"{kn}: floor {SC[('canonical', kn)]:.3f} vs edge {C12[f'canonical|{kn}']['x_fg001']:.3f}" for kn in KERN), h1)
check("R1 (reported) the alt footing's self-consistent floor against its budget edge",
      "; ".join(f"{kn}: floor {SC[('alt', kn)]:.3f} vs edge {C12[f'alt|{kn}']['x_fg001']:.3f}" for kn in KERN), True, load_bearing=False)
R.num("floors", {f"{k[0]}|{k[1]}": v for k, v in SC.items()})
nf = R.write()
sys.exit(1 if nf else 0)
