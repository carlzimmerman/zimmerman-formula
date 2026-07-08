#!/usr/bin/env python3
r"""
ADVERSARIAL REFUTATION PROBE of the passive-frame reading.
LENS: is 'u^mu is a passive horizon-anchored constraint' a GENUINE well-posed structure in a
LOCAL, diff-covariant theory, or was passivity ASSERTED, not demonstrated?

Three distinct attacks, each testing whether the compute swept dynamics under the rug.
"""
import sympy as sp

def H(t): print("\n"+"="*90+"\n "+t+"\n"+"="*90)

# =========================================================================================
H("ATTACK 1 -- Does the MOND phenomenology need u to RESPOND LOCALLY? (the E1 global-frame gap)")
# =========================================================================================
print(r"""
 The compute's E1 escape: 'u^mu = the cosmological rest frame, dynamically selected like the CMB
 frame in LCDM, 0 new dof'. This is a GLOBAL/cosmological direction (partial_t of FRW).

 But look at the framework's OWN kernel argument. Theory paper (line 102):
   'a body's inertia depends on its recent acceleration HISTORY ... encoded by a history kernel
    theta(y) entering A = a_internal + theta(y) a_external, y = omega_ext/omega_int.'
 And the covariantization the compute uses:  K(Box_u / a0^2),  Box_u = u^a grad_a (u^b grad_b .).

 The MOND effect is set by the LOCAL proper acceleration a = |a_mu| of the BODY, a_mu = u^b grad_b u_mu
 along the BODY'S worldline -- NOT the cosmological comoving direction. In deep MOND the galaxy's
 stars have proper acceleration ~a0 pointing at the galaxy center: a LOCAL, position-dependent,
 matter-sourced direction that is DIFFERENT at every point and DIFFERENT from the FRW comoving u.

 THE CRACK: if u^mu is FROZEN to the global cosmological rest frame (E1, 0 dof), then u^b grad_b u_mu
 (the four-acceleration that FEEDS Box_u and hence the MOND) is the acceleration of the COSMOLOGICAL
 flow -- ~cH_Lambda everywhere, isotropic -- NOT the local galactic field. A globally-frozen u
 CANNOT carry the local, anisotropic, matter-sourced acceleration that the RAR/MOND requires.
""")
# Symbolic witness: four-acceleration of the FRW comoving frame is isotropic/Hubble, not the local field.
# In FRW, u = (partial_t), geodesic comoving observers have a_mu = u^b nabla_b u_mu = 0 (comoving = geodesic).
# So a globally-frozen comoving u gives ZERO proper acceleration -> Box_u acting through u's own accel = 0.
print(" Fact (GR): FRW comoving observers are GEODESIC => their four-acceleration a_mu = u^b nabla_b u_mu = 0.")
print("   => if u is frozen to the cosmological comoving frame, the frame's OWN acceleration is 0 everywhere.")
print("   => the MOND-sourcing acceleration must come from the BODY moving RELATIVE to u, i.e. from the")
print("      body's velocity/acceleration w.r.t. u -- which is a MATTER-worldline quantity, fine, BUT the")
print("      form factor K(Box_u) with Box_u built from u^a grad_a then needs u to DEFINE the split, and")
print("      the SAME operator must reproduce the LOCAL galactic field at each point.")
print("""
 VERDICT ATTACK 1: The E1 'frozen cosmological u' is INSUFFICIENT to source LOCAL RAR/MOND on its own
 -- but that does NOT force u to be dynamical. The local acceleration lives in the MATTER worldline
 (body relative to the passive u), exactly as the paper's algebraic law g_bar=G(a) uses the body's own
 |a|. So Attack 1 does NOT force aether dynamics. It DOES show E1's phrase 'reproduce ALL its
 phenomenology with frozen u' is glib: the phenomenology is carried by MATTER relative to u, which is
 what the paper actually says. NOT a refutation by itself -- but see Attack 2.
""")

