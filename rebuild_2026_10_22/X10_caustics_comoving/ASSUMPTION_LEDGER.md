# X10_caustics_comoving: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT, plus
FITTED (κ = ½, L★), ILLUSTRATIVE (round model values, not data), ADOPTED (a posed bracket, not derived) and METHOD (numerics).

## A. What the open items rest on

| ingredient | class | where | used here as |
|---|---|---|---|
| X8's self-consistent axisymmetric khronon-fluid solver (Q1 FEM + B2 particles, v3s switched static start) | METHOD (record code), validated by X8 R0, V-a1, V-a2, V-b | `X8_soft_side_caustics/x8_core.py`, `x8_validate_results.json` (72515e7e75) | imported read-only; reproduced first (R-X8a/b) |
| X8's v = 0 khronon start around moving galaxies | ADOPTED in X8 (the review's case definition) | X8 FROZEN §2 | the comparison bracket (R-X8b, D-X8) |
| O1's claim: every moving mass focuses the khronon wind into a line behind it | FRAMEWORK-NATIVE record (argument, not a solve) | `O1_ownership_action/README.md` §3(ii) | the hypothesis of (b) |
| Galilean covariance of the PN system; the static branch only in the khronon rest frame | FRAMEWORK-NATIVE (SYMPY, H5 A2) | `H5_v3s_lobe_growth/README.md` | justifies the boost (§2a) |
| capture law: a system moving at V through its khronon holds it only where 2GM_b/r ≥ V² | FRAMEWORK-NATIVE (U1 literal reading; H5 A2/A3: the stream feels φ_N of the baryons) | `U1_v3_dust_content/README.md` part (b); H5 A3 | the held extent (§2b), with the Plummer potential the code uses |
| Danby–Camm focusing (ρ/ρ∞ = b²/[R(2b − R)], focal distance b²V²/2GM) | FRAMEWORK-NATIVE record (H5 A5, residual 8e-15) | H5 README | hand estimates of §0 only |
| sign of ρ_τ is a Lagrangian invariant; the wind's charge is positive | FRAMEWORK-NATIVE (H5 A4) | H5 README | the (b) statistic uses stiff labels |

## B. This lane's ingredients

| ingredient | class | source |
|---|---|---|
| v3s action and weak-field PN system, switched stiffness, J_x (μ = x/(1+x)) | FRAMEWORK-NATIVE (adopted 2026-10-23; J_x POSTULATED; BS24 PN transcription PROVISIONAL) | V3_FULL_PICTURE §1, §2; X3; X8 §1 |
| AQUAL static equilibrium (not QUMOND) as the initial positions | FRAMEWORK-NATIVE (the theory's static limit) | V3_FULL_PICTURE §2; X8 A1(e) |
| a₀ footings 9.3603e-11 / 1.1312e-10 m/s² | FITTED (κ = ½) | doors BRIEF; X8 `x8_core.A0` |
| L★ = 21.682 / 22.849 pc, γ_L = K L★²/2 | FITTED | X3 D4; X8 |
| μ_K → 0, no BS dust | framework regime choice (the review's and X8's setting) | X8 ledger |
| MW 6e10 M☉, M31 1e11 M☉ baryons; Plummer ε = 20 kpc | LITERATURE-INPUT, ILLUSTRATIVE (as X8) | X8 ledger |
| M31 distance 780 kpc and radial velocity −110 km/s | LITERATURE-INPUT (observed kinematics, as X8) | X8 ledger |
| O1 Newtonian timing Kepler orbit (effective mass 4.3e12 M☉ is an orbit parameter; in a ΛCDM reading it would include a halo) | ADOPTED kinematic bracket (as X8) | X8 ledger |
| O2 constant-velocity orbit | ILLUSTRATIVE bracket (as X8) | X8 ledger |
| t₀ = 13.8 Gyr | LCDM-PROCESSED age, used only as the orbit clock (as X8) | X8 ledger |
| t_i ∈ {3, 6, 9} Gyr; window to r = 300 kpc | ILLUSTRATIVE (the review's / X8's case definition) | X8 FROZEN §2 |
| **the co-moving start**: held-by-g labels (e_g < 0 ≤ e_g′) boosted to V_g = ż_g(t_i); common and background labels at rest | ADOPTED (the coordinator's posed bracket: "held halo boosted, background at rest"); extent FRAMEWORK-NATIVE (capture law); no new constant | FROZEN §2 |
| straddle-label exclusion (J stencil across a velocity class boundary) | METHOD (constant-free, layer of thickness h) | FROZEN §3 |
| V-cm boost speeds 74.8 / 44.9 km/s and run time 15.167 Gyr | METHOD (the largest production boost per galaxy and the longest production window) | FROZEN §4 |
| D-ISO speeds 68.75 / 41.25 km/s | ILLUSTRATIVE (the O2 speeds) | FROZEN §6 |
| thresholds J_crit = 0.05, sustain 0.1 Gyr, convergence max(0.5, 0.1(t_c − t_i)), \|ΔS\| ≤ 0.05, V-a2 line 0.1, N-check 0.2 Gyr / 0.02 | reused from X8 unchanged | X8 FROZEN §4, §5, A2 |
| upstream line J_up > 0.5 | the coordinator's pre-declared line | lane brief |
| G = 4.498502151469554e-6 kpc³ M☉⁻¹ Gyr⁻²; unit conversions | RAW constants (as X8) | `x8_core.py` |
| grid, deposit, solvers, integrator, dt, tol, B_out, q, h ladder {20, 10, 5} | METHOD (X8's, each varied by X8's h ladder and N-checks) | X8 A1 |

## C. Not used

- **LCDM-PROCESSED:** only the 13.8 Gyr orbit clock (as X8); no halo model, no NFW, no ΛCDM-processed mass.
- **STANDARD-MOND-MACHINERY:** none in any verdict quantity. QUMOND appears only as the initial guess of X8's AQUAL Newton
  iteration (the converged AQUAL state does not depend on it).
- **RAW survey data:** none; this is a theory-consistency lane on an illustrative system.
- No new fitted constant, no smoothing function, no knob scan. No downloads, no PM simulation, nothing from the heavy queue.
