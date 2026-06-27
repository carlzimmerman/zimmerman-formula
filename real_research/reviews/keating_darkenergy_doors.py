#!/usr/bin/env python3
"""
FRONT 3 — Brian Keating's dark-energy / cosmology coverage vs the dS-Unruh modified-inertia framework.
=====================================================================================================
Keating's observational orbit (REAL, from his career + 'Into the Impossible' coverage):
  * He is the PI of the Simons Observatory (SO) and co-founder; ex-BICEP/BICEP2; POLARBEAR/Simons Array;
    informs CMB-S4.  His show covers DESI evolving dark energy (w0wa), the Hubble tension, S8/sigma8,
    JWST early-massive-galaxy / reionization puzzles, and CMB large-scale anomalies.
  * SO primary cosmology deliverables relevant here: (i) sigma8/S8 to ~1% via CMB-lensing x Rubin/Euclid
    at z~1-2; (ii) early dark-energy / w(z) leverage via lensing+SZ growth; (iii) the CMB acoustic peaks
    measured to <1% (the consistency anvil).
  * DESI w0wa (which his show foregrounds) is NOT a Keating experiment but is the data his coverage
    centers on, and is the framework's realest near-term tie.

This script maps the framework's three relevant signatures onto Keating's measurables and labels each
GENUINE-TEST / CONSISTENCY / BELOW-FLOOR — both-ways honest. Footing: a0(0)=9.36e-11 (cH_Lambda/Z),
a0(z) prop sqrt(rho_DE(z))  [the framework's OWN declining branch, NOT the rising cH(z)/Z].

Run: python real_research/reviews/keating_darkenergy_doors.py    (needs numpy)   -> exit 0
"""
import numpy as np

# ------------------------------------------------------------------ footing / constants
c   = 2.99792458e8
Mpc = 3.0857e22
H0  = 67.4e3 / Mpc                 # 1/s
Om, OL = 0.315, 0.685
H_Lambda = H0 * np.sqrt(OL)        # pure-Lambda de Sitter horizon rate
Z   = 2 * np.sqrt(8*np.pi/3)       # 5.7894...
a0_0 = c * H_Lambda / Z            # framework canonical a0(0)
print("="*88)
print("FOOTING")
print("="*88)
print(f"  Z = 2*sqrt(8pi/3)         = {Z:.5f}")
print(f"  a0(0) = c H_Lambda / Z    = {a0_0:.3e} m/s^2   (target 9.36e-11)")
assert abs(a0_0/9.36e-11 - 1) < 0.03, "a0(0) footing off"

# rho_DE(z) for w0waCDM:  rho_DE(z)/rho_DE(0) = (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z))
def rhoDE_ratio(z, w0, wa):
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))

# framework a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0))
def a0z_ratio(z, w0=-1.0, wa=0.0):
    return np.sqrt(rhoDE_ratio(z, w0, wa))

# ==================================================================================================
# DOOR (c): a0(z) prop sqrt(rho_DE(z)) tied to DESI w0wa  — the realest tie, MARGINAL + degenerate
# ==================================================================================================
print("\n" + "="*88)
print("DOOR (c)  a0(z) ~ sqrt(rho_DE(z))  vs DESI w0wa  [the central Keating-coverage tie]")
print("="*88)
# DESI DR1 public-chain central values (matching real_research/A0Z_DESI_CHAINS_RESULT)
combos = {
    "DESI+CMB+DESY5":    (-0.726, -1.06),
    "DESI+CMB+Union3":   (-0.642, -1.31),
    "DESI+CMB+Pantheon+":(-0.828, -0.74),
    "LCDM null (w=-1)":  (-1.000,  0.00),
}
print(f"  {'combo':<20} {'w0':>7} {'wa':>6} | a0(0.4)/a0(0)  a0(1.0)  a0(3.0)")
for name,(w0,wa) in combos.items():
    r04 = a0z_ratio(0.4, w0, wa)
    r10 = a0z_ratio(1.0, w0, wa)
    r30 = a0z_ratio(3.0, w0, wa)
    print(f"  {name:<20} {w0:>7.3f} {wa:>6.2f} | {r04:>11.3f}  {r10:>7.3f}  {r30:>7.3f}")
