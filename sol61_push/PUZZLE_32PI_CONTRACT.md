# Coefficient investigation contract

Requested by Carl after the first review: investigate the 32pi puzzle too, using best judgment. Base checkpoint: 8a295b11e63ed4ddd34d489343309c0bca6c3725. All writes remain under sol61_push; no other lane is modified. Goal remains OPEN.

Exact target, in c = 1 units: Lambda = 32 pi a0^2, equivalently G rho_Lambda/a0^2 = 4, with Lambda = 8 pi G rho_Lambda. In physical units rho_Lambda is mass density and a0 = (c/2) sqrt(G rho_Lambda). The puzzle is 32 pi, not 32 pi squared; the latter arises after multiplication by a chosen Schwarzschild horizon area.

A solution must derive the coefficient and identify the same a0 in galaxy dynamics from one action plus physically justified boundary/formation data. Fitting a free constant to 32 pi, finding that number elsewhere, or restating the target does not qualify. Empirical exactness is itself unsettled: the current evidence lane does not distinguish nearby coefficients at existing systematic precision.

Routes executed:

1. Exact P2 action reconstruction and vacuum normalization: independently obtain the primitive and test whether its zero/high-field conditions fix vacuum energy. Prior K already excludes a generic offset derivation, including the same inverse interpolation; this is an explicit target dictionary, not a novel route or rerun of its data scan.
2. Internal dipole response: eliminate the EFT length, impose the published linear-cancellation constraint on charge ratios, derive a parameter-independent bound on the required oriented amplitude product, and test phase averaging as a substitute for state selection. This extends the old coefficient scan by using its cancellation constraint. No actual formation mechanism is inferred.
3. Same-field vacuum selection: investigate a simple classical gauge condensate L = -V(X), X = sum F_a^2/4, with an isotropic purely magnetic background. Derive its stress and perturbative electric kinetic matrix at a putative w = -1 vacuum. This is a bounded subclass, not the full non-Abelian dipole action or all condensates.
4. Stream orientation: extend the local response to three spatial dimensions. For dipoles linear in g with constant response matrices determined by a single incident velocity, compute the longitudinal cross term and test sign reversal and directional uniformity. This is a necessary orientation-selection check, not an exclusion of nonlinear or spatially evolving media.

The proposed RG route was deprioritized after reviewing prior Q/U/K lanes: no specified quantum action or beta functions are available to compute a new selection condition. It remains deferred until such an action is fixed. The executed magnetic route is more directly tied to the previous medium investigation.

Checks use exact symbolic real algebra and deterministic float64 evaluations; no stochastic sampling. Numerical bounds are explicit in coefficient_constraints.py. The script's exit code certifies only its declared identities and scoped obstructions. A mutation changing the required dipole product must be rejected.
