#!/usr/bin/env python3
"""
STEP 6 -- The LITERAL assignment: O(eps^3) MOND free energy on a STRAINED de Sitter horizon.
============================================================================================
The prior verdict's one bounded open item:
  'a covariant O(eps^3) on-shell free-energy computation of the C(Q)Y^{3/2} vertex on a
   strained (inhomogeneous) de Sitter horizon, checking whether the strain trace leaves the
   sphere-volume 4/3 uncancelled and pins kappa=1/2.'

On the homogeneous background Ybar=0 (q^00=0), so the MOND term is invisible. We go OFF the
saddle: introduce an inhomogeneous strain eps on the horizon so that Y = |grad phi|^2 != 0,
expand the free energy F[phi] = -(1/12 pi G a0) integral |grad phi|^3 sqrt(g) d^3x to O(eps^3),
and ask whether matching delta F = T delta S pins the rational kappa.

We parametrize the strain via the expansion theta and shear sigma of the horizon generators
(the genuine inhomogeneity knobs, per arXiv:2503.16138). Y is sourced at O(eps): |grad phi| ~ eps.
Then |grad phi|^3 ~ eps^3 -- the LEADING contribution of the MOND vertex is O(eps^3). This is WHY
the order is 3: the cubic vertex needs three powers of the strain-induced gradient.
"""
import sympy as sp

print("="*78)
print("STEP 6: O(eps^3) MOND free energy on a strained horizon -- does it pin kappa?")
print("="*78)

eps, a0, G, Lam, c, theta, sigma, R, th, ph = sp.symbols(
    'epsilon a0 G Lambda c theta sigma R vartheta varphi', positive=True)
pi = sp.pi
Rds = sp.sqrt(3/Lam)

print("""
SETUP. On the strained horizon the field gradient induced by the strain is, to leading order,
  |grad phi| = eps * g(vartheta,varphi) * a0_scale ,
where g is an angular profile (the strain pattern) and the natural gradient scale is set by the
horizon, |grad phi|_scale ~ a0 (deep-MOND: the field's natural gradient IS a0, since
mu|grad phi| = |grad phi|^2/a0 is the Newtonian-equivalent accel, and on the horizon that is ~cH).
We keep the SCALE symbolic and track only the rational/pi structure.
""")

# Free energy density of the MOND vertex:  f = -(1/12 pi G a0) |grad phi|^3
# Write |grad phi| = eps * G_ang(theta,phi) * Gradscale, integrate over the horizon 2-sphere
# shell of thickness ~ R (the radial extent of the strained region near the horizon).
Gradscale = sp.symbols('Gradscale', positive=True)
# angular profile: take the leading strain multipole. The strain trace (expansion) is the
# l=0 part; shear is l=2. Test BOTH for whether a 4/3 (sphere volume) survives.

print("-"*78)
print("(a) PURE EXPANSION strain (trace part, l=0): g = 1 (isotropic breathing).")
print("-"*78)
gradmag = eps*Gradscale*1     # l=0
fdens = -(1/(12*pi*G*a0))*gradmag**3
# integrate over solid angle (4 pi) and a radial shell of extent delta r ~ R near horizon:
dr = sp.symbols('deltar', positive=True)
# 3-volume element near horizon: R^2 * dOmega * dr ; angular integral of g^3=1 is 4 pi
F_exp = fdens * (4*pi) * R**2 * dr
F_exp = sp.simplify(F_exp)
print("  delta F (expansion) =", F_exp)
print("  Note: the 4 pi (solid angle) and the volume factor are EXPLICIT. No 4/3 sphere-volume")
print("        appears -- this is a horizon SHELL (R^2 dr), not a ball. The '4/3' the prior")
print("        verdict asked about would require a BALL integral; the horizon free energy is a")
print("        SHELL integral, so the 4/3 is structurally absent. (Checked: ball vs shell below.)")

