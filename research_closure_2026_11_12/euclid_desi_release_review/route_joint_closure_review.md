# Independent audit of dimensionless galaxy–BAO closure design

12 November 2026. Conditional algebra/identifiability review; no data fitting. Galaxy-route premise is supplied, not proved here: resolved galaxy data must independently identify T(z)=D_A(z)a0(z), in velocity-squared units, without fixing stellar M/L normalization or importing a cosmological distance prior. The present audit does not establish that an available sample measures T.

## Verdict

Algebra and units PASS under the stated GR-FRW and component-conservation assumptions. This is a potentially useful conditional measurement design: a joint galaxy/BAO fit can test kappa without calibrating H0 or the absolute BAO ruler. It does not derive kappa or establish a healthy gravity theory. Identifiability is conditional and can fail exactly; common-mode calibration remains binding.

## Definitions and derivation

Write u=1+z. Let DM=u DA be transverse comoving distance and DH=c/H. BAO observables are dM=DM/rd, dH=DH/rd, with one common constant sound-horizon ruler rd.

    q = T u/(c^2 dM)
      = DA a0 u rd/(c^2 DM) = a0 rd/c^2,
    h = 1/dH = H rd/c.

T has units m^2/s^2. q and h are dimensionless. This cancellation uses the geometrical DA=DM/u definition in FRW; DM is the transverse, not necessarily line-of-sight radial, comoving distance. If observational DA was inferred via luminosity distances, distance duality and its calibration are additional assumptions.

For mass-equivalent densities and constant GR Newton constant G,

    H^2 = (8 pi G/3)[rho_m0 u^3 + rho_r0 u^4 + rho_DE(z)]
          - k c^2/a^2.

Define A=(8 pi G/3)rho_m0 rd^2/c^2, B analogously for radiation, and K=-k rd^2/a_today^2. Since a0^2=kappa^2 c^2 G rho_DE,

    h^2 = A u^3 + B u^4 + K u^2 + C q^2,
    C = 8 pi/(3 kappa^2).

Thus kappa=1/2 predicts C=32 pi/3; a measured positive C gives |kappa|=sqrt[8 pi/(3C)]. Only the magnitude of kappa is recoverable from this squared relation. Positivity of acceleration convention usually fixes kappa>0. No H0, absolute rd or early omega_m prior appears in these coefficients. A,B,K remain nuisance coefficients, not known values.

The rd cancellation is a shared-scale symmetry: rd -> lambda rd rescales h and q by lambda and A,B,K by lambda^2, leaving C unchanged. This is a conditional algebraic invariance, not a claim that real BAO reduction has no calibration or cosmology dependence.

## Identifiability, bin count and explicit determinant

In a flat, late-time approximation B=K=0, define hi=1/dHi and qi from Ti,dMi. Two distinct redshifts give

    D = u1^3 q2^2 - u2^3 q1^2,
    C = (u1^3 h2^2 - u2^3 h1^2)/D,
    A = (h1^2 q2^2 - h2^2 q1^2)/D.

Full rank requires D != 0. Near-zero D makes C unstable. If q^2 is proportional to u^3 over the sampled range, the dark-energy contribution is observationally indistinguishable from matter in this test. Distinct redshifts alone do not ensure identifiability. If q is constant and redshifts differ, rank is normally two; constant a0 does not itself destroy rank.

Two exact bins estimate two coefficients with zero residual degrees of freedom. They may constrain a preselected C by requiring one common A, but do not independently establish the assumed two-column functional decomposition. At least three bins overdetermine the free A,C model; four overdetermine A,K,C; five overdetermine A,B,K,C. These are necessary counting conditions, not power forecasts. Correlations and nearly collinear columns may leave effectively much less information. A fixed-kappa null has one fewer free parameter, so its goodness-of-fit count must be calculated separately.

In the full design, rank must be checked for the columns [u^3,u^4,u^2,q^2]. Any q^2 in the span of the first three makes C unidentifiable. Narrow redshift ranges make u^2,u^3,u^4 and a smooth q^2 difficult to distinguish even without an exact identity. Radiation cannot simply be declared measured without its own prior; dropping it is an explicit controlled late-time approximation. Massive-neutrino transitions and nonconserved components require their actual redshift functions rather than automatically assigning them to u^3 or u^4.

## The first uncertain implication is the galaxy T measurement

If only deep-limit rotation is observed, velocities generally constrain a mass–a0 product; if only Newtonian accelerations are observed, a0 is unobservable. Resolved imaging alone does not supply an absolute baryonic mass. Therefore the phrase 'without overall M/L' is not enough: an explicit rank/sensitivity calculation must show the galaxy likelihood separates T from stellar amplitude, gas calibration, inclination, pressure support, radial M/L gradients and environment. A transition-spanning, structurally constrained galaxy model might do so, but this remains the upstream obligation. Nonparametric radial M/L can absorb curvature that would otherwise appear to measure T.

Infer T directly in angular coordinates. Deriving physical radii/masses with an assumed cosmology, fitting a0, and multiplying by that same assumed DA does not prove independence unless the full inference and its priors transform covariantly. Neither independent T values nor robust astrophysical errors have been established in this note.

## Covariance and distance treatment

q contains dM, while h contains dH from the same anisotropic BAO fit. Their covariance, cross-redshift covariance, T errors and common astrophysical calibration errors must be retained. Ordinary least squares with noisy q^2 treated as an exact regressor is inappropriate and can bias C. A generative likelihood for raw/latent [T,dM,dH] is preferable. Nonlinear inverse/square transformations also make Gaussian covariance propagation unreliable for broad errors or q near zero.

