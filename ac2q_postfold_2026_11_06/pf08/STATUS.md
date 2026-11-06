# PF08: coupled steepening and the native-continuation gap

The requested scientific classification is **not closed**. This phase strengthens
the case for coupled compressive breakdown and repairs another numerical
constraint issue. It does not establish that every admissible singular native
continuation fails, or that one is uniquely selected.

## Numerical evidence

The Fourier/GMRES constraint solver agrees with the dense solver. Solving for
the polarization derivative avoids high-resolution derivative roundoff. An exact
constraint-based expansion eliminates cancellations between large derivative
terms in the adapted momentum rate. The reduced state evolves only the mean
longitudinal momentum and reconstructs its spatial dependence; it checks the
original canonical rate through the differentiated constraint.

The current reduced implementation separately enforces reconstructed mean,
tangent mean and unaugmented tangent equation compatibility. Six validation
checks pass. At t=.5 the charge discrepancy from the prior formulation is
5.2e-13; the canonical momentum rate discrepancy is 1.4e-10 relative.
See reduced_validation002/result.json and REDUCED_REVIEW.md.

| Independent points | First failing time | Charge gradient there | Stop |
|---|---:|---:|---|
| 511 | 1.412500 | 1.5991 | momentum-field spectral tail >1e-3 |
| 1023 | 1.441875 | 2.5277 | momentum-field spectral tail >1e-3 |
| 2047 | 1.459844 | 3.9844 | momentum-field spectral tail >1e-3 |
| 4095 | 1.471250 | 6.3067 | momentum-field spectral tail >1e-3 |

These are **accuracy stops, not physical singularities**, and failing steps are
not accepted evolution. Charge, positive X, cap separation and the reconstructed
constraints remain well controlled at the reported stops. The gradients and
stop times increase with resolution. At shared t=1.4, charge extrema agree to
less than 1e-5 relative; peak charge gradients differ by 0.57% between 511 and
1023 points, and 0.0068% upon halving the 511-point timestep. These are endpoint
diagnostic comparisons, not full-field norm convergence or an event-time proof.
See comparison001/result.json. The 4095-point run uses larger evaluation padding after t=1.423; it is
therefore not a pure same-padding spatial refinement. Finer runs prolong *valid* checkpoints; they do
not recover any unresolved history or independently re-evolve fine initial data.

This remains the constant-V dimensionless stress fixture, not a canonical
astrophysical parameter prediction. No artificial viscosity, surface term or
postshock prescription has been added.

## Analytic progress

The exact auxiliary principal system is genuinely nonlinear near the homogeneous
reference state. A finite-coupling frozen-auxiliary simple wave is not an exact
solution, so that calculation alone cannot prove breakdown.

The curved auxiliary constraint system nevertheless has a weighted positive
energy identity. It supplies a periodic inverse bound without differentiating
matter stress or losing coefficient derivatives, provided clock, cap,
hyperbolicity, metric and slice-length margins hold. A previously omitted
-2P E_beta K/r gradient forcing has been restored. See
principal_review/COERCIVITY.md and CURVED_COERCIVITY.md.

This inverse excludes a freely adjustable regular auxiliary time rate on a
closed controlled clock slice: its homogeneous kernel is zero. It does not
select a distributional interface stress after those controls are lost.

A covariant characteristic calculation also removes free spin-connection
derivatives. The direct gradients w_sigma=K+sigma e(log r)/c have a self-quadratic
coefficient G/4>0 near the reference state; an r,A-dependent positive weight
cancels the opposing-family quadratic product exactly. Five symbolic checks in
riccati002 pass. The independently audited covariant variation estimate and weighted-gradient
comparison now give a conditional breakdown argument for narrow localized
packets. The small-amplitude auxiliary and ADM constraint construction is
also available. See principal_review/RIEMANN_SOURCES.md. The remaining
foundation is a full constrained local-existence/continuation theorem in the
hold law's available finite regularity, including constraint propagation.
The clock-gauge gradient block is symmetrizable, but the native W_PP(P)
has an absolute-value cusp at P=0. A naive high-Sobolev smooth-coefficient
existence theorem therefore does not apply to generic crossing data. A tailored
characteristic or finite-regularity argument is needed; smoothing the hold law
would change the model. This obstruction to one proof strategy is not evidence
of illposedness.

## What remains undecided

1. Establish the full nonlocal coupled local-existence/continuation theorem
   and apply it to the audited constraint-compatible localized packet family.
   A clock-gauge first-order hyperbolic/elliptic reduction is a candidate route;
   its constraint propagation and regularity have not yet been proved.
2. For singular continuation, fix an admissible native solution class and show
   existence plus uniqueness from the same incoming smooth data, or prove its
   failure. An undefined nonlinear distributional product is not a proof of two
   distinct solutions; two different regularizers are two different theories.

The earlier PF07 no-layer theorem still excludes bounded regular native layers
under its stated trace, current, metric and compactness hypotheses. Those
hypotheses must not be silently extended to clock degeneration, cap
concentration, singular gravity, nonmeasure currents or bulk oscillatory
stress defects. No such singular escape has been constructed and uniquely
selected, but their universal exclusion has not been proved either.

The defensible result remains: **AC2q has no demonstrated predictive postfold
completion as written. A completion is needed to use it beyond breakdown;
whether it can be derived from a native singular limit remains open.** This is
not yet a theorem that new physical degrees of freedom are unavoidable.

All 26 PF08 experiment manifests validate against their recorded artifacts.
Stopped runs remain stopped; manifest integrity does not validate a physical
claim. The derivative-growth figure is refinement.png.
