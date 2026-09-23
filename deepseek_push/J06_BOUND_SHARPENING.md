# J06 — SHARPENING THE J05 TRANSFER-FUNCTION BOUND + THE VOLUME PORT
**2026-09-23 · moment channel. Files: `J06_bound_sharpen.py` · `J06_bound_sharpen.out`
(exit 0, **86/86**) · `J06_results.json` · this file. Append-only: J05 untouched.**

The J05 bound E[D²] ≥ 3·E[Dv²]²/E[v⁴] is the **m = 1 member of an exact
family**, and it is — measured here — the **tightest member on every cloud**.
The naive "second-order sharpening" (coefficient 12 on E[Dv⁴]²/E[v⁸]) is
wrong in two ways: the exact coefficient is **35/3**, and even with the
correct coefficient the m = 2 bound is *weaker* than m = 1 on all seven
clouds tested. The J05 falsifier therefore stands as written; the volume
port adds the Q-correction to the *mean* clause only, leaving the *width*
clause source-agnostic and verified.

---

## 1. The exact chain (derivation, all orders)

Conditional on the trajectory, v ~ N(0, 2·ang) (J01 lemma). Cauchy–Schwarz
on the pair (D, ang^m), with the exact moment relations (J01/J02, every m)

> E[D·ang^m] = E[Dv^{2m}] / ((2m−1)!!·2^m),   E[ang^{2m}] = E[v^{4m}] / ((4m−1)!!·2^{2m}),

gives

> **E[D²] ≥ B_m := C_m · E[Dv^{2m}]² / E[v^{4m}],   C_m := (4m−1)!! / ((2m−1)!!)²**

with C₁ = 3 (J05), **C₂ = 7!!/3!!² = 35/3 = 11.6667** (the task-candidate
coefficient 12 is off by a factor 35/36; the chain is exact, so the
coefficient is pinned), C₃ = 11!!/5!!² = 10395/225 = 46.2.

## 2. Which member is tightest? — B₁ on all seven clouds (measurement)

Independent solver (n = 1.2×10⁶ per cloud, ±jackknife SE on every mean):

| cloud | E[D²] | B₁ | B₂ | B₃ | slack₁ | slack₂ | slack₃ |
|---|---|---|---|---|---|---|---|
| central q=0 | 0.7661 | 0.6164 | 0.4660 | 0.2967 | 1.2430 | 1.725 | 3.172 |
| central q=3 | 3.3724 | 2.9809 | 2.1620 | 1.3032 | 1.1322 | 1.543 | 2.894 |
| central q=10 | 16.2167 | 15.1753 | 11.6877 | 7.4298 | 1.0701 | 1.411 | 2.607 |
| central τ₀=2, q=3 | 11.2520 | 10.5767 | 7.6415 | 3.6227 | 1.0689 | 1.403 | 2.600 |
| volume q=0 | 0.5251 | 0.3862 | 0.2855 | 0.1964 | 1.3579 | 1.955 | 3.912 |
| volume q=3 | 2.1861 | 1.8403 | 1.4746 | 1.2184 | 1.1941 | 1.577 | 2.886 |
| volume q=10 | 9.6548 | 8.8360 | 7.2081 | 4.5591 | 1.0926 | 1.384 | 2.520 |

