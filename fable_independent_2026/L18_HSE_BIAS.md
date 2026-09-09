# L18 — the hydrostatic mass bias, propagated through L7 and L2

`L18_hse_bias.py` / `L18_hse_bias.out`. **6 FAIL of 10.** Both controls PASS.

This lane exists to attack the strongest result this lane produced tonight, using the one
systematic every number in it depends on. **The attack fails, and the failure is one-sided:**
the hydrostatic bias does not rescue the framework, it makes the adverse conclusion stronger,
and the *b* that would rescue it is on the **opposite side of zero** from everything measured.

---

## What the repository already knew (surveyed, not duplicated)

The bias treatment is not new here. Five places already carry it, and this lane extends them:

| where | what it already says |
|---|---|
| `closure_2026/cluster_measurement_audit_2026/results.json` | every row carries `HSE_multiplicative_factor_for_exact_match`, which **is** 1/(1−b) for the audit's exact exponential law. Its published 300 kpc values 0.282 / 0.264 / 0.307 are **b = −2.55 / −2.79 / −2.26**. |
| `.../CLUSTER_AUDIT.md` | proves the sign constraint directly: to remove the discrepancy the non-thermal pressure must *increase outward*, and "with zero nonthermal pressure at the outer endpoint the required inner nonthermal pressure is negative: that restricted proposed explanation is impossible." It also warns, correctly, that Eckert+2019's α = P_NT/P_tot is a pressure **fraction**, "not generally the hydrostatic mass bias". |
| `hunt_2026/u02_...py` block E2 | applies b = 0.10/0.20/0.30 to the X-ray ledger rows: "**WRONG SIGN**: it makes the X-ray liability WORSE". |
| `hunt_2026/u01_...py` PATTERN 3 | b = 0.20 moves the framework's two best cluster rows *toward* the weak-lensing rows. |
| `fable_independent_2026/L2_cluster_inverse.py` C8 | already prices the same escape in a physical variable: σ₁D = 857 km/s, 5.2× Hitomi. |

**One intra-repo contradiction found and settled.** `hunt_2026/u13_mass_efe_and_domain.py`
line 334 applies `B -= 0.5*log10(1.25)` for a 20% bias, and its C3 concludes a hydrostatic bias
"is real, **helps**, and is not the answer". `u02` line 565 applies the *same magnitude with the
opposite sign*. Check **H2** settles it from the profiles: the sign in u02/u01 is right and u13's
C3 is wrong. For the record the contradiction is confined to C3's prose — u13's C7 immediately
overwrites `B = 0.0` for every cluster row, so no published number of u13 moves.

## The literature values used

| b | source |
|---|---|
| 0.03 (median), 0.17 (80th pct) | **X-COP itself** — Ettori & Eckert 2022, A&A 657 L1 (arXiv:2112.07554) |
| 0.15 | X-COP gas-fraction SZ calibration 1−b = 0.85 ± 0.05, Eckert+2019 A&A 621 A40 |
| 0.20 (median), 0.33 (80th pct) | local cluster population, Ettori & Eckert 2022 |
| 0.20 | FLAMINGO at R500c, cluster scale, Kugel+2024 (arXiv:2409.07849) |
| 0.22 | CCCP weak lensing, 1−b = 0.78 ± 0.09, Hoekstra+2015 |
| 0.31 | Weighing the Giants, 1−b = 0.69 ± 0.07, von der Linden+2014 |
| 0.42 | Planck 2015 XXIV counts-vs-CMB, 1−b ≈ 0.58 — carried as an **upper envelope**, not a measurement of b |
| radial | Nelson, Lau & Nagai 2014 ApJ 792 25, P_nth/P_tot = 1 − A{1+exp[−(r/BR₂₀₀ₘ)^γ]}, A = 0.452, B = 0.841, γ = 1.628 |

**Adopted measured range b ∈ [0.00, 0.42]; X-COP's own sample b ∈ [0.03, 0.17].**

