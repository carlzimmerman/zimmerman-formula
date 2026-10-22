# A61 — THE K CONVENTION AND THE 16.99 pc COINCIDENCE

Lane A61. `a61_checks.py` (19 checks, 19/19 PASS, exit 0, 2 s, sympy only), `a61.out`,
`a61_results.json` (every number below), `MUTATE.md` (5 mutations, each breaks a different check).
Constants: BRIEF §4, plus `σ_c = 8.33 km/s` (A20 candidate 1) and the `10⁴ K, μ = 1.22` thermal width
`8.23 km/s` (A16/A20). No fitted constant is introduced. Read first: A37 §3.2, A33 §1.1, A16 §"What this
does not do" #4, A20 §Derivation.

## Claim

**There is one coupling, `K = 4πG`, and "K = 8πG" is not a second convention but a factor-2 mislabel of the
same symbol.** The action's Einstein–Hilbert normalisation `1/(4K)` is `1/(16πG)`, the static lapse equation
gives `∇²Φ = Kρ`, and the Friedmann coefficient `8πG` is `2K`. Three "πG" numbers, one coupling:
`16πG = 4K`, `8πG = 2K`, `4πG = K`. With K fixed, **`L* = 24.02 pc`** and **`16.99 pc` is `λ_P = L*/√2`** —
a different object, not the same object in another convention. The "coincidence" is an **exact identity**,
`L*(2K) ≡ λ_P(K) = √(γ/K)`, true for every γ and every K, and therefore carrying **zero** information: it is
the same factor 2 that sits in `γ = KL*²/2` and in `m² = K/η`. R_core = π√(γ/4πG) depends on γ **alone**, so
the physics is K-invariant — but every formula in the record is written in `L*`, so a K-slip moves every
quoted number by exactly 1.41×. That is why the convention is load-bearing here, and why the record's
`L*`-anchor (not γ) is the thing that must be got right. Corrected
numbers: `K = 4πG`, `L* = 24.025 pc`, `λ_P = 16.988 pc`, `R_core = 53.37 pc`, `r_switch = 3.73 / 18.43 pc`
(MW / dwarf), `λ_J = 106.74 pc`, and **A20's window `[24.0, 90.0] pc` stands unchanged**.

## 1. K from the action

**(1) Einstein–Hilbert normalisation.** The A33 §1 action's gravitational slot is
`(R3 + K_ijK^ij − (1+β)θ² − 2Λ)/(4K)`. The standard ADM form of `(R−2Λ)/(16πG)` is
`(R3 + θ² − K_ijK^ij − 2Λ)/(16πG)`. Matching coefficients, `1/(4K) = 1/(16πG)` has the **unique** root

    K = 4πG = 8.387172739e-10 m³ kg⁻¹ s⁻².                                              [K1]

The identification uses the `R3` coefficient, which is `+1` in both forms and is unaffected by the sign
convention of the extrinsic-curvature term (A33 prints that term with the opposite sign to its own lapse
equation — a separate defect, no number affected). There is no second root and no free normalisation: `G`
*is* the coefficient of `R` in the EH action. (A33 §1.1
states the same value but calls the BRIEF's K "a different symbol"; the sentence it gives for it —
"`G_μν = 2KT_μν` with `K = 4πG`" — already shows it is the same symbol multiplied by 2, since `2K = 8πG`.)

**(2) Poisson.** Computed from scratch rather than quoted: for `h_ij = (1−2Φ)δ_ij` the linearised 3-Ricci
scalar is exactly `4∇²Φ` (K2a, sympy, residual 0). The static lapse equation `R3 = 2Λ + 4Kρ` at `Λ = 0` then
gives

    ∇²Φ = Kρ   ⇒   K = 4πG.                                                             [K2b]

This is the sharpest statement in the lane: **with K = 8πG the action's Newtonian limit would be
`∇²Φ = 8πGρ`, i.e. `G_eff = 2G`.** No measurement of G survives that, so 8πG is not an admissible value of
this symbol.

**(3) Friedmann.** A33's (F1) at β = 0 is `3(2+3β)H² = 2Λ + 4Kρ`, i.e. `6H² = 2Λ + 4Kρ`, i.e.

    H² = Λ/3 + (2K/3)ρ = Λ/3 + 8πGρ/3.                                                 [K3]

