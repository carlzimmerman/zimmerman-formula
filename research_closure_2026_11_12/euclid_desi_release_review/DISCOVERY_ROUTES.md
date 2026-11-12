# The strongest surviving lead

12 November 2026. **A conditional observable construction has survived independent algebraic review. No new astronomical confirmation or healthy all-gate theory has been established.** The useful advance is a way to target the acceleration–cosmology connection while removing some nuisance normalizations; we also constructed explicit cases in which the method fails.

## 1. Measure acceleration times distance from radial shape

For a fixed angular baryonic template b(θ), an unknown global stellar mass-to-light multiplier U, and independently measured circular speeds, define

\[
w_i=v_{c,i}^2/\theta_i,\qquad A=D_AU,\qquad T=D_Aa_0.
\]

The simple-μ algebraic rule implies

\[
\frac{w_i^2}{b_i}=A w_i+B,\qquad T=B/A.
\]

The quadratic rule instead implies

\[
\frac{w_i^2}{b_i}=C b_i+E,\qquad T=E/\sqrt C.
\]

Thus the overall stellar normalization cancels separately for each galaxy. This does not require the same mass-to-light ratio at different redshifts. It does require a constrained radial baryonic shape, independent dynamics and enough acceleration range to identify both coefficients. Two radial measurements determine two coefficients; additional resolved modes are required to test the law.

The information calculation gives a precise reason to seek the transition region. For independent log-speed-squared errors, the two-parameter Fisher determinant is

\[
\det F=\sum_{i<j}\omega_i\omega_j(t_i-t_j)^2,
\]

where t_i is the local response to T. Entirely deep data have t_i=1/2; entirely Newtonian data have t_i=0. Both limiting cases lose the needed parameter separation. A single reported flat rotation speed cannot implement this method.

These linear identities are for the chosen pointwise algebraic prescriptions. A general AQUAL disk admits an angular scaling in A and T, but requires its actual field solver; the linear formulas do not become exact disk field equations.

## 2. Combine that observable with DESI without fixing the sound horizon

Write d_M=D_M/r_d and d_H=D_H/r_d. Then

\[
q(z)=\frac{(1+z)T(z)}{c^2d_M(z)}=\frac{a_0(z)r_d}{c^2},\qquad
h(z)=\frac{1}{d_H(z)}=\frac{H(z)r_d}{c}.
\]

Let g_G=G_cosm/G_N be constant. Under a Friedmann background with separately conserved matter and radiation, curvature and the density relation a₀²=κ²c²G_Nρ_DE,

\[
\boxed{h^2=A_m(1+z)^3+A_r(1+z)^4+K(1+z)^2+C_{\rm DE}q^2,\qquad
C_{\rm DE}=\frac{8\pi g_G}{3\kappa^2}.}
\]

This supplies a **joint consistency test without fixing H₀, the absolute sound horizon or an early-universe matter-density prior**. The measured coefficient identifies κ/√g_G. The value 32π/3 tests κ=1/2 together with g_G=1, or equivalently κ/√g_G=1/2. It cannot determine κ and the gravitational coupling ratio separately.

This is noncircular only if T is extracted with a₀ free from galaxy kinematics and light, without imposing the acceleration–cosmology relation. It tests the specified background closure together with the galactic law; it is not model-independent cosmology and does not cover arbitrary modified-gravity backgrounds.

Identifiability has another exact gate: the q² column must not lie in the span of the matter, radiation and curvature columns. For a flat late-time two-parameter fit, two bins can determine two coefficients but have zero residual degrees of freedom; at least three are needed for a shape-consistency check. Free curvature or radiation requires more independent information. The original correlated BAO/galaxy likelihood must be used; noisy q² is not an exact regression variable.

## 3. What the adversarial checks found

The cancellation is narrow and useful, not universal:

- **Radial mass-to-light gradients do not cancel.** An exact positive-density spherical construction reproduces the same flat rotation curve for every positive a₀. A change from a₀ to 0.91a₀ needs only 0.0324 dex of radial M/L variation over the demonstrated window, after a free overall normalization. This is a counterexample, not a claimed empirical gradient distribution.
- **Velocity/inclination calibration remains.** With the light geometry held fixed, a multiplicative bias b in T biases inferred κ/√g_G by the same factor b. The example of a true 55° disk treated as 60° shifts log₁₀T by −0.0483 dex; real light deprojection adds correlated changes.
- **Unmeasured gas can change the radial template.** Known gas shapes with unknown global conversion factors can be included as separate templates, subject to rank and sufficient resolved modes. An arbitrary unseen gas profile cannot be eliminated algebraically.
- **Entirely deep data remove too much information.** They constrain the product of stellar normalization and a₀, leaving the two inseparable. More galaxies in that same degenerate regime do not supply the missing within-galaxy shape information.

The 54 deterministic synthetic checks verify the stated identities and illustrative information calculations, not observational precision. Independent review reconstructed the formulas without using the checking implementation. See the full route and audit files for domains, hashes and limits.

The next check was executed on three existing SPARC development galaxies, using their actual radial sampling and quoted velocity errors. Across **42 local Fisher scenarios**, free inclination produced exact rank deficiency in all six galaxy/kernel combinations. With free stellar/gas amplitudes, the catalogue inclination prior and an illustrative radial M/L-gradient prior, the conditional errors were:

| Existing development galaxy | Simple-μ σ(log₁₀T) | Quadratic σ(log₁₀T) |
|---|---:|---:|
| NGC2403 | 0.080 dex | 0.056 dex |
| NGC3198 | 0.141 dex | 0.086 dex |
| DDO154 | 0.392 dex | 0.600 dex |

These are local sensitivity estimates under incomplete nuisance models, **not measured uncertainties, a new fit or a Euclid forecast**. The M/L-gradient prior is a dimensionless radial power-slope uncertainty of 0.1, not a measured property of these galaxies. Correlated errors, photometric deprojection changes, pressure support and a full AQUAL disk calculation remain outside the check. Its practical result is that transition-spanning profiles are worth pursuing, whereas the deep-only DDO154 template has little normalization-independent information. Fixing the angular gas coefficient and geometry creates misleadingly small optimistic-control errors; knowing a gas conversion factor alone does not fix that coefficient when distance remains unknown.

## 4. Why Euclid matters, and where spectra help

Euclid adds high-resolution light profiles, multiband information and a large candidate population to constrain radial shape, colour gradients and geometry. These are the inputs the method needs beyond a global stellar mass. Foundation does not by itself provide the resolved circular velocities and gas constraints needed to extract T.

A second route derives a matched-clump, opposite-dispersion estimator:

\[
\Delta v_{kl}=\frac{\boldsymbol e\cdot[(\boldsymbol y_{+k}-\boldsymbol y_{+l})-(\boldsymbol y_{-k}-\boldsymbol y_{-l})]}{2k_\lambda},
\]

where k_λ converts velocity into angular spectral displacement. The double difference removes unknown same-line clump positions and common exposure translations. It does not require an Hα centroid to equal the broadband-light centroid.

The counterexample is decisive: unresolved spatial changes in [NII]/Hα can produce a 152 km/s apparent difference with zero motion. Opposite dispersions remove spatial ambiguity, not wavelength-blend ambiguity. The 225 exact synthetic centroid cases and the false-velocity construction are recorded in the spectral route.

The Gabarra paper's 252 km/s demonstration uses single-orientation blue-grism data at z≈0.696; its Hα is outside the red-grism wavelength range. It cannot immediately use the proposed opposite-red-grism Hα estimator. A different target with suitable red-grism wavelength and verified multi-orientation coverage is needed. This distinction prevents the illustrative speed being mistaken for a ready acceleration test. [Gabarra et al.](https://pubs.euclid-ec.org/public/dr1/gabarra.pdf).

## 5. What was already in the repository

The September dark-energy inverse work already contains acceleration–background inversion, distinguishes density and pressure portals, and identifies κ/√g_G rather than κ alone. AT1 already uses normalized redshift comparisons. Earlier rotation-curve work already explores shape estimators and their hidden bulge/M/L dependencies. Therefore the background relation and the general nuisance-cancellation idea are **not new discoveries here**.

The narrower contribution of this investigation is the explicit angular T reconstruction, its information/rank condition, the BAO-based joint measurement design, and the constructive gradient counterexample that specifies its failure mode. Broader literature novelty has not been established.

There is also a clean conditional way to compare the competing physical couplings already present in the repo. For the same independently constrained background, let S=[q(z)/q(z_r)]² and X=ρ_DE(z)/ρ_DE(z_r). Density coupling predicts S/X=1; negative-pressure coupling predicts w(z)/w(z_r); a realizable canonical-potential coupling predicts [1−w(z)]/[1−w(z_r)]. Constant amplitudes cancel, and **all three shapes coincide when w is constant**. The pressure branch requires negative w, and the canonical scalar cannot cross w=−1. This is a potential discriminator for evolving backgrounds, not evidence that such evolution has been measured. The background must be constrained independently or each hypothesis fitted as a separate joint forward model; imposing density tracking to construct X and then testing S/X=1 would be circular.

Likewise, the lensing route reproduces known deep-MOND virial content: under isolated spherical self-gravity, constant M/L, global dispersion and a no-slip metric, c²α/σ_global² tends to 9π. Changing to point-mass-dominated tracers gives 6π. It is a conditional structure/metric test, not a universal normalization test. A85 already pursues related lensing-to-dynamics consistency.

Double-source-plane candidates offer another known-method route: use DESI geometry to test lens-profile shape. Mass-sheet and multiple-plane effects remain; this does not make the 84 candidates independent measurements of a₀. See [the restricted derivation](route_double_source.md).

## 6. Theory implication and remaining work

The data suggest a useful separation: fit what the images and spectra measure, test the force-law shape within galaxies, then compare independently inferred accelerations with background geometry. A healthy theory must predict all three with the same action, couplings and boundary rules. None of the inspected completions has yet done that across the existing gates.

The actual-sampling preflight resolves part of the information question. The remaining load-bearing step is a full forward test with measured two-dimensional kinematics, gas/stellar covariance, geometry, PSF, external fields and the chosen physical disk solver. It must predict held-out resolved information and remain informative under observationally allowed gradients. Foundation's morphology helps supply this experiment; it does not supply all its measurements. The derivations, recorded predecessors and counterexamples specify what that next experiment must decide.