If T estimates use the same photometric redshifts or survey calibrations, they can correlate among bins; if galaxies overlap BAO samples, assess shared selection/cosmic variance. Distances and redshifts must be evaluated on consistent windows, not paired by nearest effective-redshift labels without a justified interpolation. FRW also relates DM and H through the curvature-dependent distance integral; enforcing that relation may add information but must be declared. It does not license treating BAO transverse and radial estimates as independent.

## Counterexamples / failure modes

1. Matter-like dark energy: q^2=L u^3 gives h^2=(A+CL)u^3 in the flat late model. Every C fits after shifting A. No precision or sample size at those redshifts breaks the exact degeneracy without other information.
2. Common galaxy calibration: if measured Tobs=b Ttrue with constant b, then qobs=b qtrue and Cfit=Ctrue/b^2, hence kappafit=b kappatrue. Avoiding the absolute ruler does not remove the galaxy acceleration-calibration floor. Large N does not cure b.
3. Extra untracked component: an additional density proportional to q^2 shifts C and exactly mimics another kappa. An independent cosmological constant creates another constant column; if q^2 is also constant, it is exactly degenerate with C. The design assumes the entire residual dark-energy density is the density in the a0 relation.
4. Modified background gravity: replacing the Friedmann source by redshift-dependent Geff, extra kinetic terms or a different gravitational equation changes the decomposition/coefficient. Failure of C=32pi/3 rejects the specified combined GR-background + conserved-component + a0 hypothesis, not the identity in every modified-gravity completion. If the galaxy law uses a distinct local G, its relation to cosmological G must be supplied.
5. Evolution of the BAO ruler, opacity/distance-duality failure where applicable, or lensing/kinematic reconstruction using hidden fiducial distances can spoil the cancellation. These are assumptions to check, not reasons to dismiss the algebra.

## Repo overlap and distinction

CFG689 README lines 18–22 explicitly uses a pre-switch rd=147.07 Mpc and conserved physical matter density to turn BAO into absolute H and rhoDE. Lines 68–69 record that its no-CMB/no-H0 positivity-only bracket cannot fix matter density. Its statement that BAO alone cannot distinguish the framework from LCDM (12–17) remains intact: the present design adds an independently measured galaxy acceleration scale.

AT1 README lines 7–9 uses same-estimator a0(z)/a0(0); kappa cancels and it cannot pin kappa. Lines 21–29 emphasize the common-mode systematic floor and inconclusive overlap. The proposed joint dimensionless coefficient preserves the relative acceleration-to-BAO scale and therefore can in principle retain kappa information, unlike an a0 ratio alone.

This bounded search checked those named predecessors; it does not establish broad novelty across the entire repository or literature. The useful new route-level synthesis is a scale-free joint coefficient test contingent on a truly identifiable T. It is not BAO-only evidence and not a result already obtained by AT1/CFG689.

## Next discriminating step

Before data agreement fitting: (1) independently prove or refute T identifiability with the galaxy forward model and realistic nuisance freedoms; (2) generate only synthetic measurement designs with known truth, including the q^2 proportional u^3 rank-collapse mutation and a common T calibration mutation; (3) evaluate the weighted full-design condition number and expected uncertainty on C at actual available redshift windows, with BAO covariance; (4) test the fixed coefficient against a free-C alternative only after sample/priors/windows are frozen. If the upstream T rank or common-mode floor fails, record NO VERDICT. If it succeeds, this is a concrete model-conditional measurement-design advance, not a completed theory.

## Reviewed source SHA256
- `campaign_fresh_gravity/CFG689_native_ruler_bao/README.md`: `a60302df185927cdc6b7532655937dceef33f7ea407d04ff59cb7dabcf668ca8`
- `rebuild_2026_10_22/AT1_a0z_tracking_decision/README.md`: `f82973dddd002546f5294cf0926c651d5574e28be87d13db94b23b5229e1f3a4`


## Fix-forward: earlier inverse-cosmology prior art and two Newton constants

A further explicit predecessor was located after the initial scoped search: `real_research/dark_energy_inverse_2026_09_26/scales/REPORT.md` lines 24–46 distinguishes gG=G_cosm/G_N. Its lines 34–38 already state that background-rate/acceleration comparison identifies kappa/sqrt(gG), not kappa alone. Therefore the general joint coefficient is

    C = 8 pi gG/(3 kappa^2),
    kappa_cosm = kappa/sqrt(gG) = sqrt[8 pi/(3C)].

The C=32pi/3 null is the joint hypothesis kappa=1/2 AND gG=1; equivalently it is kappa_cosm=1/2. The earlier single-G derivation is valid only under that explicitly stronger assumption. With unknown constant gG the design does not isolate local-normalized kappa. With running gG(z) the single-coefficient column model generally fails and must be extended.

`real_research/dark_energy_inverse_2026_09_26/reconstruction/RESULT.md` lines 112–150 already provides an inverse pressure-ratio test, cancellation of H0/kappa/constant gG in a theoretical redshift ratio, and an integral Friedmann family whose constant-a0 limit is vacuum-plus-dust. Thus the general acceleration–background inverse connection and constant-a0 Friedmann relation are prior work in this repo. The proposed angular T measurement plus uncalibrated BAO observables is a narrower measurement-design synthesis; do not present the background relation itself as new. Pressure tracking and density tracking coincide for constant vacuum but differ for evolving w, so that predecessor is overlap rather than universal algebraic identity with the present density test.