**The "8πG/3" of the Friedmann equation is `2K/3`, not K.** The same 2 appears in `ρ_Λ = Λc²/(8πG)` and in
the quadratic term of W (§2), which is why the mislabel is so easy to make and why it propagated.

**Census.** `16πG = 4K = 3.354869096e-9`; `8πG = 2K = 1.677434548e-9`; `4πG = K = 8.387172739e-10` [K4].
So the answer to the question as posed: **the 8πG in BRIEF and the 4πG in A33 are the same glyph used for two
different objects, and their ratio is exactly 2.** The BRIEF's K is the Einstein-tensor normalisation
(`G_μν = 2KT_μν`), the action's K is the inverse EH coefficient. They are not two conventions for one object;
they are one coupling written with and without its factor 2.

## 2. Where K appears, and where it cancels

**(4) W.** `W(u) = (a₀²/K)[−u/a₀ − ln(1−u/a₀)] = u²/(2K) + u³/(6a₀K) + O(u⁴)` [K5]. The quadratic
coefficient is `1/(2K) = 1/(8πG)` at K = 4πG. The formula in the task, `W = u²/(2a₀)`, is **not** in the
record and is dimensionally an acceleration (dim `(0,1,−2)`), not an energy density (`(1,−1,−2)` = Pa); A22
line 163 and A33's mutation table both carry the correct `u²/(2K)`. This is a third instance of the same
glyph confusion: `a₀` and `K` differ in dimensions by `[m² kg⁻¹ s⁻²]` and cannot be interchanged.

**(5) The law cannot see K.** `KW′(u) = u/(1−u/a₀)` exactly, with no K left (K6, residual 0). The K in the
prefactor cancels the K inside `u = K|P|`: `W′` carries `1/K`, `u` carries `K`. Hence no galactic observable
outside the stiffness sector can measure K, and no redefinition of K can change the law `g = u/(1−u/a₀)`.

**(6) The P equation's source.** The source is `KW′(u)P_i`, i.e. again `u/(1−u/a₀)·P_i` — K-free once
written in u. The gradient term's contribution to the lapse equation is
`4K·(γ/2)(D·P)² = 2γ(D·u)²/K = L*²(D·u)²` when `γ = KL*²/2`. **The P sector's entire contribution to the
field equation is L*'s, not K's.** Every occurrence of K in a physical ratio is either cancelled (as here) or
enters only through `γ/K`.

## 3. γ is the physical coefficient; `γ = KL*²/2` is its 4πG spelling

**(7)** A16/A20's equation of state is `p = (γ/2)ρ_c² = πGL*²ρ_c²`, i.e.

    γ = 2πGL*²,   K-free.                                                               [K7]

**(8)** `γ = KL*²/2` equals (7) **iff K = 4πG**. In an 8πG spelling the coefficient must be **1/4**, not 1/2:
`(8πG)L*²/4 = 2πGL*²` [K8]. The formula is therefore *not portable* — it carries the convention inside it.
This is the technical core of the lane: **the "2" in `γ = KL*²/2` is the same 2 that distinguishes K from
2K**, so a document that changes K without changing that coefficient silently doubles γ.

**(9) The polytrope.** `p = (γ/2)ρ²` ⟹ `a² = γ/(4πG)` ⟹

    R_core = πa = π√(γ/4πG) = (π/√2)L*,                                             [K13]

a function of **γ alone**. As a function of γ it cannot move under a K relabel (K13: `dR_core/dK = 0`), and it
does move by √2 when γ doubles.

## 4. The two conventions, tabulated

Three books, not two. Column (a) is the action's own convention. Column (b) holds γ fixed and relabels
K = 8πG, then uses the record's `L*`-formulas — the reading A37/A58 describe. Column (c) holds L* = 24.02 pc
fixed and recomputes γ from `γ = KL*²/2` with K = 8πG — the reading A16 §"What this does not do" #4
quantifies, and the one the record's own bookkeeping produces, because the record anchors L* and derives γ.

