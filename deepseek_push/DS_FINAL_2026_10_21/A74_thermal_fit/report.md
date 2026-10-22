# A74 — THE DECISIVE FIT: what fixing a0 at the thermal value costs

**Lane:** A74_thermal_fit · **Date:** 2026-10-22 · **Base:** `deepseek_push/DS_FINAL_2026_10_21`
**Script:** `a74_checks.py` — **29/29 PASS, exit 0, 27 s** · **Output:** `a74.out` · **Data:** `a74_results.json`
**Mutations:** 20, each one input, each **exit 1**, **29/29 checks killed** (`MUTATE.md`, `a74_MUTATE_*.out`)
**Read:** `A71_global_fit` (the likelihood: SPARC 171/3375, corrected SLACS 70 lenses, A18 clusters, shared
κ/B/u, one Υ per galaxy), `A72_coefficient` (the thermal derivation), `A70_slacs_audit` (the SLACS model
and Treu's IMF prior). **No new data. Nothing committed.**

**The three numbers.**

```
(a) a0 FREE          kappa_P3 = 0.377651 +- 0.025787 (stat) +- 0.117904 (syst)   chi2 = 5.686091  (A71: 0.377651, 5.686091)
(b) a0 = 8.620e-11   kappa_P3 = 0.381010                                        chi2 = 5.703008   Delta = +0.016917
(c) a0 = 9.354e-11   kappa_P3 = 0.413453                                        chi2 = 7.566877   Delta = +1.880786

Delta-chi2 (c) - (b) = +1.863869  ->  1.365 sigma (1 dof)  ->  LR thermal : kappa=1/2 = 2.5394 : 1
```

---

## 0. Bottom line

1. **Fixing a0 at the thermal value costs Δχ² = 0.016917 — nothing.** The free fit already sits **0.1301σ**
   from it. A theory that declares a0 = cH_Λ/2π and fits nothing else loses 0.017 units of χ² over three
   channels and 174 parameters.
2. **Fixing it at κ = ½ costs Δχ² = 1.880786 (1.3714σ).** That is the whole price of the rival, and it is
   not a rejection either. **Neither point is excluded by any channel.**
3. **The decisive number is Δχ² = 1.8639 → 1.365σ → LR 2.54 : 1 for the thermal point.** A72's 2.6 : 1
   estimate **survives a full refit** (it shrinks by 2.4%), and it was never evidence: 3σ needs
   Δχ² ≥ 9, i.e. σ(a0)/a0 = 2.84%, and the present fit gives 31.96%.
4. **No channel rejects the thermal point.** SPARC is the only channel that gets *worse*, by **0.100σ**
   (pull −0.610 → −0.710); SLACS improves by 0.005σ and clusters by 0.052σ. The largest pull anywhere at
   the thermal point is the IMF normalisation at **1.955σ** — the same 2σ IMF tension A71 reported, not a
   new one.
5. **The falsifier is clean at the thermal point:** y_t = **77.944** ∈ [60, 140], L\* = **26.087 pc** ∈
   [24, 90], R_core = **57.95 pc** (< 200), m_P = **4.370e-61 kg** (the task's literal ħ/(cL\*)) or
   **6.180e-61 kg** (A56's λ_P = L\*/√2 convention). All inside.
6. **The one caveat that could overturn the "cannot tell":** the raw χ² of the same two points differs by
   **116.43**, which rescaled to χ²/dof = 1 is **7.24σ**. The declared error model (block bootstrap,
   9.39%) turns that into 1.37σ. The verdict is a statement about the error model, exactly as in A51/A71,
   and it is computed here rather than asserted (§5).

---

## 1. Task 1 — the three fits

**Same data, same priors, same compression, same minimiser as A71.** Parameters: κ (or a0), B, u, and
171 profiled Υ. `chi2 = chi2_SPARC(κ) + chi2_SLACS(κ,B) + chi2_cluster(κ,u) + (ln B)²/σ_prior²`, with
B = 1.00 ± 0.036 dex (Treu+2010) and u = 0.45 ± 0.03 (A18). SPARC enters as a Gaussian in κ with the
200-draw block-bootstrap width (σ/κ = 0.093888688), SLACS as `B_req(κ) ± 0.014251 dex`, and the cluster
term as A18's R_req = 5.552 ± 0.427 with u profiled.

| fit | a0 (m/s²) | κ_P3 | B | u | χ² (compressed) | Δχ² vs (a) | n_par |
|---|---|---|---|---|---|---|---|
| **(a) free** | 8.544010e-11 | **0.377651 ± 0.025787** (stat) ± 0.117904 (syst) | **1.191631 ± 0.036358** | **0.442670 ± 0.02294** | **5.686091** | — | 174 |
| **(b) thermal** | 8.620000e-11 | **0.381010** (fixed) | **1.190385 ± 0.036320** | **0.444240 ± 0.022882** | **5.703008** | **+0.016917** | 173 |
| **(c) κ = ½** | 9.354000e-11 | **0.413453** (fixed) | **1.178557 ± 0.035959** | **0.459046 ± 0.022358** | **7.566877** | **+1.880786** | 173 |

`n_par = 3 shared + 171 Υ` for (a) and `2 + 171` for (b),(c). σ_B is the conditional error at fixed κ
(measurement ⊕ prior); at the free fit the marginal error from the (κ, B) covariance is 0.037598
(A71 K28's σ(ln B) = 0.031552, reproduced to 1e-6).

**Per-channel χ²/dof, on the raw (uncompressed) likelihoods** — dof: SPARC 3204, SLACS 68, clusters 1:

| fit | SPARC raw χ²/dof | SLACS raw χ²/dof | cluster raw χ²/dof | χ² (compressed) |
|---|---|---|---|---|
| (a) free | 7136.38 / 3204 = **2.2273** | 61.75 / 68 = **0.9081** | 0.080 / 1 | 5.686091 |
| (b) thermal | 7143.31 / 3204 = **2.2295** | 61.70 / 68 = **0.9074** | 0.049 / 1 | 5.703008 |
| (c) κ = ½ | 7259.74 / 3204 = **2.2658** | 61.21 / 68 = **0.9002** | 0.119 / 1 | 7.566877 |

The raw table says what the compressed one hides: **SPARC's raw χ² rises monotonically with a0**
(7136.38 → 7143.31 → 7259.74) while **SLACS's raw χ² falls** (61.75 → 61.70 → 61.21). The lensing
channel prefers the higher a0 and the rotation curves prefer the lower one; the thermal point sits between
them, nearer SPARC.

**Does (a) reproduce A71?** Yes, to the last digit A71 quoted:
κ = 0.3776513 vs 0.3776513, B = 1.1916305 vs 1.1916305, u = 0.4426705 vs 0.4426705, χ² = 5.6860907 vs
5.6860907, σ(κ)_stat = 0.025787 vs 0.025787, σ(κ)_tot = 0.120691 vs 0.120691. The **one** numerical
difference in the whole comparison is the raw SPARC χ²: 7136.3828 here vs A71's stored 7136.3469
(5.0e-6 relative), because A71 stored a **cubic-spline interpolation** of χ²(κ) on a 31-point grid while
this lane evaluates χ² directly at the minimum. That is 0.036 units of χ² on 3204 dof and it changes no
conclusion. **A71's numbers are not adjusted.**

**What the fixing costs, decomposed** (positive = the fixed point is worse than the free fit):

```
thermal vs free:  SPARC +0.132134 | SLACS+prior -0.061542 | clusters -0.053676 | sum +0.016917
kappa=1/2 vs free: SPARC +2.441136 | SLACS+prior -0.630705 | clusters +0.070355 | sum +1.880786
```

Fixing a0 at the thermal value is not a compromise: SLACS and the cluster band both *improve* slightly,
because the free fit (κ = 0.3777) sits below both of them, and the only cost is SPARC's 0.13. At κ = ½ the
SPARC cost is 2.44 and SLACS gives back 0.63.

**The convention, stated once.** The rival is "κ = ½", which is a0 = 9.354e-11 only in the ρ_DE
convention: κ_P3 = **0.413453**, κ_DE = **0.499662** in A71's Ω_Λ = 0.6847 (0.499991 in A72's
Ω_Λ = 0.6838). Every fit above is in **κ_P3**, so 0.4135 is the number that enters, not 0.5. The two
footings differ by 0.07%, which is 1/120 of the 8.52% gap between the candidates and is printed rather
than mixed. For the same reason κ_P3(1.1312e-10) = 0.499998 is A71's "κ = ½" and is *not* this task's
rival.

---

## 2. Task 2 — the likelihood ratio

```
chi2(b) = 5.703008 ; chi2(c) = 7.566877 ; Delta = chi2(c) - chi2(b) = +1.863869
sigma (1 dof) = sqrt(Delta) = 1.365236
LR = P(data|thermal)/P(data|kappa=1/2) = exp(Delta/2) = 2.5394
```

**The data lean to the thermal point by 2.54 : 1 — 1.37σ. They cannot tell the two apart.**
Both hypotheses fix one parameter and refit the same two nuisance parameters (B, u), so this is a
like-for-like likelihood ratio, not a Bayes factor: it has no prior-volume or Occam factor, and the two
points are not nested.

**Against A72.** A72's 2.6 : 1 came from moving κ with the nuisances **frozen** at the joint fit:
Δχ² = 1.910676 here (A72 stored 1.914583, a 0.2% difference from A72's use of a0 = 8.618166e-11 rather
than the declared 8.620e-11), LR = 2.5995 : 1 (A72 stored 2.6046 : 1). **Refitting B and u at each point
shrinks Δχ² by 0.046807 (2.4%), leaving 2.5394 : 1.** So A72's estimate survives a full refit almost
intact — and, as A72 said, it was never evidence. The shrink is the signature of the channel structure:
going to κ = ½ costs SPARC 2.309 but SLACS+prior gives back 0.569 and clusters cost only 0.124.

**What it would take to decide it.** 3σ needs Δχ² ≥ 9 for 1 dof, i.e. σ(κ_P3) ≤ 0.010814 or
σ(a0)/a0 = **2.8384%** — against the present 31.9583%. This lane confirms A72's forecast: nothing in the
current data or the record's forecast set reaches it.

**And on the declared systematic error floor** (A71's 31.2%: estimator 20.8%, distance 16.1%, H0 12.5%,
law 10%, Υ 5%), the two candidates are **0.269σ** apart. A fit-quality Δχ² and a measurement-accuracy
σ are different objects; the first says 1.37σ, the second says 0.27σ, and both say the same thing.

---

## 3. Task 3 — the channel pulls at the thermal point

Pulls are (channel's own best fit − value adopted by the fit)/σ_channel. SPARC's σ is the bootstrap
0.033538; SLACS's is its own 0.014251 dex on B; the cluster pull is (u − 0.45)/0.03.

| channel | pull at free (a) | pull at thermal (b) | change | verdict |
|---|---|---|---|---|
| SPARC (κ − κ_fit)/σ | **−0.610σ** | **−0.710σ** | **+0.100σ worse** | preference for lower a0, not a rejection |
| SLACS B (ln B_req − ln B)/σ_B | +0.837σ | +0.832σ | −0.005σ better | — |
| clusters (u − 0.45)/0.03 | −0.244σ | −0.192σ | −0.052σ better | — |
| SLACS, κ direction | +1.965σ | +1.955σ | −0.010σ better | — |
| IMF normalisation log₁₀B/σ | +1.967σ | +1.955σ | −0.012σ better | the lane's standing 2σ |

**The largest worsening is 0.100σ, and no channel is worse by more than 1σ.** The only channel that
degrades is SPARC, it degrades by a tenth of a sigma, and its own best fit is 0.71σ from the thermal
point. That is a **preference**, and at 0.71σ it is not evidence — the same conclusion A71 reached about
the free fit's −0.61σ, moved by 0.1σ.

Two details worth keeping:

- **The thermal point *relieves* the SLACS tension**, in both directions it can be measured: the B pull
  falls from +0.837 to +0.832σ and the κ-direction ridge pull from +1.965 to +1.955σ. The lensing channel
  wants a *higher* a0, so moving up from the free fit helps it — which is exactly why the total Δχ²
  (1.86) is smaller than SPARC's own contribution (2.31).
- **The thermal point does not add to the IMF tension.** The 1.955σ pull on B is the one thing in the fit
  that is above 1σ, it was 1.967σ at the free fit, and it is a statement about Treu's prior and the
  cross-method IMF spread (A70/A71), not about a0.

---

## 4. Task 4 — the falsifier at a0 = 8.620e-11, κ_DE = Z/4π

| quantity | value at the thermal point | band / reference | status |
|---|---|---|---|
| κ_DE from a0 | **0.460454** | Z/4π = **0.460659**; from Λc⁴/a0² = 0.460757 | consistent to 0.07% |
| **y_t** from I(y_t) = 8π/κ_DE² | **77.943961** | pre-registered **[60, 140]** | **INSIDE** |
| **L\*** = σ_c²/a0 (σ_c = 8.33 km/s) | **26.087484 pc** | pre-registered **[24, 90] pc** | **INSIDE** |
| **R_core** = (π/√2)L\* | **57.951818 pc** | A20 ceiling 200 pc (53.3146 pc at L\* = 24) | **INSIDE** |
| **m_P** = ħ/(cL\*) (task's literal form) | **4.369912e-61 kg** = 2.451341e-25 eV | — | — |
| m_P = ħ/(cλ_P), λ_P = L\*/√2 (A56's convention) | **6.179989e-61 kg** = 3.466720e-25 eV | A56: 6.7105e-61 kg | **0.920943×** |

Supporting numbers, all computed: N_Λ = Λc⁴/a0² = **118.384859**; the closure root is identical under the
tan-substitution quadrature and A28's rational integral to **7.0e-12**; at κ = ½ y_t = **66.467712** and at
the free-fit κ_DE = 0.4564 y_t = **79.302910**; at κ = ½ L\* = **24.040422 pc** (and at the canonical
9.36e-11, **24.025012 pc**, A20's anchor — which is an *inversion* of L\* = 24, not a prediction, and A65
says so). The band in κ_DE is [0.3415, 0.5267] and 0.460454 is inside it.

The two κ_DE values in the first row that differ (0.460454 from a0, 0.460757 from Λ) differ by 0.0658%
because the BRIEF's Λ = 1.0890e-52 implies Ω_Λ = 0.6838 while A71 uses 0.6847. Both are printed; neither
is mixed into the fit.

**One line: the thermal point predicts the coefficient of the de Sitter horizon, a0/(cH_Λ) = 1/(2π) =
0.159155, i.e. κ_DE = Z/4π = 0.460659 and a RAR scale 8.52% below the κ = ½ value — and the measurement
that separates them is a0 to 2.84% (3σ), which nothing on disk reaches (best: 31.96%) and which A72
forecasts only for a wide-binary γ_v at 18–22 kAU with ≈ 4 × 10⁵ pairs.**

---

## 5. The error-model caveat, computed

The same two fixed points compared on the **raw** SPARC χ² (Υ profiled) differ by **116.4276**. Rescaled
so that χ²/dof = 1 (factor 2.2209) that is **52.4228 → 7.24σ**, against the compressed likelihood's
**2.3090 → 1.37σ** — a factor **50.4**. The reason is the one A51 K6 established: the formal Δχ² = 1
error in a0 is **1.1269%**, the 200-draw block bootstrap is **9.3889%**, a factor **8.33**.

So: **if the per-point SPARC errors were correct, the thermal point would beat κ = ½ at 7.2σ.** It does
not, because the 3375 points are not independent (≈ 20 correlated points per galaxy and one profiled Υ
each), and the block bootstrap is the declared honest error. This lane inherits that choice to be
comparable with A51/A71 — and states the consequence rather than burying it. Every "cannot tell" in this
report is conditional on that error model being right; if the true error on a0 is nearer the formal 1.1269%
than the bootstrap 9.3889%, the question is already decided in favour of the thermal point.

---

## 6. Where this agrees or disagrees with A71/A72 — explicitly

1. **A71 is reproduced, not revised.** κ, B, u, χ², σ_stat and σ_tot all match to ≤ 1e-6 relative. The
   only difference anywhere is the 5.0e-6 relative on the raw SPARC χ², caused by A71 storing a spline
   interpolation (§1). Nothing in A71 is adjusted.
2. **A72's 2.6 : 1 survives the full refit at 2.54 : 1** (§2). A72's σ(a0)/a0 = 2.874% for 3σ becomes
   2.838% with the task's rounded pair 8.620/9.354e-11; A72's 8.54% gap becomes 8.5151% (or 8.5468% with
   A72's unrounded pair). These are rounding differences of the same statement.
3. **A72's κ_DE = 0.460659 is the algebraic value**; the deployed a0 = 8.620e-11 gives 0.460454, 0.044%
   lower, entirely from rounding 8.618166e-11 → 8.620e-11. The difference is 1/190 of the gap between the
   candidates and does not affect any fit (all fits are in κ_P3).
4. **"κ = ½ at a0 = 9.354e-11" is exact only in A72's Ω_Λ = 0.6838** (0.499991). In A71's Ω_Λ = 0.6847
   it is 0.499662. This lane uses A71's constants throughout and reports both, because a 0.07% convention
   difference must not be allowed to look like a 0.07% physical one.
5. **The A71 headline Δχ²(κ = ½, B profiled) = 20.92 is a different object** from this lane's 1.881: A71
   moved κ alone inside the *free* model (whose B is not at B_req for the new κ); here B and u are refit at
   each point, which is the only like-for-like comparison between two fixed values of a0.
6. **A70's SLACS model and Treu prior are used unchanged** — B_req(κ = 0.5) = 1.17383 (A70: 1.174),
   dlnR/dlnB = 0.77748, dlnR/dlnκ = 0.12054, σ(log B) = 0.014251 dex, 56 lenses, 95% upper bound 1.17671.

---

## 7. What this does not do

1. **No new data and no new likelihood.** Every number is A71's machinery, evaluated at two extra points.
   The data files are read-only and hashed (SPARC `469f4f556dc813b2`, SLACS `d78d7627d6bbcc07`).
2. **The compressed χ² is not a χ² with thousands of dof.** It is a four-term Gaussian summary (one number
   per channel plus the IMF prior). The raw per-channel χ²/dof are reported beside it and tell a sharper
   story (§1), but they are not used for the likelihood ratio and should not be.
3. **The error model dominates everything** (§5): a factor 50 in Δχ². No statement here is stronger than
   that choice.
4. **The thermal derivation is not tested here.** A72 derives the *scale* a0 = cH_Λ/2π from a quantum
   carrier at the Gibbons–Hawking temperature; A62 K15 showed that mechanism's response is analytic
   (slope 1) and so does not derive MOND's shape. This lane fits the scale, not the mechanism.
5. **B is one number for 70 lenses of one survey.** With A70's cross-method IMF width (0.103 dex instead of
   0.036) the SLACS give-back shrinks and Δχ²(thermal vs ½) rises to 2.349408 (LR 3.2372 : 1 in that run) — still sub-2σ. That is the
   `imf_prior` mutation.
6. **m_P depends on the convention.** The task's literal ħ/(cL\*) is √2 smaller than A56's ħ/(cλ_P) with
   λ_P = L\*/√2; both are printed and the ratio is exactly √2.
7. **The cluster channel is circular** (u and R_req from the same amplitudes) and the SPARC error carries
   A51's estimator/distance systematics as a separate 31.2% floor, not inside the likelihood.

---

## 8. Checks (29/29 PASS, exit 0)

| id | what it proves | measured | killed by |
|---|---|---|---|
| C1 | SPARC vector is A71's, byte for byte | 175/171/3375, sha 469f4f556dc813b2 | drop_gal |
| C2 | SLACS sample is A70's | 85 rows, 70 lenses, sha d78d7627d6bbcc07 | drop_lens |
| C3 | SPARC likelihood is the record's (zero-parameter χ²/dof) | 6.8651 / 6.6312 / 2.4714 | floor10 |
| C4 | the convention: which a0 is κ = ½ | κ_P3 0.413453, κ_DE 0.499662 / 0.499991 | kappa_de |
| C5 | the thermal value from three constant routes | 8.618166e-11, 8.623833e-11, 8.620e-11 | thermal_pi |
| C6 | SPARC-only fit vs A51's stored values | a0 8.081465e-11, κ 0.357207, χ²/dof 2.2209 | floor10 |
| C7 | bootstrap vs formal error, and vs A51 | 0.093888688 vs 0.093888688; ratio 8.33 | boot_draws |
| C8 | the SLACS model is A55's/A70's per lens | median 0.885232, max dev 0.0 | sersic35 |
| C9 | B_req = 1.174, not A55's 1.283 | 1.17383 / 1.27610 | arcsec |
| C10 | the two responses and their ratio | 0.77748 / 0.12054 / 6.45 | resp_lin |
| C11 | σ(log B) two routes | 0.014251 vs 0.015469 dex | sersic35 |
| C12 | Treu+2010 reproduces its abstract | 56 lenses, mean −0.00054, 95% hi 1.17671 | treu_shift |
| C13 | A18's cluster anchor | 1.6863 Mpc / 3.7702 / 2.6179 | cluster_a |
| C14 | cluster-only κ and its u-circularity | 0.39339 ± 0.04316 (10.97%) | u_prior |
| C15 | fit (a) IS A71 | κ 0.3776513, B 1.1916305, u 0.4426705, χ² 5.6860907 | no_boot |
| C16 | independent 3-parameter minimiser | agree to 1e-5 in κ and B | b_marg |
| C17 | σ(κ), σ(ln B), σ(B) are A71's | 0.025787 / 0.031552 / 0.036358 | no_boot |
| C18 | Δχ²(thermal vs free) small, decomposition closes | +0.016917 | thermal_pi |
| C19 | Δχ²(κ=½ vs free) | +1.880786 | imf_prior |
| C20 | B spline vs a direct 70-lens root at the thermal κ | 1.223343 vs 1.219356 | sersic35 |
| C21 | Δχ² → σ → LR is one consistent transform, in the sub-2σ regime | 1.365236 / 2.5394 / Δ 1.8639 | thermal_pi |
| C22 | A72's 2.6 : 1 survives the refit | 2.5995 → 2.5394, shrink 0.0468 | imf_prior |
| C23 | no channel worse by 1σ at the thermal point | −0.710 / +0.832 / −0.192 | no_boot |
| C24 | SLACS's κ-direction pull is relieved, not worsened | +1.965 → +1.955 | imf_prior |
| C25 | y_t at the thermal point, two quadratures, inside the band | 77.943961, 7.0e-12 apart | lambda_off |
| C26 | L\*, R_core, m_P inside their pre-registered values | 26.0875 pc, 57.9518 pc, 6.180e-61 kg | thermal_pi |
| C27 | the cost decomposition closes and its sign structure | SPARC +2.309, SLACS −0.569, clusters +0.124 | a0_off20 |
| C28 | the per-channel χ²/dof quoted are A71's objects | 2.227335 vs 2.227324 | drop_gal |
| C29 | the raw-χ² route and the 8.33× error-model factor | 116.43 → 7.24σ vs 2.31 → 1.37σ | a0_off20 |

20 single-input mutations, all exit 1, every check killed by at least one (`MUTATE.md`). None was deleted.

---

## VERDICT

**(1)** With a0 fixed at the thermal value 8.620e-11 and B, u and all 171 Υ refit, the total χ² is
**5.703008** against the free fit's **5.686091** — **Δχ² = +0.016917 (0.13σ)**, i.e. the thermal point is
free. The κ = ½ point (a0 = 9.354e-11, κ_P3 = 0.413453) gives **7.566877**, **Δχ² = +1.880786 (1.37σ)**.
The decisive difference is **Δχ² = 1.863869 → 1.365σ, a likelihood ratio of 2.5394 : 1 for the thermal
point**; A72's 2.6 : 1 survives the full refit, shrinking 2.4%, and confirms that the data cannot decide.
**(2)** SPARC drives it: +2.309 of the 1.864, with SLACS+prior giving back 0.569 and clusters costing 0.124
— the lensing channel prefers the higher a0, which is why the net preference is smaller than SPARC's own.
**(3)** Neither point is rejected, and no channel rejects the thermal point: the only channel that gets
worse is SPARC, by **0.100σ** (pull −0.610 → −0.710), while SLACS improves by 0.005σ and clusters by
0.052σ; the largest pull anywhere is the IMF normalisation at 1.955σ, unchanged from the free fit's
1.967σ. **(4)** The falsifier is clean at the thermal point — **y_t = 77.944** inside [60, 140],
**L\* = 26.087 pc** inside [24, 90], R_core = 57.95 pc under A20's 200 pc ceiling, m_P = 4.370e-61 kg
(ħ/cL\*) or 6.180e-61 kg (A56's λ_P convention) — so the thermal point survives everything this dataset
can throw at it, and the honest summary is: **the theory's declared value costs nothing measurable, its
rival costs 1.4σ, and the 2.5 : 1 lean is worth exactly what a 1.4σ lean is worth — nothing yet, because
the whole comparison rests on a 9.4% bootstrap error that is itself 8.3× the formal one; with the
per-point errors the same data would prefer the thermal point at 7.2σ.**
