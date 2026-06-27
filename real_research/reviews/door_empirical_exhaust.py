#!/usr/bin/env python3
"""
DOOR 3 (EMPIRICAL) — exhaustion verdict: the LIVE, decidable frontier (2026-2028).
Carl: push the three open doors to exhaustion. Doors 1+2 (neutrino absolute mass, E6xSU(3)/modular flavor) are
EXHAUSTED FOR A FORCING (founded-not-derived stays). Door 3 is NOT exhausted -- it is the genuinely open frontier.

The key question: which framework tests are SEPARABLE from the dynamical-dark-energy degeneracy (i.e. decide the
framework on its OWN modified-inertia terms, independent of the w(z) model), vs which are DE-HOSTAGE (live but
degenerate, dissolve if w->-1)? This script lays out the answer, both-ways. Footing a0=9.36e-11, Z=sqrt(32pi/3).
NOT a TOE: every item is a GRAVITY / dark-sector test, not a mass derivation.
"""
print("="*100)
print("  DOOR 3 (EMPIRICAL) — the live frontier: DE-SEPARABLE MI-vs-MG locks vs DE-HOSTAGE falsifiers")
print("="*100)

# (sector, prediction, MI value, MG/null value, separable from dynamical-DE?, data, when)
SEPARABLE = [
 ("Cassini quadrupole", "|gamma-1| preferred-frame / MI strong-field",
  "framework PASSES ~5.5 orders under bound", "MG differs", "YES (strong-field, no w(z))", "IN HAND", "decided -> PASS"),
 ("Cluster relational sigma-spread", "non-adiabatic velocity-dispersion spread",
  "MI 6-13%", "MG EXACTLY 0 (MG-impossible)", "YES (kinematic, no w(z))", "member-sigma samples", "near-term"),
 ("MW-dwarf sigma-eccentricity clock", "sigma tracks ORBITAL eccentricity (the bath's clock)",
  "MI: correlation present", "MG: EXACTLY 0 (MG-impossible)", "YES (kinematic, no w(z))", "Gaia DR4 orbits", "DR4 (pilot NULL-but-UNDERPOWERED -> genuinely unrun)"),
 ("s^TX SME boost-dipole", "a0-induced preferred-frame Lorentz violation @ CMB apex",
  "8.7e-10, CPT-even, ~1.5x under bound", "MG: no induced s^TX", "YES (Lorentz sector, no w(z))", "INPOP/Cassini/Gaia DR4", "2026-2028"),
]
HOSTAGE = [
 ("a0(z) tomography", "a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE0)",
  "declining branch ~0.74 @ z=3", "DE-DEGENERATE; MUSE-DARK III (Ciocan 2026) reads a0 RISING (CONTESTED, LCDM-degenerate)", "DIES if w->-1"),
 ("Neutrino Sigma blade", "m1=E_L=2.2395 meV -> Sigma_NO ~ 61.3 meV (2.6 meV above floor)",
  "founded-not-derived (k=1 by fit)", "DE-model degenerate; dynamical DE RELIEVES not adds pressure", "JUNO (first data 2026-06-10) + DESI DR3"),
]
print("\n--- SEPARABLE from dynamical-DE (decide the framework on its OWN MI terms) ---")
for s in SEPARABLE:
    print(f"  * {s[0]:32s} | {s[1]}")
    print(f"      MI = {s[2]}   vs   {s[3]}")
    print(f"      separable: {s[4]}   data: {s[5]}   when: {s[6]}")
print("\n--- DE-HOSTAGE (live but degenerate; cite honestly, NOT clean locks) ---")
for h in HOSTAGE:
    print(f"  * {h[0]:32s} | {h[1]}")
    print(f"      MI = {h[2]}   caveat: {h[3]}   {h[4]}")

# the neutrino number the exhaustion confirmed (E_L forced, absolute mass NOT)
rho_DE_qtr_meV = 2.2395   # rho_DE^(1/4) in meV (7 sig figs, verified)
dm21, dm31 = 8.66e-3, 50.0e-3  # eV, sqrt of solar/atmospheric splittings (NO)
m1 = rho_DE_qtr_meV*1e-3      # eV, IF m1 = E_L (k=1 by FIT, not derivation)
import math
m2 = math.sqrt(m1**2 + dm21**2); m3 = math.sqrt(m1**2 + dm31**2)
Sig = (m1+m2+m3)*1e3
print(f"\n  neutrino check (Door 1, founded-not-derived): E_L = rho_DE^(1/4) = {rho_DE_qtr_meV} meV is FORCED (same rho_DE as a0);")
print(f"    IF m1=E_L (k=1 BY FIT): Sigma_NO = {Sig:.1f} meV, ~{Sig-58.8:.1f} meV above the minimal-NO floor 58.8 meV.")
print(f"    -> the ORDER is right and FORCED; the ABSOLUTE mass (k) is NOT forced. Founded-not-derived STANDS.")

print("\n"+"="*100)
print("""  EXHAUSTION VERDICT (Door 3 = the live frontier, both-ways):
   WHAT'S LEFT TO PUSH = the 4 DE-SEPARABLE MI-vs-MG locks above. They can CONFIRM or KILL the framework on its own
   modified-inertia terms, independent of the dynamical-DE degeneracy that hostages a0(z)/neutrino-Sigma:
     - Cassini (IN HAND) = the cleanest, already a PASS by ~5.5 orders;
     - the relational sigma-spread + the dwarf sigma-eccentricity clock = MG-IMPOSSIBLE (MG gives exactly 0), Gaia-DR4-era;
     - s^TX = the crunchiest LIVE test (~1.5x under bound, INPOP/Gaia DR4, 2026-2028).
   The DE-HOSTAGE falsifiers (a0(z), neutrino Sigma) stay live but DE-degenerate -- cite, do not over-debit (a0(z) rising
   is CONTESTED/LCDM-degenerate; dynamical DE RELIEVES the Sigma blade). Decisive window: Gaia DR4 + JUNO/DESI DR3, 2026-2028.
   NOT a TOE; NOT 'no doors' -- the framework's decidable content is real and near-term, on its own gravity-sector terms.""")
print("="*100)
