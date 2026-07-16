#!/usr/bin/env python3
r"""
SETUP C -- DOES THE GENERIC-AETHER STRONG-COUPLING RESULT EVEN APPLY?

Decisive question (Q0): the c13->0 / lambda->1 "aether strong-coupling wall" (BPS 0906.3046,
1007.3503; Jacobson "Undoing the twist" 1310.5115) is a statement about the SELF-INTERACTIONS
of a PROPAGATING scalar/vector mode whose CANONICAL KINETIC NORM -> 0. This script establishes,
by dof-counting + the strong-coupling-scale formula, whether that wall applies to the
FRAMEWORK's PASSIVE horizon-anchored frame (MOND-in-MATTER) or ONLY to aether-MOND (MOND carried
by a DYNAMICAL aether, AeST/khronometric-like).

We do NOT re-derive the framework's Saturn evasion (established: Q2~7e-34, matter sector).
We test PRIOR to the wall: does the framework's own structure FORCE a dynamical aether kinetic
term (so the wall bites), or supply u as a passive constraint (so the wall does not arise)?

Default skeptic BOTH ways.
"""
import sympy as sp

print("#"*96)
print("# PART 1 -- WHAT the strong-coupling wall IS (so we can test applicability, not import a verdict)")
print("#"*96)
print(r"""
 The wall (BPS 0906.3046, 1007.3503; Jacobson 1310.5115; Foster gr-qc/0509083):
   * Einstein-aether L_kin = -M^2[c1(grad u)^2 + c2(div u)^2 + c3(...) + c4 a^2] is a
     2-DERIVATIVE kinetic term for a DYNAMICAL unit vector u. It PROPAGATES a spin-1 (2 dof)
     and a spin-0 (1 dof) mode ON TOP of the graviton.
   * Canonical kinetic NORMS: spin-1 ~ N1 = 2 c14 (1-c13); spin-0 ~ c14(2-c14) (with c14=c1+c4).
   * Strong-coupling SCALE (self-interaction of the CANONICALLY-NORMALIZED mode):
        M_sc ~ sqrt(N) * M_Pl ,   N = the mode's kinetic norm.
     As the couplings c_i -> 0 (forced by GW170817 c13<~1e-15 + pulsar bounds), N -> 0, so
     M_sc -> 0: the PROPAGATING mode's self-interactions blow up. THAT is the wall.
   * KEY: the wall is a property of the mode's KINETIC NORM. NO kinetic term => NO propagating
     mode => NO canonical normalization => NO M_sc => the wall is UNDEFINED (not passed, not
     failed -- it does not ARISE). This is the applicability hinge.
""")

print("#"*96)
print("# PART 2 -- DOF COUNT: passive-frame constraint system vs dynamical Einstein-aether")
print("#"*96)
r"""
Two candidate realizations of the frame field u^mu (unit timelike, u.u = -1):

(i) PASSIVE / CONSTRAINT frame (the framework's dS-Unruh premise):
      u^mu is the local rest frame of the de Sitter-Unruh vacuum -- the frame in which the
      horizon bath is isotropic. It is DETERMINED by the cosmological background + the local
      inertial response; it is imposed by a Lagrange multiplier lambda(u.u+1) and (optionally)
      u^mu = -grad T / sqrt(-grad T . grad T) with T the (non-dynamical or minimally-constrained)
      cosmic time. THERE IS NO c_i (grad u)^2 KINETIC TERM. The action is
         S = S_EH[g] + S_matter[g, u; rho_m K(Box_u)]  + lambda (u.u+1)
      u appears ALGEBRAICALLY (through the matter form factor) + via the unit constraint, NOT
      via a propagating kinetic term.

(ii) DYNAMICAL Einstein-aether (AeST / khronometric, the framework is NOT this):
      S = S_EH[g] + M^2 L_kin(c1..c4)[grad u] + lambda(u.u+1) [+ AeST free-fn F(Y) carrying MOND]
      u PROPAGATES: +2 (spin-1) + 1 (spin-0) dof. The MOND is carried by the aether/F(Y).
"""
lam = sp.symbols('lambda_c', real=True)  # Lagrange multiplier for the unit constraint

# --- dof count via constraint counting (schematic but exact for the point) ---
# A unit timelike vector u^mu has 4 components; the constraint u.u=-1 removes 1 -> 3 potential dof.
# In (ii) Einstein-aether: those 3 (2 spin-1 + 1 spin-0) become PROPAGATING (each has a 2nd-order-
#   in-time kinetic term from L_kin) -> 3 new propagating dof with kinetic norms N -> M_sc ~ sqrt(N) M_Pl.
# In (i) PASSIVE: with NO L_kin, u^mu has NO time-derivative kinetic term. Its 4 components are fixed by:
#   - 1 unit constraint (u.u=-1),
#   - 3 conditions from being the (non-dynamical) cosmic rest frame / khronon gradient direction
#     (u_i = -grad_i T / |grad T|, T non-dynamical background OR pinned by the multiplier structure).
# => 0 propagating aether dof. u is a CONSTRAINED BACKGROUND field, not a propagator.

