# C1_aest_embedding — FROZEN CRITERIA (written before any script or number)

Question: is the screened theory's static sector (AQUAL μ = x/(1+x) + stiffness γ = K L★²/2 + clock term +
cold medium) a limit of an AeST-type covariant action? If yes, which free function F, which parameters, which
field map; if no, the exact obstruction.

## Record checked before freezing

- `covariant_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`.
- Target: A33 `MASTER_ACTION.md` §1–3 (action, (L), (P), `γ_F = γ_L` status "C"), DSF-21 `THEORY.md` §1–2,
  E2 README (PAPER49 Lagrangian at γ = 0: `−|∇Φ − KP|²/2K − ρΦ − W_rem(u)`, AQUAL μ = x/(1+x); transverse
  fraction of h = 0.2185 at r_M in `e2_field_equation_results.json`), D7d README + json (static (L)/(P) with L★,
  planet bounds and unscreened `no_turnoff` anomalies), A68 (5 DOF), D9 MAP, D9b, E5 (NG1, NG2, D-T hypotheses).
- AeST in the record: `real_research/bridge1_aest_equations.md` (Eq. 5 action and the MOND-limit coefficient,
  stated there as transcribed from the arXiv LaTeX `newRMONDLett.tex` on 2026-08-14; **the LaTeX itself is not on
  disk** — searched the repo and the filesystem for `newRMONDLett*`), `real_research/THE_NEXT_CALCULATION_aest_quasistatic.md`,
  `real_research/AEST_MASS_SCALE_two_doors.md`, `hy4_push/H001_zimmerman_aest_action.py` (an earlier "AeST with
  fixed free function" attempt for the n = 2 law, without the clock/J term or stiffness),
  `opus_48_extended_research/reviews/aest_embedding/` (2026-06 notes on a₀ into AeST). None of these derives the
  static limit of AeST against the A33/PAPER49 action with stiffness. That comparison is new here.
- External input (literature, via the record's transcription, not verified against a file on disk): AeST action
  Skordis & Złośnik, PRL 127, 161302 (2021), arXiv:2007.00082, Eq. (5):
  `S = ∫ √−g/(16πG̃) [R − (K_B/2)F^{μν}F_{μν} + 2(2−K_B)J^μ∇_μφ − (2−K_B)Y − F(Y,Q) − λ(A^μA_μ+1)] + S_m[g]`,
  `J^μ = A^ν∇_νA^μ`, `Y = q^{μν}∇_μφ∇_νφ`, `q^{μν} = g^{μν}+A^μA^ν`, `Q = A^μ∇_μφ`; MOND limit
  `F(Y,Q₀)/(2−K_B) → 2λ_s/(3(1+λ_s)a₀) Y^{3/2}`; cosmological part `−K(Q)` with `K ⊃ K₂(Q−Q₀)²`.
  The definition `J^μ = A^ν∇_νA^μ` (aether acceleration) is from the literature, flagged "not verified on disk".

## Method (fixed now)

Static weak field, Newtonian gauge `g₀₀ = −(1+2εψ)`, `g_ij = (1−2εϕ)δ_ij`; `φ = Q₀t + εχ(x)`; `A_i = εa_i(x)`, `A₀`
from the exact unit constraint. sympy computes √−g R, F², J^μ∇_μφ, Y, Q exactly and truncates at O(ε²); `F(Y,Q)` is
kept as `(2−K_B)𝒥(Y) − K₂(Q−Q₀)²` with 𝒥 an abstract function (no Λ, static minimum `I₀ → 0`).

## Checks (pass lines)

- **K1 (static limit).** The Euler–Lagrange equations (ψ, ϕ, χ, a_x, a_y, a_z) of the truncated AeST Lagrangian
  equal those of the claimed reduced form `L_A` (to be printed) identically. PASS: every residual simplifies to 0.
- **K2 (AQUAL).** There is an explicit 𝒥 for which the algebraic (curl-stiffness → 0) static limit is
  `∇·[μ(|∇Ψ|/a₀)∇Ψ] = 4πGρ` with `μ = x/(1+x)` exactly. PASS: symbolic residual 0, and the 𝒥 small-Y limit
  equals the record's AeST coefficient `2λ_s/(3(1+λ_s)a₀)` at a stated λ_s (residual 0).
- **K3 (map to A33 static).** With the field map `KP_i = ∂_iχ + Q₀a_i`, `Φ = Ψ`, the reduced AeST Lagrangian minus the
  A33/PAPER49 static Lagrangian (with its γ_L and γ_F set to whatever AeST supplies) is 0. PASS: residual 0;
  the supplied γ_L and γ_F are printed.
- **K4 (clock coefficient).** The clock coefficient ξ implied by AeST's ratio of the J·∇φ and Y terms. PASS iff
  ξ = 1 exactly (symbolic).
- **K5 (longitudinal stiffness theorem).** In Fourier space, with the most general weak-field quadratic aether
  gradient terms (`K_B`, and Einstein-aether-type `c₁, c₂, c₃`) and χ entering only through first derivatives,
  the effective static kernel of the longitudinal part of `KP` has no k² term. PASS iff the k² coefficient of the
  longitudinal kernel is exactly 0 for all (c₁, c₂, c₃, K_B), and the transverse k² coefficient is nonzero.
  (If K5 FAILS, AeST's class can supply γ_L.)
- **K6 (consequence, record numbers).** If γ_L,eff = 0: a radial P has F_ij ≡ 0, so the isolated Sun obeys the
  unstiffened law. Compute the anomalous sunward acceleration at Earth, Mars, Saturn on both footings and compare
  with D7d's `no_turnoff` values. PASS iff relative agreement < 1e-3 (reported with the ratio to D7d's planet bounds).
- **K7 (hypersurface-orthogonal aether).** With `a_i = ∂_i α` (khronometric AeST) the anomalous field V is
  curl-free, while the AQUAL solution's V = (1−μ)∇Φ is not, for a generic non-symmetric test field. PASS iff
  `|∇×V_AQUAL| > 0` at a test point (so the khronometric version is NOT AQUAL off symmetry); E2's transverse
  fraction is quoted from its json.
- **K8 (static field content).** The static quadratic form in (χ, a_L, a_T1, a_T2) at fixed (ψ, V) has exactly one
  zero direction (χ ↔ a_L), so the static content is 3 components, equal to A33's P_i. PASS iff nullity = 1.

`--mutate` (env `C1_MUTATE=1`): the J·∇φ coefficient 2(2−K_B) → (2−K_B) and a term −(γ_L/2)(∇²χ)² is added. K3/K4
must FAIL (ξ ≠ 1) and K5 must FAIL (longitudinal k² term appears). Outputs `*_MUTATE.out`, `*_results_MUTATE.json`.

## Verdict lines (fixed now)

- **EMBEDS**: K1–K4 PASS and K5 FAILS (AeST's own class supplies γ_L).
- **EMBEDS WITH EXTRA TERM**: K1–K4 PASS, K5 PASS (γ_L,eff = 0): the missing term is named, its coefficient counted,
  and whether it lies in AeST's class is stated.
- **NO-GO**: K2 or K3 FAILS for every 𝒥 (no AeST static limit is AQUAL μ = x/(1+x)); the obstruction is stated.

No-go audit (NG1, NG2, D-T) is a hypothesis table in the README, each line tagged DERIVED / OPEN; no check line.
Rules: κ = ½ FITTED; footings 9.36e-11 / 1.13e-10 m/s² never pooled; no DM particle; not "theory closed"; nothing
here says the data favour the framework. Runs `OMP_NUM_THREADS=1 nice -n 10`, < 1 GB RSS, single thread.
