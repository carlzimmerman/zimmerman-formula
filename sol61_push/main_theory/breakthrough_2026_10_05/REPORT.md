# Formation memory: conservative internal switch and a transition obstruction

Checkpoint SOL61-MAIN-FORMATION-2026-10-05-A. Common base
`a36191815030afddf1277d413f488fb0c3ac520f`. Writes confined to this directory.
**The complete gravity goal is not reached.** The strongest new result is a
scoped obstruction: a local pressureless density-reading switch cannot both
have zero internal energy on its exact OFF and ON plateaus and have positive
fluid/internal stiffness throughout their interpolation, if its frozen MOND
energy changes by a nonzero constant. This remains true when the internal
oscillator is individually healthy and arbitrarily stiff. A positive conservative
construction supplies a distinct stress-free OFF branch, then exposes this
missing transition arrow rather than concealing it.

## Contract and relationship to existing work

The intended object is one sourced conserved action giving bound MOND, full
FRW off, ownership, cold transport and cosmology. This report attacks only
switch transport, stress and local transition stability. It does not import
C-H/K chassis passes or cold FL1 passes into candidate B. Source matching,
tensor sector, cold sector and nonlinear gravitational constraints are not
certified here. All calculations use signature (-,+,+,+), c=1.

Search scope: Sol61, campaign_fresh_gravity, fable_independent_2026,
qwen_claude_field_theory and real_research, querying advected labels, formation
memory, Clebsch and multiplier Hamiltonians. CFG48 G3 already distinguishes
prescribed advected labels (causal but initial-data postulates) from eliminated
path-dependent history (advanced residuals). CFG60 A17/A18 preserves that scope.
Thus the passive-label idea is **not novel**. New relative to the located
records are the constrained label-production reduction, the convective
perfect-square oscillator action, and its density-interpolation stiffness
obstruction. This is a bounded repository comparison, not a literature novelty
claim. CFG348 is read only; no energy reader is implemented here.

## Route A: transport is causal but does not produce ownership

Use a conserved baryon current density J^mu, n=sqrt(-g_mu_nu J^mu J^nu)/sqrt(-g)
and u^mu=J^mu/(sqrt(-g)n). Append to a standard fluid action

    S_label = integral [lambda J^mu partial_mu q + sqrt(-g) B f(q)] d^4x.

Here B denotes the signed MOND Lagrangian density in this convention; it is not
assumed to be an independent field in the final gravity theory. Variation gives
J^mu partial_mu q=0 and partial_mu(lambda J^mu)=sqrt(-g) B f'(q).
The second equation records reaction; replacing q by a prescribed external
function discards it. An exact constant OFF initial label remains OFF along
every regular baryonic trajectory. It cannot become ON merely because the
trajectory collapses. This is a characteristic uniqueness statement, not a
finite simulation. It extends only until a smooth timelike single-fluid
trajectory description breaks down. Stars require a phase-space distribution
or distinct streams; baryon-current advection does not derive merger ownership.

One local attempt to create labels is to add -sqrt(-g)lambda n R(n,q), giving
u dot partial q=R. With fixed homogeneous current J^0=J>0 in a box,

    L = J lambda qdot - J lambda R(q) + B f(q),
    p_q = J lambda, p_lambda=0,
    H = p_q R(q) - B f(q).

The two primary constraints have Poisson bracket magnitude J and determinant
J^2: they are second class and eliminate lambda,p_lambda, not q,p_q. Hence,
for R(q) nonzero at an admissible q and unconstrained real p_q, this reduced
internal Hamiltonian is unbounded below. The explicit R=.1,q=.5,Bf=.005
counterfamily is saved in results.json. R=0 is an important control: ordinary
advection has H independent of p_q and this objection does **not** apply.

Scope: this proves the fixed-current minimal-production completion has an
unbounded internal Hamiltonian. It does not prove every constrained fluid or
GR completion is unstable, or rule out sign-restricted species populations,
open-system Schwinger-Keldysh dynamics, a bath, or genuine positive kinetic
internal states. Additional constraints must be derived, not assumed to fix p_q.
A GR Hamiltonian constraint alone was not used as a substitute for that derivation.

## Route B: a conservative internal oscillator evades spatial-range obstruction

Change the premise from a freely propagating scalar to a local internal state
carried by baryons. Let I,K>0 and append

    L_int = n I/2 (u^mu partial_mu q)^2 - n K/2 [q-Q(n/nbar)]^2,
    L_gate = B f(q).

Q and f are dimensionless smooth functions with flat OFF and ON plateaus.
Choose Q=0 near n/nbar=1 and Q=1 well inside a dense bound system; f=0 near q=0
and f=1 near q=1. The numerical control uses the C^2 quintic smoothstep,
10x^3-15x^4+6x^5 on [0,1], constant outside. A C-infinity replacement leaves
the endpoint theorem intact but was not numerically tested. Thresholds,
profile widths, K and I are new inputs, not framework predictions. nbar is
provisionally a baryonic leaf-average reference. A prescribed time-dependent
nbar is an external control, not a closed covariant action. A fully varied
leaf average can be diff-safe on a supplied khronon foliation, but its global
variation is still required in the assembled theory.

