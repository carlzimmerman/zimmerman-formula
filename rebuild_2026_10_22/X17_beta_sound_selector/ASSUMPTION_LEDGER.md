# X17_beta_sound_selector: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT, plus
FITTED (κ = ½, L★, the dust abundance), ILLUSTRATIVE (round model values, not data), ADOPTED (a posed choice, not derived)
and METHOD.

## A. What the question rests on (the record)

| ingredient | class | where | used here as |
|---|---|---|---|
| v3s action, static limit AQUAL with the simple μ; PN Lagrangian (X3 L1 in 3D + C1, X15 `L3`) | FRAMEWORK-NATIVE (J_x and stiffness POSTULATED; K(Q) LITERATURE-INPUT, BS24) | V3_FULL_PICTURE §1–2; X15 script L609–628 | the theory under test; H-PN |
| C1 operator −βK²/(4K), B = βc²/(2+3β), window [β_min(foot), β_max(μ_K)] | FRAMEWORK-NATIVE record (X14 SYMPY/NUM, X15 S0-2/S0-3; the upper edge rests on C5's IR-band estimate) | X14 JSON `classes.C1.FT_window`; X15 JSON `S0_2` | graded β set; S0-1, S0-2 |
| khronon linear dispersion (ρ_τ + Bk²/K)(k²/χ − K), χ = k²/(KM_θ + Θγ_Lk²) + μ_K²/K; M_θ ∈ [1 + x, (1 + x)²] | FRAMEWORK-NATIVE (SYMPY record: X3 B1-S, X14 C1-R, X15 S0-3) | X14 `disp` (copied) | S0-3, H-RESP, G-CA0, G-DISP |
| c_A = c√(β(M_θ − 1)/(2+3β)) and its values (fold radii, cluster point) | FRAMEWORK-NATIVE record (NUM) | X15 JSON `T3a_mach`, `T3c_cherenkov` | S0-1, S0-2 |
| X15 step-3b moving-galaxy estimate (indicial p₁, δ ln g formula), Cherenkov drag form | FRAMEWORK-NATIVE record, labelled ESTIMATE there; drag form LITERATURE-INPUT [mem] (Ostriker-type) | X15 script L655–725 | ΔA_bulk, drag (reported) |
| X15's moving-galaxy subsonic rotation-curve maximum | FRAMEWORK-NATIVE record (ESTIMATE) | X15 JSON `T3b_rotation` | isolated-galaxy change for moving galaxies (verdict rule 3 only) |
| μ-pincer theorem (relation, horns, K-independent Part F) | FRAMEWORK-NATIVE record (sympy + numerics, 18/18) | STANDING.md L296; condensate_pincer_2026 VERDICT + script | P0 scope statement |
| F3/X4 growth ODE (two fluids, J_x kernel, growing-dust start at a_i), background A, R(0) values | FRAMEWORK-NATIVE record (ODE is an upper-bound convention, X4) + LCDM-PROCESSED background parameters (C2b refit, as X4) | `x4_growth.py`, X4 JSON `ode`; F3 JSON K2 | S0-5, step 3 baseline |
| X7 tercile A_MID (CAL) and edges; X2 tercile median MGAS500; X13 selection-corrected A_MID, Z | SURVEY-CALIBRATION (KiDS shear, eRASS1 MGAS500) processed by FRAMEWORK-NATIVE law predictions; read only | X7, X2, X13 JSON | S0-4; E_T in the verdict; E3 masses |
| F1 sample-median enclosed gas at 0.5 and 1.0 Mpc; stellar fraction f★ = 0.20 (0.10, 0.30 variants) | SURVEY-CALIBRATION (eRASS1 gas, F1's profile shapes) + ADOPTED (f★, as F1) | F1 JSON `dust`; F1 `predict()` | E3 enclosed baryons |
| S4's static μ_K branch and its M^{1/6} onset ordering | FRAMEWORK-NATIVE record (LEAN `onset_exponent`) | V3_FULL_PICTURE §4.4 | step 4 (reported) |

## B. This lane's ingredients

| ingredient | class | source |
|---|---|---|
| a₀ = 9.3603e-11 / 1.1312e-10 m/s² | FITTED (κ = ½) | doors BRIEF |
| L★ = 21.682 / 22.849 pc (only in S0-3's stiffness symbol and the FRW stiffness-only speed) | FITTED | X3 D4 via X14/X15 |
| native H₀ = 67.2 km/s/Mpc for β_max and drag times; background A's h for growth and H(z) | FRAMEWORK-NATIVE (as X14/X15) / as X4 | X15, X4 |
| covariant check: static diagonal metric, τ = t; ADM spherical ansatz (N, N^r, A, Bf); unitary-gauge khronon equation implied by diffeomorphism invariance | METHOD (standard ADM algebra) | H-COV |
| uniform held background, WKB response to a moving source (valid for structure much smaller than the host scale) | METHOD (ADOPTED approximation) | H-RESP, ΔA_mem |
| spherical point-mass law at the enclosed baryon mass for x, v_c and the local phantom | ADOPTED (as X14/X15's `aqual_point`) | E2, E3 |
| E3 enclosed mass: self-similar scaling of F1's sample-median gas by MGAS500_T/MGAS500_med; log-log extrapolation to 0.3 Mpc; bracket ×{0.5, 2} | ADOPTED | §2 |
| ΔA ≡ δ ln g for the lensing amplitude in MID (lensing sees ψ = φ in v3) | ADOPTED | ΔA_bulk |
| members: f_mem = f★/(1+f★) (all stars moving, upper side); Maxwellian with σ_1D = v_c/√2; sub-phantom 1/m with m ∈ {x, 2x + x²} | ADOPTED / ILLUSTRATIVE | ΔA_mem |
| speeds w ∈ {369, 600, 1000} km/s; R_h ∈ {1, 10} Mpc; galaxy masses {1e9, 1e10, 6e10, 2e11} M☉; member mass 6e10 M☉; lnΛ = ln 100 | ILLUSTRATIVE (X15's lists where they exist) | §2, §5 |
| baryon sound speed at z = 1100: T = 2.7255 K × 1101, μ = 1.22, γ = 5/3 | RAW constants + ILLUSTRATIVE composition | E1 |
| FRW sub-horizon limit of the C1 current: δ̇ = −(1 + Bk_p²/(Kρ̄_τ))θ, Hubble drag on θ; O(β) change of G_cos and O((aH/k)²) terms dropped | METHOD (ADOPTED; the static-background limit is checked by G-DISP) | step 3 |
| growth classes' [0.5, 2] power margin | FRAMEWORK-NATIVE record convention (X4 F) | §6 |
| projectable-Hořava IR scalar: c_s² = −(λ−1)/(3λ−1) for λ > 1 (equals −B/c² at λ = 1 + β) | LITERATURE-INPUT [mem], PROVISIONAL; reported cross-check only | — |
| G, c, M☉, k_B, m_p, pc | RAW constants | CODATA / IAU values in the script |

## C. Not used

- No shear is recomputed; no survey catalogue is opened (only committed JSON of X2, X7, X13, F1).
- No QUMOND, no EFE formula (STANDARD-MOND-MACHINERY); the law and its phantom are the theory's own static limit.
- No new fitted constant; β is never scanned outside X14/X15's window; no knob scan; no simulation; no downloads; no edits
  outside this lane. Record scripts are run only as patched copies in a temporary directory (X15), or their functions are
  copied with provenance (X14 `disp`, X15 `L3`/`aqual_point`/`p1_of`, F3/X4 ODE).
