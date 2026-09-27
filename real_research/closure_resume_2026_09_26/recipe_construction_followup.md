# Exact-exponential C-H/K scalar repair calculation — 2026-09-26

**Result:** positive clock inertia can stabilize a finite momentum range even
when the exponential kernel has negative longitudinal response. The precise
range and its first singular boundary can be derived from the existing scalar
action. A larger-inertia example is healthy and subluminal on a bounded
acceleration branch, but it does not satisfy the recipe's static/PPN requirements.
These are constructive linear calculations, not a finished relativistic theory.

This follows up `recipe_audit.md`. It corrects any inference that `C_L<0` alone
implies instability for every clock coupling and every momentum. The exact
exponential law remains the target; no substitute kernel is used below.

## Source, variables and scope

Use `real_research/g03_audit_2026/L340_filtered_khronon_completion.py:137–151`
with its extra couplings `a2=a3=g=0`, and the real-time scalar action in
`qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md`
under “There is a second concrete warning,” plus L340's two action terms.
The L340 source SHA-256 is
`b8e52d88c2c3190a015d39a0df2b8f8343ca14164e2f414a289362003a4df1a2`.
The review began at HEAD `4e16ccf585f6fcc775a2f9d62ac30d329212e0af`.
Concurrent external work advanced HEAD to
`03524d209b7ca0c3900f47ccf5dfe42f9187d7c3` before the recorded run. The L340
and C-H source hashes remained unchanged; the run manifest pins both.

Set `A=alpha_c`, `B=c2`, and use `k>0`, `B>0`. Set `c=1` in this local
calculation; the speed ratios below are relative to the physical metric cone.
`C` is one eigenvalue of the frozen filtered constitutive response at the
chosen nonzero background. It is not a new free scalar field. Keep the lapse
`phi`, spatial potential `psi`, shift `beta` and auxiliary `U` independent.

The calculation is a frozen-coefficient principal block. It does not include
the lower-order negative-density terms, gate variations, changing-background
terms or the full nonlinear constraints. No conclusion here treats `k=0` as
the limit of an eliminated `k!=0` system. This block has a scalar mode; its
full gravitational/matter classification remains a separate recipe obligation.

## Independent action reduction and dispersion relation

The real-time quadratic Lagrangian, with the common positive gravitational
prefactor suppressed, is

\[
\begin{aligned}
L_2={}&-6\dot\psi^2+4k^2\beta\dot\psi
+2k^2\psi^2-4k^2\phi\psi
+2k^2(U-\phi)^2+2k^2 C U^2\\
&-B(3\dot\psi-k^2\beta)^2+A k^2\phi^2.
\end{aligned}
\]

Define `D=A+(A+2)C` and `N=2−A(1+C)`. When `D!=0`, the three auxiliary
equations give

\[
\beta=\frac{2+3B}{Bk^2}\dot\psi,\qquad
\phi=\frac{2(1+C)}D\psi,\qquad U=\frac2D\psi.
\]

Substitution yields

\[
\boxed{L_{\rm red}=\frac{2(2+3B)}B\dot\psi^2
-2k^2\frac ND\psi^2},\qquad
\boxed{\frac{\omega^2}{k^2}=\frac{BN}{(2+3B)D}}.
\]

Thus the reduced time kinetic coefficient is positive for `B>0`. The exact
strict stability condition on this regular block is `N/D>0`; it is not simply
`C>0`. A fresh independent Fourier calculation of L340's four-by-four matrix
gives

\[
\det M=64k^8\{BN k^2-(2+3B)D\omega^2\},
\]

agreeing with the action elimination. Both identities were checked symbolically
with SymPy, exit 0. At `D=0` the eliminated equations are singular; the apparent
divergence in speed must not be declared a regular physical limit. `N=0` is a
zero-speed boundary, not part of the strict healthy branch.

For `0<A<2`, the ordinary branch containing `C=0` is precisely

\[
\boxed{-\frac A{A+2}<C<\frac2A-1}.
\]

The upper bound matters in deep MOND: constant nonzero `A` is not automatically
harmless when the positive transverse coefficient becomes arbitrarily large.

## Heat filter: exact stable band and first dangerous momentum

For the exact exponential spherical law, use `x=g/a0>1` and

