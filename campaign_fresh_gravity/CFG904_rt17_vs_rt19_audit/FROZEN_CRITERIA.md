# CFG904 — RT-17 versus RT-19: frozen criteria (committed alone, before any script)

Block 900–909 (reserved in LEDGER.md). Audit lane for CFG894 prerequisite **P4** (KAPPA_DOORS.md). This is **not** a new
κ attempt: it recomputes two existing records and settles which one stands. κ = ½ is FITTED (CFG493: κ_Λ = 0.417 ± 0.095 on
ρ_DE). Never cite de Sitter–Unruh for κ = ½. Never "theory closed".

## 1. The records under audit (read-only; blobs pinned)

| tag | file | blob at HEAD | claim |
|---|---|---|---|
| RT-17 | `reviews/mi_kernel_measure_from_desitter_2026.py` (commit a96497f0e) | ede61ff97854 | KMS at T_GH fixes the kernel variable: identification I1 `w = x` gives Z = 2π, κ = √(2/(3π)) = 0.4607, "the first genuinely PREDICTED κ", "no data input" |
| RT-19 | `reviews/mi_dsunruh_kernel_package_2026.py` (commit e54059e9c) | d09e0f9bfee9 | the dS–Unruh ΔT construction forces a₀ = 2cH_Λ (Z = ½, κ = 5.79); RT-17's cH_Λ/2π "is WITHDRAWN -- it disagrees with the correct reading by 4π" |

