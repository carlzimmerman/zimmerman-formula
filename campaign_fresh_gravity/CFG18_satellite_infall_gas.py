#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG18 -- FG001's SATELLITES WITH THEIR INFALL BARYONS, done properly.  A robustness test of FG001's exploratory H8 (NOT blind: H8's
outcome is known and is reproduced below as a control).

WHY.  FG001's class A says an accreted satellite KEEPS THE COLD COMPONENT IT CARRIED AT INFALL.  Its committed H4 nonetheless scored
the satellites with their CURRENT baryons (stars only -- ram pressure has since removed their gas), and the M31 LVD dwarfs sat
+0.116 / +0.096 dex above the isolated law (2.6 / 2.2 sigma): FG001's one failed satellite gate.  The FG001-consistent prediction
uses the baryons at infall.  FG001's H8 (exploratory) estimated the infall gas from a log-linear fit to the Local Volume field dwarfs
WITH HI DETECTIONS ONLY (32) and extrapolated it to every mass -- biased gas-rich (non-detections dropped) and extrapolated below the
calibrated range.  This lane removes both biases and propagates the spread.

THE METHOD (declared before the first run).  Calibration set: every LVD field dwarf with M_V and HI information -- detections
(mass_HI) and non-detections (mass_HI_ul) -- M_* = 2.0 L_V (FG001's Upsilon_V), gas = 1.33 M_HI.  For each satellite inside the
calibrated stellar-mass range, its infall gas-to-star ratio is drawn from its k = 5 nearest calibration dwarfs in log M_* (uniformly);
non-detections count as ZERO gas (the conservative bracket for FG001, headline) or AT THEIR UPPER LIMIT (reported).  Satellites below
the calibrated range get no infall gas (reionisation-era fossils; declared), with the nearest-neighbour draw reported.  Infall
baryons = M_* + max(current gas, the drawn gas).  2000 realisations (seed 18); per realisation the sample's median offset
log10(sigma_obs / sigma_isolated-law) and FG001's error of the median, 1.2533 rms / sqrt(n).  FG001's committed machinery is exec'd
read-only.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  FG001's committed H4 isolated medians (current stars) and H8 exploratory offsets reproduced exactly (both footings).
  H1  [HEADLINE; MUTATE must fail] with the infall gas drawn from field dwarfs at similar stellar mass (non-detections as zero), the
      MW classical dSphs and the M31 LVD dwarfs sit within 2 sigma of zero on both footings (the mean over realisations of the median
      offset, against the mean error of the median).
  H2  (reported) the same for M31 Collins+13 and the MW ultra-faints; the upper-limit bracket; the spread over realisations.
MUTATE=1: no infall gas (current baryons, FG001's H4) -- the M31 LVD offset returns to 2.6 sigma and H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG18_satellite_infall_gas.py   (MUTATE=1 for the control; ~1 min)
"""
import os, sys, math, json, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
import hunt_lib as HL
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG18_satellite_infall_gas", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: no infall gas (FG001's H4 baryons) -- H1 must FAIL ***")

FGP = os.path.join(HERE, "CFG7_hierarchy_fg001.py")
ns = {"np": np, "math": math, "os": os, "csv": csv, "C": C, "HL": HL}
ns = C.C4.exec_slices(FGP, [("G, kpc, Msun, A0H = HL.G", "# ================================================================================================ K1 h43"),
                            ("MW_MB, M31_MB, UPS_V = 6.0e10", "REF43 = {")], ns=ns, name="fg001_slices")[0]
A0H, UPS_V, resid = ns["A0H"], ns["UPS_V"], ns["resid"]
SAMPLES = {"ufd": ns["ufd"], "cls": ns["cls"], "col": ns["col"], "m31": ns["m31"]}
LABEL = {"ufd": "MW ultra-faint", "cls": "MW classical dSph", "col": "M31 Collins+2013", "m31": "M31 LVD"}
FG = json.load(open(os.path.join(HERE, "CFG7_hierarchy_fg001_results.json")))["numbers"]

# ================================================================================================ C1
R.banner("C1  CONTROL: FG001's committed H4 and H8 reproduced")
dev = 0.0
fg = [(math.log10(UPS_V * d["LV"]), math.log10(1.33 * d["MHI"] / (UPS_V * d["LV"]))) for d in ns["FIELD_ALL"]
      if d["LV"] and d["MHI"] and d["MHI"] > 0]
cf = np.polyfit(np.array([a for a, b in fg]), np.array([b for a, b in fg]), 1)
fgas_h8 = lambda d: UPS_V * d["LV"] * 10 ** np.polyval(cf, math.log10(UPS_V * d["LV"]))
for foot, a0 in A0H.items():
    for key in ("cls", "m31", "col", "ufd"):
        dev = max(dev, abs(float(np.median(resid(SAMPLES[key], a0, efe=False))) - FG["SAT"][f"{foot}|{key}"]["med_iso"]))
        dev = max(dev, abs(float(np.median(resid(SAMPLES[key], a0, efe=False, extra_mass=fgas_h8))) - FG["H8"]["offsets"][f"{foot}|{key}"]))
check("C1 CONTROL: FG001's committed H4 isolated medians and H8 exploratory offsets reproduced exactly", f"max |d| {dev:.1e}", dev <= 1e-12)

# ================================================================================================ the calibration set
def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None


CAL = []
for r in csv.DictReader(open(os.path.join(ns["DSPH"], "lvd_dwarf_local_field.csv"))):
    MV = fnum(r["M_V"]); mh = fnum(r["mass_HI"]); ul = fnum(r["mass_HI_ul"])
    if MV is None or (mh is None and ul is None):
        continue
    ms = UPS_V * 10 ** (0.4 * (4.83 - MV))
    det = mh is not None
    CAL.append((math.log10(ms), 1.33 * 10 ** (mh if det else ul) / ms, det))
CAL.sort()
LCAL = np.array([c[0] for c in CAL]); RAT = np.array([c[1] for c in CAL]); DET = np.array([c[2] for c in CAL])
LO, HI = LCAL.min(), LCAL.max()
P(f"\n  calibration set: {len(CAL)} LVD field dwarfs ({int(DET.sum())} HI detections, {int((~DET).sum())} upper limits); "
  f"log M_* {LO:.2f}-{HI:.2f}; detections' median gas/star {np.median(RAT[DET]):.2f}")
K = 5
rng = np.random.default_rng(18)
NREAL = 2000


def draws(sample, bracket, below="none"):
    """(NREAL, n) infall gas masses for a satellite sample."""
    out = np.zeros((NREAL, len(sample)))
    for j, d in enumerate(sample):
        lm = math.log10(UPS_V * d["LV"])
        if MUTATE:
            continue
        if lm < LO and below == "none":
            continue
        nn = np.argsort(np.abs(LCAL - lm))[:K]
        r_ = np.where(DET[nn], RAT[nn], RAT[nn] if bracket == "limit" else 0.0)
        pick = rng.integers(0, K, NREAL)
        out[:, j] = r_[pick] * UPS_V * d["LV"]
    return out


def offsets(sample, a0, gas):
    """per-realisation median offset and error of the median; infall baryons = M_* + max(current gas, drawn gas)."""
    meds, errs = [], []
    cur = np.array([1.33 * d["MHI"] for d in sample])
    for i in range(gas.shape[0]):
        extra = np.maximum(gas[i] - cur, 0.0)
        rr = resid(sample, a0, efe=False, extra_mass=lambda d, _e=dict(zip([id(s) for s in sample], extra)): _e[id(d)])
        meds.append(float(np.median(rr))); errs.append(1.2533 * float(np.std(rr)) / math.sqrt(len(rr)))
    return np.array(meds), np.array(errs)


# ================================================================================================ H1 / H2
R.banner("H1 / H2  THE SATELLITES WITH THEIR INFALL BARYONS")
RES = {}
for key in ("cls", "m31", "col", "ufd"):
    smp = SAMPLES[key]
    for bracket in ("zero", "limit"):
        gas = draws(smp, bracket)
        for foot, a0 in A0H.items():
            m_, e_ = offsets(smp, a0, gas)
            RES[(key, bracket, foot)] = dict(mean=float(m_.mean()), p16=float(np.percentile(m_, 16)), p84=float(np.percentile(m_, 84)),
                                             err=float(e_.mean()), z=float(abs(m_.mean()) / e_.mean()),
                                             stars_only=FG["SAT"][f"{foot}|{key}"]["med_iso"])
    if key == "ufd":
        gas = draws(smp, "zero", below="draw")
        for foot, a0 in A0H.items():
            m_, e_ = offsets(smp, a0, gas)
            RES[(key, "zero+draw-below", foot)] = dict(mean=float(m_.mean()), p16=float(np.percentile(m_, 16)),
                                                       p84=float(np.percentile(m_, 84)), err=float(e_.mean()),
                                                       z=float(abs(m_.mean()) / e_.mean()), stars_only=FG["SAT"][f"{foot}|{key}"]["med_iso"])
    n_in = sum(1 for d in smp if math.log10(UPS_V * d["LV"]) >= LO)
    for (k2, br, foot), v in RES.items():
        if k2 == key:
            P(f"    {LABEL[key]:18s} ({n_in}/{len(smp)} in range) {br:16s} {foot:9s}: median offset {v['mean']:+.3f} "
              f"(68% of realisations {v['p16']:+.3f}..{v['p84']:+.3f}) +- {v['err']:.3f} -> {v['z']:.1f} sigma "
              f"(stars only {v['stars_only']:+.3f})")
h1 = all(RES[(k, "zero", f)]["z"] <= 2.0 for k in ("cls", "m31") for f in A0H)
check("H1 [HEADLINE] with the infall gas drawn from field dwarfs at similar stellar mass (non-detections as zero), the MW classical "
      "dSphs and the M31 LVD dwarfs sit within 2 sigma of zero on both footings" + ("  [MUTATE: no infall gas]" if MUTATE else ""),
      "; ".join(f"{LABEL[k]} {f[:3]}: {RES[(k, 'zero', f)]['mean']:+.3f} ({RES[(k, 'zero', f)]['z']:.1f} sigma)" for k in ("cls", "m31")
                for f in A0H), h1)
check("H2 (reported) M31 Collins+13 and the MW ultra-faints; the upper-limit bracket",
      "; ".join(f"{LABEL[k]} {br} {f[:3]}: {v['mean']:+.3f} ({v['z']:.1f} sigma)" for (k, br, f), v in RES.items()
                if k in ("col", "ufd") or br == "limit"), True, load_bearing=False)
R.num("calibration", dict(n=len(CAL), n_det=int(DET.sum()), logMs_range=[float(LO), float(HI)], k=K))
R.num("RES", {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in RES.items()})
nf = R.write()
sys.exit(1 if nf else 0)
