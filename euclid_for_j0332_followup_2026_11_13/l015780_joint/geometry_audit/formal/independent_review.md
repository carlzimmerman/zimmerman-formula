# Independent audit of FiniteCapacity.lean

**Verdict: proved as written for the declared finite-array/box theorem.** The observational and PDE interpretation remains conditional. I inspected the raw definitions/proofs, independently reconstructed the generator output and exact rational estimates, and compiled the unchanged source in the recorded Lean workspace. No certificate inputs were mutated. This review does not certify a physical theory exclusion.

## Exact audited instance and source bridge

Source SHA256 `f0de03d4b468ab083fcc38b093169437a95eff2192d6b118175e5fc520f5d89e`; generator SHA256 `baca959852264e9c256fbf69f6856ab54b5a6545937c42372140491c947ddea6`; NPZ SHA256 `4c86113c50ac5ab9db3bcd57933b4daf604202d0faf81bc1b71b70c6ed712e3a`. All agree with instance.json at review. Generator template was read as a literal via Python AST (not executed), its explicit substitutions independently reconstructed, and the reconstructed text is byte-identical to FiniteCapacity.lean.

NPZ extraction selects inclination index0=90.0deg and mass index9=11.925000000000002. Array `alpha_hat_sky` at these indices is exactly equal to the eight JSON floats. Each JSON exact rational equals Fraction.from_float of its binary64 entry, and each is substituted in the correct coordinate/point slot. Thus the theorem represents the actual STORED floating-point values exactly as real rationals, not a decimal re-rounding of them. That does not make those floats exact solutions of the field equation.

NPZ theta_sky is [[−1.95,−.55,2.65,−.55],[−1.85,−2.65,−.75,1.75]], matching the Lean exact decimal-rational coordinates by intended decimal values. Binary64 representations of these input decimal coordinates are not themselves the Lean rational decimals; any physical astrometric tolerance is outside this certificate. The theorem fixes these positions exactly and robustifies only deflections. The mass11.925 stored-grid fixture is distinct from the recomputed point aperture fixture11.926878886 in shape_probe_01; do not silently identify them.

The four-decimal centerAX/AY values are correctly close to the stored entries (largest discrepancy<0.000043arcsec), far inside the declared±0.05 component box. Lean also proves stored_X/Y_in_box directly. Consequently the hypotheses are satisfiable and the robust theorem is not vacuous: e.g. choose arrays at centers, or use the stored arrays, and beta=0 or1 is admissible. There is no incompatible hidden parameter assumption.

## Mathematical proof reconstructed

The functional uses x weights[−72,7,130,−65] and y weights[−69,−61,0,130]. Both weight sums are0. It therefore annihilates arbitrary constant source translations. Its shear contractions with the fixed positions also vanish exactly, and nuisance_cancels proves the resulting expression `1033.6−beta*projection(alpha)`. Source definitions encode exactly a uniform trace-free matrix [[g1,g2],[g2,−g1]], with BOTH g1 and g2 arbitrary real arguments. No shear-size constraint is hidden.

four_pair_identity is the valid scalar pairwise identity under zero sum weights. projection_pair_identity expands the corresponding12 coordinate-difference terms directly by ring; it does not merely assume the general identity. The coefficient absolute values sum1336. If every Euclidean pair separation≤0.3, then each x/y coordinate difference lies within±0.3. Applying the matching one-sided inequalities term by term yields4*projection≤1336*.3=400.8, hence projection≤100.2. This is conservative: independent coordinate/pair bounds need not be jointly attainable, but enlarging the source gate in this direction cannot create a false rejection.

For the deflection centers, exact projection is1788627/2500=715.4508. Independent component deviations±.05 can change the functional by at most(534)*.05=26.7, giving upper bound742.1508. The Lean proof deliberately relaxes that to750; slack is19623/2500=7.8492. No unproved bound or floating comparison enters this step.

For0≤beta≤1, beta*projection(alpha)≤beta*750≤750, even when the deflection projection might be negative. Therefore source projection≥1033.6−750=283.6, contradicting the gate upper100.2. Both beta inequalities are used with the proper signs; there is no illicit multiplication by an unknown-sign quantity. The robust theorem quantifies ALL real8-component deflection arrays inside the specified box, ALL beta∈[0,1], and unrestricted realg1/g2. The nominal theorem is a valid specialization using exact box-membership proofs.

## Compilation and trust checks

Recorded command independently executed:

`lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/euclid_for_j0332_followup_2026_11_13/l015780_joint/geometry_audit/formal/FiniteCapacity.lean`

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026`.

Observed exit0. Only warnings were unused aY/aX binders in sourceX/sourceY, which are harmless (each component uses its respective deflection). All five #print axioms outputs reported exactly `propext, Classical.choice, Quot.sound`; no sorryAx or custom axioms. Source inspection found no sorry/admit, unsafe, implemented_by, or native_decide. The imported Mathlib foundation and normal Lean kernel/library trust remain the ordinary formal trust base.

## Scope and remaining bridges

The theorem is a finite geometric impossibility result, stronger than a statement about one rounded float array because it covers a full explicit deflection box. The box is a mathematical robustness domain, NOT an interval-certified PDE error estimate, mass uncertainty region, or confidence region. Field numerical convergence must separately imply actual deflections lie in that box before transporting the theorem to an exact continuous field solution.

Zero external convergence is built into sourceX/Y. Nonzero convergence adds a term proportional to theta and can alter the contradiction. Arbitrary nonlinear perturbers, multipane terms, spatialM/L gradients and an environmental change to the nonlinear field are not represented by the two shear coefficients. Beta≤1 is an explicit enlarged lensing-efficiency assumption, not a measured source redshift. There is no stellarpopulation, DESI dispersion, image likelihood or source-redshift statement in Lean.

The supplied positions being corresponding images of one source region with pairwise diameter≤0.3arcsec is a physical association premise, not a theorem established from image pixels. This gate bounds diameter, not radius; substituting a radius0.3 premise would change the claim. The mass/inclination/profile identification relies on external NPZ provenance and the generator checks above, not a Lean PDE or photometry calculation. Continuous uncertainty in theta, light shape, stellar mass or inclination is not certified. This exact finite result must not be described as an unconditional exclusion of the user's theory.
