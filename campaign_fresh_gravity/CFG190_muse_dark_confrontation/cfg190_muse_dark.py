#!/usr/bin/env python3
"""CFG190 -- MUSE-DARK II (bTFR at z ~ 1) against MUSE-DARK III (a0 rising with z): can one a0(z) law fit both?

Frozen criteria: FROZEN_CRITERIA.md in this directory (8f251a5a9).  ABSTRACT-LEVEL inputs (the data chat's notes), unverified against
the PDFs; no per-galaxy table read.
  III   a0(z) = a0(0) + a1 z, a0(0) = 1.0 +- 0.04, a1 = 1.59 +- 0.10 (1e-10); a0(0.87) = 2.38 +- 0.1  ->  log ratio vs a0(0).
  II    bTFR offset along the mass axis at fixed V, z ~ 1: 0.00 +- 0.06 dex (declared z = 1.0).
  map   P2 at fixed g_obs: g_bar^2 + g_bar a0 = g_obs^2 solved exactly; y = g_bar/a0 at II's 2 R_e bracketed: deep, 0.3, 1.0.
  laws  flat; a0 ~ E(z) (Omega_m 0.315); T = t(z)/t0; III's own linear law 1 + 1.59 z.
MUTATE=1: II's offset set to -0.38 dex (III's deep-regime implication): III's law must fit both, the headline must change.
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour any model, or that the theory is closed.
Run: python3 campaign_fresh_gravity/CFG190_muse_dark_confrontation/cfg190_muse_dark.py
"""
import os, sys, math, json
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
sys.path.insert(0, CFG)
import CFG7_common as C

MODE = os.environ.get("MUTATE", "").strip()
assert MODE in ("", "1")
R = C.Report("cfg190_muse_dark" + ("_MUTATE1" if MODE else ""), False)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())

OM = 0.315
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def tratio(z, om=OM):
    k = math.sqrt((1 - om) / om)
    return math.asinh(k * (1 + z) ** -1.5) / math.asinh(k)


A00, SA00, A1, SA1, A087, SA087, Z3 = 1.0, 0.04, 1.59, 0.10, 2.38, 0.10, 0.87
II_D, II_S, Z2 = (-0.38 if MODE == "1" else 0.00), 0.06, 1.0
LAWS = {"flat": lambda z: 1.0, "a0 ~ E(z)": E, "T = t(z)/t0": tratio, "III linear": lambda z: 1 + A1 / A00 * z}

# ================================================================== controls
R.banner("C1 / C2  CONTROLS")
check("C1 CONTROL: E(0.87), t(0.87)/t0 and III's linear law at 0.87",
      f"E = {E(0.87):.4f}; t/t0 = {tratio(0.87):.4f}; III: {A00 + A1 * 0.87:.3f} (abstract 2.38)", abs(A00 + A1 * 0.87 - 2.383) < 1e-3)


def dlogM(ratio, y):
    """log M_b shift at fixed g_obs when a0 -> ratio * a0 (P2, exact); y = g_bar/a0 at the reference (z = 0) a0; y = 0: deep limit"""
    if y == 0:
        return -math.log10(ratio)
    gobs2 = y * y + y                                           # in units of a0^2 at the reference
    a = ratio
    gb = (-a + math.sqrt(a * a + 4 * gobs2)) / 2                # g_bar^2 + g_bar a = g_obs^2
    return math.log10(gb / y)


sens = {y: (dlogM(1.001, y)) / math.log10(1.001) for y in (1e-9, 1.0)}
check("C2 CONTROL: the P2 fixed-g_obs inversion reproduces d ln g_bar / d ln a0 = -1/(2y + 1): -1 (deep), -1/3 (y = 1)",
      f"deep {sens[1e-9]:.4f}, y = 1: {sens[1.0]:.4f}", abs(sens[1e-9] + 1) < 1e-3 and abs(sens[1.0] + 1 / 3) < 1e-3)

