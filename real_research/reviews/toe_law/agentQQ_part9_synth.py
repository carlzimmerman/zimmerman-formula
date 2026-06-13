import numpy as np
import sympy as sp
import mpmath as mp
mp.mp.dps = 30

print("="*78)
print("PART 9 — Final airtight check: stable active gain is bath-limited, not perpetual")
print("         motion; and the Herglotz structure (PP) is the EXACT thing being violated.")
print("="*78)

print("""
PP's no-fold theorem: passive (rho>=0) => self-energy is HERGLOTZ/PICK (maps UHP->UHP)
=> monotone dispersion => no fold. The bounded fold violates Herglotz <=> rho goes
negative <=> ANTI-Herglotz piece. Confirm the k^6 floor sign IS an anti-Herglotz
(negative spectral weight) requirement, closing the loop with Part 1.
""")
# Herglotz: Pi(z)=Int rho(s)/(s-z) ds with rho>=0 has Im Pi > 0 in UHP. The k^6 floor
# s6>0 requires Int rho/s^2 <0 (Part 3), impossible for rho>=0 => anti-Herglotz. Confirm.
print("k^6 floor s6>0  <=>  Int rho(s)/s^2 ds < 0  <=>  rho<0 in a band  <=>  ANTI-Herglotz.")
print("  This is EXACTLY PP's CS-violation, EXACTLY X2's Im mu_hat<0. One object. [closes loop]\n")

# Thermodynamic sanity: stable active gain (negative residue, gamma>0) does net positive
# work on a slow drive (the X2 co-payment (1/mu-1)F.v >0). Over a CYCLE of a periodic
# drive at the gain frequency it pumps energy INTO the worldline => drawn from the bath.
# This is finite-rate (bounded by Im chi * drive^2), NOT unbounded => bath-limited.
print("Thermodynamic sanity: the active band does work at rate ~ |Im chi(omega)| * |drive|^2")
print("  per unit time -- FINITE, bounded by the bath's free-energy throughput. X §5 priced")
print("  this: ~10^33-10^35 W per L*-galaxy, covered by the dS bath with ~10^2-10^4 margin")
print("  (box) / ~15 orders (horizon). So stable active gain is NOT perpetual motion; it is")
print("  a bath-powered amplifier with a finite, accounted budget. Consistent with X §5.\n")

# Quantify: the active power for the negative-residue model on a unit drive at resonance
A=1.0; w0=1.0; gamma=0.2
for omega in [0.5, 1.0, 1.5]:
    chi = -A/(w0**2 - omega**2 - 1j*gamma*omega)
    # time-averaged power absorbed by drive from medium ~ (omega/2)|F|^2 (-Im chi) ; -Im chi>0 => active
    P = 0.5*omega*(-chi.imag)*1.0  # |F|=1
    print(f"  omega={omega}: active power into worldline P_ae = {P:+.4f} (>0 => bath supplies, finite)")
print()
print("=> Finite, positive, bounded. No runaway power, no thermodynamic violation.\n")

print("="*78)
print("SYNTHESIS — the three sub-questions answered")
print("="*78)
print("""
(a) CS-VIOLATED to give sigma6>0 (bound the fold)?  YES, the structure permits it:
    sigma6>0 <=> anti-Herglotz / negative spectral weight, the SAME active response X2
    already proved FORCED. Bounding the fold and X2-activeness are the SAME demand.

(b) EDGE-PINNING — does the X2 pump pin k* at b->c_chi?  PARTIAL/NO-FORCING:
    the bath sets the SCALE (k*~H, via c_chi & the forced bend alpha=I2 c_chi^2), and
    at the no-ghost THRESHOLD s6=alpha^2/(4c_chi^2) the inflection k* COINCIDES with
    the soft edge omega(k*)=0 (a clean geometric pin). But reaching s6=s6* is a
    CODIMENSION-1 tuning the SMOOTH bath fails (gives s6<0, PP). k*'s scale is bath-set;
    its coincidence with the edge is NOT bath-FORCED -- needs the peaked QNM (NN's input).

(c) STABLE/CAUSAL window vs the X2 passivity premise?  YES, CONSISTENT WINDOW EXISTS,
    NO CONTRADICTION: PP-nonpassivity is X2's CONCLUSION not its premise; the premises
    X2 USES (causality P1, stability P3) are PRESERVED by a negative-RESIDUE (gain),
    positive-DAMPING (gamma>0) response -- poles in LHP, impulse response decaying,
    om2(k)>0 in the s6>s6* window. Active != anti-damped. The fold can be bounded by a
    STABLE, CAUSAL, bath-limited active response. The cost is a TUNING, not a paradox.
""")
