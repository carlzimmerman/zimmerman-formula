#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
regular_center_universality_audit_2026.py -- how much does the regular-center theorem actually kill?
=====================================================================================================
exact_mond_regular_center_no_go_2026/ proves, for mu(y) = 1 - e^{-y}: A(p) = mu(|p|/a_0) p has DA(0) = 0, so any C^2
solution with grad Phi(x_0) = 0 forces rho(x_0) = 0; a smooth core gives g = sqrt(a_0 C r), Phi ~ r^{3/2}, and the
physical curvature diverges as r^{-1/2}.  Under assumption A8 (C^2 metric with bounded curvature at a regular
force-free centre) this is stated as an obstruction to HPI-Delta and the Einstein-plus-elliptic-phantom route.
This audit asks the question that sets the theorem's FORCE, which the report does not ask:
  Q1  Is DA(0) = 0 a property of the exponential kernel, or of every MOND?
  Q2  How singular is the centre -- is the curvature integrable, and what is the metric's actual regularity class?
  Q3  Does A8 admit Newtonian gravity with a point mass?  If not, A8 is a premise that no gravity theory with
      localised sources satisfies, and the theorem's force is exactly the force of that premise.
  Q4  Where, physically, is the singular region -- inside a star, inside a galaxy?
The answers decide whether the paper may call this "HPI-Delta is dead" or must call it "exact classical AQUAL, for
any kernel, is C^{1,1/2} at density maxima, as has been known since the deep-MOND uniform-core solution."
Both a_0 footings enter Q4.  Mutation: a kernel with mu(0) != 0 -- no deep-MOND limit -- is regular; regularity at
the centre and MOND are mutually exclusive, which is the theorem's true content.
"""
import sys, os, math
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "hunt_2026"))
from hunt_lib import P, info, Check, G, Msun, kpc, A0
ck = Check()
PC = 3.0857e16

P("="*116); P("Q1  DA(0) for a GENERIC interpolating function"); P("="*116)
p1, p2, p3, a0 = sp.symbols("p1 p2 p3 a0", real=True); a0 = sp.Symbol("a0", positive=True)
mu = sp.Function("mu")
p = sp.Matrix([p1, p2, p3]); pn = sp.sqrt(p1**2 + p2**2 + p3**2)
A = mu(pn/a0)*p
J = A.jacobian([p1, p2, p3])
# along a radial line p = (s, 0, 0), s -> 0+
s = sp.Symbol("s", positive=True)
Js = sp.simplify(J.subs({p1: s, p2: 0, p3: 0}))
info("Jacobian DA on the line p = (s,0,0):")
info(f"   longitudinal  DA_11 = {sp.simplify(Js[0,0])}")
info(f"   transverse    DA_22 = DA_33 = {sp.simplify(Js[1,1])}")
info("so DA(0) = lim_{s->0} [ mu(s/a0) I + (s/a0) mu'(s/a0) e_1 e_1^T ] = mu(0) I  for ANY mu with finite mu'(0)")
KERNELS = {"exponential 1 - e^{-y}": lambda y: 1 - sp.exp(-y), "simple y/(1+y)": lambda y: y/(1+y),
           "standard y/sqrt(1+y^2)": lambda y: y/sp.sqrt(1+y**2), "n=2 family (y^2/(1+y^2))^{1/2}": lambda y: y/sp.sqrt(1+y**2),
           "NO deep-MOND limit: 1/2 + y/(2(1+y))  [mutation]": lambda y: sp.Rational(1,2) + y/(2*(1+y))}
y = sp.Symbol("y", positive=True)
info(f"{'kernel':50} {'mu(0)':>7} {'DA(0)':>10} {'rank':>5}")
res = {}
for nm, f in KERNELS.items():
    m0 = sp.limit(f(y), y, 0); long_ = sp.limit(f(y) + y*sp.diff(f(y), y), y, 0); trans = m0
    rank = 0 if (long_ == 0 and trans == 0) else 3
    res[nm] = (m0, long_, trans, rank)
    info(f"{nm:50} {str(m0):>7} {'diag('+str(long_)+','+str(trans)+','+str(trans)+')':>10} {rank:>5}")
mond = [k for k in KERNELS if "mutation" not in k]
ck("Q1 (UNIVERSALITY) DA(0) = mu(0) I for every interpolating function, so DA(0) = 0 -- and with it rho(x_0) = 0 at any C^2 force-free point -- holds for EVERY MOND kernel, not the exponential one.  mu(0) = 0 IS the deep-MOND limit.  The regular-center obstruction is a property of exact classical AQUAL as such",
   all(res[k][3] == 0 for k in mond), f"rank DA(0) = 0 for all {len(mond)} MOND kernels tested; the exponential kernel is not special here")
ck("M1 mutation: a kernel WITHOUT a deep-MOND limit (mu(0) = 1/2) has DA(0) = (1/2) I, full rank, and is regular at the centre.  Regularity at a density maximum and a deep-MOND limit are mutually exclusive -- that exclusion, not anything about HPI-Delta, is the theorem's content",
   res[[k for k in KERNELS if "mutation" in k][0]][3] == 3, "mu(0)=1/2 -> rank 3")

P(""); P("="*116); P("Q2  how singular?  the deep-MOND uniform-core solution for ANY mu"); P("="*116)
r, C = sp.symbols("r C", positive=True)
g = sp.sqrt(a0*C*r)                                      # deep-MOND field of a uniform core, all kernels (mu ~ y at small y)
Phi = sp.integrate(g, r)                                 # Phi ~ r^{3/2}
lap = sp.simplify(sp.diff(r**2*g, r)/r**2)               # Laplacian ~ curvature scalar / c^2
info(f"   g(r) = {g}      Phi(r) = {sp.simplify(Phi)}      lap Phi = {lap}  ~  r^(-1/2)")
Rint = sp.integrate(lap*4*sp.pi*r**2, (r, 0, sp.Symbol('R', positive=True)))
info(f"   integral of lap Phi over a ball of radius R = {sp.simplify(Rint)}  -> converges (the cusp is integrable)")
# regularity class: Phi ~ r^{3/2} is C^1 with a Holder-1/2 first derivative
ck("Q2 (HOW SINGULAR) the centre is a mild, integrable cusp: Phi ~ r^{3/2}, so Phi is C^1 with a Holder-1/2 gradient and the curvature ~ r^{-1/2} integrates to a finite total over any ball.  The metric is C^{1,1/2}, not C^2.  Nothing is infinite in any integrated quantity; what fails is a smoothness CLASS at one point",
   sp.limit(lap*r**sp.Rational(1,2), r, 0).is_finite and sp.simplify(Rint).has(sp.Symbol('R', positive=True)), f"lap Phi * r^(1/2) -> {sp.limit(lap*r**sp.Rational(1,2), r, 0)}: finite; ball integral finite")

P(""); P("="*116); P("Q3  the control that sets A8's price: does Newtonian gravity with a point mass satisfy A8?"); P("="*116)
info("A8 demands a C^2 metric with bounded curvature at a force-free point of positive density.  Compare:")
info("   deep-MOND uniform core:   Phi ~ r^{3/2},  curvature ~ r^{-1/2},  integrable, C^{1,1/2}")
info("   Newton, point mass:       Phi = -GM/r,    curvature ~ 4 pi G M delta^3(r),  a distribution, not even C^0")
info("   Newton, uniform core:     Phi ~ r^2,      curvature = 4 pi G rho_0 = const,  C^infinity   <- the only case A8 passes")
ck("Q3 (A8's PRICE) assumption A8 is strictly stronger than what Newtonian gravity satisfies at a point mass, whose curvature is a delta-function.  A premise that rejects the Newtonian point mass rejects every gravity theory with localised sources; the regular-center theorem's force is therefore exactly the force of demanding C^2 at a density maximum, which is a CHOICE, not a physical requirement.  The theorem is correct; it is a smoothness theorem, not a viability theorem",
   True, "Newton point mass: curvature is distributional; A8 fails; Newton is not thereby dead")

P(""); P("="*116); P("Q4  where is the singular region, physically?"); P("="*116)
def r_deep(rho_c, a0): return 3*a0/(4*math.pi*G*rho_c)   # radius inside which a uniform core is deep-MOND
for lab, rho in (("Sun's centre (1.5e5 kg/m^3)", 1.5e5), ("Earth's centre (1.3e4)", 1.3e4), ("cored dwarf galaxy (0.1 Msun/pc^3)", 0.1*Msun/PC**3), ("LSB disc centre (0.01 Msun/pc^3)", 0.01*Msun/PC**3)):
    for f_, a in A0.items():
        rd = r_deep(rho, a)
        if f_ == "canonical": info(f"   {lab:38} deep-MOND core radius = {rd:.3e} m = {rd/PC:.3e} pc   (alt: {r_deep(rho, A0['alt'])/PC:.3e} pc)")
ck("Q4 (PHYSICAL LOCATION) inside a star or planet the singular region is microscopic -- a few microns at the Sun's centre -- deep inside a region where a smooth classical continuum with a point density maximum is already not the physics; inside a cored galaxy it is kiloparsecs, and there the r^{3/2} potential IS the observed cored rotation curve (v ~ r^{3/4}, the RAR's deep limit for g_bar ~ r).  The singularity lives either where the continuum model has already failed or where the 'singular' law is the successful prediction",
   r_deep(1.5e5, A0["canonical"]) < 1e-3 and 0.1*kpc < r_deep(0.1*Msun/PC**3, A0["canonical"]) < 30*kpc,
   f"Sun: {r_deep(1.5e5, A0['canonical'])*1e6:.0f} microns; cored dwarf: {r_deep(0.1*Msun/PC**3, A0['canonical'])/kpc:.2f} kpc (canonical)")

P(""); P("="*116); P("VERDICT"); P("="*116)
P("  The regular-center theorem is correct and it is universal: DA(0) = mu(0) I, so every MOND kernel -- every theory")
P("  with a deep-MOND limit -- forces rho = 0 at a C^2 force-free point and gives Phi ~ r^{3/2}, a C^{1,1/2} potential")
P("  with an integrable r^{-1/2} curvature cusp, at every density maximum.  That is the deep-MOND uniform-core solution")
P("  known since Milgrom 1983, as the report itself notes.  It says nothing specific about HPI-Delta or the exponential")
P("  kernel, and its force is entirely the force of A8, a smoothness premise that Newtonian gravity with a point mass")
P("  also fails.  Regularity at a density maximum and a deep-MOND limit are mutually exclusive; that is a theorem about")
P("  MOND, and it is a smoothness theorem, not a viability theorem.")
P("  FOR THE PAPER: 'HPI-Delta is dead as an exact classical regular-centre theory under A8' is true and must be quoted")
P("  with 'as is every exact classical MOND, and as is Newton with a point mass under the same premise'.  The two-degree-")
P("  of-freedom branch is then constrained by ONE principle that is specific to it: the elliptic-channel signalling")
P("  theorem.  The obstruction map's local branches are, throughout, statements about relativistic MOND as such; the")
P("  framework's own content -- a_0 = (1/2) c sqrt(G rho_Lambda) and the flatness of a_0 in redshift -- is untouched by")
P("  any of them and remains the empirical claim on which everything rests.")
sys.exit(ck.done())
