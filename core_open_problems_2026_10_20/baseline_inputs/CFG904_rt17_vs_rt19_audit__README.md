# CFG904 — RT-17 versus RT-19: which κ does the de Sitter tie give? (CFG894 P4)

Block 900–909. Criteria `FROZEN_CRITERIA.md`, committed alone first (15f9ba56f). Audit lane: it derives nothing and adds no
trial to the look-elsewhere count. **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095 on ρ_DE). Not theory closed.

## Verdict: V-C — RT-19's withdrawal stands, its "4π error" does not

**0.4607 is not a coefficient-free value of the de Sitter tie.** RT-19 was right to withdraw it, but the 4π it blamed on RT-17
is not one error in RT-17. Split it into two factors:
- **2π is a real error in RT-17.** Its identification I1 does not agree with the Unruh relation it cites.
- **2 is not an error.** It is the deep-limit slope of a different construction, Milgrom's 1999 ΔT construction, which
  RT-19 used and RT-17 never did.

| test | result | what it shows |
|---|---|---|
| T1 RT-17 arithmetic | PASS | T_GH → x = 2πω/H_Λ → w = Zω/H_Λ → Z = 2πλ → κ = √(8π/3)/Z. I1 gives Z = 2π and κ = √(2/(3π)) = 0.460659 exactly. All four of RT-17's rows reproduce its printed table |
| T2 RT-17 determinacy | **FAIL (MENU)** | No equation in the chain fixes λ: Z = 2πλ is a one-parameter family. RT-17's own I1–I4 give κ = 0.4607, 0.9213, 0.2303, 2.8944, a spread of 2.66 against the window width of 0.38 (extremes differ by exactly 4π). RT-17 itself says (line 95) the identification is "an ADDED AXIOM ... not a theorem" |
| T3 RT-17 consistency | **FAIL** | RT-17 calls I1 "the direct reading of 'a₀ is the de Sitter–Unruh scale'" and ties its 2π to Unruh's. But T_U(a₀^I1)/T_GH = **1/(2π)**. The Unruh relation T_U(a₀) = T_GH gives a₀ = cH_Λ, Z = 1, κ = 2.894, which is RT-17's own I4. I1 sets a₀/c equal to the thermal angular frequency k_B T_GH/ħ = H_Λ/2π, not to the Unruh rate 2πk_B T_GH/ħ = H_Λ |
| T4 RT-19 chain | PASS | μ = [T(a) − T(0)]/T_U(a) = (√(u²+1) − 1)/u, with the thermal 2π, ħ and k_B cancelling. The series match solved for the scale (not assumed) has the single root λ* = 2, and the full-function residual μ_dS(2x) − μ₁(x) is identically 0. So a₀ = 2cH_Λ, Z = ½, κ = 2√(8π/3) = 5.789. Report only: the deep limit μ_dS → u/2 fixes a₀ = 2a_dS for *any* kernel with μ → x. The α = 2 kernel admits no full-function scale (it fails at O(x³)) |
| T5 is the 4π one error? | **FAIL** | Single-step corrections: c1 (T_GH is correct; Z stays 2π), c2 and c3 (Unruh-consistent S4 or S2; Z = 1), c4 (S5 against Friedmann is correct). None reaches Z = ½. **Z_RT17/Z_RT19 = 4π = 2π × 2**: the 2π sits in RT-17's step S4, and the 2 in RT-19's ΔT slope |
| T6 identity checks | PASS | Rename test I4 (law κ ½ → 0.4): neither output moves, only the comparison lines do. The claim "RT-19's κ equals the law's Z" holds only at κ_law = ½, so it is a coincidence. Convention rename (ħ → h/2π, ω → 2πν, k_B → 1): no leak. Scaling I3: κ invariant. π-weight tracking I8: κ² carries π⁻¹ (RT-17) and π⁺¹ (RT-19), both odd as declared, so exact ½ is impossible in either. The π in the ratio enters at RT-17's S1 (T_GH's 1/2π, kept by x) and cancels in RT-19's ratio μ. Forbidden-constant grep: clean |

**MUTATE: 4 of 4 controls bite as predicted** (exit 1, `cfg904_audit_MUTATE.out`).
- M1 (thermal 2π → 4π) moves RT-17 from Z = 2π to Z = 4π and leaves RT-19 and the Unruh-consistent a₀ = cH_Λ fixed. This is
  the π-locator: the same mutation moves one chain and not the other.
- M2 (8πG → 4πG) leaves every Z unchanged and multiplies every κ by 1/√2.
- M3 (λ = 1 → ½) gives Z = π, κ = 0.921.

## The corrected chain (what the de Sitter tie actually gives)

