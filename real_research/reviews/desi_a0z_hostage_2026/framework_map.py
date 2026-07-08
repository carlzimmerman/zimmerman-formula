#!/usr/bin/env python3
"""
Scout C: FRAMEWORK MAPPING of the dS-Unruh modified-inertia MOND hostage.

Distinctive content:  a0(z) = a0(0) * sqrt(rho_DE(z)/rho_DE(0))
The framework INHERITS w(z) from observation; a0 propto sqrt(rho_DE) is
DEGENERATE with generic CPL evolving DE. This script maps the magnitude of
the distinctive a0(z) signal across the DESI DR2 (2025) SNe combos and shows
it -> flat (a0(z)=const) as w->-1, at which point the framework DISSOLVES to
plain constant-a0 MOND (non-distinctive), NOT falsified.

Footing: canonical a0(0) = c*H_Lambda/Z = 9.36e-11 m/s^2  (rho_DE footing).
"""
import numpy as np

A0_CANON = 9.36e-11  # m/s^2, canonical rho_DE / cH_Lambda footing

def rho_DE_ratio(z, w0, wa):
    """
    CPL w(a) = w0 + wa*(1-a), a = 1/(1+z).
    rho_DE(z)/rho_DE(0) = a**(-3*(1+w0+wa)) * exp(3*wa*(a-1))
    """
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+w0+wa)) * np.exp(3.0*wa*(a-1.0))

def a0_of_z(z, w0, wa):
    return A0_CANON * np.sqrt(rho_DE_ratio(z, w0, wa))

# DESI DR2 (2025) CPL best-fit combos (DESI BAO + CMB + each SNe sample)
# arXiv:2503.14738 (DESI DR2 cosmology). Values as provided in the tasking.
combos = {
    "DESY5 (w0=-0.752, wa=-0.86)":     (-0.752, -0.86),
    "Pantheon+ (w0=-0.838, wa=-0.62)": (-0.838, -0.62),
    "Union3 (w0=-0.667, wa=-1.09)":    (-0.667, -1.09),
    "LCDM (w0=-1.0, wa=0.0)":          (-1.0,    0.0),
}

# probe the bump epoch and grid
z_bump_scan = np.linspace(0.0, 1.2, 241)

print("="*78)
print("SCOUT C -- FRAMEWORK a0(z) MAPPING  (canonical a0(0)=9.36e-11 m/s^2)")
print("  a0(z) = a0(0)*sqrt(rho_DE(z)/rho_DE(0)),  CPL w(a)=w0+wa(1-a)")
print("="*78)

header = f"{'combo':<34}{'bump@peak':>11}{'z_peak':>8}{'a0(0.4)/a0(0)':>15}{'a0(3)/a0(0)':>13}"
print(header)
print("-"*len(header))

results = {}
for name, (w0, wa) in combos.items():
    ratio_scan = np.sqrt(rho_DE_ratio(z_bump_scan, w0, wa))  # a0(z)/a0(0)
    ipeak = int(np.argmax(ratio_scan))
    z_peak = z_bump_scan[ipeak]
    bump_peak = ratio_scan[ipeak] - 1.0            # max fractional bump
    r_04 = np.sqrt(rho_DE_ratio(0.4, w0, wa))      # at z~0.4
    r_3  = np.sqrt(rho_DE_ratio(3.0, w0, wa))      # deep, z=3
    results[name] = dict(w0=w0, wa=wa, z_peak=z_peak, bump_peak=bump_peak,
                         r_04=r_04, r_3=r_3)
    print(f"{name:<34}{bump_peak*100:>+9.2f}%{z_peak:>8.2f}"
          f"{r_04:>15.4f}{r_3:>13.4f}")

print("-"*len(header))
print("Notes:")
print("  * bump = peak of a0(z)/a0(0) > 1 (phantom side, w<-1-ish region early)")
print("  * a0(3)/a0(0) < 1 = the distinctive DECLINE deep in matter era")
print("  * LCDM row = 1.0000 flat everywhere -> DISSOLVED (non-distinctive)")

# ---- Prove-by-moving: walk wa -> 0 (toward w=-1) and watch the signal die ----
print()
print("PROVE-BY-MOVING: hold w0=-1, sweep wa -> 0  (approach to LCDM)")
print(f"{'wa':>8}{'bump@0.4':>12}{'a0(3)/a0(0)':>14}")
print("-"*34)
for wa in [-1.0, -0.6, -0.3, -0.1, -0.01, 0.0]:
    r_04 = np.sqrt(rho_DE_ratio(0.4, -1.0, wa))
    r_3  = np.sqrt(rho_DE_ratio(3.0, -1.0, wa))
    print(f"{wa:>8.2f}{(r_04-1.0)*100:>+10.3f}%{r_3:>14.4f}")
print("  -> as wa->0 (w->-1), a0(0.4)/a0(0)->1 and a0(3)/a0(0)->1: signal DIES.")

# ---- Magnitude spread across evolving combos ----
evolving = [k for k in combos if "LCDM" not in k]
bumps = [results[k]["bump_peak"]*100 for k in evolving]
a03s  = [results[k]["r_3"] for k in evolving]
print()
print("MAGNITUDE SPREAD across evolving-DE combos (dataset-specific):")
print(f"  peak bump:   {min(bumps):+.2f}%  to  {max(bumps):+.2f}%")
print(f"  a0(3)/a0(0): {min(a03s):.3f}  to  {max(a03s):.3f}")
print("  => SIGN structure (bump-then-decline) robust; MAGNITUDE not.")

# ---- Hostage-alive significance: DESI DR2 (2025) evolving-DE sigma ----
print()
print("HOSTAGE-ALIVE SIGNIFICANCE (w=-1 exclusion, DESI DR2 2025, arXiv:2503.14738):")
sigmas = {
    "DESI+CMB+DESY5":    4.2,
    "DESI+CMB+Union3":   3.9,
    "DESI+CMB+Pantheon+":2.8,
    "DESI+CMB (no SNe)": 3.1,
}
for k, s in sigmas.items():
    print(f"  {k:<22}: {s:.1f} sigma")
print("  Range 2.8-4.2 sigma; SNe-sample-driven (DESY5 high, Pantheon+ low).")
print("  Framework a0 propto sqrt(rho_DE) sits INSIDE this contour BY CONSTRUCTION")
print("  (it inherits w(z)); ALIVE is NECESSARY, not a WIN. Degenerate w/ CPL.")
print("="*78)
