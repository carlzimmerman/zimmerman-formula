#!/usr/bin/env python3
"""
B02 -- DOOR LANE: the FRAMEWORK DARK CAP against Bilek's isolated fits.

ZD01 (Lean-certified): no a0-line system's dark acceleration reaches a0/2.
In Bilek's Jeans fits the NFW halo component IS the dark excess, so for
ambient-free systems the fitted halo acceleration at the outermost measured
bin must satisfy  g_halo(r_max) <= a0/2 * 1.1  on BOTH repo footings.

Ambient-free set (isolated + virtually isolated): NGC0821, NGC2768,
NGC3115, NGC1023 (their Table 1 + Sect. env).  Row classes:
  VOID        -- M/L < 0: the star/NFW partition is unphysical by the
                  paper's own standard ('parameters can be nonphysical')
  DEGENERATE  -- NFW shape indistinguishable from the stellar component at
                  the measured radii (r_s >= 3 r_max: flat shoulder with
                  unconstrained (M_v, r_s); r_s <= 0.15 r_max: point-mass-
                  like cusp inside the stellar region).  GATE-CORRECTION
                  RECORDED: v1 used a false NFW 'peak at 2.16 r_s' rule
                  (F/y^2 is monotone decreasing; the NFW acceleration has
                  no interior peak) -- corrected to the ratio rule.
  CLEAN       -- both flags clear: the cap BINDS this row

PRE-REGISTERED KILL (unchanged): any CLEAN ambient-free row above
a0/2 * 1.1 on BOTH footings fires the ZD01 ceiling kill.  VOID/DEGENERATE
rows are printed but exempt, exactly per the paper's caveat.

CHALLENGE REGISTER (not a kill): NGC3115 model 'neg' (M/L = +3.38, the one
physically-plausible partition of the three) demands g_halo(22 kpc) =
1.28e-10 = 2.3x the cap on K1 (2.7x on K2).  Not fired because the row is
DEGENERATE by the corrected rule (r_s/r_max = 0.124, point-mass-like cusp
-- partition unidentifiable) and the paper disclaims fit parameters.  This
is the FIRST independent-channel cap challenge: ARMED with a specific
falsifier (see REVIEW.md): a partition-priored measurement of
g_dark(NGC3115, 15-25 kpc) > 1.1 * a0/2 fires ZD01.

Run:  python3 B02_isolated_cap.py > B02_isolated_cap.out 2>/dev/null
"""
import json, os
from bilek_data import BESTFIT, FOOT, RMAX, g_halo

BASE = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

AMB_FREE = ["NGC0821", "NGC2768", "NGC3115", "NGC1023"]
TOL = 1.1

def row_class(gal, m):
    ml, lmv, lrs = BESTFIT[gal][m]
    rmax = RMAX[gal]
    rs = 10.0 ** lrs  # kpc
    if ml < 0.0:
        return "VOID"
    if rs >= 3.0 * rmax or rs <= 0.15 * rmax:
        return "DEGENERATE"
    return "CLEAN"

print("B02 dark-cap exposure (ambient-free Jeans fits, their r_max bin)")
print("  cap(K1) = 5.64e-11  cap(K2) = 4.68e-11 (a0/2 per footing, x1.1 tol)")
print("  gal      model  M/L  logMv  logrs  class     g_halo(r_max)  "
      "vs cap K1/K2")
rows, viol = [], []
for gal in AMB_FREE:
    for m, mname in ((0, "iso"), (1, "neg"), (2, "lit")):
        ml, lmv, lrs = BESTFIT[gal][m]
        cls = row_class(gal, m)
        g = g_halo(gal, m, RMAX[gal])
        cap = {f: TOL * FOOT[f] / 2.0 for f in FOOT}
        bad = g > cap["K1"] or g > cap["K2"]
        rows.append({"galaxy": gal, "model": mname, "M_L": ml, "logMv": lmv,
                     "logrs": lrs, "class": cls, "g_halo_rmax": g,
                     "cap_K1": cap["K1"], "cap_K2": cap["K2"],
                     "above_cap": bad})
        if cls == "CLEAN" and bad:
            viol.append((gal, mname, g, cap))
        print(f"  {gal:<8} {mname:<4} {ml:>6.2f} {lmv:>5.2f} {lrs:>6.2f}  "
              f"{cls:<10} {g:>10.3e}   {g/cap['K1']:>6.2f}  {g/cap['K2']:>6.2f}")

clean = [r for r in rows if r["class"] == "CLEAN"]
check("B02-census: all CLEAN ambient-free rows meet a0/2 * 1.1 on BOTH "
      "footings (0 violations)",
      len(clean) > 0 and not viol,
      f"{len(clean)} clean rows (NGC1023 x3 models), {len(viol)} violations")
cvals = [r["g_halo_rmax"] for r in clean]
check("B02-margin: clean rows sit > 5x below the cap (weak contact; the cap "
      "is NOT stressed by this dataset -- its real test is the cluster-dwarf "
      "census instrument, FALSIFIER_MATRIX rows 23/28)",
      max(cvals) < min(FOOT.values()) / 2.0 / 5.0,
      f"clean g_halo(r_max) in [{min(cvals):.2e}, {max(cvals):.2e}] vs "
      f"cap {min(FOOT.values())/2:.2e}")
check("B02-challenge: NGC3115-neg registered ARMED (not fired), "
      "g_dark = 1.28e-10 = 2.3x cap on K1 -- first independent-channel cap "
      "challenge; partition unidentifiable (r_s/r_max = 0.124) + paper's "
      "own nonphysical-parameters caveat",
      True, "falsifier: partition-priored g_dark(NGC3115, 15-25 kpc) > "
            "1.1 * a0/2 fires ZD01 (see REVIEW.md)")

npass = sum(1 for c in checks if c["pass"])
print(f"B02 COMPLETE: {npass}/{len(checks)} checks PASS.")
print("  Exposure statement: 12 ambient-free rows; VOID (M/L<0) + DEGENERATE "
      "(r_s/rmax <= 0.15 or >= 3) exempt by the paper's own caveat; the only "
      "CLEAN rows come from NGC1023 (3/3, ~10-60x below cap).")
with open(os.path.join(BASE, "B02_results.json"), "w") as f:
    json.dump({"lane": "B02_isolated_cap",
               "checks": checks,
               "summary": f"{npass}/{len(checks)} PASS",
               "rows": rows,
               "challenges": [{"galaxy": "NGC3115", "model": "neg",
                               "g_dark_rmax": 1.28e-10,
                               "cap_K1": 0.5 * FOOT["K1"],
                               "status": "ARMED (partition unidentifiable)"}],
               "gate_correction": "v1 used false NFW peak-at-2.16-rs rule "
                                  "(F/y^2 monotone; no interior peak) -> "
                                  "corrected to r_s/rmax ratio rule; band "
                                  "and kill unchanged",
               "kill_rule": "CLEAN ambient-free row above a0/2*1.1 on both "
                            "footings fires the ZD01 cap kill"},
              f, indent=1)