| reading | condition | a₀ | Z | κ (ρ_DE) | status |
|---|---|---|---|---|---|
| Unruh scale (identity) | T_U(a₀) = T_GH; the two 2π's cancel | cH_Λ | 1 | 2.894 | forced by the identity; outside W_data |
| dS–Unruh ΔT, Milgrom 1999 | inertia ∝ T(a) − T(0), matched to the kernel | 2cH_Λ | ½ | 5.789 | the only reading that matches a whole function, at a unique scale; outside W_data (the record's "dS–Unruh forces 2cH_Λ") |
| KMS frequency, RT-17 I1 | a₀/c = k_B T_GH/ħ, i.e. T_U(a₀) = T_GH/2π | cH_Λ/2π | 2π | 0.4607 | an **assignment**: the 2π is put back by hand. One entry of the menu {0.4607, 0.921, 0.230, 2.894}. Inside W_data, not significant |

The same table answers PAPER6's sentence. a₀ = c²/(2πL_dS) is "coefficient-free" only in the trivial sense that the
expression has no fitted number. It is not the Gibbons–Hawking/Unruh identity, which gives c²/L_dS. It is also not the only
such expression: Z ∈ {½, 1, π, 2π, 4π} are all coefficient-free in that sense. It was singled out because it lands near the
data (k03 line 5: "right-size").

Report only: with today's W_data, the RT-17 menu has *two* entries inside the window, 0.4607 and 0.2303 (Z = 4π, 1.97σ).
So "the one un-excluded" is no longer true either.

**Prior record.** T3 is not new:
- fable_independent_2026 L40 (B2, 2026-09-08) and HANDOFF_CONTRACT.md:263 already state that reaching 0.4607 needs
  T_U = T_dS/2π, "an assignment, not an identity".
- The MNRAS v2/v3 text (mnras_a0_lambda_v2.tex:590, v3.tex:618) already says it correctly.

This lane adds three things: the side-by-side recomputation, the 2π × 2 split of RT-19's 4π, and the list below. Chronology:
on 08-02, RT-17 (a96497f0e, 14:33) and mi_quadratic_z_escape (d83f7ad40, 14:37) were both committed before RT-19
(e54059e9c, 14:47).
k03 and PAPER6 (09-06) brought the same value back as the "Gibbons–Hawking/Unruh form" a month after the withdrawal,
without engaging it. PAPER6 v2 (09-27) kept the sentence after L40.

## The file list (FROZEN_CRITERIA §7; read-only; nothing here was edited)

How the list was built:
- Search: `git grep` at the pinned commit 15f9ba56f, over tracked text files only.
- That found 1274 hit lines; 824 of them are in κ context.
- 303 lines were CLAIM-flagged and all were read by hand: **47 are class A**, 223 B, 33 C.
- Miss-rate check: 0 of 40 randomly sampled non-flagged context lines turned out to be A.
- The full table is `cfg904_filelist_A.csv`, with every hand class in `cfg904_manual_review.csv`.

**Class A, strong** (says coefficient-free, derived, predicted or "no data"; 21 lines in 12 files):
- `README.md:135`; `STANDING.md:195` — "The one coefficient-free alternative ... (κ = 0.461)"
- `qwen_claude_field_theory/papers_2026/PAPER6_kappa_no_go_2026.tex:11` (abstract), `:51` ("the only coefficient-free
  identification in hand"); `PAPER6_kappa_no_go_2026.zenodo.json:14` (deposited abstract)
- `kappa_closure/k03_half_vs_two_pi_precision.py:5`, `:6` (the source of PAPER6's sentence, and the "Gibbons–Hawking/Unruh
  form" label); `kappa_closure/README.md:32`, `:41`; `kappa_closure/k02_global_constraint_average.py:92` and its `.out:22`
- `opus_48_extended_research/papers/THE_HORIZON_FORM_OF_THE_BTFR.md:136`
- `qwen_claude_field_theory/papers_2026/mnras_submission_2026/mnras_a0_lambda_coefficient.tex:130` (v1, rejected)
- `reviews/mi_kernel_measure_from_desitter_2026.py:4`, `:125`, `:203`, `:228`, `:255` (RT-17 itself: no withdrawal notice in
  the file)
- `reviews/mi_quadratic_z_escape_2026.py:12`, `:197`, `:198` ("DERIVED, with no data at all: the de Sitter TIE"; never
  corrected)

**Class A, weak** ("principle-shaped", "only un-excluded", "X gives", "the derivation"; 16 lines in 14 files):
- `qwen_claude_field_theory/papers_2026/PAPER6_kappa_no_go_2026.tex:61`
- `kappa_closure/k03_half_vs_two_pi_precision.py:56`, `:59` and its `.out:15`, `:18`
- `kappa_closure/k05_is_32pi_special.py:8` and its `.out:5`
- `qwen_claude_field_theory/closure_2026/RESUME_HERE.md:229`
- `campaign_fresh_gravity/CFG0_own_findings_inventory.md:40`
- `qwen_claude_field_theory/papers_2026/mnras_submission_2026/COVER_LETTER.md:11` (v1)
- `fable_independent_2026/L32_kappa_necessary.py:459` and its `.out:86` ("horizon thermodynamics gives the identification")
- `fable_independent_2026/L144_verdict_and_lean_propositions.py:74` and its `.out:16`
- `fable_independent_2026/L135_ppn_solar_system_gate_pincer.py:488` and its `.out:152` (in passing)

**Copies (10 lines in 5 files).** These clear when their source is fixed:
- `real_research/dark_energy_inverse_2026_09_26/scales/source_snapshots/kappa_closure/` (README.md:32, :41;
  k03 .py:5, :6, :51, :54; k03 .out:15, :18)
- `kappa_closure/k05_is_32pi_special_MUTATE.out:5`
- `campaign_fresh_gravity/CFG891_kappa_D3_c_term_census/cfg891_scan.out:122`

**Related mislabels (class B, no coefficient-free claim).** These call cH_Λ/2π the "Gibbons–Hawking/Unruh"
or "GH as Unruh" reading, but that identity gives cH_Λ:
- kappa_closure/README.md:65; k05 .out:68 (and its MUTATE copy, :70)
- real_research/predictions/coefficient_landscape.py:65
- CFG891 FROZEN_CRITERIA.md:187
- ROUTE5_NULL_STEELMAN_Z_UNFORCED_2026-06-15.md:28
- AS066 result.json:11 and make_result.py:48. AS066 itself calls the normalisation *adopted*, so it does **not** present
  0.4607 as coefficient-free in its own voice. CFG894's P4 note overstates AS066.

**Allowed replacement** (KAPPA_CAMPAIGN_RULES §10): "the Z = 2π assignment a₀ = cH_Λ/2π lands at κ = 0.461, inside today's
window, not significant. It is one entry of a menu, and it is not the Gibbons–Hawking/Unruh identity, which gives
a₀ = cH_Λ (κ = 2.894)."

## Consequences for CFG894 (not applied here; that lane's files are not this lane's)

- K459 (RT-17) is a **MENU** entry with options {0.4607, 0.921, 0.230, 2.894}, not a determinate DATA-LEVEL landing. When
  CFG894 reruns `kappa_campaign_lee.py`, the determinate in-window count drops by one.
- K461 (RT-19) stands as the ΔT output (MISS).
- The ledger's phrase "a 4π error" should read "a 2π assignment error plus the factor 2 of the ΔT construction".
- Proposed register row (next free K id, append-only, for CFG894 to add):
  `K?,CFG904,HT,campaign_fresh_gravity/CFG904_rt17_vs_rt19_audit/cfg904_audit.py,audit of K459 vs K461 (KMS w=x vs dS-Unruh Delta-T),,{0.4607;0.921;0.230;2.894},audit,0,K459 is a MENU (lambda unfixed; I1 Unruh-inconsistent by 2pi); K461 stands (MISS); 4pi = 2pi x 2,<this lane's result commit>`

## What this lane does not claim

- It does not claim that a₀ = 2cH_Λ is the framework's coefficient. That reading is a MISS by ×11.58, and κ = ½ stays FITTED.
- It does not claim that any dS reading gives ½: both chains are π-odd.
- It does not say which kernel is in force. RT-19's full-function identity needs α = 1; under α = 2 only the deep limit ties
  the scale.

## Files

- `FROZEN_CRITERIA.md`
- `cfg904_audit.py` with `.out`/`.json` (normal run, exit 0) and `_MUTATE.out`/`_MUTATE.json` (exit 1)
- `rt17_original_rerun.out` and `rt19_original_rerun.out`: the two records rerun read-only, blobs ede61ff97854 and
  d09e0f9bfee9 unchanged; 9/9 and 7/7 checks
- `cfg904_filelist.py` (`extract`, then `merge`)
- `cfg904_filelist_candidates.csv`, `cfg904_manual_review.csv`, `cfg904_filelist_A.csv`, `cfg904_filelist.out`

Rerun: `nice -n 10 python3 cfg904_audit.py > cfg904_audit.out`; `MUTATE=1 python3 cfg904_audit.py > cfg904_audit_MUTATE.out`;
`python3 cfg904_filelist.py extract && python3 cfg904_filelist.py merge > cfg904_filelist.out`.
