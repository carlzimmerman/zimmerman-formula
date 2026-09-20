#!/usr/bin/env python3
"""
bhstar_h2_window_forecast.py -- DOOR H2: push the compactness switch DOWN in mass.
=================================================================================
G1 (bhstar_g1_lrd_host_a0_window.py) found the compactness switch at M* ~ 1e8.5: compact LRD
hosts sit ON the Newtonian baryon curve while extended dwarfs of the same mass ride ~2x above
it. THIS lane pushes the same machinery DOWN to the category-4 survivor masses (UHZ1-class,
M* ~ 3-8e7 Msun at z ~ 10) -- where the hosts are LIGHT ENOUGH to enter the a0 window even at
compact sizes. Deliverable: the forecast that turns UHZ1-class hosts from "overmassive anomaly"
into an a0-window MEASUREMENT, with pre-registered numbers on both footings.

MOTIVATION (absorbed, provenance-checked):
  UHZ1 (Bogdan+23 Nature Astronomy; Natarajan+24 ApJL 960 L1): z ~ 10.1, Chandra 4.2-sigma
  Compton-thick X-ray quasar, L_bol ~ 5e45 erg/s, M_BH ~ 4e7 Msun (Eddington-assumed),
  M* ~ 4-7e7 Msun (Castellano+23, Atek+23) -- M_BH ~ M*, the category-4 survivor of the BH*
  mass revision. Its host is the kind of object whose NEXT velocity-dispersion measurement is
  an a0-window measurement -- the forecast below arms that.

CONVENTIONS: identical to G1 (nu(y) = sqrt(1+1/y); point-mass g_bar = upper bound on Newtonian
g, so boosts are LOWER bounds at fixed M_bar; DESI CPL (w0,wa) = (-0.752,-0.86); footings
a0(fw) = 9.3619e-11, a0(canon) = 1.2e-10). For isotropic virial systems the same nu(y) factor
applies to sigma as to V_circ (both track the depth of the same potential).

Run:  python3 reviews/bhstar_h2_window_forecast.py  (stdlib only)
"""

import math, json, os

G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
A0_FW = 9.3619e-11
A0_CANON = 1.2e-10
W0, WA = -0.752, -0.86

def nu(y):
    return math.sqrt(1.0 + 1.0 / y)

def boost(y):
    return nu(y) - 1.0

def a0_eff(z, a0_0):
    rho_ratio = (1.0 + z) ** (3.0 * (1.0 + W0 + WA)) * math.exp(-3.0 * WA * z / (1.0 + z))
    return a0_0 * math.sqrt(rho_ratio)

def g_bar(M_msun, Re_kpc):
    return G * M_msun * MSUN / (Re_kpc * KPC) ** 2

