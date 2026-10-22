# C5_health — FROZEN CRITERIA (written before any script or number)

Question: is the candidate covariant screened theory healthy? The candidate is C4's parent: the Blanchet–Skordis (BS)
Khronon action with J chosen so the static limit is AQUAL μ = x/(1+x), P promoted to an independent spatial covector
(n·P = 0) and one stiffness −(γ_L/2)(D·P)², γ_L = K L★²/2. In unitary gauge τ = t this is A33's action. The same
question is asked of C1/C3's AeST version (AeST + the γ_L operator, capped F).

## Record checked before freezing

- `covariant_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`.
- C4 README + script (theory definition; BS's action R − 2J(Y) + 2K(Q), K = μ²(Q−1)², read via WebFetch, NOT on disk).
- C1 README (AeST capped F = (2−K_B)𝒥, 𝒥′ → ∞ at the cap), C2 README §6 + PROVENANCE (SZ papers now on disk at
  `../_external_data/aest_papers_2026_10_22/`, outside the repo: SZ stability 0 < K_B < 2, λ_s > −1, K₂ > 0, λ_s > 0 for the
  ω = 0 mode; 5 + 1 modes), C3 README (β_L term −β_L[∇_μ(q^{μν}∇_νφ)]², β_L = (2−K_B)L★²/2).
- DSF-21 A33 `MASTER_ACTION.md` (action, coefficient table: β free, η free with "η ≥ γ (scalar luminality)", γ_F = γ_L chosen),
  A68 (5 DOF; scalar Z = K(2+3β)/β + ηp², ω² = γp⁴/Z, gapless k⁴; m_T² = K/η, c_T² = γ/η; healthy for β, η, γ > 0),
  A69 (η/γ unfixed; k⁴-mode strong-coupling momentum 2.836e-69 eV), round-2 relativity report
  (`core_open_problems_round2_2026_10_20/03_relativity/report.md`: de Sitter scalar ½a³[(B+ηp²)σ̇² − (γp⁴+2BH²)σ²];
  oblique principal criterion β > 2ηa₀²/K; non-tensor sup v² = (γ/η)(1 + 4ηu²/K)), E5 (NG2 positivity, R3θ ghost theorem G),
  D9 MAP row 12 (A33 "healthy EFT, not UV"), D7d (Solar System sits in the Galactic external field, x_e = 1.15–2.6;
  screened hedgehog GM/L★² ≤ 4.6e-6 u_e).
- New here (not in the record): (i) the β = 0 case, which is what BS's covariant R gives (no (∇·n)² term); (ii) the BS
  K(Q) lapse term in the perturbations; (iii) the static backgrounds with u₀ ≠ 0 at finite k (strong unscreened fields,
  where J grows outside BS's class), not only the principal symbol; (iv) the AeST + γ_L version's modes.

## External inputs

- SZ21 = arXiv:2007.00082, `newRMONDLett.tex` (on disk, outside the repo, sha256 in C2 PROVENANCE): Minkowski quadratic
  action (eq. `Minkowski_action`), vector mass M² = (2−K_B)(1+λ_s)Q₀²/K_B, scalar ω² = 0 and
  ω² = (2−K_B)(1 + K_Bλ_s/2)k²/(K₂K_B) + M², "λ_s ≡ F_Y/(2−K_B) at the background", conditions above.
  The transcription is checked by re-deriving both dispersion relations (H3). The tex line has a missing operator before
  K_B|Ȧ − ½∇h⁰⁰|²; the sign "+" is fixed by H3 (the vector mass must come out as SZ state it).
- BS24/BS25 (via C4, NOT on disk): only the action form and K(Q) = μ_K²(Q−1)² are used.

## Method (fixed now)

Units c = 1; all P-sector terms carry an overall 1/K after P = p/K, so K = 1 in the symbolic work and η̂ = η/K, γ̂ = γ/K
are lengths². ADM, unitary gauge, spatial gauge h_ij = 2ζδ_ij + h^TT_ij (no ∂∂E, no ∂_(iF_j)).

**Theory family T(β, η, γ_L, γ_F, μ_K, W):** L/(N√h) = [R₃ + K_ijK^ij − (1+β)θ² + 2μ_K²(1/N − 1)²]/(4K) + P^iD_i ln N
− W(u) + (η/2)E_iE^i − (γ_L/2)(D·P)² − (γ_F/4)F_ijF^ij, W the record's log (u < a₀).
- **C4-literal** = (β = 0, η = 0, γ_F = 0, μ_K ≥ 0): BS's R has no θ² deformation; C4 named no P kinetic term.
- **C4 = A33** = (β > 0, η > 0, γ_F = γ_L, μ_K = 0): A33 written with τ (needs the (∇·n)² term, i.e. β ≠ 0, added).
- Intermediate rows (β = 0, η > 0), (β > 0, η = 0), and μ_K > 0 are computed too.

**Local (frozen-coefficient) backgrounds:** flat h, N̄ = 1 + g·x, constant P̄ = (u₀/K)P̂ at angle θ to k, W's Hessian
entered as M_L ≡ K W″(u₀) and M_T ≡ W′(u₀)/u₀ (M_L = M_T = 1 at u₀ = 0; for the record's W, M_T = a₀/(a₀−u₀),
M_L = M_T²). Each perturbation is a plane wave; the θ-averaged quadratic Lagrangian is a Hermitian matrix M(ω, k) over
(n, N_i, ζ, h₊, h×, δP_i). sympy computes √h R₃, K_ij, D·P, F, E, the clock and W to second order from scratch.
- Mode count = number of nonzero roots in ω² of det M (route 1); ω = 0 roots are reported separately.
- Ghost test = Krein sign of each root, ω v†(∂M/∂ω)v on the null vector (route 2), and, where the constraint block is
  invertible, the eliminated kinetic matrix (route 3). Gradient/tachyon test = all roots ω² real and ≥ 0.
- Speeds: phase ω/k and the large-k limit ω²/k² (front speed).
- Backgrounds evaluated: Minkowski (u₀ = 0, g = 0); galactic (y = g/a₀ = 1); unscreened strong field
  (u₀ = a₀y/(1+y), g = a₀y, y = 10², 10⁴, 10⁸); screened Solar System (u₀ = a₀x_e/(1+x_e) from D7d's x_e, local g at
  1 AU); NS-like (screened, g = 10¹² m/s², same u₀). L★ ∈ {20, 24, 90} pc; footings a₀ = 9.36e-11 / 1.13e-10 m/s²,
  never pooled. η ∈ {γ_L, 10γ_L}; β ∈ {1, 10⁻³, 0}.

**FRW:** scalar sector (ζ, n, Y ≡ ∇²ψ, σ with P_i = ∂_iσ), h = a²e^{2ζ}δ, N̄(t) = 1/Q̄(t) (unitary gauge), from scratch
with sympy (Fourier mode, time-dependent coefficients); eliminate n and Y; read the kinetic matrix and the sub-horizon
gradient matrix. Background equations from the minisuperspace action.

## Checks (pass lines)

- **H1 (my action vs A68).** At u₀ = g = μ_K = 0, β > 0, my from-scratch M(ω, k) gives: tensor ω² = k²; transverse P
  ω² = (K + γ_F k²)/η; scalar ω² = γ_L k⁴/(K(2+3β)/β + ηk²). PASS iff all three residuals are 0 (symbolic).
- **H2 (my FRW vs round-2).** At μ_K = 0, β > 0, de Sitter, my FRW reduction gives
  ½a³[(B + ηp²)σ̇² − (γp⁴ + 2BH²)σ²], B = K(2+3β)/β (up to a total derivative). PASS iff the residual is 0.
- **H3 (SZ transcription).** SZ's quadratic action, as transcribed with "+K_B|…|²", reproduces SZ's vector and scalar
  dispersion relations (residuals 0) and has exactly two scalar normal-mode branches (ω² = 0 and the massive one).
- **H4 (mode count, two routes).** For each row of the family, the count of nonzero ω² roots (route 1) equals the count
  of positive-norm + negative-norm modes found by route 2. PASS iff routes agree on every row AND C4 = A33 gives 5 (A68).
  The C4-literal count is reported as COMPUTED (no pass line on its value).
- **H5 (static-background closed form).** A closed-form scalar/transverse reduction in the decoupling limit
  (dropping terms suppressed by g/k and by K γ̂ P̄²-type factors, whose size is computed) matches the full numeric
  M(ω, k) roots at every record background to relative 1e-6. PASS iff max relative deviation < 1e-6 AND every dropped
  factor < 1e-6 at the record's values.
- **H6 (strong field: J outside BS's class).** On the unscreened strong-field backgrounds (y up to 10⁸) and the screened
  Solar System / NS backgrounds, for C4 = A33 at the record's values: PASS (= no ghost, no gradient instability) iff every
  root has ω² ≥ 0 and positive Krein sign at k L★ ∈ {10⁻³, 1, 10³}. A FAIL is a result: report the mode and where.
- **H7 (β = 0, BS's covariant R).** Report, for η > 0 and u₀ ≠ 0 (every galaxy, and the Solar System via x_e), the sign of
  each root's ω² and Krein norm at β = 0 and at β just above and below round-2's line 2ηa₀²/K. PASS iff the computed sign
  change sits at β = 2η̂u₀² (my route) to relative 1e-3, confirming the record's criterion is the boundary; the verdict
  then states whether BS's β = 0 is healthy.
- **H8 (k⁴ mode).** Report on which backgrounds the scalar is gapless with ω ∝ k² (Minkowski only?) and its fate at β = 0.
  Strong coupling from W's cubic K²|P|³/(3a₀) (the potential-only vertex, as round-2 §5 and A69): p_sc in both regimes
  (B-dominated, ηk² ≪ B; η-dominated), at L★ ∈ {20, 24, 90} pc and both footings. PASS iff p_sc < H_native in both regimes
  (H_native² = 64πa₀²/(3(2+3β)), round-2's framework relation, at β = 1) — i.e. weakly coupled on all sub-Hubble scales.
- **H9 (FRW with K(Q)).** For β > 0 and for β = 0, with μ_K > 0 and Q̄ > 1: the kinetic matrix of (ζ, σ) is computed;
  PASS iff its determinant and trace are positive for the stated conditions AND the sub-horizon squared speeds are ≥ 0
  given Q̄ ≥ 1; the conditions are stated as inequalities. Whatever the sign, the IR band (k ≲ μ_K) is reported.
- **H10 (AeST + γ_L, capped F).** From SZ's quadratic action plus −(2−K_B)(L★²/2)(∇·V)², with λ_s,eff = 𝒥′ (transverse)
  and 𝒥′ + 2Y𝒥″ (along V) at the background: scalar and vector dispersion, Krein signs and the k → ∞ speed. PASS iff the
  mode count is unchanged by the γ_L term and every ω² ≥ 0 for 0 < K_B < 2, K₂ > 0, λ_s,eff ≥ 0. The speeds are reported.

## Mutation

`C5_MUTATE=1`: clock coefficient ξ = 1 → 2 (breaks H1's scalar cancellation), and the SZ K_B term's sign "+" → "−"
(breaks H3). Outputs `*_MUTATE.*`.

## Verdict lines

- **HEALTHY:** C4-literal (as BS's action gives it) has no ghost, no gradient instability, and a finite mode count at the
  record's values on every background above, with no added term.
- **CONDITIONALLY HEALTHY:** healthy only under stated inequalities (on β, η, γ_L, W's Hessian, μ_K, Q̄); the verdict
  says whether the record's values meet them and whether meeting them needs a term BS's action lacks.
- **UNHEALTHY:** a ghost or gradient instability at the record's values in the screened theory's regime; name the mode
  and the background.
- The README says which parent (Khronon + P, or AeST + γ_L) survives, and states the speed results separately from the
  ghost/gradient results (superluminality in a preferred-frame theory is reported, not counted as a ghost).

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the
framework.
