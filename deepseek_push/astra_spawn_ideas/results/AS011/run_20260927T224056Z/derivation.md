# AS011 — Alternative footing as a separate hypothesis: derivation

**Run:** `run_20260927T224056Z` · **Branch:** CORE scale identities (branches remain labelled; Q/RAR/MU2/EXP/MONO comparisons only) · **Worker:** `deepseek/deepseek-v4-flash-0731` (openrouter; Hermes subagent, macOS host) · **UTC:** started 2026-09-27T22:40:56Z, finished 2026-09-27T22:47Z

## 1. Precise claim, symbols, boundary conditions, assumptions

### Symbols and units (SI unless stated)

| symbol | meaning | unit |
|---|---|---|
| `a0` | vacuum (MOND) acceleration scale | m s⁻² |
| `kappa` | dimensionless normalization coefficient of the scale law | 1 |
| `c = 299792458` | speed of light (input) | m s⁻¹ |
| `G = 6.67430e-11` | Newton/scale coupling of the identity (input; framework keeps `G_N`, `G_bare`, `G_cosmo` separate — here a single `G` enters the scale identity, and any Λ statement carries the `G_E/G_N` ratio) | m³ kg⁻¹ s⁻² |
| `rho_Lambda` | vacuum **mass** density (`rho_Lambda = 4 a0²/(G c²)` derived below) | kg m⁻³ |
| `eps_Lambda = rho_Lambda c²` | vacuum energy density | J m⁻³ = kg m⁻¹ s⁻² |
| `Lambda` | cosmological constant in the Einstein equation, `Lambda = 32π a0²/c⁴` **conditional on G_E = G_N** | m⁻² |
| `M_b` | baryonic mass | kg |
| `r_M = sqrt(G M_b/a0)` | MOND radius | m |
| `v_flat` | deep-limit circular speed, `v_flat⁴ = G M_b a0` | m s⁻¹ |
| `B = g_bar` | Newtonian baryonic acceleration, `B = G M_b/r²` | m s⁻² |
| `y = B/a0` | dimensionless acceleration argument | 1 |
| `R_a = a0_alt/a0_can = 1.2047768081...` | footing ratio | 1 |
| `M_sun = 1.98847e30`, `pc = 3.085677581491367e16`, `k_B = 1.380649e-23` | carried constants (M_sun, pc used in dimensional examples; k_B unused) | kg, m, J K⁻¹ |

Subscripts: `_can` = canonical footing, `_alt` = alternative footing. `kappa_can = 1/2` **adopted** (fitted, not derived; README records the distance-free measured `0.551 ± 0.043` — not used here).

### Claim (what this seed establishes)

**(C)** Let `a0 = kappa · c · sqrt(G · rho_Lambda)` with positive `G, c, rho_Lambda, kappa`. With the canonically adopted `kappa_can = 1/2` and the given roundings `a0_can = 9.3619e-11 m s⁻²`, `a0_alt = 1.1279e-10 m s⁻²`, the alternative footing is a **separate hypothesis**, exactly reproducible in two mutually exclusive one-cell models:

- **(A) fixed density:** with `rho_Lambda = rho_Lambda,can` kept, `kappa_alt = R_a/2 = 0.6023884040...` (a new adopted coefficient; shift `Δkappa = +0.1023884040`, +20.4767 % relative to 1/2);
- **(B) fixed kappa:** with `kappa = 1/2` kept, `rho_Lambda,alt = R_a² · rho_Lambda,can = 1.45148716 · rho_Lambda,can` (+45.15 %; `Lambda_alt = R_a² Lambda_can` under `G_E = G_N`).

Both cannot hold in one cell: the map `(kappa, rho_Lambda) → a0` is injective in each argument. Dimensionless relations in `y = B/a0` are footing-covariant in form ("same prediction in equivalent variables"); at fixed baryonic input the dimensional predictions rescale by exact powers of `R_a` (table in §4). No value of `a0` is fitted per object anywhere in this seed.

### Framework inputs vs conclusions

- **Inputs (adopted, not derived):** `kappa = 1/2`; `a0_can`, `a0_alt` (given roundings); `G`, `c`, `M_sun`, `pc`, `k_B`; the identification of `rho_Lambda` with the cosmic vacuum density; the `a0–Λ` relation itself (requirement 13 keeps this "preserve or derive if possible" — it stays an input here).
- **Derived (this seed, exact algebra):** `rho_Lambda = 4 a0²/(G c²)`; `R_a`, `R_a² = 1.45148716`; `kappa_alt = R_a/2` under (A); `rho_Lambda,alt = R_a² rho_Lambda,can` under (B); the rescaling exponents of `r_M`, `v_flat`, deep `g`, Newtonian `g`; the master factorization `R_a² = (kappa_alt/kappa_can)² · (rho_Lambda,alt/rho_Lambda,can)`.
- **Boundary conditions / domain:** all variables positive (`G, c, kappa, rho_Lambda, M_b, r > 0`); real arithmetic; no observational fit; no dynamics beyond the scale identities; the operative gate (filtered MONO, criterion B) is untouched — Q/RAR/MU2 appear only as labelled comparisons (§5).

