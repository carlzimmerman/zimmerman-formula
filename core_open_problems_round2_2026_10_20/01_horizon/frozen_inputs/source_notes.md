# Source checks: horizon normalization

Checkpoint HORIZON-2026-10-20-01; checked 2026-10-20 (local date).
No novelty claim or exhaustive literature search. The three primary texts below
were opened in full, with metadata checked against their arXiv abstract pages.
The project cache had no exact hit for gr-qc/9706018v1 or astro-ph/9805346v1;
the latter discovery led to checking the published-version preprint v2 instead.
No external full text is committed or newly cached; therefore there is no local
external-source byte hash. Exact version URLs below are the source pins.
Repository input hashes are in run_002/manifest.json.

## S1 — thermal temperature, not a force law

S. Deser and O. Levin, *Accelerated Detectors and Temperature in (Anti) de Sitter
Spaces*, CQG 14 (1997) L163–L168, [arXiv:gr-qc/9706018v1](https://arxiv.org/html/gr-qc/9706018v1),
[DOI](https://doi.org/10.1088/0264-9381/14/9/003).
Equation (8) and the following conformal-field discussion establish the
temperature on the specified uniformly accelerated de Sitter trajectories.
Our units give `kB T = hbar sqrt(a²+(cH)²)/(2 pi c)`.
Both HTML and PDF were checked; the application uses geometric radius R in
(8), not the apparent inconsistent radius/curvature wording in the preamble.
**Verified:** temperature for that trajectory and conformally coupled massless
scalar setting. **Unverified:** a gravity law or a mapping from a freely
orbiting star to this proper acceleration.

## S2 — the force identification is hypothetical

M. Milgrom, *The Modified Dynamics as a Vacuum Effect*, Physics Letters A 253
(1999) 273–279, [arXiv:astro-ph/9805346v2](https://arxiv.org/html/astro-ph/9805346v2),
[DOI](https://doi.org/10.1016/S0375-9601(99)00077-8).
Section IV, equations (6)–(9), gives the temperature-excess expression with
scale `a0_hat=2 sqrt(Lambda/3)` in natural units. The next paragraph leaves the
inertia identification and circular-motion transfer unestablished. Equations
(10)–(11) exhibit another temperature functional with a different scale.
**Verified:** conditional algebra and caveat. **Conditional:** interpreting
it as inertia. **Inapplicable as-is:** deriving CFG695's simple-mu potential.

## S3 — actual transition rate and gap dependence

Md. Sabir Ali, S. Bhattacharya, K. Lochan, *Unruh-DeWitt detector responses for
complex scalar fields in de Sitter spacetime*,
[arXiv:2003.11046v2](https://arxiv.org/html/2003.11046v2), 18 February 2021.
Section 3.1, equation (15), at alpha=0 is the real conformal scalar rate;
their `p=2 DeltaE/H`, with hbar=1, maps to our `x0=pi p`.
The rate is `DeltaE/[2 pi (exp(2 pi DeltaE/H)-1)]`, after removing the detector
coupling and matrix element. For the accelerated trajectory, S1's Wightman
dictionary supplies `H -> sqrt(H²+a²/c²)`; our shifted-contour integral checks
that transfer for the conformal field. We do not transfer the paper's complex
or minimally coupled results into this formula.
**Verified:** comoving conformal rate and notation; accelerated rate under S1's
field and trajectory assumptions. No gravitational force law follows.

## Nearest local predecessors and changed information

- CFG695 supplies the postulated potential, not a microscopic derivation.
- `argon_push/AG4_law_from_action/README.md` separates simple-mu from the
  quadratic capacity family. We check their capacities and low-field series.
- `sol61_push/cold_final_mile_2026_10_13/ACTION_CORRECTION.txt` supplies the
  necessary full-versus-remainder potential correction.
- `campaign_fresh_gravity/CFG904_rt17_vs_rt19_audit/README.md` already resolves
  the frequency/temperature normalization conflict. The earlier CFG894
  `KAPPA_DOORS.md` P4 item is stale. No new resolution is claimed here.
- `reviews/mi_dsunruh_freedom_audit_2026.py` supplies the ambient `A=a0/2`
  origin of the 1/11.58 language. Its claims about arbitrary response functions
  exceed its tested power-law family; we make no such universal claim.
- `opus_48_extended_research/reviews/toe_law/agentYY_modular_a0.md` already
  studies spectral dependence of relative entropy. Our qubit calculation is
  a transparent check, not a new general information-theory no-go.
- `sol61_push/cold_production_2026_10_11/mechanism_2026_10_12/NODAL_RING_ORIGIN.md`
  already shows zero-temperature nonanalytic cubic response and thermal
  rounding. The finite-dipole argument exposes the regularity issue directly
  in the ordinary dielectric-saturation analogy.

The added checkpoint is the analytic-readout obstruction for CFG695's exact
function, independent Fourier verification of the detector rate, and explicit
gap-dependent thresholds at both acceleration fractions. It is an independent
audit/calculation, not a claim of literature novelty.
