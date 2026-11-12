# Redshift route: a mass-normalization-free acceleration–distance observable

2026-11-12. Bounded derivation and synthetic checks, using the computation-audit workflow. No Euclid data, residual or model fit was used. No repository files were changed. This is an observable construction under specified gravity/baryon assumptions, not a new action or a claim that the theory passes its other gates.

**Result.** A resolved light profile plus a resolved circular-velocity curve can, under a one-template baryon model, identify **T = D_A a0 while exactly eliminating a galaxy’s unknown global stellar mass-to-light normalization**. Dividing two such T values by the corresponding dimensionless BAO angular distances also removes the common sound-horizon/distance scale. This gives a conditional test of the dark-energy linkage rather than a new measurement of kappa. It requires information across the transition; a deep-MOND-only sample cannot do it. Inclination, radial mass-to-light gradients, unmeasured gas geometry and the field equation remain material constraints.

## 1. Inputs and what changes relative to existing lanes

The current scale hypothesis is

\[
a_0(z)=\kappa c\sqrt{G\rho_{\rm DE}(z)}.
\]

It does **not** say a0 is proportional to H(z). Its ratio prediction is independent of kappa and the canonical/alternate local footing. Existing AT1 already takes a same-estimator redshift ratio but retains non-cancelling population IMF, gas and pressure-support modes, with required common mode below 0.055–0.084 dex. [AT1 README:7–29](/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/AT1_a0z_tracking_decision/README.md:7). The construction below profiles a separate **global** stellar normalization for every galaxy instead of requiring that normalization to transfer between epochs.

The repository already has a distance-immune shape estimator, with fixed/scanned disc and bulge M/L. Its own audit says the apparent disc-M/L cancellation merely relocates uncertainty into bulge M/L. [Earlier estimator:11–32](/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews/mi_distance_free_gbar_estimator_sparc_2026.py:11), [current implementation:208–246](/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/paper_numbers.py:208). Thus shape-based nuisance separation is prior art here. The narrower candidate contribution is the explicit T = D_A a0 reconstruction and its **BAO-corrected redshift ratio**; no universal novelty claim is made. A bounded targeted prior-art search is recorded in `route_redshift_prior_art_hits.txt`.

## 2. What the angular light template means

Let D = D_A(z), theta be an angular radius in radians, and let

\[
w(\theta)=v_c^2(\theta)/\theta,
\qquad g(\theta)=w(\theta)/D.
\]

Both w and T have dimensions of velocity squared. v_c must be an independently inferred circular speed, with pressure support/non-circular motion handled; it is not a velocity inferred by assuming the gravity law.

Choose an arbitrary **reference** stellar mass-to-light ratio Upsilon_ref and deproject the observed light using specified geometry. Let b(theta) be the Newtonian acceleration of that reference mass model. Write the actual baryon acceleration as

\[
g_b(\theta)=U\,b(\theta),\qquad U=\Upsilon/\Upsilon_{\rm ref}>0.
\]

Here U is dimensionless and b has acceleration units. For a fixed angular shape b is independent of the unknown absolute distance: luminosity-derived mass scales as D_L squared and squared physical radius as D_A squared. With distance duality, the rest-frame surface luminosity density is

\[
\Sigma_L(\theta)=4\pi(1+z)^4 K(z,\theta)\,I_{\rm obs}(\theta).
\]

K is defined here as the multiplicative band/SED correction into a common rest-frame luminosity convention; it is one for bolometric flux. Multiplication by Upsilon_ref gives a reference mass surface density. This explicitly assumes photon conservation/distance duality and consistent dust/SED/deprojection treatment. A single global photometric or K-correction factor can be absorbed into U and will cancel below; a **radially varying** K correction changes b’s shape and does not cancel. For discs, the deprojection depends on inclination and thickness.

The immediate algebra below is exact for the specified **pointwise algebraic law**, including its spherical realization. For a general nonspherical AQUAL disc, pointwise g = nu g_b need not hold; Section 7 gives the corresponding scale covariance without making that identification.

## 3. Exact two-radius elimination of global M/L

Define A = D U and T = D a0.

### Simple-mu law

For g_b = g squared / (g + a0),

\[
w_i^2=A b_i(w_i+T),\qquad
p_i\equiv w_i^2/b_i=A w_i+B,\qquad B=A T.
\]

At two distinct w values,

\[
A=\frac{p_2-p_1}{w_2-w_1},\qquad
B=p_1-Aw_1,\qquad
\boxed{T=B/A}.
\]

Require A > 0 and B > 0. In exact data this is an identity; real data need a full forward likelihood, not a least-squares line in transformed variables.

### Quadratic a0-line

For g squared = g_b squared + a0 g_b,

