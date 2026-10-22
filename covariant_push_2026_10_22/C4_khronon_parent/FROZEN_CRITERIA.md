# C4_khronon_parent — FROZEN CRITERIA (written before any script or number)

Question: is the Blanchet–Skordis Khronon theory a covariant parent of the screened theory's static sector
(AQUAL μ = x/(1+x), clock term coefficient 1, longitudinal stiffness γ_L = K L★²/2), and does it escape C1's
khronometric (curl-free) obstruction? What sets its dust abundance?

## Record checked before freezing

- `covariant_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`.
- C1 README/criteria (AeST verdict EMBEDS WITH EXTRA TERM; khronometric AeST gives curl-free V, not AQUAL; planet
  ratios in `c1_aest_embedding_results.json` K6), C2 (AeST dust abundance = Q₀I₀, I₀ free), C3 (decoupling theorem).
- A33 `MASTER_ACTION.md` §1–2 (clock ξ = 1 status D; K5's −0.55 a₀ at ξ = 2, g = a₀/3; γ_F = γ_L status C; no K(Q) term;
  cold sector is a separate Vlasov medium with imported abundance).
- E2 (action's γ = 0 branch = AQUAL μ = x/(1+x); transverse fraction 0.2185; AQUAL Q₂ / Hees 2σ = 2.44–4.59 canonical,
  2.85–5.19 alt, every y_t row incl. "none"), D7 (turn-off P5 needed: bare anomaly a₀; closure F(y_t) = Λc⁴/a₀²; "a turn-off
  needs a new invariant, e.g. a nonlinear clock coupling f(|∇ln N|)"), D7b, D7d (stiffened action passes Q₂), D9 MAP, D9b, E5.
- Khronon in the record: `fable_independent_2026/KHRONON_2404.06584_COMPARISON.md` (action Eqs. 2.1–2.7 quoted from a cached
  full text that is **not on disk**), `real_research/bs_khronon_2026/` (BSK1: khronon mass density = MOND phantom; BSK2:
  khronon dust at BS24's μ fails a σ₈ gate, ratio 0.037, registered tension), `real_research/khronon_momentum_2026/`,
  `opus_48_extended_research/reviews/*` (same K(Q) = μ²(Q−1)² as AeST's ghost condensate). None maps the Khronon action onto
  A33/PAPER49 with stiffness, and none relates J(Y) to the record's closure. That is new here.

## External inputs (via WebFetch of arxiv.org/html, 2026-10-22; NOT verified on disk; PROVISIONAL)

- 2404.06584v2 (BS24): n_μ = −(c/Q)∇_μτ (1); Q = c√(−g^{μν}∇_μτ∇_ντ) (2); A_μ = c²n^ν∇_νn_μ = −c²q_μ^ν∇_ν ln Q (3);
  Y = A_μA^μ/c⁴ (5); S = (c³/16πG)∫√−g[R − 2J(Y) + 2K(Q)] + S_m (6); K = μ²(Q−1)² (7); φ = ψ + O(c⁻²) (24);
  ∇·[(1+J_Y)∇φ] + μ²φ = 4πGρ (35); f = 1 + J_Y (36); J = Λ − Y + (2c²/3a₀)Y^{3/2} + … (37); strong field J = Λ∞ + O(a₀/y) (40);
  K_Q = I₀/a³ (47); Q̄ = 1 + I₀/(2μ²a³) (53); w = w̃₀/(w̃₀ + a³), w̃₀ = I₀/4μ² (57).
- 2507.00912v1 (BS25): same action (1)–(3), (5); J = 0 for Y ≫ a₀²/c⁴ (4a); (4b) = (37) with Λ the measured cosmological
  constant; ρ̄_K = I₀(1 + w̃₀/a³)/(8πGa³) (17); a DBI K(Q) with a second constant λ_D (6).
- Every one of these is cross-checked below by re-deriving it from the quoted action (K1, K7). A failure of a cross-check
  means the transcription (not the physics) is suspect, and the lane stops at that point for that item.

## Method (fixed now)

Units c = 1. Static weak field ds² = −(1+2εψ)dt² + (1−2εϕ)δ_ij dx^i dx^j, τ = t (unitary gauge), ψ, ϕ arbitrary functions of
(x, y, z) (no symmetry). sympy computes √−g R exactly, A_μ from n_μ by Christoffels, Y and K(Q), and truncates at O(ε²);
J − J(0) is kept as an abstract function of Y. Minisuperspace FRW for cosmology. Numbers in double precision, single thread.

## Checks (pass lines)

- **K1 (static limit, AQUAL type).** The EL equations of the truncated BS24 Lagrangian give ϕ = ψ and
  ∇·[(1+J′(Y))∇ψ] + μ²ψ = 4πGρ with Y = |∇ψ|², in full 3D. PASS: both residuals simplify to 0, and A_i computed from n_μ
  equals ∂_i ln N exactly (static metric). (Cross-checks Eqs. 3, 24, 35.)
- **K2 (μ = x/(1+x) exactly).** J_x(Y) = Λ − 2a₀²[y − ln(1+y)], y = √Y/a₀. PASS iff 1 + J_x′ − y/(1+y) = 0 and the small-Y
  series of J_x equals Eq. (37) through Y^{3/2} (residual 0). Reported: lim J_x/√Y at Y → ∞ (if ≠ 0, x/(1+x)-exact lies
  OUTSIDE BS's admissible class, Eqs. 40 / 4a).
- **K3 (clock = Legendre dual).** A33's static γ = η = 0 Lagrangian −|∇Φ|²/2K + ξP·∇Φ − W(K|P|) with P eliminated
  algebraically equals BS24's static Lagrangian with J = J_x at ξ = 1 (residual 0). At ξ = 2 it must reproduce A33 K5:
  g_N − g²/(g+a₀) = −0.55 a₀ at g = a₀/3 (|diff| < 1e-12). PASS iff both.
- **K4 (curl structure).** For a non-symmetric test field (two point masses), the auxiliary P* = (1−μ)∇Φ/K has |∇×P*| > 0
  at an off-axis point, while K1 holds with no symmetry assumed. PASS iff curl magnitude / |∇P*| > 1e-3 at the test point.
  (So the Khronon's MOND law is AQUAL off symmetry; its difference from AQUAL is identically 0; E2's transverse fraction
  0.2185 is quoted as the size of the error the curl-free khronometric-AeST law would make.)
- **K5 (pure Khronon cannot screen).** PASS (= obstruction confirmed) iff all three hold: (a) with J_x the planetary anomaly
  is a₀ (C1/D7d ratios > 1 on both footings, quoted); (b) with any turn-off obeying Eq. (40)/(4a), Q₂ under AQUAL still
  exceeds the Hees 2σ line at every y_t row on both footings (E2 json min ratio > 1); (c) the μ² term is negligible at the
  Q₂ radius r ≈ 7000 AU: μ²r² < 1e-6 for μ⁻¹ ≥ 100 kpc (Eq. 39).
- **K6 (covariant Khronon + P).** The covariant clock coupling P^μA_μ (n^μP_μ = 0) reduces to P^i∂_i ln N in the static
  metric (residual 0), so A33 written with τ is a Khronon-vector theory. The O(γ) elimination of P into a pure-lapse operator
  is invalid where screening acts: PASS iff (L★/r)² ≫ 1 (> 1e6) at 1 AU for L★ = 24 and 90 pc (P must stay an independent
  field; the stiffness is non-perturbative in the Solar System).
- **K7 (cosmology).** From the FRW minisuperspace action of BS24 (N(t), a(t), τ = t), derive K_Q = I₀/a³, Q̄, w and ρ̄_K.
  PASS iff Eqs. (47), (53), (57) and BS25 (17) are reproduced (residuals 0), and Y ≡ 0 on FRW (a₀ absent from the background).
- **K8 (closure identity).** If J(∞) = 0 (BS25 Eq. 4a, premise) then Λ = J(0) − J(∞) = 2a₀²∫₀^∞ (y − y_N) dy (c = 1). With the
  record's turn-off law (D7 kernel), check numerically that ∫(y − y_N)dy = ∫(y − y_N)dy_N = F(y_t) (rel. < 1e-6) and that
  y(y_N) is monotone (J single-valued, AQUAL elliptic). PASS iff both. Reported: Λc⁴/a₀² = 2F(y_t) (vs the record's
  F(y_t) = Λc⁴/a₀²), and the y_t this gives at quoted Λ (canonical, alt) and at 32π (κ = ½).

`--mutate` (env `C4_MUTATE=1`): K1's target uses f = 1 − J′ (wrong sign), K3 uses ξ = 2 for the ξ = 1 identity, K8 compares
Λc⁴/a₀² with ∫(y − y_N)dy without the factor 2. K1, K3 must FAIL. Outputs `*_MUTATE.out`, `*_results_MUTATE.json`.

## Verdict lines (fixed now)

- **EMBEDS**: K1–K4 PASS and K5 FAILS (some pure-Khronon J screens the Sun and passes Q₂).
- **EMBEDS WITH EXTRA TERM**: K1–K4 PASS, K5 PASS: the additions needed for the stiffness are named and counted
  (field and term), and compared with C1's AeST count in one table.
- **NO-GO**: K1 or K2 FAILS (the Khronon's static limit cannot be AQUAL μ = x/(1+x)) or K4 FAILS (curl-free law).
- **UNDECIDED**: a WebFetch'd equation fails its cross-check and the item depends on it.

No-go audit (D9 MAP, D9b, E5: NG1, NG2, Λ_LV, D-T) is a hypothesis table in the README, tagged DERIVED / OPEN.
Rules: κ = ½ FITTED; footings 9.36e-11 / 1.13e-10 m/s² never pooled; no DM particle; not "theory closed"; nothing here says
the data favour the framework. Runs `OMP_NUM_THREADS=1 nice -n 10`, < 1 GB RSS, single thread.
