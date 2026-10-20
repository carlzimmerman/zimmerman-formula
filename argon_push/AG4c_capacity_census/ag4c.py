#!/usr/bin/env python3
"""AG4c: tether-capacity census. n=2 caps the tethered phantom field at g_ph < a0/2 (107 Msun/pc^2 in AG4's convention), n=1 at
g_ph < a0 (214).  Class C1 = SPARC points with g_bar >= 2 a0, Upsilon from stellar populations (0.50 / 0.70 at 3.6 um, 0.10 dex),
distance/inclination/velocity errors from SPARC; g_ph = g_obs - g_bar with linear error propagation.
Criteria: FROZEN_CRITERIA.md (committed alone, before this script).  Run: OMP_NUM_THREADS=1 nice -n 10 python3 ag4c.py
AG4C_MUTATE=1 injects g_obs = g_bar + 0.9 a0 with errors shrunk x10: it must return EXCLUDES n=2 (exit 1 = bites).
kappa = 1/2 fitted; footings never pooled; not theory closed."""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LANES = os.path.join(REPO, "campaign_fresh_gravity"); sys.path.insert(0, LANES)
import CFG4_common as C

MUT = os.environ.get("AG4C_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag4c{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n"); OUT.flush()
FAILS = []
def check(name, ok, detail=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else "")); (None if ok else FAILS.append(name)); return ok

LN10 = math.log(10.0); KPC_S = 3.0857e19; SIG_U = 0.10; WELL = 0.15
P("AG4c: tether-capacity census (n=2 cap a0/2, n=1 cap a0) on SPARC points with g_bar >= 2 a0" + ("   *** MUTATE: injected cap-violating phantom ***" if MUT else ""))
P("kappa = 1/2 fitted; footings never pooled; not theory closed.")

# ------------------------------------------------------------------------------------------------ controls
P("\nControls")
def u_of(gb, n):            # rest-state phantom field of the capacity family: u^2 + n gb u = gb (a0 = 1 units)
    return (-n * gb + np.sqrt((n * gb) ** 2 + 4 * gb)) / 2
gb = np.logspace(-3, 6, 901); ok1 = True
for n in (1, 2):
    u = u_of(gb, n); ok1 &= bool(np.all(u < 1.0 / n)) and abs(u[-1] - 1.0 / n) < 1e-5 * (1.0 / n) * 100
check("K1 u < a0/n everywhere and u -> a0/n (n = 1, 2)", ok1, f"u(1e6 a0): n=1 {u_of(np.array(1e6), 1):.6f}, n=2 {u_of(np.array(1e6), 2):.6f}")
P(f"  (reported) at g_bar = 5 a0: u = {u_of(np.array(5.0), 1):.3f} a0 (n=1), {u_of(np.array(5.0), 2):.3f} a0 (n=2)")
SIG_CAP = {f: C.A0[f] / (math.pi * C.G_SI) / (C.MSUN / C.PC ** 2) for f in C.FOOTS}
check("K2 Sigma cap a0/(pi G) = 213.7 and half 106.9 Msun/pc^2 (canonical)", abs(SIG_CAP["canonical"] - 213.7) < 0.1 and abs(SIG_CAP["canonical"] / 2 - 106.9) < 0.1,
      f"{SIG_CAP['canonical']:.2f} / {SIG_CAP['canonical'] / 2:.2f}; alt {SIG_CAP['alt']:.1f} / {SIG_CAP['alt'] / 2:.1f}")

