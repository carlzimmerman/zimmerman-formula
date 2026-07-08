#!/usr/bin/env python3
r"""
refute_wellposed.py -- ADVERSARIAL counter-check on the SURVIVES verdict.

LENS: ghost-freedom + well-posedness of the FULL theory (aether kinetic + nonlocal
MI-matter K(Box_u)). Does the combination stay ghost-free AND hyperbolic/well-posed,
or does making u^mu dynamical (to get inertness) while keeping the nonlocal K(Box_u)
matter coupling reintroduce a ghost / strong coupling / bad Cauchy problem?

Two SEPARATE hazards the SURVIVES compute did NOT test:

  (H1) STRONG COUPLING at the PPN-safe corner. Einstein-aether's spin-0 mode kinetic
       normalization -> 0 exactly where alpha1=alpha2=0 forces c14->0. A vanishing
       kinetic normalization = strong coupling = loss of predictivity / breakdown of the
       linearized (perturbative) Cauchy problem. The SURVIVES corner c4=-c3^2/c1,
       c2=(-2c1^2-c1c3+c3^2)/(3c1): is c14 bounded away from 0, or does inertness DRIVE
       c14->0?  Also: the SURVIVES script's OWN witness had s0^2 finite -- but does the
       spin-0 STRONG-COUPLING scale stay above solar-system frequencies?

  (H2) THE REDUCTION THAT PRODUCED "l=0/parallel-to-u". Step [4] replaced K(Box_u/a0^2)
       by a SCALAR k (constant-|a| reduction). That reduction is LOCAL. But the paper
       (line 42/61) says K is NONLOCAL and that nonlocality is the ONLY thing killing the
       Ostrogradsky ghost. The variation delta S_matter/delta u^mu of the FULL nonlocal
       K(Box_u) is NOT -rho s k u^mu: Box_u depends on u (Box_u f=u^a grad_a(u^b grad_b f)),
       so varying u INSIDE Box_u produces derivative-of-u source terms the reduced scalar k
       throws away. Are those terms (a) transverse (metric-sourcing, spin-1/spin-0 exciting),
       and (b) higher-time-derivative in u (Ostrogradsky, once u is dynamical)?

We test both AT THE MODIFIED-INERTIA PREMISE (do NOT re-litigate the sign; do NOT judge
through standard-MOND). Prove-by-moving. Default skeptic: only clear H1 AND H2 keeps
SURVIVES; either one biting -> REFUTE to PARTIAL (fine-tuned/strong-coupled/ill-posed).
"""
import sympy as sp
import numpy as np

FAIL_SURVIVES = False   # set True if an adversarial hazard bites
notes = []

print("#"*94)
print("# (H1) STRONG COUPLING: does inertness (alpha1=alpha2=0) drive the spin-0 kinetic")
print("#      normalization c14 -> 0 on the SURVIVES corner?")
print("#"*94)
c1,c3 = sp.symbols('c1 c3', real=True)
# SURVIVES corner:
c4 = -c3**2/c1
c2 = (-2*c1**2 - c1*c3 + c3**2)/(3*c1)
c13 = c1+c3
c14 = sp.simplify(c1+c4)
c123 = sp.simplify(c1+c2+c3)
print("\n c14 on the corner  = c1 + c4 =", sp.simplify(c14), "= (c1^2 - c3^2)/c1 = (c1-c3)(c1+c3)/c1")
print(" c123 on the corner = ", c123)
# spin-0 kinetic normalization ~ c14 (Jacobson): the spin-0 mode's kinetic term coefficient
# in the linearized action is proportional to c14 (and 2-c14). If c14->0 the spin-0 mode is
# strongly coupled (its speed s0^2 = c123(2-c14)/(c14(1-c13)(2+c13+3c2)) has c14 in DENOMINATOR
# -> s0^2 blows up as c14->0, i.e. the mode becomes non-dynamical/strongly-coupled).
s0sq = sp.simplify(c123*(2-c14)/(c14*(1-c13)*(2+c13+3*c2)))
print("\n s0^2 on the corner =", s0sq)
# Evaluate along the diagonal to see the behavior as c3 -> c1 (where c14 -> 0):
print("\n prove-by-moving: walk c3 -> c1 at fixed c1=0.5 (c14 -> 0) and watch the spin-0 sector")
print(f"   {'c3':>7} {'c14':>10} {'s0^2':>12} {'spin0 kinetic ~c14':>20}")
c1v = 0.5
for c3v in [0.0, 0.2, 0.4, 0.45, 0.49, 0.499]:
    c14v = (c1v**2 - c3v**2)/c1v
    s0v = float(s0sq.subs({c1:c1v, c3:c3v}))
    print(f"   {c3v:>7.3f} {c14v:>10.4f} {s0v:>12.3f} {c14v:>20.4f}")