At q=Q and u dot partial q=0, both perfect-square factors vanish. L_int and
its first variation with respect to every field, metric and current vanish.
Consequently its stress vanishes on this branch even when Q depends on a
varied leaf average. On FRW, Q=0 in a finite density neighborhood and q=0:
the internal oscillator has positive quadratic kinetic/potential terms and
zero *linear* stress; f is exactly zero on a finite q neighborhood. This is
an exact unexcited OFF branch of the appended sector. Excited oscillator
initial data have positive quadratic energy and gravitate. Neither their
absence nor primordial excitation is predicted. No full growth ODE is claimed.
In a stationary saturated region q=1, the appended internal stress and
f' reaction vanish; L_gate becomes the original MOND sector. This does not
derive its force law or the ownership boundary.

For a local homogeneous frozen-reference patch with B=0, baryon mass density
rho=nm, equilibrium q=Q(n), and ordinary positive gas compressibility,

    E_qq = nK,
    E_nq = -nK Q_n,
    E_nn = e_gas'' + nK Q_n^2,
    E_nn - E_nq^2/E_qq = e_gas''.

This exact Schur cancellation is the useful constructive step. In the local
fluid rest frame, for longitudinal displacement xi and dq, define

    A = c_gas^2 k^2, b=K/I,
    G = (n^2 K Q_n^2/m) k^2.

The nonrelativistic displacement inertia is rho=nm and the internal inertia
is nI. Their dispersion relation is

    (A+G-w)(b-w)-Gb = (A-w)(b-w)-G w = 0,
    w=omega^2.

For positive A,b and G>=0 both roots are real and positive. There is no
free-space scalar Yukawa range: q follows the material trajectory. This
construction therefore evades the particular luminal reach premise of CFG347.
It is an advected oscillator, with zero spatial propagation relative to the
fluid, not a scalar with strictly positive standalone spatial sound speed.
This is an admissible passive internal variable, not a proof of general
relativistic hyperbolicity or collisionless stream health.

Static Schur cancellation does not ensure finite-frequency gas fidelity. For
the low root connected to A at small k (and b>.9A), the exact 10% condition is

    G <= b/9 - A/10.

At large K, G/b = n^2 I Q_n^2 k^2/m: I sets a residual response cost which cannot
be suppressed merely by increasing K. Passing this bound requires specifying
physical I,K and checking every relevant k and background. No fitted physical
point is supplied by the dimensionless control.

## Route C: restoring the MOND gate obstructs a cold, zero-cost transition

Treat B>0 as fixed in the local patch, and allow any smooth internal potential,
not just the perfect square. Suppose the physical stationary branch q_*(n)
is a smooth stable minimum, E_qq>0, across density interval [n0,n1]. Assume
exact stationary plateau energies

    E_eff(n)=mn              near n0,
    E_eff(n)=mn-B            near n1,
    E_eff(n)=min_q E(n,q).

These encode pressureless baryons and zero added internal energy on both
plateaus, with the signed frozen gate energy -B on ON. Then

    E_eff'' = E_nn - E_nq^2/E_qq.

Let h=E_eff-mn. h(n0)=0, h(n1)=-B and h'(n0)=h'(n1)=0. If h''>=0 throughout,
h' is nondecreasing from 0 to 0, hence h'=0 throughout, contradicting the
nonzero energy difference. Thus h''<0 somewhere. More quantitatively, if
L=n1-n0 and h''>=-C, then

    -B = integral_n0^n1 (n1-n) h''(n) dn >= -C L^2/2,
    sup[-h''] >= 2B/L^2.

This is a proof for the stated smooth branch, not a scan extrapolation.
At that point the two-variable energy Hessian has negative determinant;
with positive diagonal kinetic coefficients the local fluid/internal system
has a negative omega^2 mode at every nonzero k in this frozen patch. For a
finite I and positive frozen high-frequency compressibility the negative
root can approach a *finite* limit as k grows: this is not automatically a
Hadamard failure. It nonetheless refutes all-mode positive stiffness. Gravity
and source variation are not part of this reduced theorem; a constraint that
removes the negative direction or a correlated B variation may evade it.
The pressureless limit is essential. Gas pressure, a nonzero plateau energy
cost, nonlocal transport, a nondifferentiable phase transition, or a different
sign/convention of the gate energy change the premises. Reversing the sign
of the nonzero step still forces both curvature signs under zero endpoint
slopes, so there is still a negative region, although the stated quantitative
bound is for a downward step.

For the explicit perfect-square E=e(n)+nK(q-Q)^2/2-Bf(q),

    E_qq=nK-B f'',
    E_nq=K(q-Q)-nKQ_n,
    E_nn=e''-2K(q-Q)Q_n+nKQ_n^2-nK(q-Q)Q_nn.

