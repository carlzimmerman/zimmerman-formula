# PRE-REGISTRATION — a0-line ESTIMATOR-BIAS MOCK STUDY

**prereg_id:** `a0_line_estimator_bias_v1`
**Frozen:** 2026-07-25, BEFORE any mock was generated and BEFORE any estimator other than the
two already-committed ones was evaluated on anything.
**Frozen artifacts:** this file, `prereg_estimator_bias_config.json`, `prereg_freeze.py`.
Digests in `PREREG_ESTIMATOR_BIAS.sha256`.
**Framework:** Zimmerman de Sitter–Unruh **modified-inertia** framework, its OWN interpolation
`g_obs = sqrt(g_bar^2 + a0*g_bar)`, horizon-derived `a0 = c*H_Lambda/Z`, `Z = sqrt(32*pi/3)`.
Judged on its own terms; McGaugh's ν is never used as the yardstick.

---

## S0. THE QUESTION, AND WHAT THIS STUDY CAN AND CANNOT SETTLE

Committed Step-A ground truth (`per_galaxy_budget.py`, `reach_target.py`, `estimator_theory.py`):
on the gas-dominated SPARC subsample (**49 galaxies, 310 points**, point cut
`Vgas^2 > Ud*Vdisk^2 + Ub*Vbul^2` at `Ud = 0.70`, `Ub = 1.4*Ud`), the a0-line box is **16.1%** and
**estimator choice is the single largest variance term (30.1%)** — larger than Υ (25.3%) and
gas-cal (20.6%). The two committed estimators disagree by `2.089e-11` = **22% of canonical**, which
**exceeds the footing gap itself** (`ALT − canonical = 1.951e-11` = 21%):

| estimator | real-data value | lands on |
|---|---|---|
| GLS through-origin, `a0_hat = Σ w E g / Σ w g²`, `E = g_obs² − g_bar²`, `g = g_bar` | `1.181e-10` | ≈ ALT footing `1.1305e-10` |
| robust median of per-point `a0_pt = (g_obs² − g_bar²)/g_bar` | `9.726e-11` | ≈ canonical `9.355e-11` |

So **how you fit the slope decides which footing you get.** That is why Step A returned NO-GO.
This is a *statistics* question, answerable today with mocks — not a data limitation.

**What this study CAN settle:** whether each candidate estimator recovers a *known injected* a0
without bias, and with what scatter — i.e. whether the 22% spread is an estimator artifact or real
data structure.

**What it CANNOT settle:** (i) whether the framework's ν is correct — the mocks are generated FROM
that ν, so they are circular with respect to it by construction and are used only as an estimator
testbed; (ii) the framework's coefficient. **a0's VALUE remains POSITED regardless of which
estimator wins.** This resolves a MEASUREMENT ambiguity, not the theory's free parameter. No
"theory closed", no TOE claim, both footings carried on every dimensional number.

---

## S1. THE MOCK RECIPE (fixed truth structure — real SPARC, not synthetic galaxies)

**Sample (fixed, never re-drawn):** `fire_common.load(Ud=0.70)` → per-galaxy `gasdom` point mask.
SPARC cuts `Q<=2`, `inc>=30 deg`, point cut `eV/Vobs < 0.10` (Lelli+2017). Asserted:
**N = 310 points, N_gal = 49.** The 49 galaxy names, their `f_D`, `sigma_lnD`, inclination,
points-per-galaxy, and the per-point `(g_bar_true, phi, fv)` triples are enumerated verbatim in
`prereg_estimator_bias_config.json → sample.manifest`. Distance-method census (galaxies):
**29 Hubble-flow (σ_lnD = 0.25), 18 TRGB (0.05), 2 UMa (0.10)**; per-point census
**154 / 147 / 9**. Sample spans `y = g_bar/1e-10` from **0.0088 to 0.1735** (median 0.044) —
the subsample is **deep-MOND throughout**; `phi` (stellar share) median 0.344, max 0.500;
`fv` median 0.046, max 0.0998; inclinations 30–90°; 1–23 points per galaxy.

**Truth:** the real data's `g_bar` values ARE the truth structure. They are held fixed and are
never regenerated from a model — this is what "use the REAL gas-dominated structure" means here.

**Injection (exact identity, no approximation):**

```
g_obs_true_i = sqrt( g_bar_true_i^2 + a0_inj * g_bar_true_i )
```

**Observable generation** (order: global offsets → per-galaxy offsets → per-point noise):

