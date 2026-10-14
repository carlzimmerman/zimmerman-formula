# CFG767: Lean certificates for the formation clock and the P-wave gap — CERTIFIED (7 theorems, 0 sorry, standard axioms)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (5dc0650d4), 2026-10-14. Block CFG760–769.
- **Files** (`fable_independent_2026/lean_2026/`): `CFG767_clock_gap.lean` → `.out` (exit 0; no error, no sorry; every theorem
  depends only on [propext, Classical.choice, Quot.sound]); `CFG767_clock_gap_MUTATE.lean` → `_MUTATE.out` (exit 1: C2 reversed
  fails `linarith`, C5 with ln 9 fails its rewrite).
- κ = ½ FITTED (unused); not "theory closed". Algebra/analysis only.

| theorem | English claim | Lean statement | match |
|---|---|---|---|
| C1 `frac_mono_t` | more time, more cold energy | StrictMono (t ↦ 1 − e^{−t/τ}), τ > 0 | MATCH |
| C2 `frac_anti_tau` | slower formation, less cold energy | t > 0, 0 < τ₁ < τ₂ ⇒ f(t, τ₂) < f(t, τ₁) | MATCH |
| C3 `frac_bounds` | fraction in [0, 1) | 0 ≤ f < 1 for t ≥ 0, τ > 0 | MATCH |
| C4 `window` | CFG763's band | τ_min ≤ τ ≤ τ_max ⇒ f(τ_max) ≤ f(τ) ≤ f(τ_min) | MATCH |
| C5 `sparc_upper` | f ≥ 0.9 after t ⇔ τ ≤ t/ln 10 | as stated (t, τ > 0) | MATCH (with t = 8 Gyr this is CFG763's 3.47 Gyr and CFG764's k bound) |
| C6 `below_gap_evanescent` | below ω_g, k² < 0 | ω² < 2v/s + 2/s² ⇒ ω² − 2/s² − 2v/s < 0 | MATCH (algebra; that k² < 0 means no local propagation is the reading) |
| C7 `deep_gap_cp` | c_P,max = V/(x√(2s₀)) in the deep limit | V/(x √(2/s₀) s₀) = V/(x √(2 s₀)) | MATCH (the deep-limit ω_g = √(2/s₀) is the premise; CFG760 uses the full profile) |

Not certified: the Green's-function suppression numbers (CFG760/761), the TDG/SPARC fits (CFG763/764), any physical premise.
