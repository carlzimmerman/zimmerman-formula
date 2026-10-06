# Independent cold-lane audit

Primary verdict: **refuted, with a valid counterexample**, for the normalized
claim that the unchanged FL1 static gate-on action can realize every radial
maximum B+max(F,P) using a nonnegative material-wave density. The cold report's
scoped obstruction and edge-only qualifications are correct. No actionable
mathematical error was found. This is an independent derivation by the main
lane agent, not execution of the author's script or a full gravity audit.

## Raw object and dependencies

I read REPORT.md, source_matching.py, the retained action in
real_research/dark_fluid_2026/FL1_order_parameter.py, CFG4_README T5, and
CFG45_rule_readings' distinct radial-max and edge-reduced readings.
FL1 has a complex nonrelativistic field with rho_c=m(a^2+b^2), m>0. Its
kinetic action is b a_t-a b_t-(a_x^2+b_x^2)/(2m). Its dark-density potential
coupling before elimination is -rho_c(Phi+lambda/2). Thus the dark force cannot
be inferred from the metric-only term -rho_c Phi.

Independently rebuilt the static one-dimensional auxiliary Lagrangian and
applied Euler variation while auxiliaries remained independent. SymPy gives

    2 u''-8piG(rho_b+rho_c)=0,
    v''-4piG rho_c=0,
    w''-u''+v''=0,
    Psi''+lambda''=0,
    2Phi''-2u''-Psi''=0.

All five exact residuals vanish. The isotropic three-dimensional version uses
Laplacians and the same integrations by parts; dropping boundary terms requires
appropriate fixed/matched variations. Matching the residual harmonic modes
then gives w=u-v, lambda=-Psi, Phi=u+Psi/2. Nonzero harmonic differences are
not excluded by these PDEs alone: these are genuine boundary hypotheses.

Consequently w is baryon-sourced, cold sees Phi+lambda/2=u, and baryons see
Phi=u+chi with chi=Psi/2. With chi independently calibrated to the stipulated
baryonic phantom and spherical matched boundaries, the effective enclosed
baryon-source mass is B+C+P. This conclusion applies to f=1,M2=0 only, not to
a switch edge or variable f. The unspecified q in the cold script does not
itself prove that a particular MOND kernel is realized; the report explicitly
conditions on that calibration.

For real potential u, the Schrodinger equation gives
rho_c,t+div Im(psi*grad psi)=0 in hbar=1 units. Positivity follows directly
from m|psi|^2, not from continuity. At nodes the wave current remains regular;
no phase-only velocity is needed. Vanishing flux conserves total mass. The
Newtonian cross interaction -G integral rho_b rho_c/|x-y| produces reciprocal
forces. The lack of a cold argument in the eliminated baryonic kernel does
not remove the Newtonian cold gravity sourced in u.

## Positivity obstruction and counterexample

Subtracting B+P from B+max(F,P) forces exactly C=[F-P]_+. Every positive
spherical material measure has nondecreasing enclosed mass. On intervals
F>P, C'=F'-P'; for absolutely continuous inputs the positive-part derivative
has no additional negative measure at equality. A nondecreasing right-continuous
C with proper origin value defines a positive radial mass measure, but this
is not sufficient for a smooth finite-hbar stationary wave. The report keeps
that distinction.

For the claimed G=a0=B=1 P2 exterior, g_N=1/r^2 and
r^2 sqrt(g_N^2+a0 g_N)-1=sqrt(1+r^2)-1. This confirms the report's P, including
its P2 restriction. The Plummer F=5.36 r^3/(1+r^2)^(3/2) has density derivative
3(5.36)r^2/(1+r^2)^(5/2)>0 and finite total mass 5.36.
I recomputed independently:

    C(2)=2.59923581750785,
    C(4)=1.77097795158608,
    C(6)=0.0614150789626038,
    C'(4)=-0.754227048209873.