# =========================================================================================
H("ATTACK 2 -- The paper's OWN formulation is a NON-covariant algebraic law; the covariant")
print(   " S_matter = -1/2 rho u K(Box_u) u is a SEPARATE object the paper does NOT commit to.")
# =========================================================================================
print(r"""
 Decisive textual fact (theory paper, line 92):
   'As an ALGEBRAIC state law g_bar = G(a) -- a constitutive closure like p=p(rho) -- the eom is the
    ordinary second-order xddot = sqrt(g_bar^2 + g_bar a0). There is no acceleration inside the LAW,
    hence NO higher-derivative ghost; this is precisely how the theory EVADES THE LOCAL-GATING TRAP
    (gating inertia by |a| in the ACTION would put xddot in the Lagrangian and produce a ghost;
    an equation of state does not).'

 So the FRAMEWORK'S OWN WRITTEN theory is:
   (a) a worldline/point-particle ALGEBRAIC constitutive law, NOT a local covariant field action, and
   (b) it EXPLICITLY WARNS that putting the acceleration-dependence into a Lagrangian (an ACTION with
       Box acting on fields) reintroduces the Ostrogradsky ghost -- the very 'local-gating trap'.

 The compute's covariant object S_matter = -(1/2) rho_m u^mu K(Box_u/a0^2) u_mu is an
 INFINITE-DERIVATIVE action (Box_u appears to all orders inside K). By the paper's OWN warning, THIS
 is the construction that risks the ghost the algebraic law was designed to avoid. The compute even
 CONCEDES this (applicability.py Part 6; constraint_analysis was scoped to 2-point): K has branch
 points at z=0,-1/4, is NOT entire, so it is NOT automatically Barvinsky/Biswas-Mazumdar ghost-free.

 => The 'passive frame is well-posed' claim is established only for the 2-point / principal-symbol
 truncation of an object (a) the paper does not adopt and (b) that lives in exactly the derivative-in-
 action regime the paper flags as the ghost trap. The all-orders Cauchy problem + ghost-freedom is
 OPEN by the compute's own admission.
""")
z = sp.symbols('z')
K = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z))
print(" K(z) branch points (where 1+4z=0 and z=0):  z = -1/4 and z = 0 (sqrt branch)")
print("   K entire?  NO (two branch points) => Biswas-Mazumdar entire-function ghost-free theorem does")
print("   NOT apply. Ghost-freedom of the full tower is NOT established. (compute's own caveat).")

# =========================================================================================
H("ATTACK 3 -- Is a khronon/vector with NO kinetic term (E2) actually WELL-POSED, or degenerate?")
# =========================================================================================
print(r"""
 E2 escape: 'a minimal unit-norm khronon constraint lambda(u.u+1), Hessian carries no derivatives of
 u, hence no kinetic term, no propagating dof.' The compute reads this as HEALTHY (no strong coupling).

 ADVERSARIAL READING: a field that appears in the action with NO kinetic (2-derivative) term and only
 an algebraic constraint + a coupling to matter is NOT automatically healthy -- it can be
 CONSTRAINT-DEGENERATE. Two failure modes the compute did not rule out:

  (i) If u (via T) appears in S_matter through Box_u (derivatives of u), then even WITHOUT an explicit
      c_i(grad u)^2 aether term, the MATTER COUPLING itself generates grad-u terms in the u-EOM
      delta S_matter/delta u. The u equation of motion is then NOT vacuous -- it is
          delta S_matter/delta u^mu + 2 lambda eta_mu_nu u^nu = 0,
      an ALGEBRAIC-looking equation whose delta S_matter/delta u CONTAINS DERIVATIVES OF u (because
      Box_u does). This is an induced kinetic structure for u -- a 'kinetic term through the matter
      coupling', precisely the thing the pure-constraint counting missed.
  (ii) A Lagrange-multiplier vector with the multiplier's OWN eom p_lambda=0 and NO kinetic term for u
      gives a system where u is fixed pointwise by matter -- if delta S_matter/delta u is degenerate
      (non-invertible for u), the constraint does NOT determine u and the Cauchy problem is ILL-POSED
      (constraint does not close / infinite secondary tower). The compute asserted C2 is 'definitional'
      and closes trivially, but that is true ONLY if u is genuinely non-dynamical -- which requires
      delta S_matter/delta u to NOT feed back derivatives, contradicting (i).
""")
# Demonstrate (i): with u inside Box_u, delta S_matter / delta u DOES contain derivatives of u.
# Toy: S = -1/2 rho * f * (u^a grad_a phi)(...) is schematic; here show Box_u u carries grad u.
# Box_u X = u^a d_a (u^b d_b X). Vary w.r.t. u: delta = (d_a X)(u^b d_b X) + u^a d_a(delta u^b d_b X)+...
# The point: the variation contains u^a d_a(...) acting on delta u  => a DERIVATIVE of delta u
# => the u-EOM is a DIFFERENTIAL (not algebraic) equation for u whenever u sits inside Box_u.
t = sp.symbols('t')
uf = sp.Function('u')(t); Xf = sp.Function('X')(t)
Box_u_X = uf*sp.diff(uf*sp.diff(Xf,t),t)   # 1D toy of u d_t(u d_t X)
# vary: dependence on u and its role -- differentiate structure w.r.t. u treating as field:
print(" 1D toy Box_u X = u d_t(u d_t X) =", sp.expand(Box_u_X))
print("   -> contains u*u''*X-type and u*u'*... terms: VARYING w.r.t u yields terms with d_t(delta u),")
print("      i.e. the u-EOM from S_matter is DIFFERENTIAL in u, NOT purely algebraic.")
print("""
 VERDICT ATTACK 3: The 'no kinetic term => 0 dof => trivially well-posed' inference is NOT SOUND when
 u sits INSIDE Box_u in S_matter. The matter coupling induces derivative-of-u terms in delta S/delta u,
 so u's equation of motion is differential and u is NOT manifestly non-propagating. Whether those
 induced terms (a) vanish on the constraint surface, (b) give a healthy hyperbolic reduced system, or
 (c) are degenerate/ill-posed is EXACTLY the all-orders question the compute left OPEN. The compute's
 own E2 sympy check (Hessian of lambda(u.u+1) = 2 lambda eta, no derivatives) only shows the CONSTRAINT
 TERM has no kinetic piece -- it says NOTHING about the S_matter coupling, which is where the
 derivatives of u actually live. The 'passive' inference used the wrong Hessian.
""")