\[
C_{L,0}=-d(x),\qquad
d(x)=\frac{x-1}{e^x+x-1}>0.
\]

On the frozen flat background a heat filter supplies two factors
`S(k)=exp(−xi²k²/2)`, so the block coefficient is

\[
C(k)=-d\,e^{-\xi^2k^2}.
\]

For `0<A<2`, `N>0` throughout this negative-`C` sector. Therefore

\[
\omega^2>0\quad\Longleftrightarrow\quad
(A+2)d e^{-\xi^2k^2}<A.
\]

If `(A+2)d>A`, decreasing momentum from the stable high-frequency region first
reaches the auxiliary singularity at

\[
\boxed{k_*\xi=\sqrt{\log\frac{(A+2)d}{A}}}.
\]

Modes with `k>k_*` are stable in this block; those with `0<k<k_*` have negative
`omega²` and positive reduced kinetic coefficient. Changing positive `B`
changes the growth rate but not this sign boundary. Setting `B=0` does not
provide the same solution: elimination fails and the original frozen-phantom
response returns.

At `x=2`, `d=1/(e²+1)`. Illustrative numbers, freshly evaluated:

| `A` | `k_* xi` | Longest allowed period `2π/k_*` in units of `xi` |
|---|---:|---:|
| `9.6240479669e−14` | 5.342111 | 1.176162 |
| `1e−9` | 4.391980 | 1.430604 |
| `3.2e−9` | 4.257503 | 1.475791 |

A compact cubic domain with period `L` has `k_min=2π/L`; imposing
`L<2π/k_*` removes the unstable nonzero modes in this idealized block. This
is a real finite-domain repair, not an all-domain theorem. For `A=1e−9` and
`xi=0.031 pc`, it demands `L<0.04435 pc`; a generic galactic domain does not
meet that condition. Enlarging `xi` to meet a chosen `L` also changes the
static filtering. That change must be derived alongside the exact static law.

## Larger clock inertia: an actual bounded healthy witness

Stability of this negative branch for every positive momentum requires
`A>=2d/(1−d)` (strict inequality also keeps the `k→0` block nonsingular).
The exponential identity simplifies this to

\[
\frac{2d(x)}{1-d(x)}=2(x-1)e^{-x},\qquad
\max_{x>1}2(x-1)e^{-x}=2e^{-2}\approx0.2706705665.
\]

The maximum occurs at `x=2`, since the derivative is `2(2−x)e^(−x)`.
Choosing `A=0.3`, `B=0.01` therefore supplies positive kinetic and gradient
terms for the whole negative-longitudinal sector, including its unfiltered
endpoint. It is also subluminal there: the maximal squared speed is
`0.3309895765`, at `x=2` with unit filter factor.

More generally,

\[
\frac{\partial c_s^2}{\partial C}
=-\frac{4B}{(2+3B)D^2}<0.
\]

For `x>=0.2`, the exponential transverse coefficient obeys
`C_T=1/(exp(x)−1)<=4.516656` and both directional coefficients after filtering
lie between `−1/(e²+1)` and `4.516656`. The above witness has
`2/A−1=5.666667`, so **every coefficient in this bounded background/momentum
domain has `0<c_s²<=0.330990` and positive reduced kinetic coefficient**.
This is a constructive counterexample to “negative `C` is always fatal.”

An exact rational envelope avoids relying on the displayed decimal endpoints:
for `x>=1/5`, `exp(x)>1+x` implies `C_T<5`, while `exp(2)>7` implies
`d(x)<=1/(exp(2)+1)<1/8`. The latter exponential bound follows by summing
its first five Taylor terms, whose sum is 7, and retaining the positive
remainder. Thus the entire response lies in `−1/8<=C<=5`. On that interval,
the chosen `A=3/10`, `B=1/100` give

\[
K_\psi=406,\qquad D\ge\frac1{80},\qquad N\ge\frac15,
\qquad \frac1{11977}\le c_s^2\le\frac{139}{203}<1.
\]

The `D,N` bounds are affine endpoint bounds; the speed bounds follow from
the strictly negative derivative above. The recorded exact computation checks
these endpoints and the derivative, so the uniform interval statement has a
stated analytic reduction rather than a sampling argument.

