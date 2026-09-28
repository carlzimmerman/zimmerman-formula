# AS014 — Measured G versus bare action coupling

**Run:** `AS014-r1-20260927T225402Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter; Hermes Agent subagent) — see `result.json`
**Task:** `deepseek_push/astra_spawn_ideas/AS014_measured_g_versus_bare_action_coupling.md`
(sha256 `07f8c3dc0c33282ed76518bb3a2f19f261588d81f1470db0e0d8daca32f7d7f1`)
**Branch:** CORE scale identities (Group A01 — scale, units and independent inputs).
No branch transfer: Q / RAR / MU2 / EXP are touched only as *labelled comparison*
kernels in the regime checks; MONO appears only through its numerical landmark
constants. All conclusions live in the declared branch.
**Sources (pinned hashes verified against SOURCE_MANIFEST.json, all three match):**
`README.md` `91a5fac4…6b6ed` · `FRIED_CHICKEN_SPEC.md` `98d9149f…d8e3f` ·
`FINAL_ACTION.md` `b8c04d4e…7546e`.

---

## 1. Precise claim, symbol dictionary, premises

### 1.1 Claim (AS014-T)

Let `C_N := G_bare / G_N > 0` be the conversion between the **bare action
coupling** `G_bare` (coefficient of the gravitational sector in the action,
`M_P^2 = (8π G_bare)^{-1}` in the CA4-GNC action, FINAL_ACTION §1) and the
**measured Newton coupling** `G_N` (Cavendish / solar-system value, framework
input `6.67430e-11` SI). `G_E` (Einstein coupling of the vacuum-curvature term
`Λ_eff`; for the CA4-GNC action `G_E = G_bare`, because one `M_P^2` multiplies
`R` and `Λ_eff` together) and `G_cosmo` (Friedmann/critical-density coupling;
unused here, kept separate) remain distinct symbols throughout.

Then, for **every** positive value of the parameters:

**(T1) scale conversion** — if the action derives its own scale from its own
coupling, `a0_b = κ c sqrt(G_bare ρ_Λ) = sqrt(C_N) · a0` with
`a0 = κc√(G_N ρ_Λ)`, κ = ½ adopted;

**(T2) substitution cell** (framework objects with `G_bare` inserted, `a0`
held at the measured footing — the task's `G_N = G_bare/C_N` reading):

```
r_M(G_bare)² = G_bare M_b / a0  = C_N · r_M(G_N)²      →  r_M ∝ C_N^(1/2)
v_flat(G_bare)⁴ = G_bare M_b a0 = C_N · v_flat(G_N)⁴   →  v_flat ∝ C_N^(1/4)
a0_b = sqrt(C_N) a0
Λ_eff(G_E = G_bare) = 32π (G_bare/G_N) a0²/c⁴ = 32π C_N a0² / c⁴        (T3)
```

**(T4) error audit** — when the action's field equations run on `G_bare` but
the galaxy calculation (analyser) assumes `G_N` everywhere:

| channel | error factor (action/analyst) | exact |
|---|---|---|
| Newtonian limit (g ≫ a0): force | `C_N` | g_act = C_N g_N |
| deep MOND, mixed cell (a0 pinned at measured value): g², v⁴ | `C_N` | g_act² = C_N a0 g_N; v⁴_act = C_N v⁴_ana |
| deep MOND, full cell (a0_b = √C_N a0): g, v⁴ | `C_N^(3/4)`, `C_N^(3/2)` | v⁴_act = C_N^{3/2} v⁴_ana |
| inferred scale from BTFR, mixed / full cell | `C_N` / `C_N^(3/2)` | a0_inf = v⁴_obs/(G_N M_b) |
| MOND radius, mixed / full cell | `C_N^(1/2)` / `C_N^(1/4)` | — |
| vacuum identity mismatch | `C_N` | Λ_eff = C_N Λ_conv, Λ_conv := 32πa0²/c⁴ |
| interpolation regime (generic kernel) | `R(y) = C_N ν(√C_N·y)/ν(y)`, monotonically between the limits | deep → C_N^{3/4}, Newtonian → C_N |

**(T5) matching equivalence (Lean-certified):** under T3,
`Λ_eff = Λ_conv ⟺ C_N = 1`. The framework identity `Λ_eff = 32π(G_E/G_N)a0²/c⁴`
(AS002-T1, certified) is a **matching condition**, never permission to set the
couplings equal: with `G_E = G_bare` the printed same-G dictionary
`Λ = 32πa0²/c⁴` holds **iff** the action forces `G_bare = G_N`.

**(T6) negative control (task-mandated):** at `C_N = 2` the unconverted
formula fails the physical normalization on every channel by an O(1) factor:
a0_inf ratios 2.0 / 2.828, Λ ratio 2.0, deep-g ratios 1.414 / 1.682, Kepler
mass-inference ratio 2.0 (all exact, 60-digit mpmath; Lean-instanced for the
Λ and a0_inf channels).

**Domain:** all symbols real and strictly positive (C_N > 0, G_N > 0, G_bare >
0, ρ_Λ > 0, a0 > 0, c > 0, M_b > 0, κ = ½ adopted). Both registered footings
carried separately (below). No limiting-regime assumption enters T1–T6: they
are exact power laws; the regime section derives the *leading neglected
terms* of the interpolation formula separately.

### 1.2 Symbol dictionary

| symbol | meaning | SI unit |
|---|---|---|
| `G_N` | measured Newton coupling (framework input, `6.67430e-11`) | m³ kg⁻¹ s⁻² |
| `G_bare` | bare action coupling: `M_P² = (8πG_bare)^{-1}` (FINAL_ACTION §1) | m³ kg⁻¹ s⁻² |
| `G_E` | Einstein coupling in `ρ_Λ = Λ_eff c²/(8πG_E)` (AS002-P1); `G_E = G_bare` for the CA4-GNC action (one `M_P²` multiplies `R` and `Λ_eff`) | m³ kg⁻¹ s⁻² |
| `G_cosmo` | Friedmann/critical-density coupling (recorded, unused in this task) | m³ kg⁻¹ s⁻² |
| `C_N` | `G_bare/G_N = 1/(G_N/G_bare)`, dimensionless conversion | 1 |
| `a0` | `κ c √(G_N ρ_Λ)`, κ = ½ **adopted input** (not derived here) | m s⁻² |
| `a0_b` | `κ c √(G_bare ρ_Λ)` (the action's own scale if derived from its own coupling) | m s⁻² |
| `ρ_Λ` | vacuum mass density `= 4 a0²/(G_N c²)` (κ=½ restatement) | kg m⁻³ |
| `Λ_conv` | same-G dictionary value `32π a0²/c⁴` | m⁻² |
| `Λ_eff` | effective vacuum curvature `8π G_E ρ_Λ/c² = 32π (G_E/G_N) a0²/c⁴` | m⁻² |
| `r_M`, `v_flat` | `√(G_N M_b/a0)`, `(G_N M_b a0)^{1/4}` | m, m s⁻¹ |
| `y` | `g_N/a0`, `g_N = G_N M_b/r²` (dimensionless witness variable) | 1 |
| `ν` | interpolation kernel (labelled comparison only: RAR explicitly, MONO by landmarks) | 1 |

### 1.3 Framework inputs vs conclusions

**Inputs (axioms/calibrations):** κ = ½ adopted (README: fitted, not derived;
k01/k03 no-go record untouched); `G_N`, `c`, `M_sun`, `pc` framework defaults;
both footings `a0 ∈ {9.3619e-11, 1.1279e-10}` m/s²; the scale relation
`a0 = κc√(G_N ρ_Λ)` as the framework's declared premise; AS002-T1
(`Λ_eff = 32π(G_E/G_N)a0²/c⁴`) as an externally certified identity (reused as
a premise of the Lean certification, not re-derived as a new claim);
`G_E = G_bare` for the CA4-GNC family (FINAL_ACTION §1: one `M_P²` multiplies
`R` and `Λ`); kernel-cell data for the regime checks are **comparisons** (RAR
formula; MONO landmarks `y_p ≈ 2.5396`, `y* ≈ 2.3374`, δ = 0.05 from the
contract).

**Conclusions (this task):** T1–T6, the error table, the matching equivalence,
the regime leading neglected terms, and the operative-gate statement
(requirement 10). `C_N` is **not** derived from the action here — deriving it
is the first unresolved implication (child AS014.C01).

---

## 2. Step 2 — insert C_N symbolically throughout r_M, BTFR and the vacuum identity

From `G_bare = C_N G_N` (task statement `G_N = G_bare/C_N`):

**MOND radius.** `r_M² = G M_b / a0`. Substituting the coupling,
```
r_M(G_bare)² = G_bare M_b / a0 = C_N · (G_N M_b / a0) = C_N r_M(G_N)²
⇒  r_M(G_bare) = sqrt(C_N) · r_M(G_N).            (E1)
```
Dimension check: `C_N` dimensionless, `m² = m²`. Sign: positive (C_N > 0).
If the action also supplies its own scale `a0_b = √C_N a0` (full cell), then
`r_M,b² = G_bare M_b/a0_b = C_N G_N M_b/(√C_N a0) = √C_N r_M²`, i.e.
`r_M,b = C_N^{1/4} r_M`. The exponent differs by cell; the two cells are
stated separately and never mixed.

**BTFR.** `v_flat⁴ = G M_b a0`. Substituting,
```
v_flat(G_bare)⁴ = G_bare M_b a0 = C_N · v_flat(G_N)⁴
⇒  v_flat(G_bare) = C_N^{1/4} v_flat(G_N).        (E2)
```
Deep-MOND with the action's own scale (full cell):
```
v⁴_act = a0_b G_bare M_b = √C_N a0 · C_N G_N M_b = C_N^{3/2} v⁴_ana.   (E3)
```

**Vacuum identity.** AS002-T1 (certified there): `Λ_eff = 32π (G_E/G_N) a0²/c⁴`.
With `G_E = G_bare = C_N G_N` (two-line algebra, every factor carried):
```
Λ_eff = 32π (C_N G_N / G_N) a0²/c⁴ = 32π C_N a0² / c⁴ = C_N · Λ_conv.   (E4)
Λ_conv := 32π a0²/c⁴   (the README/AS002 same-G value at G_E = G_N).
```
The factor `32π` (κ=½ ⇒ 1/κ² = 4, times the Einstein 8π), the ratio
`G_E/G_N = C_N`, and no hidden factor are dropped or invented; AS002's
negative control (dropping the 8π changes a0 by √(8π)) is not repeated here —
cited as certified. Conversely, from E4:
```
matching:  Λ_eff = Λ_conv  ⟺  C_N = 1   (G_E = G_bare fixed).           (E5)
```
If instead `G_E ≠ G_bare`, matching requires `G_E = G_N` exactly: the
Einstein coupling of the vacuum term must equal the measured coupling for the
printed dictionary to be single-valued. For the CA4-GNC action family
`G_E = G_bare`, so E5 reads: **the framework identity holds iff the action
forces the measured Newton constant to equal its bare coupling** — that is
exactly the content of amended requirement 10 ("derive the measured Newton
constant rather than assuming it equals the bare coupling"); the current
single-`G` printing of the README dictionaries is the C_N = 1 convention,
never a derived statement.

**Error when the action uses G_bare but the galaxy calculation assumes G_N**
(raw residuals, exact): the analyser's formulas are the framework cell; the
action's predictions are the substitution/full cells of §4 table. In
particular the *inferred* scale from the BTFR,
```
a0_inf := v_obs⁴/(G_N M_b) = a0 · G_bare/G_N = C_N a0         (mixed cell)
a0_inf = a0 · C_N^{3/2}                                       (full cell)
```
so a misidentification of the coupling is a **multiplicative** error in the
fitted scale — it does not average out over galaxies.

---

## 3. Step 3 — intermediate algebra, scale factors, signs, units; limiting regimes

All T1–T6 steps are exact single-line substitutions (shown in §2); no
integration, no expansion, no fitted input. The only place a limiting regime
appears is the interpolation channel, where the *kernel* (not the conversion)
furnishes subleading structure. Let `y = g_N/a0`, `g_N = G_N M_b/r²`, and a
generic kernel `ν` with `ν(y) → 1` (Newtonian) and `ν(y) → y^{-1/2}` (deep).
Full cell: `y_b = G_bare M_b/(a0_b r²) = √C_N · y`; `g_b = ν(y_b) G_bare
M_b/r² = C_N ν(√C_N y) g_N`. Hence

```
R_full(y) := g_b/g_ana = C_N · ν(√C_N y) / ν(y).            (E6)
```

**Limits (kernel-independent asymptotics).** `y → 0⁺`: `R → C_N ·
(√C_N)^{1/2} = C_N^{3/4}` (g-channel; v⁴-channel exponent 3/2 — consistent
with E3). `y → ∞`: `R → C_N` (Newtonian, linear in G). Both limits are
derived purely from the asymptotics of ν, so they hold for RAR **and** MONO
(which coincides with RAR below `y*` and satisfies `ν_mono → 1` above).

**Leading neglected terms, deep regime** (RAR kernel, exact in `s = √y`):
```
ν_RAR(z) = z^{-1/2} [1 + s/2 + s²/12 − s⁴/720 + O(s⁵)],  s = √z,
R/C_N^{3/4} − 1 = (a − b)/(1 + b),
  a = s₁/2 + s₁²/12 + …,  b = s₂/2 + s₂²/12 + …,  s₁ = C_N^{1/4}√y, s₂ = √y,
