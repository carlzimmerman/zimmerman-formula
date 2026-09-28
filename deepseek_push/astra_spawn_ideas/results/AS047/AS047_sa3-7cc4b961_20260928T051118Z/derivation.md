# AS047 — Uniform force-error versus derivative-error control (derivation)

**Run:** `AS047_sa3-7cc4b961_20260928T051118Z` — worker `hermes-subagent sa-3-7cc4b961`
(deepseek/deepseek-v4-flash-0731 via openrouter), reserved in `claims/AS047.json`
(worker `sa-3-7cc4b961`, state running, dispatched 2026-09-28T04:52:16Z).
**Branch:** operative MONO only. **Outcome:** supports_scoped_claim (counterexample to
the derivative-control inference; the branch's own force-vs-derivative norm gap is quantified).

---

## 0. Dispatch discrepancy (mandatory note)

The orchestrator brief named the task file `deepseek_push/astra_spawn_ideas/AS047_log_phantom_disk_self_consistent_profiles.md`
(plus a "phantom disk profiles" work description). **That file does not exist in the
repository** (verified by file-name search `*phantom_disk*`, `*self_consistent_profile*`,
and content search for "log phantom"/"phantom disk"; zero hits in `deepseek_push/astra_spawn_ideas/`).
The claims ledger `claims/AS047.json` pins `task_sha256 = ddab4669ce9f5f2f122e04acf651726f4bf26532bd134ba9266be285959fd287`,
which is **exactly the SHA-256 of the registered on-disk seed**
`AS047_uniform_force_error_versus_derivative_error_control.md` (recomputed: `ddab4669…`).
`INDEX.md` row AS047 likewise registers the uniform force-error seed. The registered seed is
therefore the authoritative dispatched task; the brief's title is a stale alias of the same
MONO log-phantom continuation object. This run executes the registered seed's numbered steps
exactly, and additionally reports the "log phantom disk profiles" content the brief named
(supplementary script + §5 below), built on the same certified functions, clearly labelled
as an appendix, not as a separate task.

## 1. Precise claim, symbol dictionary, assumptions

**Claim under test** (registered seed, "Mathematics and principal test"):

> `|nu_mono/nu_RAR − 1|` small does not bound `|h'_mono − h'_RAR|` or higher derivatives.

**Symbols** (all dimensionless except where noted; `y = B/a0 > 0`, `B = g_bar = g_N`):

| symbol | definition | status |
|---|---|---|
| `h_RAR(y)` | `y/(exp(sqrt y) − 1)` | derived from `nu_RAR = 1/(1−exp(−sqrt y))` via `h = y(nu−1)` |
| `nu_RAR(y)` | `1 + h_RAR(y)/y ≡ 1/(1−exp(−sqrt y))` | framework input (RAR branch) |
| `h'_RAR(y)` | `[2(e^s−1) − s e^s]/[2(e^s−1)²]`, `s=√y` | derived (exact) |
| `h''_RAR(y)` | `e^s[2s e^s − (e^s−1)(s+3)]/[4s(e^s−1)³]` | derived (exact) |
| `y_p` | unique positive max of `h_RAR`: `(2−s_p)e^{s_p}=2`, `s_p=√y_p` | derived, root; `y_p = 2.5396382821881653` |
| `h_p` | `h_RAR(y_p) = 0.6476102378919149` | derived |
| `δ` | `0.05` | framework input (FRAMEWORK_CONTRACT MONO cell) |
| `c` | `δ·h_p = 0.032380511894595745` | derived |
| `P(y)` | `c/(y + y_p)` | framework derivative-rule branch |
| `y_star` | unique solution of `h'_RAR(y_star) = P(y_star)` | derived, root; `y_star = 2.3374124052663294` |
| `h_star` | `h_RAR(y_star) = 0.6469603693249751` | derived |
| `h_mono(y)` | `h_RAR(y)` for `y ≤ y_star`; `h_star + c·ln((y+y_p)/(y_star+y_p))` for `y ≥ y_star` | construction (MONO continuation) |
| `nu_mono(y)` | `1 + h_mono(y)/y` | derived |
| `h'_mono(y)` | `max(h'_RAR(y), P(y))` by rule; `= P(y)` on the continuation | framework rule |
| `r_M` | `sqrt(G M_b/a0)` | framework |
| `C_ph` | `v_flat² = sqrt(G M_b a0)` | framework (deep phantom constant) |
| `Σ_crit` | `a0/(2πG)` | derived scale (plane-parallel) |

**Boundary conditions / domain:** `y ∈ (0, ∞)`; value continuity of `h_mono` at `y_star`
(`h_mono(y_star) = h_RAR(y_star)`, the framework contract's "joined continuously" clause);
initial conditions: none (static constitutive statement).

**Assumptions distinguished:**
- *Framework inputs (not derived here):* `nu_RAR` law, `δ = 0.05`, the max-rule
  `h'_mono = max(h'_RAR, P)`, splice-value continuity, `κ = 1/2` adopted (STANDING: fitted,
  measured 0.465±0.076; not derived), `a0 = κ c sqrt(G ρ_Λ)`.
- *Conclusions established here:* exact closed forms of `h'`, `h''`, the C¹∖C² splice class
  with the exact second-derivative jump, the force envelope, the derivative/first-derivative
  and Hessian mismatches, the recovery-rate gap, and the logarithmic divergence of the
  integrated derivative difference (the "log phantom").
- *New assumptions:* none beyond the framework's own declared cell. No branch imported for repair.

## 2. Force and derivative differences at the splice and the high-field tail

### 2.1 The splice (`y = y_star`)
By construction (value continuity + max-rule equality at the crossing):
- **force difference is exactly zero:** `nu_mono(y_star) = nu_RAR(y_star)` (`h` values equal ⇒
  `nu = 1 + h/y` values equal); measured `0.0` at 50 digits (check C2).
- **first derivative difference is exactly zero:** `h'_mono(y_star) = P(y_star) = h'_RAR(y_star)`
  by the crossing equation; measured `2.04e-51` (check C2bis, numeric zero at 50 dps).
- **second derivative jumps:** `h''_mono(y_star+) = P'(y_star) = −c/(y_star+y_p)²`, while
  `h''_RAR(y_star)` is finite; the jump is
  `J = h''_mono(y_star+) − h''_RAR(y_star) = −0.0013613480436970372 − (−0.03610606159853314)
       = +0.034744713554836104`.
  Hence the operative branch is **exactly C¹ and not C²** at the splice (matches the
  independent AS034 result `+3.4744713554836107e-2`).

### 2.2 The phantom peak (`y = y_p`)
At the peak `h'_RAR(y_p) = 0` by definition, while the continuation slope is positive:
`h'_mono(y_p) = P(y_p) = c/(2 y_p) = 0.0063750243728993815`.
Force error at the same point: `|nu_mono/nu_RAR − 1| = 0.00020886117564109785`
(9.07e-5 dex). **Ratio: the first-derivative error is 30.5× the force error at the same y**
(`0.0063750/0.00020886 = 30.52`).

### 2.3 High-field tail (`y → ∞`)
- `h_RAR(y) ~ y e^{−√y} → 0` ⇒ `nu_RAR − 1 ~ e^{−√y}` (exponential recovery).
- `h_mono(y) = h_star + c ln((y+y_p)/(y_star+y_p)) ~ c ln y` ⇒ `nu_mono − 1 ~ c ln(y)/y`
  (logarithmic recovery). Both → 0: Newtonian recovery holds on both branches.
- At `y = 1e3`: `(nu_mono−1)/(nu_RAR−1) = 4.4370990602661095e10` — **the phantom-recovery
  rates differ by 11 orders of magnitude at the same field** (log vs exponential tail).
- The **integrated derivative difference diverges exactly:**
  `∫_{y_star}^Y (h'_mono − h'_RAR) dy = h_mono(Y) − h_RAR(Y) = c ln(Y/(y_star+y_p)) + h_star − h_RAR(Y)`,
  evaluated `0.7410417792439832 (Y=1e2)`, `0.8938958897206144 (Y=1e4)`,
  `1.0430055175046185 (Y=1e6)`, `1.1921232040763083 (Y=1e8)` — **∝ ln Y** (the "log phantom":
  the accumulated phantom-`h` excess is unbounded while the pointwise force envelope is ≤ 0.0104 dex).

### 2.4 The norm required by a stability claim
The force envelope is an `L∞` control on the *constitutive function at the level of the
force law* `ν`. The field equation of the operative branch,
`∇²Φ = 4πGρ_b + S* div[(ν_mono(|∇Su|/a0) − 1) ∇Su]`, is second order in the potential; its
ellipticity, contraction and any well-posedness/stability argument depend on first and second
derivatives of the constitutive function (`ν'`, `ν''` ∝ `h'`, `h''`) through the symbol of the
nonlinear operator. A valid transfer therefore requires a `W^{1,∞}` (or `C²`) control on
`h_mono − h_RAR` — **not** the `L∞` force envelope. §2.2, §2.3 and the splice jump
demonstrate that the envelope controls none of these.

## 3. Algebra with scale factors, signs, units

All statements in this task are dimensionless (`y`, `h`, `ν`, derivatives w.r.t. `y`); the
single dimensional input is the footing `a0` used only in §5 and the footing table. The one
coefficient that appears is `c = δ·h_p = 0.05 × 0.6476102378919149 = 0.032380511894595745`
(dimensionless) — no other free coefficient entered.

**Derivation of `h'_RAR` (exact):** with `s = √y`, `ds/dy = 1/(2s)`,

```
d/dy [y/(e^s − 1)] = 1/(e^s−1) − y e^s (ds/dy)/(e^s−1)²
                  = [2s(e^s−1) − s² e^s] / [2s(e^s−1)²]
                  = [2(e^s−1) − s e^s] / [2(e^s−1)²].
```

**Peak condition (exact):** `h'_RAR(y_p)=0 ⇔ 2(e^s−1) = s e^s ⇔ (2−s)e^s = 2`, `s=√y_p`
(also the AS032 peak statement). Root: `y_p = 2.5396382821881653`, `h_p = 0.6476102378919149`
(bisection on brackets with sign change, 50 digits; check C1).

**Splice equation (exact):** `h'_RAR(y_star) = c/(y_star + y_p)`; root `y_star = 2.3374124052663294`
(check C1). Consistency with the amended requirement-1 landmarks (2.5396 / 2.3374) verified.

**Second derivative (exact, chain rule):**

```
h''_RAR = e^s [2s e^s − (e^s−1)(s+3)] / [4s (e^s−1)³].
```

**Continuation slope (exact):** `d/dy [h_star + c ln((y+y_p)/(y_star+y_p))] = c/(y+y_p)` —
certified in Lean (theorem `mono_continuation_deriv`), and numerically to 1e-51.

**Log-potential Poisson inversion (exact, 3-D):** for `Φ_ph = C ln(r/r0)`,

```
∇²Φ_ph = (1/r²) d/dr (r² C/r) = C/r²  ⇒  ρ_ph = C/(4πG r²)
```

— certified in Lean (theorems `log_potential_deriv`, `log_poisson_density`), numeric
residual 0.0 at 50 digits. On the MONO branch this is the deep-side phantom law
(`r ≫ r_M`, where `h_RAR ≈ √y`), with `C_ph = v_flat² = sqrt(G M_b a0)`.

**Radial phantom-density profile on the continuation** (`y = (r_M/r)²`):
`ρ_ph(r) = a0/(4πG r²) · d/dr [r² h_mono(y(r))]`, and the chain identity
`d/dr[r² h(y(r))] = 2r h − 2r y h'(y)`; on the continuation `h' = c/(y+y_p)` so
`ρ_ph(r) = (a0/2πG r)·(h − y·c/(y+y_p))` — a `1/r · ln(r_M/r)`-type phantom profile in the
log regime (not the deep-side `1/r²`). Independent numeric differentiation matches the closed
form to `2.2e-24 … 6.1e-21` (supplementary check); deep-side rows reproduce
`C_ph/(4πG r²)` to `≤ 5.26e-5` relative for `r ≥ 32 r_M` (asymptotic log-law approach, exact
limit certified by the Lean Poisson-inversion theorems).

## 4. Independent checks (different representations, actual residuals)

All tolerances were set before evaluation. Observed residuals (50-digit mpmath):

| check | representation | residual | tolerance | result |
|---|---|---|---|---|
| C1 landmarks | bisection vs declared equations | `y_p=2.5396382821881653, h_p=0.6476102378919149, y_star=2.3374124052663294` | within 1e-3/1e-5 of requirement-1 landmarks | pass |
| C2 splice force | pointwise `nu_mono/nu_RAR − 1` at `y_star` | `0.0` | < 1e-45 | pass |
| C2bis splice slope | `h'_mono − h'_RAR` at `y_star` | `2.04e-51` | < 1e-45 | pass |
| C3 splice Hessian jump | `J = −c/(y_star+y_p)² − h''_RAR(y_star)` | `+0.034744713554836104` | `|J| > 1e-6` (C¹∖C² detectable) | pass |
| C4 force envelope | sup `|log10(nu_mono/nu_RAR)|` on 181-pt dex grid + 4000-pt scan | `0.010370149547419268` at `y=14.351589377477898` | < 0.0104 dex (amended req-1 "most at y = 14.35") | pass |
| C5 peak derivative counterexample | `dh1/force` at `y_p` | `0.0063750 / 0.00020886 = 30.5` | ratio > 5 | pass |
| C6 max-rule pointwise | `h'_mono = max(h'_RAR, P)` on all grid points | max gap `0.0` | < 1e-45 | pass |
| C7 continuation derivative | numeric differentiation vs `c/(y+y_p)` (5 points) | all `0.0` | < 1e-45 | pass |
| C7b continuation 2nd deriv | numeric vs `−c/(y+y_p)²` (3 points) | `0, 3.26e-55, 5.10e-57` | < 1e-45 | pass |
| C8 FTC quadrature | `∫_{y_star}^y c/(t+y_p) dt` vs closed form | `3.1e-53 … 3.3e-52` | < 1e-45 | pass |
| C9 representation | `1+h_RAR/y ≡ 1/(1−e^{−√y})` on grid | max `3.03e-42` | < 1e-38 (50-dps dynamic-range floor; identity exact by algebra) | pass |
| supplementary S1 | Poisson inversion `ρ_ph = C/(4πG r²)`, numeric Laplacian | `0.0` | < 1e-45 | pass |
| supplementary S2 | `d/dr[r²h]` closed vs numeric | `1e-24 … 1e-21` | < 1e-18 | pass |
| supplementary S3 | deep regime `ρ_mono → C/(4πG r²)` | `≤ 5.26e-5` at `r ≥ 32 r_M` | asymptotic, `→0` with `1/√y` tail | pass |

## 5. Negative controls (both capable of failing)

**N1 — "Infer matching Hessians from a 0.0104-dex force envelope and display a derivative
counterexample"** *(registered seed's required control)*. Naive inference:
`|Δh''| ≤ (10^{0.0104} − 1)·|h''_RAR(y_star)| = 0.02417 × 0.036106 = 8.73e-4`.
Actual: `|Δh''| = |J| = 3.474e-2` — **39.8× above the envelope-scaled prediction**, and at
the same point the force error is *exactly zero*. The inference **fails**, and the displayed
counterexample is the splice itself (C¹∖C², `J = +0.034744713554836104`), reinforced by the
peak (30.5× slope excess at 9e-5 dex force error), the tail (recovery-rate ratio
`4.44e10` at `y=1e3`), and the divergent integrated derivative difference (∝ ln Y).
**Control verdict:** exercised, capable of failing, failed the inference as required.

**N2 — deep and Newtonian limiting regimes.** *Deep, `y → 0`:* below the splice MONO ≡ RAR
exactly (`h'_RAR → 1/(2√y) ≫ P(0) = c/y_p`, so the max rule selects the RAR branch), force
error `0.0`, and `h_RAR(y)/√y → 1` (deep-MOND `h ~ √y`; measured `0.9999950000083333` at
`y=1e-10`, series match to ~1e-12). *Newtonian, `y → ∞`:* both `ν → 1` (measured
`ν_mono−1 = 1.192e-8`, `ν_RAR−1 = 0` at `y=1e8`, i.e. recovery on both), but with the
disparate rates of §2.3 (log/y vs exp(−√y), ratio `4.44e10` at `y=1e3`). Exact identities
(normalization/boundary cases) are distinguished from numeric checks: C7/C7b/C8 are exact
derivative/FTC identities at 1e-45; C4's envelope value is a numeric sup on declared grids.

## 6. Strongest surviving statement (exact_claim)

With `y = B/a0 > 0`, `h_RAR(y) = y/(e^{√y}−1)`, `δ = 0.05`, `y_p` the unique maximum of
`h_RAR`, `h_p = h_RAR(y_p)`, `y_star` the unique splice solution of
`h'_RAR(y_star) = δ h_p/(y_star+y_p)`, and the operative continuation
`h_mono(y) = h_RAR(y_star) + δ h_p ln[(y+y_p)/(y_star+y_p)]` for `y ≥ y_star`, `ν = 1 + h/y`:

1. **Force envelope:** `sup_y |log10(ν_mono/ν_RAR)| = 0.010370149547… dex` (extremum at
   `y = 14.3516`), consistent with the amended requirement-1 bound "within 0.0104 dex, most
   at y = 14.35".
2. **The envelope does not control the first derivative:** at `y_p`, force error `9.07e-5 dex`
   (2.09e-4 relative) vs `|h'_mono − h'_RAR| = δ h_p/(2 y_p) = 6.375e-3` (30.5×); on the tail
   the recovery rates differ by `4.44e10` at `y = 1e3`.
3. **The envelope does not control the second derivative:** the splice is exactly `C¹ ∖ C²`
   with `h''` jump `J = h''_mono(y_star+) − h''_RAR(y_star-) = −δ h_p/(y_star+y_p)² − h''_RAR(y_star)`,
   numerically `−0.0013613480436970372 − (−0.03610606159853314) = +3.4744713554836107e-2`;
   pointwise force error at the same point is exactly `0`.
   The naive Hessian inference from the envelope fails by 39.8×.
4. **The integrated derivative difference diverges logarithmically:**
   `∫_{y_star}^Y (h'_mono − h'_RAR) dy = h_mono(Y) − h_RAR(Y) = 0.741 (Y=1e2) … 1.192 (Y=1e8)`,
   unbounded ∝ `δ h_p ln Y` while the force envelope stays ≤ 0.0104 dex — the "log phantom".

**⇒ Norm required for transfer:** a stability/ellipticity claim on the operative filtered
field equation needs a `W^{1,∞}` control (or an explicit ellipticity-ratio bound across the
splice) on `h_mono − h_RAR`; the `L∞` force envelope alone is insufficient. Statements 2–4
are exact/analytic consequences of the declared branch (with the numerically-bracketed
landmarks `y_p`, `y_star`); the envelope's sup value is a numeric result on the declared grids.

## 7. Log-phantom disk profiles (appendix answering the dispatch brief's title)

Derived on the same MONO branch (supplementary script `AS047_supplementary.py`):

- **Phantom density from the log potential (exact 3-D inversion, Lean-certified):**
  `Φ_ph = C ln(r/r0) ⇒ ρ_ph = C/(4πG r²)`, `C = v_flat² = sqrt(G M_b a0)`.
  Numeric Laplacian residual `0.0` at 50 digits.
- **MONO continuation (log) regime:** for `y ≫ y_star ⟺ r ≪ r_M/√y_star
  (= 7981 pc canonical / 7271 pc alternative for M_b = 1e11 M_sun)`,
  `h_mono ~ δ h_p ln y` and the spherical radial phantom density is
  `ρ_ph(r) ≈ (a0/2πG r)·(h − y δ h_p/(y+y_p))` — `1/r` with `ln(r_M/r)` modulation (log
  phantom), not the deep-side `1/r²`.
- **Rotation curve** (radial circular speed `v² = G M_b/r + a0 h_mono·r`): flat part
  `v_flat⁴ = G M_b a0` (187.7 km/s canonical / 196.7 km/s alternative at 1e11 M_sun),
  with log corrections on the continuation bounded by the §6 envelope control on 2.4% force;
  deep side `v/v_flat → 1` (1.0025 at `r = 100 r_M`).
- **Surface-density consistency:** plane-parallel `g_N = 2πG Σ` gives `y = Σ/Σ_crit`,
  `Σ_crit = a0/(2πG) = 0.22324 kg m⁻²` (canonical) / `0.26896 kg m⁻²` (alternative)
  (`0.0223 / 0.0269 g cm⁻²`); the splice sits at `Σ_star = y_star·Σ_crit =
  0.5218 / 0.6287 kg m⁻²`; the log regime is the high-`Σ` (inner-disk) side, the `1/r²`
  phantom the low-`Σ` (outer) side.
- **Domain of the approximation:** the continuation formula is exact on `y ≥ y_star` by
  construction; its log asymptote `h ~ δ h_p ln y` is the operative behavior for
  `y ≫ y_star` (i.e. `r ≪ 0.654 r_M`), and the deep `1/r²` law holds for `r ≫ r_M`.
  **This appendix is a spherical radial proxy: no full nonspherical disk field solve was
  performed** (out of the registered seed's scope; the disk solve is a separate gate).

## 8. Footings (mandatory, both separately)

| quantity | canonical `a0 = 9.3619e-11 m/s²` | alternative `a0 = 1.1279e-10 m/s²` |
|---|---|---|
| `ρ_Λ = 4a0²/(Gc²)` | `5.844412454021875e-27 kg m⁻³` | `8.483089619559098e-27 kg m⁻³` |
| `κ_eff` if `ρ_Λ` fixed | — | `0.6023884040632778` |
| `r_M` (M_b = 1e11 M_sun) | `12201.97 pc` | `11116.72 pc` |
| `v_flat` (same M_b) | `187.747 km/s` | `196.698 km/s` |
| `g(y_star)` | `2.18826e-10 m/s²` | `2.63637e-10 m/s²` |
| `C_ph = v_flat²` | `3.52488e10 m²/s²` | `3.86899e10 m²/s²` |
| `Σ_crit = a0/(2πG)` | `0.22324 kg m⁻²` | `0.26896 kg m⁻²` |
| `r_log_domain = r_M/√y_star` | `7981.1 pc` | `7271.2 pc` |

The dimensionless theorem (§6) is footing-independent and applies identically on both
footings; every dimensional example is reported separately. `κ = 1/2` remains an adopted
input (`rho_Lambda` fixed ⇒ alternative footing implies `κ_eff = 0.6024`; `κ` fixed ⇒
alternative density as tabulated). `G_N`, `G_bare`, `G_cosmo` kept separate; only the
measured Newton `G = 6.67430e-11` enters this task.

## 9. Limitations

- The envelope sup `0.01037 dex` is a numeric result on the declared grids, not an exact
  global inequality; `y_p`, `h_p`, `y_star` are 50-digit roots, not exact closed forms.
- No statement about the filtered field equation: heat filter `S = e^{(ξ²/2)Δ}`,
  `S*div[(ν_mono−1)∇Su]` regularity, ellipticity ratio across the splice, well-posedness,
  criterion B or the thirteen-item target are **not** established here; the C¹∖C² kink's
  distributional role in the filtered operator is an open consequence (AS034's C01).
- The log-phantom divergence (∝ ln Y of the integrated derivative difference; `1/r·ln` phantom
  density on the continuation) is a property of the unbounded continuation on `(y_star, ∞)`;
  real disks are finite — the phantom-mass budget cutoff for a finite disk is not computed here.
- The disk-profile appendix is a spherical radial proxy; no nonspherical disk field solve.
- `κ = 1/2` adopted, not derived; `δ = 0.05` and the max-rule are framework inputs.
- The dispatch brief's task title does not exist on disk; the registered seed was executed
  and the discrepancy is recorded in §0 (this is a provenance finding, not a scientific one).

## 10. Next unresolved implication

The first missing bridge to the full theory: **quantify the norm that the force envelope
actually controls at the level of the operative filtered static operator** — i.e., the
distributional class and ellipticity ratio of `S*div[(ν_mono(|∇Su|/a0)−1)∇Su]` on both sides
of the C¹∖C² splice, and a certified `W^{1,∞}` bound on `h_mono − h_RAR` (or an explicit
ellipticity-ratio inequality) that would license any stability/well-posedness transfer.
Second: the finite-disk truncation of the log-phantom mass budget (`∫ρ_ph d³x` diverges on
the unbounded continuation; a finite exponential disk cuts it — quantify the cutoff scale
and its dependence on `r_M`, `Σ_crit`).

## 11. Suggested followup (one discriminating continuation)

Dispatch **AS047.C01 (proposed)**: "Derivative-norm transfer across the MONO splice" —
certified (Lean + numeric) ellipticity-ratio bound `λ_max/λ_min` of the spliced constitutive
operator across `y_star` under the heat filter at fixed `ξ`, with a mutated-jump control
(increase `δ` → show the bound tightens; decrease → loosens, so the control can fail) and the
`W^{1,∞}` difference bound; plus compute the finite-disk phantom-mass cutoff for an
exponential disk on the log continuation (ties to AS090/AS091/AS1488). Dependencies: this run
(unreviewed), AS034 (unreviewed), FRAMEWORK_CONTRACT MONO cell, FRIED_CHICKEN requirement-1.
Dispatch state: spec proposed in result.json only; not dispatched (no child runner in wave).

## 12. Provenance

- Registered seed executed: `deepseek_push/astra_spawn_ideas/AS047_uniform_force_error_versus_derivative_error_control.md`
  (sha256 `ddab4669ce9f5f2f122e04acf651726f4bf26532bd134ba9266be285959fd287`; matches the
  claims-ledger pin and `INDEX.md`).
- Source hashes verified against `SOURCE_MANIFEST.json`: README `91a5fac4…`,
  FRIED_CHICKEN_SPEC `98d9149f…`, peer-review README `521d9ac3…` — all exact.
- Lean certificate: `AS047_certificate.lean`, 3 theorems, exit 0, zero `sorry`,
  axioms = {propext, Classical.choice, Quot.sound}.
- All artifacts hashed in `result.json` (`artifacts_sha256`).
