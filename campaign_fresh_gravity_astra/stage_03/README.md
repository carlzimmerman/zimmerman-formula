# Precision checkpoint: what closes, and what remains open

2026-09-27. Three independent agent assignments and a coordinator inference
calculation are complete. **The conditional mathematical results below are
established to the stated scope; the physical theory is not closed.**
No new empirical fit establishes agreement with all observations.

This campaign derives forward from the user's registered scale and radial
laws. It uses existing local data as evidence, and does not import a literature
mechanism or claim literature-wide novelty. The neighboring
`campaign_fresh_gravity/` campaign was not edited.

## Fixed framework

The primary scale remains a = kappa c sqrt(G rho_Lambda), with both adopted
normalizations 9.3619e-11 and 1.1279e-10 m/s². Kappa is an input, not a result
of this stage. The constant-vacuum branch and the separate comparison
a(z)=a(0)E(z) are evaluated distinctly. E(3)=4.5656324863 for the registered
background. Scaling is already included in the discrepancy calculations.

The two explicit radial laws are

    Q: F(B;a) = sqrt(B²+aB),
    R: F(B;a) = B/[1-exp(-sqrt(B/a))].

B is baryonic Newtonian acceleration; F is predicted physical acceleration.
They are different functions. The inherited monotone radial branch M is
evaluated separately in the cluster lane; the scalar dynamical construction
below covers Q and R only.

## Four results that survive this pass

| Question | Result | Scope and evidence |
|---|---|---|
| Do the moment and measurement derivations withstand independent reconstruction? | Yes, after a real support correction to necessity claims. | [Independent audit](proof_precision/AUDIT.md), [correction](SUPPORT_CORRECTION.md). Numerical checks and all four stage-two programs pass. |
| Can simple gas motion or one calibration factor remove the cluster residual? | The declared steady spherical flow fails a force-sign test; tested common scalar corrections leave a shape mismatch. | [Cluster report](cluster_precision/REPORT.md). Central reconstructed profiles, conventional matter mechanics, no raw-data likelihood. |
| Can the radial law support conservative time evolution? | An explicitly assumed scalar family can; it is not uniquely selected by the radial law. | [Dynamics derivation](dynamics_precision/DERIVATION.md), [scoped independent review](proof_precision/DYNAMICS_CROSS_REVIEW.md). No metric or lensing completion. |
| Can greater spectral precision uniquely measure the scale? | Sometimes with fixed maps; not along an exact symmetry when two map calibrations float freely. | [Joint inference](joint_identifiability/RESULT.md). Synthetic recovery and an exact algebraic invariance, not observed calibration errors. |

### 1. The proof correction is consequential

For alpha=P^T l4 and beta=P^T l2, exact fourth-moment broadening correction
for every independently variable emitting-source velocity requires

    diag(I)[s² alpha-beta] = 0.

The earlier unweighted full-vector condition is sufficient, but is necessary
only on the active source support. A zero-emission cell cannot constrain a
spectrum. A known zero projection or a dynamical restriction can reduce the
allowed nuisance space further. The audit supplies an exact rational
counterexample to the unrestricted necessity claim. Earlier evidence remains
unchanged; the additive correction supersedes that wording.

The synthetic disk had positive emission and projection throughout, so its
stored numerical conclusions survive. Variance claims also require finite
eighth moments for the second/fourth-moment estimators, and finite twelfth
moments for the sixth-moment delta-method calculation. Calibration, matching
weights and flux/exposure conventions remain explicit assumptions.

### 2. Cluster explanations now face a coupled force and measurement test

Write Delta=gH-F(B;a), with outward-positive gas velocity u. Conventional
Euler balance with additional isotropic pressure Pnt requires

    partial_t u + u partial_r u = Delta - (1/rho) partial_r Pnt.

