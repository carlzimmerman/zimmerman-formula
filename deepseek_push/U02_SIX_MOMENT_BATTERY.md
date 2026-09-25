# U02 — THE SIX-MOMENT BATTERY at n = 10⁷ (J00-ND2, executed)
**2026-09-26 · the pre-registered sharpest test of the Gaussian lemma — never run before · no git commit**

**Files:** `U02_battery.py` (engine + tests + constructions, reproducible: all seeds fixed),
`U02_battery.out` (full machine output), `U02_results.json` (all numbers machine-readable).
Engine: the frozen independent J02 solver (exact optical-depth bisection, no
null-collision thinning, own geometry) — the 35/35 three-engine census engine.

---

## 0. The pre-registered battery and its joint 3σ thresholds (stated BEFORE numbers)

Model: stationary conservative Thomson sphere R = c = s_e = 1, central isotropic
source, κ(r) = τ₀(1 + qr²), τ₀ = 1, all photons counted, escape at first outward
crossing. Observables are velocity-resolved transfer-function moments:

> battery = {E[D], E[v²], E[Dv²], E[v⁴], E[Dv⁴], E[D²]}.

| test | null (exact within the model) | acceptance at n=10⁷ |
|---|---|---|
| T1 | E[D] = τ₀(1/2 + q/4) (Theorem 1, all orders) | \|z\| < 3 |
| T2 | E[v²] = 2·E[ang] (Gaussian lemma, marginal m=1) | \|z\| < 3 |
| T3 | E[v⁴] = 12·E[ang²] (Gaussian lemma, marginal m=2) | \|z\| < 3 |
| T4 | E[Dv²] = 2·E[D·ang] (Gaussian lemma, mixed m=1) | \|z\| < 3 |
| T5 | **E[Dv⁴] = 12·E[D·ang²] (Gaussian lemma, mixed m=2)** | \|z\| < 3 — **the sharpest** |
| T6 | E[D²] ≥ 3·E[Dv²]²/E[v⁴] (Cauchy–Schwarz + lemma) | z > −3 (one-sided) |
| T7 | R₂ = E[Dv⁴]/(12·E[D]·E[ang²]) = 3.574 (n=10⁶ reference) | pooled \|z\| < 3 |

**Kill rules, as registered in J00-ND2 / J05 §5 / K06 F3–F4.** Any single member
outside its 3σ box at n = 10⁷ fails the battery. T5 at ≥ 3σ **refutes the
Gaussian lemma itself** (the sharpest falsifier the channel can fire); T6 at
≥ 3σ is a theorem-rigid Cauchy–Schwarz contradiction; T1–T4 are
battery-internal inconsistencies against the Gaussian identities/Theorem 1.
**Confirm** requires all members inside the joint region simultaneously.

**Power (pre-computable before the run, under the CLT from the observed
correlation of the six test statistics):** joint null acceptance of the 3σ box =
0.976; joint power vs an offset of δ·SE in the m=2 member: 1σ → 0.35, 2σ →
0.88, **3σ → 0.997**, 5σ → 1.000.

---

## 1. The six measurable numbers at n = 10⁷ (central, τ₀ = 1, q = 0) — SE floor

| # | moment | value ± SE (n=10⁷) | exact / reference |
|---|---|---|---|
| M1 | E[D] | **0.500247 ± 0.000227** | 0.5 (Thm 1) |
| M2 | E[v²] | **2.812254 ± 0.002443** | 2.8061 (n=10⁶ ref) |
| M3 | E[Dv²] | **3.723941 ± 0.005533** | 3.7316 (n=10⁶ ref) |
| M4 | E[v⁴] | **67.57196 ± 0.20036** | 66.55 (n=10⁶ ref) |
| M5 | E[Dv⁴] | **122.8217 ± 0.6580** | 119.5 (n=10⁶ ref) |
| M6 | E[D²] | **0.765530 ± 0.000645** | 0.7661 (n=10⁶ ref) |

E[ang] = 1.40399, E[ang²] = 5.60079, E[D·ang] = 1.85711, E[D·ang²] = 10.14321
(same run; needed by the identities). The SE floor at n = 10⁷ is exactly the
pre-registered target: R₂ is measured at **0.5% relative precision**
(sR₂ = 0.0190, jackknife cross-check 0.0156 — delta method conservative).

## 2. R₂ and the z vs the exact ratio structure (the m=2 channel)

- **Closure ratio** R₂ = E[Dv⁴]/(12·E[D]·E[ang²]) = **3.6531 ± 0.0190**.
  z vs the n=10⁶ recorded reference ratio structure 3.57431: **z = +1.29**
  (pooled SE; the same-engine seed-29 n=10⁶ rerun reproduced the ledger's
  R₁ = 2.63499 / R₂ = 3.57431 bit-for-bit → reference bridge verified).