```
so the leading neglected term is `(C_N^{1/4} − 1)√y/2 + O(y)` **in the
ratio**, and the exact residual is positive for C_N > 1, negative for C_N < 1
(verified to 1:10⁸ at y = 10⁻⁶, 10⁻⁴; §C5). Domain of the one-term form:
`y ≪ 1`.

**Leading neglected term, Newtonian regime** (RAR): `ν(z) = 1 + e^{−√z} +
e^{−2√z} + …` (convergent for large z), so
```
R/C_N − 1 = e^{−C_N^{1/4}√y} − e^{−√y} + O(y e^{−√y}),   y ≫ 1,
```
exponentially small. **MONO's Newtonian approach is slower**: from
`h_mono(y) = h_RAR(y*) + δ h_p ln[(y + y_p)/(y* + y_p)]`,
`ν_mono(y) − 1 = h_mono(y)/y = O(ln y / y)`, so
`R_MONO/C_N − 1 = O(ln y / y)` — numerically `1 − R_MONO/C_N = 5.95×10⁻⁷` at
`y = 10⁶` (vs RAR `~7.4×10⁻⁴³⁴`... : RAR residual `0.0` at 10⁶, `3.7×10⁻⁴⁴`
at 10⁴). Both agree on the *limit*; the label comparison is recorded, not
transferred (kernel branch laws are not this task's conclusions).

Landmarks recomputed from the contract definitions (h'_RAR = 0 and the δ-floor
crossing): `y_p = 2.539638` (quoted 2.5396), `h_p = 0.647610` (matches the
README's saturation value 0.6476), `y* = 2.337412` (quoted 2.3374) — the
MONO numerical cell in the checks uses these, not imported values.

**Units.** Every conversion factor is `C_N^{p}` with `p ∈ {1/4, 1/2, 3/4, 1,
3/2}` — dimensionless, so the power laws hold identically on both footings;
the *numerical* cells quote both footings separately (κ = ½ fixed, hence
distinct densities, `ρ_alt/ρ_can = (a0_alt/a0_can)² = 1.4514871574`; the two
footings never share a fixed density **and** a fixed κ).

---

## 4. Step 4 — independent check (different representation)

Identities T1–T5 were verified in **four independent representations**:

1. **Symbolic (sympy)**: all six insertion/vacuum identities simplify to
   exactly 0 after substituting `G_bare = C_N G_N` (C1). Exact, no floats.
2. **mpmath 60-digit**: all conversion ratios match `C_N^{p}` to
   `≤ 1.6×10⁻⁶¹` (C2, C3, C4) on both footings for `C_N ∈ {1.5, 2, 0.9}`.
   E.g. `Λ_eff = 2.181600e-52` m⁻² at C_N = 2 (canonical), exactly `2·Λ_conv`
   (residual 0.0); `Λ_eff = 3.166564e-52` m⁻² (alternative).
3. **float64**: same ratios in IEEE double, residuals `≤ 2.3×10⁻¹⁶` (C9).
4. **Lean 4 formal proof** (`AS014_measuredG_bare_coupling.lean`): 9
   theorems, zero `sorry`, axioms exactly `{propext, Classical.choice,
   Quot.sound}` (unfiltered `#print axioms`): L1 scale conversion, L2 r_M²
   substitution, L3 v⁴ substitution, L4 full-cell v⁴, L5 vacuum identity at
   G_E = G_bare (AS002-T1 taken as the premise — reuse, dependency stated),
   L6 matching equivalence (T5), L7/L8/L9 the two negative-control channels
   at C_N = 2. Compile: `lake env lean` exit 0.
   Note the certification bar: AS002-T1 enters L5/L6 as a **hypothesis**, not
   a re-derivation — L5/L6 prove the AS014-specific implication (substitution
   + matching) *given* T1; the Lean file is self-contained (compiles
   standalone with the hypothesis declared).

