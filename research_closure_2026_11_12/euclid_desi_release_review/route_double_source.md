# R4: two source planes as a shape test

Owner: root. Base checkpoint: 09b8dd7c6aad534bde13ade93b764607aae45b58. Status: conditional analytic reduction and explicit obstruction; not a new lensing method or a data fit.

## Target and inputs

Can the 84 double-source-plane candidates in [Lines et al.](https://pubs.euclid-ec.org/public/dr1/lines.pdf) test a deflection profile while cancelling its overall mass normalization? The release source is pinned in paper_inventory.json. Additional primary sources are [Collett et al. 2012](https://arxiv.org/abs/1203.2758), [Johnson et al., line-of-sight effects](https://arxiv.org/html/2501.17153v1), and the new [Johnson et al. 6 November 2026 paper](https://arxiv.org/html/2611.09856v1), sections 3–4. These are outside the 26-paper Foundation cohort and are not counted as Foundation manuscripts.

This route's calculations are symbolic. No actual ring radius, source redshift, mass normalization or predicted residual was extracted or fitted.

## Restricted derivation

Assume a circular main lens, two aligned sources with known redshifts, one effective lens plane, negligible mass in the first source, and a specified background geometry. Put f_i=D_ls,i/D_s,i. At the two tangential critical rings,

\[
\theta_i=f_i\widehat\alpha(\theta_i).
\]

For a power-law physical deflection \(\widehat\alpha=K\theta^{1-t}\), division gives

\[
\left(\frac{\theta_2}{\theta_1}\right)^t=\frac{f_2}{f_1},\qquad
t=\frac{\ln(f_2/f_1)}{\ln(\theta_2/\theta_1)}.
\]

K cancels exactly. Under the standard GR projection, a spherical three-dimensional power-law density with 1<γ<3 gives t=γ−1. A GR point mass instead has t=2; an isothermal deflection has t=1. An isolated deep-MOND point baryon source with a no-slip metric also tends to constant deflection and t=1. Thus the latter limit is shared with an isothermal dark-halo model; it does not identify Zimmerman or measure κ.

For a non-power-law deflection this same logarithmic expression measures a two-radius secant. The exact constraint is

\[
\frac{\widehat\alpha(\theta_2)}{\widehat\alpha(\theta_1)}
=\frac{\theta_2/\theta_1}{f_2/f_1}.
\]

Measured Sérsic shape plus a fixed force/deflection law can predict that ratio after a first-radius calibration. The second radius is then held-out shape information, provided it was not already used to determine the model. Near the transition, the overall stellar normalization changes profile shape too; cancellation of a multiplicative K does not eliminate all baryon uncertainty for a nonlinear gravity law.

## Counterexample and modern source check

A uniform projected contribution adds a term proportional to θ, so the deflection is Kθ^(1−t)+Sθ. Two rings no longer determine both t and S independently. A rescaling of source coordinates produces the familiar single-plane mass-sheet degeneracy. In multiple planes, source 1 can itself lens source 2; a geometry constraint alone does not remove all corresponding transformations.

Johnson et al. (November 2026), equations 19–23 and 35, explicitly retains these transformations. A prior on relative expansion constrains a combination of the two plane contributions, not both separately. Its reported relation is

\[
\zeta_{12}=\eta\zeta_1+\zeta_2-\zeta_1\zeta_2
=\frac{\widetilde\eta-\eta}{\widetilde\eta-1}.
\]

Here η is the physical, line-of-sight-dressed scaling factor: in the cited paper η=(1−κ_η)η_background. The background factor is f₂/f₁ and is what an external expansion likelihood constrains; a line-of-sight model is still required to obtain η. The tilded quantity belongs to a specified lens-model convention; the ζ parameters describe sheet-like deviations from that convention. Values inferred with different base profiles cannot simply be compared. Line-of-sight perturbations additionally affect the geometry and need not cancel between sources. These qualifications follow the cited sources; the simple ring-ratio derivation above is the restricted case rederived here.

Two ring radii alone determine a secant, not arbitrary curvature: adding a small deflection perturbation ε(θ−θ₁)(θ−θ₂)h(θ) leaves both ring conditions intact while changing the interior shape. Within a positive-density baseline on a finite interval, sufficiently small smooth perturbations can preserve positivity. Extra image information or explicit profile restrictions are necessary.

## What this changes

The useful Euclid–DESI connection is to use an external relative-expansion likelihood to constrain lens-profile shape within a specified profile-plus-sheet family or with additional extended-image information, rather than extract cosmology from an imposed isothermal profile and then use that same cosmology to confirm the profile. This can confront the existing CFG712 shape tension and its radial dependence, but it requires flexible image fits, both source redshifts, first-source mass and line-of-sight treatment. The SIE catalogue alone cannot perform it.

Prior overlap: the repository already studies J0946 lens perturbers (CFG671/667) and outer photon-deflection shape (E13). The restricted targeted search found no exact same ring-ratio phrase in those selected directories, which is not evidence of novelty. The external literature establishes that double-source-plane geometry and mass-sheet tests are known.

Continuation is open: identify confirmed multi-source candidates and available redshift/image products, then forecast whether their radial leverage distinguishes the chosen fixed gravity model from its controlled comparator. We have not certified the 84 candidates as 84 usable systems. This route does not evade the missing metric completion or establish an all-gate theory pass.
