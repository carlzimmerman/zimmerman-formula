# H4_v3_saddle_stability: is v3's khronon/dust pair healthy where the phantom density D·P < 0? FROZEN CRITERIA

Written and committed before the lane script exists and before any script has produced a number. Rules:
`rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md` + `BRIEF_E_AUDIT.md`. κ = ½ is FITTED. Footings
canonical a₀ = 9.36e-11 m/s² and alt a₀ = 1.13e-10 m/s², never pooled. No dark-matter particle. Never "theory closed";
nothing here says the data favour the framework. Verdict words per system: HEALTHY / BOUNDED INSTABILITY (with e-folds) /
ILL-POSED. The assumption ledger is `ASSUMPTION_LEDGER.md` (committed with this file).

## 0. What was read before freezing, and the not-blind statement

Read: `rebuild_2026_10_22/P3_v3_strong_field/` (README, FROZEN_CRITERIA + A1/A2, script Part E, results json E4 rows);
`covariant_push_2026_10_22/C5_health/README.md`, `C8_instantaneous/README.md`, `C4_khronon_parent/README.md`,
`THEORY_V3_DRAFT.md` §1 and the P3/H4 row; `rebuild_2026_10_22/I1_gammaL_causality/README.md`;
`real_research/bs_khronon_2026/BSK1_moving_source_gate.py` (M1–M5: BS24's PN system and the phantom-fluid WKB
dispersion); `deepseek_push/DS_FINAL_2026_10_21/A38_saddle_resolution/report.md` (third AQUAL saddle solver) and
`A23_no_efe_saddle/report.md` (EFE sweep); `argon_push/AG7_saddle_trough_preflight/README.md`;
`rebuild_2026_10_22/S4_v3_muK_clusters/README.md` (the μ_K² term and its guard).

**Not blind.** Before this file I did hand work (nothing run, nothing committed):
- Writing v3's PN Lagrangian as BS24's PN system with the J term replaced by C4's P sector, the linear system
  (Poisson + P equation + khronon continuity + Bernoulli) gives by hand ω² = ρ_τ [k²/χ(k) − K],
  χ = k²/(K M_θ + γ_L k²) + μ_K²/K, ρ_τ = D·P − μ_K²Ξ/K (K = 4πG). At μ_K = 0 this is
  ω² = K ρ_τ (M_θ − 1 + L★²k²/2). So where ρ_τ < 0 the γ_L branch looks UV-unbounded (Γ ∝ k), and at γ_L = 0 it reduces
  to BSK1 M4 (bounded). P3's E1/E4 (decoupling limit) is the same expression without the self-gravity term −Kρ_τ.
- Hand sizes (MW–M31 saddle, |ρ| ≈ 0.24 √(GMa₀)/(Gd²) from A38): γ_L branch 1 e-fold per Hubble time at λ ~ 0.7 kpc;
  hundreds of e-folds at λ = 1 pc. In the screened linear regime, D·P is a Yukawa-smoothed (range L★/√2) copy of the
  positive mass density, so the Solar System looks positive. In the linear EFE regime the AQUAL phantom of a point mass has
  negative equatorial lobes. These estimates set no threshold below.

## 1. The theory tested (v3) and the questions

