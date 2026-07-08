#!/usr/bin/env python3
r"""
ADVERSARIAL REFUTATION of the SURVIVES verdict.
LENS = MOND-preservation + the Bianchi lock.

The SURVIVES compute rests on ONE structural claim (kinetic_compute.py [4],
aether_stress_and_source.py, mi_backreaction.py):

    J_nu = dS_matter/du^nu = -rho_m s k u_nu   (PARALLEL to u, l=0, dust-like)
    => soaked entirely by the unit-timelike Lagrange multiplier lambda = -k rho_m s
    => does NOT excite the transverse spin-1/spin-0 metric-sourcing aether modes
    => u stays inert.

This J_nu was obtained by the REDUCTION  K(Box_u/a0^2) -> scalar k = mu_fw(|a|/a0),
i.e. treating the kernel as a MULTIPLIER that does not depend on u through derivatives.

THE ADVERSARIAL POINT (lens a): the SAME reduction that makes J parallel-to-u is the
reduction that would KILL the MOND if you take it seriously as the field equation.
Two things must BOTH be true for SURVIVES:
  (A) u is inert:            dS_matter/du = parallel to u  (l=0)
  (B) the MOND is real:      S_matter still produces the a=sqrt(a0 g_N) law on matter.

REFUTATION TEST 1 (the "soaked by lambda" trap):
  If K is genuinely a SCALAR multiplier k(u.u-independent), then
     u^mu k u_mu = k*(u.u) = -k   ON SHELL (u.u=-1).
  So S_matter = -(1/2) rho_m s * (-k) = +(1/2) rho_m s k  -- it depends on u ONLY through
  k=mu_fw(|a|/a0), and |a| is the MATTER worldline's acceleration, NOT the field u.
  Then dS_matter/du = (the k-gradient piece) and the "u^mu...u_mu" bilinear variation
  2 k u_nu is EXACTLY CANCELLED on-shell by the constraint -- it carries NO information.
  => The whole "parallel to u, soaked by lambda" statement is TRIVIAL: on the unit-
     timelike shell the bilinear is a constant (-k) and its u-variation is pure gauge.
  QUESTION: after the l=0 bilinear is soaked, is there ANYTHING LEFT that (i) carries the
  MOND and (ii) is transverse (hence sources the metric)?  If the ONLY remaining piece is
  the k-gradient, is THAT piece the MOND, and is it transverse?

REFUTATION TEST 2 (does inert-u still give MOND, or did we throw it out?):
  The MOND force on MATTER comes from varying S_matter wrt the MATTER worldline x, NOT u.
  Compute dS_matter/dx and check the deep-MOND law a=sqrt(a0 g_N) is STILL there when u is
  the passive background clock.  If u being inert does not touch dS_matter/dx, MOND survives.
  BUT: check the coupling that produces MOND is the SAME object whose u-variation we called
  "l=0/parallel".  If MOND requires Box_u to act as a genuine 2nd-order u-derivative operator
  (not a scalar k), then dS_matter/du is NOT simply -rho s k u -- it has the higher-derivative
  aether pieces that the reduction DROPPED, and those are exactly Ostrogradsky/transverse.

REFUTATION TEST 3 (Bianchi lock on the ACTUAL surviving stress):
  The l=0 "dust-like" T^u_{mu nu} ~ rho k u_mu u_nu is only the LEADING piece. The MOND-
  carrying piece is the (nu-1) transverse residual. In the deep-MOND regime (nu-1) is O(1),
  NOT 7e-7. So in a GALAXY the residual is O(1) and the Bianchi lock's l=2 shear channel is
  fully populated. Cassini is deep-Newton (residual 7e-7) so it's safe THERE -- but the
  claim "the MI source is l=0/parallel-to-u, evading the lock" is a DEEP-NEWTON artifact,
  not a structural evasion. Test: is the lock evaded STRUCTURALLY (all accelerations) or
  only because Saturn is deep-Newton (in which case the evasion is just the (nu-1)^2
  suppression already counted, and there is no NEW structural content)?
"""
import sympy as sp
import numpy as np

