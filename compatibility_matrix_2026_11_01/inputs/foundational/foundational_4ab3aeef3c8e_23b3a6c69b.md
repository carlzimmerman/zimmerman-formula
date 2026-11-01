# PN28 continuation contract

Original target: derive a conserving finite-halo pressure mechanism and its
vacuum-normalized acceleration coefficient without feeding the desired a0
into the parent. Base `66c45c5082f651dd54e171f98c11acd9cb3d9086`; exact inputs
and reviewed revisions are in INPUTS.json, route provenance and
VERIFICATION.json. User authorization is continued theory work; new files
and bounded calculations are authorized. No new permission is required for
the next mathematical discriminator. No manuscript integration, external
message, publication, commit or long simulation has been requested.

The target is **open**. The current synthesis is REPORT.md. Do not reload the
entire repository or rerun past failed normalizations unchanged.

## Strongest surviving construction

Read dispersion_coupling/EOS.md, dispersion_coupling/REPORT.md,
dispersion_coupling/STATIC_WATERBAG.md, halo/DERIVATION.md and the
finite_gradient route's final record. The specific parent has relative
kinetic metric exp(2s), potential V+B(exp(3s)-3s-1), and a selected canonical
waterbag. Its total reduced pressure tends from rho^(5/3) to B ln rho.
The static energy-cutoff waterbag realizes the state in the occupied interior.
The full static scalar/Poisson system is

    n=exp(3s) psi_+^(3/2),
    Delta psi=-n,
    epsilon Delta s=exp(3s)(1-psi_+^(5/2))-1.

The vacuum continuation is explicitly static u=pi_s=0. A general dynamical
Hamiltonian at zero density remains undefined by expressions j/rho and
|j|²/rho alone. Do not call a static solution a well-posed formation theory.

The auxiliary limit has an analytic finite-radius theorem and an asymptotic
quarter-column coefficient xi_q defined by Theta''+2Theta'/r=1/Theta,
Theta(0)=1, Theta'(0)=0, Theta(xi_q)=4. Its numerical value is about 5.84477.
This is total pressure, not the original MC27 bare kinetic closure. At finite
scalar stiffness gradients prevent unrestricted use of the infinite-density
limit. B/V and phase level remain independent.

## Route dispositions and exact next steps

| Route | Current disposition | Next executable discriminator / resumption condition |
|---|---|---|
| DISP / field origin | Conditional constructive mechanism, open | Derive or prohibit the exp(6s) vacuum-preserving deformation from an explicit symmetry/microscopic action. Merely repeating the chosen exp(3s) potential does not establish universality. |
| DISP / normalization | Free B/V, open | Specify a physical state/symmetry linking canonical scalar stiffness and dispersion coupling to gravitating V, then vary allowed couplings at fixed V. A permitted variation changing B disproves that proposed selection. |
| HALO | Reduced finite-radius and core-limit obligations resolved | Use finite_gradient evidence for actual static field profiles; establish an error bound or existence argument in its finite epsilon regime if a theorem is wanted. Do not substitute the local EOS at finite gradients. |
| GRAD | Six static cases and two domain/tolerance refinements passed; finite radius follows conditional on a regular decaying branch | Read finite_gradient/DERIVATION.md and the independent REVIEW_FINITE_GRADIENT.md. The next physical task is stability/formation of the selected stationary kinetic state with its reciprocal scalar and a specified vacuum extension. The finite observations do not establish universal columns or fixed-mass response. |
| TRANS | Positive local Fourier repair refuted under fixed EOS/homology | Reopen with a genuinely changed flux, anisotropic stress, moving phase boundary or direct microscopic exchange; check the full central-moment hierarchy and reciprocal energy. |
| RES | Local fixed-C vacuum closure has negative acoustic response at p>A | Reopen only with delayed/nonlocal response, independent stresses or changed density/energy map. Adding an energy-only source while omitting vacuum force repeats the failed construction. |
| REL | Exact relativistic normalization and static all-hot discriminator resolved | To seek spatial log pressure, specify a massive mixed-temperature self-gravitating model and its global phase/energy constraints. K=vacuum and phase-span=density-span remain unproved. |
| Covariant completion / data | Open, deferred pending a chosen consistent parent | Define the vacuum coupling, mass-energy sources and interpolating force law for this changed stress model before comparing with existing observational likelihoods. Old passes do not transfer automatically. |

These continuations remain open; this checkpoint does not label them
exhausted or impossible. Mathematical success of the constructed branch is
partial progress toward the user's original target.

## Review and evidence rules

- Independent EOS/core proof reconstruction:
  relativistic_mixing/REVIEW_EOS_HALO.md. It also checks specified action
  identities and records zero-density/gradient restrictions.
- Independent local reservoir reconstruction:
  transport/REVIEW_RESERVOIR.md, including the corrected physical domain.
- Independent finite-gradient reconstruction:
  relativistic_mixing/REVIEW_FINITE_GRADIENT.md. The endpoint spline second
  derivative remains an unverified auxiliary diagnostic; integrated checks
  and the imposed zero central slopes must not be presented as its validation.
- Coordinator transport cross-check:
  transport/COORDINATOR_REVIEW.md; this is not a blind fresh-session review.
- Finite evidence is retained in v2 runner manifests, with input and output
  hashes. Read run.status, not just validator success. Superseded drafts and
  serialization-only failed runs are historical, not current positive evidence.
- No worldwide novelty claim has been established. Source transfers in
  reservoir/SOURCES.md are bounded exact-version checks.

All agents wrote disjoint route directories. The coordinator reconciles
current results into REPORT.md and VERIFICATION.json. Nothing in this
checkpoint authorizes another agent to change the pre-existing theory files
or contact other chats without user instruction.