v3 (THEORY_V3_DRAFT §1; C5's Lagrangian at β = η = γ_F = 0, ξ = 1):
L/√−g = R/(4K) + P^μA_μ − W(K|P|) − (γ_L/2)(D·P)² + μ_K²(Q−1)²/(2K), K = 4πG, W′(u) = u a₀/(K(a₀ − u)), γ_L = K L★²/2,
P ⊥ n, n_μ = −∂_μτ/Q. Static limit: AQUAL with μ = x/(1+x) (C4 K1–K3, J = J_x).

Q1. The pair's local dispersion relation including every term that can matter at high k (first-order background-gradient
term, γ_L, BS dust kinetic/pressure terms, μ_K², J_x's M_L, M_T, the self-gravity of the perturbation); bounded or
UV-unbounded where ρ_τ < 0.
Q2. Where ρ_τ < 0 in v3's AQUAL static solution for realistic systems, and how deep.
Q3. Growth rate and e-folds per region; verdict per system and overall.
Q4. Attempts to break the answer (second route, frame change, P3 sign convention, sign-flip mutate).

Weak-field PN Lagrangian used (BS24 PN form, J term → C4's P sector; τ = t + σ, c = 1):
L = −|∇φ|²/(2K) − ρ_m φ + P·∇Ξ − W(K|P|) − (γ_L/2)(∇·P)² + μ_K² Ξ²/(2K), Ξ = φ − σ̇ + |∇σ|²/2.
Its use is checked by A1 (static limit and the khronon continuity identity) and A2/A3 (covariant leaf divergence and clock
term at the order used).

## 2. Checks (script prints `ID PASS/FAIL value threshold`; exit 0 iff all PASS)

**Part A (sympy, exact; residuals must be identically 0):**
- A1: (i) the σ Euler–Lagrange expression of the PN Lagrangian equals −[∂_tρ_τ + ∇·(ρ_τ v_τ)] with ρ_τ = ∇·P − μ_K²Ξ/K,
  v_τ = −∇σ; (ii) static, γ_L = 0, μ_K = 0: eliminating P (P ∥ ∇φ, |∇φ| = K W′(u)) gives ∇·[μ(|∇φ|/a₀)∇φ] = Kρ_m with
  μ = x/(1+x).
- A2 (covariant): on Minkowski with τ = t + εσ(t,x), P_μ ⊥ n with spatial part P0_i(x) + εp_i(t,x): the identity
  D·P = ∇_μP^μ − P^μA_μ holds, and the O(ε) part of D·P has no σ-dependent term (the tilt term −P0·∇σ̇ from ∂_tP^0 cancels
  the one in P·A).
- A3 (covariant decoupling, plane-symmetric P0_z(z) on Minkowski): the O(ε²) part of P^μA_μ equals −½(∂_zP0_z)(∂_zσ)²
  plus total derivatives; and integrating p_z out at leading WKB gives the kinetic coefficient χ = k²/(K M_θ + γ_L k²)
  (P3 E1).
- A4 (PN linear system: Poisson, P equation with the W Hessian H = K[M_T I + (M_L − M_T)P̂P̂] along k, khronon continuity,
  Bernoulli; WKB, frozen background): det = 0 gives ω² = ρ_τ (k²/χ − K) exactly; with γ_L = 0 it reproduces BSK1 M4
  (ω² = Kρ_τ(k² f_θ − μ_K²)/(k²(1 − f_θ) + μ_K²)) under f_θ = 1 − 1/M_θ; without the Poisson feedback it reproduces P3's
  decoupled ω² = ρ_τ k²/χ.
- A5 (J_x): 1 − μ = 1/(1+x) and 1 − d(xμ)/dx = 1/(1+x)², i.e. M_T = 1 + x, M_L = (1+x)² (C5).
- A6 (frame): about a background moving uniformly at V (σ0 = −V·x + V²t/2) the dispersion is (ω − k·V)² = ρ_τ(k²/χ − K):
  growth rates are frame-independent.

**Part B (well-posedness):**
- B1 (sympy): lim_{k→∞} ω²/k² is computed. If it equals γ_L ρ_τ/(1 + μ_K²γ_L/K) (≠ 0), the ρ_τ < 0 branch is
  **UV-unbounded** (Γ ∝ k). The γ_L = 0 limit of ω² as k → ∞ is computed and must be finite (bounded branch). Scored:
  both limits derived (finite symbolic expressions).
- B2 (numeric, variable coefficients, no WKB): 1D periodic slab, ρ_τ(x) = ρ̄ + Δ cos(2πx/L) negative over part of the
  slab, constant M, Fourier–Galerkin generalised eigenproblem from A4's operators. Ladder N = 64, 128, 256, 512.
  PASS iff (a) with γ_L > 0 the largest growth rate grows with resolution, Γ_max(512)/Γ_max(256) ∈ [1.8, 2.2]
  (Hadamard signature), and (b) with γ_L = 0 it converges: Γ_max(512)/Γ_max(256) ≤ 1.01 and
  |Γ_max(512)/√(K(M−1)|min ρ_τ|) − 1| ≤ 0.01.
- B3 (P3 sign convention): with P3's own E4 inputs (json G_hat = Kρ_τ, Z_hat = Kχ, k), this lane's dispersion reproduces
  P3's c_π on every row where the self-gravity term is negligible (G_hat/k² ≤ 1e-3 G_hat/Z_hat): |c_π/c_π(P3) − 1| ≤ 1e-3,
  both footings, all L★. The rows where it is not negligible are reported with the correction factor
  √(1 − Z_hat/k²), not scored.

**Part C (where ρ_τ < 0, and how deep):**
- C1 (AQUAL solver validation, this lane's own axisymmetric solver): (i) single deep-MOND Plummer lens:
  |4πr²ρ_ph/(√(GMa₀)/G) − 1| ≤ 0.02 for r ∈ [0.2, 2] (units of the box scale), away from the core;
  (ii) isolated equal deep pair: mid-plane C(0.2d) = ρ_ph/(√(GMa₀)/(Gd²)) within 1.5 % of A38's −0.2413;
  (iii) A23's EFE sweep (deep, equal pair, uniform field along the axis, full domain): C(0.2d) within 0.02 (absolute) of
  −0.0315 at e = 0.3, and C(0.2d) > 0 at e = 0.68.
- C2 (every declared system × footing solved, full μ = x/(1+x)): the negative region R₋ = {ρ_ph + f ρ̄_K < 0} is
  mapped; its volume and its median |ρ| change by ≤ 10 % between the two declared resolutions.
- C3 (screened Solar System, linear response about the Galactic P background): D·P > 0 at every sample point (Sun–Earth
  and Earth–Moon Newtonian saddles, 1 AU, 100 AU, 0.1 pc), both footings, every L★, using a lower bound on the
  anisotropic Yukawa kernel (C3 is PASS = "screening removes the region").

**Part D:** D1: the verdict table is computed and every number in it is finite.

## 3. Declared systems (ILLUSTRATIVE inputs; verdict margins are insensitive to factor-2 changes)

Baryonic masses (M☉), separations, Plummer scales:
- S1 MW–M31: 6.0e10 (3 kpc) + 1.0e11 (4 kpc), d = 780 kpc; external field along the axis g_e/a₀ ∈ {0, 0.01}.
- S2 LMC–MW: 6.0e10 (3 kpc) + 3.0e9 (1.5 kpc), d = 50 kpc; g_e = 0.
- S3 galaxy pair: 5.0e10 (3 kpc) + 5.0e10 (3 kpc), d = 300 kpc; g_e/a₀ ∈ {0, 0.01}.
- S4 cluster pair: 1.5e14 (300 kpc) + 1.0e14 (250 kpc), d = 3 Mpc; g_e/a₀ ∈ {0, 0.01}.
- S5 disc galaxies (axisymmetric, exponential disc, sech² vertical): MW-like M_d = 5e10, R_d = 2.6 kpc, h_z = 0.3 kpc,
  Plummer bulge 1e10 (0.6 kpc); dwarf disc M_d = 1e9, R_d = 1.5 kpc, h_z = 0.2 kpc; g_e/a₀ ∈ {0, 0.01} along the
  symmetry axis. The question is whether ρ_ph < 0 off-plane.
- S6 single galaxy in an external field (EFE lobes): 6.0e10 (3 kpc), g_e/a₀ = 0.01.
- S7 Solar System (Sun–Galaxy, Earth–Moon): screened linear response (C3), Galactic background u at the Sun from the
  record's x_e = 1.15–2.6 range (C5/D7d).
g_e/a₀ = 0.01 is the record's cosmic-mean scale (A23: "30× below the cosmic mean" for 3e-4); ILLUSTRATIVE.

Dust offset: ρ_τ = ρ_ph + f ρ̄_K, ρ̄_K = Ω_K·3H₀²/(8πG) with Ω_K = 0.26 (BS25 via C4, illustrative) and H₀ = 68.6
(native upper end, C2/A78; the larger H₀ shrinks R₋, conservative); f = 0 (primary) and f = 3 (dust-conditional check,
a local overdensity of 3). The hydrostatic μ_K² dust is set to 0 in the maps (μ_K → 0, the regime of every v3 galaxy tile;
S4: μ_K ≥ 0.1 Mpc⁻¹ fails the isolated-galaxy guard); its size at μ_K = 0.1 Mpc⁻¹ and at BS's cap is reported as an
estimate only.

L★ ∈ {floor 21.7 pc (canonical) / 22.9 pc (alt), 24 pc, 90 pc}. Region lifetimes T = min(T_H, ℓ₋/v) with T_H = 13.8 Gyr,
ℓ₋ the extent of R₋, and v = 110 (S1), 320 (S2), 150 (S3), 1000 (S4) km/s; S5, S6: T = 10 Gyr. All ILLUSTRATIVE.

Reported per region: median and max |ρ_τ| over R₋ (max excludes cells within 2 grid cells of a null point), the field
x = |∇Φ|/a₀ there, the bounded-branch rate Γ_b = √(K|ρ_τ|((1+x)² − 1)) (γ_L → 0, with self-gravity), the γ_L-branch rate
Γ(k) = √(K|ρ_τ|((1+x)² − 1 + L★²k²/2)) at λ = L★, 1 pc, 1 AU, the e-folds Γ·T, and λ₁ (one e-fold in T).

## 4. Verdict rules (per system; overall)

- **ILL-POSED** iff (a) R₋ is non-empty with linear extent ≥ 10 × 90 pc in the f = 0 map, and (b) B1 gives a non-zero
  UV limit γ_L ρ_τ/(1 + μ_K²γ_L/K) and B2 passes (resolution-growing rate). Reported with "(dust-conditional)" if R₋
  disappears in the f = 3 map.
- **BOUNDED INSTABILITY** iff R₋ is non-empty but the UV limit is finite (only possible if B1 finds no γ_L k² term);
  reported with e-folds Γ_max·T.
- **HEALTHY** iff R₋ is empty in the f = 0 map for both footings (for S7: iff C3 passes).
- **Overall:** ILL-POSED if any declared system is ILL-POSED; HEALTHY iff all are HEALTHY; otherwise BOUNDED INSTABILITY.
- Reading (not a verdict line): the e-folds of the γ_L → 0 (pure BS/AQUAL) bounded branch per region, i.e. what the
  saddles would do without the stiffness; and the EFT-cutoff reading: the cutoff wavelength that would be needed to keep
  < 1 e-fold in T (λ₁) compared with the AU scales where the same γ_L term must act for Solar-System screening.
- Nonlinear saturation: reported as a reading (what grows, what the action offers to stop it); it does not change a
  linear verdict.

## 5. Mutation

`H4_MUTATE=1` flips the sign of the first-order (background-gradient) term: the khronon continuity coefficient ρ_τ → −ρ_τ
in the linear system. A4 and B3 must FAIL; the verdicts are recomputed and must swap (saddles healthy, Solar System
ill-posed). Outputs: `h4_v3_saddle_stability_MUTATE.out`, `h4_v3_saddle_stability_results_MUTATE.json`.

## 6. Compute

`OMP_NUM_THREADS=1 nice -n 15`, single thread, < 1 GB RSS, minutes; no downloads; no PM runs; nothing from the heavy
queue touched.