print("""
 The spin-0 mode kinetic normalization ~ c14 = (c1-c3)(c1+c3)/c1. It is NOT forced to 0 by
 inertness: c14 vanishes only on the SPECIAL line c3=+/-c1 (a codim-1 edge INSIDE the corner),
 not on the whole corner. The SURVIVES witness c1=0.526,c3=0.261 has c14=0.526-0.129=... away
 from 0. So inertness does NOT drive strong coupling generically -- H1 does NOT bite by itself.
 (This actually CONFIRMS a piece of SURVIVES: the alpha=0 corner in Einstein-aether is codim-2,
 distinct from the c14->0 strong-coupling edge. Good.)""")
# But: verify the witness is a FINITE distance from the c14=0 edge AND the c123=0 edge.
c1w,c3w = 0.526,0.261
c14w=(c1w**2-c3w**2)/c1w; c123w=float(c123.subs({c1:c1w,c3:c3w}))
print(f" witness c1=0.526,c3=0.261: c14={c14w:.4f} (dist to 0 = {abs(c14w):.3f}), c123={c123w:.4f}")
h1_ok = abs(c14w) > 0.05 and abs(c123w) > 0.05
print(f"   witness bounded away from BOTH strong-coupling edges (c14=0, c123=0): {h1_ok}")
if not h1_ok:
    FAIL_SURVIVES=True; notes.append("H1: witness sits on a strong-coupling edge")

print("\n"+"#"*94)
print("# (H2) THE LOAD-BEARING GAP: does the FULL nonlocal K(Box_u) source, with u DYNAMICAL,")
print("#      still reduce to 'l=0/parallel-to-u soaked by lambda'? Or do the Box_u-varied,")
print("#      u-derivative source terms EXCITE the transverse (metric-sourcing) modes AND/OR")
print("#      reintroduce higher-time-derivatives of u (Ostrogradsky, now that u propagates)?")
print("#"*94)
print(r"""
 The SURVIVES step [4] varied M = k*(u^mu u_mu) with k HELD FIXED (a scalar). But the true
 matter scalar is  M_full = u^mu K(Box_u/a0^2) u_mu,  Box_u f = u^a grad_a(u^b grad_b f).
 K is NONLOCAL in Box_u; Box_u is BUILT FROM u. So delta M_full/delta u^nu has THREE pieces:
   (i)   the two explicit u factors: 2 K(Box_u) u_nu           <- the "parallel" piece [4] kept
   (ii)  delta of Box_u INSIDE K, hitting the LEFT u^a:  (grad_a . )-type, TRANSVERSE
   (iii) delta of Box_u INSIDE K, hitting the RIGHT u^b: another grad, TRANSVERSE
 Pieces (ii),(iii) are the ones the scalar reduction k DISCARDS. They are NOT parallel to u,
 and they carry TWO extra covariant derivatives (Box_u = 2nd order), acting through K'(Box_u).
""")
# Model the essential structure on a worldline (paper's own reduction domain) to SEE the
# discarded terms. Use the point-particle image: along a worldline u=dx/dtau (unit), Box_u
# acting on the frame reduces to proper-time 2nd derivative; the matter scalar is effectively
# F(|a|^2/a0^2) with |a|^2 = a^mu a_mu, a^mu = u^b grad_b u^mu = du^mu/dtau (the 4-accel).
# So M_full ~ u.u renormalized by K(a^2/a0^2). The u-variation of a^mu = u-dot brings in u-DDOT.
tau = sp.symbols('tau', real=True)
x = sp.Function('x')(tau)                       # 1D worldline coordinate (schematic)
xd = sp.diff(x,tau); xdd = sp.diff(x,tau,2); xddd = sp.diff(x,tau,3)
a0s = sp.symbols('a0', positive=True)
# Framework gate as the matter Lagrangian along the worldline (schematic, |a|~|xdd|):
F = sp.Function('F')                            # K-derived gate; F(z)=z*K(z) schematically -> depends on |a|^2
L = -F(xdd**2/a0s**2)                           # the per-body MI gate: DEPENDS ON xdd (2nd deriv)
print(" schematic worldline MI Lagrangian L = -F(xdd^2/a0^2)  (xdd = 4-acceleration = u-dot)")
# Ostrogradsky non-degeneracy test: d^2 L / d(xdd)^2  (must be 0 for a healthy 2nd-order theory)
dLdxdd = sp.diff(L, xdd)
d2Ldxdd2 = sp.simplify(sp.diff(L, xdd, 2))
print("\n d^2 L / d(xdd)^2 =", d2Ldxdd2)
# Non-degenerate <=> this is not identically zero <=> Ostrogradsky ghost (Milgrom-1994 wall, check-3)
is_degenerate = (sp.simplify(d2Ldxdd2) == 0)
print(" degenerate (d2L/dxdd2 == 0, i.e. NO Ostrogradsky ghost)?", is_degenerate)
print("""
 => d2L/d(xdd)^2 = -2 F'/a0^2 - 4 xdd^2 F''/a0^4  is NON-ZERO for a generic gate F.
    This is EXACTLY the framework's OWN check-3 Ostrogradsky result: a LOCAL gate that
    depends on the acceleration (xdd) is Ostrogradsky non-degenerate -> ghost. The paper
    ESCAPES this ONLY by K being NONLOCAL (infinite-derivative / branch-cut), NOT by the
    scalar reduction. Tonight's step [4] used the LOCAL scalar k = F' -> it is the LOCAL,
    ghost-CARRYING truncation, not the nonlocal ghost-free object.""")

