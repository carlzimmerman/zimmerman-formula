# X15_c1_preferred_frame: does C1, inside its X14 window, survive the preferred-frame PPN bounds, and does it leave galaxy statics and dynamics intact in v3s? FROZEN CRITERIA

Written and committed (with `ASSUMPTION_LEDGER.md` and `LITERATURE_MAP.md`) before any lane script exists and before any
number is computed by code. Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`. κ = ½ is FITTED.
Footings canonical a₀ = 9.3603e-11 m/s² and alt a₀ = 1.1312e-10 m/s², never pooled. No dark-matter particle. Never "theory
closed"; nothing here says the data favour the framework. This is a theory-consistency lane; the only data are published
bounds (transcribed in the record). Small jobs only: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes;
`compute_queue/` and every other lane untouched; no downloads.

## 0. What was read, and the not-blind statement

Read before freezing: X14 (README, FROZEN_CRITERIA, LITERATURE_MAP, ASSUMPTION_LEDGER, the C1 part and `aqual_point` of
`x14_caustic_completion.py`, its `.out` and the C1 block of its JSON); X3 README §E2; `covariant_push_2026_10_22/
THEORY_V3_DRAFT.md` §0–1, `V3_FULL_PICTURE.md` §1–4; `C8_instantaneous/README.md`; A22 (`deepseek_push/DS_FINAL_2026_10_21/
A22_ppn_frames/report.md` and `a22_checks.py`); C5_health README (β lines); `data_assembly/DOOR11_LITERATURE_2026-09-29.md`
§1; `rebuild_2026_10_22/BRIEF.md`. One PROVISIONAL web look-up (LITERATURE_MAP L1).

**Not blind.** Before freezing I reasoned on paper (no script, no code-computed number) as follows; these expectations
shaped which quantities §3–§5 compute. Thresholds below are structural (published bounds, signs, limits, factor-of-1e3
validity margins), not tuned to them.
- In the screened Solar System (u = K|P| ≪ a₀, D·P > 0), v3s linearised about Minkowski is a khronometric theory with
  Hořava λ = 1 + β (C1), no K_ijK^ij change, and a scale-dependent acceleration coefficient η(k) = 2/(M + γ_L k²/K)
  obtained by integrating out P. Expectation: α₁(k) = −4η(k) (a G_N(k) ≠ G mismatch), α₂(k) ≈ η(η − β)/(2β) (BPS Eq. 91
  with α_BPS = η, β_BPS = 0, λ′ = β), both → 0 as kL★ → ∞; residual sizes ~(r/L★)² ≈ 1e-13 at 1 AU and ~(r/L★)⁴/β.
- The pure λ-term's own khronon equation forces the leaves to constant mean curvature (maximal at this order), which is
  the standard PPN slicing at 1PN, so C1 should drop out of the metric; A22's K5 ("d(θ²)/dh|₀ = 0") is a background
  statement, not a linear-response one, so A22's "α₁ = α₂ = 0 for every β_ADM" needs this lane's derivation.
- At β = 0 the linear khronon has zero longitudinal stiffness (c_S = 0), so the moving-source linear problem is
  expected to be non-analytic in w (the static hedgehog is not carried).
- Step 3 rough expectation: a galaxy moving at w through the khronon has its rotation curve changed at O((w/c_β)²),
  c_β = c√(β/2) ≈ 300–670 km/s across the μ_K = 0.1 window, which can exceed 0.05 dex for w ≳ 100–200 km/s; Cherenkov
  emission only for w above the local khronon speed.

## 1. Definitions

- **v3s** (V3_FULL_PICTURE §1; THEORY_V3_DRAFT §0–1): BS khronon with J_x, K(Q) = μ_K²(Q − 1)², the independent covector P
  (clock term P^i D_i ln N, W(u) = (a₀²/K)[−u/a₀ − ln(1 − u/a₀)], u = K|P|), switched stiffness −(γ_L/2)[max(D·P, 0)]²,
  γ_L = K L★²/2, K ≡ 4πG. Gravitational sector [R3 + K_ijK^ij − K²]/(4K) (A22 D1 at β_ADM = 0).
- **C1** (X14): the term −β K²/(4K) added inside that bracket (K = trace of the khronon leaves' extrinsic curvature), i.e.
  Hořava λ = 1 + β; X14's PN coefficient B = βc²/(2 + 3β). The window to test is X14's: β ∈ [β_min(foot), β_max(μ_K)],
  β_min = 1.99355e-6 (canonical) / 2.19755e-6 (alt); β_max = 1.00493e-5 (μ_K = 0.1 Mpc⁻¹), 1.11675e-4 (μ_K = 0.03 Mpc⁻¹).
- **The C1 members tested** (class list, frozen): the single operator β K² of the khronon leaves. Its literature aliases
  (mimetic γ(□φ)², projectable-Hořava λ ≠ 1, ghost-condensate (□φ)²) coincide with it at the PPN order used here only
  through this operator; no other member and no K_ijK^ij (BPS β) or a² (BPS α) term is added. Variants with an added
  K_ijK^ij term enter only in the relation clause of §5.
- **Linear screened system** (the object of step 1): fields n (lapse), ψ (h_ij = (1 − 2ψ)δ_ij), N_i (shift = g_0i), P_i,
  in the khronon's unitary gauge (τ = t), quadratic Lagrangian
  (1/4K)[2|∇ψ|² − 4∇n·∇ψ + K_ijK_ij − (1 + β)K²] + P·∇n − (KM/2)|P|² − (γ_LΘ/2)(∇·P)² − M_s(n + w²ψ − w·N)δ³(x − wt),
  K_ij = −ψ̇δ_ij − ∂_(iN_j), K = −3ψ̇ − ∂·N, M_s = M/√(1 − w²), c = 1. Screened Solar System: M = 1 (u/a₀ ≈ 2.6e-6, A22 D4),
  Θ = 1 (D·P > 0 for a point mass, A22 eq. 7), μ_K term dropped (μ_K r ≤ 5e-15 at 30 AU). Unscreened report: Θ = 0, M = M_θ.
- **Source**: a point mass M moving at constant w relative to the khronon frame (the frame where the khronon is at rest at
  infinity); all fields ∝ exp[i(k·x − Ωt)], Ω = k·w; k along z, w = (w_x, 0, w_z).
- **PPN identification** (standard PPN gauge, ζ_i = ξ = α₃ = 0 [LITERATURE_MAP L2]): in the preferred frame, for this source,
  g̃_0i = −½(8 + α₁) w_i Ũ + (1 + α₂) k_i(k·w)Ũ/k², with no 𝒜 (∝ (k·w)²/k²) term in g̃_00 at O(w²).
  Extraction by gauge-invariant combinations (invariant under t → t + ξ⁰): Ñ_x and Φ_inv ≡ ñ − (Ω/k)Ñ_z.
  Ũ_N(k) ≡ −Φ_inv at O(w⁰); α₁(k) = −2 [O(w) coefficient of Ñ_x]/(w_x Ũ_N) − 8;
  α₂(k) = 3 + α₁(k)/2 − (c_zz − c_xx)/Ũ_N, with c_xx, c_zz the coefficients of w_x², w_z² in Φ_inv. γ(k) = ψ̃/ñ at w = 0.
- **PPN order vs residual**: α_∞ ≡ lim_{kL★→∞} α(k) multiplies the PPN potentials and is the PPN-order parameter. The rest,
  expanded in (L★k)^(−2m), maps to non-PPN potentials ∝ r^(2m−1); its size at radius r is the **α-equivalent**
  α^eq(r) = |c_m| × (position-space ratio of the m-th term to the U-type term for the same tensor structure), computed
  from the exact inverse Fourier transforms of 1/k^(2n) and k_ik_j/k^(2n) (f_n = (−1)^(n+1) r^(2n−3)/(4π(2n−2)!)).

## 2. The bounds (record transcription, `data_assembly/DOOR11_LITERATURE_2026-09-29.md` §1; all assume the CMB frame, w ≈ 369 km/s)

| parameter | bound used | source (as transcribed) | where applied (test radius r) |
|---|---|---|---|
| α₁ (weak field) | \|α₁\| < 1e-4 (the stricter of LLR (−0.7 ± 1.8)e-4 95 % and Oost et al.'s adopted 1e-4) | Müller et al. via Shao & Wex 2012; Oost, Mukohyama & Wang 2018 | Earth–Moon 3.844e8 m (Earth's field), planets 1 AU and 30 AU (Sun) |
| α₂ (weak field) | \|α₂\| < 2.4e-7 | Nordtvedt 1987 (secondary) | 1 AU, 30 AU (Sun) |
| α̂₁ (strong field) | \|α̂₁\| < 2.1e-5 (Liu et al. 2020); interval −3.5e-5…3.3e-5 (Shao & Wex 2012) | DOOR11 | binary separation 1.73e9 m (J1738+0333, C8 table); **weak-field proxy only** |
| α̂₂ (strong field) | \|α̂₂\| < 1.6e-9 | Shao et al. 2013 | NS radius 1.2e4 m; **weak-field proxy only** |

The strong-field rows are scored with this lane's weak-field residual at the stated radius and labelled a proxy: no
neutron-star sensitivity is computed. If the local khronon frame is not the CMB frame the bounds scale as (369/w)²; this
is reported, not used.

## 3. Step 0: reproductions (stop rule: any failure → verdict UNDECIDED, no further scoring)

- **S0-1 (A22, record code).** `a22_checks.py` (sha256 f20cf27b…ff95), run read-only by subprocess with `--json-out` into this
  lane's directory: exit 0, 13/13 PASS, `alpha1_ppn_order = alpha2_ppn_order = 0`.
- **S0-2 (X14 window, record formulas).** X14's β_min (both footings, conservative M_θ − 1 = x, five fold radii, w ∈ {68.75,
  74.8} km/s, its `aqual_point`) and β_max = 2H₀²/(c²μ_K² − 3H₀²) (H₀ = 67.2 km/s/Mpc, μ_K = 0.1, 0.03 Mpc⁻¹), copied with
  provenance, equal X14's JSON (sha256 5af0afb8…) to relative 1e-12.
- **S0-3 (this lane's system ↔ X3/X14's khronon).** The scalar-sector determinant of §1's system (no source, μ_K = 0) has
  the khronon root ω² = B k² (M − 1 + Θγ_Lk²/K), B = β/(2 + 3β), i.e. X14's (ρ_τ + Bk²/K)(k²/χ − K) at ρ_τ = 0, residual 0
  for Θ = 1 and Θ = 0.
- **S0-4 (GR control).** With the P sector removed and β = 0, the (gauge-degenerate) system's solution gives Φ_inv and Ñ_x
  independent of the free gauge function, and α₁(k) = α₂(k) = 0, γ = 1 exactly.
- **S0-5 (A22 at β = 0 in this lane's system).** (a) Static source (w = 0, Θ = 1, M = 1): ñ = ψ̃ = −(KM/k²)(1 + 2/(L★²k²)),
  i.e. A22 eq. 8, Φ = Ψ = −GM/r + (GM/L★²)r (residual 0). (b) Moving source at β = 0: the PPN-order α₁,∞ = 0 and α₂,∞ = 0
  (reproduces A22's PPN-order statement). Whether the β = 0 moving solution is analytic in w and carries the hedgehog is
  **reported**, not gated.

## 4. Step 1: derivation (sympy, PYTHONHASHSEED=0)

- **D1** α₁(k; β, L★, M, Θ) and **D2** α₂(k; …) closed forms from §1's extraction, and γ(k).
- **D3** η-form: with P integrated out, η(k) = 2/(M + Θγ_Lk²/K); report whether α₁ = −4η and α₂ = η(η(1+2β) − β)/(β(2 − η))
  or another closed form; report the exact expressions as derived.
- **X-BPS (required, cross-check PROVISIONAL).** At leading order in small (η, β) with η/β fixed (BPS's expansion), the
  derived α₁, α₂ equal BPS 2011 Eq. 91 at
  β_BPS = 0, α_BPS = η, λ′ = β: α₁ = −4η, α₂ = η(η − β)/(2β). The exact derived α₂ is compared (reported) with the record's
  Einstein-aether c₁₃ = 0 formula c₁₄(c₁₄ + 2c₂c₁₄ − c₂)/[c₂(2 − c₁₄)] at c₁₄ = η, c₂ = β.
- **P-A1 / P-A2 (required).** α₁,∞ = 0 and α₂,∞ = 0 (exact limits) on the screened branch for symbolic β > 0.
- **P-LIN (required).** Linear validity at every test radius r and every scored β: C1 dominance over the khronon charge
  transport, B/(Kρ_τ r²) ≥ 1e3 with ρ_τ the Sun's (or Earth's, or the pulsar's) hedgehog charge M/(2πL★²r) (A22) plus the
  local Galactic phantom (≤ 1e-21 kg/m³); and subsonic khronon at the test scale, c_S(k = 1/r) ≥ 10 × 1000 km/s.
- **P-RES (required).** α₁^eq(r) and α₂^eq(r) (leading residual terms, m = 1 and the first 1/β term) below every §2 bound at
  its test radius, on a 41-point log grid spanning each window [β_min(foot), β_max(μ_K)], both footings (L★ = 21.682 /
  22.849 pc), μ_K = 0.1 and 0.03.
- **Unscreened branch (reported, no verdict weight).** Θ = 0, M = M_θ ∈ [1 + x, (1 + x)²] at X14's five fold radii, both
  footings: α₁, α₂ values at the window edges, stated as frame-dependence sizes, not PPN parameters (the field is not 1/r).

## 5. Verdict (scored on the screened branch, both footings, never pooled)

The surviving window W_PPN(foot, μ_K) = {β in X14's window : P-A1, P-A2 hold and every P-RES entry is below its bound and
P-LIN holds}.
- **C1 SURVIVES PPN** iff W_PPN is non-empty on both footings at μ_K = 0.1 Mpc⁻¹ (the S4 edge). The surviving window is
  reported at μ_K = 0.1 and 0.03.
- **WINDOW CLOSED BY PPN** iff W_PPN is empty on both footings at both μ_K.
- **SURVIVES ONLY WITH A RELATION BETWEEN CONSTANTS** iff W_PPN is empty, but becomes non-empty only on a relation not
  implied by v3s (e.g. a BPS-type α_BPS = 2β_BPS with an added K_ijK^ij coefficient tied to η, or β tied to L★).
- **UNDECIDED** iff any S0 check fails (stop rule), a required derivation check cannot be completed, or the footings
  disagree.

## 6. Step 3 (reported only; no verdict weight)

- **(3a) Mach numbers** w/c_A, with X14's c_A = c√(β(M_θ − 1)/(2 + 3β)) at its five fold radii (read from X14's JSON at
  β_max(0.1), scaled to β_min and to β_max(0.03)), for ILLUSTRATIVE relative speeds w ∈ {70 (X8/X10), 220 (Sun vs a
  Galaxy-static khronon), 369 (CMB dipole), 600 (typical field-galaxy peculiar speed, upper), 1000 (cluster members)} km/s.
- **(3b) Rotation curve of a moving galaxy (ESTIMATE).** From the 3D PN Lagrangian (X3 L1 in 3D + C1, sympy): the O(w)
  steady equation for the khronon in the galaxy frame, −w·∇ρ_τ − ∇·(ρ_τ∇δσ) + (B/K)∇⁴δσ = 0 (derived, residual 0), its
  particular solution δσ = −w·x (fully held) and its ℓ = 1 indicial polynomial on a ρ_τ ∝ r⁻² phantom,
  R p(p−1)(p+2)(p−3) = (p−2)(p+1), R = B/(Kρ_τr²) (derived). Streaming exponent p₁ = smallest real root > 1. Estimate
  δ ln g ≈ (dg/dg_N − 1) × (p₁ − 1)(p₁² + 2)/3 × (w/v_c)² × (r/R_h)^(2(p₁−1)), the a₀-line law, the AQUAL phantom of a
  6e10 M☉ point mass (X14's `aqual_point`), r ∈ {10, 30, 100} kpc, R_h ∈ {1, 10} Mpc (ILLUSTRATIVE held-halo radius),
  β ∈ {0, β_min, β_max(0.1), β_max(0.03)}, both footings. Compared with 0.05 dex.
- **(3c) Cherenkov (ESTIMATE).** Emission requires w > local khronon speed (c_A from 3a); its drag is bounded by the
  supersonic dynamical-friction form F = 4π(GM)²ρ_bg lnΛ/w² (LITERATURE_MAP L4), lnΛ = ln(1 Mpc/10 kpc), ρ_bg = (i) cosmic
  khronon dust ≤ ρ_crit (H₀ = 67.2, upper bound), (ii) a 1e14 M☉ (baryons) cluster's AQUAL phantom at 300 kpc; MW mass
  6e10 M☉, w ∈ {600, 1000} km/s; report t_drag = Mw/F in units of 1/H₀.

## 7. Checks, MUTATE, outputs

- Required checks: S0-1 … S0-5, D1, D2, X-BPS, P-A1, P-A2, P-LIN, P-RES, plus S3-1 (the 3b steady equation and indicial
  polynomial, residual 0). The script exits 0 iff every required check passes. Step-3 numbers are reported, not checks.
- **MUTATE** (`X15_MUTATE=1`, all at once); each named check must FAIL:
  - m1: the sign of C1 flipped in this lane's action (β → −β there only) → **S0-3** fails;
  - m2: the stiffness removed in the screened Solar-System system (Θ = 0, M = 1) → **P-A1** fails (α₁,∞ = −8);
  - m3: the matter-current coupling w·N dropped from the source → **S0-4** fails;
  - m4: H₀ doubled in the copied β_max → **S0-2** fails;
  - m5: A22's script run with its own `--mutate alpha1_forced` → **S0-1** fails.
- Outputs: `x15_c1_preferred_frame.out`, `x15_c1_preferred_frame_results.json` and `_MUTATE` twins; README with verdict,
  derivations (JSON keys), every amendment labelled PRE-RESULT or POST-RESULT, and "what this does not show".
- Git: pathspec commits of this lane only; never push; no rebase or amend.
