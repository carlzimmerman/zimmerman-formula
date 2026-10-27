# FGF049 independent full proof audit

Normalized claim: for every specified fixed coefficient/background choice,
either separately normalized a_ref, any fixed Gamma>0, and all sufficiently
large integer N satisfying the author's explicit physical-domain thresholds,
no positive classical solution of the exact four coupled Q/scale/isothermal
fluid equations with the unchanged C1,1 velocity profile can cover the stated
cone through T_N=B_*/omega while both full-interval budgets

    integral_0^T_N sup_{K_t}|g| dt <= Gamma V,
    integral_0^T_N sup_{K_t}(-g_x)_+ dt <= eta omega

hold. Here V=v0 N, ell=L/N^3, omega=V/ell, and B_*,eta are the exact constants
in author (1.3), not fitted or N-dependent physical parameters.

Primary verdict: **conditional on a named input**, namely the full-interval
feedback budgets (F),(D), for the requested actual-family upper-lifespan
conclusion. The displayed conditional nonexistence-through-time theorem is
proved under its stated hypotheses. No correction to the author's proof is
required. The actual coupled family has not been shown to satisfy those
hypotheses beyond the shorter FGF048 interval. This audit does not accept an
unconditional upper lifespan or an actual maximal-endpoint classification.

## Exact evidence and independence

Author derivation: deepseek_push/astra_spawn_ideas/fresh_gravity_followups/
results/FGF-049/fgf049_run_001/DERIVATION.md, SHA256
187330b696fa88fe9300e974d8870a053f524d25852ffda1957a6be649696f5e.
Author result SHA256:
34f62b2da6894e06e47e62da0fb042dca88e91b97dcb395bd13633385a88bdde.
These exact pins were verified before reading the new author derivation.

The reviewer froze INDEPENDENT_DERIVATION.md at
2026-10-06T05:42:47.875713+00:00 with SHA256
3a8633989256cfe94b6ddfefcf0ed1384399f86009e54aa3bc55daf2d803eb4c.
It remains unchanged. That route used a stronger pointwise adverse-gradient
bound and a bounded-force hypothesis. The author's weaker integrated budgets
and its future-tail correction were first inspected after freeze. They were
independently reconstructed in this audit; the earlier file was not edited to
appear to predict them. No new root or other reviewer proof was read.

Old source texts were read before their individual pin check; the task and
all nine ancestry pins subsequently matched before the independent derivation.
This differs from the author's own pre-read hash chronology and is disclosed.
The exact first author-read clock time was not separately recorded; the later
AUTHOR_EXPOSURE.json records the actual ordering, pinned bytes, and record time.

## Dependency graph

1. Exact fluid equations, positive density and retained sound speed c>0
   imply the r,s characteristic equations. [Internal algebra; passed.]
2. C1 characteristic label differentiation and density weighting give the
   exact moving-force gradient identities. [Internal proof; passed.]
3. (F), the explicitly chosen speed S_N and large-N domain threshold imply
   backward-cone and selected-forward-characteristic containment. [Conditional
   input plus internal proof; passed under (F).]
4. (D) bounds the upper weighted-gradient envelope and inverse density.
   [Conditional input plus strict bootstrap; passed under (D).]
5. The future adverse-budget correction yields a positive Riccati variable,
   hence a negative reciprocal at T_N, a contradiction. [Internal proof;
   passed under prior items.]
6. Exact field/density identities identify the density derivative and scale
   contributions that would have to establish (F),(D). [Internal identities;
   passed. The proposed full-interval bound is not supplied.]
7. Separately, compact state, positive chart margins, bounded first gradients,
   and a buffered domain propagate the C1,1 seminorm and give a compatible
   C1 trace. The pinned accepted local construction then restarts it.
   [Conditional internal proposition plus accepted local construction; passed
   within the explicit extra hypotheses, not as an actual endpoint claim.]
8. Full equations imply local energy/flux balance, moving boundary terms and
   the exact hydrostatic control. [Internal identities; passed.]

There is no external theorem, numerical-evidence or author-agreement leaf.
The FGF047/048 local construction and old FGF045 formulas are accepted pinned
internal ancestry; the old fixed-force upper theorem is not used as a theorem
for the moving-field problem. The two named full-time budgets remain unchecked
assumptions for the actual family, not consequences of their shorter-time
verification.

## Obligation matrix