print("\n"+"#"*94)
print("# THE DECISIVE POINT: the SURVIVES 'inert' mechanism was DERIVED in the LOCAL reduction,")
print("#   but the GHOST-FREEDOM lives ONLY in the NONLOCAL object. Are they COMPATIBLE?")
print("#"*94)
print(r"""
 The tension is structural, not numerical:

   * SURVIVES-inertness argument (step [4]): needs K(Box_u) -> scalar k, so that
     delta S_matter/delta u = -rho s k u (parallel, l=0, soaked by lambda). This is the
     LOCAL reduction. In the LOCAL reduction the matter gate is Ostrogradsky-GHOSTY
     (check-3 / the line-42 'local truncation carries the ghost'). So the inertness
     mechanism, taken literally, lives on the GHOSTY (local) truncation.

   * Ghost-freedom (line 61): needs K FULLY NONLOCAL (infinite-derivative). In the nonlocal
     object, delta S_matter/delta u is NOT the single parallel term -rho s k u: the variation
     of Box_u inside K contributes an INFINITE tower of grad(u) terms (K' * delta Box_u + ...),
     which are TRANSVERSE (they carry grad, so they have spin-1/spin-0 content) and NONLOCAL
     in time. Whether that infinite transverse tower stays (nu-1)-suppressed AND does not
     excite a metric-sourcing quadrupole was NOT computed -- step [4] discarded the entire
     tower by the scalar reduction.

 So the SURVIVES verdict rests on evaluating the INERTNESS in a regime (local scalar k) where
 the theory is ghost-CARRYING, while claiming ghost-freedom from a DIFFERENT regime (fully
 nonlocal K) whose u-variation was never computed. The two legs of the argument are evaluated
 at DIFFERENT points and not shown to hold SIMULTANEOUSLY.
""")

# Quantify: how big is the DISCARDED transverse tower relative to the kept parallel piece,
# at leading (nu-1) order, on a circular orbit? The kept piece ~ rho k ~ rho*mu_fw ~ O(rho).
# The discarded Box_u-variation piece ~ rho K'(z) * (grad^2 of delta-u structure). On a circular
# orbit Box_u ~ |a|^2, K'(|a|^2/a0^2). In deep-Newton |a|>>a0: K(z)->1, K'(z)-> -1/(4 z^{3/2})
# (from K=mu_fw(sqrt z)=sqrt(1+1/sqrt z)... compute exactly):
z = sp.symbols('z', positive=True)
Kz = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z))
Kp = sp.simplify(sp.diff(Kz, z))
print(" K(z) =", Kz)
print(" K'(z) =", sp.simplify(Kp))
# deep-Newton z = (|a|/a0)^2 >> 1: expand
Kp_large = sp.series(Kp.rewrite(sp.sqrt), z, sp.oo, 3)
print(" K'(z) as z->oo :", Kp_large)
# The transverse source ~ K'(z)*z * (curvature of u) relative to K(z)*(unit) ~ K'(z)*z / K(z).
# Numerically at Saturn: z = (a_Sat/a0)^2.
c=2.99792458e8; G=6.674e-11; Msun=1.989e30; AU=1.495978707e11
a_Sat=G*Msun/(9.58*AU)**2
for lab,a0 in [("rho_DE",9.362e-11),("rho_tot",1.130e-10)]:
    zz=(a_Sat/a0)**2
    Kv=float(Kz.subs(z,zz)); Kpv=float(Kp.subs(z,zz))
    ratio=abs(Kpv*zz/Kv)
    print(f"   {lab}: z=(a_Sat/a0)^2={zz:.3e}  K={Kv:.6f}  K'={Kpv:.3e}  |K' z / K| = {ratio:.3e}")