| quantity | formula | (a) K = 4πG, γ = 2πGL*² | (b) K = 8πG, same γ | (c) K = 8πG, L* held |
|---|---|---|---|---|
| γ (SI: m⁵kg⁻¹s⁻²) | `2πGL*²` / `KL*²/2` | 2.304697e26 | 2.304697e26 | 4.609395e26 |
| `L*` (pc) | `√(2γ/K)` | **24.025** | 16.988 | 24.025 |
| `λ_P` (pc) | `L*/√2 = √(γ/K)` | **16.988** | 12.013 | 16.988 |
| `R_core` (pc) | `(π/√2)L*` | **53.370** | 37.738 | 75.477 |
| `r_switch` MW (pc) | `L*√f_c` | **3.7297** | 2.6373 | 5.2746 |
| `r_switch` dwarf (pc) | `L*√f_c` | **18.426** | 13.029 | 26.058 |
| `λ_J` (pc) | `√2πL*` | **106.740** | 75.477 | 150.954 |
| **`R_core` from γ** | `π√(γ/4πG)` | **53.370** | **53.370** | 75.477 |
| σ_c implied (km/s) | `√(a₀L*)` | **8.326** | 7.005 | 8.326 |
| A20 window in L* (pc) | `[L*, R0.3/(π/√2)]` | **[24.03, 90.03]** | [16.99, 90.03] | [24.03, 63.66] |

Every entry is in `a61_results.json`; K12 checks the closed forms and the √2 ratios.

**Reading the table.** The last-but-three row is the discriminator. `R_core` depends on γ alone (§3 eq. 9),
so in (a) and (b) the physics gives **53.370 pc** — yet the record's `L*`-formula `(π/√2)L*` returns 53.370 in
(a) and **37.738** in (b). That gap is the whole story: **the physics is K-invariant, but every formula in the
record is written in `L*`, so a K-slip corrupts every quoted number by √2.** K13/K17/K18 prove the invariance
of `R_core`, `r_switch` and `λ_J` as functions of γ; the `L*`-formulas for them are not invariant, which is
exactly why the convention matters in practice.

- **(a) is internally consistent.** All four formulas agree with the γ-only expressions; `L*(4πG)` and
  `λ_P(4πG)` differ by exactly √2 [K9].
- **(b) contradicts itself.** It keeps γ (so the core is 53.370 pc) while its `L*`-formulas return 37.738 pc.
  The label moved and the physics did not, so (b) is not a description of a different theory — it is a
  description of the same theory with one number wrong. Note that `L*(8πG)` is **the 4πG `λ_P`** (§5).
- **(c) is self-consistent but a different theory.** It doubles γ, so the core really is 75.477 pc (×1.4142),
  `r_switch` ×√2, `λ_J` ×√2, and it also breaks the EH normalisation (`G_eff = 2G`).

**Which matches A20's inner cores.** Column (a): `R_core = 53.370 pc`, **3.75×** below IC_10's 200 pc
turnover, and `σ_c = √(a₀L*) = 8.326 km/s`, **1.012×** the `10⁴ K, μ = 1.22` thermal width of 8.23 km/s
(8.2255 km/s recomputed here) — the 1.2 % that A20's candidate 1 quotes. Book (b) keeps γ, so its core is
53.370 pc, but its `L*`-formulas return 37.738 pc and an implied `σ_c = 7.005 km/s`, **0.851×** the thermal
width: a **15.9 %** miss, which is the empirical face of the same √2. Book (c) gives 75.477 pc, 1.4142× too
large and only 2.65× below the turnover, with `σ_c = 8.326` unchanged. A20's C4 gate (`σ_c ≤ 2×8.23`) is
passed by all three, so the gate does not decide; the *match* does — 1.2 % for (a) against 15.9 % for the 17 pc
number, on top of (b)'s self-contradiction and (c)'s `G_eff = 2G`.

## 5. The coincidence test

**(10)** The P mass from the action is `m² = K/η` (A33 §3.6), so `λ_P = 1/m = √(η/K)`; with A33's
status-C choice `η = γ`,

    λ_P = √(γ/K) = L*/√2.                                                               [K11]

**(11)** `L*² = 2γ/K` and `λ_P² = γ/K` give `L* = √2 λ_P` — exact, no numbers.