**Residuals (actual, not booleans):** see `result_checks_raw.json` — all 114
checks: worst exact-residual `1.56×10⁻⁶¹` (60-digit), worst float64 residual
`2.22×10⁻¹⁶`; regime leading-term ratios equal 1 to `1.5×10⁻⁸` (deep) and
`6.1×10⁻⁹` (Newtonian RAR).

---

## 5. Step 5 — negative control, strongest surviving statement, next implication

### 5.1 Task negative control: C_N = 2

Take `G_bare = 2 G_N` and apply the **unconverted** (same-G, C_N = 1) formula
set. Every physical normalization fails by an O(1) factor (both footings;
60-digit mpmath; Lean-instanced for the scale and vacuum channels):

| channel | unconverted vs converted | canonical (a0 = 9.3619e-11) |
|---|---|---|
| inferred a0 (mixed cell) | a0_inf/a0 = 2.000 | 1.872380e-10 m/s² (100% error) |
| inferred a0 (full cell) | a0_inf/a0 = 2.828… | 2.647945e-10 m/s² (183% error) |
| Λ_eff (G_E = G_bare) | Λ_eff/Λ_conv = 2.000 | 2.181600e-52 m⁻² |
| deep-g error (mixed / full) | 1.414… / 1.682… | — |
| Newtonian mass inference (Kepler) | M_inf ratio = 2.000 | 1.988416e30 → 9.942078e29 kg |

