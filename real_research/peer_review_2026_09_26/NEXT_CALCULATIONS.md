# Next calculations: continue the existing work without pooling models

The peer review is [here](README.md). Preserve both exact branches requested by
the user. Reuse the prior response/inertia and gate-variation derivations in
`closure_resume_2026_09_26` and `closure_doors_2026_09_26`; do not restart their
already completed calculations or treat known obstructions as new results.

## 1. Resolve the actual source/force operator before another pooled window

**Inputs:** L361 action, L377 PM force and L370 region force; use one shared
gate and one declared kernel. The present PM solver computes a Newtonian
field from global baryons, then masks the constitutive response. The merger
solver restricts the baryonic source to each connected region first. These
operations do not generally commute.

**Next calculation:** derive which operation follows from the chosen action,
including source reciprocity and interface terms. Evaluate both existing
operators on the same resolved spherical halo with an exterior baryonic
source, and compare the physical potential/force, boundary flux and source
mass. Test a shrinking mesh and a no-gate control. Declare a controlled
approximation only with a measured or proved error appropriate to the
observable; otherwise implement the action-derived operator in both solvers.

**Pass criterion:** one explicitly identified operator and matching source
couplings on both sides. Similar retained total mass is insufficient.

## 2. Repair the active merger-gate mismatch

Make p and xc0 explicit inputs of the merger evaluation; record the actual
resolved gate in every result. L370 already defines `p2_x2.0`, but L371
imports `p1_x1.5`, and L381/L387 never replace it. The lensing root and both
main/substructure map calls must use the intended input. Make source
operator, kernel, a0 footing, background, retention epoch and shape explicit
alongside the gate so a future adapter cannot silently inherit another model.

**First physical rerun after item 1:** one S2 case at 600 km/s under the matched
gate, with its own matched intact-carrier control. The old p1 intact reference
must not be demanded of a p2 calculation. Then evaluate whether slower kicks
remain informative. L386/L387's pending status is not a positive result.

Run each exact kernel as its own branch. An exact-kernel rerun needs its own
retention and core-shape calculation; it cannot reuse `nu_mono` results by
renaming them. Candidate kick/decay dynamics must retain their phenomenological
label until derived from the permitted field action.

## 3. Finish the omitted filter variations, retaining the existing algebra

XC1's flat decoupling expansion can be reused. Start from the existing
localized heat action and its endpoint terms, or the exactly eliminated
weighted adjoint form. Include delta S from metric and clock variation
before eliminating the lapse/shift/auxiliary. Derive the mixed quadratic
symbol and cubic/quartic vertices on one admissible nonzero background.

**Controls:** the direct fixed-metric limit must reproduce the old cubic
counting; the hard/soft heat variation must reproduce the explicit Duhamel
coefficients in the review. Track momentum-dependent kinetic normalization.
Do not assume one Gaussian suppression per varied field leg. Treat the
`nu_mono` splice as nonsmooth unless an explicit smooth alternative is chosen;
choosing one changes the branch and requires its own static comparison.

**Pass criterion:** a bound on all physical interaction channels of that
same reduced action over a stated background and momentum domain. A tiny
coupling from one selected vertex is not a full strong-coupling pass.

## 4. Address the actual zero-field configuration

The test configuration is U=constant on a compact leaf, including the
homogeneous cosmological sector. Both exact laws have a square-root flux
response to an amplitude perturbation. Generic simple-zero quadratures
cannot settle this case.

**Next calculation:** state the physical-time unknowns and evolution norm,
then derive a solution-difference or monotonicity estimate for the full
constraint-reduced equations at this background. Keep k=0 distinct from
nonzero spatial harmonics. If a nonsmooth variational method works, prove
its applicable hypotheses instead of claiming an ordinary bounded tangent.

For the auxiliary leaf solve, reuse the valid monotone-kernel convexity
argument. For RAR and EXP either establish the required lapse restriction,
an actual nonconvex solvability theorem, or derive and test a modified filter.
Replacing the filter changes its metric/clock variation and empirical gates.
Repair XC2's numerical lapse fixture so its supplied acceleration is exactly
D ln N; it currently rescales these separately.

## 5. Continue response/inertia construction on both exact laws

The previous EXP result and this review's RAR extension identify the same
small-alpha obstruction in the current scalar block. Preserve both physical
potentials and the measured Newton constant while changing the architecture.
Use the existing generalized auxiliary-weight and integrated-primitive
calculations in `closure_doors_2026_09_26/response_inertia` as the starting
point. No repeat of the 243-cell momentum scan is needed.

**Pass criterion:** an explicit same-action construction that preserves the
chosen exact static law and its lensing, counts the clock/other modes, and
remains regular and healthy over a declared nonempty domain. Extend that
domain before claiming cosmology, full PPN or nonlinear closure. A bounded
low-field witness is useful progress, not the entire theory.

These items remain open research obligations. Their listed order exposes
dependencies; it does not claim that a solution is guaranteed or that the
alternatives are exhausted.
