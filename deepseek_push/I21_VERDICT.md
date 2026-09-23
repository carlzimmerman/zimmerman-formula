# I21 — D-YM1 Hamiltonian door: polymer-threshold Lean audit — VERDICT: PASS

**Audit date:** 2026-09-23 (UTC 19:52) · **Auditor:** subagent (lean-math-certification lane)

**Target:** `fable_independent_2026/lean_2026/I21_ym1_polymer_threshold.lean` (untracked/uncommitted, as stated)
**Companions audited alongside:** `I21_ym1_combinatorics.lean`, `I22_ym1_dobrushin.lean` (both also untracked)

## 1. Toolchain

- `lean` on PATH: `/opt/homebrew/bin/lean`, **Lean 4.34.0-rc2** (arm64-apple-darwin), lake 5.0.0-src+6a10ac8.
- Project toolchain: `fable_independent_2026/lean_2026/lean-toolchain` = `leanprover/lean4:v4.34.0-rc2` — matches.
- `lakefile.toml` requires mathlib `v4.34.0-rc2`; oleans restored from the local mathlib cache
  (`~/.cache/mathlib`, 17,640 ltars; `lake exe cache get` → "Already decompressed 8747 file(s)").
- Compile method = repo's method: `lake env lean <file>.lean` from `fable_independent_2026/lean_2026`
  (same as the pre-existing `<name>.out` artifacts in that directory; a pre-existing
  `I21_ym1_polymer_threshold.out` matched the fresh run exactly, so the result is reproducible).

## 2. Compile results

| file | exit code | time | sorries | axioms |
|---|---|---|---|---|
| `I21_ym1_polymer_threshold.lean` | **0** | 29 s | 0 | {propext, Classical.choice, Quot.sound} for all 13 theorems |
| `I21_ym1_combinatorics.lean` | **0** | 6 s | 0 | {propext, Classical.choice, Quot.sound} for all 6 theorems |
| `I22_ym1_dobrushin.lean` | **0** | 6 s | 0 | {propext, Classical.choice, Quot.sound} for all 8 theorems |

Unfiltered `#print axioms` (the file ends with one per theorem): every theorem depends on exactly
`[propext, Classical.choice, Quot.sound]`, no `sorryAx`, no other axioms. The only occurrence of the
string "sorry" in the file is the header docstring "Zero `sorry`; …". **Zero `sorry`. File NOT modified.**

## 3. What I21 states (precise)

Namespace `I21`, `Real` arithmetic, certified parameters G = 7/100, b = 1/2 (C_F = 1 in C_F units),
a₁ = 4G², c = (1−b)/(1+G+G²), a₂ = cG(1+G), κ = G/(1+G)⁷, K* = 6⁶/7⁷,
λ_*(d)/C_F = G·c·e^{−a₁}/(32(d−1)(1+G)⁷) — identical to PROOF.md Theorem 1's λ_*(d) = C_F·6.2137e-4/(d−1).

Thirteen theorems, exactly the scalar chain of `real_research/reviews/ym_door_swings_2026_09_22/ym1_hamiltonian/PROOF.md` §§5–7:

1. `c_identity` — c + a₂ + b = 1 (§6 parameter choice).
2. `kappa_le_Kstar` — κ ≤ 6⁶/7⁷ (tree criticality, §5).
3. `tree_supersolution` — 0 ≤ g ≤ G ⟹ κ(1+g)⁷ ≤ G (monotone branching iteration stays in [0,G], Lemmas 5.1–5.2).
4. `KP_a2_identity` — d > 1 ⟹ 2(d−1)·(16·λ_*(d)·e^{a₁}·(1+G)⁸) = a₂ (the **Kotecký–Preiss event-contact half (6.2) as an exact identity** — the "sum-of-weights threshold satisfies KP" statement).
5. `kappaB_lt` — κ_B := κe^{2a₁}/(1−2G−2G²) ≤ 0.95·K* (boundary-sum condition, §7).
6. `boundary_supersolution` — κ_B·(1+3/25)⁷ ≤ 3/25 (g = 3/25 supersolution).
7. `path_ratio` — 7·(3/25)/(1+3/25) < 1 (marked-path step ≤ 3/4 < 1, Γ₀ₜ uniform in t).
8. `exp_neg_a1_lower` — e^{−a₁} ≥ 1/(1+a₁+a₁²/2+2a₁³/9) (from Mathlib `Real.exp_bound'`, n = 3).
9. `eps_uniform` — N ≥ 2, 0 ≤ b_N ≤ 2N, x > 0 ⟹ λ/C_F = 2b_N/(x²C_F) ≤ 32/(3x²) (**uniform in N**).
10. `X3` — x ≥ 1853/10 = 185.3 ⟹ 32/(3x²) ≤ λ_*(3)/C_F.
11. `X2` — x ≥ 1311/10 = 131.1 ⟹ 32/(3x²) ≤ λ_*(2)/C_F.
12. `X4` — x ≥ 227 ⟹ 32/(3x²) ≤ λ_*(4)/C_F.
13. `gap_conversion` — x ≥ 0, C_F ≥ 3/4 ⟹ 3x/16 ≤ (x/2)(C_F/2) (= x·C_F/4).