At all 252 evaluated shell/branch points Delta is positive. If Pnt decreases
outward, the required acceleration is positive. But steady spherical
source-free continuity, using each piecewise gas-mass profile Mgas=C r^s,
gives

    u partial_r u = (1-s)u²/r.

All 189 interpolation intervals overlapping 100–1000 kpc have s>1, ranging
from 1.185516 to 2.678286. At the evaluated interior shells, continuity thus
demands a nonpositive acceleration. **Those assumptions cannot jointly
explain these central reconstructions.** This does not exclude time-dependent
motion, asphericity, mass sources, different density reconstruction or changed
matter dynamics. Euler-only speed bounds are not viable flow solutions.

Changing inferred density, pressure and distance must change both sides of
the comparison. With their ratios eta, pi and d, and stellar M/L ratio upsilon,

    B' = eta d Bgas + upsilon Bstar,
    gH' = pi gH/(eta d).

For X-ray amplitude chi, SZ amplitude psi, temperature ratio tau and
emissivity ratio ell, the declared thermal map gives

    chi=eta² ell d,  psi=pi d,  tau=pi/eta,
    d=psi² ell/(chi tau²).

Consequently these freedoms cannot be adjusted independently while claiming
unchanged observations. For canonical vacuum R at 300 kpc, pointwise force
equality requires median density factor 2.1208 at fixed pressure/distance, or
distance factor 1.9394 at fixed X-ray/SZ amplitudes and emissivity. The latter
also predicts a median temperature ratio 0.7181. Fixed emissivity under a
temperature change is only a conditional slice, not a plasma/detector fit.

Even the optimal common distance in that X-ray/SZ-preserving slice leaves
a minimum largest multiplicative force mismatch of 1.6095 over 21 shells.
This is a deterministic shape discrepancy, not a significance or an exclusion
of richer calibration models. There are no independent error priors here.

### 3. A conservative dynamical construction needs additional physics

Directly multiplying the Newtonian vector field by F(B;a)/B is generally
nonconservative: an explicit harmonic vacuum field gives nonzero curl for
both laws. A newly assumed scalar constitutive construction avoids that:

    b(g;a)=F^{-1}(g;a),  W(g;a)=integral_0^g b(s;a) ds,
    div[(b/g) grad(phi)] = 4 pi G rho.

It returns the registered radial law in spherical symmetry. Its nonspherical
field is determined by the differential equation, not pointwise rescaling.
The lane provides a bounded-domain weak existence/uniqueness argument under
specified Dirichlet/source hypotheses; this functional-analytic part has not
received the separate proof agent's audit. Ellipticity degenerates at zero
field, and no global evolution theorem is asserted.

