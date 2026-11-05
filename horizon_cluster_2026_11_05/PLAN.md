# Black holes, galaxy sizes, cluster interactions, and the 32π puzzle

Authorized 2026-11-05: comprehensive computations and rigorous investigation.
Owner: root agent. Base checkpoint HC-001, Git 9fd8b73d126df4184f4efbb84ca3e420cc0485f6.
Existing checkout is dirty; exclusive write scope is this directory. No manuscript changes.

## Target contract

Determine whether observed black-hole properties explain galaxy/cluster gravitational discrepancies beyond measured baryons, established environmental effects, and accretion feedback; determine whether any independently specified mechanism selects AΛ=32π². A correlation alone is not causation or a derivation. A failed mechanism is not a universal exclusion.

Three distinct routes: (H) horizon/curvature identities and scale bounds; (G) ordinary gravitational mass, tides and collective fields; (D) observational size/host/environment relations and feedback. The first uncertain arrows are respectively a physical selection principle, enough extra acceleration without double counting, and an independent residual association after confounders/selection. Execute inexpensive discriminators first.

Conventions: SI; Λ=1.09e-52 m^-2 as a fiducial input, with sensitivity tests; a0=1.2e-10 m/s² as an independent empirical reference, not a fitted target. Also report aΛ=c²sqrt(Λ/(32π)) separately. Schwarzschild radius rs=2GM/c²; Kerr area is 8π(GM/c²)²(1+sqrt(1-χ²)). Galaxy Re means projected circularized spheroid half-light radius, NOT disk edge, full diameter, halo radius, or 3D half-mass radius. Cluster M500 and R500 must stay paired. Ordinary gravity, MOND diagnostics, and hypothetical new couplings are labeled separately.

## Comprehensive work queue

Statuses: [x] executed/documented, [ ] open. No checkbox denotes proof unless the linked evidence says so. Final executed status is in STATUS.md.

### A. Provenance and prior work
- [x] A01 Fix hypotheses, units, area definitions, and success/failure criteria.
- [x] A02 Pin base revision and isolate outputs from concurrent research.
- [x] A03 Read the 32π record including corrections and October coefficient counterfamily.
- [x] A04 Read the collective-cluster report; distinguish archived claims from fresh verification.
- [x] A05 Audit the old Jensen/conservation claims with nonspherical boundary counterexamples.
- [x] A06 Hash all new inputs, code, results, and record versions/commands.

### H. Horizon and cosmological scale tests
- [x] H01 Compute rs, horizon area, surface gravity, and AΛ for the complete acquired sample.
- [x] H02 Compare the constructed puzzle radius/mass with de Sitter and Nariai limits.
- [x] H03 Scan spin χ=0..1; test whether Kerr area can remove the scale discrepancy.
- [x] H04 Test summed areas at fixed total BH mass; contrast sum(M_i²) with (sum M_i)².
- [x] H05 Bound even an extreme cluster made entirely of black holes.
- [x] H06 Derive r_M²=rs R*/2 for R*=c²/a0; label this an identity, not new dynamics.
- [ ] H07 Separate local curvature, Ricci vacuum curvature, and Weyl tidal curvature.
- [x] H08 Scan Λ and a0 independently; never use their proposed relation as validation.
- [x] H09 Specify what extra equation would select the coefficient rather than define it.

### G. Ordinary gravity and interactions
- [x] G01 Compute BH circular-speed contributions at 1, 10, 100 and 1000 kpc.
- [x] G02 Compute rs, r_infl=GM/σ², r_M=sqrt(GM/a0), and turnaround radii separately.
- [ ] G03 Bound direct BH fractions relative to host stellar mass, with uncertainty.
- [ ] G04 Compute pair forces, tidal acceleration, escape speeds, and orbital times.
- [ ] G05 Scan separation, BH mass, host mass, and cluster enclosed mass independently.
- [x] G06 Compare gravitational acceleration with Λ repulsion and expansion times.
- [x] G07 Evaluate nonrelativistic compactness; test whether an ordinary cluster is near a common horizon.
- [x] G08 Evaluate fixed-mass clumpiness using surface-flux QUMOND integration and convergence.
- [x] G09 Check alternative interpolation functions and Newtonian limit.
- [ ] G10 Test adding BH mass to a fixed stellar distribution without counting it twice.
- [ ] G11 Solve galaxy-specific mass profiles and projected kinematics where data permit.
- [ ] G12 Fit actual cluster gas/stellar/lensing profiles with covariance and matched apertures.
- [ ] G13 Model merger/non-equilibrium systems separately from relaxed clusters.

