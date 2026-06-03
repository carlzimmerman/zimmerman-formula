#!/usr/bin/env python3
"""
Deriving Z = 2 sqrt(8 pi/3) = 5.789 from first principles -- how far each route gets.
====================================================================================
a0 = (c/2) sqrt(G rho) = c H(z)/Z,   Z = 2 sqrt(8 pi/3).
Z factorises as  Z = 2 x sqrt(8 pi/3), and the two factors are NOT the same kind of object:
  * sqrt(8 pi/3) = 2.894  is EXACT (Friedmann); it is the H <-> sqrt(G rho) conversion.
  * the 2         is the O(1) coefficient -- THIS is the whole game.
So "derive Z" == "derive the factor of 2 in a0=(c/2)sqrt(G rho)". We work every route and
compute what each yields, then say honestly which (if any) is forced. No number is rigged.
"""
import numpy as np

c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
TARGET = 2*np.sqrt(8*np.pi/3)
print("="*84)
print(f"TARGET:  Z = 2 sqrt(8pi/3) = {TARGET:.4f}   <=>   a0 = (c/2) sqrt(G rho)")
print("="*84)

# ---- the data only pins Z to a BAND (so 'exactly 5.79' is not even data-required) ----
print("\n[0] What the data actually allows (Z = c H0 / a0):")
print(f"    {'H0':>6}{'a0[e-10]':>10}{'Z=cH0/a0':>11}")
band = []
for H0 in (67.4, 70.0, 73.0):
    H0s = H0*1e3/Mpc
    for a0 in (1.10e-10, 1.20e-10):
        Z = c*H0s/a0; band.append(Z)
        print(f"    {H0:>6}{a0*1e10:>10.2f}{Z:>11.2f}")
print(f"    => data allows Z in [{min(band):.2f}, {max(band):.2f}].  So 2sqrt(8pi/3)=5.79,")
print(f"       Verlinde 6, and Milgrom 2pi=6.28 are ALL consistent. Data cannot pick one.")

# ---- STEP 1: the sqrt(8pi/3) is exact, IF a0 tracks the gravitational rate sqrt(G rho) ----
print("\n"+"="*84)
print("[1] The sqrt(8pi/3): EXACT (not a posit) -- but it encodes a physical CHOICE")
print("="*84)
print("    Friedmann (flat):  H^2 = (8 pi G/3) rho  =>  sqrt(G rho) = H sqrt(3/8pi).")
print(f"    So if a0 = K * sqrt(G rho), then a0 = K H sqrt(3/8pi) = cH/Z with Z = c/(K) sqrt(8pi/3).")
print(f"    The CHOICE is to set a0 by the Newtonian free-fall rate sqrt(G rho) (local gravity,")
print(f"    sourced by density) rather than the expansion rate H. That choice is physical:")
print(f"    a0 is a LOCAL gravitational acceleration, so the local source-rate sqrt(G rho) is the")
print(f"    natural clock. GRANT that, and sqrt(8pi/3)={np.sqrt(8*np.pi/3):.3f} is forced. [DERIVED, given the choice]")

# ---- STEP 2: the factor of 2 -- the actual content ----
print("\n"+"="*84)
print("[2] The factor of 2 in a0=(c/2)sqrt(G rho): every route, computed")
print("="*84)
sqrt83 = np.sqrt(8*np.pi/3)
routes = [
    ("simplest horizon: c^2/a0 = c/sqrt(Grho) (Rindler hor. = free-fall light-cross)",
     1.0*sqrt83, "K=c -> a0=c sqrt(Grho); NO factor 2 -> Z=sqrt(8pi/3)=2.89 -> a0=2.3e-10 RULED OUT"),
    ("FRAMEWORK: c^2/a0 = 2 c/sqrt(Grho)  (horizon = 2x free-fall length)",
     2.0*sqrt83, "K=c/2 -> a0=(c/2)sqrt(Grho) -> Z=5.79 -> a0=1.13e-10  MATCHES"),
    ("surface gravity of a horizon: kappa=c^2/(2R) (the Schwarzschild/Rindler 1/2)",
     2.0*sqrt83, "the 1/2 in kappa=c^2/2R IS the factor -> same K=c/2 -> Z=5.79"),
    ("free-fall clock: v gained over t_g=1/sqrt(Grho) equals c/2",
     2.0*sqrt83, "a0 t_g = c/2 -> a0=(c/2)sqrt(Grho) -> Z=5.79 (but 'why c/2' = the posit)"),
]
print(f"    {'route':70}{'Z':>7}")
for name, Z, note in routes:
    print(f"    {name:70}{Z:>7.2f}")
    print(f"        -> {note}")