print(" DOF LEDGER")
print("  Component budget of a unit timelike u^mu:              4  (minus u.u=-1 => 3 would-be)")
print("  (ii) DYNAMICAL Einstein-aether:  propagating aether dof = 3  (spin-1 x2 + spin-0 x1)")
print("       -> each has kinetic norm N_i; STRONG-COUPLING scale M_sc ~ sqrt(N_i) M_Pl DEFINED.")
print("  (i)  PASSIVE constraint frame:   propagating aether dof = 0  (NO L_kin(grad u)^2 term)")
print("       -> NO canonical mode, NO N_i, NO M_sc: the wall's central object DOES NOT EXIST.")

print("\n#"+"#"*95)
print("# PART 3 -- STRONG-COUPLING SCALE: literal formula, both realizations")
print("#"*96)
c1,c3 = sp.symbols('c1 c3', positive=True)
c14 = sp.symbols('c14', real=True)
N_spin1 = 2*c14*(1 - (c1+c3))          # spin-1 kinetic norm (Jacobson 0801.1547)
# strong-coupling scale (schematic canonical estimate): M_sc = sqrt(N)*Mpl
Mpl = sp.Rational(2435,1)*sp.Integer(10)**15  # 2.435e18 GeV reduced Planck
print(" (ii) dynamical aether: M_sc = sqrt(N_spin1) * M_Pl,  N_spin1 = 2 c14 (1-c13).")
import numpy as np
Mpl_f = 2.435e18
print(f"   {'c13 (=c14 scale)':>18} {'N ~ c':>12} {'M_sc/GeV':>14}   note")
for cval,note in [(0.787,"GW170817-EXCLUDED O(1) witness"),
                  (1e-2,"pulsar-ish"),
                  (1e-15,"GW170817-REQUIRED corner")]:
    N = 2*cval*(1-cval)
    Msc = np.sqrt(max(N,0))*Mpl_f
    print(f"   {cval:>18.0e} {N:>12.3e} {Msc:>14.3e}   {note}")
print("""
   => at the OBSERVATIONALLY REQUIRED corner c13<~1e-15, N~1e-15, M_sc ~ 1e11 GeV and the
      LINEAR (2-point) certification loses control; the wall is a genuine predictivity issue
      FOR THE DYNAMICAL AETHER (this is exactly what refute_strongcoupling.py found).

 (i) passive constraint frame: N is UNDEFINED (no kinetic term). There is no canonically-
     normalized aether mode whose vertices ~1/sqrt(N)^n blow up. The strong-coupling SCALE
     M_sc does not exist. The only propagating dof is the graviton (M_Pl, healthy). The
     matter form factor K(Box_u) modifies the MATTER sector (already shown ghost-free 2-pt,
     RAR-correct, Saturn-evading); it does NOT introduce a new propagating vector.
""")

print("#"*96)
print("# PART 4 -- IS the passive frame FORCED to become dynamical by local covariance? (the real test)")
print("#"*96)
print(r"""
 A WALLED verdict is ONLY valid if the framework's OWN structure FORCES a c_i(grad u)^2 kinetic
 term. Enumerate the ways u^mu can be a covariant, diffeomorphism-respecting field WITHOUT a
 generic-aether kinetic term (existence proofs in the literature -- these are CONSISTENT theories):

  (a) KHRONOMETRIC / hypersurface-orthogonal u = -grad T/|grad T|, T = cosmic (dS) time.
      This is a CONSTRAINT: u is the gradient of a scalar. The dynamical content is T (ONE scalar,
      the khronon), NOT 3 aether dof. In the framework T is the dS-Unruh vacuum clock (horizon-
      anchored). If T is NON-dynamical (fixed cosmological background) -> 0 propagating dof.
      If T is minimally dynamical -> khronometric, ONE mode -- and even THAT can be gapped/frozen
      by the cosmological potential (the frame is PINNED to the horizon rest frame, not free).

  (b) LAGRANGE-MULTIPLIER / non-dynamical vector: S includes lambda(u.u+1) but NO (grad u)^2.
      u is a background structure varied only against the multiplier + matter coupling. This is a
      consistent constrained field theory (Bekenstein/aether-lite constructions). 0 aether dof.

  (c) FIXED preferred-frame BACKGROUND (SME-style): u^mu is a specified background vector (the
      CMB/cosmic rest frame). The framework's own SME bridge (project_sme_lorentz_bridge) ALREADY
      treats u this way -- as a background inducing s_munu, PASSING every gravity bound. 0 aether dof.

 In ALL of (a)-(c) there is NO generic 2-derivative aether kinetic term and hence NO c13->0
 strong-coupling scale. Local covariance is SATISFIED (diff-invariant actions exist for each).
 => local covariance does NOT, by itself, FORCE the generic Einstein-aether kinetic term.

 WHAT WOULD force it: if the framework REQUIRED u to carry PROPAGATING dynamics that reproduce
 the MOND phenomenology THROUGH THE AETHER (as AeST does via F(Y), or as a khronon whose OWN
 kinetic twist supplies the deep-MOND force). The framework does NOT: its MOND is in S_matter's
 K(Box_u) form factor (a MATTER coupling), and the frame is the PASSIVE argument of that form
 factor. The aether-MOND coupling that DRIVES BPS/Jacobson to need a large-normalization
 dynamical aether is ABSENT.
""")