print("#"*94)
print("# REFUTATION TEST 1 -- is 'J parallel to u, soaked by lambda' TRIVIAL on-shell?")
print("#"*94)
u0,u1,u2,u3 = sp.symbols('u0 u1 u2 u3', real=True)
k = sp.symbols('k', positive=True)
rho,s = sp.symbols('rho_m s', real=True)
lam = sp.symbols('lambda', real=True)
g = sp.diag(-1,1,1,1)
u = sp.Matrix([u0,u1,u2,u3]); ul = g*u
uu = (u.T*ul)[0]

# The FULL u-dependent part of the action (matter bilinear + constraint):
#   L(u) = -(1/2) rho s k (u.u)  +  (lambda/2)(u.u + 1)     [k a scalar multiplier here]
L = -sp.Rational(1,2)*rho*s*k*uu + sp.Rational(1,2)*lam*(uu+1)
# Field equation for u^nu (vary L):
dL = sp.Matrix([sp.diff(L,ui) for ui in (u0,u1,u2,u3)])
print("\n dL/du^nu =", [sp.simplify(x) for x in dL])
# Solve the field eq dL/du = 0  -> (-rho s k + lambda) u_nu = 0 -> lambda = rho s k (for u!=0).
# i.e. lambda is fixed and u is UNDETERMINED (any unit u solves it). CONFIRM:
sol = sp.solve([sp.Eq(dL[i],0) for i in range(4)], [lam], dict=True)
print(" solving dL/du=0 for lambda:", sol)
print("""
 => VERDICT of TEST 1: with K reduced to a scalar k, u's field equation is
    (lambda - rho s k) u_nu = 0, whose ONLY content is lambda = rho s k. u itself is
    COMPLETELY UNDETERMINED by S_matter (any unit-timelike u solves it). The bilinear
    contributes NOTHING to u's dynamics -- it is pure constraint renormalization. So the
    'soaked by lambda' claim is CORRECT but TRIVIAL: at scalar-k order S_matter does not
    source u AT ALL (l=0 or otherwise). The inertness is not in question here; the
    QUESTION is whether the MOND is ALSO gone at this order.
""")

print("#"*94)
print("# REFUTATION TEST 2 -- at scalar-k order, is the MOND on MATTER still present?")
print("#"*94)
# The MOND force is dS_matter/d(matter worldline). With K->k=mu_fw(|a|/a0) a scalar built
# from the MATTER 4-acceleration |a|, S_matter per unit mass on shell:
#   L_m(x) = -(1/2) rho s k(|a|) (u.u) = +(1/2) rho s k(|a|)   (u.u=-1) ... but this has NO
# explicit x-worldline acceleration coupling UNLESS k depends on the MATTER acceleration.
# The paper's reduction is Box_u f -> |a|^2 f where |a| is the acceleration of the CONGRUENCE
# u carries -- for a test body, its OWN 4-acceleration a^mu = u^nu grad_nu u^mu.
# The framework's MOND: -mc^2 F(|a|/a0) with F' = mu_fw gives a = sqrt(a0 g_N). Reconstruct:
print("\n Framework MOND on matter (its OWN nu):  mu_fw(a/a0) * a = g_N  =>  deep-MOND a=sqrt(a0 g_N).")
a0v=9.36e-11; G=6.674e-11; Msun=1.989e30
def mu_fw(x): return (np.sqrt(1+4*x*x)-1)/(2*x)
from scipy.optimize import brentq
# check the law at a deep-MOND radius (dwarf outskirts): g_N tiny
for r_kpc in [0.5, 5, 50]:
    r=r_kpc*3.086e19
    gN=G*Msun*1e10/r**2   # ~1e10 Msun galaxy
    a=brentq(lambda a: mu_fw(a/a0v)*a - gN, 1e-14, 1e-6)
    print(f"   r={r_kpc:>4} kpc: g_N={gN:.2e}  a={a:.2e}  a/sqrt(a0 gN)={a/np.sqrt(a0v*gN):.3f}  (deep-MOND->1)")