```
g_bar_obs_i = g_bar_true_i * ( phi_i*exp(dlnU) + (1-phi_i)*exp(dlnG) ) * exp(eps_shape_i)
g_obs_obs_i = g_obs_true_i * exp(-dlnD_k) * ( sin(inc_k)/sin(inc_k+di_k) )^2 * (1+dv_i)^2
E_i         = g_obs_obs_i^2 - g_bar_obs_i^2          # NO clipping
a0_pt_i     = E_i / g_bar_obs_i                      # NO clipping
```

`g_bar` is **exactly** distance-independent for gas AND stars (`estimator_theory.py` S2,
sympy-verified: `d ln g_bar/d lnD = 0` for both components); distance enters only via
`g_obs ∝ 1/D`. Hence `d ln g_obs = -dlnD - 2 dln sin i + 2 dv/v`, which reproduces the committed
S3 sensitivities exactly.

**Error terms (magnitudes, all lifted from `fire_common.py` — nothing invented):**

| term | symbol | distribution | scope | source |
|---|---|---|---|---|
| stellar M/L offset | `dlnU` | `N(0, 0.23)` | **GLOBAL**, one draw / realization | `SIG_LNU = 0.23` = 0.10 dex |
| gas-calibration offset | `dlnG` | `N(0, 0.10)` | **GLOBAL**, one draw / realization | `SIG_LNG = 0.10` |
| `g_bar` shape scatter | `eps_shape` | `N(0, 0.10)` | per point, independent | `SLNB = 0.10` |
| distance | `dlnD` | `N(0, sigma_lnD[f_D])` | per galaxy, independent | `SIG_LND = {Hubble-flow 0.25, TRGB 0.05, Cepheid 0.05, UMa 0.10, SNIa 0.08}` |
| inclination | `di` | `N(0, 3 deg)` | per galaxy, independent | `SIG_INC = 3 deg`; redraw if `inc+di ∉ (5°, 90°]` |
| velocity | `dv` | `N(0, fv_i)` | per point, independent | `fv_i = eV_i/Vobs_i` from the REAL data |

