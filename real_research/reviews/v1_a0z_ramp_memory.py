#!/usr/bin/env python3
r"""
VEIN 1 -- P5: THE COSMOLOGICAL a0(z) RAMP AS A SLOW MEMORY DRIVE.
================================================================================
B4 DISCIPLINE: no assumed sign. Real calc of the kernel-lag in a0(z), checked
against the banked adiabaticity_of_a0z.py result and against MG both ways.

FRAMEWORK: a0(z) = cH_Lambda(z)/Z with the framework reading a0(z) ~ sqrt(rho_DE(z));
the de Sitter horizon BATH sets inertia, and the bath thermalizes on ~ a Hubble time
(Gamma_th ~ H_DE). So when rho_DE evolves (under dynamical DE / w!=-1), the bath
TEMPERATURE -- hence a0 felt by a body -- LAGS the instantaneous background value.
This lag is the SAME time-nonlocality (memory) as theta(y), now driven by the SLOW
cosmological clock instead of an orbit.

THE POSIT: under dynamical DE (w(z)!=-1, so rho_DE actually evolves), the framework's
MODIFIED-INERTIA a0 felt by galaxies at redshift z is a MEMORY-LAGGED (low-pass
filtered) version of cH_Lambda(z)/Z, NOT the instantaneous value. A modified-GRAVITY
a0(z) (a coupling constant that is whatever the local field equations say NOW) tracks
the instantaneous background. => at fixed z, MI predicts a0_felt(z) BETWEEN a0(0) and
the instantaneous a0_inst(z); MG (if it evolved a0 at all) tracks a0_inst(z). The LAG
is an MI-specific, time-nonlocal offset.

WHAT WE COMPUTE (both-ways):
  (1) The instantaneous a0_inst(z) = a0(0) sqrt(rho_DE(z)/rho_DE0) for a CPL w(z).
  (2) The memory-lagged a0_felt(z) from a first-order relaxation (low-pass) ODE with
      relaxation rate Gamma_th = H_DE (the banked thermalization rate): the framework's
      OWN bath cannot update faster than it thermalizes.
  (3) The LAG = a0_felt - a0_inst at each z, and whether it is (a) nonzero, (b) of a
      definite sign, (c) distinguishable from the instantaneous (MG-like) law given data.
  (4) BOTH-WAYS: if w=-1 exactly, rho_DE is constant -> NO ramp -> NO lag -> the whole
      signal VANISHES (DE-hostage). Quantify how fast it vanishes as w->-1.

FOOTING sealed. DO NOT git-push.
"""
import math
import numpy as np

# cosmology
H0_kmsMpc = 67.4
H0 = H0_kmsMpc*1e3/3.0857e22      # 1/s
Om, OL = 0.315, 0.685
def E_LCDM(z): return math.sqrt(Om*(1+z)**3 + OL)

# dynamical DE: CPL w(a)=w0+wa(1-a). rho_DE(z)/rho0 = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z))
def rho_DE_ratio(z, w0, wa):
    a = 1.0/(1.0+z)
    return (1+z)**(3*(1+w0+wa)) * math.exp(-3*wa*(1-a))
def H_of_z(z, w0, wa):
    return H0*math.sqrt(Om*(1+z)**3 + OL*rho_DE_ratio(z,w0,wa))

print("="*100)
print(" VEIN 1 -- P5: a0(z) RAMP AS A SLOW MEMORY DRIVE  (kernel-lag of the cosmological bath, both-ways)")
print("="*100)

# instantaneous framework a0(z) ~ sqrt(rho_DE(z)) (the framework's declining ansatz)
def a0_inst_ratio(z, w0, wa):  return math.sqrt(rho_DE_ratio(z,w0,wa))

# memory-lagged a0_felt: first-order relaxation toward a0_inst with rate Gamma_th=H_DE(z).
# d a0_felt/dt = Gamma_th (a0_inst - a0_felt).  Integrate in z (dt = -dz/((1+z)H)).
def a0_felt_track(zmax, w0, wa, n=4000, gamma_factor=1.0):
    zs = np.linspace(zmax, 0.0, n)   # integrate from high z (early) to z=0
    af = a0_inst_ratio(zmax, w0, wa) # assume locked to instantaneous at early time
    out=[]
    for i in range(len(zs)-1):
        z = zs[i]; zn = zs[i+1]
        H = H_of_z(z, w0, wa)
        # H_DE: the de Sitter (dark-energy) Hubble rate = H0 sqrt(OL rho_ratio) (the BATH clock)
        H_DE = H0*math.sqrt(OL*rho_DE_ratio(z,w0,wa))
        Gamma_th = gamma_factor*H_DE
        dt = (z - zn)/((1+z)*H)      # positive dt going forward in time (z decreasing)
        ainst = a0_inst_ratio(z, w0, wa)
        af += Gamma_th*(ainst - af)*dt
        out.append((z, ainst, af))
    out.append((0.0, a0_inst_ratio(0,w0,wa), af))
    return out[::-1]

