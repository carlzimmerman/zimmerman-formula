# Analytic review and continuation record

18 October 2026. Checkpoint ZAR-2026-10-18-01; repository baseline `3c01aa2861bf576f4c2d942251eb9d2f89cae108`. The files in this folder are new research notes, not amendments to frozen criteria or a manuscript claiming completion.

## Overall physical verdict

**Incomplete, with the smallest missing implication being a finite, warm, dynamically stable halo whose population partition and amplitude follow from physical formation.** The idealized stationary family below supplies a compatibility result for an effective spherical model. It does not supply that implication.

## Kinetic family audit

**Claim.** For smooth compact spherical profiles, the stated energy varies to the two stated accelerations. For the corresponding deep cubic forces, the infinite profiles M_t = f A r and M_f = (1-f) A r with 0 < f < 1 admit the displayed Jeans moments and positive isotropic stationary distributions. The finite-stock one-population virial identity holds with the stated boundary and stationarity assumptions.

**Mathematical verdict: proved as written under those explicit hypotheses.** Physical formation, finite matching, stability, finite stiffness and relativistic completion are outside this claim.

| Obligation | Evidence | Status |
|---|---|---|
| Radial functional variation | A mass relocation changes enclosed mass by minus that mass over the traversed interval. Differentiating the integrands yields -G M_f/r^2 and G^2 M_t^2/(a0 r^4) for t, and -G(M_t+M_f)/r^2 for f, plus the common baryonic force. | Passed |
| Reciprocal t/f coupling | Both accelerations use the same symmetric cross energy -G integral M_t M_f/r^2 dr. Separate population masses are conserved. | Passed in spherical effective model |
| Constant partition forces | Substitute M_t = f A r, M_f = (1-f) A r and A^2 = a0 M_b/G. | Passed |
| Jeans moments | Differentiate sigma_i^2 = C_i/(3r) + D_i/2 + H_i r^2 in the stated Jeans equation. Bounded outer branch has H_i = 0. | Passed |
| Positive phase-space density | Phi_i' = (C_i + D_i r)/r^2 > 0 and rho_i'' = 2 b_i(C_i+2 D_i r)/(C_i+D_i r)^3 > 0. | Passed |
| Distribution normalization | Swapping the positive Abel integrals gives the beta integral pi(s-Phi)/2; remaining integration by parts returns rho_i(Phi). | Passed |
| Endpoint convergence | For finite E the lower inverse-square-root singularity is integrable; rho_i'' decays exponentially at high potential. | Passed |
| Global energy | Infinite mass and singular center make the scale-free family inadmissible as a finite-energy state of the compact-profile functional. | Not established; explicitly excluded from claim |
| Virial boundary and sign | From div Pi = rho a, integrate x dot div Pi = B - 2K. Finite boundaries and nonstationarity retain their respective terms. | Passed |
| Fraction and amplitude selection | f and the target amplitude A are inputs to the equilibrium ansatz. | Not addressed |
| Stability and nonspherical dynamics | A positive stationary distribution and reciprocal action do not establish either. | Not addressed |

The root derived the constant-partition extension and spherical functional. The theory reviewer independently derived the partition dispersions and supplied the positive-distribution construction. A separate data reviewer then checked the functional variations, virial sign, Jeans moments, derivative, Abel normalization, endpoint convergence and the written kinetic note without a scientific run. This is separate same-team review, not a formal certificate or external referee report.

Prior art inside the repository includes the warm-carrier obstruction, two populations and their current/charge distinction. The explicit compatibility family is the scoped addition. The new mathematical claims do not depend on an external theorem leaf: their derivations are written in [KINETIC_PARTITION.md](KINETIC_PARTITION.md).

## Shape null audit

**Claim.** For positive h, a single positive geometry factor Q, a common baryon-template scale lambda, positive a0 and an operative algebraic radial law, the simple and quadratic candidates imply their respective three-radius determinants vanish. They are exactly distinguishable for three distinct h values, while practical limiting-regime power can be poor.

**Verdict: correct only after the stated restriction to gas-only or exactly fixed-composition templates and a common geometry normalization.** A generic SPARC disk does not automatically satisfy those hypotheses.

The separate data reviewer rederived both eliminations, their behavior under shared rescalings, the positive-coefficient condition and strict-concavity separation. The root checked the exact rational example by hand. Correlated transformed-axis errors, radial stellar contamination and warp/curl effects remain empirical obligations. No detector data, SPARC determinant, covariance fit, p-value, registered statistic or threshold was evaluated.

Dependency graph: candidate polynomial law + definitions g = Q q and b = lambda h -> affine relation -> determinant zero. Strict concavity supplies separation. No external computational or theorem leaf is needed. Generic shape estimators already exist in k01/k02; the novelty statement is limited accordingly.

## Donor volume audit

**Claim.** Conserved compact spherical redistribution from uniform positive rhobar_c, with enclosed excess M_h within r_e and compensation completed by r_c, satisfies r_c^3 >= r_e^3 + 3 M_h/(4 pi rhobar_c).

**Verdict: proved as written.** The bound follows by integrating delta rho >= -rhobar_c over the compensating volume. For the cold contrast alone, compact exact compensation also gives DeltaSigma = 0 beyond r_c. This is not a prediction that the intermediate lensing contrast must be negative.

The experiment reviewer supplied the inequality and checked it again in the written overview; the root independently reconstructed the mass integral and projected outer limit. It is an elementary sharpening of the existing donor/depletion route. An overdense initial reservoir, open mass flux, creation or noncompact compensation changes the hypotheses.

## Evidence review corrections

The separate evidence review caught one terminology error in the draft: the clumping summary's I/I_initial = 1.0391 is a field-intensity ratio, not an established cold-mass density ratio. The overview now gives I = abs(Psi)^2 and links the defining code. This did not enter any new mathematical derivation. Earlier status summaries remain untouched.

The review also preserves the distinction between a cold contrast and the total baryon-plus-environment lensing signal, and between inherited likelihood assumptions and evidence that those assumptions caused a failure. No failed candidate was silently upgraded.

## Route disposition and handoff

| Route | Outcome of this work | Disposition | First useful next check |
|---|---|---|---|
| Kinetic extension | Explicit reciprocal spherical forces and a positive stationary idealized family | Open; finite-halo successor deferred to a separate analytic work package | Construct finite core/outer matching and check positive distribution, virial boundary terms and coupled stability |
| Calibration elimination | Exact distinct null identities with explicit nuisance cancellation | Open; empirical use deferred because geometry, stellar contamination, transition leverage and covariance need admission | Establish whether an existing sample can distinguish the curves before evaluating or registering a rejection threshold |
| Supply/environment | Exact positivity lower bound and outer projection distinction | Open; donor profile not selected | Apply the bound to a single counted candidate and derive its complete projected contrast |

No route is marked exhausted. Further simulations and registered data evaluations remain deferred while the existing computational chain runs. The immediate physical bottleneck is the finite, source/current-consistent successor, not a request for a larger scan.

## Verification and proofreading

Verification consisted of explicit analytic derivations, separate algebra reviews, read-back of the written equations and status claims, local-link checks, math-delimiter checks, and small-file input hashing. No scientific result was rerun. These checks cannot establish a physical theory's success or global novelty.

Math-proofreading scope: this folder only. Definitions, one-dimensional versus total velocity moments, positive parameter domains, boundary assumptions, and force signs were checked in context. The draft field-intensity terminology was corrected as an evidence issue; no previous repository equation or status was edited. Full source freshness and final artifact hashes are recorded in the provenance and completion metadata files.