The Nelson fraction is **not** set equal to b (the audit's warning). It is converted through the
exact gradient relation M_true/M_HSE = 1 + k + (dk/dlnr)/(dlnP_th/dlnr), k = f/(1−f), giving
b(0.8 R500) = 0.12–0.17 for dlnP_th/dlnr = −2 to −4 — at the pessimistic end for this sample,
which is the direction adverse to this lane, which is why it is carried.

---

## The direction, worked out rather than assumed

M_HSE = (1−b)M_true. **g_bar does not move**: gas mass comes from the X-ray emission measure and
stellar mass from the stellar profile, neither of which uses the temperature *gradient*. So
s = g_bar/a₀ and M_kernel are untouched and only g_HSE moves, to g_HSE/(1−b). Hence the two exact
identities

    f_bar(b) = (1 − b) · f_bar(0)                          → f_bar goes DOWN, away from cosmic 0.156
    M_dark/M_bar(b) = [1 + M_dark/M_bar(0)]/(1 − b) − 1     → the ratio goes UP, above cosmic 5.43
    M_resid/M_bar(b) = [1 + M_dark/M_bar(0)]/(1 − b) − M_kernel/M_bar   → the framework's shortfall GROWS

**Verified numerically, not assumed** (H2): at the population median b = 0.20 the framework
residual moves 3.09 → **4.85** baryonic masses, the maximum required boost 2.94 → **3.80**, and
the fitted log-slope 0.811 → 0.818. All three move away from the framework.

## L7 under the bias (1000 kpc = 0.80 R500, twelve X-COP clusters, canonical footing)

| b | f_bar | retained | M_dark/M_bar | scatter | M_resid/M_bar | σ from 0 |
|---|---|---|---|---|---|---|
| 0.00 | 0.149 | 96% | 5.73 | 12% | 3.09 | 15.1 |
| 0.03 (X-COP median) | 0.144 | 93% | 5.94 | 12% | 3.31 | 15.8 |
| 0.17 (X-COP 80th) | 0.123 | 79% | 7.11 | 12% | 4.53 | 18.9 |
| 0.20 (population) | 0.119 | 76% | 7.41 | 11% | 4.85 | 19.6 |
| 0.31 (WtG) | 0.103 | 66% | 8.75 | 11% | 6.19 | 21.9 |
| 0.42 (Planck envelope) | 0.086 | 55% | 10.60 | 11% | 8.01 | 24.1 |

Radial models at 0.80 R500 give b = 0.12–0.24 and land between the b = 0.15 and b = 0.31 rows.
Note the X-COP-anchored radial law makes b **smaller** at L7's radius than at R500 (0.75 b₅₀₀),
which is the direction adverse to this lane and is carried anyway.

## L2 under the bias (canonical, stellar-7)

| b | A | p | max Δ_req | cluster/galaxy ratio by bin | worst \|z\| |
|---|---|---|---|---|---|
| 0.00 | 5.47 | 0.811 | 2.94 | 2.2 3.3 4.3 4.3 4.4 5.1 | 11.8 |
| 0.20 | 7.09 | 0.818 | 3.80 | 2.9 4.3 5.5 5.6 5.7 6.5 | 13.1 |
| 0.31 | 8.39 | 0.821 | 4.48 | 3.4 5.0 6.5 6.5 6.7 7.7 | 14.7 |
| 0.42 | 10.18 | 0.824 | 5.41 | 4.1 6.1 7.8 7.9 8.1 9.3 | 15.2 |

The 2.2–5.1× discrepancy becomes **2.9–6.5×** at the population median and **4.1–9.3×** at the
Planck envelope. The slope p moves *towards* 1 — towards "constant rescaling of G, i.e. extra mass
tracing the baryons" — and further from the 1/2 that caps any kernel with a deep-MOND limit.

---

## The key question: the b that would rescue the framework

| what it would rescue | required b |
|---|---|
| L7's residual to zero at 0.80 R500 | **−0.82** (canonical), **−0.68** (alt); per cluster −1.25 to −0.52, all twelve negative |
| L2's cluster/galaxy overlap to agreement | **−2.07** (bins −2.21 to −0.95; identical at both footings, since a₀ cancels from a ratio of measured accelerations) |
| L2's slope down to the class ceiling p = 1/2 | −6.8 (order of magnitude only — a third of the rows go unphysical; the usable statement is dp/db > 0, so no positive b can ever do it) |
| the lead's own audit, exact exponential law, 300 kpc | −2.55 / −2.79 / −2.26 |

**Measured: b ∈ [+0.00, +0.42]; X-COP's own [+0.03, +0.17]; single-cluster empirical floor ≈ −0.20.**

The required value is **negative** and every measured value is **positive**. They are not merely
different in size — they are on opposite sides of zero, so no tightening of the measured range can
reach it. In magnitude the requirement is 2.0× (L7) to 4.9× (L2) the largest number in the whole
measured range, and 5–12× X-COP's own.

**And the required b is not a physical quantity at all.** A bias b > 0 is non-thermal support:
σ² = [b/(1−b)]·g_HSE·r/α_g with ρ_g ∝ r^−α_g. A negative b needs **σ² < 0 in 12 of 12 clusters**.
Written without turbulence it is the demand that the measured thermal pressure gradient be
*over*-stated by a factor 1.82 — the exact branch the lead's CLUSTER_AUDIT.md already proves
impossible with a non-negative outer boundary pressure. Sanity check on the conversion: the
*allowed* b = 0.20 corresponds to σ₁D = 559 km/s, i.e. f_nth = 25% at kT = 6 keV, against
Nelson+2014's simulated 21% at this radius — so b = 0.20 and the simulated turbulence are the same
statement, and that correction hurts the framework.

---

## PASS/FAIL

```
  [PASS] H0 [CONTROL] at b = 0 this pipeline reproduces L7's published numbers (f_bar = 0.149, Newtonian ratio 5.73, 12% scatter)   (f_bar = 0.149 [0.115, 0.160], ratio_N = 5.73 +/- 0.68 (12% scatter), ratio_F = 3.09 (15 sigma from 0); alt footing ratio_N = 5.73)
  [PASS] H1 [CONTROL] at b = 0 it also reproduces L2's published numbers (Delta_req = 5.47 s^0.811 and cluster/galaxy ratios 2.2-5.1)   (A = 5.47 (L2: 5.47), p = 0.811 (L2: 0.811), rms 0.094 dex (L2: 0.094), ratios 2.2-5.1 (L2: 2.2-5.1))
  [FAIL] H2 [DIRECTION] correcting the masses for the MEASURED (positive) hydrostatic bias REDUCES the framework's required residual   (at b = 0.20 the framework residual moves 3.09 -> 4.85 M_bar (+1.76), the maximum required boost 2.94 -> 3.80 (+0.85) and the slope 0.811 -> 0.818 (+0.006): ALL THREE MOVE AWAY FROM THE FRAMEWORK.  u02's E2 sign is right and u13's C3 line 334 sign is wrong)
  [FAIL] H3 [KEY, L7] there is a b inside the measured range [0.00, 0.42] that brings the framework's residual at 0.80 R500 to zero   (required b = -0.819 (canonical) / -0.681 (alt); every one of the twelve clusters needs a negative b (-1.25 to -0.52); the measured range is [+0.00, +0.42] and X-COP's own is [+0.03, +0.17] -- the required value is on the OPPOSITE SIDE OF ZERO, 8.5 single-cluster scatters (taking sigma_b = 0.10) below the X-COP median)
  [FAIL] H4 [KEY, L2] there is a b inside the measured range that brings the cluster boost down to the measured galaxy boost at the same acceleration   (required b by bin (canonical/stellar-7): -0.95, -1.64, -2.10, -2.16, -2.03, -2.11; median -2.07, over all footings and subsets -2.21 to -0.95; measured [+0.00, +0.42])
  [FAIL] H5 [L2 slope] there is a b inside the measured range for which the required Delta_req acquires the log-slope of a kernel of the class, p <= 1/2   (b(p = 1/2) = -6.793; a POSITIVE b moves p the wrong way, 0.811 -> 0.818 at b = 0.20 and 0.824 at b = 0.42, i.e. towards the p = 1 'constant rescaling of G' end)
  [FAIL] H6 [L7 cosmic] L7's cosmic-ratio agreement survives the measured bias range: across 0 <= b <= 0.33 the Newtonian M_dark/M_bar stays inside R1's depletion-allowed 5.4-8.0   (ratio_N runs 5.73 to 9.04 over b in [0, 0.33] (R1 band 5.43-7.76); it leaves the band above b = 0.23, so R1 as WRITTEN survives X-COP's own b <= 0.17 and the population median 0.20 but not the population 80th percentile 0.33.  What is leaving is R1's 30% DEPLETION ALLOWANCE, not the cosmic reading: f_bar falls 0.149 -> 0.100, i.e. baryon retention 96% -> 64%)
  [PASS] H7 [CROSS] this script's required-b solve reproduces the lead's own HSE_multiplicative_factor_for_exact_match on the lead's exact exponential law   (independent re-solve of all 248 stored rows agrees to 2.50e-15 relative; converted, the audit's published 300 kpc factors 0.282/0.264/0.307 are b = -2.55/-2.79/-2.26)
  [FAIL] H8 [PHYSICAL] the required b is physically available: it is a non-thermal support with the right sign (P_nt >= 0, increasing outward) and sigma_1D at most 2x Hitomi's 164 km/s   (the required b is negative in 12 of 12 clusters, so sigma^2 < 0 -- it is not turbulence but a demand that the measured thermal pressure gradient be OVER-stated by a factor 1.82; even the ALLOWED b = 0.20 already needs sigma_1D = 559 km/s = 3.4x Hitomi (f_nth = 25% at kT = 6 keV, matching Nelson+2014's 21%), and that correction hurts the framework rather than helping it)
  [PASS] H9 [SCATTER] the 12% cluster-to-cluster universality of the Newtonian ratio (L7's R2) survives the bias correction across the measured range   (fractional scatter runs 11%-12% over b in [0, 0.42], both footings (a constant b cannot change the ordering, and it slightly TIGHTENS the fractional scatter because the ratio grows))
```

---

## The one correction this lane owes L7

**H6 is a genuine, if partial, hit on my own result, and it is reported as such.** L7's headline
was stated as "f_bar = 0.149 against cosmic 0.156" and "5.73 against cosmic 5.43, a 5% agreement".
That closeness at b = 0 is **partly an artefact of ignoring the bias** and should not be quoted as
a 5% agreement any more. At X-COP's own b ≤ 0.17 the ratio is 7.11 and at the population median it
is 7.41 — both still inside L7's R1 band 5.4–8.0 — but at b = 0.33 it is 9.04, and R1 *as literally
written* fails above **b = 0.23**.

What is leaving the band is R1's own **30% depletion allowance**, not the cosmic reading. At b = 0
the clusters retain 96% of the cosmic baryon share at 0.80 R500, the very top of that window;
b = 0.20 puts them at 76%, its middle. Read as physics the bias makes the cosmic-share reading
**more** self-consistent, not less. What the bias cannot touch at all is the **universality**
(11–12% across the whole range, H9) and the fact that the required ratio is of order the cosmic one
for every one of the twelve — which is L7's actual argument.

## Verdict

**L2 is robust and strengthened.** Every value of b in the measured range makes its impossibility
worse — larger amplitude, larger cluster/galaxy discrepancy, a slope pushed further from the
kernel-class ceiling — and the b that would close it is −2.07, of the wrong sign and five times the
magnitude of anything measured. **L7's conclusion survives, but one of its numbers needs a caveat:**
the qualitative result (clusters need close to the cosmic dark share, universally, and the
framework's residual is 13–15σ from the zero it predicts) holds across the whole measured range and
gets stronger, while the exact 5.73-vs-5.43 coincidence is bias-dependent and should be dropped as
a headline. **The hydrostatic bias is not an escape**: the required correction is not merely outside
the measured range but on the other side of zero, and it is not non-thermal support at all —
σ² < 0 in twelve of twelve clusters, the branch the lead's own audit already proved impossible.

**Limits, stated.** b is applied as a multiplicative correction to the tabulated g_HSE, not as a
refit of the X-ray spectra, and it does not carry the covariance of the temperature reconstruction.
A per-cluster b drawn from the measured scatter could put *one* system near b = −0.2; the solve
needs −0.82 in *all twelve* simultaneously. Nothing here tests a bias in the **baryon census**,
which is a different systematic and the door the lead's audit deliberately left open ("an
additional, as-yet-unidentified baryonic component").