**(12)** Therefore, for arbitrary γ and arbitrary K,

    L*(2K) = √(2γ/(2K)) = √(γ/K) = λ_P(K).                                             [K10]

**This is an identity, not a coincidence, and the residual is exactly 0** (sympy, symbolic γ and K). It is
also *not* a statement about 24 or 17: it holds at γ = 1, K = 1. The 16.99 pc that A37 saw twice is
`√(γ₀/4πG)` computed once as `L*` at K = 8πG and once as `λ_P` at K = 4πG. **Note the direction**: the 8πG
`L*` equals the 4πG `λ_P`; the prompt's phrasing ("L*(4πG) = λ_P(8πG)") has the conventions on the wrong
sides — `λ_P(8πG) = 12.013 pc` and `L*(4πG) = 2λ_P(8πG)`. A37 §3.2 states it correctly in the body but
loosely in the summary line.

**(13)** The identity has one premise: `η = γ`. Without it `L*/λ_P = √(2γ/η) = √2 c_s`, so the general
statement is `L*(2K) = c_s λ_P(K)` [K11]. The √2 in `L* = √2λ_P` is the same √2 as in `K = 2K`, both coming
from the factor 2 in `γ = KL*²/2`.

**(14) The 0.1 % residual is bookkeeping.** `16.9882` vs `16.9706` is `24.025/√2` vs `24.000/√2`; the ratio
1.001042 decomposes as `1.0010332` (the `(8.33/8.3257)²` σ_c ratio) times `1.0000088` (the `24.000` vs
`L*(8.3257) = 24.0002` pc rounding) [K16]. Both factors are bookkeeping — the three σ_c values in the record
(8.23 / 8.3257 / 8.33 km/s) and the 24 pc rounding — and neither is a residual of the identity. So: **the algebraic relation is exact; the
numerical near-match is limited only by which σ_c the record uses.**

## 6. Verdict

1. **One convention: `K = 4πG`.** Fixed three ways (§1), and the only value for which the printed action has
   the correct Newtonian limit. BRIEF §1's `K = 8πG` is a factor-2 error, not a convention.
2. **One number: `L* = 24.025 pc`** (σ_c = 8.33 km/s), `λ_P = 16.988 pc`, `R_core = 53.370 pc`,
   `r_switch = 3.7297 pc` (MW) / `18.426 pc` (dwarf), `λ_J = 106.740 pc`.
3. **`16.99 pc` is `λ_P`, not `L*`** — and the fact that `L*(8πG) = λ_P(4πG)` is an identity means the
   numerical coincidence can never be used as evidence for either a convention slip or its absence.
4. **A20's window does not move: `[24.0, 90.0] pc`.** The lower end is `σ_c²/a₀` (no G, no K in it); the
   upper end is `R0.3/(π/√2) = 200/2.22144 = 90.03 pc`. Both were computed in the correct convention. If the
   8πG label were adopted *with L\* held*, the window would become [24.0, 63.66] pc (top ÷ √2) and every
   stiffness prediction would move by 1.41× — which is the size of the error being avoided, not a correction
   to A20.
5. **No number in A16/A20/A22/A33 changes.** No lane ever *evaluated* a formula with K = 8πG: A16 states the
   cost explicitly (c_s² doubles, `λ_J = 2πL*`, `r_switch = √2L*` — the (c) column), and A22/A33/A45 use 4πG.
   A37 and A58 quote 16.99 pc only as a warning. The only carriers of the mislabel are BRIEF §1 and the two
   sentences that quote it, so the correction is a label, not a recomputation.

## Status

**`DERIVED`** for §1–3 and §5 (every identity exact, sympy residual 0, including the 3-Ricci coefficient
computed from the metric rather than quoted) **+ `NUMERICAL`** for §4 and §6.

## Checks

`a61_checks.py`, 19/19 PASS, exit 0, 2 s, sympy, no network.