Already the two radii 2 and 4 furnish the smallest displayed counterexample:
a positive annulus would have negative mass C(4)-C(2). These exterior radii
must be inside the active plateau; an edge beyond 6 is a sufficient choice.
A compact baryon source inside radius 2 supplies the exterior B=1 premise.
No claim about arbitrary kernels or all T5 meanings follows.

## Edge repair and changed-action gate

At R=4, s=1-P(R)/F(R)=0.361860994739681 and C=sF has positive density and
finite total 1.93957493180469. P+C=F at R exactly. At r=2 I recover
acceleration ratio .749469935608131, velocity ratio .865719316873622,
and log10 velocity residual -.0626228919224396 dex.
This is an aperture match with a different interior force profile, not a
radial maximum. T5's global/edge bookkeeping does not automatically impose
radial max; CFG45 explicitly supplies the latter as a distinct reading.
The report appropriately refuses to promote this example into a universal
T5 failure or dynamically selected wave halo.

With fixed ordered enclosed-mass labels and conserved angular momentum,
linearizing rddot=j^2/r^3-G[B+C]/r^2 about
j^2=G[B+C]r gives radial stiffness G[B+C]/r^3>0. This is a classical
ordered-shell test only. Neither quantum-pressure equilibrium nor nonradial
or collective stability follows. The Plummer excess surface density
C_total S^2/[pi(S^2+h^2)^2] follows from the Newtonian projected profile;
a relativistic lensing dictionary is not provided and is not claimed.

The alternative reservoir identity F+WP=max(F,P), W=[1-F/P]_+, is correct
for nonnegative F,P with the stated P=0 convention. It is purely a cumulative
mass identity. On 0<F<P, varying W(F,P)E0 adds -E0/P in the F direction;
there are generally extra mixed and spatial-derivative terms. Independently
expanding the toy E0=-B^2/r, P=Br gives
E_gate=-B^2/r+BD/r^2, mixed B,D derivative 1/r^2, and the difference between
its full radial derivative and W dE0/dr is -BD/r^3. This verifies the chain
rule in the toy, not an actual MOND action. In a field action, F,P are nonlocal
functionals; their functional derivatives and boundary conditions remain
required. No gate-transition result follows from the f=1 plateau calculation.

## Obligation matrix

- Plateau retained-action variations and wave force dictionary: passed with
  matched harmonic boundary modes.
- Reciprocal baryon/cold source reaction and positive wave mass: passed in the
  stated nonrelativistic static sector.
- Necessary monotonicity criterion and finite positive-budget counterexample:
  passed, with active-region and P2 restrictions.
- Edge-only finite positive measure and radial prediction: passed; wave
  equilibrium and selection remain not addressed.
- Reservoir gate algebra and naive-energy derivative: passed at their stated
  algebraic/toy scope; conserved completed gate action not addressed.
- Full action, cosmology, cold abundance, formation, mergers and relativistic
  lensing: not addressed here. The report does not claim them.

## Inputs and reproduction

Independent calculation used an inline Python/SymPy reconstruction and direct
scalar arithmetic, writing no cold files and importing/executing none of the
cold author's scripts. This is exact-symbolic proof checking and a tiny direct
floating cross-check, not a fresh rerun of all 21 author checks. Input SHA256:

    REPORT.md: d53fd7e3879e9f3daf0eedc40f43a2fb54b42e893f2efcc0430998ae17f7a226
    source_matching.py: f10e1c4c8165b98321af561a558fa5f095800e9dcb27dcd2668a60b599259a0f
    FL1_order_parameter.py: 6bc3f0edf8eda07796f186d1955115e14db87e2271dcd5f1909ea3433e25f289
    CFG4_README.md: 9c772cb9d0495ac55e516f912e3ce83aa7b7a28836e7336767b78a97d3dca0a9
    CFG45_rule_readings.py: 03c2ef6a3258e320b7b32c666c230403c3298d5a6976f55b839cc03518689030

The exact remaining implication is a reciprocal changed action or independently
selected positive wave state implementing an explicitly chosen T5 reading.
The unchanged plateau radial prescription is obstructed for the displayed
witness; edge-only bookkeeping remains possible at the measure level.
