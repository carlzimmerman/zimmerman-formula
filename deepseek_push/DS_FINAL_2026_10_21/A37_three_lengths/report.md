# A37 — THE THREE LENGTHS

Lane A37. `a37_checks.py` (10 checks, 10/10 PASS, exit 0), `a37.out`, `a37_results.json`
(symbol table and audit as data), `MUTATE.md` (5 mutations, each breaks a different check).
Constants: BRIEF §4 only, plus `σ_c = 8.33 km/s` (A20 candidate 1, the number the task names).
No fitted constant is introduced. Deterministic, stdlib + sympy, 1.1 s.

## Claim

**There is one length, not three.** `c²/a₀` is the only dimensionful length the framework owns;
the other two objects are that length multiplied by a pure number —
`ℓ₁ = κ·(c²/a₀)` and `L* = (σ_c/c)²·(c²/a₀)`. The record writes all three as `L`, `ℓ₀` or
`L*`, so a symbol swap is not a typo but a factor between 2 and 1.7e18. The audit finds
**six conflation sites**; five are arithmetically harmless because the length cancels or the
number was never used, **one conclusion is withdrawn** (A11's superluminal window), and the
single worst conflation — the coordinator's brief defining `L* = c²/a₀`, 1.297e9× too large — was
caught by A30 before it reached a number. **But the theory document still carries the collision
live**: `FINAL_THEORY.md` §0 line 28 defines `ℓ₀ ≡ √(8π/Λ)` (the cell) while §1.4 line 134 uses
`ℓ₀` as `c²/a₀` (the MOND length). Substituting one into the other returns `R = 1`, `κ = 1` —
the value the data exclude at 6.14σ. Correction item #10 names the inconsistency but neither
equation was changed.

## 1. The three objects

| object | adopted symbol | definition | value (m) | value (pc) | value (Gpc) | what fixes it |
|---|---|---|---|---|---|---|
| MOND length | `L_MOND` | `c²/a₀` | 9.6021e26 | 3.1118e10 | **31.12** | `a₀` — measured; footing-dependent (`7.9536e26 m = 25.78 Gpc` on the alt footing) |
| vacuum cell length | `ell_1` | `√(8π/Λ)` | 4.8040e26 | 1.5569e10 | **15.57** | `Λ` alone (a₀-free) |
| stiffness length | `L*` | `σ_c²/a₀ = √(2γ/K)` | 7.4133e17 | **24.03** | 2.40e-8 | the cold medium's dispersion `σ_c` (equivalently `γ`) |

Derived, not independent: `r_H = √(3/Λ) = 1.6598e26 m = 5.379 Gpc`;
`c/H₀ = 1.3725e26 m = 4.448 Gpc`; `λ_P = L*/√2 = 16.9706 pc` (16.9882 pc at `σ_c = 8.33`).
`L*` is quoted as 24 pc throughout the record; the exact `σ_c = 8.33 km/s` value is 24.025 pc
(A20's `σ_c = 8.23 km/s` gives 23.45 pc; the 2.4 % is `(8.33/8.23)²` — the thermal width at
`μ = 1.22` vs the inversion of `L* = 24 pc`. Both are in the record and neither is a new
parameter; the symbol table must say which.)

**What each is, in one line.** `L_MOND` is the Rindler-horizon distance `c²/a` of an observer
at the law's own acceleration `a₀` — which is why it is a horizon-scale object (7.00 `c/H₀`,
5.79 `r_H`). `ell_1` is the radius of the 4-ball whose area times `Λ` equals the Euler charge
`32π²χ` (A19 eq. 6) — a pure vacuum construction, no `a₀`. `L*` is the *same functional* `c²/a` with
the cold medium's dispersion in place of `c`, i.e. the distance over which the medium's elastic
stress can hold itself up.

## 2. The exact relations

Symbols: `Λ > 0`, `ρ_Λ = Λc²/(8πG)`, `κ := a₀/(c√(Gρ_Λ))`, `R := u/(a₀²/G)` with
`u = Λc⁴/(8πG)`. All verified in sympy, residuals **exactly 0** (K2, K3).

    (1)  L_MOND ≡ c²/a₀                                    [definition]
    (2)  ell_1  ≡ √(8π/Λ)                                  [definition]
    (3)  κ ≡ ell_1/L_MOND = a₀√(8π/Λ)/c²                   [identity, given a₀ = κc√(Gρ_Λ)]
    (4)  R ≡ Λc⁴/(8πa₀²) = ΛL_MOND²/(8π) = (L_MOND/ell_1)² = 1/κ²
    (5)  L_MOND = 2 ell_1  ⟺  κ = ½  ⟺  R = 4  ⟺  ΛL_MOND² = 32π
                          ⟺  a₀ = c²√(Λ/32π) = 9.354173e-11 m/s²
    (6)  L*/L_MOND = σ_c²/c²                               [given L* = σ_c²/a₀]
    (7)  L*/ell_1  = (σ_c²/c²)/κ = 2(σ_c/c)²  at κ = ½
    (8)  λ_P = L*/√2  ⇒  m_P = ħ/(c λ_P)

