# Independent analytic check of PROFILE_GATE

**Verdict: proved as written within the declared scope.** Equations (1)–(3), the additive/nonlinear distinction, the disk-ring warning and the inference limits pass. No author-file correction is required.

Reviewed file: `reviews/collective_state_door_2026_10_20/PROFILE_GATE.md`.
SHA-256: `aea7839863a69f6008b5c4714c0c524b36bd46c717285b8d51ab60aa9cdedc8d`.

The normalized claim is a *recommended conditional feasibility test*, not an executed reconstruction or evidence for a detected remnant. The adopted baryonic baseline, geometry, distance, inclination, circular-velocity interpretation and uncertainties must be fixed or explicitly admitted as nuisance inputs.

| Obligation | Status | Independent check |
|---|---|---|
| (1), additive spherical inverse | passed | `Delta g=GM_x(<R)/R^2` and `M_x'=4 pi R^2 rho_x` give both formulas, with correct units and signs. |
| Positive spherical mass and boundary conditions | passed | `M_x>=0`, `M_x'>=0`; the stated origin/outer extension is necessary. An exact outer plateau means outside compact support; finite mass with tails gives an asymptotic plateau. |
| Additive versus jointly nonlinear response | passed | Adding free mass can change the medium's response and hence the baseline. The difference of two nonlinear solutions is not generally the Newtonian field of the added mass alone. The note expressly declines that inverse. |
| (2), positive sources and signed force kernels | passed | Newtonian superposition is linear at fixed geometry. Positive mass does not force each inward radial acceleration coefficient to be positive. |
| Unconstrained cone warning | passed | Thin rings near measured radii can provide excessive fitting freedom; no claim that every constrained matrix is degenerate is needed. |
| (3), finite-grid negative certificate | passed | If `A m=d`, `m>=0` and `A^T y>=0`, then `y^T d=(A^T y)^T m>=0`, contradicting `y^T d<0`. Only this direct implication is asserted. |
| Detection, physical-state uniqueness or lifetime | not addressed | Neither the gate nor this audit supplies them. |

For the ring sign, a positive circular ring of radius `a` has in-plane potential near its center
`Phi(R)=-GM/a[1+R^2/(4a^2)+O(R^4/a^4)]`. Thus `partial_R Phi<0`: its force is outward in the inward-positive convention. An interior source gives the opposite sign. Already at one measurement radius, unrestricted positive sources can therefore generate either residual sign. Arbitrarily thin rings near measurement radii add further flexibility. Independently specified height, support, resolution, supply and outer-profile/state restrictions are essential; a successful unconstrained ring fit would not identify a mechanism. The spherical test consequently does not exclude every positive disk, and radial kinematics do not fix the vertical force.

The uncertainty restriction on (3) is material. At fixed `A`, a common robust certificate requires `sup_{d in D} y^T d<0` over the admitted error set, together with `A^T y>=0`. Nuisance-dependent kernels require the corresponding dual condition for all admitted kernels, or valid exclusion of each admitted joint case. A finite-grid certificate does not exclude an unrepresented continuum source family. Cone feasibility is only preliminary: additional physical constraints still need enforcement, and feasibility does not prove formation or uniqueness.

The local source wording is appropriately calibrated. The AG4h README lists the five positive-pull Q=1 objects as a post-hoc follow-up set and explicitly calls it “not a detection.” It retains noncircular/projection effects, stellar decomposition and radial mass-to-light gradients as alternatives. A positive fitted pull does not establish a positive radial residual at every radius. The UGC08286/UGC00731 priority comparison matches the reported TRGB/CF4 versus Hubble-distance metadata; this audit does not validate the underlying catalogues. CFG926's README makes its IMF red-lens reduction conditional on its adopted red/disc asymmetry and other stated limitations. The gate preserves that qualification. The separate `recent/UPDATE` owns the full source-status reconciliation; these README checks do not audit their scripts or observations.

The safe outcome is a follow-up criterion: test a predeclared admissible remnant family against the measured radial profile and independently constrained stellar/kinematic alternatives in the same observational space. A permitted inverse solution would supply a subsequent density/scale target. It would still owe the canonical operator/action, release mechanism and retention dynamics.

**No radial reconstruction, mass inversion, stellar-gradient fit, broad fit, scientific numerical run, new mass profile, detection or lifetime inference was performed.** This is independent analytic reconstruction of the current note only. The completed `audit_finite/RESULT.md` and `audit_finite/provenance.json` were hash-checked and left unchanged. Only this review and `profile_gate_provenance.json` were written. Mathematical self-proofreading found no unresolved issue in this scope; no mathematical-token correction was made. The provenance contains all raw source hashes and final report verification.
