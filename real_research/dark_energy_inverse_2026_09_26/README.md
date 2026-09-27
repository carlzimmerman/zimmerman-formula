# CD26-3 — following the inverse relationships to cosmic tension

The inverse audit finds a sharper physical target: **the negative-pressure
response, `Pi=-p`, rather than an independently identified new substance**.
“Cosmic tension” is a useful provisional name for that role. If it is the
effective stress of modified geometry, call it *effective cosmic tension*.
Reserve *vacuum tension* for an established constant vacuum contribution
`T_mn=-epsilon_vac g_mn`. This is terminology for stress, not a claim that
space is an elastic material or that the microscopic origin is solved.

This checkpoint builds on CD26-2 and the existing kappa, DE1–DE4, L273 and
clock work. It keeps the author's filtered `nu_mono`, criterion B and
no-new-dark-matter-particle direction. The shared Git history advanced during
the audit; individual source hashes and run revisions are the provenance.
No unrelated changes or historical results have been overwritten.

## The most useful new test

Under a flat Einstein-form FLRW background, constant couplings, negligible
ordinary pressure and the proposed pressure law,

\[
 a_0^2=\kappa^2G_N\Pi_X,\qquad
 \Pi_X=\frac{c^2}{8\pi G_{\rm cosm}}(2\dot H+3H^2),
\]

the prediction is

\[
 \boxed{\left[\frac{a_0(z)}{a_0(0)}\right]^2
 \frac{[2\dot H+3H^2]_{0}}{[2\dot H+3H^2]_{z}}=1.}
\]

The ratio requires `a0(0) != 0` and `Q(z)>0` on the tested branch.
The pressureless contribution cancels exactly. No particle dark-matter
abundance needs to be fixed to write this test. Constant `kappa`,
`G_cosm/G_N` and the overall Hubble normalization also cancel in the
theoretical ratio. Actual galaxy calibration, derivative errors, curvature,
radiation and cross-covariances still need to be handled.

This is a **conditional prediction to test**, not a reported observational
pass. The Einstein-form stress can be effective bookkeeping in modified
gravity. Its identification with a particular clock or vacuum must be
derived from the same action that gives the galactic force law.
The full calculation is in [reconstruction/RESULT.md](reconstruction/RESULT.md).

## What the inverse map actually tells us

| Relationship audited | Inverse information | Remaining freedom or test |
|---|---|---|
| `a0²=kappa² G_N Pi` | Negative pressure after independent kappa calibration | A fitted kappa that already used vacuum density gives a circular density recovery |
| Constant pressure plus conservation | `epsilon=Pi+D a^-3` | The independent constant D; constant a0 does not imply the whole sector has w=-1 |
| Expansion history | Total effective density and pressure under specified background equations | Stress decomposition and action; pressure cancels an arbitrary conserved dust term |
| Density, curvature, Hvac, horizon, temperature | A dictionary of the same scale once coefficients are fixed | No extra independent measurement; retain `g=G_cosm/G_N` and Hvac versus Htotal |
| Gate threshold at several epochs | Gate exponent and normalization if vacuum fractions are independently known and vary | Otherwise only `p ln f_v` is identified; select the correct switch branch |
| Clock sound and dispersion | Local potential derivatives on the circular canonical branch | Vacuum zero is absent; pressure plus a specified potential model is needed to infer it |
| Positive lapse profile | `A/b=-4 Delta sqrt(N)/sqrt(N)` | Source, geometry, trace coupling and unit calibration; one zero eigenvalue is insufficient |
| Rotation-curve point | A kernel-dependent algebraic inverse in restricted unfiltered spherical limits | Ill-conditioning near Newtonian recovery; the operative nonlocal theory needs a forward source solution |

Detailed independent routes:

- [Scale, coupling and temperature inverses](scales/REPORT.md).
- [Gate branches, clock stress and dispersion](gates_clock/RESULT.md).
- [Lapse inverse, exact counterfamilies and consistency tests](spectral_inverse/REPORT.md).
- [Pressure/density reconstruction and acceleration inverses](reconstruction/RESULT.md).

Several results directly improve the working ingredients:

1. **Do not equate constant a0 with a uniquely selected vacuum state.** For
   pressure promotion, every `epsilon=Pi+D a^-3` has the same constant a0.
   A charge or density boundary condition must fix D. This is a mathematical
   integration constant, not a new-particle requirement.
2. **Distinguish the Newton and cosmological couplings.** With
   `g=G_cosm/G_N`, `Z_H²=8 pi g/(3 kappa²)` and
   `Lambda_geom=8 pi g a0²/(kappa² c⁴)`. The familiar coefficient at
   `kappa=1/2` is recovered for `g=1`, or after explicitly switching to a
   Newton-normalized density definition of Lambda. Horizon and temperature
   relabeling cannot calibrate g or kappa independently.
3. **Keep the material gate separate from its upper branch.** DE1's
   phantom-inclusive edge inverse uses a dynamical acceleration profile.
   DE4's matter-only lower switch requires an actual material-density profile.
   Their shared gate algebra does not make their edge bounds interchangeable.
   The previously background-free DE1 bound is also kept separate from the
   corrected deep bound and the full-profile numerical result.
4. **Use clock stress to distinguish excitation from vacuum offset.**
   `rho+P` cancels the offset. Local sound/dispersion data alone cannot
   recover it. In the specified quartic circular model, adding separately
   identified pressure makes the four-parameter inverse locally invertible;
   this remains a conditional route, not a cosmological detection.
5. **Turn lapse reconstruction into a falsifiable spatial test.** Once
   sources and couplings are calibrated, the inferred vacuum coefficient
   must be spatially constant. Without the trace-coupling calibration, the
   same positive lapse, matter and expansion admit positive, zero or negative
   vacuum coefficients in the explicit bounded counterfamily.

## The path from this checkpoint toward closure

The immediate common-action obligation is to derive **which stress scalar
sets a0**. Vary the proposed vacuum/clock sector with respect to the physical
metric; calculate `epsilon`, `p`, charge and energy exchange; then show that
the same action's static `nu_mono` coefficient is a function of the specified
pressure or density. A pressure law inserted after this variation is still
a postulate. A valid phenomenological theory may retain such an input if
the specification permits it; that is distinct from explaining its origin.

Use the same action to determine measured `G_N`, the background coupling,
the material gate and any clock contribution to the source. The existing
CD26-2 spectral cosmology and charged-clock witnesses do not yet establish
their simultaneous embedding in the operative static theory. Their exact
inverse identities remain useful, conditional construction tools.

With those bridges fixed, perform three independent reconstructions:

1. Infer a0 through the actual filtered source-to-observable calculation,
   retaining baryonic, distance and environment uncertainties.
2. Reconstruct the pressure combination from expansion data and its full
   covariance, and test the normalized ratio above without choosing an
   unobserved dust abundance.
3. Test the same gate and source branch with edge/lensing data; where a
   clock or lapse observable is available, use its additional inverse to
   test the stress split rather than assume it.

Agreement would constrain a shared physical response. A failure would
identify which proposed bridge must change. Neither outcome alone settles
the microscopic vacuum constant. The full nonlinear constraints,
well-posedness, stability, PPN and same-action observational tests in the
recipe remain required. This checkpoint closes the stated algebraic inverse
calculations, **not the complete gravity theory**.

## Evidence and current literature

The [accepted evidence](EVIDENCE.md) includes **31 compiled Lean statements
in four files** and **six validated bounded-run manifests**. The scripts use
exact symbolic identities, explicit non-identification
families, rank tests, negative controls and declared finite illustrations.
The Lean files certify stated mathematical bridges with their hypotheses;
they do not certify empirical truth or a complete field theory. Accepted
compiles, hashes and counts are consolidated by `verify_evidence.py` in
`evidence_summary.json`; failed/superseded attempts are retained separately.

The [source check](SOURCE_CHECK.md) acknowledges the known background dark
degeneracy, credits the repository's earlier pressure/density calculations,
and records the newer August 2026 DESI Ly-alpha paper. Existing 2025 CPL
illustrations are not presented as a September 2026 likelihood. No new data
fit or global novelty claim is made.

The [standalone figure](reconstruction/plot_run2/inverse_relationships.pdf)
shows why density promotion and pressure promotion predict different scale
histories, and why the same constant pressure can have different w(z).
All curves are declared synthetic examples.