Downstream presentations (P4): PAPER6 §"The observable side" ("the only coefficient-free identification in hand is
a₀ = c²/(2πL_dS), i.e. κ = 0.4607"), its source `kappa_closure/k03_half_vs_two_pi_precision.py`, and AS066.

## 2. Inputs and conventions (from the record; no measured value enters any test)

- Law: a₀ = κ c √(G ρ_DE); H_Λ² = 8πGρ_DE/3; Z ≡ cH_Λ/a₀ = √(8π/3)/κ (KAPPA_CAMPAIGN_RULES §0).
- T_GH = ħH_Λ/(2πk_B) (RT-17 L1). Unruh: T_U(a) = ħa/(2πck_B) (invoked by RT-17 L1a, "the same 2π as in Unruh's a/2πc").
- dS–Unruh: T(a) = (ħ/2πck_B)√(a² + a_dS²), a_dS = cH_Λ; Milgrom-1999 ansatz μ(a) = [T(a) − T(0)]/T_U(a) (RT-19 D1).
- Kernel variable w = ωc/a₀ (RT-17 L1b; prep_2026/mi_fingerprint/KERNEL_THEORY.md §2). α = 1 kernel
  μ₁(x) = (√(1+4x²) − 1)/(2x) (RT-19 D2; KERNEL_THEORY.md Theorem A).
- Symbols only: G, c, ρ_DE, ħ, k_B, ω, a, a_dS. Measured numbers appear only in report-only window lines (W_data
  [0.227, 0.607], ρ_DE, from KAPPA_CAMPAIGN_RULES §7).
- **Footing:** ρ_DE (κ values on this footing). Z statements are footing-free statements about cH_Λ.

## 3. Option space Ω (declared now, from KAPPA_DOORS P4)

κ ∈ {0.4607 (Z = 2π), 0.921 (Z = π), 0.230 (Z = 4π), 2.894 (Z = 1), 5.79 (Z = ½)}. Any other value that a recomputation
produces is reported as found, never forced into Ω.

**π-parity and ħ (declared).** Both chains use only a₀ and H_Λ (a-and-H class, `odd`): κ² ∈ ℚ·π^odd, so exact ½ is
impossible in either (CFG263, L4). ħ enters both through a temperature; it must cancel — in RT-17 inside x = ħω/(k_B T_GH), in
RT-19 inside the ratio μ. The script prints both cancellations.

## 4. Tests (each PASS/FAIL, printed with its evidence)

- **T1 RT-17 arithmetic.** Recompute L1–L2 step by step in sympy: T_GH → x → w → Z(λ) = 2πλ → κ = √(8π/3)/Z. PASS iff I1
  gives Z = 2π and κ = √(2/(3π)) exactly and I1–I4 reproduce RT-17's listed values.
- **T2 RT-17 determinacy** (KAPPA_CAMPAIGN_RULES §4). Does any equation of the RT-17 chain select λ? The admissible set is
  RT-17's own four identifications I1–I4 ("every natural way ... enumerated"). PASS iff some equation of the chain fixes λ,
  or the κ spread over I1–I4 is smaller than the W_data width (0.380). Otherwise RT-17 is a **MENU**.
- **T3 RT-17 internal consistency.** RT-17 reads I1 as "a₀ is the de Sitter–Unruh scale" and ties its 2π to Unruh's. PASS iff
  T_U(a₀^I1) = T_GH exactly. Otherwise report the ratio and the a₀ that the Unruh relation gives.
- **T4 RT-19 chain.** Recompute D1–D5: μ_dS closed form and limits; scale λ in μ_dS(λx) ≡ μ₁(x) solved (not assumed) from
  the series and then verified on the full function; uniqueness of λ; the D5 ratio Z_RT17/Z_RT19. PASS iff the residual
  vanishes identically at a unique λ and a₀ = λ a_dS = 2cH_Λ follows. Report-only: whether the deep-MOND limit alone
  (any kernel with μ → x) fixes the same scale, and whether the α = 2 kernel admits any λ.
- **T5 attribution of the 4π.** Is the 4π one error in RT-17's chain? Steps of RT-17: S1 T_GH, S2 KMS variable x, S3 kernel
  variable w with a₀ = cH_Λ/Z, S4 identification w = λx (λ = 1), S5 κ = √(8π/3)/Z. Single-step corrections evaluated:
  c1 S1 (check T_GH against the Gibbons–Hawking form), c2 S4 replaced by the Unruh-consistent reading T_U(a₀) = T_GH,
  c3 S2 replaced by the Unruh variable (equivalent to c2 if consistent), c4 S5 checked against Friedmann. Any further
  arithmetic error the recompute finds is added and reported. PASS iff some single corrected step, all else unchanged, turns
  RT-17's output into Z = ½. Otherwise factor Z_RT17/Z_RT19 into its pieces and name the step that carries each.
- **T6 identity checks** (KAPPA_CAMPAIGN_RULES §6):
  - **I4 rename test:** set the law's κ to 0.4 in the code. RT-17's and RT-19's outputs must not move (neither may use the
    law's κ upstream); only the comparison lines may change. A moved output = consistency relation, reported as such.
  - **Convention rename:** rewrite both chains with ħ → h/2π, ω → 2πν (kernel variable carried consistently), k_B → 1.
    Z must be invariant in both; a change means a convention leak.
  - **I3 scaling:** G → λG, ρ → μρ, c → νc must give a₀ → ν√(λμ) a₀ with κ invariant, for both outputs.
  - **I8 π-weight tracking:** print the π exponent of every intermediate quantity in both chains (as rational × π^k) and of
    κ²; confirm `odd` for both; locate the step at which the π-weight of Z_RT17/Z_RT19 enters.
  - **I1 grep:** the script must not contain the forbidden §2 constants (9.36e-11, 1.13e-10, 1.2e-10, 5.7888, √(32π/3) as an
    input, 0.1727). Z_FW is used only as a report-only comparison, built from the law's κ symbol.

## 5. Mutation control (separate run, `MUTATE=1`, writes `_MUTATE` outputs)

- **M1 thermal 2π → 4π** in both T_GH and the Unruh prefactor. Expected: RT-17's Z moves 2π → 4π (κ 0.4607 → 0.230);
  RT-19's μ_dS and Z = ½ do **not** move (the prefactor cancels). This is the π-locator: the same mutation must move one chain
  and leave the other fixed.
- **M2 Einstein coupling 8πG → 4πG** in Friedmann. Expected: Z unchanged in both chains, every κ × 1/√2.
- **M3 identification λ = 1 → ½** (I2). Expected: RT-17 Z → π, κ → 0.921.
- Convention (chain6): the MUTATE run exits **1** when every control bites as predicted, **3** if any fails to bite (then the
  normal-mode result is void). The normal run exits 0 when all tests were evaluated and every reproduction check held, 2 on an
  internal failure.

## 6. Verdict classes (frozen)

| class | condition | owner's term |
|---|---|---|
| V-A **RT-17 STANDS** | T1, T2, T3 all PASS | "RT-17 correct": 0.4607 is a coefficient-free (forced) dS value; RT-19's withdrawal is wrong |
| V-B **RT-19 STANDS IN FULL** | RT-17 fails T1, T2 or T3, and T4 and T5 PASS | "RT-19 correct": one 4π error in RT-17; corrected, the dS tie gives 2cH_Λ |
| V-C **WITHDRAWAL STANDS, 4π ATTRIBUTION DOES NOT** | RT-17 fails T1, T2 or T3; T4 PASS; T5 FAIL | "both wrong" as stated: 0.4607 is not a forced value (RT-19's conclusion holds), but the 4π is not one error in RT-17 |
| V-D **BOTH FAIL** | RT-17 fails T1, T2 or T3, and T4 FAILS | "both wrong", RT-19's own chain also broken |
| V-E **INCONSISTENT** | any other combination | re-examine before any record change |

Any T6 failure or a mutation control that does not bite voids the verdict (reported as VOID with the failing check).

**What each class means for the record.** Under V-A the "dS tie gives 0.461" sentence may stand. Under V-B, V-C or V-D it
must not be presented as coefficient-free, derived, forced or predicted; the allowed form is KAPPA_CAMPAIGN_RULES §10's
"route X lands at 0.461, inside today's window, not significant", with the menu named.

## 7. The file list (what counts as "presents 0.4607 as coefficient-free")

- **Search** (tracked files only; `git grep -n -E` over *.md, *.py, *.tex, *.txt, *.json, *.out, *.lean; _external_data
  excluded): `0\.4607`, `0\.46066`, `0\.461` not followed by a digit, `sqrt(2/(3` and its LaTeX forms, the cH_Λ/2π forms
  (`H_Lambda/2pi`, `H_Lambda/(2 pi)`, `H_Λ/2π`, `H_\Lambda/2\pi`, `H_\Lambda/(2\pi)`), `c^2/(2 pi L_dS)` forms and `dS tie`.
- **Pre-filter (scripted).** Keep hits with a κ context word (kappa, κ, 2π, horizon, de Sitter, dS, thermal, KMS, Unruh,
  Gibbons, Milgrom, coefficient, Z = 2π, H_Λ) on the line. Flag a hit **CLAIM** if the line or ±2 lines carry a claim word:
  coefficient-free, derive/derived/derives/derivation, forced, predict/predicted/prediction, first-principles, no data,
  parameter-free, closed form, principle-shaped, un-excluded/unexcluded, "the only", "dS tie gives", "de Sitter gives",
  "thermality gives", naturalness. Flag it **CAVEAT** if the same window carries withdrawn/WITHDRAWN, menu/MENU, RT-19,
  4π/4pi error, conflict, "not derived", "never cite", "do not cite", "not a derivation", posit, conditional.
- **Manual review.** Every CLAIM hit is read in context and classed:
  - **A (correction candidate):** presents 0.4607/0.461/√(2/(3π))/cH_Λ/2π as the value that de Sitter, horizon, thermal,
    KMS, Gibbons–Hawking or Unruh physics gives, described as coefficient-free, derived, forced, predicted, principle-shaped
    or the only un-excluded value, with no withdrawal/menu/conditional caveat in the same passage.
  - **B (compliant):** comparison value or label only, or the claim is caveated or withdrawn in the same passage.
  - **C (unrelated):** not this κ value.
  Snapshot or generated copies (source_snapshots/, raw_output.json, .out of a listed script) are listed but marked as copies.
- **Miss-rate check.** A seeded random sample of 40 non-CLAIM context hits is read by hand; the number found to be class A is
  reported, so the reader knows how much the keyword filter may miss.
- The list is report-only. No listed file is edited by this lane. The CFG894 register row is proposed in the README, not
  appended (that file belongs to CFG894).

## 8. Second prediction (S4)

Not applicable: an audit lane, not a derivation attempt. It adds no trial to the look-elsewhere count.