print("\n"+"#"*90)
print(" SYNTHESIS: is 'passive u' REAL or WISHFUL?")
print("#"*90)
print(r"""
 * The NARROW claim -- 'the generic Einstein-aether c13=c14=0 strong-coupling wall is a statement about
   a propagating aether mode's vanishing kinetic norm, and a theory with NO c_i(grad u)^2 term has no
   such mode' -- is CORRECT and well-supported. The wall, LITERALLY, does not apply to a frame with no
   2-derivative aether kinetic term. This much is real.

 * BUT the WINDOW_SURVIVES verdict needs MORE: that u CAN be supplied passively AND the resulting local
   covariant system is well-posed. Here the passive reading is only PARTLY demonstrated:
     - E1 (frozen cosmological u): insufficient to carry local RAR by itself (Attack 1); the paper's
       actual mechanism is matter-relative-to-u, an algebraic worldline law (not the covariant action).
     - E2 (khronon constraint): the 'no kinetic term' inference used the constraint Hessian, but the
       DERIVATIVES OF u live in the S_matter coupling (Box_u), whose variation is differential in u
       (Attack 3). So u is NOT manifestly non-dynamical once you covariantize; an induced kinetic
       structure appears through the matter coupling, and its well-posedness is the OPEN all-orders
       question -- NOT closed.
     - The covariant action itself sits in the derivative-in-action regime the paper's own text flags
       as the Ostrogradsky/ghost trap (Attack 2), and K is non-entire so the ghost-free theorem fails.

 CONCLUSION: 'passive u' is REAL as a statement that the AETHER STRONG-COUPLING WALL is mis-applied
 (the framework is not a dynamical Einstein-aether). It is WISHFUL as a statement that the local
 covariant realization is WELL-POSED: passivity of u in the covariant action was ASSERTED via the wrong
 Hessian; once u enters Box_u, delta S/delta u is differential and the non-propagation is NOT
 established. The compute's OWN honest layer (Setup C Part 6: 'CONTESTED-leaning-favorable, not a clean
 WINDOW_SURVIVES') is the correct reading; the final verdict OVERSTATED it to WINDOW_SURVIVES by
 scoping to the aether-wall binary and quietly setting aside the induced-dynamics + all-orders edge.
""")
import sys; sys.exit(0)
