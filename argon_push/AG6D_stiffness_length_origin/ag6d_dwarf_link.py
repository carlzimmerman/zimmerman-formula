#!/usr/bin/env python3
"""AG6D Part C2: one universal clump radius R_TF = pi L*/sqrt2 (Part A, free self-gravitating cold energy, class-A hybrid)
against the record's dwarf requirements. FROZEN_CRITERIA.md section 5 (b94d6b89b). Numbers copied from lane READMEs:
  CFG870 r_c = 104 pc (shape M ~ r^3/(r^2 + r_c^2)), rho0 ~ 0.58 Msun/pc^3; CFG871 UFD best r_c 133 / 139 pc (canonical / alt);
  CFG877 cap radius 237 / 205 pc (CFG884 inputs); CFG884 synthesis: Sextans MP needs >~ 6e8 Msun out to >~ 1.7 kpc (PROVISIONAL).
Classes: CONSISTENT (all implied L* in window and max/min <= 2); INCONSISTENT (Sextans lower bound > x2 the largest group
value); else TENSION. Supply check (reported): M_TF = 4 R^3 rho0 / pi vs catchment stock 53.64 M_b, M_b = 1e5..1e7 Msun.
MUTATE (AG6D_MUTATE=1): Sextans' required R set equal to the CFG870-implied R -> class must become CONSISTENT; exit 1.
"""
import json, os, sys
import numpy as np
from scipy.optimize import brentq

MUT = os.environ.get("AG6D_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
out_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out_lines.append(s)


WIN = {"canonical": (24.0, 1000.0), "alt": (24.7, 1000.0)}
xh = brentq(lambda x: (x * x + 3) / (x * x + 1)**2 - 1.5, 0.1, 2.0)      # CFG870 shape half-central-density, r/r_c
sh = brentq(lambda s: np.sin(np.pi * s) / (np.pi * s) - 0.5, 0.1, 0.99)  # n=1 sinc half-density, r/R
k = np.sqrt(2) / np.pi                                                  # L* = (sqrt2/pi) R_TF
P(f"mapping: CFG870 half-density at r = {xh:.5f} r_c; sinc half-density at r = {sh:.5f} R; L* = {k:.5f} R_TF")
rho0 = 0.58
res = {"lane": "AG6D", "part": "C2", "mutate": MUT, "x_half": xh, "s_half": sh}
cls_all = {}
for foot, (rc871, rcap) in {"canonical": (133.0, 237.0), "alt": (139.0, 205.0)}.items():
    R870 = xh * 104.0 / sh
    vals = {
        "CFG870 r_c 104 pc": k * R870,
        f"CFG871 UFD r_c {rc871:.0f} pc": k * xh * rc871 / sh,
        f"CFG877 cap {rcap:.0f} pc as R_TF": k * rcap,
    }
    R_sex = R870 if MUT else 1700.0
    L_sex_lo = k * R_sex
    grp = list(vals.values())
    lo, hi = WIN[foot]
    in_win = all(lo <= v <= hi for v in grp) and (L_sex_lo <= hi)
    ratio_grp = max(grp) / min(grp)
    ratio_sex = L_sex_lo / max(grp)
    if ratio_sex > 2.0:
        cls = "INCONSISTENT"
    elif in_win and max(grp + [L_sex_lo]) / min(grp + [L_sex_lo]) <= 2.0:
        cls = "CONSISTENT"
    else:
        cls = "TENSION"
    P(f"\n=== {foot} ===")
    for kname, v in vals.items():
        P(f"  {kname:28s} -> L* = {v:7.1f} pc   (R_TF = {v/k:7.1f} pc)  {'in window' if lo <= v <= hi else 'OUTSIDE'}")
    P(f"  {'CFG884 Sextans MP (R >= %.0f pc)' % R_sex:28s} -> L* >= {L_sex_lo:7.1f} pc")
    P(f"  group max/min = {ratio_grp:.2f}; Sextans bound / group max = {ratio_sex:.2f}  -> CLASS {cls}")
    # supply check
    sup = {}
    for name, R in (("group R (CFG870)", R870), ("Sextans R", 1700.0)):
        M = 4 * R**3 * rho0 / np.pi
        need = {f"{mb:.0e}": 53.64 * mb for mb in (1e5, 1e6, 1e7)}
        sup[name] = {"R_pc": R, "M_TF_Msun": M, "stock": need, "exceeds_stock_for": [kk for kk, s in need.items() if M > s]}
        P(f"  supply: {name:16s} R = {R:6.0f} pc, M_TF = {M:.2e} Msun at rho0 = {rho0}; exceeds 53.64 M_b for M_b = "
          f"{sup[name]['exceeds_stock_for']}")
    res[foot] = {"implied_Lstar_pc": vals, "Sextans_Lstar_lower_pc": L_sex_lo, "group_ratio": ratio_grp,
                 "sextans_over_group": ratio_sex, "class": cls, "supply": sup}
    cls_all[foot] = cls
res["class"] = cls_all
P(f"\nCLASS C2: canonical {cls_all['canonical']}, alt {cls_all['alt']}" + ("  [MUTATE: planted consistency]" if MUT else ""))
with open(os.path.join(HERE, f"ag6d_dwarf_link_results{TAG}.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)
with open(os.path.join(HERE, f"ag6d_dwarf_link{TAG}.out"), "w") as fh:
    fh.write("\n".join(out_lines) + "\n")
sys.exit(1 if MUT else 0)