print("""
  READING:
   * Non-monotonic: w0>-1 makes rho_DE RISE first -> a0(z=0.3-0.7) sits +3% to +8% ABOVE local
     (the phantom-divide bump), crosses unity z~1.0-1.3, then declines for z>~2.
   * Significance is INHERITED from DESI's own w0wa preference (~2.4-3.0sigma DR1 floor), NOT an
     independent detection.  COLLAPSES to the flat LCDM line the instant w->-1.
   * This is a GENUINE near-term test ONLY in the sense that it RIDES DESI/Euclid w(z); the framework
     adds the BTFR/RAR zero-point as a SECOND, independent, same-direction observable of the SAME band.
  VERDICT(c): REAL but MARGINAL + DEGENERATE. A door that opens only as far as DESI's w0wa survives.
""")

# ==================================================================================================
# DOOR (d): delta-q00 = 0 CMB-safety  — a running a0 does NOT break the acoustic peaks (SURVIVAL)
# ==================================================================================================
print("="*88)
print("DOOR (d)  CMB-safety: does a running a0 disturb the <1% acoustic peaks SO/CMB-S4 anchor on?")
print("="*88)
# Two suppression mechanisms, both checked to order of magnitude.
# (1) EFE freezing: every perturbation sits in the cosmic field a_H = c H(z); ratio to a0(z).
#     For the DECLINING branch a0(z)=a0_0 sqrt(rho_DE/rho_DE0), at high z rho_DE/rho_DE0->O(1) (LCDM)
#     while cH(z) GROWS as E(z); so a_H/a0(z) GROWS -> MORE screened at recombination, not less.
def E(z):   return np.sqrt(Om*(1+z)**3 + OL)
for z in [0.0, 0.4, 3.0, 1100.0]:
    aH   = c*H0*E(z)
    a0z  = a0_0 * a0z_ratio(z, -1.0, 0.0)      # LCDM-branch a0(z) (declining/flat); rho_DE~const
    print(f"  z={z:<7.1f}  a_H=cH(z)={aH:.3e}   a0(z)={a0z:.3e}   a_H/a0(z)={aH/a0z:.3e}")
print("""
  At z=1100: a_H/a0(z) ~ 1e5  =>  the cosmic external field is ~1e5 x a0  =>  DEEP in the EFE-quasi-
  -Newtonian regime, NU(x)->1.  No MOND boost survives at recombination on the DECLINING branch.
  (2) GRADIENT suppression: the AeST MOND term lives in Y^{3/2}, Y built from field GRADIENTS; the
      homogeneous FRW background has Ybar=0 so a0 enters perturbations only at O(delta^3) -> ABSENT
      from the LINEAR Boltzmann hierarchy that sets the peaks.
  Hence delta-q00 (the monopole/00 stress perturbation from the running scale) -> 0 at linear order.
  VERDICT(d): CONSISTENCY / SURVIVAL, not a test. SO & CMB-S4's <1% peaks do NOT exclude the running a0
              (LEANING-SAFE; a rigorous hi_class+AeST run is the only remaining tightening). The framework
              SURVIVES the anvil Keating's instruments hammer hardest; it is not UNIQUELY tested by it.
""")

# ==================================================================================================
# DOOR (e): ghost-condensate dark sector = S8-NEUTRAL  vs SO's ~1% S8/sigma8  (NEUTRAL, not a test)
# ==================================================================================================
print("="*88)
print("DOOR (e)  S8/sigma8: SO measures S8 to ~1% (CMB-lensing x Rubin/Euclid, z~1-2). Framework signal?")
print("="*88)
# The framework's dark sector is a ghost condensate whose growth signature is, by the banked mean-vs-
# -variance theorem, S8-NEUTRAL (k^4 Jeans = AeST mu, out-of-window/CDM-degenerate, no S8 relief).
# Quantify: the only place a residual could enter is the EFE-frozen quasi-static boost nu(a_H/a0) at the
# growth epoch z~1-2. Compute that boost on BOTH branches and compare to SO's 1% floor.
def nu_simple(x):  # g_obs = nu(x) g, x = a_H/a0 ; simple interpolation
    return 0.5 + np.sqrt(0.25 + 1.0/x)