\[
p_i=C b_i+E,\qquad C=A^2,\quad E=A T.
\]

At two distinct b values,

\[
C=\frac{p_2-p_1}{b_2-b_1},\qquad
E=\frac{b_2p_1-b_1p_2}{b_2-b_1},\qquad
\boxed{T=E/\sqrt C}.
\]

Require C > 0 and E > 0. C has dimensions of length squared and E has dimensions of length times velocity squared, giving the correct dimension for T.

Under a global light recalibration b -> k b, simple-mu A and B both scale as 1/k. In the quadratic form C -> C/k squared and E -> E/k. **T is unchanged in both cases.** This holds independently for each galaxy, so global M/L evolution between samples need not cancel statistically: its normalization has already been removed algebraically.

Two radii identify two parameters but cannot test the law. Three or more resolved radii provide an overdetermined shape test and a held-out radius can reject the specified law/template. A positive fitted T alone is not a pass.

## 4. Exact information condition and why transition radii matter

Let t_i be the response of log w_i to log T at fixed A. The other response is 1 - t_i:

\[
t_i=\frac{1}{w_i/T+2}\quad\hbox{(simple-mu)},
\qquad
t_i=\frac{1}{2(1+g_{b,i}/a_0)}\quad\hbox{(quadratic)}.
\]

For independent log-w errors with weights omega_i, the two-parameter Fisher determinant is

\[
\boxed{\det F=\sum_{i<j}\omega_i\omega_j(t_i-t_j)^2}.
\]

Thus at least two radii with different responses are necessary for local identification. In the exact deep limit all t = 1/2: only A T is measured. In the exact Newtonian limit all t = 0: T disappears. With finite but extreme accelerations identification is formally possible and numerically ill-conditioned. This is the missing qualification in a claim that an arbitrary BTFR sample could remove M/L.

An idealized calculation with three exact b values, independent **1% errors in w**, no nuisance geometry, and g_b/a0 = 0.1, 1, 10 gives marginalized sigma(log T) = 0.0309 (simple-mu) or 0.0266 (quadratic), in natural logarithms. The corresponding deep and Newtonian windows are orders of magnitude worse. These numbers establish sensitivity of this toy model only; they are **not** an achieved error or survey forecast. One percent in w corresponds to about 0.5% in v.

Errors in w enter both axes of the proposed transformed line and errors in b enter both axes in the quadratic version. Covariance, PSF, inclination and the nonlinear transform forbid naive ordinary least squares on real measurements. Fit the original w_i model with nuisance templates and compare its information matrix to a frozen threshold.

## 5. The BAO-corrected ratio and a test of the portal itself

Use two finite redshifts with independent galaxy samples. Define the measured dimensionless BAO angular distance

\[
d_A(z)=\frac{D_M(z)/r_d}{1+z}=D_A(z)/r_d.
\]

Then

\[
\boxed{\mathcal Q(z,z_r)=\frac{T(z)}{T(z_r)}\frac{d_A(z_r)}{d_A(z)}
=\frac{a_0(z)}{a_0(z_r)}}.
\]

The same r_d cancels exactly; absolute distance calibration cancels; kappa cancels; global M/L cancels separately within each galaxy. The redshift hypothesis is

\[
\boxed{\mathcal N=\mathcal Q^2\big/\big[\rho_{\rm DE}(z)/\rho_{\rm DE}(z_r)\big]=1}.
\]

Constant Lambda predicts Q = 1; density tracking predicts Q = sqrt(X); H-tracking predicts Q = H(z)/H(z_r), which is generally different. This does **not** determine the special coefficient kappa = 1/2, and generic galaxy/halo models can be tested only after specifying their own predicted Q distribution.

One must not call the denominator rho_DE model independent. BAO constrains distances divided by a ruler; density extraction adds matter/radiation, curvature, gravity and conservation assumptions. CFG689 explicitly imports early physical-density priors and CAMB’s ruler to break that degeneracy. [CFG689 criteria:10–34](/Users/carlzimmerman/new_physics/zimmerman-formula/campaign_fresh_gravity/CFG689_native_ruler_bao/FROZEN_CRITERIA.md:10). A joint likelihood must propagate correlations between d_A and the inferred density ratio. A local reference at z = 0 cannot be inserted into this formula because D_A(0) = 0; use finite BAO-supported redshift bins or a separately justified distance interpolation.

This statistic also separates the two portals in CT7 rather than conflating them. For a canonical scalar, V = (1-w_DE) rho_DE / 2. A potential portal a0 squared proportional to V predicts

\[
\mathcal N_{V}=\frac{1-w_{\rm DE}(z)}{1-w_{\rm DE}(z_r)},
\]