## 2. The two model comparisons — why they are different models

**Master identity.** Squaring `a0 = kappa c sqrt(G rho)` is exact; forming the ratio of two footings and using positivity (`sqrt(u/v) = sqrt(u)/sqrt(v)` for `u ≥ 0, v > 0`):

```
(a0_alt / a0_can)² = (kappa_alt / kappa_can)² · (rho_Lambda,alt / rho_Lambda,can)        [F]
```

certified in Lean (`footing_factorization`), with the two specializations

```
kappa_alt = kappa_can  ⇒  (a0_alt/a0_can)² = rho_Lambda,alt/rho_Lambda,can             [B]  (fixed kappa)
rho_Lambda,alt = rho_Lambda,can  ⇒  a0_alt/a0_can = kappa_alt/kappa_can                 [A]  (fixed density)
```

**Interpretation A (fixed density; effective kappa shift).** `rho_Lambda,can = 4 a0_can²/(G c²) = 5.8444124540...e-27 kg m⁻³`. Substitution into the undivided law:

```
kappa_alt = a0_alt / (c·sqrt(G·rho_Lambda,can)) = a0_alt/(2 a0_can) = R_a/2
          = 0.6023884040... ,   Δkappa = (R_a − 1)/2 = +0.1023884040 (+20.4767 %)
```

exact (verified to relative 3.3e-60 at 60 digits). This model keeps the vacuum content identical and changes the **coefficient** of the scale law from the adopted 1/2 to a new number. Since nothing in the framework derives `kappa = 1/2`, the value 0.6023884040... is a *new free input* — a re-fit of the same constant the framework already had to adopt. It is not an uncertainty band on 1/2 (the fitted value `0.551 ± 0.043` straddles neither 0.5 nor 0.6024 comfortably at 1σ; in any case a fitted constant is a different object).

**Interpretation B (fixed kappa; changed density).** `rho_Lambda,alt = 4 a0_alt²/(G c²) = 8.4830896195...e-27 kg m⁻³ = R_a² rho_Lambda,can = 1.45148716 rho_Lambda,can`, and with `G_E = G_N`: `Lambda_alt = R_a² Lambda_can`, `eps_Lambda,alt = R_a² eps_Lambda,can`. The vacuum is 45.15 % denser — a different cosmological input (Λ 45 % larger), not a different coefficient.

**Why A ≠ B as model comparisons:** A fixes `(G, rho)` and changes the dimensionless coefficient; B fixes the coefficient and changes the dimensioned input `rho` (hence Λ and every horizon/critical-density statement). They attribute the `+20.5 %` discrepancy in `a0` to different objects, and they carry different observational signatures (A modifies only the scale-law normalization — all `a0`-dependent dimensional predictions shift; B additionally changes the implied vacuum energy budget). The control `NC1` (§6) shows a single `(kappa, rho_Lambda)` cell cannot realize both `a0` values; the factorization `[F]` is the exact bookkeeping of that incompatibility (`R_a² = K²·D` with `K² = D = 1` reproducing only `1 ≠ R_a²` — flagged).

## 3. Intermediate algebra, all factors, signs, units; limiting regimes

**Dimensional audit.** `G·rho_Lambda : [m³ kg⁻¹ s⁻² · kg m⁻³] = [s⁻²]`; `sqrt(G·rho_Lambda) : [s⁻¹]`; `c·sqrt(G rho) : [m s⁻¹ · s⁻¹] = [m s⁻²]` ✓. All factors non-negative; no signs. Derived density: `a0² = kappa² c² G rho ⇒ rho = a0²/(kappa² G c²)`; at `kappa = 1/2`: `rho_Lambda = 4 a0²/(G c²)`; dimension `[m² s⁻⁴ · kg⁻¹ m⁻¹ s² · s² m⁻²] = [kg m⁻³]` ✓ (the `4` is `1/kappa²`, no other factor). Λ: `a0 = c² sqrt(Lambda/(32π)) ⇒ Lambda = 32π a0²/c⁴ : [m² s⁻⁴ · s⁴ m⁻⁴] = [m⁻²]` ✓, holding when the Einstein coupling equals the scale `G`; the framework contract's general form `Lambda_eff = 32π (G_E/G_N) a0²/c⁴` carries the ratio `G_E/G_N` — this seed never sets it to 1 beyond the explicitly conditional statement.

