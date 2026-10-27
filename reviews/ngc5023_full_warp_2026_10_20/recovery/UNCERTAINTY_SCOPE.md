# Scope of the NGC5023 reconstruction uncertainty experiment

Checkpoint `ngc5023-full-warp-2026-10-20`, assessment base
`c821a8bccc8a20e107b4c6771d31e02d05aa8b10`. This is a source and design
check, completed 20 October 2026. No new cube fit or residual was examined
for this note. It evaluates the planned family and the source conventions,
not the numerical outcome of the parent experiment.

The defensible output is a **range over an explicitly tested,
source-anchored reconstruction family**. It is not a joint confidence
region for the preferred model, an exhaustive uncertainty envelope, or a
posterior over its nominal 206 parameters. Finding a remainder outside
this finite family establishes a conditional mismatch; it does not remove
the unidentified freedom of the original fit.

## What the source errors mean

The retained primary source is Kamphuis et al. (2013),
[arXiv1306.5312v1](https://arxiv.org/abs/1306.5312v1), published as
[MNRAS434,2069](https://doi.org/10.1093/mnras/stt1153). The exact retained
`reviews/ngc5023_cube_2026_10_20/warp/Kamphuis_2013.tex` SHA256 is
`2323426866bdb41e15fed1a528847befeb446e1a334eb412b7d72cf3b007f600`.
Source line numbers below refer to that immutable TeX, not publisher PDF
pagination.

At lines313–337, the authors describe varying one parameter while holding
the others fixed until model and data clearly deviate. Table4 reports
the average maximum upward/downward deviation, usually next to a central
value. It does not provide two separate asymmetric limits, a likelihood
threshold, a coverage probability, a covariance, or independent ring
errors. Consequently, even the symmetric interval made by adding and
subtracting that average need not equal both actual one-sided limits.
The paper explicitly warns about parameter degeneracy and neighboring-ring
degeneracy. Joint corners of a box of these ranges are not established
acceptable models.

The lag has a different provenance. Table3 and lines261–262 describe
two TiRiFiC fits started from0 and−22km/s/kpc, with the final lag and its
error determined by averaging those fits. The preferred−9.4±3.8km/s/kpc
is therefore a source fit estimate, not another Table4 visual-deviation
error. Neither source supplies a joint distribution that can be combined
with the other ranges as independent Gaussian priors.

| Proposed variation | Defensible interpretation | Qualification |
|---|---|---|
| Inclination±1.3°, PA±1° | Table4 visual range used as a source anchor | The quoted values are central. Extending them coherently to a complete radial profile is our chosen mode, not a published joint radial envelope. Preserve the inner-ten-ring tie, shared disk/arm geometry, and the two side profiles. |
| Rotation±5km/s | Source uncertainty anchor at the velocity measured at D_HI | A common offset to all rings, or a common fractional rescaling, is a declared analyst mode. Table4 does not establish a±5 pointwise error at every radius. |
| Lag magnitude9.4±3.8km/s/kpc | Range anchored to the two-start preferred fit | Distinct estimation method; not a Gaussian confidence interval or evidence that every joint endpoint remains acceptable. |
| Heights9.1±3,14±9,9±6arcsec | Source visual ranges for the three constant scale heights | The heights may trade against inclination, warp, arm placement and amplitudes. A product of three intervals does not recover those correlations. |
| Arm phase±7.5°; widths±23/25arcsec | Source visual-deviation anchors | Coherent offsets are only a subset of allowed smooth profile changes. Preserve unwrapped phase interpolation. The large negative-width direction requires an explicitly stated nonnegative treatment. |
| Pixel/trace perturbations | Bounded graphical reconstruction errors under the declared readout procedure | Deterministic line/axis envelopes, not independent ring standard errors. Coherent perturbations do not exhaust smooth shape changes. Keep separate from the source model ranges. |
| Radius0–360 versus0–361arcsec | Structural reconstruction sensitivity | The latter is authenticated for the related author baseline, not for the missing preferred file. It must not replace the plotted profile without being labeled an alternative. |
| Radial interpolation, edge support or final half-cell extension | Structural reconstruction sensitivity | No exact preferred INTY/support card was recovered. The paper explicitly says the disk edge was not observed (lines339–341). |
| Gaussian/sech²/uniform vertical alternatives | Analyst sensitivity to unresolved structure and conventions | The related author baseline supports LTYPE3 exponential. Other vertical families are not Table4 uncertainties; declare how their characteristic widths are matched. |
| Changing arm azimuthal extent, lag clipping, dispersion or spectral response | Analyst or instrumental sensitivity | These are not additional published error bars. Identify each assumption and do not silently pool it into a confidence interval. |

Calling the numerical min/max over the executed cases a bounded family
envelope is accurate if the finite family is named. Calling that envelope
the bounded uncertainty of the actual galaxy, or implying that the visual
ranges guarantee simultaneous coverage, is not supported.

## Correlations and profile freedom that remain unidentified

The source adds122 nominal arm parameters: two constant heights and
40 each of amplitude, phase and width (lines339–342). It explicitly
regularizes **phase and width** smoothly between rings, accounting for
80 correlated arm values. It does not state the same smoothness constraint
for every arm-amplitude node. A206-parameter count is a bookkeeping
description, not a recovered effective dimension or covariance matrix.

The source begins with logarithmic arms of20° pitch, then lets their phase
profiles change under manual smoothness regularization. It does not force
a logarithmic spiral or a single common pitch (line298); the final arms
only approximately resemble a22° spiral. A coherent phase offset leaves
the radial phase shape unchanged. Thus the most important untested shape
freedoms include smooth phase slope/curvature, smooth width slope/taper,
and redistribution of arm brightness between radii. The disk brightness
shape also has no pointwise Table4 errors. Such alternatives can be
declared as analyst-selected low-dimensional shape modes constrained by
the plot/source ranges. They cannot be assigned a probability from this
paper, and they must not be selected by improving the protected residual.

Warp and spiral placement are particularly correlated. The paper refits
PA because arms can imitate warps when the disk is not exactly edge-on
(line298). It requires arm inclination to follow the disk at every radius
(line267), and the preferred arms also follow its rotation and orientation.
The inner ten rings share one inclination and PA; outer rings vary by
side (line341). Keep these ties in every source-family case. Include
opposite-direction side warp modes, or explicitly report that only global
coherent changes were tested. Independent arm tilts would add a different
model class rather than propagate the stated preferred-model errors.

The source discarded a radially varying lag because the preferred
spiral model was not significantly improved, while noting visible possible
radial variation (line311). A radial lag mode is therefore an informative
analyst sensitivity, not an uncertainty already exhausted by9.4±3.8.
The paper's fixed-arm-height and removed-line-of-sight-warp examples
(line312) are useful source-described model-class controls. Their
refitted lags are not independent observations or parameter posteriors.

## Flux, widths and protected-strip amplitude calibration

Table4 masses are total component fluxes inferred from the same cube and
the adopted6.6Mpc distance. They are not external independent constraints
on disk/arm decomposition. Their quoted ranges can anchor a conditional
flux family. They do not establish that three component masses are
independent hard bounds, or that their errors add in quadrature.

Two different width experiments answer different questions:

1. Change widths while retaining the digitized peak-amplitude profile.
   Integrated arm flux generally changes. This is closer to a literal
   one-parameter variation with the other profile values fixed, but may
   leave the separately quoted component-flux ranges.
2. Change widths and rescale amplitudes to retain arm flux or a source
   flux range. This explores a declared correlated, conditional family.
   It is physically useful, but the compensating amplitude rule was not
   recovered from the source fit and is not its published covariance.

Report these cases separately where feasible. The paper clamps a
negative lowered ring value to zero in its error exercise (line313).
A zero-width arm with finite peak brightness has vanishing integrated
flux at that radius. Holding nonzero flux while width tends to zero
requires divergent peak amplitude. A positive width floor, truncation
rule, unresolved delta-arm limit, or omitted zero-width case must be
explicitly declared; none is supplied as a fitted physical scale by the
paper. A global total-mass constraint does not constrain the radial
location of that mass.

Calibrating three amplitudes using only the predeclared central strip is
a reasonable conditional nuisance procedure. Retain the unfitted
source-normalized prediction too. Record bound hits and component
identifiability, such as the singular values of the weighted component
design matrix. A source bound can force an apparently stable amplitude
when the central strip itself cannot distinguish the arms. Free-amplitude
fits are diagnostics, not extra source evidence. The current authentic
baseline's10% total-mass allowance is an analyst allowance; it is not
the preferred disk-only Table4 mass error.

Calibration is not external validation: Table4 and the original preferred
profiles were inferred from the full observations. The present strip
protects the new amplitude calibration from direct reuse of the chosen
high-latitude validation bins, but does not make those bins historically
blind. Beam and line-of-sight mixing also couple the strips. Guarded
|z|≥70arcsec is useful, with the same qualification. All training gates,
known-feature enlargement, and any selection among family members must
be fixed before inspecting new residuals. Training failures should be
retained and labeled, not silently discarded or treated as new signals.

## Missing or separately scoped nuisance controls

Table4 also prints systemic velocity404.8±4km/s and center RA
13h12m11.83s±4.3s of time, Dec44°02′16.9″±6″. The literal RA range is
approximately±46.37″ east/west at this declination. Its surprising size
is already documented in the immutable source-control report; no
clarified preferred value was recovered. Test it as a literal source
stress control or explicitly state that the analysis conditions on the
nominal center. Substituting±4.3″ would change the source. The optical
catalog center's precision does not bound the physical HI center. Keep
feature exclusions anchored to their observed sky/velocity locations
when translating a trial model center or systemic velocity.

The10km/s velocity dispersion includes instrumental effects (line197).
If an additional native-channel response is applied, distinguish the
intrinsic line dispersion from the effective source dispersion so the
entire instrumental broadening is not counted twice. Actual cube beam,
channel correlations, interpolation/quadrature and CLEAN/restoring-beam
limitations remain separate observation/reconstruction issues. A Gaussian
restoring-beam kernel is not a recovered residual dirty-beam model.

Distance is unnecessary for angular position/velocity observables. The
paper's6.6Mpc is only needed here to translate its km/s/kpc lag and to
check masses from flux; retain that convention together. Distance
alternatives, if tested, should be identified explicitly and should not
be folded into a fitted halo or acceleration law.

HR and LR are two imaging products of the same WSRT observations.
WHISP is older observational material already inspected in the parent
campaign; it cannot become a blind holdout for a residual chosen now.
These checks can demonstrate reproducibility across products or observing
material with the declared reuse, not fresh discovery significance.

## Recommended interpretation of the executed phase

Separate at least four outputs: source-reconstruction variation,
source-anchored parameter modes, analyst structural/instrumental
sensitivities, and empirical noise. Do not add them in quadrature or
assign frequencies to a hand-chosen ensemble. State which tested
profiles pass predeclared ordinary-data checks and show the failing ones
as model inadequacy controls. If many training-compatible cases make
materially different high-latitude predictions, the result is
nonidentifiability. If no tested case fits the ordinary training data,
there is no calibrated preferred-family subtraction from which to
certify a new remainder. A coherent residual persistent across acceptable
cases remains conditional on the finite modes tested and still needs
the declared observational controls; it is not by itself a new-force
or physical-memory measurement.

Design snapshot read for this note: `forward_model.py` SHA256
`5dd958224055476458a8c51df3474e4ae31ba807f2976c14f51d5606e2ff03cd`;
`compare_model.py` SHA256
`49a2d60ab132a12d671a49cb77258768dce3ef16f4e81508b9bc59691698f54d`.
These identify the inspected version only; later parent changes are
outside this note's read-only code review scope.