whereas the requested energy-density portal predicts N = 1. These coincide only when w is constant. CT7 already found that its healthy potential portal fails the exact rho_DE tie, while its energy portal becomes unhealthy in high-acceleration regions. [CT7:30–48](/Users/carlzimmerman/new_physics/zimmerman-formula/complete_theory_2026_11_04/CT7_candidate_C/CT7_REPORT.md:30). The ratio is a way to **test** a portal; it supplies no repair of that health problem.

For source distance conventions and public dimensionless BAO measurements, see the official [DESI likelihood documentation](https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/README.html). No external numerical measurement is used in the synthetic checks.

## 6. Adversarial nuisance tests: what does not cancel

**Inclination / velocity normalization.** If inferred w is multiplied by lambda, both estimators return T multiplied by lambda. A rotation velocity derived as v_los / sin i therefore gives a T bias proportional to sin squared i_true / sin squared i_used, holding the light geometry fixed. A true 55-degree disc modeled at 60 degrees shifts log10 T by **-0.04833 dex**. This alone can be comparable to AT1’s common-mode budget. Light deprojection also changes with inclination, adding a separate correlated effect. Only an identical multiplicative velocity calibration in both redshift samples cancels in Q; unrelated inclinations do not.

**Radial IMF, population gradients or unseen gas: an exact obstruction.** Set a spherical circular-speed curve to v_c = V at every radius. For every a > 0, the simple-mu law is exactly reproduced by

\[
M_b^{(a)}(<r)=\frac{V^4 r}{G(V^2+a r)},\qquad
\frac{dM_b^{(a)}}{dr}=\frac{V^6}{G(V^2+a r)^2}>0.
\]

These are physically nonnegative spherical densities, all giving the **same** rotation curve with different a0. If the observed luminosity density is proportional to the density for a_old, the alternative a_new is realized by the positive local mass-to-light profile

\[
\frac{\Upsilon_{\rm new}(r)}{\Upsilon_{\rm old}}=
\left[\frac{V^2+a_{\rm old}r}{V^2+a_{\rm new}r}\right]^2.
\]

For V squared = a_old = 1 and radii 1–8 in the corresponding units, changing a0 to 0.91 needs only **0.03243 dex of radial M/L variation across the window**, apart from its free overall amplitude. Changing a0 by a factor two needs 0.20023 dex. This is a constructive counterexample to any claim that light plus circular speeds yield a baryon-free redshift test when arbitrary radial M/L is allowed. Finite central structure can replace the idealized flat-curve cusp outside the measured radial interval; the counterexample concerns the specified interval, not formation plausibility.

Unknown gas has the same logical role if its radial profile is unconstrained. If a gas map supplies a known shape with an unknown **global** conversion coefficient, one need not assume its amplitude: in the simple-mu case several known templates b_k give

\[
w_i^2=\sum_k A_k b_{ki}w_i+\sum_k C_k b_{ki},\qquad C_k=T A_k.
\]

A full-rank multi-template fit can profile amplitudes and test the common ratio C_k/A_k = T. It requires enough radii and independent template information. This is not a cancellation of an unmeasured gas distribution; arbitrary added radial structure restores the counterexample.

## 7. General AQUAL scale covariance, without a disk shortcut

For the specified AQUAL equation in physical coordinates,

\[
\nabla_x\cdot\{\mu(|\nabla_x\Phi|/a_0)\nabla_x\Phi\}=4\pi G\rho,
\]

write x = D theta and rho = U j_tilde(theta)/D, where j_tilde is the distance-independent angular deprojection of the reference surface mass density. Multiplication by D squared gives

\[
\nabla_\theta\cdot\{\mu(|\nabla_\theta\Phi|/T)\nabla_\theta\Phi\}
=4\pi G A\,j_{\rm tilde}(\theta).
\]

The angular problem depends on A = D U and T = D a0, with Phi measured in velocity-squared units. Therefore the same parameter separation and BAO-ratio idea can be posed for an actual disc solver. The **linear two-radius identities and toy Fisher numbers are not inherited** by that solver. Boundary/external-field parameters must be included; a fixed external acceleration gives angular boundary gradient D g_ext. Jeans observables introduce anisotropy parameters. Establishing identification in the real morphology/kinematics model is the first uncomputed implication.

## 8. A concrete next discriminating calculation

Freeze the interpolation/field equation and baryon-template class. For one isolated, bulgeless development galaxy with independent resolved kinematics and gas information, use the measured light shape to fit A and T in the original observable space. Hold out at least one radial annulus and require that it predicts that annulus. Independently vary radial M/L, gas-map shape, inclination and external-field boundary over observational priors. Stop if the T direction becomes unidentifiable or if nuisance variations exceed the redshift separation. Only after that should one assemble independent finite-redshift samples and score Q against the DESI density-ratio band.

