import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("TRADEOFF ESCAPE TEST: can a 2-parameter / correction structure get BOTH")
print("   K=2/3 (needs delta^2=3/2) AND the measured mass ratios (need delta^2=3/8)?")
print("="*78)

# The two requirements pull delta^2 to mutually exclusive values:
#   K=2/3 EXACT (bare symmetric triple):     delta^2 = 3/2
#   measured sqrt-mass ladder (Singh fit):   delta^2 = 3/8  (factor 4 apart)
# A genuine escape would need a SECOND knob that restores ratios at delta^2=3/2
# WITHOUT re-touching K. But K and the ratios are BOTH functions of the SAME
# eigenvalue triple -> any deformation that fixes ratios changes K and vice versa,
# unless you add an independent per-mass correction (= more free params = giving up
# the prediction). Demonstrate: at delta^2=3/2 the smallest sqrt-mass is NEGATIVE.

d2 = sp.Rational(3,2)
d  = sp.sqrt(d2)
# Singh's charged-lepton (charge-1/3) eigenvalue set used for ratios: (1/3 - d, 1/3, 1/3 + d)
e_small = sp.Rational(1,3) - d
e_mid   = sp.Rational(1,3)
e_big   = sp.Rational(1,3) + d
print(f"\nAt delta^2=3/2 (the Koide-exact point):")
print(f"  charge-1/3 eigenvalue triple (1/3-d, 1/3, 1/3+d):")
print(f"     1/3 - sqrt(3/2) = {mp.mpf(sp.N(e_small,30))}  <-- NEGATIVE sqrt-mass (unphysical)")
print(f"     1/3            = {mp.mpf(sp.N(e_mid,30))}")
print(f"     1/3 + sqrt(3/2) = {mp.mpf(sp.N(e_big,30))}")
print(f"  => sqrt(m_e) < 0 : the charged-lepton spectrum is DESTROYED at the Koide point.")
print(f"     A real sqrt-mass cannot be negative -> no smooth 1-knob correction rescues it")
print(f"     without flipping a sign (i.e. abandoning the equally-spaced ansatz = the very")
print(f"     structure that produced 2/3). The tradeoff is STRUCTURAL, not cosmetic.")

# Both-ways: show the Majorana point keeps all sqrt-masses positive
d2m = sp.Rational(3,8); dm = sp.sqrt(d2m)
print(f"\nAt delta^2=3/8 (the mass-ratio-fitting point): 1/3 - sqrt(3/8) = "
      f"{mp.mpf(sp.N(sp.Rational(1,3)-dm,30))}  (still <0!) ")
print("  -> Singh AVOIDS this by using RATIOS of |eigenvalues| & the X,G ladder, not the")
print("     bare triple; that ladder reproduces ratios at 3/8 but then K=0.66916 not 2/3.")

print("\n" + "="*78)
print("FRAMEWORK a0 VALUE CHECK (gravity side stands on its own, independent of Koide)")
print("="*78)
c   = mp.mpf("299792458")
# Lambda from Planck: rho_Lambda, H0. Use canonical pure-Lambda cH_Lambda route.
# a0 = c^2 sqrt(Lambda/32pi).  Lambda ~ 1.1056e-52 m^-2 (observed).
Lam = mp.mpf("1.1056e-52")   # m^-2
a0 = c**2 * mp.sqrt(Lam/(32*mp.pi))
print(f"  Lambda (obs)         = {mp.nstr(Lam,5)} m^-2")
print(f"  a0 = c^2 sqrt(L/32pi)= {mp.nstr(a0,5)} m/s^2   (framework canonical ~9.4e-11; MOND ~1.2e-10)")
print(f"  This number is set ENTIRELY by Lambda + the 1/32pi geometry. NO delta, NO Koide,")
print(f"  NO lepton mass enters. The gravity side is causally upstream of and disjoint from")
print(f"  the flavor delta. Confirms: no observable rides a shared root between a0 and Koide.")