| Obligation | Status | Audit evidence |
|---|---|---|
| Task and nine OLD ancestry exact pins | passed | independent hash checks before derivation |
| Final author source/result, all input and artifact pins | passed | 12 inputs, six artifact-map entries, seven freeze entries |
| Exact Q source and all scale terms | passed | author (1.1),(5.1),(5.2),(5.4),(5.7) |
| Genuine C1,1 joins and C1 obstruction regularity | passed | label-Jacobian derivation requires no classical v_xx at joins |
| Retained pressure and correct weighted signs | passed | (3.1), reconstructed below |
| Conditional physical containment | passed | (F), S_N, ell+2S_N T_N<R |
| Integrated inverse-density envelope | passed | (4.1)-(4.2), strict 1.5A versus 2A margin |
| Future-tail correction and reciprocal contradiction | passed | (4.3)-(4.6), reconstructed below |
| Actual-family full-interval (F),(D) | conditional | missing source/scale/chart estimate in Section 5 |
| Coupled C1,1 propagation and buffered restart gate | passed | separate conditional proposition, (6.1) |
| Unconditional actual endpoint mechanism | not addressed | no such classification is proved or accepted |
| Full energy/flux and Reynolds terms | passed | (7.1)-(7.2) |
| Hydrostatic zero-velocity control | passed | all four equations and zero full flux |
| Both normalizations and distinct histories/laws | passed | Section 8 |
| Physical metric, photons, DOF and closure claims | out of scope | explicit exclusions |
| Mathematical proofreading | passed | no correction needed; full author Markdown mathematical bundle reviewed |

## Decisive reconstruction

With q=log(n/nref), alpha=(v+cq)_x and beta=(v-cq)_x, the actual equations
imply Dplus q=-beta and Dminus q=-alpha. Differentiating Dplus r=-g along
its C1 label flow gives Dplus alpha=-v_x alpha-g_x, with v_x=(alpha+beta)/2.
Therefore h=n^(-1/2), y=h alpha, zeta=h beta obey

    Dplus y=-y^2/(2h)-g_x h,
    Dminus zeta=-zeta^2/(2h)-g_x h,
    Dv h=(y+zeta)/4.

These identities retain pressure, omit no time-dependent force term, and
require only continuous g_x and first fluid derivatives on the hypothetical
classical slab. The derivative of a spatial source remains g_x; no g_t arises.

The source integral bounds |r|,|s| by (1+Gamma)V+cQ0 on the cone. The author's
S_N adds c, both field speed bounds and v0, giving a strict fluid-speed margin.
The field speeds obey sqrt(B_g/tau)<tau^(-1/2) for g,a>0. A lower B_g bound
is not needed for speed containment, although it matters for chart restart.
Consequently the cone bootstrap is not circular. The initial selected point
is at distance ell/sqrt(3), and ell+2S_N T_N<R leaves it strictly inside
K_t for all relevant times. The comparison footprint shrinks by O(N^-3),
not a fixed physical distance or an assumed invariant original support.

Initially alpha0=omega f'-g0/c and beta0=omega f'+g0/c. The threshold
omega>=G0/(c d_f) gives M(0)<=2d_f h0 omega=A omega. For M=max(0,sup y,
sup zeta), the exact equations give
M<=A omega+integral K_N H and H<=h0+integral M/2. Under M<2A omega,
H<=h0+A omega t<=H_*. Since eta H_*<=A/2, (D) strictly improves M to
1.5A omega. This proves the envelope without an absolute compression-gradient
bound and without any pointwise inference from (D).

On the selected plus characteristic let w_c=-y. Hydrostatics and g0>0 give
w_c(0)>=b_* omega. The author's defining correction

    u(t)=w_c(t)-H_* integral_t^T_N K_N(s) ds

has u(0)>=b_* omega-H_* eta omega>=b_* omega/2. Its derivative satisfies

    u'>=w_c^2/(2h)+K_N(H_*-h)>=w_c^2/(2h).

The sign in front of H_*K_N is positive because the differentiated integral
has a moving lower endpoint. Thus u remains positive and nondecreasing and
w_c=u+nonnegative>=u. The reciprocal inequality follows:

    1/u(t)<=2/(b_* omega)
       -log(1+A omega t/h0)/(2A omega).

The selected B_* makes the logarithm 8A/b_* at T_N. The right side is
-2/(b_* omega)<0, impossible for finite positive u. The earlier zero at
t_hat is also strictly before T_N. Only a hypothetical full slab uses the
future budget; no unknown continuation past an actual endpoint is assumed.
The sup functions are continuous on the compact moving intervals for the
stipulated C1 solution, so these integrals and differentiations are legitimate.

## Exact remaining coupled estimate