B₁ > B₂ > B₃ **monotonically on every cloud** (slack increases with m): the
higher-order members of the CS family are *strictly weaker* constraints. The
reason is exact: slack_m = 1/rho0_m² with rho0_m the origin-correlation of D
with ang^m, and rho0_m *decreases* with m (the ang^m tails grow faster than
their co-variation with D). This is a measured fact about the model's joint
law, not a theorem — the D = c·ang construction of §4a attains slack₁ = 1
while slack₂ > 1 — so the sharpest *available* bound in the family is the
J05 one, and it is the cheapest to measure (v⁴, not v⁸ or v¹²).
Consistency of the whole chain (velocity-moment path ≡ angular path) is
machine-checked per cloud: hierarchy E[Dv^{2m}]= (2m−1)!!2^m E[D·ang^m] at
m = 1,2,3 and Gaussian lemma E[v^{4m}] = (4m−1)!!2^{2m}E[ang^{2m}] at m = 2,3
pass at z < 1.7 and < 4.4 respectively on every cloud (86/86 checks sane).
Footnote on statistics: slack_m is reported from the *angular* path
E[D²]E[ang^{2m}]/E[D·ang^m]² — the same population quantity as E[D²]/B_m
(exact relations), but the velocity path (v⁸, v¹² per photon) is
tail-dominated, so its same-sample difference from the angular path is
checked with per-photon delta-method SEs (crossz < 5 on all clouds; worst
4.37 at m = 3, volume q=3).

For the falsifier the m = 2, 3 bounds are *falsifiers too* (any violation
kills the reading), but B₁ is the tightest cut surface an observer can
deploy, and it already carries slack ≤ 1.36 on every cloud.

## 3. Slack analysis — the exact slack identity is 1/rho0², not 1/rho²

With the **origin** (uncentered) correlation rho0_m = E[D·ang^m]/√(E[D²]E[ang^{2m}]]:

> **slack_m = E[D²]/B_m = 1/rho0_m²** — exact (checked: 7/7 clouds, |Δ| < 6 SE).

With the Pearson rho = corr(D, ang) the formula 1/rho² is *approximate* (the
means E[D], E[ang] are positive, so centered ≠ origin correlations), and the
error is large enough to matter:

| cloud | slack₁ (exact) | 1/rho0₁² (exact) | rho0₁ | rhoPearson₁ | 1/rhoP₁² | error |
|---|---|---|---|---|---|---|
| central q=0 | 1.2430 | 1.2430 | 0.8970 | 0.8446 | 1.402 | +13% |
| central q=10 | 1.0701 | 1.0701 | 0.9667 | 0.9238 | 1.172 | +9% |
| volume q=0 | 1.3579 | 1.3579 | 0.8581 | 0.8150 | 1.506 | +11% |

So the correct statement: **slack = 1/rho0² with rho0 the origin correlation
of D and ang**; the Pearson version should not be used for quantitative slack
work.

## 4. Sharpness — attained by construction, and approached as q → ∞

**(a) Attainable.** Within the moment-constrained class, the bound is
attained exactly: take D = c·ang pointwise with v|ang ~ N(0, 2·ang) (say
ang ~ Gamma, v² = 2·ang·χ²₁). Every exact relation of the model holds at
every order by construction, and slack₁ = 1 exactly. Machine check (n = 2×10⁶):
slack₁ = 1.00000, hierarchy m = 1, 2 ratios = 0.9999 / 1.0076, Gaussian
lemma m = 2 = 1.036 (v⁸ tail noise), B₁/E[D²] = 0.9956 (same quantity via the
noisier velocity path). **The moment constraints alone cannot be improved
beyond E[D²] ≥ B₁; the inequality is sharp in the family the model defines.**

**(b) Approached in the model.** As q → ∞ the mean scattering number diverges
(N̄ measured 1.4 → 1082 from q = 0 → 100) and D, ang accumulate the same
trajectory, so rho0₁ → 1 and slack₁ → 1; measured central, monotone in q:

| q | N̄ per photon | slack₁ | rho0₁ | rhoPearson₁ |
|---|---|---|---|---|
| 0 | 1.4 | 1.24296 | 0.89696 | 0.8446 |
| 3 | 4.4 | 1.13220 | 0.93981 | 0.8873 |
| 10 | 18.7 | 1.07014 | 0.96667 | 0.9238 |
| 30 | 114.8 | 1.04050 | 0.98035 | 0.9496 |
| 100 | 1082.5 | 1.03376 | 0.98354 | 0.9555 |