The script solves nK(q-Q)=Bf'(q), then retains every term. At B=.01,K=100,
I=.01, n in [1.01,1.99] (99 points), with e''=0, **49/99** samples have
negative Schur stiffness (minimum -0.18836), while scalar stiffness remains
positive everywhere (minimum across all runs 100.99999). A pressure control
e''=.5 restores positive Schur stiffness at all 99 samples (minimum .31164).
A same-action finite-inertia control with e''=5, I=1e-8, the same B,K and
99 densities, and k=1,10 has positive coupled roots on all 198 points and
maximum gas-mode fractional change 0.03768 (below 10%). Its low root is computed
in rationalized form to avoid cancellation. This demonstrates an actual tuned
local escape with sufficient pressure and small finite inertia, rather than
merely declaring that tuning might work. It is dimensionless and has no
astrophysical units or observationally admissible pressure assigned.
These points establish a reduced counterexample and costed controls, not an
astrophysical fit. The f' constitutive-field mixing
when B is dynamical remains absent and is explicitly unverified.

## Formation timing and conservation control

No damping is hidden in the conservative oscillator. For conserved baryon
number, a^3 n is constant on comoving FRW, so the material kinetic action has
constant homogeneous inertia a^3 n I: there is no automatic 3H Hubble friction
in q's equation. A freely propagating scalar's friction cannot be transferred
here. For the **bare internal-sector control B=0** (or a force-free f' throughout),
a density history that moves Q linearly from 0 to 1 over time T, initially
q=qdot=0, has exact solution during the ramp q=t/T-sin(omega t)/(omega T), omega=sqrt(K/I).
Afterward its persistent amplitude around 1 is

    a=2|sin(omega T/2)|/(omega T),
    oscillator energy density=nK a^2/2.

The four controls omega T=.1,1,10,100 give amplitudes .99958,.95885,.19178,
.0052475, respectively. Slow formation can suppress excitation; rapid collapse
leaves an order-one oscillation and substantial extra stress. None relaxes
after the ramp. These analytic amplitudes do not solve a full MOND gate
crossing: generally that equation has an additional B f'(q)/(nI) force.
A full crossing trajectory and its energy transfer remain uncomputed. The driver does work on the internal sector; when Q is generated
by the fluid that work must be recovered in the fluid energy equation. The
externally prescribed ramp is a response discriminator, not an energy-conserving
collapse solution. A positive bath or two-species conversion is a possible
continuation, with its own stress/entropy and reaction budget, not a free fix.

## Self-audit and next implication

Passed: characteristic transport invariant; second-class bracket and reduced
production Hamiltonian; zero-first-variation branch; exact Schur cancellation
at B=0; finite-frequency determinant/fidelity boundary; smooth cold-transition
obstruction; explicit full potential Hessian counterexample; pressure and
formation controls. Review is self-review, not fresh independent endorsement.

Not addressed: full mean-density variation, baryon/gravity constrained
characteristics including delta B f', collisionless multistream evolution,
merger ownership, formation initial data, damping reservoir, physical parameter
fit, cold distribution and source matching. The algebraic cold-sector target
W=[1-F/P]_+ supplied by the parallel cold lane is not obtained from Q(n/nbar)
or these labels: it depends on cumulative cold/phantom distributions and
requires its own variational source/reaction map. These routes cannot be pooled.

The next concrete implication is to derive the *same* internal-state action's
full constrained high-k transition Hessian with a varied baryonic leaf average
and the dynamical MOND constitutive field. If its negative frozen direction is
physical, choose and fund a nonzero plateau energy or compressibility/bath
before scoring gas fidelity and formation timing. If constraints remove it,
exhibit that reduction explicitly. A passive transported label is already
closed as a label-production mechanism from homogeneous OFF data. The minimal
unconstrained production completion is obstructed within its stated scope.
The positive oscillator route remains open with the full transition coupling
as the first unresolved arrow; it has not passed a bound-system dataset.

## Reproduction and provenance

Run `python3 sol61_push/main_theory/breakthrough_2026_10_05/formation_checks.py`.
The authoritative final evidence is `run_final_b/results.json`, with outer
`run_final_b/manifest.json`, `stdout.txt`, `stderr.txt`, and `contract.json`.
The original `run_final/` is retained as the pre-review checkpoint. Peer
review clarified the ramp's B=0 scope; `run_final_b/` records the corrected
comments and contract with no mathematical implementation change. The
standard computation-audit bounded runner completed and its manifest was
validated against the repository root. The final result includes input SHA256
hashes, observed Git HEAD, Python/SymPy/NumPy/SciPy versions, all 297 transition
rows, 198 costed fidelity rows and ramp controls. `results.json` is an earlier
interactive checkpoint; its script hash predates final provenance support and
it is not the final evidence record.
The mathematical claims are exact identities/proofs; the numerical assertion
is only the saved finite range with double precision root bracketing.
An initial execution completed its mathematical checks but failed JSON encoding
on a NumPy integer count; casting the count to int fixed serialization, with
no mathematical or numerical criterion changed. No failed physics control
was erased. No commits or global research ledgers were modified.
