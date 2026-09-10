# Shared-action clock: pointwise success, preservation obstruction

This continues the nonaffine-clock action at commit `1e8f58095`, and reviews
Claude/Fable's newer `7295d6a55` (L124) and `d0db626c4` (L125).
**The complete gravity theory is OPEN.**
No dark-matter particles or per-galaxy acceleration scale are added. Carl
Zimmerman's global dark-energy/acceleration-scale proposal and explicit-clock
direction motivate this search. The fitted coefficient `kappa=1/2` is an
input, not a result of these calculations. The derivative-conformal action
class itself is not claimed new.

## Same action throughout

In the conventions of the preceding varied-action package,

\[
 S=\int d^4x\sqrt{-g}\left[F(X)R+
 \frac{3F_X^2}{2F}(\nabla X)^2+P(X)-G(X)\Box\phi\right]+S_m[g,\psi],
 \qquad X=-\frac12\nabla_\mu\phi\nabla^\mu\phi.
\]

Here `G(X)` is the braiding function, not Newton's constant or the exponential
MOND primitive. The clock is explicit; it is not claimed to be a nondynamical
auxiliary. The target exterior uses the fixed exponential `mu(y)=1-exp(-y)`
in units with one global `a0=1`. The two `epsilon` values are exterior mass
parameters, **not yet calibrated to baryonic interiors or measured G_N**.
No empirical galaxy or CMB likelihood is computed in this package.

The target metric is input to an inverse varied-equation calculation. Passing
the inverse equations at a point is not a derivation of a universal sourced
MOND solution, independent Phi/Psi predictions, or acceptable PPN parameters.

## The new constraint on the search

At the same clock value `X`, two exteriors must share `F,F_X,P,P_X,G_X` and
their derivatives. Write `f=F_X`, `j=F_XX`, and `w=f X'`, where prime is a
radial derivative. The exact reduced inverse in `structure/` supplies

\[
 P=\mathcal P(F,X,y,U,w),\qquad
 P_X=f\,\mathcal K(F,X,y,U,w),\qquad
 G_X=f\,\Gamma(F,X,y,U,w).
\]

The functions on the right contain neither `f` nor `j`. Along the actual
shared action flow,

\[
 D_X=L_0+fL_1+j\partial_f.
\]

Let `Delta` denote the difference between the two exteriors and define the
two-vectors

\[
 A=L_0\Delta(\mathcal K,\Gamma),\qquad
 B=L_1\Delta(\mathcal K,\Gamma),\qquad E=A+fB.
\]

Common lower jets require `Delta P=Delta K=Delta Gamma=0`. Common second
jets additionally require `E=0`. The next preservation equations are

\[
 \boxed{N+jB=0,\qquad
 N=(L_0+fL_1)(A+fB)\ \text{with f held fixed}.}
\]

Thus, when a component of `B` is nonzero,

\[
 \boxed{N_1B_2-N_2B_1=0}
\]

is necessary and sufficient for a common `j` **at this preservation stage**.
The conditional Lean certificate extends the common-control criterion to any
indexed family of equations and handles zero-control exceptions. It does
not formalize the entire physical action, numerical roots, or Dirac analysis.
On a matched lower/second-jet surface, `F_XXX` multiplies an already vanishing
lower mismatch; it cannot repair failure of this next equation.

These are action-function compatibility equations, **not** a substitute for
Hamiltonian constraint preservation. Both are required in a complete theory.

## Construction attempt and falsification

The first bounded searches were not decisive: holding `f=.05` or limiting
`|w|` too tightly produced no matches. Eliminating common pressure and solving
for the shared `f` instead found genuine numerical initial matches. This
demonstrates why failed optimization alone was not a no-go.

For `F=.525`, `X=.5`, `epsilon=(1e-6,2e-6)`, `y1=.1`, `U1=3e-8`, one
high-precision initial solution is approximately

