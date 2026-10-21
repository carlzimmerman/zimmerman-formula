# Discrete reference bracket for the depleted late remnant

The completed `matched_refs_run_004` supplies Q136000 and Q140000 reference caches at L=60, N=599/1199. Its v2 manifest independently validates and all47 declared checks pass. Exactly four gyroscopic mode matrices were computed across the attempts; the completed Q136000 cases were recovered byte-for-byte from the later-failed intermediate run instead of recomputed.

| Reference Q | N | omega | Localized ell2 Omega | Discrete E |
|---|---:|---:|---:|---:|
| 136000 | 1199 | .9120838357251844 | .060387406141327836 | 127465.40887380933 |
| 136000 | 599 | .912081827502379 | .06039149165564203 | 127464.88075585343 |
| 140000 | 1199 | .9116133426803649 | .059587045281958545 | 131112.7968218612 |
| 140000 | 599 | .9116113599141207 | .05959107784155831 | 131112.26072232382 |

The fine-grid modes have more than99.04percent of canonical radial norm at r<15, unit no-half K, pencil residuals below4.7e-13, and phase-Noether residuals about1.3e-13. Integrated discrete Q agrees with its target to numerical precision. The chiral m2 normalization obeys J=2K/Omega; using the same radial mode for the actual axisymmetric m0 projection gives J=0. These are localized candidates continuing the prior branch near the declared shifts .060/.059, not a globally complete or continuum spectrum theorem. Measured RSS was107724800 bytes.

For the fine references use

    matched_refs_run_004/Q136000_L60_N1199.npz
    matched_refs_run_004/profile_Q136000_L60_N1199.npz
    matched_refs_run_004/Q140000_L60_N1199.npz
    matched_refs_run_004/profile_Q140000_L60_N1199.npz

The mode caches contain `r,mode,Zmode,omega,Omega,Q,E,K_normalization,background_fields` and exact discrete-charge diagnostics. The profile caches contain API-compatible `r,y,omega,Q,E`. Their metadata explicitly says **INTERPOLATED DISCRETE stationary reference, NOT a true-origin BVP**. At r=0 the profile uses an even quadratic extrapolation from the first two discrete field values and a derivative-zero cubic interpolant. The cumulative-charge row is a discrete diagnostic. These interpolants do not claim to solve continuum field equations at the origin or between grid points.

The new pair of charges brackets late aperture-stock diagnostics and enables reference-sensitivity checks. It does not prove that either value is the unique bound remnant charge, identify aperture charge with mass, validate the old Q160000 reference after charge loss, or transfer its radiation coefficient to these different backgrounds. Actual projection/time-series and remnant-compatibility checks remain separate.

## Preserved failures and repair provenance

`matched_refs_run_001` failed the unchanged15-step discrete Newton cap with the direct Q160000 seed, before any eigenvalue solve. `run_002` also reached that cap after geometric radius rescaling. The separate `newton_diagnostic_run_001` records the exact unchanged iteration history: full residual fell4.0677 to2.4123, the undamped omega step fell .002555 to .000473, and accepted line-search steps increased to one half at the cap. This was continuing damped convergence, not a precision floor or evidence against the branch.

A separately named local source raised only the outer Newton cap15 to80 and retained full histories; equations, line search, target charges and pass tolerances stayed fixed. Q136000 then converged in19/18 recorded iterates. That `run_003` successfully wrote both Q136000 caches but later failed before Q140000 because a local profile-output variable shadowed the dense input-seed array. The original failed run/source remain unchanged.

`matched_refs_v4.py` fixes that variable name, validates and copies the two completed Q136000 cases, and computes only the two remaining Q140000 cases. They converge in15 recorded iterates each. The final run and its sources pin the exact intermediate cache bytes and full histories. A successful final recovery does not relabel any earlier full run as completed.