**Rescalings at fixed `(G, M_b)` under `a0 → λ a0`** (λ = R_a for the footing change), all exact:

| quantity | formula | scaling | ratio (λ = R_a) |
|---|---|---|---|
| Newtonian `g` | `G M_b/r²` | λ⁰ | `1.0000000000` |
| deep circular `g` | `sqrt(G M_b a0)/r` | λ^{1/2} | `1.0976232542` |
| `v_flat` | `(G M_b a0)^{1/4}` | λ^{1/4} | `1.0476751663` |
| `r_M` | `sqrt(G M_b/a0)` | λ^{−1/2} | `0.9110594151` |

**Limiting regime (labelled Q-branch comparison, not the task branch).** On Q, `g² = B² + a0 B`, `B = G M_b/r²`, circular speed `v² = g·r`:

```
v⁴ = g² r² = B² r² + a0 B r² = (G M_b)²/r² + a0 G M b          (exact identity, all r > 0)
```

Deep limit `r → ∞` (`r ≫ r_M`): `v⁴ → G M_b a0`; **leading neglected term** `(G M_b)²/r² = G M_b a0 · (r_M/r)²`; relative correction `(r_M/r)²`, smaller than 1% for `r > 10 r_M` (verified: at `r = 10 r_M` the correction ratio equals `(1/10)² = 0.01` to rel 1e-43). Domain: `(r_M/r)² ≪ 1 ⟺ r ≫ r_M`. All signs positive; the identity is *exact algebra*, and the numeric witness (§6) is a finite consistency check of it with recorded residual 6.4e-60.

**MU2 (labelled).** The contract's MU2 reads `mu2(x) = 1 − (1+x/2)^{−2}`, equivalently `mu_n(Y)` at `n = 2`, `Y = g/s`, `s = 2 a0` on the adopted footing. Under footing B, `s → 2 a0_alt`; under footing A, `s → 2 a0_alt` likewise. The dimensionless shape is unchanged; the dimensional saturation scale shifts with `a0`. No MU2 statement transfers to the operative MONO target here.

**Approximation errors.** The core-identity results above are exact rearrangements — no series was used; all numeric witnesses run at 60 significant digits (residuals ≤ 6.9e-60 where checked). The only quoted expansion is the Q-branch deep limit with its stated leading term and domain. Input roundings (`a0_can`, `a0_alt`, 5 significant figures) limit *physical* significance of `R_a`, `R_a²` to about 1e-5 relative; the computed `R_a² = 1.45148716` agrees with the campaign-stated constant to 1.8e-9 relative (tolerance 2e-7), i.e. the stated constant is exactly the two roundings' ratio.

## 4. Dimensional examples — both footings carried separately

| quantity | canonical `a0 = 9.3619e-11` | alternative `a0 = 1.1279e-10` | ratio |
|---|---|---|---|
| `rho_Lambda` (kg m⁻³) | `5.8444124540e-27` | `8.4830896195e-27` | `1.4514871574` |
| `eps_Lambda` (J m⁻³) | `5.2526959597e-10` | `7.6242207273e-10` | `1.4514871574` |
| `Lambda` (m⁻², G_E=G_N) | `1.0907997633e-52` | `1.5832818477e-52` | `1.4514871574` |
| `r_M`, M_b = 1e11 M_sun (kpc) | `12.2019668076` | `11.1167167432` | `0.9110594151` |
| `v_flat`, M_b = 1e11 M_sun (km s⁻¹) | `187.7466476786` | `196.6975003381` | `1.0476751663` |
| `r_M`, M_b = M_sun (pc) | `0.0385860070` | `0.0351541450` | `0.9110594151` |
| `v_flat`, M_b = M_sun (km s⁻¹) | `0.3338659979` | `0.3497831149` | `1.0476751663` |

(60-digit arithmetic; truncated display. Full values in `raw_output.json` → `dimensional_examples`.)

## 5. Independent checks — different representations, actual residuals