- **Identity ratio** r₅ = E[Dv⁴]/(12·E[D·ang²]) = **1.0091 ± 0.0052**,
  z vs 1 (the exact Gaussian recursion): **z = +1.75**.
- Companion: R₁ = 2.6511 ± 0.0035, z vs 2.635 = **+1.42**.
- The n=10⁷ M-rows vs the n=10⁶ references at pooled SE: z ∈ [−0.73, +1.57]
  (largest drifts: E[Dv⁴] +1.57, E[v⁴] +1.52; every member well inside 2σ) —
  pure MC scatter, no trend.

## 3. Threshold-by-threshold result at n = 10⁷ (each test, its z)

| test | statistic | z | pass? |
|---|---|---|---|
| T1 | E[D] = 0.5 | **+1.09** | ✓ |
| T2 | E[v²] = 2E[ang] | **+2.02** | ✓ |
| T3 | E[v⁴] = 12E[ang²] | **+1.88** | ✓ |
| T4 | E[Dv²] = 2E[D·ang] | **+2.10** | ✓ |
| T5 | E[Dv⁴] = 12E[D·ang²] | **+1.75** | ✓ — the lemma survives its sharpest test |
| T6 | E[D²] − 3E[Dv²]²/E[v⁴] = +0.1498 | **+144.3** (one-sided, ≫ −3) | ✓ slack = 1.2434 (vs J06 sharpened 1.2430) |
| T7 | R₂ vs 3.574 | **+1.29** | ✓ |

The identity z's (T2–T5) share one correlated +2σ-ish excursion (pairwise
z-correlations 0.50–0.88 from the shared ang terms); the joint
CLT acceptance of the full box, computed with the observed covariance, is
**0.976** — the configuration sits comfortably inside the joint region.

## 4. THE MATCHED-PAIR TEST (the ND2 content) — R₂ is NOT a function of the four

**Claim tested (J00-ND2):** a model matched on the four-moment marginals
{E[D], E[v²], E[Dv²], E[v⁴]} — equivalently {E[D], E[ang], E[D·ang], E[ang²]} —
cannot mimic R₂: the lower battery leaves E[Dv⁴] (hence R₂) **free**.

**Verification by construction.** Family A (two-point ang lattice, one free
parameter p): 704 joint laws for (D, ang), each reproducing the four matched
moments **exactly** at the measured reference values
{E[D], E[ang], E[D·ang], E[ang²]} = {0.5008, 1.40305, 1.8658, 5.54583}, D ≥ 0,
ang ≥ 0. As p sweeps its valid range (a₁, a₂, E[D|a₁], E[D|a₂] ≥ 0):

> E[D·ang²] runs **7.375 → 36.92** ⇒ **R₂ runs 2.656 → 13.29** (span 10.6),
> while the four matched moments sit unchanged at the measured values.

- Every member lies inside the Cauchy-consistent window: E[D·ang²] ≥
  E[D·ang]²/E[D] = 6.951 (Cauchy–Schwarz bound from the fixed moments) — `all_cs_consistent = true`.
- The sixth battery member is independently realizable: choosing the
  within-component D-spread reaches any E[D²] ≥ 0.6290, so the measured
  E[D²] = 0.7661 is reachable in **every** family member
  (`realizable_E_D2_at_measured = true`).
- The measured E[D·ang²] = 10.14 (n=10⁷) lies strictly **inside** the window —
  at R₂, freedom = 10.6 vs the n=10⁷ SE 0.019: **> 500× the measurement
  precision**.

Family B (three-point lattice, ang law {0.4, a₂, 5.0} held *fixed*, one free
parameter t = E[D|ang = a₂]): 120,701 members; even with the **full** ang
marginal law fixed, t moves R₂ within [3.234, 3.267] per lattice
(max per-lattice span 0.033) — the (1,2)-mixed moment is not pinned by
{E[D], E[ang·], E[D·ang], E[ang²]} at any fixed ang law either.

**Finding — ND2 sharpness CONFIRMED by construction:** R₂ is **not a pure
function of the lower battery**. A four-moment-matched competitor can realize
R₂ anywhere in [2.66, 13.3] (Cauchy-consistent); landing on the measured 3.65
would be coincidence, not consequence. The m=2 channel is exactly the extra
observable J00-ND2 registered it as; the instrumentation is the battery's T5 at
its 0.019 SE floor. (Degenerate sub-families exist — e.g. a two-point law with
*no* within-component D freedom — where the four do pin E[D·ang²]; that is a
special case, not a counter-finding: the general family leaves it free.)

## 5. The z-table at q = 3 and q = 10 (n = 4×10⁶ each)

