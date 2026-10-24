# X12_caustics_3d: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT, plus
FITTED (κ = ½, L★), ILLUSTRATIVE (round model values, not data), ADOPTED (a posed bracket, not derived) and METHOD (numerics).

## A. What the open items rest on

| ingredient | class | where | used here as |
|---|---|---|---|
| X8's axisymmetric self-consistent khronon-fluid solver (Q1 FEM + B2 ring particles, v3s switched static start) | METHOD (record code), validated by X8 R0, V-a1, V-a2, V-b | `X8_soft_side_caustics/x8_core.py`, `x8_validate_results.json` | imported read-only by R-X10's 2D runs; the 2D reference |
| X10's co-moving start (held labels e_g < 0 ≤ e_g′ boosted with their galaxy, the rest at rest) and straddle exclusion | ADOPTED bracket (X10 §2, §3); extent FRAMEWORK-NATIVE (U1 capture law) | `X10_caustics_comoving/FROZEN_CRITERIA.md`, `x10_run.py` | unchanged, in 3D |
| X10's results: O2 soft folds (axis collapses and in-plane folds), MW wake line, D-ISO | record (2D) | `X10_caustics_comoving/README.md`, `runs/`, `x10_validate_results.json` | the 2D references of X-ISO, X-B0 and R-X10 |
| O1's claim: every moving mass focuses the khronon wind into a line behind it | FRAMEWORK-NATIVE record (argument) | `O1_ownership_action/README.md` §3(ii) | the hypothesis of (a) |
| Galilean covariance of the PN system | FRAMEWORK-NATIVE (SYMPY, H5 A2) | `H5_v3s_lobe_growth/README.md` | the boost; V-cm |
| Danby–Camm focusing (focal distance b²V²/2GM) | FRAMEWORK-NATIVE record (H5 A5) | H5 README | hand estimates of §0 only |
| the sign of ρ_τ is a Lagrangian invariant; the wind's charge is positive | FRAMEWORK-NATIVE (H5 A4) | H5 README | wake statistic on stiff labels; soft set by sign |
| "the axis collapse / axis focus may be an artefact of axisymmetry" | the open question (X8, X10 "what this does not show") | X8, X10 READMEs; V3_FULL_PICTURE §6 | tested here |

## B. This lane's ingredients

| ingredient | class | source |
|---|---|---|
| v3s action and weak-field PN system, switched stiffness, J_x (μ = x/(1+x)) | FRAMEWORK-NATIVE (J_x POSTULATED; BS24 PN transcription PROVISIONAL) | V3_FULL_PICTURE §1, §2; X3; X8 §1 |
| AQUAL static equilibrium (not QUMOND) as the initial state, with the stiffness outer loop | FRAMEWORK-NATIVE (the theory's static limit) | V3_FULL_PICTURE §2; X8 A1(e) |
| a₀ footings 9.3603e-11 / 1.1312e-10 m/s² | FITTED (κ = ½) | doors BRIEF; `x8_core.A0` |
| L★ = 21.682 / 22.849 pc, γ_L = K L★²/2 | FITTED | X3 D4; X8 |
| μ_K → 0, no BS dust | framework regime choice (as X8, X10) | X8 ledger |
| MW 6e10 M☉, M31 1e11 M☉ baryons; Plummer ε = 20 kpc | LITERATURE-INPUT, ILLUSTRATIVE (as X8) | X8 ledger |
| M31 distance 780 kpc and radial velocity −110 km/s (O2's anchor) | LITERATURE-INPUT (observed kinematics, as X8) | X8 ledger |
| O2 constant-velocity orbit, t_i = 3 Gyr, window to d = 300 kpc | ILLUSTRATIVE bracket (X8's case definition; t_i chosen per FROZEN §0) | X8 FROZEN §2 |
| t₀ = 13.8 Gyr | LCDM-PROCESSED age, used only as the orbit clock (as X8) | X8 ledger |
| impact parameters b ∈ {0, 50, 150} kpc | ILLUSTRATIVE (the coordinator's suggested values; case definitions, not fitted) | lane brief; FROZEN §2 |
| straight parallel tracks (no deflection by the impact) | ADOPTED kinematic bracket (the baryons' orbits are prescribed, as X8/X10) | FROZEN §2 |
| isolated-mass speed 68.75 km/s | ILLUSTRATIVE (MW's O2 speed; X10 D-ISO) | X10 FROZEN §6 |
| wake window W_a = 9.067 Gyr | ADOPTED (the window of X10's PRESENT cells; chosen knowing X10, disclosed) | FROZEN §0, §5a |
| thresholds J_crit = 0.05, sustain 0.1 Gyr, convergence max(0.5, 0.1(t_c − t_i)), \|ΔS\| ≤ 0.05, V-a1 1e-4 / 1e-2 kpc, V-cm 0.1, N-check 0.2 Gyr / 0.02, J_up > 0.5, axis zone R⊥ ≤ 30 kpc, 2ε…1000 kpc | reused from X8 / X10 unchanged | X8 §4, §5, A2; X10 §4, §5 |
| X10's convergence tolerance used as the 2D–3D agreement line (X-ISO, X-B0) | reused, no new constant | FROZEN §4 |
| mirror symmetry y → −y (E) and x, y → −x, −y (W, V-a1, V-cm) | exact symmetries of the posed configurations; METHOD (half / quarter domain) | FROZEN §0, §3 |
| 3D discretisation: variational FD (cell-averaged squared edge gradient), TSC particles, fast diagonalisation, Anderson hold law, KDK + adaptive dt | METHOD (X8 A1's design in 3D; validated by V-a1, V-cm, X-ISO, X-B0) | FROZEN §3 |
| grid regulators: h ∈ {20, 15, 10} kpc, q = 1.25, B_out = 5 Mpc, fine-zone bounds, tol 1e-7, dt factor 0.15 | METHOD (varied by the h ladder and the N-checks) | FROZEN §3, §4 |
| G = 4.498502151469554e-6 kpc³ M☉⁻¹ Gyr⁻²; unit conversions | RAW constants (as X8) | `x8_core.py` |

## C. Not used

- **LCDM-PROCESSED:** only the 13.8 Gyr orbit clock (as X8); no halo model, no NFW, no ΛCDM-processed mass.
- **STANDARD-MOND-MACHINERY:** none in any verdict quantity. QUMOND appears only as the initial guess of the AQUAL Newton
  iteration (the converged AQUAL state does not depend on it).
- **SURVEY-CALIBRATION / RAW survey data:** none; this is a theory-consistency lane on an illustrative system.
- No new fitted constant, no smoothing function, no knob scan. No downloads, no PM simulation, nothing from the heavy queue.