# ------------------------------------------------------------------------------------------------ census
GAL = C.load_sparc(); RES = {"lane": "AG4c", "mutate": MUT, "criteria": "FROZEN_CRITERIA.md", "Sigma_cap": SIG_CAP, "footings": {}}
for f in C.FOOTS:
    a0 = C.A0[f]; rows = []
    for g in GAL:
        meta = g.get("meta")
        if not meta:
            continue
        R, Vo, eV, Vg, Vd, Vb = (np.asarray(g[k], float) for k in ("R", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"))
        Rm = R * KPC_S
        gstar = (0.5 * Vd ** 2 + 0.7 * Vb ** 2) * 1e6 / Rm; ggas = np.sign(Vg) * Vg ** 2 * 1e6 / Rm
        gbar = gstar + ggas; gobs = (Vo * 1e3) ** 2 / Rm
        inc = math.radians(meta["Inc"]); einc = math.radians(meta["eInc"])
        sig = np.sqrt((LN10 * SIG_U * gstar) ** 2 + (gobs * 2 * np.clip(eV, 0, None) / np.clip(Vo, 1, None)) ** 2
                      + (gobs * meta["eD"] / meta["D"]) ** 2 + (gobs * 2 * einc / math.tan(max(inc, 0.05))) ** 2)
        if MUT:
            gobs = gbar + 0.9 * a0; sig = sig / 10.0
        m = (Vo > 0) & (gbar >= 2 * a0) & np.isfinite(sig)
        for j in np.where(m)[0]:
            rows.append(dict(gal=g["name"], Q=meta["Q"], gbar=float(gbar[j] / a0), gph=float((gobs[j] - gbar[j]) / a0), sig=float(sig[j] / a0)))
    sigs = np.array([r["sig"] for r in rows]) if rows else np.array([np.nan])
    well = [r for r in rows if r["sig"] <= WELL]
    P(f"\n=== footing: {f} (a0 = {a0:.4e}) ===")
    P(f"  PRE-FLIGHT: {len(rows)} points in {len({r['gal'] for r in rows})} galaxies at g_bar >= 2 a0; median sigma(g_ph) = {np.nanmedian(sigs):.2f} a0 "
      f"(10th pct {np.nanpercentile(sigs, 10):.2f}); well-measured (sigma <= {WELL} a0): {len(well)} points in {len({r['gal'] for r in well})} galaxies")
    ex2 = [r for r in well if r["Q"] <= 2 and r["gph"] - 2 * r["sig"] > 0.5]
    ex1 = [r for r in well if r["Q"] <= 2 and r["gph"] - 2 * r["sig"] > 1.0]
    rd = "NOT DIAGNOSTIC" if not well else ("EXCLUDES n=2" if ex2 else "CONSISTENT")
    if well:
        gp = np.array([r["gph"] for r in well]); P(f"  well-measured g_ph/a0: median {np.median(gp):+.2f}, max {gp.max():+.2f}; above a0/2 at 2 sigma: {len(ex2)}; above a0 at 2 sigma: {len(ex1)}")
    P(f"  READING ({f}): {rd}" + (f"; n=1 also excluded by {len(ex1)} points" if ex1 else ""))
    RES["footings"][f] = dict(n_points=len(rows), n_gal=len({r['gal'] for r in rows}), median_sigma=float(np.nanmedian(sigs)), n_well=len(well),
                              n_well_gal=len({r['gal'] for r in well}), n_exceed_half=len(ex2), n_exceed_full=len(ex1), reading=rd,
                              n2_survives_AG4c=rd != "EXCLUDES n=2", exceed_half=ex2[:20])
surv = all(RES["footings"][f]["n2_survives_AG4c"] for f in C.FOOTS); RES["n2_survives_AG4c"] = surv
P(f"\nAG4c: " + "; ".join(f"{f} {RES['footings'][f]['reading']}" for f in C.FOOTS) + f".  n=2 survives AG4c: {surv}")
if not MUT and all(RES["footings"][f]["reading"] == "NOT DIAGNOSTIC" for f in C.FOOTS):
    P("  Data that could decide (not pulled here): late-type strong lenses with kinematic mass-to-light ratios (bulge/disc decomposition from\n"
      "  lensing + stellar kinematics), or any tethered system whose baryonic mass at g_bar >> a0 is known to <~5% without stellar-population M/L.")
bites = MUT and all(RES["footings"][f]["reading"] == "EXCLUDES n=2" for f in C.FOOTS)
if MUT:
    P(f"MUTATE: {'control BITES (exit 1, as designed)' if bites else 'control DID NOT BITE (recorded)'}")
P(f"controls failed: {FAILS or 'none'}")
json.dump(RES, open(os.path.join(HERE, f"ag4c_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(1 if bites or FAILS else 0)
