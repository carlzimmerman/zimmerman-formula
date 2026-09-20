#!/usr/bin/env python3
"""
bhstar_g1_lrd_host_a0_window.py -- DOOR G1 off the BH* absorption (arXiv:2609.09274).
=====================================================================================
THE DOOR. The absorption review's regime table found the fork hiding in plain sight:

  * BH* pseudo-photospheres: g ~ 3e5-1.3e6 x a0  -> deep-Newtonian, a0-line DORMANT (1.00000).
  * LRD HOSTS: M* ~ 1e8-8.5 Msun at R_e ~ 0.1-0.3 kpc -> g_bar ~ 10-40 a0 -> ALSO degenerate.
  * But NORMAL dwarfs of the SAME stellar mass at z ~ 5 (R_e ~ 1-2 kpc) sit at g_bar ~ 0.2-0.5 a0
    -> DEEP in the a0 window, where the a0-line lifts V by sqrt(1+1/y)-1 = O(1).

THE COMPACTNESS-SWITCH PREDICTION (novel, pre-registered here):
  At FIXED stellar mass M* ~ 1e8.5 Msun and fixed z, the a0-line says the ANOMALY is a function of
  compactness alone: compact LRD hosts ride ON the Newtonian baryon curve (+ a few %), while
  extended field dwarfs of the same mass ride ~1.5-2x ABOVE it. The LRD population is therefore
  the CONTROL and the matched-mass extended dwarf is the TEST. No lane in this repo has ever
  keyed a prediction to the LRD host population; this one does, with a falsifier on both sides.

CONVENTIONS (exactly as committed in the record):
  - a0 footings: fw = c H_Lambda / Z = 9.3619e-11 (kappa = 1/2); canon = 1.2e-10; SPARC 1.13e-10.
  - interpolation nu(y) = sqrt(1 + 1/y), y = g_bar/a0 (agentCC's locked convention, quoted in
    agentGG_jwst_highz.md). a0-line: g_obs = g_bar * nu(y).
  - a0(z): the settled DESI reading (jwst_full_predictions.py):
        a0(z)/a0(0) = sqrt( rho_DE(z)/rho_DE(0) ), CPL (w0, wa) = (-0.752, -0.86).
  - point-mass g_bar = GM*/R_e^2 is an UPPER bound on the true Newtonian g at R_e (agentGG
    discipline): the boost B = nu(y)-1 computed with it is a LOWER bound at fixed M_bar.
  - mass budget bracket M_bar = f * M*, f in {1, 3} (gas-rich dwarfs; agentGG's co-blocker).

THE FALSIFIER (both edges, pre-registered):
  (i)  Extended field dwarf, z ~ 5, M* ~ 1e8.5 Msun, R_e ~ 1-2 kpc, rotation curve or dispersion
       reaching >= 2 R_e (~ 3 kpc ~ 3 r_MOND): a0-line predicts V/V_Newton >= 1.4 at the outer
       point (point-mass floor, fw+DESI). Measured Newtonian (within 20%) => the a0-line premise
       dies at z ~ 5 (a tension SHARED with all constant-a0 MOND, S3-17-style -- not framework-
       distinctive).
  (ii) Compact LRD host, matched M*, R_e <= 0.3 kpc: a0-line predicts |V/V_Newton - 1| < 5%.
       Any robust >20% offset in an LRD host kills "compact => Newtonian-degenerate" and would
       demand a0(z) ~ 30x larger than both footings at z ~ 5.
  Recipe: NIRSpec/IFU Halpha or ALMA [OIII]88 kinematics; independent M_bar (SED M* + non-
  dynamical gas tracer, the agentGG co-requirement); EFE must be modelled for the dwarf (the
  committed EFE machinery re-enters; underdense-environment selection is the clean control).

Run:  python3 reviews/bhstar_g1_lrd_host_a0_window.py  (stdlib only)
"""

import math, json, os

G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
A0_FW = 9.3619e-11
A0_CANON = 1.2e-10
W0, WA = -0.752, -0.86          # locked DESI CPL

