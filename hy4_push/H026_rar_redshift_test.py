#!/usr/bin/env python3
r"""H026 -- THE PRE-REGISTERED TEST: does the RAR weaken with redshift?

Run against H025's frozen thresholds. Nothing here was chosen after seeing a
result: the method, bins and thresholds are those pre-registration.

  PREDICTION (H024):  sigma(z) = sigma_0 * s(0)/s(z),  sigma_0 = 0.064 dex
  PASS:  high-z scatter >= 1.5x the local floor, monotone in z across >= 3
         bins, and sigma(z)/sigma_0 matches s(0)/s(z) within a factor 2.
  FAIL:  high-z scatter <= 1.2x the local floor in EVERY bin.
  INSTRUMENT-FAIL: <10 galaxies in any bin, or no per-galaxy baryons.

DATA: MSA-3D (30 galaxies, z = 0.6-1.2) with Re_disk_kpc, logMstar, Vrot_Re,
fDM_Re -- everything needed for a genuine per-galaxy RAR residual.
"""
import math, csv, os, json
import numpy as np

RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, d=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "pass": ok})
    if ok: NP_ += 1
    else:  NF_ += 1
    return ok

G, c = 6.67430e-11, 2.99792458e8
H0  = 67.4e3/3.0856775814913673e22
OmL = 0.685
MSUN= 1.98892e30
PC  = 3.0856775814913673e16
kpc = 1000.0*PC
FOOT = {"canonical": 9.3619e-11, "alternative": 1.1279e-10}
rho_c = 3.0*H0**2/(8.0*math.pi*G)

print("="*74)
print("H026 -- THE PRE-REGISTERED TEST: THE RAR vs REDSHIFT")
print("="*74)

# ---------------------------------------------------------------- step 4: data
MSA = ("/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/"
       "data/msa3d_2026_rotation_curves.csv")
rows = []
with open(MSA) as f:
    for r in csv.DictReader(f):
        try:
            z   = float(r["z"])
            mst = float(r["logMstar"])          # log10(Mstar/Msun)
            Re  = float(r["Re_disk_kpc"])       # kpc
            vrot= float(r["Vrot_Re"])           # km/s
            if z > 0 and Re > 0 and vrot > 0:
                rows.append({"z":z, "logM":mst, "Re":Re, "V":vrot})
        except (ValueError, TypeError, KeyError):
            continue
print(f"\n  MSA-3D: {len(rows)} galaxies with z, Mstar, Re, Vrot")
zs = np.array([r["z"] for r in rows])
print(f"  z range: {zs.min():.3f} - {zs.max():.3f}")

# ---------------------------------------------------------------- the RAR residual
def mu2(u): return 1.0 - 1.0/(1.0 + u)**2
def solve_g(gbar, a0):
    if gbar <= 0: return 0.0
    lo, hi = 0.0, max(10.0*gbar, 10.0*a0)
    for _ in range(120):
        mid = 0.5*(lo+hi)
        if mu2(mid/(2.0*a0))*mid < gbar: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)

def residual(a0):
    """per-galaxy RAR residual in dex, using the ZERO-PARAMETER theory curve"""
    out = []
    for r in rows:
        Mb = (10.0**r["logM"])*MSUN
        Rm = r["Re"]*kpc
        # baryonic acceleration at Re (spherical estimate from the disc mass)
        gbar = G*Mb/Rm**2
        # observed acceleration from the rotation velocity
        gobs = (r["V"]*1e3)**2/Rm
        # theory prediction (zero parameters: a0 from Lambda)
        gth  = solve_g(gbar, a0)
        out.append(math.log10(gobs) - math.log10(gth))
    return np.array(out)

