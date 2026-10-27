# Claude's latest work: what can actually be closed

Review date: 2026-10-27 (America/New_York). Review began at
`e6d278b74755885d9f62106becef5d7b753c512c`; the checkout advanced during review.
The accompanying `AUDIT_RECORD.json` pins the inspected files. Three isolated
reviewers examined the M6/forest, selector, and halo/convergence chains; the
coordinator inspected the decisive source passages and checked the arithmetic
and shell counterexample below. This is an audit, not a production rerun.

**Primary verdict: incomplete.** Claude has excluded useful, specified model
families and exposed real tensions. The record does not establish that M6 is
the only remaining physical possibility, that galaxy lensing passes absolutely,
or that the pending forest test can close the theory. Several exclusion steps
need correction before they can support even branch-level closure.

The practical route is finite: repair those implications, determine whether a
single admissible mass distribution can satisfy the data, and require any
surviving mechanism to generate that distribution. A successful descriptive
fit, a dynamical mechanism, and a derivation of kappa are separate obligations.

**1. The pending M6 test can at most exclude the specified optimistic template.**

[P1D1's frozen criteria](../../rebuild_2026_10_22/P1D1_m6_boera_high_z_forest/FROZEN_CRITERIA.md),
lines 100–104, say that excluding the upper-envelope signal also excludes weaker
realizations at the same physical amplitude. This implication is reversed.
If the observed excess is near zero, a smaller signal can fit after a larger
one has been excluded. A fitted template limit becomes a physical baryon-fraction
limit only through a validated response mapping.

There is a second, independent gap. X63 uses the **maximum allowed** depleted-patch
baryon fraction, about 0.060/0.048 on its inherited background. That is not a
minimum fraction required to explain galaxies. Its +0.26–0.39 high-redshift signal
is therefore a prediction of the chosen bound-saturating toy model, not an
unavoidable signal of displacement. See [X63's model and caveats](../../rebuild_2026_10_22/X63_displacement_forest_prediction/README.md),
lines 13–21 and 34–46.

The missing closure inequality is

\[
F_{b,\mathrm{required}}>F_{b,\mathrm{allowed}},
\]

with both quantities defined for the same patch population, background, dynamics,
and flux-response model. Estimating the required fraction needs a population
and selection calculation: how many isolated galaxies and their environments
must originate in depleted patches, and how many baryons those patches contain.
It cannot be set by the upper bound itself. X57 also needs to evolve its initial
deficits into the claimed present-day exclusion; that mapping is assumed.

**2. The forest nuisance model merges two physically different operations.**

[P1D1 criteria](../../rebuild_2026_10_22/P1D1_m6_boera_high_z_forest/FROZEN_CRITERIA.md),
lines 63–70, identify thermal broadening with the pressure filter. In the stated
linear proxy, after expressing both scales in compatible units, the operations are

\[
P_{1D}(k;R_J)=\frac{1}{2\pi}\int_k^\infty
qP_{3D}(q)e^{-q^2R_J^2}\,dq,
\qquad
P_{1D,\mathrm{thermal}}(k)=e^{-k^2s_{\rm th}^2}P_{1D}(k;R_J).
\]

One filter acts on every three-dimensional mode being integrated; the other
acts on the line-of-sight mode after projection. They are not exactly degenerate.
A common thermal factor cancels in the idealized M6/adiabatic ratio, whereas
changing R_J changes that ratio. Bias and tilt might approximate their combined
effect over a limited range, but fitting the null does not validate the response
to the added compensated mode.

This distinction is also explicit in [Boera et al., arXiv:1809.06980v2,
Introduction and Fig. 3](https://arxiv.org/html/1809.06980v2): the thermal and
pressure-smoothing responses have different scale dependences. The paper uses
hydrodynamic spectra to model the flux response. That source verifies the
distinction, not the validity of M6 or a new simulation on the project's background.

The existing G0 adequacy and G1 sensitivity checks are useful safeguards for a
template exercise. Physical exclusion additionally needs independently generated
mock spectra or a controlled response calculation on the declared background,
with pressure smoothing, thermal broadening, velocities and flux conversion
accounted for. No inference here requires importing a cosmological posterior
that the project has prohibited.

**3. The cluster-outskirts exclusion has two separate errors.**

First, [X57's code](../../rebuild_2026_10_22/X57_exclusion_mechanism/x57_exclusion.py),
lines 481–484, declares failure outside two standard deviations but compares a
possible repair with the drop needed to reach the **central measured value**.
To enter the allowed band from above, the necessary drop is

\[
\Delta A_{\min}=\max[0,A_{\rm pred}-(A_{\rm meas}+2\sigma)].
\]

Recalculation from X57's committed JSON gives:

| Footing | h=0.672: drop to enter band | h=0.686: drop to enter band | X57's generous deficit bound D |
|---|---:|---:|---:|
| canonical | 0.00077834 | 0.01950774 | 0.32316075 |
| alternative | 0.08495336 | 0.10218429 | 0.32316075 |

The alternative-footing comparison with 0.344 is therefore not a valid exclusion
at the stated two-sigma threshold. The bound exceeds the necessary drop in both
cells. This does **not** prove an achievable deficit profile: D is only a generous
bound, and the actual projected response must be computed. It means the bound
used in this argument cannot close the escape. M6's alternative-footing exclusion
rests on R4b alone in [X57's summary](../../rebuild_2026_10_22/X57_exclusion_mechanism/README.md),
lines 12–23.

Second, [X57 criteria](../../rebuild_2026_10_22/X57_exclusion_mechanism/FROZEN_CRITERIA.md),
lines 129–130, infer additional positive shear from nonnegative density. Shear
depends on excess surface density, DeltaSigma = meanSigma(<R) - Sigma(R), so
this implication is false for unrestricted radial profiles. The earlier
[X30 statement](../../rebuild_2026_10_22/X30_sheet_cluster_profile/README.md),
line 31, was explicitly restricted to a monotone component.

An analytic counterexample is a positive spherical shell of mass M at radius a.
For 0<R<a, write u=sqrt(1-R^2/a^2). Direct projection gives

\[
\Sigma(R)=\frac{M}{2\pi a^2u},\quad
\overline\Sigma(<R)=\frac{M}{\pi a^2(1+u)},\quad
\Delta\Sigma=\frac{M}{\pi a^2}
\left[\frac1{1+u}-\frac1{2u}\right]<0.
\]

A narrow smooth positive shell preserves the negative sign away from its edge.
At R/a=1/2 the bracket is -0.04145188. This refutes the general positivity
argument; it does not demonstrate an equilibrium shell, a fit to the full
cluster profile, or a mechanism producing one. It identifies a bounded question
for radial-profile feasibility that the monotone-profile exclusion cannot answer.

**4. The selector failures cover a finite family. One physical proxy is also miscomputed.**

[The final verdict](../../covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md),
line 450, says every object-property key is excluded. X64 actually tests eight
predefined scalar formulas with a single threshold in either direction; see
[criteria lines 84–110](../../rebuild_2026_10_22/X64_oblique_object_keys/FROZEN_CRITERIA.md).
No coverage proof reduces all multivariate, nonmonotone or history-dependent
mechanisms to those formulas. Dwarfs/galaxies/clusters requiring retain/exclude/retain
refutes a monotone mass threshold, not every mass function. Merely encoding that
pattern with two thresholds would still supply no physical explanation.

X64's C6 is advertised as escape speed divided by circular speed at r_a0. Its
[implementation](../../rebuild_2026_10_22/X64_oblique_object_keys/x64_oblique_keys.py),
lines 129–137 and 247–249, retains the potential at the catalogue radius r while
using r_a0 in the denominator. For a point mass the intended value is
sqrt(2/nu(1)); the implemented value includes an extra sqrt(r_a0/r).
The named physical key cannot be excluded without correcting or relabelling it
and regrading. This does not change the other candidate calculations.

The reported 3/120 random-label separation frequency is a null relabelling
statistic, not statistical power against a defined physical alternative.

[X62's own conclusion](../../rebuild_2026_10_22/X62_environment_keyed_switch/README.md),
lines 40–49, is appropriately narrower: none of the **three concentration
prescriptions tried** passes every line, and the halo core prescription is the
limiting piece. Failure of that selector-plus-profile package does not reject
environment selection generally.

**5. Relative preference for the law has been promoted to an absolute pass.**

[The theory statement](../../rebuild_2026_10_22/THEORY_STATEMENT_2026-10-26.md),
lines 19–20, says galaxy lensing passes to 3 Mpc. [X53's actual result](../../rebuild_2026_10_22/X53_outer_lensing_law_vs_halos/README.md),
lines 24–39, says no tested model fits well absolutely: the bare law has chi-square
160.7/127.6 for 60 points and p approximately 4e-11/9e-7. The substantial relative
preference over the frozen halo prescription survives. It is not evidence that
the preferred model has passed the absolute test.

X55 usefully shows that refitting the halo mass relation alone does not remove
the mismatch in its specified model. But its [assumption ledger](../../rebuild_2026_10_22/X55_one_halo_mass_for_both/ASSUMPTION_LEDGER.md),
lines 5–10, fixes a deterministic relation with no intrinsic scatter, particular
core rules and outer boundaries, and differing baryon-mass conventions. Its
4.55/4.26-sigma contour-contact score should retain that definition rather than
becoming a universal exclusion significance for gravitating halos.

**6. The concentration experiment is not yet clean convergence evidence.**

X48 A2 reports concentrations 11.63/8.22/7.31 and fails the SPARC line under the
adopted core prescription. A3 tests nine seeds at 10^12 solar masses and ng=64,
with unchanged softening; see [criteria lines 89–111](../../rebuild_2026_10_22/X48_native_cf_zoom/FROZEN_CRITERIA.md).
It does not test convergence of the two larger mass bins.

In [x48_zoom.py lines 71–78](../../rebuild_2026_10_22/X48_native_cf_zoom/x48_zoom.py),
the Gaussian Fourier arrays are drawn with resolution-dependent shapes. Reusing
the same seed at a different ng does not preserve the same low-frequency phases;
even the start of the imaginary draw moves. Per-seed differences therefore
include different initial realizations. An ensemble comparison remains informative,
but a 20% median agreement does not establish paired force, time-step, softening
or profile-estimator convergence. Use nested common modes for that purpose.

**A finite route to closure.**

| Work item | Required deliverable | What it can close |
|---|---|---|
| Correct the review record | Scoped selector conclusions; corrected R4b band test; physical C6; absolute/relative fit distinction; preserve old results as history | Unsupported claims of exclusion or success |
| Make M6 falsifiable | Independently justified minimum depleted-patch baryon fraction plus a calibrated flux response and a confidence limit | The specified displacement branch if its required and allowed populations are incompatible |
| Test one common mass-profile family | One finite, nonnegative, phase-space-admissible family and population relation; declared scatter, sample selection and boundaries; exact dynamics and lensing projection; acceptable absolute fits across galaxies, groups and all cluster bands | That specified profile family, with either an admissible witness or a scoped infeasibility result |
| Establish its dynamics | Conserving evolution from allowed initial conditions, early cold behavior, stable late profile, baryonic normalization and independently checked predictions | A specified physical completion, if all obligations succeed |

The immediate priority is the first two items and the common-profile feasibility
test. Radial redistribution is worth including only with explicit mass, phase-space
and projection constraints; an arbitrary shell fitted separately to each system
would not establish a common mechanism. More catalogue thresholds cannot repair
a profile family that has no common fit.

The [October 26 review](../claude_missing_piece_2026_10_26/REPORT.md) identified
multistream stress as a possible activation variable. That remains a conditional
ingredient: it does not supply transport, a stable stopping rule, or the
baryon–halo normalization. A positive density or Jeans solution also does not
certify a nonnegative, dynamically admissible distribution function.

Even empirical and dynamical success would leave kappa=1/2 fitted unless a further
argument selects it. There is no established derivation of that coefficient here.

**Verification and limits.** Original research sources, frozen criteria and running
jobs were not modified. No full simulation, CLASS run or new P1D fit was executed
for this review. The new numerical checks were limited to reading X57's saved JSON
and recomputing the four band-entry distances and the shell example; their
reproduction command and input hash are recorded beside this report. The shell
sign and filter distinction were checked analytically. The primary literature
check was limited to Boera v2's treatment of thermal and pressure smoothing.
Reviewers also inspected stored results and generating code; agreement among
reviewers is not a proof certificate.

An additional issue in the live P1D implementation at the pinned revision:
`SIGN` affects both the fitted template (line 237) and the planted mock (line 372),
so its sign-flipped mutation need not fail recovery. Fix the injected reference
independently before crediting this as a physical sign check. This review makes
no claim about the outcome of the still-running fit.
