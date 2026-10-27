# Closure progress: corrected claims and the M6 population test

2026-10-27. User-authorized follow-through on
[`reviews/claude_closure_audit_2026_10_27/REPORT.md`](../reviews/claude_closure_audit_2026_10_27/REPORT.md).
The checkout is shared with live research; original frozen scripts/results and
running P1D2/X48 jobs were preserved. Corrections have separately named code,
results and amendments. No commits or blanket staging were performed.

**M6 is not closed.** A limited population can fit the inherited mass budget
under explicit retention assumptions, but compatibility with observed forest
spectra has not been established. None of the inspected forest calculations supplies the
calibrated upper bound required to decide the branch. A required population
fraction has also not been measured with the selection M6 actually needs.
This is not a positive validation of M6.

## 1. Corrections that change the record

| Issue | Executed correction and resulting scope |
|---|---|
| X57 R4b compares against the central value, not entry into the allowed band | Corrected band-entry calculation, including fractional units; the inherited generous response bound exceeds the required change in all four cells. M6 changes to **NOT DECIDABLE on both footings**. M1–M4 retain independent failures |
| Positive density was assumed to imply positive added shear | Analytic positive-shell counterexample and numerical regression. Unrestricted radial-profile R4b remains unresolved; monotone-component claims retain their stated scope |
| X64 C6 mixes two radii | Rebuilt the same catalogue members and computed the adopted binding/circular-speed proxy at one radius, with enclosed mass evaluated there. Primary-label separation still fails for all eight tested candidates |
| X64 result was generalized to all possible selectors | Restricted the conclusion to the eight scalar formulas and one-sided thresholds. The previously declared reported strict-need labels **do separate under corrected C6R**, with gaps 0.2494/0.2546 dex. This depends on adopted profiles and is not a derived physical mechanism |
| Relabelling statistic was called power | Corrected terminology; after C6R the finite-family null relabelling frequency is 2/120 |
| Preferred galaxy-lensing model was described as an absolute pass | Corrected the theory summary: X53's relative preference survives, but its absolute fit fails; X55's contour-contact score remains conditional on its profile and no-scatter mass relation |
| P1D1 upper-envelope exclusion and pressure/thermal degeneracy | Additive amendment withdraws the invalid weaker-signal implication and distinguishes the two smoothing operations. Its data verdict remains NOT DIAGNOSTIC |
| P1D1 injection shares the candidate's sign | A separate regression uses literal positive injected truth and actual historical fitting kernels. The positive model recovers it; the sign-flipped model fails rather than passing vacuously |
| X48 reused seeds do not preserve Fourier modes across resolution | Added a separate opt-in common-mode helper and launcher. Independent review found and resolved a further constraint-covariance masking issue. Eight bounded tests pass in corrected run 002; no new convergence result is claimed |

Details and immutable numerical evidence:
[`gate_fixes/README.md`](gate_fixes/README.md) and
[`technical_fixes/README.md`](technical_fixes/README.md).
The common-radius C6R is explicitly a Newtonian baryonic binding-speed divided
by the law's circular speed; it is not the escape speed of an infinite isolated
modified-gravity potential. Its reference radius is defined by catalogue mass,
not necessarily the actual transition radius of an extended source.

## 2. How much population the provisional M6 budget can hold

For a two-phase compensated baryon field, write delta>0 for the patch
overdensity, f for volume filling fraction and F for the fraction of all
baryons in patches. Exact conservation gives

\[
\delta_{out}=-\frac{f\delta}{1-f},\qquad F=f(1+\delta),\qquad
\operatorname{Var}(\delta_b)=\frac{\delta^2F}{1+\delta-F}.
\]

Using the same numerical point-variance budget as the inherited prescription,
but retaining its exact compensation, gives:

| Quantity | Canonical | Alternative |
|---|---:|---:|
| Native patch baryon overdensity | 4.23577 | 5.12956 |
| Exact conditional patch fraction F | 6.0615% | 4.8566% |
| Patch baryon density, solar masses per cubic Mpc | 3.7529e8 | 3.0069e8 |
| Number density at the fixed representative radius, per cubic Mpc | 0.010321 | 0.007064 |

