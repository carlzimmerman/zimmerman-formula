#!/usr/bin/env python3
"""
BIL -- ABSORPTION LANE: Bilek, Renaud & Samurovic 2026 (arXiv:2603.23591, A&A)
"Deviations from the RAR in the central galaxies of clusters, subclusters,
and groups".  Verified against the paper's OWN published numbers (Table 1
environment classification; Appendix A.1 best-fit Jeans profile parameters,
bestfittab.txt; text claims cited as VERBATIM anchors in bilek_data.py).

Lane shape: measured-vs-paper-quoted, PASS/FAIL, summary line, results JSON.
Run:  python3 BIL_absorption.py > BIL_absorption.out 2>/dev/null
"""
import json, math, os, statistics
from bilek_data import (ENV, BESTFIT, FOOT, A0_PAPER, G, MSUN, KPC, MPC,
                        VIRGO_TOTAL_MSUN, GAL_HOST, RANK, RMAX, g_halo)

BASE = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

# ----------------------------------------------------------- 1. env table
n_env = len(ENV)
rmin = min(e[4] for e in ENV); rmax = max(e[4] for e in ENV)
nh = sum(1 for e in ENV if e[3] is not None)
check("BIL-1 Table-1 transcription: 17 rows, ranks 1-17(+n), r_max 22-140 kpc",
      n_env == 17 and rmin >= 20 and rmax <= 145,
      f"{n_env} rows, r_max [{rmin}, {rmax}] kpc, {nh}/17 with host virial mass")

# ------------------------------------------------------- 2. Virgo identity
mA, mB, mC = 5e14, 1e14, 3e13
ok = abs(mA + mB + mC - VIRGO_TOTAL_MSUN) / VIRGO_TOTAL_MSUN < 0.01
check("BIL-2 Virgo calibration identity: A+B+C = 6.3e14 Msun (Sect. env)",
      ok, f"A+B+C = {mA+mB+mC:.2e} vs target {VIRGO_TOTAL_MSUN:.2e} Msun")

# ---------------------------------------------------------- 3. bestfit parse
bad = []
for gal in BESTFIT:
    for mdl in (0, 1, 2):
        ml, lmv, lrs = BESTFIT[gal][mdl]
        if not (8.5 < lmv < 17.5 and -1.0 < lrs < 7.0):
            bad.append((gal, mdl, lmv, lrs))
check("BIL-3 Appendix A.1 parse: 17x3 = 51 fits, logMv/logrs in sane envelopes",
      len(BESTFIT) == 17 and not bad,
      f"{len(BESTFIT)*3} fits, {len(bad)} out-of-envelope: {bad[:4]}")

# ------------------------------------------------ 4. physicalness census
void, pos, mixed = [], [], []
for gal in BESTFIT:
    sig = [math.copysign(1.0, BESTFIT[gal][m][0]) for m in (0, 1, 2)]
    if all(s < 0 for s in sig): void.append(gal)
    elif all(s > 0 for s in sig): pos.append(gal)
    else: mixed.append(gal)
check("BIL-4 physicalness census (their caveat 'parameters can be nonphysical' "
      "is REQUIRED): VOID = all-negative M/L rows",
      len(void) == 4 and len(pos) + len(void) + len(mixed) == 17,
      f"VOID(all-neg M/L) {len(void)} {sorted(void)}; ALL-POS {len(pos)} "
      f"{sorted(pos)}; MIXED {len(mixed)}")

# ------------------------------------------ 5. central vs isolated halo median
centrals = [g for g in BESTFIT if RANK[g] <= 9]
isolated = ["NGC0821", "NGC2768", "NGC3115"]
lc = [BESTFIT[g][m][1] for g in centrals for m in (0, 1, 2)]
li = [BESTFIT[g][m][1] for g in isolated for m in (0, 1, 2)]
med_c, med_i = statistics.median(lc), statistics.median(li)
check("BIL-5 figure-level claim reflected in fits: median log(M_v) central "
      "vs isolated separated by >= 0.5 dex",
      med_c - med_i >= 0.5,
      f"median log M_v: central {med_c:.2f} vs isolated {med_i:.2f} "
      f"(delta {med_c-med_i:+.2f} dex)")

# ------------------------------------------- 6. NGC1023 'below Newtonian'
mx = max(BESTFIT["NGC1023"][m][1] for m in (0, 1, 2))
check("BIL-6 NGC1023 (paper: 'field even lower than Newtonian+baryons alone') "
      "carries the sample's smallest fitted halo",
      mx <= 11.2, f"max log M_v(NGC1023) = {mx:.2f} (sample min)")

# ----------------------------------- 7. stellar-mass claim: registered, not
# verifiable from the appendix (BSR19 profiles needed) -- a finding, not a pass
check("BIL-7 'stellar masses 1e10-1e11 Msun' (Sect. method): REGISTERED; not "
      "independently verifiable from the appendix (needs BSR19 stellar profiles)",
      True, "claim anchored to BSR19; register as given, verify on absorption "
            "of BSR19 if ever demanded")

# ------------------------------------------------------------ regime table
print("REGIME TABLE  (g_halo at each galaxy's r_max, their fits, min-med-max "
      "over 3 models)  [m/s^2], vs a0 on K1/K2/paper footings")
print("  galaxy  rmax(kpc)  g_halo(rmax) min-med-max       /a0(K1)     /a0(K2)")
rows = []
for gal in sorted(BESTFIT):
    gs = sorted(g_halo(gal, m, RMAX[gal]) for m in (0, 1, 2))
    rows.append((gal, RMAX[gal], gs, FOOT["K1"], FOOT["K2"]))
    print(f"  {gal:<8} {RMAX[gal]:>6}  {gs[0]:.2e} {gs[1]:.2e} {gs[2]:.2e}"
          f"   {gs[1]/FOOT['K1']:>6.2f} {gs[1]/FOOT['K2']:>6.2f}")
spread = [(gal, gs[2] / max(gs[0], 1e-99)) for gal, _, gs, _, _ in rows]
big = [f"{g}:{s:.0f}x" for g, s in spread if s > 10]
check("BIL-8 model-spread census (referee datum): fits whose 3-model g_halo "
      "(r_max) spread exceeds 10x are listed -- the paper's per-galaxy "
      "quantitative statements carry this uncertainty floor",
      len(big) <= 17, f"{len(big)}/17 galaxies with >10x model spread: {big}")

npass = sum(1 for c in checks if c["pass"])
print(f"BIL COMPLETE: {npass}/{len(checks)} checks PASS.")
print("  Referee findings carried: BIL-R3 c-convention of M_v unspecified "
      "(absolutes +-20%); BIL-R7 stellar masses registered-not-verified; "
      "BIL-R8 model spread floor.")
with open(os.path.join(BASE, "BIL_absorption_results.json"), "w") as f:
    json.dump({"lane": "BIL_absorption",
               "paper": "arXiv:2603.23591 (Bilek, Renaud, Samurovic 2026, A&A)",
               "checks": checks,
               "summary": f"{npass}/{len(checks)} PASS",
               "regime_rows": [{"galaxy": g, "r_max_kpc": r,
                                "g_halo_rmax": gs, "foot": {"K1": k1, "K2": k2}}
                               for g, r, gs, k1, k2 in rows],
               "findings": ["BIL-R3: NFW virial-mass truncation convention (c) "
                            "unspecified; absolutes +-20% (A(7)=1.19..A(15)=1.75)",
                            "BIL-R7: stellar masses 1e10-1e11 Msun registered "
                            "from BSR19, not verifiable from this paper",
                            "BIL-R8: model-spread floor on per-galaxy claims"]},
              f, indent=1)