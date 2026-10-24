# X8_soft_side_caustics: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT, plus
FITTED (κ = ½, L★), ILLUSTRATIVE (round model values, not data) and METHOD (own numerics).

## A. What the open item rests on (the review's "not established, not excluded")

| ingredient | class | where | used here as |
|---|---|---|---|
| frozen-F test-particle model ẍ = Δg_b + s·Γ²(x − q), D̈ = −ΔT_b(I + D) + s·Γ²D | FRAMEWORK-NATIVE record (review §0–§1) | `reviews/v3s_soft_side_caustics_2026_10_23/caustics.py` | reproduced read-only (R0); its s = 0 content is this lane's MUTATE |
| soft region from the QUMOND phantom sign | STANDARD-MOND-MACHINERY (a disclosed proxy in the review) | review §1 | **not used**: this lane takes the sign from v3s's own discrete AQUAL phantom |
| A2 validity split (adiabatic vs slow regions) | FRAMEWORK-NATIVE record (diagnostic) | `caustics_validity.py` | motivation only; superseded by the self-consistent solve |

## B. This lane's ingredients

| ingredient | class | source |
|---|---|---|
| v3s action: v3 + −(γ_L/2)[max(D·P, 0)]² | FRAMEWORK-NATIVE (adopted 2026-10-23) | V3_FULL_PICTURE §1, §4.7; X3 |
| weak-field PN system (Ξ, hold law with J_Y = μ − 1, Poisson with all mass, khronon continuity and Euler) | FRAMEWORK-NATIVE; BS24 PN transcription PROVISIONAL (via C4/BSK1), re-derived in H4 A1 and H5 A1 | V3_FULL_PICTURE §2; L1 FROZEN §1; H4; H5 |
| switched stiffness as the pressure γ_Lρ₊²/2 acting where D·P > 0 (Ξ̃ = Ξ + γ_L ρ₊) | FRAMEWORK-NATIVE (X3 B1-S, B2-S) | X3 README §1 |
| J_x, μ = x/(1+x); M_T = 1 + x, M_L = (1+x)² | FRAMEWORK-NATIVE (POSTULATED in the theory) | V3_FULL_PICTURE §1; H4 A5 |
| AQUAL static equilibrium as the initial state (not QUMOND) | FRAMEWORK-NATIVE (the theory's own static limit) | V3_FULL_PICTURE §2; C4 K1 |
| linear dispersion ω² = Kρ_τ(M_θ − 1 + Θ L★²k²/2) (the V-b prediction) | FRAMEWORK-NATIVE record | H4 A4, X3 B1-S |
| a₀ footings 9.3603e-11 / 1.1312e-10 m/s² | FITTED (κ = ½) | doors BRIEF; V3_FULL_PICTURE |
| L★ = 21.682 / 22.849 pc (v3s floors), γ_L = K L★²/2 | FITTED | X3 D4 |
| μ_K → 0, no BS dust in the saddle | framework regime choice (S4: μ_K ≥ 0.1 Mpc⁻¹ fails the galaxy guard); the review's setting | S4; review §1 |
| MW 6e10 M☉, M31 1e11 M☉ baryons; Plummer ε = 20 kpc | LITERATURE-INPUT, ILLUSTRATIVE (H4 S1 masses; the review's softening) | review §1; H4 FROZEN §3 |
| M31 distance 780 kpc and radial velocity −110 km/s | LITERATURE-INPUT (observed kinematics, as used by the review) | review §1 |
| O1 Newtonian timing-argument Kepler orbit (its effective mass 4.3e12 M☉ is an orbit parameter, not baryons; in a ΛCDM reading it would include a halo) | ADOPTED kinematic bracket from the review; not v3s's own two-body dynamics | review §1, C1 |
| O2 constant-velocity orbit | ILLUSTRATIVE bracket (review) | review §1 |
| t₀ = 13.8 Gyr (orbit clock and the "Hubble time") | LCDM-PROCESSED age, used only as the orbit's time origin, as in the review | review §1 |
| t_i ∈ {3, 6, 9} Gyr; window to r = 300 kpc; khronon at rest at t_i | ILLUSTRATIVE (review's case definition) | review §1 |
| G = 4.498502151469554e-6 kpc³ M☉⁻¹ Gyr⁻²; unit conversions | RAW constants | review code |
| grid, CIC, LU + Anderson solvers, leapfrog, J by lattice differences, B_out, q, dt, tol | METHOD (own code; every regulator varied: h ladder, N-dt, N-box, N-tol) | this lane |
| V-b test background (Kρ₀ = 0.5 Gyr⁻², x₀ ≈ 1, λ = 50 kpc) | METHOD / ILLUSTRATIVE (a code test, not physics input) | this lane |

## C. Not used

- **LCDM-PROCESSED:** only the 13.8 Gyr orbit clock above (time origin, as in the review); no halo model, no NFW, no
  ΛCDM-processed mass.
- **STANDARD-MOND-MACHINERY:** none in any verdict quantity. QUMOND appears only as the initial guess of the AQUAL
  iteration (the converged AQUAL solution does not depend on it) and inside the review's code reproduced in R0.
- **RAW survey data:** none; this is a theory-consistency lane on an illustrative system.
- No downloads, no PM cosmological simulation, nothing from the heavy queue.