print("#"*96)
print("# PART 5 -- THE OVER-COUNTING DIAGNOSIS")
print("#"*96)
print(r"""
 Applying the generic-aether wall to the framework's passive frame COMMITS TWO over-counts:

  OVER-COUNT #1 (dof): it assigns 3 propagating aether dof (spin-1 x2 + spin-0) to u, then
    reads off a strong-coupling scale M_sc ~ sqrt(N) M_Pl from their kinetic norms. But a
    passive/constraint frame has 0 (or, in the khronometric sub-case, 1 gapped) aether dof.
    The wall's central object (the vanishing-norm propagating mode) is COUNTED INTO EXISTENCE
    by assuming the c_i(grad u)^2 term the framework never wrote.

  OVER-COUNT #2 (MOND placement): the BPS/AeST analysis needs the aether to CARRY the MOND
    (F(Y), the twist), which is precisely what forces a large aether response and the delicate
    c13->0 corner. The framework's MOND is in MATTER (K(Box_u)); the frame carries NONE of it.
    So the very reason the dynamical aether must sit at the pathological corner is absent.

 CONSEQUENCE: the c13->0 result, applied to the framework's passive frame, is a MIS-APPLICATION
 (it judges a MOND-in-MATTER, passive-frame theory through the AeST/aether-MOND lens -- exactly
 the standard-MOND lens the framework is not). The wall is REAL and BINDING for the framework's
 WRITTEN AeST/khronometric MG limb (D4 +6..14 sigma; the strong-coupling corner). It is
 UNDEFINED for the MI/passive-frame limb -- UNLESS one shows the passive frame cannot be
 covariantly defined, which (a)-(c) refute by explicit existence.
""")

print("#"*96)
print("# PART 6 -- THE RESIDUAL OPEN EDGE (do NOT manufacture WINDOW_SURVIVES)")
print("#"*96)
print(r"""
 The wall not APPLYING is necessary but not sufficient for WINDOW_SURVIVES. What remains OPEN,
 on the framework's OWN terms, is the Cauchy problem of the PASSIVE-FRAME + NONLOCAL-K system:

   * The passive frame removes the aether STRONG-COUPLING question (no propagating aether mode).
   * But the nonlocal matter form factor K(Box_u), Box_u = u^a grad_a(u^b grad_b .), is
     INFINITE-DERIVATIVE / has a branch cut (NOT entire) -> not AUTOMATICALLY ghost-free by the
     Biswas-Mazumdar criterion; its well-posed Cauchy problem (initial data on a nonlocal theory)
     is a SEPARATE question the framework's own ghost_test_v2 / dispersion_setup examined at
     2-point (one healthy pole + dissipative cut, no new propagating matter pole) but did NOT
     fully close at all orders with u varied inside Box_u.
   * The prior refute_wellposed.py concession stands: the nonlocal tower's DERIVATIVE ORDER and
     the well-posedness of the full passive-frame+K system are not established at all orders.

 So: the AETHER strong-coupling wall does NOT apply (Q0 answer: passive frame, not forced
 dynamical). But the passive-frame + nonlocal-K Cauchy problem is a DIFFERENT, still-open edge.
 That is CONTESTED-leaning-favorable, not a clean WINDOW_SURVIVES and NOT a WALLED.
""")

print("="*96)
print("APPLICABILITY VERDICT (Setup C):")
print("  The generic Einstein-aether / Horava c13->0 strong-coupling wall is a property of a")
print("  DYNAMICAL propagating aether mode whose kinetic norm vanishes. The framework's frame is")
print("  PASSIVE (dS-Unruh horizon rest frame) and its MOND is in MATTER, not the aether. Passive/")
print("  khronometric/background realizations of u EXIST as consistent covariant theories with 0")
print("  (or 1 gapped) aether dof -- local covariance does NOT force the generic kinetic term.")
print("  => Applying the wall to the framework's passive frame OVER-COUNTS dof and MIS-PLACES the")
print("     MOND: it is a MIS-APPLICATION. The wall BINDS the written AeST/MG limb, NOT the MI limb.")
print("  => The remaining open edge is the passive-frame + nonlocal-K CAUCHY problem (separate).")
print("="*96)
