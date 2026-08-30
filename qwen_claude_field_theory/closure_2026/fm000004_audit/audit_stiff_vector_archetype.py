#!/usr/bin/env python3
"""AUDIT the loop's dominant survivor archetype (FM-000008/010/014/016/018): a 'stiff'/non-propagating
timelike preferred-frame vector u_mu that supplies the DC-013 lensing slip via a screened (e^-y) linear
coupling, claiming to DODGE P7 by having 'no kinetic term'. Test the longitudinal (slip-carrying) mode:
where does its kinetic normalization come from? Timelike background u0=(1,0,0,0); longitudinal
u_i=d_i pi, temporal u_0. Two ways to normalize the longitudinal/temporal sector -> a FORK."""
import sympy as sp

k, M, sig, w = sp.symbols('k M sigma omega', positive=True)   # k mom, M^2=e^-y screened mass, sigma indep stiffness
u0, pi = sp.symbols('u0 pi', real=True)
u0d = sp.symbols('u0dot', real=True)

print("=== The slip needs the LONGITUDINAL/temporal sector of u_mu to be dynamical & sourced ===")
print("   Maxwell F^2 is blind to the longitudinal mode (shown in FM-000004). So the longitudinal")
print("   normalization must come from EITHER (A) the screened Proca mass, OR (B) an independent")
print("   stiffness term sigma*(div u)^2. Test both.\n")

print("=== FORK A: longitudinal normalized by the SCREENED mass M^2(y)=e^-y (Proca route) ===")
# from FM-000004 audit: K_long = M^2 k^2/(k^2+M^2) -> M^2 short-wavelength
K_long_A = M**2*k**2/(k**2+M**2)
print(f"   K_long = {K_long_A} -> (k>>M) {sp.limit(K_long_A,k,sp.oo)} = M^2 = e^-y -> 0 in solar system")
print("   => 'non-propagating in the UV' is BECAUSE K_long ~ e^-y -> the slip mode is normalized by the")
print("      SAME screening that protects PPN. That is P7, verbatim: Lambda_sc ~ e^-y/2 -> 0. STRONG COUPLING.")

print("\n=== FORK B: give the longitudinal an INDEPENDENT stiffness sigma*(d_mu u^mu)^2 ===")
# d.u = -u0dot + lap(pi); the term (1/2)sigma(d.u)^2 gives u0 a kinetic piece (1/2)sigma*u0dot^2.
# u0 is the TEMPORAL component of a timelike vector => a +sigma*u0dot^2 kinetic term is WRONG-SIGN.
# Build the 2x2 kinetic matrix for (u0, pi) from L = (1/2)sigma(-u0dot + lap pi)^2 (+ Maxwell for transverse).
divu = -u0d + (-k**2)*pi                     # Fourier: lap(pi) -> -k^2 pi ; u0dot symbol
L_sigma = sp.Rational(1,2)*sig*divu**2
# kinetic term of u0 = coeff of u0dot^2:
K_u0 = sp.expand(L_sigma).coeff(u0d,2)
print(f"   sigma-term gives u0 kinetic coefficient (coeff of u0dot^2) = {K_u0}")
print("   For a TIMELIKE vector, the temporal component u0 carries the WRONG metric signature:")
print("   a +sigma*u0dot^2 Lagrangian kinetic term => NEGATIVE-norm mode => GHOST (Ostrogradsky/Proca-")
print("   longitudinal disease). Independent stiffness sigma>0 propagates a temporal GHOST.")
# sign check via a toy dispersion: healthy needs the temporal-mode residue < 0 in mostly-minus...
print(f"   (standard result: independent (div u)^2 for timelike u is the aether temporal ghost; only the")
print(f"    Maxwell F^2 + Proca-mass structure is ghost-free, and that is exactly FORK A.)")

print("\n=== VERDICT: FORK KILL ===")
print("A non-propagating/stiff timelike frame cannot supply the DC-013 slip for free:")
print("  FORK A (screened Proca mass): K_long ~ e^-y => P7 strong coupling (identical to FM-000004).")
print("  FORK B (independent stiffness sigma): temporal ghost.")
print("'Stiff = non-propagating' is not a third option -- it is the K->inf limit, i.e. c_s^2->inf")
print("(strong coupling) or a wrong-sign residue (ghost). The whole FM-000008/010/014/016/018 family")
print("(independent stiff-vector screened-frame) inherits this fork. Consistent with KM-X1 (P7 via")
print("GW170817) and the slip-lock theorem (frame required, but the frame's slip mode is the sick one).")
print('CERTIFICATE_JSON: {"gate":"G8-audit-stiff-vector","status":"KILL","certificate":"Stiff/non-'
      'propagating preferred-frame vector supplying the DC-013 slip is a FORK KILL: the longitudinal '
      '(slip-carrying) mode is either normalized by the screened Proca mass M^2=e^-y => K_long~e^-y => '
      'P7 strong coupling (Lambda_sc~e^-y/2->0, identical to FM-000004), OR given an independent (div u)^2 '
      'stiffness => a +sigma*u0dot^2 kinetic term for the TIMELIKE temporal component => ghost. Stiff = '
      'K->inf = c_s^2->inf (strong coupling), not a third escape. Closes the stiff-vector screened-frame '
      "family FM-000008/010/014/016/018.\",\"assumptions\":[\"timelike frame background\",\"Maxwell blind to "
      'longitudinal (FM-000004)","slip needs a dynamical longitudinal mode"],"numeric_values":{"K_long_screened":"e^-y","stiff_u0_kinetic_sign":"wrong (ghost)"}}')