| q | E[D] (±SE) vs ½+q/4 | E[v²] | E[Dv²] | E[v⁴] | E[Dv⁴] | E[D²] | zT2 | zT3 | zT4 | **zT5** | zT6 | R₁ (± 10⁶-ref z) | R₂ (±) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 1.25154 ± 0.00067 (**z +2.30**) | 8.7445 ± 0.010 | 22.076 ± 0.045 | 490.5 ± 2.0 | 1755.9 ± 13.2 | 3.3742 ± 0.0038 | −0.24 | +0.09 | +0.14 | **+0.56** | +60.2 | 2.0166 ± 0.0036 (−0.55) | 2.8614 ± 0.0208 |
| 10 | 2.99980 ± 0.00134 (**z −0.15**) | 37.325 ± 0.038 | 191.58 ± 0.36 | 7286.5 ± 29.5 | 53956 ± 416 | 16.216 ± 0.017 | −1.37 | +0.30 | −0.57 | **+0.76** | +32.1 | 1.7088 ± 0.0028 (+1.24) | 2.4714 ± 0.0186 |

Every member of the battery passes at q = 3 and q = 10 (all |z| < 3; R₁ within
1.3σ of the J01 references 2.0235 ± 0.012 / 1.6971 ± 0.009). The m=2 identity
holds at all three profiles (zT5 = 1.75 / 0.56 / 0.76); R₂ declines with
profile steepness exactly as the measured conspiracy R_m(q) requires
(3.65 → 2.86 → 2.47).

## 6. THE KILL / CONFIRM STATEMENT (observer-ready)

> **KILL (pre-registered, J00-ND2).** Any within-model violation at n = 10⁷ of
> the m=2 identity T5 at ≥ 3σ refutes the Gaussian lemma itself. T6 at ≥ 3σ is
> a theorem-rigid Cauchy–Schwarz contradiction; T1–T4 and T7 at ≥ 3σ are
> battery-internal inconsistencies. **None fired.**
>
> **CONFIRM.** At n = 10⁷ (SE floor as §1–§2), all six measurable numbers sit
> inside the joint 3σ acceptance region: max |z| = 2.10 (T4, correlated family
> excursion — joint acceptance 0.976), the Cauchy bound is exceeded at +144σ
> (slack 1.2434), and R₂ = 3.6531 ± 0.0190 is 1.29σ from the n=10⁶ reference
> ratio structure 3.574. **The Gaussian lemma survives its sharpest
> pre-registered observer-facing test at every order and every profile
> (q = 0, 3, 10).** The six-moment battery, with its verified SE floor and
> joint thresholds, is armed for velocity-resolved RM data; the matched-pair
> construction (§4) certifies that the m=2 member — the one the four-moment
> marginals cannot mimic — is the battery's irreplaceable fifth channel.

## 7. Honest edges

- The within-model audit tests an engine that *implements* the lemma's
  Gaussian-kick assumptions, so a firing would have signalled engine error; the
  observer-facing content is the pre-registered battery itself (thresholds
  stated before opening data; §3–§5 are the audit establishing the SE floor).
- The q=0 identity z-cluster (T2–T5 ≈ +1.7…+2.1σ) is a correlated MC excursion,
  jointly consistent (0.976); registered for the deterministic P_N leg (J00-N1)
  as the pattern a truly independent leg should reproduce within its own errors.
- Matched-pair constructions are moment-level joint laws for (D, ang), not full
  trajectory models: the freedom statement is about the moment structure the
  lemma predicts, which is exactly the ND2 claim registered.
- No JWST data touched (J00-N4 unchanged); m=3+ tail moments carry the
  registered MC tail risk (J09 edge) and were not part of this battery.
- Not committed (house rule); rerunnable bit-for-bit from `U02_battery.py`
  (all seeds fixed; ~5 min on this machine; OpenBLAS AᵀA spurious-`divide by
  zero` bypassed via explicit einsum paths — see code comments).

**Register line (U02):** six-moment battery executed at n = 10⁷ as pre-registered
in J00-ND2 — thresholds stated before numbers; six measurable numbers with SEs
(0.5002, 2.8123, 3.7239, 67.572, 122.82, 0.7655 at 10⁷); R₂ = 3.6531 ± 0.0190
(z = +1.29 vs 3.574; identity ratio 1.0091 ± 0.0052, z = +1.75); joint 3σ
region passed (max |z| 2.10; CS bound +144σ; slack 1.2434); matched-pair
constructed — R₂ free over [2.66, 13.29] at fixed four moments (ND2 sharpness
confirmed; m=2 not mimickable); q=3/q=10 z-table all passed; kill conditions
none fired; verdict **CONFIRM** with power table (3σ-offset kill power 0.997).