Euclid morphologies could improve the angular template, inclination/thickness and resolved colour-gradient constraints that this calculation actually needs. Images alone do not supply independent circular velocities or gas maps. This route moves the binding question from shared **global** M/L evolution to a testable within-galaxy **shape and information** requirement. It neither eliminates those remaining nuisances nor produces a healthy completion.

## 9. Computation and provenance

- `route_redshift_check.py`: exact SymPy polynomial identities, Fisher determinant, positive-density counterexample derivative; 54 deterministic synthetic cases covering two laws and 3 x 3 x 3 positive D/U/a0 values. Maximum relative T recovery error 5.55e-16. Independent finite-difference responses check the information derivatives.
- `route_redshift_contract.json` specifies the tested assertions, domain and non-claims. `route_redshift_run02/results.json` contains the numbers above. No random sampling, astronomical fit or survey covariance was used.
- `route_redshift_run02/manifest.json` has **run.status = completed**; the installed manifest validator passed against the temporary project root. It hashes the script and repository-input provenance file before/after, and hashes outputs. First run is retained as failed: a NumPy-boolean JSON serialization error prevented output, and the case-count label was corrected from an incorrectly stated 108 to the actual 54 before the completed run. No mathematical conclusion is taken from the failed run.
- Requested repository base: `09b8dd7c6aad534bde13ade93b764607aae45b58`. Observed HEAD when inputs were recorded: `2ffc012fa56dcdcbb4b3d5f169ba757fe482bcb8`; worktree already dirty from unrelated ongoing work. The script does not import repository execution code.
- Full hashes of the four scoped repository inputs are in `route_redshift_repository_inputs.json`; the report’s source snapshot is those hashed contents, not an assertion that the moving whole worktree equals the requested base.
- Self-review of this report covered mathematical notation, dimensions, equations and source links. No additional mathematical-token correction was required after the checks. The finite synthetic verification supports these identities and examples; it is not verification of an astronomical prediction or a universal theory.

## 10. Root extension: a joint coefficient test without an early-Universe ruler prior

The root agent proposed extending T to a joint background equation. This is correct under the following additional assumptions: a Friedmann background with constant cosmological coupling G_cosm = g_G G_N; separately conserved matter proportional to (1+z) cubed and radiation proportional to (1+z) to the fourth power; ordinary curvature; and the **density** promotion, not the pressure or potential promotion.

Define directly in observed angular/velocity and dimensionless-BAO variables

\[
d_M=D_M/r_d,\qquad d_H=D_H/r_d,\qquad
h=d_H^{-1}=Hr_d/c,
\]
\[
\boxed{q_a(z)=\frac{T(z)(1+z)}{c^2d_M(z)}
=\frac{a_0(z)r_d}{c^2}}.
\]

q_a is dimensionless. It uses the independently reconstructed T; it does not use a Friedmann-inferred dark-energy density. Substituting the density linkage into Friedmann gives

\[
\boxed{h(z)^2=A_m(1+z)^3+A_r(1+z)^4+K(1+z)^2+C_a q_a(z)^2},
\]
\[
A_m=\frac{8\pi G_{\rm cosm}\rho_{m0}r_d^2}{3c^2},\quad
A_r=\frac{8\pi G_{\rm cosm}\rho_{r0}r_d^2}{3c^2},\quad
\boxed{C_a=\frac{8\pi g_G}{3\kappa^2}}.
\]

Here K = -k_geom r_d squared, with the scale factor normalized to one today. For universal Newton coupling g_G = 1 and kappa = 1/2, the specified coefficient is C_a = 32 pi / 3. A free coefficient measures **kappa / sqrt(g_G)**. It measures kappa alone only after fixing g_G independently. The old inverse-scale audit explicitly identified this coupling degeneracy. [scales/REPORT:30–46](/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/dark_energy_inverse_2026_09_26/scales/REPORT.md:30).

**Why this is not tautological.** First fit each galaxy’s T with no imposed density ratio or kappa. Then measure h, d_M from BAO. Across redshift these supply independent observable functions; a single C_a must work after fitting only the fixed matter/radiation/curvature basis. It is an overdetermined statement when more than four independent redshift nodes exist, or fewer nuisance coefficients are independently constrained. Constructing T by substituting a DESI-inferred a0, imposing a common a0 history in the galaxy fit, or defining the matter term separately at every redshift would instead make it tautological.

**Exact identifiability condition.** With curvature and radiation both free, the four columns

\[
(1+z)^3,\ (1+z)^4,\ (1+z)^2,\ q_a(z)^2
\]