Chained: eps_uniform + X_d ⟹ **λ ≤ λ_*(d) for every N ≥ 2, b_N ≤ 2N, x ≥ X_d**; gap_conversion with
C_F ≥ 3/4 (I15 §2 Casimir minimum) ⟹ **gap ≥ x·C_F/4 ≥ 3x/16**.

## 4. Verdict relative to the door claim

The YM door swings claim: I15 Kogut–Susskind gap strong-coupling window thresholds X₃ = 185.3
(uniform in N), X₂ = 131.1, X₄ = 227.0, gap ≥ 3x/16, via a Ueltschi cluster expansion with tracked
constants. Verdict:

- **PASS (scalar chain):** I21 machine-checks every numeric inequality in that chain — the explicit
  thresholds X₂/X₃/X₄ uniform in N, the uniform λ/C_F bound, the gap conversion 3x/16, the parameter
  identity c + a₂ + b = 1, and the **polymer/KP threshold algebra**: the event-contact identity
  `KP_a2_identity` (2(d−1)·R = a₂ at λ = λ_*(d), i.e. the sum-of-weights criterion holds exactly at the
  certified coupling), tree criticality κ ≤ K* with the [0,G]-supersolution, and the §7 boundary
  conditions κ_B ≤ 0.95 K*, g = 3/25 supersolution, path step < 1. This is precisely the
  "polymer only if the sum-of-weights threshold satisfies Kotecký–Preiss" content, formalized.
- **SCOPE LIMIT (per the file's own header):** the analytic leaves are NOT formalized and remain prose,
  twice independently refereed (`REVIEW.md`): the Dyson expansion, polymer factorisation Lemma 4.1, the
  §5 tree bounds, **Ueltschi 2004 Theorem 1** (the Kotecký–Preiss theorem itself), and the §7
  boundary-component argument. I21 certifies the tracked-constant arithmetic of the expansion, not the
  expansion theorem. It therefore *extends* the PROOF.md result (x ≥ X_d ⟹ gap ≥ 3x/16 with the polymer
  threshold formalized) rather than re-proving the cluster expansion from scratch.
- Rounding: PROOF.md rounds thresholds **up** to one decimal (e.g. 131.02 → 131.1); I21 certifies the
  rounded, sufficient values (1311/10, 1853/10, 227).
- Companions: `I21_ym1_combinatorics.lean` (BDL-extension combinatorial skeleton: sector counting,
  depth pigeonhole, corrected App. A bound, explicit 8×8 counterexample — separate lane
  `ym1_bdl_extension_2026`) and `I22_ym1_dobrushin.lean` (Euclidean door: TV lemma, tanh identities,
  Dobrushin α < 1 windows, SZZ conversion) also compiled exit 0 with the standard three axioms.

## 5. Deliverables

- `deepseek_push/I21_VERDICT.md` (this file)
- `deepseek_push/I21_results.json`
- Compile logs (fresh): `fable_independent_2026/lean_2026/I21_ym1_polymer_threshold.audit.out`,
  `I21_ym1_combinatorics.audit.out`, `I22_ym1_dobrushin.audit.out`

House rules respected: no git commits; the .lean files were not modified; nothing overwritten.