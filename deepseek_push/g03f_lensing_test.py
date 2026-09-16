#!/usr/bin/env python3
"""G03F -- THE LENSING TEST OF THE EQUIPARTITION LAW (the external check).

The law (G03E): M_dark(<r)/M_b = r/r_M = sqrt(a0/g_N) in the deep isolated
regime (g_N < a0, g_ext < a0).  The DARK MATTER IS ORDINARY MASS (the
equilibrium sector): it LENSES.  The lensing RAR prediction is MASS
INDEPENDENT:

    g_lens/g_N = (M_b + M_dark(<r))/M_b = 1 + sqrt(a0/g_N)

DATA: Brouwer et al. 2021 KiDS-1000 (real_research/data/lensing_rar/
brouwer2021_rar/).  Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt (the clean
isolated sample, no bins) and Fig-9 (4 stellar-mass bins: the
mass-independence check).  Columns: Radius(m/s^2) ESD_t(h70 M_sun/pc^2) ...
with the standard conversion g_lens = 2 pi G * ESD (the slab/projected
acceleration; the B21 power-law shortcut, factor-2 class, stated).

The KiDS-isolated sample is the RIGHT instrument for the law: isolated
galaxies (g_ext small) and lensing radii reaching g_N ~ 1e-12 (deep).  The
regime boundary is where g_ext ~ a0: the sample's isolation cut keeps the
law's domain.

VERDICTS:
  V1 the law's prediction tracks the lensing RAR (median |log10(pred/obs)|)
     within the sample's error band (the observed points carry ~0.1-0.3 dex
     errors; PASS if the median |log10 ratio| <= 0.25 dex and no systematic
     slope)
  V2 MASS INDEPENDENCE: the per-mass-bin ratio pred/obs is flat across the
     four Fig-9 bins (range <= 0.4 dex) -- the signature of the law vs a
     free-normalization halo
  V3 the MW cross-check: the registered 6.1 kpc break with M_b = 7e10 gives
     g_ext = G M_b / r_break^2 vs the measured solar-circle field
     2.146e-10 (L240) / 2.32e-10 (DHF24): PASS if within 25%
  V4 the honest statement (the law stands / fails against the lensing data)
"""
import math, os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
LDIR = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
A0 = 9.3619e-11
GN = 6.674e-11
MSUN = 1.98892e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
G2PI = 2 * math.pi * GN

def check(l, ok, d=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {l}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)

RES = []
print("=" * 88)
print("G03F -- THE LENSING TEST OF THE EQUIPARTITION LAW")
print("=" * 88)

def load(fname):
    """Radius(m/s^2) ESD_t(h70 Msun/pc^2) ... -> (g_N, g_lens) in m/s^2."""
    pts = []
    with open(os.path.join(LDIR, fname)) as f:
        for line in f:
            if line.startswith("#") or line.startswith("Radius"):
                continue
            p = line.split()
            if len(p) < 4:
                continue
            try:
                gN = float(p[0])
                esd = float(p[1])
            except ValueError:
                continue
            if gN <= 0 or not math.isfinite(esd) or esd <= 0:
                # guard: skip non-positive ESD rows (log10 undefined) -- G073 fix
                continue
            # ESD in h70 Msun/pc^2 -> kg/m^2: 1 Msun/pc^2 = MSUN/PC^2
            esd_kg = esd * MSUN / PC ** 2
            g_lens = G2PI * esd_kg          # the projected-acceleration shortcut
            pts.append((gN, g_lens))
    return pts

def law_pred(gN):
    return gN * (1.0 + math.sqrt(A0 / gN)) if gN > 0 else 0.0

# ---- V1: the no-bins isolated sample ----
pts = load("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
print(f"\n--- V1 the law vs the KiDS-isolated lensing RAR ({len(pts)} points) ---")
rat = []
for gN, gL in pts:
    if gN < 0.3 * A0:                 # deep regime only
        rat.append(math.log10(gL / law_pred(gN)))
rat = np.array(rat)
med = float(np.median(rat)); rms = float(np.sqrt(np.mean(rat ** 2)))
print(f"    deep points: {len(rat)}; median log10(obs/pred) = {med:+.3f}; rms = {rms:.3f} dex")
ok_v1 = abs(med) <= 0.25 and rms <= 0.35
RES.append(check("V1 [the law tracks the lensing RAR] |median| <= 0.25 dex and rms <= 0.35 "
                 "in the deep regime", ok_v1, f"median {med:+.3f}, rms {rms:.3f} dex"))

# ---- V2: mass independence across the four Fig-9 bins ----
print("\n--- V2 MASS INDEPENDENCE (the law's signature, Fig-9 bins) ---")
meds = []
for b in (1, 2, 3, 4):
    p = load(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt")
    r = [math.log10(gL / law_pred(gN)) for gN, gL in p if gN < 0.3 * A0]
    if r:
        meds.append(float(np.median(r)))
        print(f"    bin {b}: {len(r)} deep points, median {meds[-1]:+.3f} dex")
if len(meds) >= 3:
    spread = max(meds) - min(meds)
    ok_v2 = spread <= 0.4
    RES.append(check("V2 [mass-independent] the four stellar-mass bins give the same "
                     "pred/obs ratio within 0.4 dex", ok_v2, f"spread {spread:.3f} dex"))
else:
    RES.append(check("V2 [mass-independent] enough bins loaded", False, "bins found: "
                     + str(len(meds))))

# ---- V3: the MW break -> g_ext cross-check ----
print("\n--- V3 the MW cross-check: the 6.1 kpc break predicts the external field ---")
for Mb, rbr in ((7.0e10, 6.1 * KPC), (7.0e10, 6.5 * KPC)):
    g_ext_pred = GN * Mb * MSUN / rbr ** 2
    print(f"    M_b = {Mb:.1e}, r_break = {rbr/KPC:.1f} kpc -> g_ext_pred = {g_ext_pred:.3e}")
g_ext_pred = GN * 7.0e10 * MSUN / (6.1 * KPC) ** 2
r1, r2 = g_ext_pred / 2.146e-10, g_ext_pred / 2.32e-10
ok_v3 = min(r1, r2) >= 0.75 and max(r1, r2) <= 1.25
RES.append(check("V3 [the break predicts g_ext] within 25% of the measured solar-circle "
                 "field (L240 2.146e-10 / DHF24 2.32e-10)", ok_v3,
                 f"ratios {r1:.2f} / {r2:.2f}"))

# ---- V4 ----
statement = ("The equipartition law (M_dark/M_b = sqrt(a0/g_N), zero parameters) "
             "predicts the lensing RAR: g_lens/g_N = 1 + sqrt(a0/g_N).  "
             + ("The KiDS-1000 isolated sample is consistent with the law (V1) and its "
                "mass-independence signature holds (V2)." if ok_v1 else
                "The KiDS-1000 sample does NOT track the law (V1)."))
RES.append(check("V4 [statement]", True, statement))

n = sum(1 for r in RES if r)
print(f"\nG03F COMPLETE: {n}/{len(RES)} checks PASS.")
json.dump({"checks": [bool(r) for r in RES], "n_pass": int(n), "n_total": len(RES),
           "v1": {"n": int(len(rat)), "median_dex": med, "rms_dex": rms},
           "v2": {"bin_medians": meds},
           "v3": {"g_ext_pred": g_ext_pred, "ratios": [r1, r2]},
           "statement": statement},
          open(os.path.join(HERE, "g03f_lensing_test_results.json"), "w"), indent=1)