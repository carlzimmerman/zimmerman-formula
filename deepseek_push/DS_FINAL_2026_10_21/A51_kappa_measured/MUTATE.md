# A51 — mutations

Five mutations, each a plausible way to get a wrong κ with a confident error bar. Each is
selected by `python3 a51_checks.py --mutate NAME`, writes `a51_MUTATE_<name>.out` and
`a51_results_MUTATE_<name>.json`, prints `n/17 checks pass`, and **exits 1**. The baseline
(`python3 a51_checks.py`) exits 0 with 17/17.

| id | what it changes | checks that fail | the wrong number it produces |
|---|---|---|---|
| `kappa_de` | `kappa_P3()` is replaced by the `ρ_DE` convention, silently | **K3** | κ = 0.604254 for a0 = 1.1312e-10, called "κ = ½" |
| `fixed_ups` | the fixed-`Υ` error bar is accepted as the total | **K12** | σ(κ) = 0.0028 (0.67%) while the IMF moves κ ×0.44 |
| `dchi2_only` | Δχ² = 1 is taken as the total error | **K10** | κ = 0.371 ± 0.0042 → ½ "excluded at 30.9σ" |
| `coherent_scales` | every systematic is treated as statistical (scales as 1/√N) | **K10, K14** | σ(κ) = 0.0265 → ½ at 4.9σ; "N = 1000 reaches 3σ" |
| `cluster_direct` | `R_req` is read as a direct a0 measurement, `u`'s 6.7% dropped | **K7** | σ(a0)/a0 = 8.3% from clusters, κ = 0.393 ± 0.033 |

---

## M1 `kappa_de` — the 20.9% relabelling

**The slip.** The record quotes κ two ways: per `ρ_bare = ρ_DE/Ω_Λ = ρ_crit` (P3, THEORY §3.6)
and per `ρ_DE` (A9 D2, A14, `kappa_closure`). They differ by `√Ω_Λ = 0.8276`. The mutation uses
the second and still calls it the theory's κ.

**Effect.** `kappa_P3 = 0.604254` (the true value is 0.500000), `kappa_DE = 0.730247`, and the
a0 → κ → a0 round trip fails at **0.21** instead of 0. The theory's target is then read as
0.604, i.e. a0 = 1.367e-10 — 21% high, with no measurement in it.

**Why it matters.** Four of the seven κ values in the record are in the `ρ_DE` convention
(K16). Reading them as P3 inflates them by 21%, which is most of the apparent 0.29–0.49 span.
This is the single most likely way to "measure" κ wrongly while every number looks reasonable.

**Result:** 16/17, exit 1. `K3 FAIL kappa_P3=0.604254 kappa_DE=0.730247 round-trip 2.1e-01`.

---

## M2 `fixed_ups` — the prior-domination trap

**The slip.** Fit with a single `Υ = 0.5` (the zero-parameter version), get
χ²/dof = 6.63 and σ(a0)/a0 = 0.67% from Δχ² = 1, and report that as the κ error bar.

**Effect.** κ = 0.4174 ± 0.0028 (0.67%). The number is even *close* to A19's 0.417 ± 0.095,
which makes the mistake look like a confirmation. But the same fit with `Υ = 0.87`
(Salpeter) gives κ = 0.1832 — a **×0.439** swing from the IMF alone, 60× the quoted error
bar. The 0.67% is measuring the prior, not the data.

**Why it matters.** This is exactly the trap A9's `κ ∝ Υ^-1.23` describes. The lane's finding
is that it is escaped only by freeing `Υ` per galaxy, which costs a factor 14 in the error bar
(0.67% → 9.4%) and cuts the IMF leverage to ×1.05.

**Result:** 16/17, exit 1.
`K12 FAIL ratio 14.1, IMF move x0.439` — the mutant's claim (ratio > 10 **and** the IMF moves
κ by < 5%) is refuted by the ×0.439 it actually produces.

---

## M3 `dchi2_only` — believing the formal errors