It does not complete the requested theory. The static L340 response is
`psi/psi_N=(1+C)/(1−A(1+C)/2)`, so changing `A` distorts the constitutive
response unless the static construction is repaired simultaneously. Under the
same khronometric PPN formulas used in L340/KM3, `alpha1=−4A=−1.2`, well outside
their accepted window. Finally, the unfiltered transverse sector loses strict
stability for `x<=−log(1−A/2)=0.1625189295`. The bounded witness therefore
requires new compatibility work; it is not a replacement success criterion.

## Subluminality in the small-inertia repaired band

When `C<0` but `D>0`, one has `D<A` and `N>2−A`, hence

\[
c_s^2>\frac{B(2-A)}{(2+3B)A}.
\]

For `A<1/2`, even this lower bound exceeds one if
`B>A/(1−2A)`. At `A=1e−9`, `B=0.01`, its value is approximately
`9.8522167e6`. Thus the heat filter's stable high-frequency band does not also
solve metric-cone subluminality with L340's small-`A`, positive-`B` values.
The exact condition on a stable regular branch is

\[
c_s^2\le1\quad\Longleftrightarrow\quad
C\ge\frac{B-A-2AB}{A+2+2AB+3B}.
\]

This additional inequality can guide a finite-band redesign. It must be solved
together with static response, source tracking and PPN rather than selecting
`A`, `B` and the kernel independently.

## Verification and next construction

Fresh in-memory SymPy calculations independently derived the action reduction
and matrix determinant, checked their equality, simplified the inertia threshold
and differentiated the exact response. A separate elementary numeric evaluation
produced the table and witness values. Every command exited 0; no simulation,
existing script mutation, dependency installation or source-data rewrite occurred.

The reusable check is `recipe_followup_check.py`, with explicit contract
`recipe_followup_contract.json` and results/logs in `recipe_followup_run/`.
The bounded runner recorded Python 3.9.6, SymPy 1.14.0, exact symbolic arithmetic
apart from the labeled three-row binary64 table, no randomness, a 30-second wall
limit, 20-second CPU limit, 100000-byte output limit and cooperative single-thread
cap. No hard memory or affinity cap was requested for this small symbolic job.
It completed in 1.955 seconds with exit 0: twelve zero residuals and the negative
control `c_s²=−8/203`. Inputs were unchanged before/after execution.

`recipe_followup_run/manifest.json` passed the skill validator with `--root`
against the current checkout. Its recorded argv is
`python3 real_research/closure_resume_2026_09_26/recipe_followup_check.py`;
to reproduce provenance, use the same contract and inputs with
`computation-audit/scripts/run_experiment.py` and a fresh output directory
(also change the script's output destination for that new run). The output
SHA-256 is `37f4cfa08c41082f05c3056c8988fdec4da4f380b1e9083ef18182b931895dee`.

The external HEAD update added `real_research/extra_crispy_2026/README.md`, SHA-256
`2634cdbbeb3298d6b1a21c6b297541520eacc1e6e93b59b0ff13c26f7fcc4f96`, with an
explicit G8 PASS heading and new algebra certificates. The underlying XC1 source
is unchanged at `66994148e050d18f25f2fe380efb763da21bec25ccb8cdefe909ab7296ac183d`.
The README itself still lists uncomputed filter metric-variation vertices and
nonlinear well-posedness. Those new algebra certificates therefore do not remove
the full-action scope restriction recorded in `recipe_audit.md`. The README's
phrase that the filter removes C-H “exactly” at finite large momentum must also
be read as an approximation: `exp(−xi²k²)>0` for every finite real `k`.

**Next constructive calculation:** adjust the action's auxiliary weights and
clock coefficients jointly so that the independently varied static metric still
has the exact exponential response, then rederive `D`, `N` and the scalar
kinetic coefficient. The present calculation supplies explicit targets for that
repair, including its causal bound. A coefficient substitution made only in the
dispersion formula is insufficient because it also changes the static equations,
and field-dependent coefficients produce further variations.

This follow-up owns this report and the uniquely named `recipe_followup_*`
script, contract and run artifacts. `recipe_audit.md`, the recipe and the
canonical specification were not changed by this follow-up. Mathematical
self-review covered the new equations, domains, sign conditions and source
locators; no unresolved notation error was found.
