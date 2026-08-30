#!/usr/bin/env python3
"""VERIFY the reviewer's helicity-0/Galileon MOND-scaling no-go (verify a kill as hard as a win).
Claim: HR decoupling-limit helicity-0 (finite Galileon polynomial) cannot realize the MOND deep-field
law. Reviewer said 'both exponent conditions require n=3/2' -- CHECK THIS: it contains a slip, and the
correct statement is STRONGER."""
import sympy as sp

n = sp.symbols('n', positive=True)
# If the n-th Galileon term dominates: E^n ~ GM/r^3, E=pi'/r  =>  a_pi ~ r*E ~ (GM)^{1/n} r^{1-3/n}
mass_exp   = sp.Rational(1,1)/n          # exponent of (GM)
radius_exp = 1 - 3/n                     # exponent of r
# MOND: a = sqrt(GM a0)/r  =>  mass exponent 1/2, radius exponent -1
sol_mass   = sp.solve(sp.Eq(mass_exp, sp.Rational(1,2)), n)
sol_radius = sp.solve(sp.Eq(radius_exp, -1), n)
print(f"mass-scaling condition  M^(1/n)=M^(1/2)  =>  n = {sol_mass}")
print(f"radius-scaling condition r^(1-3/n)=r^-1  =>  n = {sol_radius}")
print(f"=> the reviewer's 'both require n=3/2' has a SLIP (mass gives n=2), and the truth is STRONGER:")
print(f"   the two conditions are MUTUALLY INCONSISTENT -- NO single power n (integer OR fractional)")
print(f"   can give the MOND deep limit from one dominant polynomial term.")
# cross-check the famous cubic-galileon Vainshtein case n=2: a ~ M^(1/2) r^(-1/2) (known result)
print(f"   check n=2 (cubic galileon): a ~ M^({sp.Rational(1,2)}) r^({1-sp.Rational(3,2)}) -- the known "
      f"M^1/2 r^-1/2 Vainshtein form, NOT MOND's r^-1.")

print("\n=== second, independent obstruction: REGIME INVERSION ===")
# Galileon nonlinearities dominate at LARGE E (small r, near source) -> screening INWARD (Vainshtein).
# MOND's nonlinearity g^2/a0 must dominate at SMALL g (large r) -> modification OUTWARD.
E, r_, GM, a0 = sp.symbols('E r GM a0', positive=True)
E_of_r = (GM/r_**3)              # E ~ GM/r^3 in linear regime: E GROWS toward the source
print(f"   E ~ GM/r^3 grows as r->0: polynomial terms E^n dominate NEAR the source (screening inward).")
print(f"   MOND needs the nonlinear branch to dominate FAR from the source (g<a0, enhancement outward).")
print(f"   => the Galileon hierarchy activates in exactly the WRONG regime. Structural, not a coefficient.")

print("\n=== third: the exact kernel needs an INFINITE constitutive hierarchy ===")
y = sp.symbols('y', positive=True)
mu = 1 - sp.exp(-y)
ser = sp.series(y*mu, y, 0, 5)
print(f"   y*mu(y) = {ser}  -- an INFINITE alternating hierarchy (e^-y resummation).")
print(f"   Ghost-free 4D decoupling limit fixes a FINITE Galileon polynomial (quartic max) with tied")
print(f"   coefficients; it cannot resum into 1-e^-y. (dRGT/HR decoupling limit is rigid.)")

print("\nVERDICT: DC-015 BIMETRIC_HEL0_GALILEON -- standard ghost-free HR decoupling-limit helicity-0")
print("cannot realize the MOND deep limit: (i) exponent conditions mutually inconsistent (n=2 vs 3/2),")
print("(ii) nonlinearities activate in the inverted regime (screen inward vs enhance outward),")
print("(iii) finite rigid polynomial cannot resum the exponential kernel. Scope: standard ghost-free")
print("Galileon/decoupling architecture ONLY -- not all scalar-bimetric constructions (degenerate/")
print("DHOST-like two-metric interactions remain open).")
print('CERTIFICATE_JSON: {"gate":"DC-015","status":"DEAD-CLASS","certificate":"HR helicity-0 Galileon '
      'cannot make MOND: mass-scaling needs n=2, radius-scaling needs n=3/2 (mutually inconsistent -- '
      'stronger than the reviewer n=3/2 slip); regime inverted (Vainshtein screens inward, MOND enhances '
      'outward); finite rigid polynomial cannot resum 1-e^-y. Scope: standard ghost-free decoupling-limit '
      'architecture only.","assumptions":["single dominant polynomial term asymptotics","4D ghost-free '
      'decoupling limit rigidity"],"numeric_values":{"n_mass":2,"n_radius":1.5}}')
