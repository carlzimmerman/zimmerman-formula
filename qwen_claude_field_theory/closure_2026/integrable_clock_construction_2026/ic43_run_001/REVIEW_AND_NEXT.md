# IC43: distinguish an auxiliary-coordinate failure from physical closure

Base commit: 527543daf1f0b754072d21ea70b69e0f984dbdcf.
Full gravity theory: **OPEN**. No empirical or novelty claim.

Carl requested maximum credit efficiency. IC42 established that the chosen
IC41 data fail fourth-time preservation with a bounded multiplier. This audit
does not retract that failure. It tests whether the multiplier itself is the
right physical regularity criterion before fitting further initial-data jets.

## 1. Exact activated-bulk auxiliary reduction

For canonical pairs (Q,P), (w,p_w), (ell,p_ell), take

    H = H0(Q,P,w) + F(Q,P,w) ell (w-wc),  F != 0,

with fixed wc and sufficiently differentiable H0,F. Absence of the two auxiliary
velocities gives primaries p_w=p_ell=0. Their preservation gives H_w=H_ell=0.
The executable differentiates before restricting to the constraint surface:

    w=wc,  ell=-H0_w/F.

It computes every entry of the four-constraint Poisson matrix. Its determinant
is F(Q,P,wc)^4 and its rank is four: four second-class constraints, no
first-class constraint in this finite pin subsystem. Secondary preservation
fixes the two primary multipliers; the substituted residuals vanish, with no
tertiary constraint in this regular finite model. The computed Dirac bracket
of the surviving variables is {Q,P}_D=1 and H_red=H0(Q,P,wc).

This leaves one canonical pair in the MECHANICAL calculation, not one
gravitational mode. In the field theory the pullback of the auxiliary canonical
one-form vanishes when p_w=p_ell=0, w=wc. This explains unchanged physical
symplectic structure for variations supported strictly inside the regular
phase; it does not calculate the remaining gravitational constraints or justify
a uniform inverse at the interface.

Differentiating the actual IC30 radial Lagrangian verifies its pin variation:

    delta L / delta ell = J eta exp(S) (w-wc).

Thus the source entering the clock equation is lambda=eta exp(S) ell, not ell
alone. F above absorbs the appropriate Hamiltonian sign and density factors.

## 2. An explicit regular reduced-action completion

Consider the mechanical H0

    H0 = (P^2+Q^2)/2 + P^4/2 + w P^2 + w^2/2,

with wc=0 and F=P^4 for P>0, F identically zero for P<0.

On the active branch, w=0 and ell=-1/P^2 diverges as P approaches zero, but
F ell=-P^2 is regular. On the inactive branch, w=-P^2; the actual constraint
matrix has rank two, giving two second-class and one first-class constraint
among the three constraints there. Both open phases have one physical
canonical pair. Preservation closes separately in these two open phases.

They admit the explicit reduced Hamiltonian

    H_red = (P^2+Q^2)/2 + max(P,0)^4/2.

This is C^3, bounded below, and strictly convex in P:
H_PP=1+6P^2 on P>0, H_PP=1 on P<0. Its physical equations

    Qdot=P+2 max(P,0)^3,   Pdot=-Q

are locally Lipschitz and cross P=0 without divergent physical force. The
DOP853 test from (Q,P)=(1,0.25), t in [0,2], crosses at
t=0.24461512987021095 and has sampled relative energy drift
4.4366288420860656e-11 (401 samples, rtol=1e-11, atol=1e-13).

This is a counterexample to inferring physical singularity from a divergent
multiplier in the open activated phase ALONE. It is not a proof that the
original singular-multiplier variational domain admits that crossing.
The reduced action is an explicitly specified completion.

A negative control matters: replacing F ell by a globally unconstrained new
multiplier would impose w=0 even on P<0. It produces the wrong off-phase
Hamiltonian, differing by P^4/2. Therefore the rescaling is NOT a globally
invertible change of variables across F=0.

## 3. Actual gravitational radial spatial junction identity