1. **Substitution into the original equation:** `kappa_can c sqrt(G rho_Lambda,can) − a0_can` → rel residual `1.068e-60`; `kappa_can c sqrt(G rho_Lambda,alt) − a0_alt` → rel `0.0` (≤1e-60). Both footings self-consistent.
2. **Λ-representation:** `a0 = c² sqrt(Lambda_can/(32π))` → rel residual `9.26e-52` (π truncated at 60 digits in the test — residual is the π-truncation tail).
3. **Energy-density representation:** `a0 = kappa sqrt(G eps_Lambda,can)` → rel residual `0.0`.
4. **Factorization [F] in both branches:** `K²·D` under (A) and under (B) each equal `R_a²` to rel ≤ 6.9e-60.
5. **Q-branch direct substitution** (`v⁴` identity): max relative residual `6.4e-60` over `r/r_M ∈ {2, 3, 10, 100, 1e4}`, M_b = 1e11 M_sun.
6. **Boundary** `y = B/a0 = 1`: `g/a0 = sqrt(2)` on *both* footings to 1e-50 (dimensionless statement — footing-covariant).

## 6. Negative controls (both capable of failing; both passed by flagging)

**NC1 — hold BOTH `rho_Lambda` and `kappa` fixed while changing `a0`.** `a0(kappa=1/2, rho_Lambda,can) = a0_can` (PASS, rel 1.1e-60) but differs from `a0_alt` by rel `0.16997`; `a0(kappa=1/2, rho_Lambda,alt) = a0_alt` (PASS, rel 0) but differs from `a0_can` by rel `0.20478`. Both inconsistencies are flagged as required (the check PASSES by detecting, i.e. the control would FAIL if the inputs were mislabelled so that no flag appeared). Lean form certified: `different_a0_forces_different_rho`, `both_fixed_implies_same_a0`.

**NC2 — limiting regimes / boundary.** Newtonian limit: `g_N`footing-invariant (ratio exactly 1, verified 1e-60); deep limit: `v_flat` ratio `= R_a^{1/4}` to rel 0 at 60 digits, deep-`g` ratio `= R_a^{1/2}` to rel 0, `r_M` ratio `= R_a^{−1/2}` to rel 2.2e-60; Q-branch `v⁴` exact identity verified at 5 radii (residual 6.4e-60, see §5.5); `y=1` boundary on both footings (§5.6). **Exact identity vs finite consistency distinguished:** the `v⁴` identity and the factorization `[F]` are proved by direct algebra (Lean-certified where real-arithmetic); the 60-digit witnesses are finite consistency checks with recorded residuals, not proofs.

All 22 computed checks pass; wall time 0.0004 s (enforced RLIMIT_CPU = 120 s), max RSS 13.9 MB (enforced RLIMIT_AS = 512 MB), zero threads spawned.

## 7. Strongest surviving statement and next implication

**Strongest surviving statement (scoped claim):** Under the framework identity `a0 = kappa c sqrt(G rho_Lambda)` with the adopted `kappa_can = 1/2` and the given roundings, the alternative footing is a separate hypothesis realizable in exactly two mutually exclusive models — (A) effective `kappa_alt = a0_alt/(2 a0_can) = 0.6023884040...` at fixed canonical density, or (B) `rho_Lambda,alt = (a0_alt/a0_can)² rho_Lambda,can = 1.45148716 rho_Lambda,can` at fixed `kappa = 1/2` — with dimensional consequences at fixed `(G, M_b)`: `v_flat ×1.0477`, deep `g ×1.0976`, `r_M ×0.9111`, Newtonian `g ×1`. One shared `(kappa, rho_Lambda)` cell cannot produce both `a0` values. Domain: positive `(G, c, kappa, rho_Lambda, M_b, r)`; all statements exact (Lean-certified) with the input `kappa` explicitly adopted.

**First additional implication to transfer to the full theory:** choose the footing physically — either derive `kappa` (freeing the adopted 1/2) or measure/predict `rho_Lambda` independently, so that requirement 13's "preserve or derive if possible" link `a0 ↔ vacuum` is no longer an input; then propagate the chosen footing through the operative filtered-MONO branch (amended requirement 1) so the 4.77 % `v_flat` difference becomes a falsifiable prediction at known `M_b` instead of a bookkeeping statement.

## 8. Files in this run directory

- `derivation.md` (this file)
- `result.json` (contract schema v2)
- `compute_AS011_footing_separation.py` (runnable; enforced bounds inside)
- `raw_output.txt` (stdout), `raw_output.json` (machine-readable results + checks)
- `time_err.txt` (wall-time record)
- `AS011_footing_separation_certificates.lean` (Lean 4 certificate, 8 theorems, zero `sorry`)
- `lean_check.out` (`#print axioms`: all 8 theorems ⊆ {propext, Classical.choice, Quot.sound})
- `_build_result_json.py` (builder for `result.json`)
- Child spec (ready, not dispatched): `deepseek_push/astra_spawn_ideas/branches/AS011/AS011.C01.md`