These are **conditional capacities**, not observational forest confidence
limits. The inherited numerical variance budget is 0.210146. Exact point
variance does not certify the assumed smoothing or flux conversion.
[`patch_capacity.py`](patch_capacity.py), its bounded run, and the
[independent accounting review](gate_fixes/CAPACITY_REVIEW.md) establish the
arithmetic and its limits.

The primary-source census, rescaled to the declared native h and physical
baryon density, gives central estimates of **4.699%** of cosmic baryons in
galaxy-bound stars, **5.815%** in stars plus atomic gas including helium, and
**5.979%** after adding molecular gas. Sources are
[Driver et al. 2022](https://arxiv.org/html/2203.08539v1),
[Jones et al. 2018](https://arxiv.org/abs/1802.00053) and
[Fletcher et al. 2020](https://discovery.ucl.ac.uk/10112984/1/staa3025.pdf).
Molecular helium is already included and is counted once. Stellar mass
systematics and cosmic variance are retained; these values are not statistical
lower confidence limits. The source surveys have not been rerun on a new
cosmology. Their low-redshift geometry dependence is checked only as a small
sensitivity. See [`population/RESULTS.md`](population/RESULTS.md) for conventions,
source verification, uncertainty sensitivities and finite mass-function
integrals.

Let q be the **mass fraction** of the entire stars-plus-cold-gas inventory in
galaxies requiring M6. Let epsilon be their retained stars-plus-cold-gas mass
divided by the initial baryon mass of their disjoint patches. For a closed
reservoir, epsilon<=1. A necessary accounting condition is

\[
F_{required}=\frac{q\,0.0597874}{\epsilon}\le F_{allowed}.
\]

If the provisional budgets above were physically valid, this becomes
q<=1.01384 epsilon on canonical and q<=0.812318 epsilon on alternative.

| Assumed retained fraction epsilon | Maximum share q, canonical | Maximum share q, alternative |
|---|---:|---:|
| 25% | 25.35% | 20.31% |
| 50% | 50.69% | 40.62% |
| 75% | 76.04% | 60.92% |
| 100% | 100% | 81.23% |

Thus an all-galaxy interpretation needs about **98.6% retention canonical** and
**123.1% alternative** at the central census values. The latter is impossible
for a closed reservoir under this assumed budget, but this is not a physical
M6 exclusion: the bound is uncalibrated and the census has systematic errors.
A 30% share needs retention of about **29.6%/36.9%**, so a subset is not ruled
out by this bookkeeping alone. Different stellar, atomic-gas and molecular-gas
selection fractions are supported separately in the saved calculation.

No measured q for the required M6 population follows from the available
catalogues. SPARC is not a volume-complete census. GAMA's ungrouped mass fraction
is not the same selection as galaxies demonstrated to require depleted
patches, and published environment marginals do not establish the needed joint
selection. The local ALFALFA/SDSS join lacks the volume weights and environment
flags needed for this calculation. Summing it would produce a spurious density.

**The patch-to-galaxy map matters.** The inherited representative radius gives
3.64e10/4.26e10 solar masses of patch baryons but X22's representative descendant
has only 7.34e9 solar masses of effective baryon mass. If one patch produces
one such descendant, implied retention is 20.2%/17.2%. That inventory is only
20.5%/14.0% of the census inventory. These are representative accounting ratios,
not a population-coverage measurement. A mass-dependent ancestry calculation
must replace them before a real population claim; see
[`patch_galaxy_mapping/RESULT.md`](patch_galaxy_mapping/RESULT.md).

## 3. Why the forest does not yet decide that capacity

P1D1's primary linear model has null chi-square 137.63/39 and fails adequacy.
Its restricted-k variant fits the null but has insufficient sensitivity at the
chosen M6 amplitude under its frozen rule. Neither establishes a physical
population limit.

The saved **provisional P1D2 primary output**, observed at 15:16:54 UTC, also
reports NOT DIAGNOSTIC: null chi-square 95.32/36 and Asimov separations
0.44/0.16. This snapshot does not certify the live job's final robustness
verdict or current execution status. P1D2's nonlinear flux map is a useful advance, but its one-dimensional
FGPA prescription lacks an independently calibrated response and omits
peculiar velocities. A calibrated same-population response remains necessary
even if a variant achieves an acceptable null fit.

**Late result checked:** Claude's completed P1D3 DESI calculation appeared
during this work. Its primary null chi-square is **7017.37/719**. It has greater
template sensitivity, but both footings and all seven variants report
NOT DIAGNOSTIC because the linear model is inadequate. Its nominal mu95 and
baryon-fraction limits are therefore not physical limits. This is an inspection
of saved output, not a rerun or source/data-release audit; the recorded DESI
blinding metadata also remains unresolved. The exact checked JSON hash is in
[`population/p1d3_late_output_check.json`](population/p1d3_late_output_check.json).

The exact status, hashes and next decision requirements are in
[`forest_review/RESULT.md`](forest_review/RESULT.md). Increasing a fitted template
amplitude or interpreting a nominal mu95 cannot replace the missing ancestry
and response maps. Therefore this stage reaches **undecided**, with quantitative
conditional thresholds, rather than either an M6 success or an exclusion.

## 4. Next closure dependencies

The sequence continues from this population test to a common admissible mass
profile, its dynamics and independent predictions. A profile must meet its
boundary and phase-space conditions before its empirical fit can establish a
physical completion. The next necessary-condition test has now been executed:
**the literal sharply truncated cluster Burkert profiles in X38/SC1 cannot be
regular nonnegative isotropic collisionless equilibria without a confining
wall.** Their density jumps from a positive interior value to zero, whereas
the velocity integral for such an energy distribution requires density to
vanish at the boundary. The analytic proof, actual-code application,
constructive local boundary examples, finite checks and independent review
are in [`profile_admissibility/RESULT.md`](profile_admissibility/RESULT.md).

This rejects that particular equilibrium interpretation, not every halo or
M6. Anisotropic distributions and genuinely different dynamical models are
outside the theorem. Smooth positive distribution functions can satisfy the
local edge condition; global consistency, stability and fitting still need
checking. The galaxy implementations do not impose the same literal edge,
so this finding is deliberately confined to the cluster part of a common
family. The empirical cutoff can remain a declared lensing convention.

Claude's now-completed CS1 atlas supplies additional descriptive evidence:
it reports a rising fitted core-density relation with slope about 0.69 and
0.25 dex intrinsic scatter. Its frozen NO SIMPLE LAW classification depends
on a three-stack residual rule whose uncertainty sensitivity it explicitly
discloses. This is useful input for a future common model, not a complete
joint dynamics/lensing or phase-space test. We did not duplicate its fits.

The remaining deliverables are concrete:

1. A survey-weighted mass distribution for the systems that actually require
   M6, with a justified selection and an explicit patch ancestry/retention map.
2. An independently validated forest response to that same distribution, with
   a physical population confidence limit. Completed P1D1/P1D3 and the
   inspected P1D2 primary do not supply it.
3. A common finite mass-profile family with specified outer boundary, scatter
   and admissible distribution function, fitted through exact dynamics and
   lensing projection across galaxies, groups and cluster bands. The completed CS1
   atlas is descriptive evidence, not this joint physical test.
4. Conserving formation and transport dynamics that produces a surviving
   profile from allowed initial conditions. The common-mode X48 correction is
   preparation for future convergence work; no new collapse run or converged
   concentration is claimed here.
5. A separate argument selecting kappa=1/2 if a derivation rather than a fitted
   coefficient is claimed. None is supplied by these observational repairs.

The missing maps in items 1–2 prevent a definitive M6 answer, and missing
profile/dynamical specifications prevent advancing directly to a unique
formation calculation. They are explicit unresolved scientific inputs, not
permissions awaiting approval. The present work repairs the evidence and
computes the available necessary tests without substituting new assumptions
for those inputs.

**Final verification.** All seven accepted current computation manifests
validate against their declared inputs (`VERIFICATION.json`); targeted gate
and technical suites pass, and the new profile implication has a separate
independent proof audit. Technical run 001 is retained as superseded evidence.
The continuation checkpoint, owners and exact next steps are in
[`HANDOFF.md`](HANDOFF.md). The scientific target remains open.
