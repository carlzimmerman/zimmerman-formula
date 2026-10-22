# C3_scale_map — FROZEN CRITERIA (written before any script or number)

Lane of the covariant push (`covariant_push_2026_10_22/BRIEF.md`). The doors-push rules
(`doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`) apply in full.

## Question

Do AeST's own scales (Skordis & Złośnik 2021, arXiv:2007.00082; "SZ21") map onto the screened theory's stiffness
length L★ (window roughly [20, 90] pc after E4/E1), and what does a covariant AeST-type version predict for the
record's local tests? Is L★ then DERIVED, FITTED, or a new constant?

## Record checked before freezing

- Briefs: covariant push BRIEF; doors BRIEF and BRIEF_E_AUDIT.
- D7d README/criteria/solver (static equations (L), (P); Route F operator `[(κ²/2)I + J − k̂k̂]`, γ_F = γ_L);
  E4 README (native floor N1 28.85 / 29.12 pc); E1 README (floor is Υ_V-dominated, 12–41 pc).
- CFG691 (isolated profile S(s)), CFG740 (γ_v − 1 = ½(s/L★)²), CFG820 (globular floor, its script).
- AeST mentions: CFG242 L12 (door remnant), CFG172 / CFG172D (v9 AeST PPN kill row N7; not scored there),
  `real_research/bridge1_aest_equations.md` (SZ21 action Eq. 5, μ = √(2K₂/(2−K_B)) Q₀, "μ⁻¹ ≳ 1 Mpc",
  r_C ∼ (r_M μ⁻²)^{1/3}), `real_research/reviews/typeII_known_limits_2026.py` (F1–F7: SZ21 quasi-static system;
  F7: the mass term is ∇²Ψ + μ²Ψ = 4πĜρ + ∇²φ, oscillatory, with SZ21's printed μ),
  `real_research/reviews/ppn_verify_transcription_2026.py` (SZ21 Eq. 6 quasi-static action; Eq. 13 static bracket;
  arXiv:2109.13287 Eq. 30 sound speed; AeST's aether map c₁ = K_B, c₂ = 0, c₃ = −K_B, c₄ = 0),
  `real_research/AEST_MASS_SCALE_two_doors.md` (μ²Φ is negligible in the Solar System).
- **Source status.** The arXiv LaTeX sources were fetched in Aug 2026 by earlier sessions, but **no copy is on disk**.
  Every SZ21 / arXiv:2109.13287 / arXiv:2304.05134 equation used here is taken from the record's transcriptions above
  and is labelled **"external input, record transcription, not verified on disk"**. No downloads in this lane.

## External inputs (labelled)

- SZ21 Eq. (5) action; SZ21 Eq. (6) quasi-static action
  `S = −∫{A[|∇Φ|² − 2∇Φ·∇φ + |∇φ|² − μ²Φ² + J(Y)] + Φρ}`, A = (2−K_B)/(16πG̃) (record transcription).
- μ² = 2K₂Q₀²/(2−K_B); the requirement μ⁻¹ ≳ 1 Mpc (SZ21 text; arXiv:2109.13287 abstract) — used at the boundary
  μ⁻¹ = 1 Mpc, the value most favourable to AeST reaching small scales.
- c_s² = (2−K_B)(1 + K_B λ_s/2)/(K₂K_B) (arXiv:2109.13287 Eq. 30, record transcription). Used only to express a
  length bound; the bound is stated as conditional on it and on c_s ≤ c.
- Local inputs exactly as D7d: a₀ 9.36e-11 / 1.13e-10 (never pooled), GM_⊙, E0–E3 from D7b's json, Hees 2014 and
  Park 2026 2σ bands, planet bounds (BOUNDS.md as carried in D7d), wide binary 1.5 M☉ at 20 kAU.
- Globulars: CFG332 table via E4's native estimator (ν_L, no EFE recipe, Υ_V = 1.6 SURVEY-CALIBRATION).

## Definitions

- **V0 = pure AeST** with the screened theory's law (J chosen so that g_N = g²/(g + a₀); this is the λ_s → ∞ member),
  μ⁻¹ ≥ 1 Mpc, no added term.
- **V1 = AeST + one named term** `−β_L [∇_μ(q^{μν}∇_νφ)]²` in the action bracket (only if Q2 below finds that no
  AeST-class term does the job). This is a new posit; it is counted (+1 term, +1 constant β_L).

## Checks (each prints `Kn PASS/FAIL value threshold`; exit 0 iff all pass)

- **K1 (sympy, mass term on a point mass, Newtonian regime).** Φ = −GM cos(μr)/r solves ∇²Φ + μ²Φ = 0 for r > 0 and
  → −GM/r as r → 0; the radial pull is GM(cos μr + μr sin μr)/r², whose series is GM/r² + GMμ²/2 + O(μ⁴r²).
  Pass: exact symbolic identities. (Gives the "hedgehog-equivalent" length L_eq = √2/μ.)
- **K2 (sympy, deep-MOND regime).** With Φ = √(GMa₀) ln(r/r₀), the mass term's extra enclosed source gives a fractional
  correction ∝ μ²r³/r_M; its unit crossing scales as (r_M μ⁻²)^{1/3}, i.e. SZ21's printed r_C. Pass: exponent 1/3 exact.
- **K3 (sympy, decoupling theorem).** Static quadratic AeST-class action in Fourier space with fields Φ, φ, α
  (longitudinal aether), A_T (transverse aether), the most general static aether gradient terms
  c₁|∇×A|² + c₁₂₃(∇·A)², and the scalar entering only through V = ∇φ + Q₀A. Pass iff (a) the solution for Φ is
  independent of c₁₂₃ and of c₁ for a longitudinal (spherical-type) source, and (b) α = 0.
- **K4 (sympy, the named term).** For a radial field V = v(r) r̂, the operator from β_L(∇·V)² equals the radial component
  of the vector Laplacian used in D7d's (P); with β_L = (2 − K_B)L★²/2 the isolated V1 radial equation equals D7d's (P),
  hence CFG691's ODE. Pass: exact identity.
- **K5 (Route F generalised).** The generalised operator `(κ²/2)[k̂k̂ + g(I − k̂k̂)] + J − k̂k̂` at g = 1 reproduces
  D7d's `chi` to 1e-12 relative; the g = 1e8 value agrees with the g → ∞ closed form to 1e-6.
- **K6 (V1 Cassini).** Q₂ of V1 (g → ∞, the AeST curl stiffness) at L★ = 24, 50, 90 pc, E0–E3, both footings, lies inside
  the Hees 2014 2σ band [−3.0e-27, 9.0e-27] and the Park 2026 band [−2.0e-27, 5.2e-27]. D7d's values are printed beside.
- **K7 (V1 wide binary).** 1.5 M☉, 20 kAU, Galactic field E0–E3, both footings, L★ = 24/50/90 pc:
  γ_v − 1 < 1e-3 (far below D2's σ_sys 0.020), plus the mass-term addition ½·(μs)²/2.
- **K8 (V1 globulars).** The V1 isolated spherical sector equals the screened theory's (K3 + K4), so the native floor is
  E4's N1. Pass: this lane's copy of E4's estimator reproduces N1 = 28.853 / 29.123 pc within 0.01 pc; the mass-term
  correction (μ r_h)² is printed.
- **K9 (V0 fails the planets; verify the fail).** Spherical first integral u·f(u) = g_N with f(u) = u/(a₀ − u): the
  anomalous pull at Earth, Mars, Saturn reproduces D7d's unscreened no-P5 values to 1e-6 relative, and the Mars ratio to
  its bound is > 1 on both footings.
- **K10 (scale map).** Every AeST length (μ⁻¹, L_eq = √2/μ, r_C for the Sun / a globular / a 10¹¹ M☉ galaxy, and the
  curl-stiffness length L★_F ≥ √2/(c_s μ)) is compared with the window top 90 pc. Pass: the smallest ratio is printed and
  is > 1e3 (otherwise an AeST length could sit in the window and the classification changes).

`--mutate`: the mass term's sign is flipped (Yukawa, −μ²) in K1 and the named term is dropped (curl-only stiffness) in
K4. At least K1 and K4 must FAIL; outputs go to `c3_scale_map_MUTATE.out`, `c3_scale_map_results_MUTATE.json`.

## Outcome lines (fixed now)

- **Q1.** If K1, K2 pass: "AeST's mass term is a LARGE-scale term (r ≳ r_C, μ⁻¹), oscillatory, opposite in direction to
  L★'s small-scale screening." If the sign comes out Yukawa: "large-scale Newtonian switch-off" instead.
- **Q2.** If K3 passes: "L★ is OUTSIDE AeST's class; the covariant screened theory is AeST + one named term (β_L)".
  If K3 fails (some AeST-class term stiffens the longitudinal mode): "L★ is INSIDE AeST", and the coefficient is reported.
- **Q3.** K6–K9 give V1's and V0's local predictions as computed; any FAIL of K6/K7 is reported as a V1 fail, not hidden.
- **Q4.** Outside AeST → L★ = "new constant of the covariant theory, value FITTED (globular floor, calibration-dominated)".
  Inside → "DERIVED from" the named AeST constants, listing the premises.
- **Verdict.** Q2 outside → `SCOPED NO-GO` (no AeST-class term gives L★), with the K6–K9 numbers. Q2 inside →
  `CRISP FINDING`. κ = ½ stays FITTED; not theory closed; never "the data favour the framework".

## What this lane will not do

No covariant well-posedness proof of V1 beyond linear order on FRW; no CMB; no nonlinear Cassini solve of V0 (V0 is
decided by K9 first); no EFE-aware globular floor (open for both theories, per E4).