**The slip.** χ²/dof = 2.22 means the per-point errors are not the truth, but the mutation
takes the Δχ² = 1 interval as the total uncertainty.

**Effect.** σ(κ) = 0.0042 (1.13% in a0, 0.40% in κ). Then
`(0.5 − 0.3708)/0.0042 = 30.9σ` — "κ = ½ is excluded at 31σ". The bootstrap says 9.4%
(8.3× larger); the estimator ensemble spans 21% (50× larger).

**Why it matters.** 0.40% in κ is the number that would be quoted if the lane were careless,
and it is the one number in this analysis that is *certainly* wrong: the per-galaxy a0 scatter
is 0.455 dex, so 0.455/√171 = 8.3% is the floor on the statistical error. A 0.4% claim would
require the galaxies to be 20× more consistent than they are.

**Result:** 16/17, exit 1.
`K10 FAIL kappa = 0.3708 +- 0.0042 (tot) ; 1/2 at 30.91 sigma`.

---

## M4 `coherent_scales` — the floor that does not shrink

**The slip.** Treat every declared systematic as if it were statistical, i.e. as if it scaled
as 1/√N. Then "N = 1000 decides it".

**Effect.** σ(κ) = 0.0265 → ½ at 4.9σ (already excluded at 2σ), and the forecast's coherent
floor `coh_k` becomes 0, so at N = 1000 the two gaps read 1.22σ and 0.15σ — the same as the
statistical-only numbers, and the report would have to say the floor is irrelevant.

**Why it matters.** The floor is the *answer* to task (4). It is 0.116 in κ (31%), made of
the estimator/error-model choice (21%), the distance zero point (16%), the `H₀` footing
(12.5%) and the law choice (10%). None of those is a counting error: a better distance zero
point needs a different survey, a smaller estimator spread needs a different likelihood (a
fitted intrinsic scatter), the `H₀` footing needs a background that is not an exact ΛCDM
relabelling, and the law choice needs a discriminator. `0.116 > 0.0176/3`, so **no N** reaches
3σ on 0.4824.

**Result:** 15/17, exit 1.
`K10 FAIL ... 1/2 at 4.88 sigma` and
`K14 FAIL ... with floor 1.22 / 0.15 sigma` (the check requires the floor to exceed gap/3).

---

## M5 `cluster_direct` — the circular cluster constraint

**The slip.** Read A18's `R_req = 5.552 ± 0.427` as a direct measurement of a0, holding the
sourcing fraction `u = 0.45` at its central value and dropping its 6.7% error.

**Effect.** σ(a0)/a0 = **8.3%** from clusters alone (κ = 0.3934 ± 0.0326), comparable to
SPARC's 9.4% and therefore apparently an independent confirmation.

**Why it matters.** It is not independent. `R_req` and `u` are both derived from the same
CFG687 MID/OUTER amplitudes; `u` was fitted by A18 *at* the canonical a0. The cluster
amplitude measures one number, `R_tot(a0)·u^{-1}`, and with `u` free the constraint on a0
vanishes. Marginalising `u` honestly gives 11.0%, and even that is generous because `u`'s
prior is not independent of the data. The channel is an 11–20% upper bound on a0's precision,
not a measurement.

**Result:** 16/17, exit 1.
`K7 FAIL sigma(a0)/a0 = 0.083 kappa_cl = 0.3934 +- 0.0326` (the check requires ≥ 10%).

---

## What the mutations jointly show

Every wrong answer in this lane comes from a *choice*, not from the data:

- the density convention (M1) moves κ by 21%;
- the stellar prior (M2) moves the error bar by 14× and κ by 2.3×;
- the error model (M3) moves the error bar by 8.3×;
- the N-scaling assumption (M4) flips the decidability verdict;
- the cluster marginalisation (M5) halves the cluster error.

The data themselves give κ = 0.3572 with a 9.4% bootstrap error and a 21% estimator spread.
Everything else is the analysis. That is why the lane's verdict is *κ = 0.371 ± 0.119, ½
admitted at 1.09σ and not decided*, and why it declines to quote the 0.40% formal error.