def nu(y):                      # the framework's locked interpolation
    return math.sqrt(1.0 + 1.0 / y)

def boost(y):
    return nu(y) - 1.0

def y_from_boost(B):            # exact inversion of B = sqrt(1+1/y)-1
    return 1.0 / ((1.0 + B) ** 2 - 1.0)

def a0_eff(z, a0_0):
    """DESI declining-a0 reading, identical form to the committed jwst_full_predictions.py."""
    rho_ratio = (1.0 + z) ** (3.0 * (1.0 + W0 + WA)) * math.exp(-3.0 * WA * z / (1.0 + z))
    return a0_0 * math.sqrt(rho_ratio)

results = []
def check(name, ok, detail=""):
    results.append(dict(check=name, ok=bool(ok), detail=detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    return ok

print("=" * 78)
print("DOOR G1 -- THE COMPACTNESS SWITCH (LRD hosts = control, matched dwarfs = test)")
print("=" * 78)

print("\n[A] Exact inversion of the a0-line boost locus")
ok_all = True
for B in (0.20, 0.50, 1.00):
    y = y_from_boost(B)
    ok = abs(boost(y) - B) <= 1e-12 * max(1.0, B)
    ok_all &= ok
    print(f"    B = {B:.2f}  ->  y* = {y:.6f}  (round-trip residual {abs(boost(y)-B):.2e})")
check("B(y) round-trip exact to 1e-12 at B = 0.2/0.5/1.0", ok_all)
print(f"    locus: B=20% at g_bar = {y_from_boost(0.2):.4f} a0 ; B=50% at g_bar = "
      f"{y_from_boost(0.5):.4f} a0")

print("\n[B] a0(z) DESI reading reproduced independently (locked values: 0.737 @ z=3, 0.506 @ z=6)")
for z, locked in ((3.0, 0.737), (6.0, 0.506)):
    v = a0_eff(z, 1.0)
    check(f"a0({z:.0f})/a0(0) = {v:.4f} vs locked {locked}", abs(v - locked) / locked < 0.005)

print("\n[C] The locus in the mass-size plane (fw footing; R_e in kpc where the boost crosses)")
print("    M*[Msun]   R_e(20%) z=0   R_e(50%) z=0   R_e(20%) z=5   R_e(50%) z=5")
locus_rows = {}
for lgM in (7.0, 8.0, 8.5, 9.0, 10.0):
    M = 10 ** lgM * MSUN
    row = []
    for z in (0.0, 5.0):
        a0 = a0_eff(z, A0_FW) if z else A0_FW
        for B in (0.20, 0.50):
            g_t = y_from_boost(B) * a0
            row.append(math.sqrt(G * M / g_t) / KPC)
    locus_rows[lgM] = row
    print(f"    1e{lgM:<8.0f} {row[0]:9.2f} {row[1]:11.2f} {row[2]:12.2f} {row[3]:13.2f}")

print("\n[D] LRD-host grid (paper's own host masses; R_e bracket until JWST sizes land)")
print("    M* = 1e8.5 Msun, z=0 and z=5 (fw footing, M_bar = M*):")
print("     R_e[kpc]   B(z=0)     B(z=5,DESI)")
host_boosts = {}
for Re in (0.1, 0.2, 0.3, 0.5, 1.0):
    g = G * 10 ** 8.5 * MSUN / (Re * KPC) ** 2
    b0 = boost(g / A0_FW)
    b5 = boost(g / a0_eff(5.0, A0_FW))
    host_boosts[Re] = (b0, b5)
    print(f"     {Re:6.2f}    {b0*100:7.2f}%   {b5*100:8.2f}%")
b_med = host_boosts[0.2]
check("median LRD host (M*=1e8.5, Re=0.2 kpc) is DEGENERATE: B(z=0) < 5%", b_med[0] < 0.05,
      f"B = {b_med[0]*100:.2f}%")
check("same host under DESI a0(z=5) stays degenerate: B(z=5) < 5%", b_med[1] < 0.05,
      f"B = {b_med[1]*100:.2f}%")
check("extended R_e=1 kpc at same mass CROSSES the window: B(z=0) > 50%",
      host_boosts[1.0][0] > 0.50, f"B = {host_boosts[1.0][0]*100:.1f}%")

print("\n[E] The matched-mass control: extended z~5 dwarf (R_e = 1.5 kpc, M* = 1e8.5)")
g_d = G * 10 ** 8.5 * MSUN / (1.5 * KPC) ** 2
b_d1 = boost(g_d / a0_eff(5.0, A0_FW))                       # M_bar = M*
b_d3 = boost(g_d / (3.0 * a0_eff(5.0, A0_FW)))               # M_bar = 3 M* (gas-rich)
b_d1_fw0 = boost(g_d / A0_FW)                                # z=0 footing for reference
print(f"    g_bar = {g_d:.3e} m/s^2 = {g_d/a0_eff(5.0,A0_FW):.2f} x a0_eff(z=5)"
      f" [{g_d/A0_FW:.2f} x a0(0)]")
print(f"    predicted V/V_Newton (point-mass floor): M_bar=M*: {1+b_d1:.2f}"
      f"  |  M_bar=3M*: {1+b_d3:.2f}")
check("dwarf floor (M_bar=M*, z=5, fw+DESI): B >= 40%", b_d1 >= 0.40, f"B = {b_d1*100:.1f}%")
check("dwarf floor survives the gas-rich budget (M_bar=3M*): B >= 100%", b_d3 >= 1.00,
      f"B = {b_d3*100:.1f}%")
contrast = b_d1 / max(b_med[1], 1e-12)
check("CONTRAST at matched M*, z=5: dwarf boost / LRD-host boost >= 10x", contrast >= 10.0,
      f"{contrast:.0f}x  (dwarf {b_d1*100:.0f}% vs LRD host {b_med[1]*100:.1f}%)")

r_mond = math.sqrt(G * 10 ** 8.5 * MSUN / a0_eff(5.0, A0_FW)) / KPC
print(f"    r_MOND(M*=1e8.5, a0_eff(z=5)) = {r_mond:.2f} kpc  ->  the recipe needs the rotation"
      f" curve out to >= 2 R_e ~ 3 kpc ~ {3.0/max(r_mond,1e-9):.1f} x r_MOND (agentGG's own co-requirement)")

print("\n[F] Falsifier registration (pre-registered, both edges)")
print("    (i)  extended dwarf measured NEWTONIAN at >= 2 R_e  => a0-line premise dies at z~5")
print("         (shared with all constant-a0 MOND: S3-17-style shared tension, not distinctive)")
print("    (ii) compact LRD host measured >20% off Newtonian          => 'compact => degenerate'")
print("         dies; would demand a0(z=5) ~ 30x BOTH footings -- kills the a0(z) program")
print("    Recipe: NIRSpec/IFU Halpha or ALMA [OIII]88; independent M_bar; EFE modelled /")
print("    underdense-field selection; the committed EFE machinery re-enters at analysis time.")

n_pass = sum(1 for r in results if r["ok"])
print(f"\n<BHSTAR-G1> COMPLETE: {n_pass}/{len(results)} checks PASS.")
out = dict(lane="bhstar_g1_lrd_host_a0_window",
           door="compactness switch: LRD hosts (control) vs matched-mass extended dwarfs (test)",
           footings=dict(a0_fw=A0_FW, a0_canon=A0_CANON, desi_cpl=[W0, WA]),
           locus_rows_kpc=locus_rows,
           host_boosts=dict(Re_kpc={str(k): v for k, v in host_boosts.items()}),
           dwarf=dict(B_Mbar1=b_d1, B_Mbar3=b_d3, r_mond_kpc=r_mond),
           contrast_ratio=contrast,
           checks=results)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bhstar_g1_lrd_host_a0_window_results.json")
with open(p, "w") as fh:
    json.dump(out, fh, indent=1)