The control is **live**: at C_N = 1 every ratio is exactly 1 (liveness probe
on record), so the harness can pass and can fail. A 0.301 dex shift of the
BTFR zero point is also an order of magnitude above the framework's quoted
0.108 dex RAR dispersion (comparison only, README) — a misidentification of
the coupling is not absorbed by the fit quality. This is exactly the
"equivalent variables" principle of the task: the framework's promise that
`(ρ_Λ, G_N)`, `(Λ_eff, G_E, G_N)` and `(a0, G_N)` parametrize the same
physics holds **only with the C_N conversion carried**.

### 5.2 Strongest surviving statement

**AS014-T (strong).** The measured-vs-bare coupling relation is a
**multiplicative matching condition, not a unit convention**: `C_N = G_bare/G_N`
enters every CORE object as an exact power law (r_M ∝ C_N^{1/2}, v ∝ C_N^{1/4},
v⁴ ∝ C_N, a0_b ∝ C_N^{1/2}, Λ_eff = C_N·Λ_conv at G_E = G_bare); the framework
identity `Λ_eff = 32π(G_E/G_N)a0²/c⁴` is satisfied by the CA4-GNC family's
printed dictionaries **iff C_N = 1** (proved iff in Lean); an action running
on `G_bare` while the analysis uses `G_N` misinfers the scale by `C_N
·a0` (mixed cell) or `C_N^{3/2}·a0` (full cell) and fails every physical
normalization O(1) at C_N = 2. Domain: all positive reals, both footings,
exact (no approximation).