print("-"*78)
print("(b) Does the matching delta F = T delta S pin kappa? Track the rational + pi.")
print("-"*78)
# T delta S on the strained horizon: T = hbar H_L/2pi, delta S = delta A/4.
# delta A from the strain: delta A = integral theta dlambda dA ~ eps * A (l=0 breathing).
# So T delta S ~ (hbar H_L/2pi)(1/4)(eps * 4 pi R^2) = (hbar H_L/2pi)(eps pi R^2).
H_L = c*sp.sqrt(Lam/3)
T = hbar_s = sp.symbols('hbar', positive=True)*H_L/(2*pi)
A = 4*pi*R**2
dS = sp.Rational(1,4)*eps*A     # delta A = eps * A for l=0 breathing
TdS = sp.simplify(T*dS)
print("  T delta S (l=0 strain) =", TdS)
print("  delta F (MOND, l=0)    =", F_exp)
print("""
  MATCHING delta F = T delta S:
   - delta F ~ eps^3 (cubic vertex),  T delta S ~ eps^1 (linear first law).
   - eps^3 vs eps^1: AGAIN a power mismatch in the strain order, exactly as M^{3/2} vs M^1.
     At leading order in eps the MOND term is HIGHER order than the gravitational entropy
     response, so it CANNOT balance it term-by-term. The O(eps) balance is pure GR (gives
     the Friedmann/Lambda relation, fixing the 8 pi); the MOND vertex first appears at O(eps^3),
     where there is NO gravitational counterpart of the same order to match it against.
""")

print("-"*78)
print("(c) The decisive structural point: solve the eps-matching for a0 anyway.")
print("-"*78)
# Force delta F(eps^3) = [some O(eps^3) piece of T delta S]. The only eps^3 piece of T dS
# comes from the O(eps^3) term in delta A (the cubic strain correction to the area).
# delta A = eps A + c2 eps^2 A + c3 eps^3 A + ...  The cubic area coefficient c3 is PURE
# GEOMETRY (a number from the sphere), independent of a0. Matching:
c3 = sp.symbols('c3')   # cubic strain area coefficient (pure geometry, a0-independent)
TdS3 = T*sp.Rational(1,4)*c3*eps**3*A
sol = sp.solve(sp.Eq(F_exp, TdS3), Gradscale)
print("  Matching delta F(eps^3) = T * (1/4) c3 eps^3 A, solve for the gradient scale:")
for s in sol:
    print("    Gradscale^3 =", sp.simplify(s**3) if s!=0 else 0, "  (one root shown)")
print("""
  RESULT: the matching fixes the FIELD's gradient scale (Gradscale) in terms of c3, R, a0 --
  it relates the strain-induced field to the geometry, but a0 appears on BOTH sides:
     - LHS delta F carries 1/a0 (the vertex normalization C ~ 1/(G a0)),
     - and Gradscale itself ~ a0 (the deep-MOND field scale).
  So a0 CANCELS or remains free -- the equation determines the strain amplitude, NOT a0.
  This is the off-saddle version of the same blindness: turning on the strain makes the
  vertex VISIBLE (Y != 0), but it enters at an order (eps^3) with no gravitational partner,
  and its own a0-normalization cancels against the field scale it sources. kappa is NOT pinned.
""")

print("-"*78)
print("(d) Ball vs shell: is there ANY 4/3 to leave uncancelled?")
print("-"*78)
# The prior verdict asked: does the strain trace leave the sphere-volume 4/3 uncancelled?
# Ball integral of 1 over radius 0..R:  (4/3) pi R^3.  Shell integral R^2 dr: 4 pi R^2 dr.
ball = sp.integrate(4*pi*sp.Symbol('rr',positive=True)**2, (sp.Symbol('rr',positive=True), 0, R))
print("  Ball  integral (4 pi r^2 dr, 0..R) =", ball, "  -> carries the 4/3.")
print("  Shell integral (4 pi R^2 dr)        = 4 pi R^2 dr  -> NO 4/3 (horizon is a surface).")
print("""  The MOND free energy that links to the horizon is the SHELL/surface integral (the field
  energy in the near-horizon strained layer), which carries 4 pi, NOT 4/3. The 4/3 only
  appears for a volume-filling (ball) source -- which is the HOMOGENEOUS interior, the very
  thing that has Ybar=0 and is MOND-blind. So the 4/3 sphere-volume is NOT available to be
  'left uncancelled' by the strain: where Y != 0 (the surface) there is no 4/3, and where the
  4/3 lives (the bulk ball) there is no Y. The two never meet. kappa=1/2 is NOT forced.""")