**The deep-MOND error amplification is DERIVED, never injected.** The `~4(y+1)` lever on `a0_pt`
is a *consequence* of the forward model above; adding it by hand would double-count. It is
therefore promoted to a validation gate (V2/V3, §S4): the mock must be shown to reproduce
`d a0_pt/d(dv/v) = +4 a0 (y+1)` and the "`~2σ`, not `σ/2`" amplification numerically. At this
sample's `y ≲ 0.17` the lever is `4(1+y) ≈ 4.0–4.7`, so per-point `a0` errors are large by
construction (median velocity term alone ≈ 19%; a Hubble-flow galaxy's distance term
≈ `2(1+y)·0.25` ≈ 52%; a 30°-inclination galaxy's ≈ `4(1+y)·cot(30°)·0.0524` ≈ 38%).

**Two anti-smuggling clauses.** (1) The gas-dominated point set is **NOT re-cut** on the mock
observables — re-applying the gas cut to noisy mocks would inject a selection effect absent from
the real pipeline. (2) Negative `E` or negative `a0_pt` are **NOT** clipped, dropped, or floored;
clipping would itself bias the estimators under test.

---

## S2. THE THREE INJECTED VALUES, AND THE REALIZATION COUNT

Mocks are generated at **all three** values so **neither footing is privileged**:

| label | injected a0 (m/s²) |
|---|---|
| canonical `c*H_Lambda/Z` | `9.354769736111044e-11` |
| ALT `c*H0/Z` | `1.1305322040279838e-10` |
| standard-MOND `g_dagger` | `1.2e-10` |

**An estimator that is unbiased must be unbiased at ALL THREE.** Unbiasedness at only one injected
value is a red flag and is a hard disqualifier (gate G3).

**Realizations: `N_real = 2000` per injected value.** Seed `20260725`; per-realization streams via
`numpy.random.default_rng(SeedSequence(20260725).spawn(N_real)[r])`.
**Common random numbers:** all estimators see the same realizations, and the same noise draws are
reused across the three injected values (paired design), so estimator-to-estimator and
injection-to-injection differences are not Monte-Carlo noise. `sigma_MC` on the median ratio
(`≈ 1.2533·s/sqrt(N_real)`) must be computed and reported and must be **< 0.50 pp**; if wall clock
forces `N_real` below 2000 the floor is **1000** and `sigma_MC` must stay **< 0.70 pp**, with the
reduction recorded in the results file.

A vectorized reimplementation of `fire_common.gls` is permitted **only** with an in-script
assertion that it agrees with `fire_common.gls` to `<1e-12` relative on (a) the real gas-dominated
sample and (b) 20 mock realizations.

---

## S3. THE ESTIMATORS UNDER TEST (frozen list — nine)

1. **`gls_origin`** *(incumbent)* — `fire_common.gls`: iterated through-origin GLS with
   MODEL-based weights, `a0_hat = Σ w E g / Σ w g²`, `w = 1/sig2_model`, `f_int` iterated to
   `chi²/N = 1`.
2. **`median_a0pt`** *(incumbent)* — median over points of `a0_pt`.
3. **`theilsen_pairwise`** — Theil–Sen with **free intercept**: median over all `i<j` pairs with
   `g_j ≠ g_i` of `(E_j−E_i)/(g_j−g_i)`; all 47,895 pairs used exactly (no subsampling at N=310).
   Intercept `median(E − slope·g)` reported as a diagnostic only.
   *Note:* the origin-anchored Theil–Sen is algebraically identical to `median_a0pt`, so the
   free-intercept form is the only non-degenerate Theil–Sen variant.
4. **`trimmed_mean_a0pt`** — symmetric 20%-trimmed mean of `a0_pt` (drop lowest 20% and highest
   20%; a standard robust choice, fixed in advance).
5. **`ivw_median_a0pt`** — weighted median of `a0_pt` with `w_i = g_bar_i² / sig2_model_i`, i.e.
   the **same error model as the GLS** (weights evaluated at the `gls_origin`-converged `a0` and
   `f_int`: a two-stage estimator). This directly probes the "GLS upweights high-`g_bar`"
   hypothesis while staying robust.
6. **`galaxy_median_then_median`** — per-galaxy median of `a0_pt`, then the unweighted median over
   the 49 galaxy values.
7. **`galaxy_gls_then_median`** — per-galaxy through-origin GLS `a0_hat_k`, then the unweighted
   median over the 49 values.
8. **`log_median_a0pt`** — `exp(median(ln a0_pt))` over points with `a0_pt > 0`; the count of
   discarded non-positive points is reported per realization (needing to discard them is itself a
   defect to be reported, not hidden).
9. **`gls_lowy`** — `gls_origin` restricted to `g_bar < 1.0e-10` (`y < 1` at a **footing-neutral**
   reference scale fixed in advance and NOT tuned; `1.0e-10` lies between the canonical and ALT
   candidates). Diagnostic estimator for the catastrophic-cancellation / high-`g_bar`-leverage
   hypothesis.

**Pre-registered mechanism hypotheses (to be tested, NOT assumed, and NOT part of any gate).**
The brief's proposed mechanism is that GLS weights `∝ w·g_bar²` upweight high-`g_bar` points where
`E = g_obs² − g_bar²` is a small difference of large numbers (catastrophic cancellation) and where
M/L leverage `~phi·a0·(2y+1)` is maximal. Honesty note recorded in advance: on **this** subsample
`y ≤ 0.174`, so `g_bar² ≤ 0.174·a0·g_bar` — `E` is NOT a small difference of large numbers here,
and the cancellation mechanism is *a priori weak*. Two alternative mechanisms are therefore
registered alongside it: **(M2)** weight concentration — `w·g_bar²` may put most of the effective
weight on a handful of points, so GLS has a small effective N and inherits their per-galaxy `D`/`i`
offsets; **(M3)** skew — `a0_pt` is strongly right-skewed by the `~4(y+1)` multiplicative lever, so
a mean-like estimator (GLS) and a median-like estimator differ by a *real* Jensen/skew offset even
when both are internally consistent. All three are diagnostics; the verdict rests on measured bias
and scatter only.

---

## S4. VALIDATION GATES THAT MUST PASS FIRST

**V1 — ZERO-NOISE NULL (the prerequisite).** With `dlnU = dlnG = eps_shape = dlnD = di = dv = 0`,
**every** estimator must return the injected value at **all three** injections:
`|a_hat/a0_inj − 1| < 1e-10` — **27 checks**. Justification of the tolerance: with zero noise
`E_i = a0_inj·g_bar_i` exactly, so every listed estimator is algebraically exact independent of its
weights; float64 roundoff on sums of 310 terms is `~1e-14`, so `1e-10` is a generous machine-level
bound. **On failure: HARD HALT** — the mock or that estimator is broken and must be fixed before
any noisy realization is run; no bias number from a failed build may be used.

**V2 — LINEAR RESPONSE.** Enabling each noise term alone at small amplitude, the measured per-point
`d a0_pt/d(lever)` must match the committed sympy coefficients — `-2a0(y+1)` for `lnD`,
`-4a0(y+1)` for `ln sin i`, `+4a0(y+1)` for `dv/v`, `-phi·a0(2y+1)` for `lnUpsilon`,
`-(1-phi)·a0(2y+1)` for `ln gascal` — to **< 1%**. On failure: HARD HALT.

**V3 — DEEP-MOND AMPLIFICATION.** With velocity noise only, median `|Δa0_pt|/a0` must equal
`4(1+y)·fv` within **5%** — the numerical confirmation that `a0` errors go as `~2×` the fractional
`g_obs` error, not half of it. On failure: HARD HALT.

---

## S5. THE BIAS METRIC AND THE DECISION RULE — FROZEN, NUMERIC

**Bias metric:** `b(est, a0_inj) = median over realizations of (a_hat / a0_inj) − 1`, in percentage
points.
**Scatter metric:** `s(est, a0_inj) = 0.5·(P84 − P16)` of `a_hat/a0_inj`, in percent;
`s(est) = ` arithmetic mean of `s` over the three injections.

> **G1 (prerequisite).** V1 zero-noise null PASSES for that estimator.
>
> **G2 (bias gate).** An estimator **PASSES** iff `|b(est, a0_inj)| < 2.0 percentage points` at
> **ALL THREE** injected a0 values.
>
> **G3 (injection independence).** An estimator PASSES iff
> `max_inj b(est) − min_inj b(est) < 2.0 percentage points`. An estimator unbiased at only one
> injected value is DISQUALIFIED from primary status and must be reported as a red flag.
>
> **G4 (efficiency).** Among estimators passing G1+G2+G3, an estimator is ELIGIBLE-AS-PRIMARY iff
> `s(est) <= 1.30 × min(s)` over that surviving set.
>
> **Tiers (reported for every estimator):** `PASS` = `max_inj |b| < 2.0 pp`;
> `MARGINAL` = `2.0 pp <= max_inj |b| < 5.0 pp`; `FAIL` = `max_inj |b| >= 5.0 pp`.
>
> **Primary selection.** Among G1+G2+G3+G4 survivors: smallest RMS bias over the three injections.
> If two are within `0.25 pp` RMS, the smaller `s(est)` wins. If still within 2% relative in `s`,
> the FROZEN PRIORITY ORDER decides: `gls_origin`, `median_a0pt`, `theilsen_pairwise`,
> `trimmed_mean_a0pt`, `ivw_median_a0pt`, `galaxy_median_then_median`, `galaxy_gls_then_median`,
> `log_median_a0pt`, `gls_lowy`.
>
> **Residual estimator systematic.** On the real data,
> `sysEst_new := (max − min)/2` over **ALL** G1+G2+G3 survivors (deliberately the wider set, not
> just the G4 set).

**Why X = 2.0 pp (pass) and 5.0 pp (fail).** The Step-A target for 3σ separation of canonical from
the `1.13–1.20e-10` cluster is a **6.31%** 1σ box (`reach_target.py`). (a) A 2.0% bias added in
quadrature to a 6.31% box inflates it by `sqrt(1+(2/6.31)²) − 1 ≈ 5%` — negligible, so a
G2-passing estimator cannot corrupt the measurement it is being chosen for. (b) 2.0% is **less
than one tenth** of the 21% footing gap and of the 22% estimator spread, so a G2-passing estimator
**cannot by itself decide which footing the data prefer** — which is precisely the property
required for the choice to be honest. (c) It is comfortably resolvable: at an expected
per-realization scatter of order 16%, `sigma_MC ≈ 1.2533·16%/sqrt(2000) ≈ 0.45 pp`, so a 2.0 pp
threshold is a `~4.5 sigma_MC` decision. Conversely **5.0 pp** is disqualifying because it is ~80%
of the entire 6.31% target box and ~1/4 of the footing gap: such an estimator would dominate its
own error budget and could shift a footing verdict by `~0.8σ` on its own.

**Why the G3 spread threshold is also 2.0 pp.** An estimator whose bias depends on the injected
truth by more than the pass tolerance is partially *encoding the assumed answer* — exactly the
circularity this study exists to eliminate. Using the same 2.0 pp number keeps the rule with one
free scale rather than two.

**Why Y = 1.30.** Among unbiased estimators, only efficiency remains. A 30% inflation of the
noise-driven term is immaterial to the real box, which is systematics-owned (the committed
`stat` line is a few percent, while Υ+gas-cal is ~11%); a factor worse than 1.30 signals real
inefficiency worth rejecting rather than a harmless robustness cost. `s` must also be finite and
stable (no divergence, no dependence on a tuning knob).

**Outcome map (all outcomes acceptable; outcome (a) is NOT to be forced).**

- **(a) exactly one estimator survives G2+G3** → the estimator-choice variance term collapses to
  its bias bound; recompute the box and state which footing the survivor's real-data value implies
  — **only after** the verdict file is written and hashed (§S7).
- **(b) several survive G2+G3** → if `sysEst_new/a0 > 5%`, the 22% spread is **REAL DATA
  STRUCTURE**: the ambiguity **STANDS** and the Step-A **NO-GO HOLDS**. If `sysEst_new/a0 <= 2%`
  the ambiguity is resolved to within the bias gate. Between 2% and 5%: **PARTIAL** shrink —
  report the new box and re-evaluate NO-GO status against the 6.31% target.
- **(c) all FAIL or MARGINAL** → report that a third estimator is needed. Any new estimator
  requires an **appended amendment** (`PREREG_AMENDMENT_<n>.md`, its own hash, and a statement of
  what was already known at the time) **before** its real-data value is computed.
- **(d) V1 fails** → no verdict at all; fix the machinery and rerun.

**FORBIDDEN after any bias number is seen:**
adding, removing, or redefining an estimator; changing `X = 2.0/5.0 pp`, `Y = 1.30`, `N_real`, the
seed, or the injected values; selecting among survivors using their real-data `a0` values or the
footing those imply; using the **sign** or **direction** of a measured bias in any gate; reporting
a footing implication before the verdict JSON is written and hashed.

---

## S6. WHY THE MANUFACTURED-WIN RISK IS SEVERE HERE, AND HOW IT IS BLOCKED

Choosing the estimator that happens to favour the canonical footing would be **fraud**. The
symmetric failure — choosing the one that favours ALT to look tough — is equally penalized. Three
structural blocks, all frozen above:

1. **Injection symmetry.** Mocks at canonical AND ALT AND standard-MOND; a passing estimator must
   pass at all three (G2) with an injection-independent bias (G3). No footing can be privileged by
   the gate.
2. **Sign blindness.** Every gate uses `|b|` only. The rule literally cannot see whether an
   estimator biases *up* (toward ALT) or *down* (toward canonical).
3. **Magnitude ceiling.** `2.0 pp` is `< 1/10` of the footing gap, so no G2-passing estimator can
   move the answer across the gap. The estimator choice is thereby made *incapable* of deciding
   the footing question by itself; only the data can.

---

## S7. FOOTING-BLINDNESS PROTOCOL

The bias verdict — per-estimator tier, G2/G3/G4 flags, the eligible set, and the primary estimator
— **MUST** be written to `estimator_bias_verdict.json` and hashed **BEFORE** any real-data
estimator value beyond the two already-committed ones is computed or reported.

**Acknowledged leak, handled honestly rather than pretended away.** The two incumbent real-data
values are already public in the committed Step-A artifacts: `gls_origin = 1.181e-10` (≈ ALT) and
`median_a0pt = 9.726e-11` (≈ canonical). They cannot be un-known. The leak is neutralized
*structurally* by S6.1–S6.3, not by a claim of ignorance.

**Counterfactual audit (mandatory output).** The results must print the FULL bias table
(9 estimators × 3 injections, with `s` and `sigma_MC`) so an adversary can re-apply the frozen rule
independently and confirm it would equally have selected an ALT-side estimator had the numbers come
out the other way.

**Posited clause (mandatory in the write-up).** Whichever estimator wins, `a0`'s VALUE remains
**POSITED** in the framework: this study resolves a MEASUREMENT ambiguity, not the theory's free
coefficient. Both footings carried on every dimensional number. No "theory closed", no TOE claim,
no "no open doors".

---

## S8. VERIFY THE FREEZE

```
cd /Users/carlzimmerman/new_physics/zimmerman-formula/prep_2026/a0_line
shasum -a 256 PREREG_ESTIMATOR_BIAS.md prereg_estimator_bias_config.json prereg_freeze.py
diff <(cat PREREG_ESTIMATOR_BIAS.sha256) -   # compare against the frozen digests
python3 prereg_freeze.py                     # regenerates the config byte-for-byte
```

`prereg_freeze.py` computes no `a0` estimate, runs no estimator, and generates no mock: it is
deliberately incapable of producing a result that could bias the frozen criterion. The frozen files
are **append-only**; any change requires a new `PREREG_AMENDMENT_<n>.md` with its own hash, and the
original digests must remain verifiable.