| id | proves | measured |
|---|---|---|
| K1 | `1/(4K) = 1/(16πG)` has the unique root `K = 4πG` | residual 0 |
| K2a | linearised `R3` of `h_ij=(1−2Φ)δ_ij` is `4∇²Φ` | residual 0 (from the metric) |
| K2b | static lapse ⟹ `∇²Φ = Kρ`; 8πG would give `G_eff = 2G` | 8.387173e-10 = 4πG |
| K3 | F1 at β=0 ⟹ `H² = Λ/3 + 2Kρ/3 = Λ/3 + 8πGρ/3` | residual 0 |
| K4 | `16πG = 4K`, `8πG = 2K`, `4πG = K`; BRIEF/action = 2 | exact |
| K5 | `W = u²/(2K) + …`; `u²/(2a₀)` is an acceleration, not a pressure | 5.9615e8 ; dims differ |
| K6 | `KW′(u) = u/(1−u/a₀)` — no K | residual 0 |
| K7 | `γ = 2πGL*²`; `p = πGL*²ρ²` | ratio 1.0 |
| K8 | `γ = KL*²/2` doubles at K=8πG; coefficient must be 1/4 | 2.000000 ; 0.25 |
| K9 | `L*(4πG)/L*(8πG) = √2` | 24.0250/16.9882 = 1.414213562 |
| K10 | `L*(2K) = λ_P(K) = √(γ/K)` identically | residual 0, symbolic γ, K |
| K11 | `λ_P = √(η/K)`; identity needs η = γ, else `L*(2K) = c_sλ_P(K)` | 1.4142 |
| K12 | the number table and its √2 ratios | 53.37/37.74/75.48 ; 3.73/18.43 ; 106.7 |
| K13 | `R_core = π√(γ/4πG)`; `dR_core/dK = 0` at fixed γ | 0 ; `= (π/√2)L*` |
| K14 | window `[24.03, 90.03]`; 8πG top = 63.66 = 90.03/√2 | exact |
| K15 | `σ_c(24.0) = 8.3257`, `σ_c(16.99) = 7.005`, thermal 8.2255 km/s | ratios 1.0116 / 0.8511 |
| K16 | the 0.104 % = 0.1033 % σ_c ratio + 8.8e-6 rounding, not the identity | 1.033213e-3 ; 1.042157e-3 |
| K17 | `r_switch² = γf_c/2πG` — no K | residual 0 |
| K18 | `λ_J² = πγ/G` — no K | residual 0 |

## What this does not do

1. **It does not measure `L*`.** 24.025 pc is A20's window bottom, and `σ_c = 8.33 km/s` is an external
   thermal input (`10⁴ K`, `μ = 1.22` gives 8.2255, a 1.3 % miss), not a theorem.
2. **It does not decide `η = γ`.** The identity `L*(2K) = λ_P(K)` is conditional on it; with `η ≠ γ` the
   relation is `L*(2K) = c_s λ_P(K)` and the numerical coincidence weakens by `c_s`.
3. **It does not audit the published record.** Only the lane directories, `THEORY.md` and `FINAL_THEORY.md`
   of this push were scanned for `K`; the Zenodo papers were not checked for an `8πG` spelling.
4. **It does not re-derive A20's polytrope or `f_c`.** Those are taken as given; what is checked is the
   algebra connecting them to γ and K.
5. **It does not claim a detection.** A20's window is a null (SPARC) plus a one-sided bound (LITTLE THINGS).

## Next

1. **BRIEF §1:** `K = 8πG` → `K = 4πG`, with the parenthetical "(the EH normalisation; the Friedmann
   coefficient is `2K = 8πG`)".
2. **Coefficient table:** replace `γ = KL*²/2` with `γ = 2πGL*²`, and keep `L*² := 2γ/K` only as a 4πG
   restatement. Same for `η [L²]` → `η = γ = m⁵kg⁻¹s⁻²` (the `[L²]` tags are the `G = 1` reading).
3. **A37 §3.2 and A58's "Next" #5** to be reworded: the `8πG` value is `λ_P`, not "L* under another
   convention"; the identity should be stated once, as `L*(2K) = λ_P(K)`.
4. **`parent_audit.py`:** add the four K-free relations `γ = 2πGL*²`, `R_core = π√(γ/4πG)`,
   `r_switch² = γf_c/2πG`, `λ_J² = πγ/G` so no future lane can reintroduce a K into them.
5. **Do not re-run A20.** The window is convention-clean; only the label changes.