print("""
 => VERDICT of TEST 2: the MOND on MATTER (a=sqrt(a0 g_N)) comes from k=mu_fw depending on
    the MATTER body's OWN 4-acceleration a^mu=u^nu grad_nu u^mu -- it is present at scalar-k
    order and is INDEPENDENT of whether u is inert. Making u a passive frame does NOT throw
    out the MOND: the MOND is in dS_matter/dx (matter EOM), the inertness is in dS_matter/du.
    So lens-(a) FAILS to refute: inert-u and live-MOND are NOT in conflict at this order.
    *** BUT this is exactly the CANDIDATE-A structure, and |a|=|u^nu grad_nu u^mu| is a
    2nd u-derivative -- see TEST 4 (the Ostrogradsky/where-is-Box_u's-u-derivative check). ***
""")

print("#"*94)
print("# REFUTATION TEST 3 -- Bianchi lock: STRUCTURAL evasion or deep-Newton artifact?")
print("#"*94)
# The l=2 traceless-shear residual carries (nu-1). In deep-MOND (nu-1) is O(1); at Saturn 7e-7.
def nm1(x): return mu_fw(x)-1 if False else (np.sqrt(1+1/x)-1)  # nu-1 with nu=sqrt(1+1/y), y=a/a0? use g/a0
# framework nu-1 as function of g/a0:
def nu(y): return np.sqrt(1+1/y)
a_sat=G*Msun/(9.58*1.496e11)**2
for label,g in [("Saturn (deep-Newton)",a_sat),("galaxy outskirt (deep-MOND)",5e-11)]:
    y=g/a0v; print(f"   {label:32}: g/a0={y:.2e}  (nu-1)={nu(y)-1:.3e}")
print("""
 => VERDICT of TEST 3: the l=2 residual is (nu-1)-suppressed. At Saturn (nu-1)=7e-7 -> Q2_u
    down by (nu-1)^2 -> the SURVIVES bound. In a galaxy (nu-1)~O(1) and the l=2 residual is
    FULLY ON -- but that is DESIRED (MOND lives there) and there is no Cassini constraint at
    galaxy scales. The Bianchi lock forbids a Phi-sourcing l=2 shear WHERE Cassini applies
    (deep-Newton solar system), and THERE the residual is (nu-1)-suppressed. So the evasion
    is REAL but it is EXACTLY the (nu-1)^2 deep-Newton suppression already banked -- NOT an
    extra structural cancellation. The 'l=0/parallel-to-u soaked by lambda' framing adds
    NOTHING beyond (nu-1)^2: at scalar-k order S_matter sources u by ZERO (Test 1), and the
    only u-source is the SAME (nu-1) gradient the Q2_u bound already uses. Consistent, not
    double-counted, not a manufactured extra evasion.
""")

