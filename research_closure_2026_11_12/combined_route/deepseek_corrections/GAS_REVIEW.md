# Independent read-only gas and density-bridge review

Date: 2026-11-12. Reviewer: independent DeepSeek-corrections subagent; no edits to
`gas_corrections/` or the combined `DERIVATION.md`.

**Verdict: the checked analytic formulas and implementations are correct under
their stated toy-model assumptions. No blocking formula, unit, shell-boundary,
beam or volume-integral defect was found. Their observational interpretation
remains conditional on the explicitly missing inputs.**

Normalized claim: for the saturated enclosed-mass example, compact central
baryons plus a gas shell of density `Sigma0/(2r)` on `Rin<r<Rout` produce the
stated projected column, emission measure, isothermal Compton-y and illustrative
X-ray flux. A circular Gaussian convolution is performed in two dimensions.
Separately, the AQUAL external-field asymptotic monopole and signed density in
`DERIVATION.md` sections 2 and 3 use total mass and cold excess consistently.

## Formula and implementation checks

| Obligation | Result |
|---|---|
| Shell mass and compact-baryon accounting | Passed. Integrating `4 pi r² rho` from Rin gives `pi Sigma0(r²-Rin²)`; adding the central baryons realizes the saturated total for r>=Rin. Below Rin, gas is zero and the compact baryons exceed the lower envelope. |
| LOS column, including b=0 and b=Rin | Passed. `Sigma0[acosh(Rout/b)-acosh(Rin/b)]` when b<Rin, with the second term omitted otherwise. The central finite limit is `Sigma0 ln(Rout/Rin)` and the column vanishes at Rout. |
| Emission measure | Passed. The integral of `1/(b²+z²)` produces arccos, not arccosh; the factors 2, XH/mu_e, mp and SI-to-cgs `1e-10` are consistent. |
| Projected area versus 3D volume | Passed. The projected mass recovers the shell mass. The emission measure integrated over projected cm² agrees with the 3D integral in cm^-3. |
| Circular beam kernel | Passed. Direct angular integration of the Euclidean 2D Gaussian agrees with the `i0e` representation. No per-radius renormalization is applied. The finite output domain can lose measured flux; a sufficiently large domain recovers total input flux. |
| tSZ and X-ray units | Passed. y is dimensionless with kT supplied in keV; luminosity in erg/s divided by a centimeter-squared distance gives erg/s/cm². The supplied cooling coefficient is explicitly illustrative. |
| Angular-diameter distance | Passed. c/H0 gives Mpc before conversion; the 1/(1+z) factor and luminosity-distance conversion are correct. |
| External-field total/excess bridge | Passed conditionally. `F_A=60.5` corresponds to cold excess 59.5, and `F_b/F_c=R/(F_A-1)` is a conditional identification, not an environment prediction. |
| Local signed density | Passed. Differentiating the potential gives the displayed positive polar and negative equatorial lobes; no G remains after division by 4 pi G. Positive-background coverage at 5 R_E is properly separated from the literal nonnegative-rest-density identity. |
| Claim calibration | Passed. Both documents disclaim a unique forced gas profile, observational likelihood or universal field no-go. The actual anisotropic lensing operator remains to be supplied. |

Code locators in `gas_corrections/corrected_signal.py`: mass normalization and
shell 22–38, projection 41–64, emission measure 67–79, 2D beam 82–95,
distance/flux 98–104, volume checks 119–125, illustrative luminosity 156–159.
The corresponding physical restrictions are explicit in `gas_corrections/RESULT.md`
lines 5–15. `DERIVATION.md` sections 2 and 3 correctly qualify the asymptotic
mass identity and the positive-background escape.

## Independent numerical witnesses

`gas_audit_check.py` performs 14 checks and never calls the candidate's `checks()`
or `result()`. It reconstructs the LOS integrals in scaled physical coordinates,
the 3D shell mass, and the beam convolution from an angular Euclidean-distance
integral rather than the Bessel kernel. Both acceleration footings and shell
boundaries b=0, just below/at/above Rin, just below/at/above Rout were included.

- Maximum relative column/EM disagreement: `3.60e-14`.
- Maximum absolute beam disagreement against direct 2D integration of a smooth
  compact source: `6.80e-7`.
- Full-plane beam flux error on a large finite grid: `8.14e-7`.
- Shell mass checks agree through approximately `8.1e-14` relative error.
- Source hash before and after the numerical run agrees.

The tiny positive `M_req(Rin)` on the alt footing is ordinary subtraction roundoff
(about 1e-16 of the baryon mass), not a physical inner-shell component.

## Limits of this review

`rho_A` represents the radial shell law before imposing an outer aperture; the
LOS, EM and luminosity routines apply Rout explicitly. Callers should retain that
outer boundary when using `rho_A` directly. No current result in the checked script
integrates it beyond Rout or asserts a finite total mass for its untruncated form.

The `--mutate` option is documented as running the same checks; it does not change
the source model or produce a distinct mutated result. The temperature factor-two
check occurs inside the common verification. This is not evidence that a general
mutation suite, data covariance or a real survey transfer function has been tested.

The checks do not authenticate a plasma emissivity, constrain the temperature,
derive an environmental vector field, measure a gas signal, or establish a
conserved microscopic carrier. No new likelihood verdict is supplied.

## Provenance

Command: `python3 research_closure_2026_11_12/combined_route/deepseek_corrections/gas_audit_check.py`.
Exit 0. Results: `gas_independent_checks.json`.

Audited code SHA-256:
`d1e3eb31a72fda517459df9a1493b43d5614b2dd67d11dc0cb6ccbca235b522d`.
Exact document and section hashes are recorded in `gas_review_sources.json`.
