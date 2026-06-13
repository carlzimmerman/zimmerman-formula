import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("PART 6 — EDGE-PINNING (question a): does the dS bath PIN k* at b->c_chi, or is k* free?")
print("="*78)

print("""
NN's edge-coincidence condition: omega''(k*)=0 must land AT the b->c_chi sonic edge
frequency. The b->c_chi edge is where the in-medium sound speed c_chi is approached
(the khronon's own sound horizon). Two scales in the problem:
  - H (dS Hubble / Gibbons-Hawking): the bath sets T_dS = H/2pi and a momentum scale.
  - the roton coefficients alpha (=-s4), beta (=s6) from the self-energy Pi(k).
QUESTION: is k* (=set by alpha,beta) LOCKED to the edge by a bath-set relation, or
do alpha,beta float freely so k* can be anywhere?
""")

# Dimensional analysis. omega^2 = c^2 k^2 - alpha k^4 + beta k^6.
# The self-energy from a thermal bath at T_dS=H/2pi has a SINGLE dimensionful scale H
# (in c=1 units). So on dimensional grounds alpha ~ 1/Lambda_a^2, beta ~ 1/Lambda_b^4,
# and if the ONLY scale the bath injects is H, then Lambda_a ~ Lambda_b ~ H (times
# dimensionless O(1) loop factors). Then k* ~ alpha/beta-ish ~ H.
# So the inflection scale is k* ~ H IF the bath's only scale is H.
H, c = sp.symbols('H c_chi', positive=True)
print("Dimensional structure (bath's only scale = H, in c=1):")
print("  alpha ~ a0 / H^2 ,  beta ~ b0 / H^4   (a0,b0 dimensionless loop coeffs)")
print("  inflection u*=k*^2 solves the cubic; at threshold u* = -2 c2/s4 = 2 c^2/alpha")
print("           => k*^2 = 2 c_chi^2 / alpha ~ 2 c_chi^2 H^2 / a0   => k* ~ (c_chi/sqrt(a0)) H\n")

# The b->c_chi EDGE in k-space. The sonic edge is where the phase velocity omega/k -> c_chi
# from below, OR where group velocity domega/dk -> 0 (the roton minimum). Let's find the
# edge frequency/k where omega^2 -> the marginal point. At threshold s6=s6*, om2(k*)=0,
# so omega(k*)=0: the dispersion touches ZERO at k*. That IS the deepest possible roton
# minimum (a 'sound horizon' where the in-medium mode goes soft).
print("KEY GEOMETRIC FACT (from Part 5): at the no-ghost threshold s6=s6*, the inflection")
print("k* coincides with omega(k*)=0 -- the mode goes SOFT (sound horizon). So 'pin k* at")
print("the edge' <=> 'tune s6 to threshold s6*=alpha^2/(4 c_chi^2)'. The edge-pinning is a")
print("ONE-PARAMETER tuning (s6 = s6*), NOT automatic.\n")

# Is that tuning FORCED by the bath or FREE? Count the inputs.
print("INPUT COUNT:")
print("  - c_chi^2 (k^2 coeff): set by the khronon kinetic term (banked, the sound speed).")
print("  - alpha (=-s4, the k^4 BEND): SIGN FORCED <0 by the dS bath (banked 851e7649,")
print("       sigma4=-I2 c_chi^2<0 forced for any passive bath w/ superluminal deriv coupling).")
print("       MAGNITUDE = I2 c_chi^2 set by the bath spectral moment I2 (a bath number).")
print("  - beta (=s6, the k^6 FLOOR): this is the CS-VIOLATING / active piece. PP: for the")
print("       SMOOTH GH continuum sigma6<0 (CS forces it) => NO floor => ghost. A bounded")
print("       floor s6>=s6* needs the PEAKED QNM resonance (NN's named unbanked input).")
print()
print("=> EDGE-PINNING VERDICT: the bath sets c_chi and alpha (so it sets the SCALE k*~H");
print("   at WHICH a fold would sit), but pinning k* EXACTLY at the soft edge requires");
print("   s6=s6*=alpha^2/(4c_chi^2). That is a CODIMENSION-1 tuning. The bath does NOT")
print("   automatically supply it: the smooth continuum gives s6<0 (PP), the wrong side.")
print("   k*'s SCALE is bath-set (~H); k*'s COINCIDENCE with the edge is NOT bath-forced —")
print("   it needs the peaked QNM whose strength is exactly tuned to hit s6=s6*.")