must have full rank over the selected bins. If q_a squared lies in the span of the first three, changing C_a can be absorbed into A_m, A_r and K. For example q_a squared proportional to (1+z) cubed is exactly degenerate with conserved matter. Constant q_a adds a constant column and, at four distinct positive redshifts, is independent of the three distinct positive powers: a nonzero polynomial with those four monomials cannot have four distinct positive roots (equivalently the corresponding generalized Vandermonde is nonsingular). Near-collinearity and real correlated errors can still destroy practical precision. Four freely fitted coefficients at four nodes provide identification but no unconstrained goodness-of-fit degrees of freedom; more nodes, positivity constraints or a specified kappa are required to test the family.

Curvature can also be tested geometrically with the **same** K:

\[
\boxed{[h(z)d_M'(z)]^2=1+K d_M(z)^2}.
\]

This follows from the derivative of the transverse comoving distance in a Friedmann geometry. Derivative estimation and its covariance must be handled in the joint distance likelihood; it is not a new noise-free curvature datum.

**What this changes about CFG689.** It adds the independent galactic observable that CFG681 lacked and can, in principle, identify the background decomposition without importing an absolute r_d, H0 or early Planck physical-density prior. That is a meaningful change of identifiability. It does **not** make the density extraction gravity independent: it replaces those priors with an independently tested galactic scale, a specified gravity law, a specified Friedmann background, constant coupling ratio and separately conserved components. A global velocity-squared calibration error lambda makes q_a -> lambda q_a and C_a -> C_a/lambda squared; hence inferred kappa/sqrt(g_G) scales by lambda. Inclination and radial-template obstructions in Section 6 remain.

**Nearest prior art, so this should not be called a new Friedmann relation.** The September reconstruction audit already derived an inverse **pressure** test, showed its conserved-dust integration ambiguity, and obtained H squared = B a0 squared / 3 + D_H a^-3 for constant a0. [reconstruction/RESULT:109–150](/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/dark_energy_inverse_2026_09_26/reconstruction/RESULT.md:109). It explicitly distinguishes pressure and density promotions at lines 9–24. The new part under consideration is the route from angular morphology and independent velocities to T, and hence the observable q_a combined with compressed BAO, rather than those previously recorded cosmological identities. The root’s independent audit is responsible for any additional finite rank calculations; none is claimed as run in this route’s manifest.

This extension is a **surviving conditional joint test**, not a present kappa measurement or healthy-action construction. Its first discriminating calculation is to show on independently measured morphology/kinematics that T is identifiable under radial M/L, gas, inclination and external-field priors. Without that result the additional observable is a formal input, and CFG689’s observational obstacle remains.

## 11. Density, pressure and canonical-potential portals: an exact shape discriminant

Take the **same** positive dark-energy density history rho_X(z), separately conserved, with w(z) = p_X / (rho_X c squared), and constant positive but independently chosen normalization coefficients for each portal. Define S(z) = [q_a(z)/q_a(z_r)] squared and X(z) = rho_X(z)/rho_X(z_r). Then

| Portal | Scale squared | Exact normalized prediction S |
|---|---|---|
| Density | constant times rho_X c squared | X |
| Negative pressure | constant times -p_X | X w(z)/w(z_r) |
| Canonical scalar potential | constant times V, V = (1-w)rho_X c squared / 2 | X [1-w(z)]/[1-w(z_r)] |

The pressure branch requires w(z) < 0 and w(z_r) < 0 for a positive nonzero scale. The potential identity assumes a canonical scalar and V > 0; that member cannot cross w = -1. The mathematical pressure/density hypotheses themselves do not establish a healthy scalar realization. No phantom crossing is asserted here.

The amplitude coefficients, kappa, constant G_cosm/G_N and common r_d cancel in these normalized shapes. Consequently the directly inferred **portal quotient** S/X is predicted to be, respectively,

\[
\boxed{1,\qquad \frac{w(z)}{w(z_r)},\qquad
\frac{1-w(z)}{1-w(z_r)}}.
\]

All three are exactly degenerate after normalization when w is constant. At any pair of epochs with different w, they are distinct in their common physical domain: equality of w/w_r and (1-w)/(1-w_r) implies w = w_r. For measurements at only a few epochs, the statement concerns those sampled values, not all behavior between them. Uncertainty in the independently inferred background w and X must be propagated; arbitrary model-specific matter histories would remove the shared-background comparison.

Near w = -1, write w = -1 + delta. To first order, pressure gives S/X = 1 - (delta-delta_r), while the canonical-potential portal gives 1 - (delta-delta_r)/2. In q itself the relative shifts are half these values. Thus density versus pressure is twice as sensitive to a small change in w as density versus potential. The familiar exact-Lambda coincidence is a real degeneracy, not a failed observational design.

To preserve the old inverse-pressure result, let t = 1+z, F = h squared and

\[
E=F-A_m t^3-A_r t^4-Kt^2.
\]

With L = t d/dt, define P = E - L E / 3 and V_b = E - L E / 6. These are proportional to -p_X and the canonical V with a shared positive conversion factor. Then

\[
S_\rho=E/E_r,\qquad S_p=P/P_r,\qquad S_V=V_b/V_{b,r}.
\]

In particular

\[
3P=3F-LF+A_r t^4-Kt^2,
\]

so conserved matter cancels **exactly**, just as in the September inverse-pressure rule. In contrast

\[
V_b=F-LF/6-A_m t^3/2-A_r t^4/3-2Kt^2/3
\]

still depends on the matter subtraction. These are different background operators; one must not reuse the pressure null to claim a density tie. The independently reconstructed q_a lets the existing inverse-pressure null become an actual cross-observable test once its galaxy information gate is met. That is a cleaner member-to-member discrimination than claiming a present precise measurement of kappa.

### Non-circular portal comparison in the directly observed background

One must not infer X by imposing the density-q_a closure and then retest S/X = 1. Use a separately constrained shared background, or fit the three **different forward joint models** with the same matter/curvature/radiation priors and likelihood.

In the flat, late-time matter-plus-X limit, put u = 1+z, F = h squared, and C = 8 pi g_G / (3 kappa squared), with each portal’s coefficient matched to the same vacuum convention. Their equations are

\[
\begin{array}{ll}
\text{density:}&C q_a^2=F-A_m u^3,\\
\text{negative pressure:}&C q_a^2=F-uF'/3,\\
\text{canonical potential:}&C q_a^2=F-uF'/6-A_m u^3/2.
\end{array}
\]

They use independent q_a, do not first reconstruct X using the portal being tested, and permit one constant C to be profiled per hypothesis. The pressure operator and its dust cancellation are the September prior result, not new discoveries. The potential formula assumes the canonical member is physically realizable. Derivative covariance, freedom in A_m and the q_a information gate determine whether these distinct equations are actually distinguishable in data.

## 12. Real development-data identifiability preflight

The smallest next calculation was executable from existing repository inputs. Three named old SPARC galaxies were selected by available resolved rotation, separate disk/gas templates, zero bulge and documented inclination, **before computing this preflight’s information values**: NGC2403, NGC3198 and DDO154. The selection was not blind: catalogue availability and the files were inspected, and these are familiar development data, not held-out Euclid observations. No galaxy, radius or kernel was selected by a gravity-law residual or the information outcome.

Inputs are immutable temporary copies of SPARC Table 1 and the three rotation/mass-model tables; their original paths and SHA-256 values are in `route_redshift_sparc_selection.json`. The repository’s data audit identifies the authentic `.mrt` and rotation files and warns that a differently named `SPARC_table.txt` is only an old 404 page; that file was not used. [SPARC input audit](/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/SPARC_table.README.md:1).

| Development galaxy | Valid radii | Angular span, arcsec | Fiducial g_b/a0 span | Catalogue inclination |
|---|---:|---:|---:|---:|
| NGC2403 | 73 | 10.4–1362 | 0.0439–1.261 | 63 +/- 3 degrees |
| NGC3198 | 43 | 4.78–659 | 0.0329–2.166 | 73 +/- 3 degrees |
| DDO154 | 12 | 25.0–302 | 0.0155–0.0634 | 64 +/- 3 degrees |

All rows with positive radius, measured speed and speed error were retained; signed gas-force convention was respected. This is a **local Fisher calculation** at Upsilon = 0.5 in the tabulated disk units and a0 = 9.3603e-11 m/s squared, for both algebraic laws. The observed velocities provide the quoted fractional error weights; no measured law residual is fitted or graded. The radial stellar and gas force templates come separately from the mass-model table. Angular radii are reconstructed with the catalogue distance only to express the existing development setup.

Nuisance parameters are free stellar amplitude, free gas amplitude, log T, a radial stellar mass-to-light source slope gamma, and inclination offset. The radial gradient is a source perturbation Sigma_star(R) proportional to (R/R_d) to the gamma power, propagated through a softened disk-ring gravity integral, not a pointwise radial rescaling of the force. Its baseline force amplitude is calibrated to the published disk template; the derivative shape is the physical ring calculation with softening h = 0.1 R_d. This is a local nuisance-response model, not an exact reconstruction of each galaxy’s vertical structure or an AQUAL disc solve.

The table reports sigma(log10 T), in dex:

| Galaxy | Kernel | Angular gas amplitude and geometry fixed: optimistic control | Gas amplitude free, catalogue inclination prior, gradient fixed | Gas amplitude free, catalogue inclination prior, dimensionless gradient sigma_gamma = 0.1 |
|---|---|---:|---:|---:|
| NGC2403 | simple-mu | 0.00499 | 0.0451 | **0.0800** |
| NGC2403 | quadratic | 0.00418 | 0.0347 | **0.0557** |
| NGC3198 | simple-mu | 0.0129 | 0.1149 | **0.1405** |
| NGC3198 | quadratic | 0.0110 | 0.0708 | **0.0857** |
| DDO154 | simple-mu | 0.00899 | 0.3904 | **0.3916** |
| DDO154 | quadratic | 0.00852 | 0.5986 | **0.6001** |

The gradient prior 0.1 means 0.1 dex of M/L change per radial decade. It is a **sensitivity bracket**, not measured information about these galaxies. The run also records gradient priors 0.3 and no gradient prior, and gas-free/fixed-inclination cases. With inclination completely free, every galaxy/kernel has the exact rank deficiency predicted analytically: scaling both baryon amplitudes and T multiplies w uniformly and can be absorbed into inclination. All six five-parameter information matrices have rank four. Catalogue inclination information is therefore doing real work; the nominally excellent fixed-nuisance errors are not a cancellation of that uncertainty.

**Interpretation.** At the actual radial sampling and quoted errors, transition-spanning galaxies can conditionally identify T after global stellar and gas amplitudes are profiled. A deep gas-dominated curve such as DDO154 cannot supply a useful amplitude-independent T in this preflight; its small fixed-gas error mostly reflects the imposed gas scale. NGC2403’s more useful information requires the observed transition profile and inclination/template controls. This is a concrete filter for the proposed measurement, not evidence for the gravity law or a precision forecast for a high-redshift sample.

**Limits.** Velocity errors were treated as diagonal. No measured stellar/gas-map covariance, inclination-induced change of light deprojection, distance/systemic correlations, pressure correction uncertainty, external field or noncircular motions were propagated. The disk-gradient response was checked by doubling the radial/azimuthal quadratures from 1024/256 to 2048/512; its maximum absolute derivative change was 0.00581, 0.00894 and 0.000163 for the three galaxies. No outcome-dependent convergence threshold was invented; these differences and the softened-disk approximation remain disclosed. The full AQUAL-disc identification question is still uncomputed.

**Reproducibility.** `route_redshift_sparc_preflight.py` and `route_redshift_sparc_contract.json` generate 42 scenarios (3 galaxies x 2 kernels x 7 nuisance treatments). The bounded runner wrote `route_redshift_sparc_run01/results.json` and a **completed** `manifest.json`; the installed validator passed against the temporary project root. Exact checks also verify the pressure dust cancellation, potential operator and portal equality condition in Section 11. No external downloads or repository writes were performed. The per-galaxy results are old-data design evidence only.

### Publication clarification: angular gas normalization and gradient units

The small 0.004–0.013 dex control errors above fix the **angular gas amplitude** A_gas = D_A times the gas conversion normalization, together with geometry/inclination and gradient. Knowing the gas conversion coefficient alone does not fix A_gas when D_A is unknown. These control errors must therefore be described as a **fixed-angular-gas, fixed-geometry optimistic control**, not as precision available from measuring the gas conversion factor. The reported free-gas-amplitude rows profile A_gas and retain their stated conditional interpretation. This clarifies the control label; it changes no computation.

The source-gradient parameter gamma is a **dimensionless power** defined by ln Upsilon(R) = constant + gamma ln(R/R_d). Its sensitivity-prior widths 0.1 and 0.3 are dimensionless widths in gamma, not dex errors in a global mass-to-light normalization. Equivalently, gamma = 0.1 gives 0.1 dex of M/L change across one dex in radius. The sigma(log10 T) outputs, in contrast, are reported in dex. These are sensitivity brackets, not measured radial-population priors.

The validated scripts, selection, contracts, results and manifests remain unchanged. This clarification affects the written interpretation only.

## 13. Final bounded continuation: nonlinear gradient injection with held-out kinematic annuli

NGC2403 was chosen **after** the information preflight because it supplied informative development coverage. This is explicitly not a blind target choice or a held-out science result. Before this continuation’s fits, `route_redshift_injection_selection_v2.json` froze two kernels, source-gradient injections gamma = -0.1, 0, +0.1, bounds, priors, three starting points per fit, and the velocity holdout mask.

The holdout consists of zero-based sorted valid indices 12–17 and 44–49: radii **1.36–1.87 kpc and 6.96–9.44 kpc**, twelve points total. The other 61 velocity points train the inverse. The full measured light/gas templates remain conditioning inputs, including their values at the held-out radii; this withholds **kinematic annuli**, not photometry or whole images.

Truth is generated by directly reweighting the disk surface density by (R/R_d) to the injected gamma power and integrating the softened disk rings. The inverse uses the same declared source-response family and either the simple-mu or quadratic algebraic prescription. Both fitted models free the global stellar amplitude, the **angular** gas amplitude and T, and profile inclination with the same 63 +/- 3 degree prior. One model fixes gamma = 0; the other profiles gamma with dimensionless Gaussian prior 0 +/- 0.1. This tests whether the nonlinear inverse follows the local information direction; it does not validate that family against a real galaxy’s velocity residuals.

The injected velocity means are noiseless. Actual SPARC velocity errors weight training and prediction. Residual powers below are squared deviations in those error units. For held-out prediction, parameter uncertainty is propagated from the train-only local posterior curvature into

\[
C_{\rm pred}=C_{V,\rm hold}+J_{\rm hold}\,C_{\theta,\rm train}\,J_{\rm hold}^{T},
\qquad \lambda_{\rm hold}=r_{\rm hold}^{T}C_{\rm pred}^{-1}r_{\rm hold}.
\]

This covariance is a local Gaussian approximation, not calibrated nonlinear coverage. The frozen marker lambda_hold >= 9 was only an optimistic separation marker, not an observed chi-square rejection rule.

| Kernel | Injected gamma | Fitted gradient | log10(T_fit/T_true), dex | gamma_fit | Held-out predictive residual power |
|---|---:|---|---:|---:|---:|
| simple-mu | -0.1 | fixed zero | **-0.4221** | 0 | 3.391 |
| simple-mu | -0.1 | profiled | -0.0199 | -0.09547 | 0.0096 |
| simple-mu | +0.1 | fixed zero | **+0.6338** | 0 | 7.716 |
| simple-mu | +0.1 | profiled | +0.0130 | +0.09769 | 0.0037 |
| quadratic | -0.1 | fixed zero | **-0.3047** | 0 | 3.398 |
| quadratic | -0.1 | profiled | -0.0150 | -0.09519 | 0.0121 |
| quadratic | +0.1 | fixed zero | **+0.3647** | 0 | 6.811 |
| quadratic | +0.1 | profiled | +0.0109 | +0.09722 | 0.0057 |

The gamma = 0 injections recover T without bias and predict the holdouts to numerical precision for both models and kernels. The nonzero injections show two distinct conclusions:

1. **The conditional nonlinear inverse works:** profiling the physical source-gradient response recovers gamma near its injected value and T within approximately -0.020 to +0.013 dex. Its remaining small bias follows shrinkage toward the specified zero-gradient prior. This supports the numerical identifiability construction inside this model family; it is not an independent test of the family.
2. **The radial holdouts alone do not make the bias safe:** fixing a small nonzero gradient to zero biases T by 0.30–0.63 dex, while maximum held-out velocity errors are only 1.1–1.7%. After train-parameter uncertainty is propagated, all four misspecified held-out powers remain **below** the frozen marker 9. Raw fixed-parameter holdout power can exceed that marker, illustrating why predictive uncertainty cannot be dropped. Training data residual powers are 21.4–43.8 in the fixed-gradient model, versus 0.023–0.045 after profiling the gradient, but these noiseless-injection contrasts are not observations or calibrated detection significances.

Inclination stays at its prior center because this data model retains the exact amplitude/inclination degeneracy. No nonzero inclination-offset injection was made, so recovery here is not evidence that the catalogue inclination is correct. The fixed photometric deprojection also does not respond to fitted inclination. Global stellar/gas amplitudes absorb substantial changes in the misspecified model; none of the twelve best fits hits its parameter bounds.

All three predeclared starts agree in objective within 8.1e-12. A direct ring evaluation at the fitted gamma differs from the interpolation used by the optimizer by at most 4.9e-7 of a quoted velocity error. The twelve cases use 36 optimizer starts total. These checks address numerical inversion, not the missing correlated PSF, velocity, gas-template, dust/population or field-equation errors.

**Reproducibility and first-launch correction.** `route_redshift_injection_v2.py`, `route_redshift_injection_contract_v2.json` and `route_redshift_injection_selection_v2.json` produced `route_redshift_injection_run02/results.json` with **completed** manifest, validated against the temporary project root. The first launch stopped **before any fit** because its assertion required decreasing final tabulated surface brightness, whereas the last two positive values were equal after rounding. The second launch restored the already used preflight convention: if the final two-bin logarithmic tail slope is nonnegative, use -1/R_d. The earlier failed source/contract/selection and run are preserved; no fitted outcome informed this correction.

**Checkpoint reached.** The next substantive check needs actual two-dimensional kinematics and correlated geometry/PSF, independently constrained radial stellar populations, measured gas morphology/conversion and a specified nonspherical gravity solver. Further mock variations inside the same shared truth/inverse family would not establish those inputs. Stop here rather than promote this internal recovery into a new observational pass.