**Empirical consistency (labelled comparison, not a fit):** the framework's
own measured κ̃ values re-expressed through the audit give C_N bounds within
2σ of 1 — distance-free κ̃ = 0.551 ± 0.043: C_N = 1.102 ± 0.086 (mixed cell,
|C_N−1| = 1.19σ) and 1.067 ± 0.057 (full cell, 1.17σ); BTFR κ̃ = 0.465 ±
0.076: C_N = 0.930 ± 0.152 (0.46σ) and 0.953 ± 0.101 (0.47σ). Current data
therefore **do not demand** C_N ≠ 1, but the T1σ band is ±10–16%, i.e. the
measured-vs-bare question is an open, quantifiable gate — it is the
observational handle for requirement 10.

### 5.3 First additional implication needed to transfer to the full theory

**Requirement-10 gate:** derive `C_N = G_bare/G_N` (or a bound) from the
**quasi-static Newtonian limit of the single common action** with minimal
matter coupling `S_b[g]` (requirement 5's actual coupling): the effective
static G of the linearized metric+scalar+clock system of the CA4-GNC family.
Until that derivation exists, every framework quantity quoted through the
single-G dictionaries carries the explicit condition `C_N = 1`; no MONO-branch
observable is affected otherwise (the scale audit is branch-free, and the
task mandates not importing another branch to repair a failure — none
occurred). This is the transfer statement; note AS003 already identified the
same ratio family (G_cosmo/G_N) as its own open dependency and AS498 consumes
the BTFR-scale corner of this triangle — no duplication: see children.

---

## 6. Both footings — dimensional table

| quantity | canonical a0 = 9.3619e-11 m/s² (ρ_Λ = 5.844412454e-27 kg/m³) | alternative a0 = 1.1279e-10 m/s² (ρ_Λ = 8.483089620e-27 kg/m³) |
|---|---:|---:|
| Λ_conv = 32πa0²/c⁴ [m⁻²] | 1.090799763e-52 | 1.583281848e-52 |
| Λ_eff at C_N = 2 [m⁻²] | 2.181599526e-52 | 3.166563695e-52 |
| a0_inf mixed at C_N = 2 [m/s²] | 1.872380e-10 | 2.255800e-10 |
| a0_inf full at C_N = 2 [m/s²] | 2.647945e-10 | 3.190183e-10 |
| a0_b = √2·a0 [m/s²] | 1.323978e-10 | 1.595094e-10 |

Conversions are dimensionless powers of C_N and apply identically on both
footings (κ = ½ fixed ⇒ distinct densities; footnote: no footing shares both
fixed ρ_Λ and fixed κ). All numeric residuals 60-digit: ≤ 1.6×10⁻⁶¹.

---

## 7. Files, commands, bounds

**Prototype `compute_AS014_gbare_audit.py`** (single thread by construction;
SIGALRM 120 s hard-enforced via `signal.alarm`; RLIMIT_AS 512 MB refused by
macOS — recorded verbatim in `failed_attempts`; actual wall 0.09 s, actual
peak RSS 78.4–79.8 MB; no RNG, deterministic). Run:
`/usr/bin/time -p python3 compute_AS014_gbare_audit.py` → `raw_output.txt`,
`result_checks_raw.json`, `time_bounds.txt` (exit 0; 114 PASS / 0 FAIL).

**Lean:** `lake env lean AS014_measuredG_bare_coupling.lean` from
`fable_independent_2026/lean_2026` → `lean_compile.out` (exit 0, zero
warnings, zero sorry); unfiltered `#print axioms` of all 9 theorems →
`lean_axioms_out.txt`: all = `[propext, Classical.choice, Quot.sound]`.
Failed attempts preserved: `failed_attempts` in `result.json` (macOS rlimit
refusal; three harness bugs caught by the controls themselves — wrong
second-derivative landmark root, missing 1/(1+b) denominator factor in the
deep leading term, rw-direction errors in Lean v1 — each fixed with the
failure recorded, none physics).

---

## 8. Limitations (what this result does not establish)

1. Does **not** derive C_N from the action (that is requirement 10's gate;
   child C01). C_N = 1 remains the convention, now with an explicit,
   quantified error calculus attached.
2. Does **not** derive κ = ½ (adopted input; k01/k03 no-go record
   unaffected).
3. Does **not** touch dynamics: no field equations, no constraint count, no
   criterion-B statement, no lensing/PPN; G_E = G_bare is asserted from
   FINAL_ACTION §1 for the CA4-GNC family (one M_P² multiplies R and Λ), not
   re-derived.
4. The κ̃ → C_N band (C8) is a **comparison** built from README's published
   fit values (0.551 ± 0.043, 0.465 ± 0.076); it is not a new fit and its
   systematics (stellar M/L, distances) are not propagated — a proper
   covariance-aware bound is child C02.
5. The kernel regime analysis (R_full, leading terms) is a scale-transformation
   lemma on labelled comparison kernels (RAR analytic, MONO numerical
   constants); no RAR/MONO branch law is derived or transferred.
6. Numerical runs are finite witnesses of exact algebra; the theorem content
   is the Lean certificate plus the symbolic identities.

## 9. Next unresolved implication and children

**next_unresolved_implication:** the value or bound of
`C_N = G_bare/G_N` from the single action's static Newtonian limit
(requirement 10); until then the printed same-G dictionaries and the ≤ ±10–16%
(1σ) band from κ̃ are the state of the measured-vs-bare gate.

**Ready child specifications (not dispatched — no spawn mechanism in this
worker; `state: ready_spec_only`):**

- **AS014.C01** — *Effective Newton coupling of the CA4-GNC static limit*:
  compute C_N for the linearized metric+scalar+clock system with minimal
  matter coupling S_b[g]; requirement 10 gate; controls: C_N = 1 must reduce
  to pure-GR Poisson; any derived C_N must re-enter the T4 error table and
  re-fit the inferred a0 on both footings; dependency: this result (T1–T6).
  Distinct from AS237 (uncertainty *propagation* into a0) and AS253
  (vacuum-floor footing translation).
- **AS014.C02** — *Covariance-aware empirical bound on C_N*: combine the
  distance-free and BTFR κ̃ channels with H₀ anchors and both footings into a
  single 2σ band for C_N, with systematics named; comparison only (no fit
  claim); distinct from AS498 (joint closure triangle requiring an
  action-derived ratio as third input — this child supplies the data corner
  that triangle needs).

Both fingerprints were checked against the AS manifest (AS149, AS237, AS253,
AS498, AS1852, AS1909, AS1926 differ in target, domain or premise) and no
existing result dir covers them.