# ---------------------------------------------------------------- binning
# Pre-registration: >= 3 bins, >= 10 galaxies each. 30 galaxies -> 3 bins of 10.
order = np.argsort(zs)
n = len(rows)
nb = 3
bins = [order[i*n//nb:(i+1)*n//nb] for i in range(nb)]

print(f"\n  bins (pre-registered: {nb} bins of {n//nb}):")
results = {}
for name, a0 in FOOT.items():
    res = residual(a0)
    sig = []
    print(f"\n  --- {name} footing (a_0 = {a0:.4e}) ---")
    print(f"      {'bin':>4s} {'z median':>9s} {'N':>4s} {'rms [dex]':>10s}")
    for i, b in enumerate(bins):
        s = float(np.sqrt(np.mean(res[b]**2)))
        sig.append(s)
        print(f"      {i+1:4d} {np.median(zs[b]):9.3f} {len(b):4d} {s:10.4f}")
    results[name] = sig

# ---------------------------------------------------------------- step 1: anchor
SIG0 = 0.064   # G013 registered local floor, frozen in H025
print(f"\n  local anchor (G013, frozen): sigma_0 = {SIG0} dex")

# ---------------------------------------------------------------- verdict
def share(z):
    gz = 1.7*(1.0+z)**1.5
    ph = 1.0/gz
    free_b = 5.408 - 1.0
    return ph/(ph + free_b)

print(f"\n  predicted vs measured (canonical):")
print(f"      {'bin':>4s} {'z':>7s} {'predicted':>10s} {'measured':>9s} {'ratio':>7s}")
pred_all, meas_all = [], []
for i, b in enumerate(bins):
    zm = float(np.median(zs[b]))
    s0 = share(0.0); sz = share(zm)
    pred = SIG0*s0/sz
    meas = results["canonical"][i]
    pred_all.append(pred); meas_all.append(meas)
    print(f"      {i+1:4d} {zm:7.3f} {pred:10.4f} {meas:9.4f} {meas/pred:7.3f}")

# Apply the frozen thresholds
meas = np.array(meas_all); pred = np.array(pred_all)
floor_ratio = meas/SIG0
monotone = all(meas[i] < meas[i+1] for i in range(len(meas)-1))
within2  = all(0.5 <= meas[i]/pred[i] <= 2.0 for i in range(len(meas)))

check("V1 [PASS CONDITION 1] high-z scatter >= 1.5x the local floor",
      "  ".join(f"bin{i+1}: {floor_ratio[i]:.2f}x" for i in range(len(floor_ratio))),
      all(r >= 1.5 for r in floor_ratio),
      "Threshold frozen in H025 at 1.5x.")
check("V2 [PASS CONDITION 2] the increase is monotone in z across >= 3 bins",
      f"scatter by bin: " + " -> ".join(f"{m:.4f}" for m in meas)
      + f";  monotone = {monotone}",
      monotone and len(meas) >= 3,
      "Threshold frozen in H025.")
check("V3 [PASS CONDITION 3] measured/predicted within a factor 2 at every bin",
      "  ".join(f"bin{i+1}: {meas[i]/pred[i]:.3f}" for i in range(len(meas))),
      within2,
      "Threshold frozen in H025.")
kill = all(r <= 1.2 for r in floor_ratio)
check("V4 [THE KILL] high-z scatter <= 1.2x the local floor in EVERY bin",
      "  ".join(f"bin{i+1}: {floor_ratio[i]:.2f}x" for i in range(len(floor_ratio))),
      not kill,
      "If this were true the evolving-partition prediction would be dead.")

verdict = "PASS" if (all(r >= 1.5 for r in floor_ratio) and monotone and within2) \
          else ("FAIL (kill)" if kill else "NOT ESTABLISHED")
print(f"\n  PRE-REGISTERED VERDICT: {verdict}")

print("\n" + "="*74)
print(f"H026 READING:  {NP_} PASS / {NF_} FAIL")
print("="*74)
print(f"""
VERDICT: {verdict}

The thresholds were frozen in H025 before this run. Honest reading: the MSA-3D
sample spans z = 0.6-1.2, which is only a factor ~1.4 in predicted scatter
(0.12 -> 0.17 dex) -- barely above the 1.5x floor threshold. So this dataset
was always going to be marginal, and H025 said so in advance.

The scatter measured here is the residual against the ZERO-PARAMETER theory
curve (mu_2 with a_0 from Lambda), which at high z includes whatever
astrophysical noise the sample carries. A large measured scatter is therefore
NOT by itself evidence for the prediction -- it is equally consistent with
sample noise, evolution in the baryon-halo connection, or measurement error.

WHAT WOULD SETTLE IT: a high-z sample spanning a wider baseline (z ~ 0 to 2)
with per-galaxy baryons, so the predicted factor ~5 in scatter can be seen
against the noise. This pre-registration is written so that when such a sample
arrives the thresholds are already fixed and cannot be moved.
""")

json.dump({"lane":"H026","pass":NP_,"fail":NF_,"results":RES,
           "verdict":verdict,
           "floor_ratios":[float(r) for r in floor_ratio],
           "measured_scatter":[float(m) for m in meas],
           "predicted_scatter":[float(p) for p in pred],
           "N":len(rows), "z_range":[float(zs.min()), float(zs.max())]},
          open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/H026_results.json","w"),
          indent=2)
print(json.dumps({"pass":NP_,"fail":NF_}))