\[
 f=259.6853685595673,\quad
 (w_1,w_2)=(-20.8245196960961,-27.4430902101842),\quad
 y_2=.1537936934617971,\quad U_2=5.2011649199890\times10^{-8}.
\]

The two values required of the **same** next coefficient disagree:

\[
 j_{\mathcal K}=-1.458331810665345\times10^9,\qquad
 j_\Gamma=-1.511505199377258\times10^9.
\]

The normalized nonzero determinant is approximately `-0.000538829413840944`.
Independent arbitrary-precision computations and finite differences of the
original varied inverse check this obstruction. Choosing the first value
leaves a `Gamma`-preservation residual about `-9.809113277667745e13`.

Importantly, this point is not excluded merely by instantaneous stability:
the actual two-pencil calculation admits a common locally healthy EF
curvature interval, and `j=1e10` is a checked witness for both exteriors.
But that healthy control does not preserve the action matching. The
coefficient required by `K` preservation also fails both local health checks.

Two further initial points and a bounded continuation test the same problem.
Repeated numerical failures exclude those evaluated data, not the entire
action class. Arbitrary precision is not a rigorous interval enclosure.
The reduced `H,Gamma` search uses the nonzero-`Gamma` branch; when `Gamma=0`,
common `H` is stronger than necessary and that sector is not exhausted.
The initial-curvature elimination also excludes a zero normalization vector;
such solver exceptions are not no-go results. Next-control zero-vector
sectors are handled separately, including the case where every control works.
The structural lower-map calculation also rules out a proposed shortcut:
lower-jet matching does not generically force equal exterior mass parameters.

## Claude's latest update

`7295d6a55` changes only `Mondlean.lean` and its README. Its new L124 master
certificate conjoins prior conditional statements. Positive exponential
eigenvalues support the monotonic radial parametrization used here. The new
conjunction supplies no universal action functions, sourced solution, full
constraint algebra, or Boltzmann/CMB fit. In particular, the annotations
around the theorem are stronger physical language than its algebraic type.
We reuse the relevant kernel facts without treating the conjunction as
certification of a full theory. No colleague's work is overwritten.

L125 arrived during this run. Its further claim that ordered clustering
cutoffs force galaxy-scale clustering confuses two different wavenumbers.
The exact counterexample and conditional Lean proof in `latest_review/`
retain the valid same-mode ordering and refute the claimed logical leap.
Thus this argument does not establish L125's universal hybrid exclusion.
It also does not give our clock candidate a CMB pass; no extra particle sector
is being added. See that subpackage's report for the separate physical
free-streaming definition, source check, literal-script rerun and non-claims.

## Next unavoidable calculation

Find a regular common-action seed satisfying **both** the next tangency
determinant and the shared health interval, then preserve all remaining
compatibility equations rather than tuning a fresh function per radius.
If no such seed exists, prove that on an explicitly delimited branch with
analytic inequalities or rigorous interval bounds. The seven numerical
continuation points do not supply that theorem.

After that gate: continue a common solution across masses, derive regular
baryonic interiors and G_N, join the same functions to expanding FLRW, derive
the complete physical-frame perturbations and constraint algebra, and run a
Boltzmann/CMB likelihood. PPN, strong coupling, zero modes, zero-field limits,
lensing and source matching remain mandatory; none is replaced by these
pointwise certificates. Global constant `a0` alone is not a CMB-safe switch.

## Reproduction and status

`run_suite.py` records commands, outputs and exit statuses. The bounded run
contract and manifests pin the source and dependency files. The separate
`structure/`, `health/`, and `health_search/` reports distinguish exact
identities, conditional Lean lemmas and numerical evidence.

The strict `high_precision_gate.py --require-next-preservation` command must
reject these seeds. An ordinary evidence run may exit zero while reporting
a failed physics gate; **script success is not gravity certification**.

Status: **OPEN action class; evaluated matched seeds fail next preservation.**