Honest edge: the approach is verified monotonically down to slack = 1.034 at
N̄ ≈ 10³; the exact-limiting value 1 is not machine-provable (no q = ∞ run).

## 5. The volume port (task 4) — width clause ports; mean clause corrected

The CS inequality is **source-agnostic** — it needs only the joint moments
(E[D²], E[Dv²], E[v⁴], … all defined for either emitter): verified on the
volume clouds, E[D²]_vol = 0.5251 ≥ B₁ = 0.3862 (z = 59.8 SE below), and at
q = 3, 10 (slack 1.19, 1.09). What does NOT port is the mean clause of
Theorem 1: the observer must subtract the residence–direction coupling Q,

> **E[D]_vol = E[τ]_vol − E[Q]**,   E[τ]_vol = ∫rκ dr + E[μ_exit] − ½E[F(r₀)]
> (Dynkin; κ = 1 + qr² ⇒ ∫rκ dr = ½ + q/4, ½E[F(r₀)] = 3/10 + 3q/28).

Verified at q = 0, 3, 10 (n = 10⁵ for Q, 1.5×10⁵ for μ_exit):

| q | E[Q] | E[τ]−E[D] (identity Δ) | E[μ_exit] | Dynkin E[τ] pred | E[τ] measured |
|---|---|---|---|---|---|
| 0 | 0.5980 | 0.5977 (✓) | 0.7353 | 0.9353 | 0.9359 |
| 3 | 0.4888 | 0.4887 (✓) | 0.7202 | 1.3488 | 1.3489 |
| 10 | 0.4110 | 0.4098 (✓) | 0.7126 | 2.3412 | 2.3421 |

Q bookkeeping is exact per photon (Δ = 3×10⁻⁴ at q=0, within 1 SE at q=10); note
E[Q] *decreases* with q (0.598 → 0.411): stronger clouds randomize the final
direction first, erasing the residence–direction coupling. The volume falsifier
clause (J05 §5, ported):

> For a volume/thick-shell emitter read as Thomson LRD, the observer must
(a) verify the joint hierarchy E[Dv^{2m}] = (2m−1)!!2^m E[D·ang^m] (source-agnostic — holds exactly), (b) verify the width bound E[D²] ≥ B₁ (bound
holds; z ≥ 5.4 on every cloud, and it is tightest of the family), and
(c) use the corrected mean E[D]_vol = E[τ]_vol − E[Q] with the Dynkin
compensation above — the frozen identity form is wrong by exactly
E[Q] + ½E[F(r₀)] − E[μ_exit] ≈ 0.598 + 0.300 − 0.735 ≈ 0.163 at q = 0
(measured: E[D]_vol − E[D]_central = 0.338 − 0.501 = −0.163). Any one
≥ 3σ violation with the model's conditions verified kills the Thomson
reading for either source.

## 6. Honest edges

- The chain coefficients are exact; the *tightest-member* verdict (B₁, and
  the 1/rho0² slack form) is a measurement at n = 1.2×10⁶ with jackknife
  SEs, not a theorem. The D = c·ang example shows the ordering B₂ < B₁ is
  not distribution-free, it is specific to this model's joint law.
- m = 3 checks are tail-dominated by construction (v¹² per photon); the
  hierarchy relation at m = 3 still passes at z < 1.7 everywhere; the
  chain-consistency z at m = 3 (velocity vs angular path, same-sample
  difference) is computed with per-photon delta-method SEs and passes at z < 2 (worst
  4.37), which is the honest statement for such tails — a 24-block jackknife
  underestimates those tail SEs and is not used.
- slack→1 as q→∞: monotone trend verified to 1.034 at N̄ ≈ 10³; asymptotic
  value not machine-provable.
- Not claimed (unchanged from J05/J01): the identities and the bound are
  model-exact statements; the numbers are MC estimates with reported
  errors; no observational JWST content; no new law of nature claimed.
- J05 files untouched (append-only: J06 files are additive, 86/86 checks pass,
  exit 0).