**On (5).** The three statements are one equation, not three: `solve` returns the *same*
single root `a₀ = c²√(Λ/32π)` for each, and that root is the only place the ratio is 2. At the
BRIEF's rounded footing `a₀ = 9.36e-11` the ratio is **1.99876** (κ = 0.500311, R = 3.99502,
reproducing A19's K2 to every quoted digit), so `L_MOND = 2ell_1` is a statement of the
*closure*, not of the definitions. This matters for reading: `ΛL_MOND² = 32π` is exact only at
`a₀ = 9.354173e-11`, and the 0.06 % by which the footing misses it is the footing's rounding,
not physics.

**On (6) — the hierarchy.** Substituting the two definitions,

    L*/L_MOND = (σ_c²/a₀)/(c²/a₀) = σ_c²/c²,   exactly; nothing else survives.

With `σ_c = 8.33 km/s`: `σ_c/c = 2.7786e-5`,
`L*/L_MOND = 7.7206e-10`, **`log₁₀ = −9.1124`** (9.11 decades), `L*/ell_1 = 1.5432e-9`
(−8.81 decades), `L*/(c/H₀) = 5.40e-9` (−8.27 decades). **The stiffness length sits nine
decades below the MOND length because the cold medium is non-relativistic**: both lengths are
`c²/a₀` with a speed inserted, and the medium's speed is `2.78e-5 c`, so its length is the
MOND length suppressed by `(v/c)²`.

Equivalently, the whole hierarchy is one number and two coefficients:
`L_MOND = c²/a₀`, `ell_1 = κ L_MOND`, `L* = (σ_c/c)² L_MOND`. There is no second scale to
derive, only the two pure numbers `κ` and `σ_c/c`.

**On the horizon relations.** At the closure `L_MOND = Z r_H` with `Z = 2√(8π/3) = 5.788810`
and `ell_1 = √(8π/3)·r_H = 2.894405 r_H` (the cell is super-horizon, A19 K14). At the rounded
footing `L_MOND/r_H = 5.7852`, 0.06 % low — again the footing, not the identity. The record's
"`a₀/(cH₀) = 1/7`" numerology is exactly `L_MOND = 7.00 c/H₀`: the MOND length **is** a
horizon-scale length, which is why the coincidence exists at all and why it carries no
information about `κ` (A1).

## 3. Audit of A1..A35

Method: every `.md` and `.py` in the 34 lane directories plus `FINAL_THEORY.md` was scanned for
the glyph families (`a37_checks.py` K5). Census: **`L*`-token lines 538, `ell_1` 68, `ell_0`
19, `λ` 383** in 120 files. The definitions attached to a single glyph were extracted
separately; the point is not that the glyphs are frequent but that each carries **more than one
definition**:

| glyph | definitions found | where |
|---|---|---|
| `ell_0` | `√(8π/Λ)` (cell) **and** `c²/a₀` (MOND) | `FINAL_THEORY.md:28` vs `A15/report.md:29`; `A31:333` quotes the clash |
| `L` | `c²/a₀` (MOND) **and** a kernel label (Lorentzian) | `A19:14,44`, `A27:31`, `A33:94` vs `A25:45,118` (30+ uses) |
| `L*` | `σ_c²/a₀` (stiffness) **and** `c²/a₀` (the brief's error) | 17 sites for the first, 6 for the second — all 6 are the *rejection* |
| `λ` | `λ_J`, `λ_FS`, `λ_max`, `λ_P` (lengths) **and** `n−1` (dimensionless) | `A16`, `A27`, `A22` vs `A35:41` |
| "cell" | `3.866652e-15 m`, `4.804e26 m`, `9.602e26 m` | `A1:128`, `A19:44`, `A19:129` |

### 3.1 The conflations, with cost and survival

| # | site | glyph used as | should be | cost | conclusion survives? |
|---|---|---|---|---|---|
| **C1** | `FINAL_THEORY.md:28` | `ell_0 ≡ √(8π/Λ)`, then `a₀ = c²/(2ell_0)` | `ell_1`, with `a₀ = c²/L_MOND` | the `κ=½` special case written as a definition: on the alt footing it returns `a₀` 17 % low | **yes** (the equation is right at `κ=½`; it is not right as a definition) |
| **C2** | `FINAL_THEORY.md:134` | `Λell_0² = 32π` — needs `ell_0 = c²/a₀` | `L_MOND` | substitute C1's `ell_0`: `Λell_0² = 8π` → `R = 1`, `κ = 1`, excluded at **6.14σ** | **yes** (the boxed identity is right in `L`; the document is self-refuting as printed) |
| **C3** | `A19_scale_functional/a19_checks.py:410` (and `:16`) | `ell0` is both the cell radius (`A = 4πell0²`) and the MOND length (`u·ell0²`) in one line | `ell_1`, `L_MOND` | none: the same glyph cancels, `P_max = u/4π` for any cell | **yes** — and the *code* uses `c²/a₀` consistently (line 416), so only the prose is fused |
| **C4** | `FINAL_THEORY.md:588` (recorded), origin: the a_P brief | `L* = c²/a₀` | `L_MOND` | `a_P = GM/L²` falls by **1.6777e18**: `1.4394e-34` instead of `2.4148e-16 m/s²` — the P sector's only independent observable would be called zero | **yes** — A30 K4 refused it; A22 uses 24 pc |
| **C5** | `A11_cold_normalization/report.md:133` | `c_s = 0.72c`, hence `L*(c_s = c) = 33.311 pc` | `c_s = 0.720473 m/s`, `L*(c_s=c) = 9.9865e9 pc = 9.99 Gpc` | **8.477 decades** in a length then compared with the 24 pc window; "91 % of the window is superluminal" inverts | **NO — withdrawn** (FINAL #2, A31 C108) |
| **C6** | `A16_cutoffs_edge/report.md:23,11,137` | `L*` for every root of the stiffness law | `L* = 24 pc` only for the physical value | `L*` spans `24 pc → 33.31 pc → 14.315 Mpc → 4.44e11 pc → 9.99 Gpc` in one report: **10.27 decades** | **yes** (no arithmetic error; highest-risk text) |

C4 and C5 are the two that would have changed a physics conclusion; C4 was caught before use,
C5 after. C1/C2 are the only ones still live in the document a reader will pick up first.

### 3.2 Adjacent defects (not length swaps, but they move a length)

- **`K` has two values.** BRIEF §1 says `K = 8πG`; A16 states `K = 4πG` and A22/A33 use it
  (`γ = KL*²/2 = 2πGL*²`). Since `L*² ≡ 2γ/K`, the same `γ` gives **24.02 pc** under `4πG` and
  **16.99 pc** under `8πG`. That second number is, to 0.1 %, `λ_P = L*/√2 = 16.97 pc` — **a
  `K`-convention slip is numerically indistinguishable from swapping `L*` for `λ_P`.** No lane
  mixes the two inside one derivation, but the definition is not portable as written.
- **`σ_c` has three values**: 8.23 km/s (`10⁴ K`, `μ = 1.22`), 8.3257 km/s (`√(a₀L*)` at
  24 pc), 8.33 km/s (A20 cand. 1). They differ by 1.2 % and correspond to 23.45 / 24.00 /
  24.03 pc. Harmless, but the symbol table must say which.
- **"One quantum per cell"** is used as a κ-candidate twice with different cells: A1's horizon
  entropy cell `3.866652e-15 m` and A19's `a₀`-cell `9.602e26 m` — **41.4 decades** apart. A1
  itself measured the hazard (P1c: attaching the strain to the cell instead of the horizon
  moves `a₀` by 40 orders). Neither derivation is wrong; the *phrase* is not identifiable.

## 4. The symbols table this programme should adopt

| symbol | object | definition | value | appears in | rule |
|---|---|---|---|---|---|
| `L_MOND` | MOND length | `c²/a₀` | 9.6021e26 m = 31.12 Gpc | closure, κ ledger | the law uses `a₀`; if a length is ever needed it is this one |
| `ell_1` | vacuum cell length | `√(8π/Λ)` | 4.8040e26 m = 15.57 Gpc | vacuum closure only | `L_MOND = ell_1/κ`; `ell_1` never appears in a galactic formula |
| `L*` | stiffness length | `σ_c²/a₀ = √(2γ/K)` | 7.4133e17 m = 24.03 pc | `r_switch`, `R_core`, `λ_J`, `a_P` | stiffness physics only; never a horizon-scale number |
| `λ_P` | P Compton length | `L*/√2` | 16.9706 pc | P mass, PPN near-source | the P mass is `ħ/(cλ_P)`; `λ_P` is never `L*` |

**Retired glyphs (do not reuse):** `L` (MOND length in A19/A27/A31/A33; Lorentzian kernel in
A25), `ell_0` (cell in FINAL §0; MOND length in A15/§1.4), `ell` (A19's `L/2`), `ell_E`,
`ell_chi`, `L★`, and `λ` for any length.

**One-line rules.**
1. The **law** uses `a₀`, not a length: `g_N = g²/(g + a₀)` contains no length at all.
2. The **vacuum closure** uses `ell_1` and `L_MOND`: `κ = ell_1/L_MOND`, `R = (L_MOND/ell_1)²`,
   and the box is `ΛL_MOND² = 32π` — never `Λell_1² = 32π` (that is `8π`).
3. The **stiffness physics** uses `L*` only: `r_switch = L*√f_c`, `R_core = (π/√2)L*`,
   `λ_J = √2πL*`, `a_P = GM/L*²`.
4. The **P mass** uses `L*/√2`, never `L*`.
5. `a₀ = κ c²/ell_1` is the general statement; `a₀ = c²/(2ell_1)` is its `κ = ½` special case
   and must be written that way.

## Status

**`DERIVED`** for §1–2 (all identities exact in sympy, residuals 0) **+ `AUDIT`** for §3
(6 conflations located, 1 conclusion withdrawn, 5 surviving; 2 live in `FINAL_THEORY.md`).

## Checks

`a37_checks.py`, 10/10 PASS, exit 0, 1.1 s, stdlib + sympy, no network.

| id | proves | measured |
|---|---|---|
| K1 | the three values and the 9-decade separation | 9.6021e26 / 4.8040e26 / 7.4133e17 m |
| K2 | `R = ΛL²/(8π) = (L/ell_1)² = 1/κ²` | max residual `0` |
| K3 | `{L=2ell_1} = {κ=½} = {R=4}`, one root | residual `0`; ratio 1.99876 at the footing |
| K4 | `L*/L_MOND = σ_c²/c²` exactly | residual `0`; `7.7206e-10`, `log₁₀ = −9.1124` |
| K5 | the glyph census and the multi-definition map | 538 / 68 / 19 / 383 lines; 2 defs for `ell_0` |
| K6 | all 6 conflation sites present at the cited line | 6/6 |
| K7 | the cost of each conflation | `R=1`; `a_P=1.4394e-34`; ratio `1.6777e18`; `8.477` decades |
| K8 | the table is one symbol per object | 4 unique symbols |
| K9 | `λ_P = L*/√2`, `m/H₀ = 2.620967e8` | 16.9706 pc |
| K10 | `L = 2ell_1` is the closure, not the definitions; A19 K2 reproduced | 2.000000 at `9.354173e-11`; 1.998755 at `9.36e-11`; 6/6 A19 digits |

## What this does not do

1. **It does not decide which length `FINAL_THEORY` should print.** It identifies the two live
   sites and gives the replacement; editing the document is outside this lane's write scope.
2. **It does not audit the Zenodo record.** A5's extract shows the published papers use `L*` for
   the stiffness length correctly (24 pc–1 kpc); whether an earlier paper ever wrote `L* = c²/a₀`
   was not checked beyond the A5 ledger.
3. **It does not resolve the `K = 4πG` vs `8πG` convention.** It shows the two differ by `√2` in
   `L*` and that the resulting number is indistinguishable from `λ_P`; choosing one is a
   coordinator decision.
4. **It does not re-derive any lane's physics.** Every number quoted from a lane is that lane's
   own, reproduced from BRIEF constants where the arithmetic is short.
5. **The census is a snapshot.** 538 `L*` lines is the count on this date; the check asserts
   structure (multi-definition, the 6 sites), not the exact count.

## Next

1. **Fix `FINAL_THEORY.md:28`**: `a₀ = κc√(Gρ_Λ)`, `ell_1 ≡ √(8π/Λ)`, `a₀ = κc²/ell_1`
   (equivalently `L_MOND = ell_1/κ`), and add `L_MOND = 2ell_1` as the `κ = ½` line. Then
   `:134` becomes `ΛL_MOND² = 32π` and the box is consistent.
2. **Add the four symbols to `parent_audit.py`** as identities: `κ = ell_1/L_MOND`,
   `R = (L_MOND/ell_1)²`, `L*/L_MOND = σ_c²/c²`, `λ_P = L*/√2`. Four lines close the whole
   collision surface mechanically.
3. **Retire `L`, `ell_0` and `λ` for lengths** in the next push's brief, and state `K` once.