print("#"*94)
print("# REFUTATION TEST 4 -- THE REAL RISK: is |a|=|u.grad u| a 2nd u-derivative -> Ostrogradsky?")
print("#"*94)
print("""
 The banked COVARIANT_MI_COMPLETION trichotomy (2026-06-26) says the LOCAL aether/vector MI
 gate S_matter=-mc^2 F(|a|/a0) is OSTROGRADSKY-UNSTABLE because |a|=|u^nu grad_nu u^mu| is a
 2nd proper-time derivative -> F'' != 0 non-degenerate -> ghost. The written action's
 Box_u f = u^a grad_a(u^b grad_b f) is ALSO 2nd-order in u-derivatives.

 THE SURVIVES compute REDUCED Box_u -> |a|^2 (scalar k) BEFORE varying wrt u. That reduction
 is what made J parallel-to-u. But the Ostrogradsky ghost lives in the DERIVATIVE structure
 that the reduction DROPPED. Two possibilities:
   (i) The framework's S_matter with Box_u acting on the KERNEL (not the worldline F(|a|)) is
       genuinely NONLOCAL/different from Candidate A's F(|a|) -> it is Route-E-class, the
       ghost-free horn -- but then u is DYNAMICAL through Box_u's u-derivatives and the
       'inert/parallel' claim needs the FULL Box_u variation, NOT the scalar-k reduction.
   (ii) It IS Candidate A in disguise (F(|a|) with |a|=|u.grad u|) -> Ostrogradsky ghost,
        which the SURVIVES compute did NOT check because it reduced Box_u to a scalar first.
 EITHER WAY the scalar-k reduction cannot simultaneously (a) be the field equation for u and
 (b) certify inertness: it drops the very u-derivatives that decide the ghost + the transverse
 sourcing. The SURVIVES 'inert' bound is therefore a bound on a REDUCED (scalar-k) theory that
 is NOT the full covariant field theory whose one edge was to be closed.
""")
# Demonstrate the Ostrogradsky non-degeneracy concretely for F(|a|) with |a| ~ xddot:
t=sp.symbols('t'); x=sp.Function('x')(t)
xdot=sp.diff(x,t); xddot=sp.diff(x,t,2)
a0s,mc2=sp.symbols('a0 mc2',positive=True)
F=sp.Function('F')
Lm = -mc2*F(sp.Abs(xddot)/a0s)   # 1-D avatar of -mc^2 F(|a|/a0)
# Ostrogradsky non-degeneracy: d^2 L/d(xddot)^2 != 0
xdd=sp.symbols('xdd',real=True)
Lm2=-mc2*F(xdd/a0s)   # drop Abs for the smooth region xdd>0
d2=sp.diff(Lm2,xdd,2)
print(" d^2 L/d(xddot)^2 =", d2, "  (!=0 for F'' != 0  -> Ostrogradsky non-degenerate -> ghost)")
print("""
 => VERDICT of TEST 4: if S_matter's u-dependence is through |a|=|u.grad u| (a 2nd u/proper-
    time derivative), the theory is Ostrogradsky-unstable UNLESS it is genuinely nonlocal
    (Route E). The SURVIVES compute reduced Box_u -> scalar k, which HIDES this: at scalar-k
    order u carries no derivatives, so no ghost AND no transverse source appear -- but that is
    a DIFFERENT (reduced, non-dynamical-u) theory. The full covariant field theory's u IS
    dynamical through Box_u, and the reduced 'inert' certification does not apply to it.
""")

print("#"*94)
print("# NET ADVERSARIAL FINDING")
print("#"*94)
print("""
 LENS (a) MOND-preservation:  NOT a refutation. Inert-u and live-MOND coexist AT scalar-k
   order: the MOND is in dS_matter/dx (matter accel |a|), inertness in dS_matter/du. Making u
   passive does not throw out the MOND. (Tests 1-2.)

 LENS (Bianchi lock):  NOT an independent refutation. The lock is evaded in the solar system
   by the SAME (nu-1)^2 deep-Newton suppression already banked; the 'l=0/parallel-to-u' story
   adds no extra cancellation (at scalar-k order S_matter sources u by ZERO). In a galaxy the
   l=2 residual is O(1) but Cassini does not apply there. Consistent, not double-counted. (Test 3.)

 THE REAL WEAKNESS (not the two named lenses, but decisive):  the SURVIVES 'inert' bound is
   computed on the REDUCED scalar-k theory (Box_u -> |a|^2), in which u is NON-DYNAMICAL through
   the kernel. That is the regime where inertness is TRIVIAL (Test 1: S_matter sources u by zero)
   and the ghost is HIDDEN (Test 4: the dropped u-derivatives are exactly the Ostrogradsky /
   transverse-sourcing ones). The full covariant field theory -- u dynamical through
   Box_u = u^a grad_a(u^b grad_b .) -- is NOT certified inert by this computation, and it is the
   theory whose one edge was to be closed. This is the paper's OWN Sec-5 open item (off-circular
   jerk / congruence shear in Box_u), which the SURVIVES compute explicitly CONCEDES it did not
   close ('further pointwise-suppressed but not formally closed here').

 => The verdict SURVIVES is NOT robustly established as a FULL covariant field theory. It is
    established for the REDUCED (constant-|a|/orbit-averaged, scalar-k, non-dynamical-through-
    the-kernel) theory. That is a PARTIAL result: the inert corner exists and is Cassini-safe
    AT the reduction the paper controls, but the edge (does the FULL dynamical-u kinetic theory
    stay inert while keeping MOND, ghost-free) is NOT closed -- the same Box_u u-derivatives that
    would make u dynamical are the ones dropped to prove inertness, and they are the Ostrogradsky/
    transverse ones. Honest verdict: PARTIAL, not SURVIVES.
""")