This part differentiates IC30's actual action, not the mechanical example.
Let F_phys=S+w and Psi_log=-(Q+w). For spatial gradients
v=(S_r,w_r,Q_r), the calculated Hessian M=partial^2 L/partial v^2 obeys

    M (-a,a,-a)^T = 0.

That jump also leaves F_phys,r and Psi_log,r continuous. The independent
(S,Q) minor is

    -4 m^2 r^4 exp(2Q+2S+4w) u^2,
    u=(S+2w)/(S+w).

The computed generic rank is two, dropping to one at u=0. These statements
assume the chart S+w != 0 and m r != 0. Neither rank is a Dirac rank or a
gravitational DOF count. The exceptional locus is retained, not ignored.

The gradient-quadratic part of the actual action becomes exactly

    L_grad = m r^2 exp(F_phys-Psi_log)
             [Psi_log,r^2 - 2 F_phys,r Psi_log,r
              + (1-u^2) F_phys,r^2].

No w_r remains in this expression. Shift terms linear in gradients do not
change their conjugate flux under the derivative jump at continuous fields,
shift, and momenta. The computed Q time momentum is 2Jq.

For a moving interface r=R(t), the normal variational flux involves
[partial L/partial f_r - Rdot partial L/partial f_t]. With continuous Jq and
the stated other data, the null direction passes this limited flux test.
It does NOT prove an evolving off-phase solution exists, that all allowed
interface variations are satisfied, or that the physical curvature stays
bounded. It also does NOT derive Phi=Psi: continuity of two independent
potentials is not equality of those potentials.

## 4. What survives and what must be done next

IC42's fourth-time divergence remains a failure in its bounded-ell class.
A weighted-multiplier or reduced-phase completion is a NEW variational
specification. In particular ell proportional to distance^(-2) is not
ordinarily locally integrable. Varying the activation zero while holding such
ell fixed can invalidate the original action integral. Finite eta ell on one
solution is insufficient to define a differentiable action on nearby fields.

The next unavoidable calculation is consequently ONE global variational
interface completion, not a fifth-time polynomial fit:

1. Specify the admissible fields/multipliers and moving phase domains. Preserve
   the true off-phase condition eta(q,w)=0, not an assumed condition on q alone.
2. Derive the inactive clock equation and the active reduced equations from
   that action, including all moving-boundary terms and interface variations.
   The radial gradient identity does not remove canonical mixing under a
   physical-metric change of variables. Do not replace this step by the toy
   mechanical elimination.
3. Solve and preserve their junction conditions, then perform the remaining
   full constraint and characteristic analysis, separately at k=0, k!=0 and
   exceptional field values.

If that fails, the completion is dead in its stated class. If it works, full
PPN, stability/causality/strong-coupling, cosmology and observations still need
to come from that same action. No other candidate's successes are imported.
There is no basis here for announcing a complete theory or a Kepler-grade
empirical prediction.

## Verification and attribution

All four newly created Python files ran, including both test files via test
discovery. New module tests were first observed to fail while their modules
were absent. Final targeted suite: 17 tests, exit 0, 42.770 seconds.
The initial 16-test suite also passed. The two scientific --strict commands
exit 2 deliberately because full-theory closure is OPEN; their runners report
exit 1. Neither is a Python exception. Four evidence manifests validate
(exit 0 each). The prior unchanged 328-test IC41 regression run is not claimed
as rerun here. Exact commands, changed-file inventory, hashes and outputs are
linked by run_index.json and the manifests.

Mathbox computation-audit and proof-audit required separating the mechanical
counterexample, actual spatial identity, and unproved global completion.
Self-proofreading covered this note; no proofreading-driven mathematical-token
changes. No Lean or formal proof-assistant certificate is claimed.

Credit Carl Zimmerman for the original framework and primordial-clock
direction; the L44 activation suggestion remains credited in IC39. This
analysis makes no priority claim and does not attribute the technical
multiplier reduction to an unrecorded conversation. Concurrent Fable work
and all earlier negative results remain untouched.
