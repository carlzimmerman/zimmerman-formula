# Independent audit of the reviewer's continuum Milky Way tail lemma

Primary verdict: **conditional on the stored Newtonian baseline and continuum
source mass normalization** for its application to all 1,375 frozen cells on
each footing. The analytic force lemma passes the obligations below under
its stated finite-mass, inversion-symmetry and whole-space Gaussian premises.

This is a separate follow-up audit by the `epsilon_cassini` agent, requested
by `epsilon_review`. It did not change the author's REVIEW or any MW solver.
The proof reviewed is KT34 `REVIEW.md`, section “New continuum Milky Way tail
bound.” The accepted revision read for this note has SHA-256
`1c448a506c922efa9aaa6853bbc4cd98ca2db277b9162cb7c8bbecbdf048f91e`.
The initial audit identified two application qualifications, now incorporated
in that revision. The independently replayed arithmetic is in
`mw_tail_audit_001/results.json` and its completed, validated manifest.

## Claim and dependencies

For every nonnegative finite source measure rho of mass M, invariant under
`x -> -x`, every positive sigma and a0, simple nu, and the isolated continuum
operator `N rho + S_sigma Phi_ph[S_sigma rho]`, with no external field, the
outer-smoothed phantom acceleration satisfies

```
|g_ph,outer(x)| <= 2 sqrt(G M a0) |x| / sigma^2.
```

The null source has zero phantom response. The source need not be spherical
or compactly supported. All quantities are physical accelerations and
lengths, with the normal Poisson Green factor `1/(4pi)` in the phantom map.

The dependency chain is:

1. Gaussian source field envelope -> uniform Newtonian-field bound.
2. Simple-nu scalar inequality -> uniform bound on the vector A.
3. Gaussian Green third derivative -> angular and radial integral bounds.
4. Whole-space longitudinal projection -> a uniform Jacobian operator norm.
5. Inversion symmetry -> zero phantom field at the origin -> force bound.
6. Assigned widths and the force bound -> a circular-speed upper bound.
7. Stored Newtonian speeds and nominal masses -> numerical exclusion at
   epsilon >= 2.5, with named accuracy qualifications.

Items 1–6 are internal derivations and conventions. Item 7 depends on the
recorded numerical inputs; this audit does not replace their computation.

## Obligations checked

| Obligation | Finding |
|---|---|
| Gaussian field `M(x)/x^2 <= min(cx/3,x^-2)` | passed, positive enclosed-mass integral and total mass one |
| Extension to arbitrary nonnegative source | passed, convolution triangle inequality times total mass |
| `|A| <= sqrt(a0 |u|)` | passed, direct rationalized simple-nu formula |
| Third-derivative tensor coefficients | passed, independently differentiated the radial Hessian |
| Angular contraction polynomial | passed, independently recomputed fourth- and second-order spherical moments |
| Operator norm and projection normalization | passed, no missing sqrt(3), G, or 4pi factor |
| Sigma scaling and radial integral | passed, third derivative scales sigma^-4 and volume sigma^3 |
| Inversion and central field | passed, even source -> odd u -> odd A -> odd phantom field |
| Rounding and physical unit conversions | passed after the small G-convention correction below |
| Finite-mass gas interpretation | passed for the intended unclipped sech-squared profile; not the literal clipping extended to infinity |
| All 1,375 cells per footing replayed | passed, from saved doubled-grid rows |
| Error bound for saved Newtonian speeds/masses | conditional, not certified by this replay |
| Intermediate epsilon exclusion | out of scope |

For the decisive kernel contraction, set `alpha=n dot v`, `beta=n dot w`,
`t=v dot w`. Independently expanding

```
D^3 f[v,w] = a n alpha beta + b(t n + beta v + alpha w)
```

and using `<alpha beta>=t/3`,
`<alpha^2 beta^2>=(1+2t^2)/15` gives

```
<|D^3f[v,w]|^2>
 = r^-8 [15U^2-12UT+6T^2 + t^2(30U^2-54UT+27T^2)].
```

The coefficient of t-squared is positive. At its maximum t-squared=1,
`45U^2-66UT+33T^2 <= 33T^2`, because `0<=U<=T`.
The radial integral is `integral T/r^2 dr = integral T'/r dr = 2c/3`.
For arbitrary unit v,w the scalar `v dot (grad g_ph)w` already bounds the
matrix operator norm; converting from a component norm is unnecessary.
The resulting constant is
`(2c sqrt(33)/3)(c/3)^(1/3) < 2`, as claimed.

## Corrections found during this audit

The solver uses `Gk_solver = G_SI M_sun/(KPC_solver*1e6)`, while the fixed
width uses `Gk_width=4.30091e-6`. Replacing only the kpc conversion is not
sufficient to make the nominal formula conservative. The correct direct
speed boost is

```
delta_v_squared = 2 sqrt(Gk_solver M a0k_solver) R0^2 exp(.005)
                  / (epsilon^2 RM_width^2).
```

Relative to the author's initial nominal formula this has factor
`sqrt(G_SI M_sun/(Gk_width KPC_width*1e6)) = 1.0000123323087406`.
The change is tiny and does not alter the exclusion, but is necessary for
the expression to be a literal upper bound. The author preserved the first
arithmetic artifact as superseded and recorded corrected v2 evidence.

The numerical density evaluator caps cosh's argument at 300. Interpreted
literally on all z, that expression has a positive vertical floor and
infinite mass. The continuum lemma applies to the intended unclipped
sech-squared gas profile, or to a finite-mass grid source under an appropriate
continuum embedding. It does not establish a bound for the capped expression
extended to infinite height. The revised REVIEW states this distinction.

## Independent finite replay

`mw_tail_audit.py` reads the archived doubled-grid Newtonian rows and their
gas-mass integral, reads physical constants from the solver source by AST,
and evaluates the direct physical-unit formula for every cell. It does not
import or rerun the MW nonlinear solver. It keeps assigned widths fixed
when allowing a larger physical mass in the robustness check.

| Footing | Maximum bound at epsilon=2.5 | With Newton speed +1 km/s and physical mass +1% |
|---|---:|---:|
| canonical | 213.601920725391 km/s | 214.603913633738 km/s |
| alt | 217.867430491756 km/s | 218.870865514194 km/s |

All 1,375 cells on each footing remain below the necessary L1 lower bound
219.9 km/s. The maximum occurs at stored index 1350 on both footings.
The largest stored grid-mass discrepancy from nominal mass is `1.838e-6`
relative. This observed agreement is not a certified continuum mass bound.
The analytic upper envelope decreases as epsilon^-2, so the same exclusion
extends to every larger epsilon, conditional on the stated baseline and
source interpretation.

The run contract is `contract_mw_tail_audit.json`; it predates execution.
`mw_tail_audit_001/manifest.json` records status `completed`, unchanged input
hashes, output hashes, one numerical thread, 30-second wall and 20-second
CPU limits. Validation command:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  rebuild_2026_10_22/KT34_reciprocal_epsilon_scan/cassini/mw_tail_audit_001/manifest.json --root "$PWD"
```

The strongest safe conclusion is a continuum large-width force lemma plus
a baseline-qualified exclusion of this frozen MW family for epsilon >= 2.5.
The remaining gaps are quantitative baseline/mass error certification and
coverage of any unsampled intermediate widths. This audit makes no claim
that an arbitrary finite harmonic filter obeys the continuum bound.