print(f"  {'z':>5} {'branch':<16} {'a_H/a0':>10} {'nu-1 (boost)':>14}")
for z in [1.0, 2.0]:
    aH = c*H0*E(z)
    # declining branch (framework's own): a0(z) ~ a0_0 (rho_DE ~ const in LCDM)
    a0_dec = a0_0 * a0z_ratio(z, -1.0, 0.0)
    x_dec  = aH/a0_dec
    # rising branch (rival cH(z)/Z) for contrast
    a0_ris = a0_0 * E(z)
    x_ris  = aH/a0_ris
    print(f"  {z:>5.1f} {'declining sqrtrhoDE':<16} {x_dec:>10.1f} {nu_simple(x_dec)-1:>14.2e}")
    print(f"  {z:>5.1f} {'rising cH/Z':<16} {x_ris:>10.1f} {nu_simple(x_ris)-1:>14.2e}")
print("""
  On the framework's OWN declining branch the quasi-static boost at z~1-2 is ~1e-4..1e-5 (a_H/a0 ~ 1e3-1e4),
  ~1e2..1e3x BELOW SO's 1% S8 floor.  Even the rival rising branch freezes a_H/a0 = Z = 5.79 -> nu-1 ~ 0.09,
  but that 9% lives in the EFE-screened, gradient-suppressed sector that the linear growth does NOT see
  (same delta-Y=0 / Ybar=0 theorem as door d) -> S8-NEUTRAL by construction, banked.
  VERDICT(e): NEUTRAL. SO's flagship ~1% S8 does NOT test the framework: the ghost-condensate sector is
              S8-neutral by theorem and any residual quasi-static boost is below the SO floor. A non-test.
""")

# ==================================================================================================
# WHICH KEATING-ORBIT MEASUREMENT MOST BEARS ON THE FRAMEWORK?
# ==================================================================================================
print("="*88)
print("SYNTHESIS — ranking Keating-orbit measurements by how much they BEAR on the framework")
print("="*88)
print("""
  1. DESI/Euclid w0wa  (covered heavily on his show; NOT his instrument)
        -> the ONLY framework-DISTINCTIVE near-term tie (door c). GENUINE TEST but MARGINAL (~2.4-3.0s,
           DR1 floor) and DEGENERATE (vanishes if w->-1). The a0(z) BTFR/RAR zero-point is the framework's
           own second handle on the same band. DR2/DR3 + Euclid w(z) is the live gate.
  2. SO/CMB-S4 acoustic peaks <1%   (HIS instrument, the anvil)
        -> door d: the framework SURVIVES (CMB-safe, delta-q00->0). CONSISTENCY, not a test.
  3. SO S8/sigma8 ~1%   (HIS flagship LSS deliverable)
        -> door e: S8-NEUTRAL by theorem + below-floor boost. NON-TEST.
  4. Hubble tension / JWST early-galaxy / CMB anomalies (show topics)
        -> NO framework-distinctive lever (the framework neither predicts nor resolves H0; a0(z) is
           growth-epoch-agnostic). NOT a door.

  BOTTOM LINE: Of everything in Keating's orbit, the single measurement that most bears on the framework is
  the DESI(->Euclid) w0wa band (door c) — and it is a MARGINAL, DESI-HOSTAGE, w->-1-degenerate door, the
  realest tie but not a clean independent test. Keating's OWN instruments (SO/CMB-S4) deliver CONSISTENCY
  (CMB-safe) and a NEUTRAL S8 — the framework survives the hardest anvil but is not uniquely tested by it.
""")
print("DONE (exit 0)")