print("""
 |K' z / K| ~ (nu-1)/2 ~ 3.6e-7 at Saturn: the transverse tower's LEADING amplitude is itself
 deep-Newton suppressed (same order as the kept residual). So the DISCARDED tower is NOT larger
 than the kept parallel residual -- it is the SAME (nu-1) order. This is a POINT IN FAVOR of the
 SURVIVES bound at LEADING order: the transverse source amplitude is (nu-1)-suppressed whether
 you keep the scalar reduction or the full nonlocal variation. BUT it does NOT resolve:
   (i)   the DERIVATIVE COUNT: the nonlocal tower carries arbitrarily-high time-derivatives of u;
         once u is DYNAMICAL these are the Ostrogradsky-dangerous terms. The nonlocal form factor
         kills the ghost in the MATTER-only (u non-dynamical) sector (paper's proof); it was NOT
         re-proven ghost-free once u ALSO has the aether kinetic term and its OWN propagator --
         the mixing u_matter-tower x u_aether-kinetic is a NEW propagator not analyzed.
   (ii)  strong-coupling: even (nu-1)-small transverse sources can RESONANTLY amplify if the
         spin-0 aether mode is near strong coupling; step [5]'s (nu-1)^2 bound assumed NO
         resonant denominator (a healthy, gapped spin-0 propagator). Not verified for the full tower.
""")

print("#"*94)
print("# VERDICT OF THE COUNTER-CHECK")
print("#"*94)
print("""
 H1 (strong coupling driven by inertness): does NOT bite. The alpha=0 SURVIVES corner is
    codim-2 and distinct from the c14->0 / c123->0 strong-coupling edges; the witness is a
    finite distance from both. SURVIVES's 'open region' claim is intact on this axis.

 H2 (the load-bearing gap): the SURVIVES 'l=0/parallel-to-u, soaked-by-lambda' inertness
    mechanism was derived in the LOCAL scalar reduction K->k, which is precisely the
    Ostrogradsky-GHOSTY truncation (this script's d2L/dxdd2 != 0 = the framework's own check-3).
    Ghost-freedom is claimed from the DIFFERENT, fully-nonlocal K, whose u-variation (an infinite
    transverse, higher-time-derivative tower) was NEVER computed with u DYNAMICAL. The leading
    AMPLITUDE of that discarded tower is (nu-1)-suppressed (good, favors the bound), but its
    DERIVATIVE ORDER and the u_matter x u_aether MIXED propagator -- the actual well-posedness /
    ghost question -- are NOT established. The two legs (inertness in the local regime, ghost-
    freedom in the nonlocal regime) are evaluated at different points and not shown compatible.

 CONSEQUENCE FOR THE VERDICT: the well-posedness/ghost-freedom of the FULL theory
 (aether kinetic + nonlocal K(Box_u), u DYNAMICAL) is NOT ESTABLISHED. The SURVIVES verdict
 is really 'SURVIVES the QUADRUPOLE-AMPLITUDE sub-question at leading order' -- it does NOT
 close the well-posedness/ghost sub-question this lens targets. Under the rule 'a fine-tuned/
 strong-coupled/ghosty corner is not a robust survives, and default skeptic when uncertain',
 the honest reading is PARTIAL: the amplitude is inert, but the full-theory ghost-freedom +
 well-posedness (the nonlocal tower's derivative order + the mixed propagator) is an
 UNCLOSED edge -- exactly the paper's own line-75 concession ('no metric variation, no u^mu
 field equation, no perturbation analysis; well-posedness/dispersion not established').
""")
import sys
sys.exit(0)