Adding a preferred-frame kinetic term K phi_t²/(8 pi G c²), K>0, yields
energy/momentum exchange identities and positive linear field energy on a
nonzero uniform-gradient background. The local characteristic relation is

    omega² = (c²/K)|k|²[(b/g) sin²(theta)+b' cos²(theta)].

K=2 and K=8 preserve exactly the same static solutions and both satisfy the
derived sufficient field-speed bound, yet response times differ by two.
**Static observations cannot select K in this family.** This is a missing
physical input, not uncertainty that more precise static fitting removes.
The independent proof lane checked conservation signs and speeds at the
exact finalized derivation hash; it did not audit the dynamics code.

For prescribed a(t), energy balance additionally contains

    W_a a_dot/(4 pi G).

Thus the separate H-scaling branch requires an actual sector supplying the
opposite exchange. In the deep regime W=g³/(3a), the source becomes
-(a_dot/a)W/(4 pi G). Merely substituting H(z) does not supply that sector.

A further restricted Lorentz-invariant first-derivative scalar construction
has radial characteristics outside an imposed metric light cone. That scoped
conflict does not prove general acausality or rule out every relativistic
completion. No photon coupling or lensing prediction is derived here.

### 4. Identification improves only when the measurement assumptions justify it

With known baryonic, geometric and emissivity maps, spatial second moments
can separate a from one unknown width-variance multiplier. All 24 tested
spatial cases recover both noiseless parameters from four starting points;
all 12 single-aperture cases remain rank-deficient. This is a restricted
nuisance model, not a claim that arbitrary unresolved broadening is removable.
An earlier two-moment example also has two distinct solutions with locally
invertible Jacobians: local rank alone does not prove global identification.

More strongly, both laws obey F(cB;ca)=cF(B;a). If source velocities are

    u_i²=gamma q_i F(beta B_i;a),

then (a,beta,gamma)->(ca,c beta,gamma/c) preserves every velocity and the
entire modeled spectrum when the other maps and conditional noise stay fixed.
Finite cubes agree to 3.34e-16. The universal claim follows from homogeneity,
not the finite computation. These calibration freedoms are mathematical
conditions, not evidence that factors of E(3) are plausible observational errors.

An immediate algebraic consequence specifies the needed calibration:

    u_i²=(gamma beta) q_i F(B_i; a/beta).

The invariant combinations are A=a/beta and C=gamma beta. If the forward
model identifies A and C, an independent beta fixes a=A beta; alternatively
an independent gamma fixes a=AC/gamma. Either anchor can break this orbit;
its uncertainty and correlations must enter the inference. No assertion
that A and C are always globally identifiable is made. This distinguishes a
specific measurement requirement from a request for more photons alone.

## Exact remaining closure obligations

1. Derive or independently justify the adopted normalization and select a
   physical scale sector. An H-dependent scale must close the energy exchange.
2. Select and constrain time evolution and matter/metric coupling. The free
   kinetic law, photon trajectories, lensing and coupled stability remain open.
3. Reconstruct joint cluster density, pressure, temperature and emissivity
   constraints at common angular shells with actual instrument responses.
   Determine whether the residual/sign assumptions survive those uncertainties.
4. Fit the same model to the distinct empirical domains using calibrated
   nuisance parameters and held-out predictions. The cached galaxy/cluster
   checks are not a cosmological or all-evidence likelihood.

The next physical derivation should address an explicit scale/time sector
and its measurable response. The next empirical calculation should test the
cluster thermal closure with independently constrained response/calibration
inputs. Neither gap is resolved by renaming the remaining mass discrepancy.

## Verification and audit coverage

The coordinator independently revalidated these five accepted version-2
computation records against the current input/output files, all exit 0:

| Lane | Accepted record | Interpretation |
|---|---|---|
| Independent mathematics | [run_003](proof_precision/run_003/manifest.json) | Independent code and derivation checks; bounded numerical grid |
| Earlier numerical reproduction | [reproduction_001](proof_precision/reproduction_001/manifest.json) | Re-executes all four original stage-two modules; shared-code reproduction |
| Cluster constraints | [run_003](cluster_precision/run_003/manifest.json) | 252 baseline shell checks, 756 pointwise roots, 288 minimax problems, 168 quadrature checks, continuity checks |
| Dynamics | [run_002](dynamics_precision/run_002/manifest.json) | 26 finite checks; energy residual <5.18e-11, momentum residual <3.63e-9 |
| Joint inference | [run_002](joint_identifiability/run_002/manifest.json) | 36 scale/width models and full-spectrum symmetry controls |

Manifest validity verifies execution provenance, not mathematical truth or
empirical adequacy. Failed runs and their explanations are preserved in the
lane reports. No failed run is counted as accepted evidence. Numerical
validation is binary64, not interval certification. Self-review of this
summary checked signs, units, quantifiers, branch distinctions and agreement
with the linked reports; it is not another independent referee review.

The record is anchored to the declared base
`eccd1c0e59459b5ec1acf2e916fb7a05a7f67971` and individual file hashes in a
dirty shared workspace. No commit or publication was made. This checkpoint
completes the precision pass; it does not declare the research objective solved.