print("\n    The three routes that give 5.79 all rest on ONE unproven step: a coefficient 1/2")
print("    (Rindler-horizon = 2x the free-fall length / surface-gravity 1/2 / 'v=c/2'). The")
print("    SIMPLEST horizon condition gives NO 2 (Z=2.89), which the data kill. So the 2 is")
print("    DATA-REQUIRED given the sqrt(Grho) form, and MOTIVATED by surface gravity, but it is")
print("    NOT uniquely derived: nothing forbids the coefficient 1 (ruled out) or 1/pi etc.")

# ---- STEP 3: the entropy routes give DIFFERENT numbers (so they are not THIS Z) ----
print("\n"+"="*84)
print("[3] Why the horizon-ENTROPY routes do not give 2sqrt(8pi/3)")
print("="*84)
print(f"    Unruh = de Sitter temperature (Milgrom):  2 pi a0 = cH  ->  Z = 2pi = {2*np.pi:.3f}")
print(f"    de Sitter horizon entropy (Verlinde):     Z ~ 6 (rational)         = 6.000")
print(f"    framework (Newtonian free-fall rate):     Z = 2 sqrt(8pi/3)        = {TARGET:.3f}")
print( "    These come from DIFFERENT principles (horizon entropy vs Newtonian collapse) and give")
print( "    DIFFERENT numbers in DIFFERENT number-fields (transcendental 2pi, rational 6, surd")
print( "    2sqrt(8pi/3)). So an entropy argument CANNOT output exactly 2sqrt(8pi/3): the framework's")
print( "    Z lives on the Newtonian-rate route, where the 2 is surface-gravity, not entropy.")

# ---- VERDICT ----
print("\n"+"="*84)
print("VERDICT -- honestly, how far the derivation gets")
print("="*84)
print(f"""  Z = 2 x sqrt(8pi/3):
   * sqrt(8pi/3) = {sqrt83:.3f}  is EXACT (Friedmann), once you posit a0 ~ sqrt(G rho) -- i.e.
     that the MOND scale is set by the local gravitational free-fall rate. [DERIVED given the form]
   * the 2 is a surface-gravity / Rindler-horizon coefficient: it is DATA-REQUIRED (the no-2
     version Z=2.89 is ruled out 2x) and MOTIVATED (the 1/2 in kappa=c^2/2R, in v_avg, in 1/2 k T),
     but it is NOT uniquely DERIVED -- no principle here forbids a neighbouring O(1). [POSIT, motivated]
   * and current data allow Z in ~[5.5,6.5], so 5.79 is NOT even distinguishable from 6 or 2pi.
  HONEST BOTTOM LINE: Z is HALF-DERIVED. The cleanest true statement is
       a0 = (c/2) sqrt(G rho)  =  (relativistic horizon factor c/2) x (Newtonian free-fall rate),
  one exact factor and one motivated O(1). To make it a real DERIVATION you must supply a single
  principle that FORCES the 1/2 (e.g. a horizon/equipartition theorem) AND predicts no neighbouring
  value -- that is the open problem, and it is honest physics, not numerology, to state it as open.""")
print("="*84)