### D. Data assembly and observational inference
- [x] D01 Acquire a named published size/BH/stellar-mass sample with source locators.
- [x] D02 Verify row count, duplicates, missing fields, flags and upper limits.
- [x] D03 Compute descriptive log mass–log size slopes by morphology and exclusions.
- [x] D04 Test constant horizon/galaxy-size ratio; compare free slope and scatter.
- [x] D05 Fit BH mass jointly with size and stellar mass; use held-out prediction.
- [x] D06 Bootstrap sampling uncertainty, permutation controls and influential-object removal.
- [x] D07 Propagate quoted BH/mass/distance uncertainties; expose missing size systematics.
- [ ] D08 Obtain velocity dispersion, mass-measurement method and resolution/selection information.
- [x] D09 Assemble environment membership and central/satellite status with source provenance.
- [x] D10 Acquire Gaspari et al. 2019 85-system hot-halo tables and audit aperture definitions.
- [ ] D11 Match independent rotation curves or lensing to directly measured BH masses.
- [ ] D12 Fit acceleration/lensing residuals versus BH mass conditional on baryons, size and environment.
- [ ] D13 Use a censored errors-in-variables hierarchical model, distance covariance and selection model.
- [ ] D14 Test dwarf/bulgeless galaxies, upper limits, compact relics and overmassive-BH systems.
- [ ] D15 Validate on an independent sample; report power and minimum detectable effect.

### F. Feedback versus gravitating mass
- [ ] F01 Compute energy-budget envelopes ε M_acc c² versus cluster thermal/binding energies.
- [x] F02 Distinguish accreted mass, present BH mass, radiative and mechanical efficiencies.
- [ ] F03 Acquire cavity pV, buoyancy ages, jet power, gas T/n and cooling luminosity.
- [ ] F04 Compare cavity/jet indicators with hydrostatic residual and independent lensing residual.
- [ ] F05 Model radial redistribution and nonthermal pressure without treating heat as extra dark mass.

### N. New mechanism and adversarial validation
- [ ] N01 Write a candidate horizon-coupling action/force law before fitting any coefficient.
- [ ] N02 Check dimensions, conservation, equivalence-principle behavior, weak-field and Λ→0 limits.
- [ ] N03 Require galaxy, cluster, lensing and Solar-System predictions from the same model.
- [x] N04 Reject tautological identities, fitted constants and data-derived BH estimates as independent tests.
- [ ] N05 Freeze discovery/validation splits and compare neighboring coefficients, not only 32π.
- [x] N06 Separate exact derivations, finite computations, literature results and conjectures.
- [x] N07 Produce plots, reproducible commands, numerical tables, limitations and continuation handoff.

## Initial execution plan and decision rules

HC-002: horizon/interaction/feedback scale calculation and an exact counterexample search for overly broad collective-gravity claims. A scale gap closes only the literal area/mass mechanism. Feedback budget sufficiency is necessary, not proof of coupling.

HC-003: complete 104-row numerical table extraction, morphology-aware descriptive fits and bootstrap/held-out diagnostics. The table contains spheroid sizes and stellar masses but no independent gravitational-discrepancy outcome or complete environments; it cannot establish the main causal claim. Missing values and upper limits must not become detections.

HC-004: acquire independent hot-halo and dynamical observations, freeze crossmatch and covariate definitions, then test residuals. Do not manufacture a discrepancy from BH mass or a BH estimate from the same covariate being tested. Formal significance awaits a selection/error model. If acquisition is unavailable, preserve precise missing inputs and continue executable theoretical checks.

No promise to derive an unknown law. The deliverable is an executed, reproducible investigation with explicit remaining dependencies, not an asserted explanation.

## HC-004 scope notes

Checked tasks are scoped to STATUS.md. D07 is a declared sensitivity calculation, not full covariance inference. D09 covers the 85-source environment labels, not a complete external group catalog. H09 specifies the missing selection equation without deriving it. G02 uses the approximate GM/sigma² influence definition. D06 controls are exploratory; no formal discovery significance is claimed. G03–G05 and F01 have partial calculations but remain open for their full stated uncertainty/tidal/binding-energy scope. D11 found only two exact-name SPARC overlaps, one excluded; its population data requirement remains open.