The field chart equations retain Hcal_chi(w-/+bk), the full scale source and
both Q characteristic speeds. Their spatial derivatives contain

    -(C/tau)n_x,  n_x=n q_x,

in both Q components. The fields traverse different +/-b characteristics;
equal algebraic source expressions do not mean equal integrated source values.
The inverse identity 2b g_x=xi_+-xi_- -2Hcal_chi k follows by differentiating
Rplus-Rminus=2Hcal(g,chi) and using chi_x=k. Thus the scale term is essential.
The same-point subtraction recovers the transport compatibility identity,
not a useful sign or size bound on g_x.

The density derivative identity Dv n_x=-2v_x n_x-n v_xx is correct in the
weak/difference-quotient sense for the existing C1,1 branch. Its integrating
factor yields author (5.6); the exponential and the factor n in its forcing
have not been suppressed. The weak upper density estimate n<=exp(O(N)) from
r,s is valid but does not provide useful N-uniform coefficient bounds. The
static-sign shortcut also fails exactly as stated: B_g g_x=Cn+tau p_t-B_chi k
has two further contributions of uncontrolled sign.

The missing implication is a non-circular full-interval estimate for the force
impulse and adverse-gradient integral from those coupled source, transport and
scale terms, or another sufficient comparison estimate. It must apply to each
candidate continuation until B_*/omega or an independently justified earlier
stopping event. FGF048's estimates give very small early budget consumption,
but all their coefficient/gradient bounds were proved only through small
kappa/omega. The remaining time interval cannot be reached by changing kappa
in the finished inequalities. The failure to close this estimate is not a
counterexample to compression, nor an existence theorem for a stable branch.

## Continuation, controls, and scope checks

The author's Section 6 preserves a distinction necessary for a sound endpoint
statement. On a compact positive chart, coefficient derivatives in (6.1) are
finite; bounded A_f and B_f make the inequality linear in H_f+H_z with finite
forcing. Finite initial seminorms therefore stay finite for fixed N. The
distributional time derivative of U_x then yields a C1 trace on a buffered
interior. Compatibility survives the limit, and the accepted local C1,1
construction restarts an extension of that trace. Its lifetime need not be
uniform in N. These steps do not apply if state compactness, positivity or
spatial buffer is lost. The paper states those gates, rather than silently
promoting the old frozen-force endpoint classification.

Energy signs were independently checked: fluid plus n phi contributes np;
W_t=Bp_x-Tw gives Q exchange -np-Tw/C; the full scale equation contributes
Tw/C. Both negative field fluxes in F are required. Reynolds terms at inward
cone endpoints have sum -S_N(E(right)+E(left)). No conserved cone integral or
pointwise-gradient estimate follows from initial O(N^-1) excess energy.
The stationary zero-velocity hydrostatic tuple obeys the exact four equations
and has zero full flux. It lacks the required O(omega) compressive trigger.

Separate a_ref=9.3619e-11 and 1.1279e-10 m/s^2 backgrounds may have different
constants and N thresholds. Frozen E^2=.315(1+z)^3+.685 comparisons and evolving
reference protocols remain distinct; the energy identity reviewed here is
fixed-reference only. Q is distinct from RAR, registered M and filtered MONO.
The diagnostic scale DOF supplies no physical vacuum, metric/photon/two-DOF,
criterion B, observational, cosmological or historical-novelty result.

## Checks, proofreading and next action

All proof checks are analytic. Administrative commands used cat/sed/shasum and
Python standard-library JSON/SHA256 reads. All author input, artifact and freeze
maps matched. No mathematical process, numeric sample, literature lookup,
service, installation, commit or write outside the assigned audit directory
was performed. The exact final read-only author metadata verifier was inspected
before execution. Hash agreement verifies provenance, not the theorem.

Proofread in review-only mode: author DERIVATION.md, REPORT.md,
FAILED_ESTIMATES.md and their metadata scope statements. Routine corrections:
none. Mathematical-token corrections: none. Remaining substantive issue:
the explicitly unproved full-interval feedback budgets. Markdown mathematical
displays require no LaTeX compilation. Self-review of this comparison report
checked notation, dimensions, strict bootstrap margins and conditional scope.

Strongest safe statement: accept the conditional integrated-budget obstruction
and separate sufficient coupled continuation gate. Keep the original actual
upper-lifespan and actual endpoint-classification questions open. The cheapest
next discriminating attempt is a signed estimate for the oppositely transported
n_x sources and scale/chart terms on the compression horizon, explicitly
retaining their dependence on the growing density and spatial derivatives.