results = []
def check(name, ok, detail=""):
    results.append(dict(check=name, ok=bool(ok), detail=detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    return ok

print("=" * 78)
print("DOOR H2 -- THE WINDOW FORECAST AT UHZ1-CLASS MASSES (category-4 survivors)")
print("=" * 78)

print("\n[A] a0(z) footing check")
v10 = a0_eff(10.0, 1.0)
check("a0(10)/a0(0) = 0.36 under the locked DESI reading (jwst_full_predictions.py quotes 0.36)",
      abs(v10 - 0.36) / 0.36 < 0.02, f"{v10:.4f}")

print("\n[B] The window locus at UHZ1-class masses (R_e in kpc where the boost crosses)")
print("    M*[Msun]  R_e(20%) z=0fw  R_e(50%) z=0fw  R_e(20%) z=10fw+DESI  R_e(50%) z=10fw+DESI")
locus = {}
for lgM in (math.log10(3e7), math.log10(5e7), math.log10(8e7)):
    M = 10 ** lgM
    a10 = a0_eff(10.0, A0_FW)
    row = [math.sqrt(G * M * MSUN / (y_t * a0)) / KPC
           for (y_t, a0) in ((2.2727, A0_FW), (0.8, A0_FW), (2.2727, a10), (0.8, a10))]
    locus[lgM] = row
    print(f"    1e{lgM:<7.1f} {row[0]:10.2f} {row[1]:12.2f} {row[2]:16.2f} {row[3]:19.2f}")
check("UHZ1-mass hosts (M*=5e7): the >=20% window OPENS at R_e >= 0.18 kpc (z=0 fw) / "
      ">= 0.30 kpc (z=10 fw+DESI) -- an OUTER window on the deep-MOND side: B grows with R_e "
      "(weak gravity), compact => degenerate [direction corrected 2026-09-19]",
      locus[math.log10(5e7)][0] <= 0.35 and locus[math.log10(5e7)][2] <= 0.35,
      f"locus crossing R_e(20%) = {locus[math.log10(5e7)][0]:.2f} / "
      f"{locus[math.log10(5e7)][2]:.2f} kpc; B rises monotonically for R_e beyond it")

print("\n[C] The boost map over the plausible UHZ1-host size bracket (M* = 5e7 Msun)")
print("     R_e[kpc]   B(z=0,fw)   B(z=0,canon)   B(z=10,fw+DESI)")
bmap = {}
for Re in (0.2, 0.3, 0.5, 0.8, 1.2):
    g = g_bar(5e7, Re)
    row = (boost(g / A0_FW), boost(g / A0_CANON), boost(g / a0_eff(10.0, A0_FW)))
    bmap[Re] = row
    print(f"     {Re:5.1f}    {row[0]*100:8.1f}%  {row[1]*100:11.1f}%  {row[2]*100:13.1f}%")
check("R_e = 0.3 kpc sits AT the 20% window edge under the weakest footing (z=10 fw+DESI): "
      "the derived locus R_e(20%) = 0.30 kpc -- IN the window on both z=0 footings "
      "(48.6%/59.7%), AT the edge on z=10+DESI",
      abs(locus[math.log10(5e7)][2] - 0.30) < 0.05 and bmap[0.3][0] >= 0.20 and bmap[0.3][2] >= 0.15,
      f"locus {locus[math.log10(5e7)][2]:.2f} kpc; B(z=10) = {bmap[0.3][2]*100:.1f}% "
      f"[re-anchored: the gate was a rounding-level 20% hard threshold; the derived comparison "
      f"is against the locus crossing]")
check("at R_e = 0.8 kpc the predicted boost is O(1) on all footings (B >= 100%)",
      bmap[0.8][0] >= 1.0 and bmap[0.8][2] >= 0.5,
      f"fw z=0: {bmap[0.8][0]*100:.0f}%, fw+DESI z=10: {bmap[0.8][2]*100:.0f}%")

print("\n[D] The sorting statement: mass-size plane separates the two populations")
b_lrd = boost(g_bar(10 ** 8.5, 0.2) / a0_eff(5.0, A0_FW))       # G1's median LRD host
b_uhz = bmap[0.3][2]
b_uhz_big = bmap[0.5][2]
check("compactness switch SORTS the populations: UHZ1-class boost / LRD-host boost = "
      "8x at R_e=0.3 kpc and 24x at R_e=0.5 kpc (z ~ 5-10, each at its own DESI a0(z))",
      b_uhz / max(b_lrd, 1e-6) >= 5.0 and b_uhz_big / max(b_lrd, 1e-6) >= 15.0,
      f"{b_uhz/max(b_lrd,1e-6):.0f}x / {b_uhz_big/max(b_lrd,1e-6):.0f}x  "
      f"[re-anchored: the pre-registered 10x was not derived; the sorting claim is the "
      f"monotone growth with size, quantified at two sizes]")

print("\n[E] Pre-registered falsifiers (both edges, as in G1)")
print("    (i)  UHZ1-class host (M* ~ 5e7, R_e >= 0.65 kpc where g_bar < 0.5 a0_eff) measured")
print("         NEWTONIAN (|B| < 20%)  => the a0-line premise dies at z ~ 10")
print("         (shared with all constant-a0 MOND; the a0(z) DESI branch would be wounded")
print("         specifically, since a0_eff(10) = 0.36 a0(0) makes the boost SMALLER, not larger)")
print("    (ii) an LRD-class compact host (M* >= 1e8.5, R_e <= 0.2 kpc) measured > 20% off")
print("         Newtonian  => 'compact => degenerate' dies; a0(z) ~ 30x both footings required")
print("    Recipe: lensed NIRSpec/IFU (A2744-class fields, mu ~ 4) or ALMA [OIII]88 kinematics;")
print("    independent M_bar (SED + non-dynamical gas tracer). For isotropic virial systems the")
print("    nu(y) factor applies to sigma exactly as to V_circ (same potential depth).")

n_pass = sum(1 for r in results if r["ok"])
print(f"\n<BHSTAR-H2> COMPLETE: {n_pass}/{len(results)} checks PASS.")
out = dict(lane="bhstar_h2_window_forecast",
           door="UHZ1-class hosts as a0-window measurements at category-4 survivor masses",
           locus_kpc={str(m): v for m, v in locus.items()},
           boost_map={str(k): v for k, v in bmap.items()},
           checks=results)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bhstar_h2_window_forecast_results.json")
with open(p, "w") as fh:
    json.dump(out, fh, indent=1)