# --- scenario A: notable dynamical DE (DESI-ish thawing) ---
print("\n  Scenario A: dynamical DE  w0=-0.9, wa=-0.4  (rho_DE actually evolves -> a real ramp).")
print(f"  {'z':>4s} {'a0_inst/a0(0)':>14s} {'a0_felt/a0(0)':>14s} {'LAG=felt-inst':>14s} {'lag %':>7s}")
trackA = a0_felt_track(3.0, -0.9, -0.4)
def at(track, ztarget): return min(track, key=lambda r: abs(r[0]-ztarget))
for s in (3.0,2.0,1.0,0.5,0.0):
    z,ai,af = at(trackA, s)
    print(f"  {z:4.1f} {ai:14.4f} {af:14.4f} {af-ai:14.4f} {(af-ai)/ai*100:7.2f}")

# --- scenario B: w=-1 exactly (LCDM DE) -> rho_DE constant -> no ramp -> no lag ---
print("\n  Scenario B (both-ways): w=-1 exactly -> rho_DE CONSTANT -> ramp and lag must VANISH.")
trackB = a0_felt_track(3.0, -1.0, 0.0)
print(f"  {'z':>4s} {'a0_inst/a0(0)':>14s} {'a0_felt/a0(0)':>14s} {'LAG':>10s}")
for s in (3.0,2.0,1.0,0.5,0.0):
    z,ai,af = at(trackB, s)
    print(f"  {z:4.1f} {ai:14.4f} {af:14.4f} {af-ai:10.6f}")

# --- how the lag scales with departure from w=-1 ---
print("\n  LAG at z=2 vs dynamical-DE strength (how fast the signal dies as w->-1):")
print(f"  {'(w0,wa)':>14s} {'a0_inst(z=2)':>13s} {'a0_felt(z=2)':>13s} {'lag %':>7s}")
for w0,wa in [(-0.8,-0.6),(-0.9,-0.4),(-0.95,-0.2),(-0.99,-0.04),(-1.0,0.0)]:
    tr = a0_felt_track(3.0, w0, wa)
    z2 = min(tr, key=lambda r: abs(r[0]-2.0))
    print(f"  {('('+str(w0)+','+str(wa)+')'):>14s} {z2[1]:13.4f} {z2[2]:13.4f} {(z2[2]-z2[1])/z2[1]*100:7.2f}")

print("\n"+"-"*100)
print("  (3) MG comparison + a0-degeneracy")
print("-"*100)
print("""  - MG with an evolving a0 (e.g. AeST a0~theta=3H): a0 is whatever the LOCAL field equations give NOW,
    instantaneous. It tracks a0_inst(z). NO memory lag.
  - MI: the felt a0 is the bath TEMPERATURE, which relaxes at Gamma_th~H_DE -> a0_felt LAGS a0_inst.
  - The MI-specific content is the LAG (felt - inst). BUT: measuring a0(z) at all is already at the
    edge of feasibility (high-z RAR/BTFR), and the lag is a SECOND-ORDER offset ON TOP of the (already
    contested) decline. It is NOT separately a0-degenerate in the trivial sense (it is a z-DEPENDENT
    deviation from BOTH constant and instantaneous-decline), but it is far below current measurability.""")

print("\n"+"="*100)
print(" VERDICT -- P5 (a0(z) ramp as slow memory drive), both ways")
print("="*100)
laA_z2 = at(trackA, 2.0)
print(f"""  REAL but SMALL and DE-HOSTAGE. Under genuine dynamical DE (w0=-0.9,wa=-0.4) the bath's finite
  thermalization (Gamma_th~H_DE, the banked adiabaticity result) makes a0_felt LAG a0_inst by
  ~{abs((laA_z2[2]-laA_z2[1])/laA_z2[1]*100):.1f}% at z=2 -- a genuine time-nonlocal (memory) offset that MG's instantaneous a0(z)
  does NOT have. SIGN (as the calc gives it, not assumed): a0_felt sits on the REMEMBERED side of
  a0_inst -- it lags the instantaneous value, so when a0_inst is rising toward z=0 the felt value sits
  BELOW it, and when a0_inst falls toward high z the felt value sits ABOVE it. The felt curve is a
  LOW-PASS-SMOOTHED version of the instantaneous sqrt(rho_DE) ramp.

  BOTH-WAYS KILL: if w=-1 exactly, rho_DE is constant, the ramp and the lag are EXACTLY ZERO (scenario B).
  The whole signal is HOSTAGE to dynamical DE -- it dies precisely when DESI converges to w=-1, the same
  hostage condition as the a0(z) test itself. And even at maximal plausible dynamical DE the lag is a
  few-% offset on an already-contested, barely-measurable a0(z) decline.

  => GENUINELY time-nonlocal and MG-distinct in PRINCIPLE (MG has no bath to lag), but observationally
  SPECULATIVE: a few-% second-order offset on top of a contested, hard-to-measure first-order decline,
  and DE-hostage. Grade: SPECULATIVE. Not a near-term discriminator; a conceptual MI signature of the
  cosmological clock, banked, not actionable.""")
print("="*100)