# ================================================================== Q1
R.banner("Q1  EACH LAW AGAINST III (log a0(0.87)/a0(0)) AND II (bTFR offset along the mass axis at z = 1)")
lr3 = math.log10(A087 / A00)
s3 = math.sqrt((SA087 / A087) ** 2 + (SA00 / A00) ** 2) / math.log(10)
P(f"  III measured: log ratio {lr3:+.3f} +- {s3:.3f} dex;  II measured: {II_D:+.2f} +- {II_S:.2f} dex (z = {Z2})")
tab, fits = {}, {}
for name, f in LAWS.items():
    pr3 = math.log10(f(Z3)); pull3 = (pr3 - lr3) / s3
    row = dict(pred_III=pr3, pull_III=pull3)
    for y in (0, 0.3, 1.0):
        d2 = dlogM(f(Z2), y); pull2 = (d2 - II_D) / II_S
        row[f"pred_II_y{y}"] = d2; row[f"pull_II_y{y}"] = pull2
        fits[(name, y)] = abs(pull3) <= 2 and abs(pull2) <= 2
    tab[name] = row
    P(f"  {name:12s}: III {pr3:+.3f} (pull {pull3:+6.1f});  II deep {row['pred_II_y0']:+.3f} ({row['pull_II_y0']:+5.1f}), "
      f"y 0.3 {row['pred_II_y0.3']:+.3f} ({row['pull_II_y0.3']:+5.1f}), y 1 {row['pred_II_y1.0']:+.3f} ({row['pull_II_y1.0']:+5.1f});  "
      f"fits both: " + ", ".join(f"y{y}:{'YES' if fits[(name, y)] else 'no'}" for y in (0, 0.3, 1.0)))
R.num("table", tab)
both = [(n, y) for (n, y), ok in fits.items() if ok]
# the III-vs-II direct tension: III's own law carried to II
P(f"\n  III's own law carried to II: pull {tab['III linear']['pull_II_y0']:+.1f} (deep), {tab['III linear']['pull_II_y0.3']:+.1f} (y 0.3), "
  f"{tab['III linear']['pull_II_y1.0']:+.1f} (y 1)")

# ================================================================== Q2 / Q3
R.banner("Q2 CIRCULARITY (declared UNDECIDED without tables)  |  Q3 THE STANDING LINE")
P("  Q2: III fits M* inside the same DC14 disc-halo model as its halo, so its a_bar -- and the a0 fitted with a fixed interpolation")
P("      function -- can inherit the halo-profile prior; II uses photometric M* and scaling-relation gas. UNDECIDED without III's per-galaxy")
P("      fitted M* (vs photometric), a0 across the seven halo families, and baryon-only fits (requested through the data chat).")
if not both:
    summary = ("NO single a0(z) law fits both MUSE-DARK II and III at any declared y (|pull| <= 2 each): flat fits II "
               f"(pull {tab['flat']['pull_II_y0']:+.1f}) but not III ({tab['flat']['pull_III']:+.1f}); III's own linear law fits III but not II "
               f"({tab['III linear']['pull_II_y0']:+.1f} deep to {tab['III linear']['pull_II_y1.0']:+.1f} at y = 1); a0 ~ E(z) misses III "
               f"({tab['a0 ~ E(z)']['pull_III']:+.1f}). The two are mutually inconsistent under any common a0(z): a ROBUST rise is not "
               "established, and the June non-diagnostic (method-split) verdict stands, now within one collaboration")
else:
    summary = "Law(s) fitting both: " + ", ".join(f"{n} at y = {y}" for n, y in both) + (
        "; flat among them" if any(n == "flat" for n, _ in both) else "; flat NOT among them")
P(f"  Q3: {summary}")
if MODE == "1":
    check("MUTATE=1 [control]: with II's offset at -0.38, III's law fits both (at least deep) and the headline changes",
          summary, ("III linear", 0) in both)
else:
    check("H1 [HEADLINE, reported] the declared reading", summary, True, load_bearing=False)
R.num("summary", summary)
P(f"\n    SUMMARY (declared): {summary}")
nf = R.write(LANE)
raise SystemExit(1 if nf else 0)
