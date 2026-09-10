# Corrections before spending on the next simulations

Scope: selected current sources and stored outputs, through `cb471a825`.
These are source-review findings, not fresh reruns of the large f32,
Boltzmann, galaxy or hydrodynamic pipelines. No universal novelty claim.

1. **f32 is not exact total α₁ cancellation.**
   `hunt_2026/f32_ppn_k4_spatial_gradient_operator.py` already constructs
   a local projected-gradient action term and differentiates its quadratic
   form. Its output explicitly distinguishes the scalar drag from total α₁.
   For example K_B=1/5, J_Y=1, (ξk)²=10⁴ gives total α₁≈−.800720,
   not zero. The displayed drag is
   −4(2−K_B)/[J_Y(1+(ξk)²)+1]; it is suppressed, not identically zero at
   finite ξk. The pure-aether part remains; the c₄ test gives
   −4(K_B+c₄). The pipeline also documents an unresolved second-order
   normalization issue affecting α₂. A nonlinear action/constraint analysis
   and physical moving-source PPN calculation are still needed. It would be
   inaccurate to call this an entirely unwritten action or a certified cure.

2. **The 300–537 km/s interval is conditional.**
   `fable_independent_2026/L153e_verdict_window.out` itself calls it
   boundary-condition dependent. Alternative lensing prescriptions give
   floors 839 and 1346 km/s, closing that particular interval. A coupled
   baryon-plus-modified-gravity growth calculation is still relevant, but
   its coefficients must be derived from the same action. Those speeds
   are not model-independent observational bounds.

3. **Two-species hydro remains useful; the universal p<3 premise does not.**
   The existing review at
   `fable_independent_2026/reviews/2026-09-10_twenty_recommendations/`
   supplies the explicit smooth barotrope
   P(ρ)=ερ⋆(1−exp(−ρ/ρ⋆)), c_s²=εexp(−ρ/ρ⋆).
   Conservation yields the local exponent
   d ln(c_s²)/d ln(a)=3(ρ/ρ⋆)(1+P/ρ), which exceeds 3 at ρ=2ρ⋆
   even for ε=10⁻⁶ and a dustlike, causal fluid. This does not establish
   viable cosmology, but excludes treating p<3 as a theorem about every
   barotrope. The power-law/asymptotic assumptions must accompany that bound.

4. **Kick tests exist; a resolved simulation is a different missing step.**
   L160 computes a two-body kick/escape filter and growth surrogate;
   L162 varies four retention prescriptions; L164 evaluates redshift-three
   power suppression. L164 explicitly keeps the arm undetermined and reports
   0.780–0.907 power ratios on its model's optimistic surrogate, not a fitted
   Lyα flux likelihood. These are not an N-body or two-fluid hydrodynamic
   validation. A particle-decay toy also does not provide a no-particle clock
   interaction: that energy-transfer law still needs an action.

5. **A high-z rotator is not a framework-independent ΛCDM discriminator.**
   Constant a₀ implies constant v⁴/(G M_b) only on the equilibrated,
   asymptotic deep-MOND branch. The repo's +.33 dex comparator is a specified
   galaxy-model expectation, not a consequence of the ΛCDM background
   equations alone. `.33/.13 ≈ 2.54` is the naive single-measurement Gaussian
   separation even if the comparator and local zero point were exact;
   model scatter and systematics weaken that reading. One must define the
   zero-point axis, selection, inclination, gas mass, pressure support and
   rival prediction before claiming a decisive test.

6. **L166 proves its algebra, not the physical identification of its inputs.**
   `lean_2026/Mondlean.lean` compares f(m_g)≤.105 with f(m_c)≥.988;
   its theorem correctly proves that this one-argument f is nonconstant.
   Mapping a late-time galaxy fraction and an early-time CMB fraction to
   values of the same mass-only function is an additional assumption.
   Epoch dependence alone can produce those two inequalities. Same-epoch
   galaxy-versus-cluster requirements are needed to establish mass dependence.
   Its p<3 hypothesis and chosen g†∝H scale similarly do not prove their
   universal physical applicability. `FINDINGS.md` overstates these
   implications despite the commit's correct "necessity only" warning.

Priority: preserve the exact results, repair these premise mappings, and
derive the one-action clock/lapse and baryon perturbation equations. Do not
spend on a full hydro campaign whose force law has not yet been specified.
The new all-domain clock principal-sign result in README.md is a useful
analytic gate, not permission to combine unrelated successful model pieces.
