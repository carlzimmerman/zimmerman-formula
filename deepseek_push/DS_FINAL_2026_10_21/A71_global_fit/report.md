# A71 — THE GLOBAL CONSISTENCY TEST

**Lane:** A71_global_fit · **Date:** 2026-10-22 · **Base:** `deepseek_push/DS_FINAL_2026_10_21`
**Script:** `a71_checks.py` — **28/28 PASS, exit 0, 27 s** · **Output:** `a71.out` · **Data:** `a71_results.json`
**Mutations:** 16, all exit 1, every check killed by at least one (`MUTATE.md`, `a71_MUTATE_*.out`).

**Read:** `A51_kappa_measured` (the joint κ fit), `A70_slacs_audit` (the corrected SLACS likelihood),
`A18_two_ratios` / `A44_no_edge` (cluster ESD and band ratios), `A24_wide_binaries` (γ_v = 1.18,
no data), `A65_stiffness_origin` (L\* fitted at 24 pc), `A28_turnoff_origin` (the closure
I(y_t) = 8π/κ²).

**One parameter set, three channels, and the pulls:**

```
kappa_P3 = 0.37765 +- 0.02579 (stat) +- 0.11790 (syst) = 0.37765 +- 0.12069
a0       = 8.5440e-11 m/s^2      (8.7% below canonical 9.36e-11, 24.5% below the P3 footing)
B        = 1.1916 +- 0.0364      (log10 B = +0.0761 +- 0.0141 dex, 1.97 sigma above 1.00)
u        = 0.4427

channel      pull in kappa      other pull
SPARC         -0.61 sigma       --
clusters      +0.37 sigma       --
SLACS         +1.97 sigma       B: +1.97 sigma
global tension T = 5.69 for 2 shared parameters -> 1.89 sigma
```

---

## 0. Bottom line

1. **One parameter set fits all three channels at 1.9σ.** The kappa channels agree to within
   2σ (SPARC −0.61, clusters +0.37, the SLACS ridge +1.97). The global tension is **T = 5.69 for
   2 shared parameters, p = 0.058, 1.89σ** — and **4.47 of the 5.69 is the IMF-prior term alone**;
   with only the three data terms, T = 1.21 (0.6σ). Nothing in kappa is pulled.
2. **The joint fit is κ = 0.3777 ± 0.0258 (stat) ± 0.1179 (syst), B = 1.1916 ± 0.0364.** The
   statistical error is unchanged from A51 (0.0265 → 0.0258); adding the corrected SLACS likelihood
   moves κ by **+0.0062** (0.24σ) relative to the same fit without it, **+0.0068** (0.26σ)
   relative to A51's published value. The new content is **B**, which now has a joint posterior rather
   than a fixed-Salpeter or fixed-κ answer.
3. **κ = ½ is inside the joint 95% region only through the declared systematic floor, and which ½
   depends on the convention.** In A51's `ρ_bare = ρ_crit` convention κ = ½ is a0 = 1.1312e-10 and
   the joint fit is **4.74σ** away statistically / **1.01σ** in total — outside the statistical 95%
   `[0.328, 0.429]`, inside the total `[0.141, 0.614]`. The **canonical footing a0 = 9.36e-11**
   (which is κ = ½ in the `ρ_DE` convention, and κ_P3 = 0.4137) is **1.40σ** statistically and
   **0.30σ** in total — the joint fit sits essentially on it. **The two footings are 3.35σ
   apart at the joint precision, and the fit sits far closer to the canonical one.**
4. **The single most valuable next measurement is a wide-binary γ_v at 18–22 kAU** (Gaia DR4,
   ~30,000 pairs over 2–30 kAU). It is the only channel with no Υ, no IMF and no distance ladder in
   the measurement, it would give σ(κ) = 0.040, and it would cut the joint error from 0.121 to 0.061. It is
   also the only channel that tests the law's EFE at the same time.

---

## 1. What is in the likelihood, and what is deliberately not

| channel | data on disk (read-only, hashed) | N | measures | nuisance | in the fit |
|---|---|---|---|---|---|
| **SPARC RAR** | `real_research/data/sparc_data/*_rotmod.dat`, sha256(concat) `469f4f556dc813b2` | 171 gal / 3375 pts | κ through a0 | one Υ per galaxy, profiled | **yes** |
| **SLACS** | `real_research/data/slacs_auger2009_lenses.tsv`, sha256 `d78d7627d6bbcc07…` | 70 lenses | B (the IMF normalisation) | — | **yes** |
| **clusters** | A18's `R_req = 5.552 ± 0.427` from the 318-cluster MID amplitude | 1 number | κ at 11% | u = 0.45 ± 0.03 | **yes**, flagged circular |
| closure `I(y_t) = 8π/κ²` | Λ_obs, a0 | — | **nothing** | — | **no — identity** (K15, K16) |
| BAO + SNe + CMB | DESI DR2 / Pantheon+ / Planck, the vector A51 fitted | 13 + 1580 + 3 | **nothing** on κ | h | **no — κ-blind** (K17) |
| wide binaries | *none on disk* | 0 | — | — | **no — no data** (K23) |
| A65's L\* = 24 pc | the same SPARC photometry | — | a0 at 0.1% | σ_c | **no — not independent** (K24) |

Three exclusions are computed, not asserted:

- **The closure is an identity.** With `a0 = κc√(Gρ_Λ)` and `ρ_Λ = Λc²/8πG`, `Λc⁴/a0² = 8π/κ²`
  exactly, so `F(y_t) = 8π/κ²` merely *defines* y_t as a function of κ. Computed: the residual of
  `F(y_t) − 8π/κ²` at the root is **≤ 4.6e-12 for every κ in [0.25, 0.80]**, the two independent
  integral representations agree to **5.3e-14**, and the elasticity is **dln y_t/dln κ = −1.9462**
  (A28: −1.946912). Counting it as data would add a zero-variance constraint on a derived quantity
  (K15, K16).
- **BAO/SNe/CMB are κ-blind.** `E(z; κ=0.20)/E(z; κ=1.00) − 1 = 0.0e+00` over z ∈ [0.05, 2.5], and
  the framework background is an **exact** reparametrisation of flat ΛCDM,
  `E_fw(z;Ω_m) = E_ΛCDM(z; Ω_m/(1+Ω_m))` to **2.2e-16**. The vector therefore supplies neither κ
  nor an independent H0 (K17). A51's full fit of it is not repeated because the exclusion is
  structural, and it is verified here rather than assumed.
- **Wide binaries have no data.** A24's prediction γ_v(20 kAU) = **1.5316** EFE-blind (A24: 1.5315,
  reproduced exactly) or **1.1811** EFE-present. It is a prediction, so it cannot enter a likelihood
  (K23).

## 2. The likelihood, and the two compressions it needs

Parameters: **κ** (or a0), **B** (the single SLACS M/L normalisation), **u** (A18's sourcing
fraction), and **171 profiled Υ** in SPARC.

```
chi2 = chi2_SPARC(kappa) + chi2_SLACS(kappa,B) + chi2_cluster(kappa,u) + (ln B)^2/sigma_prior^2
priors:  B = 1.00 +- 0.036 dex (Treu+2010, 56 lenses, same sample)
         u = 0.45 +- 0.03      (A18, from the same amplitudes -> circular, stated)
```

**SPARC is compressed to a Gaussian in κ, and it must be.** The raw χ²/dof is 2.2209, the formal
Δχ² = 1 error is **1.127% in a0**, and the 200-draw block bootstrap is **9.389%** — a ratio of
**8.3** (K6, reproducing A51's 0.093889 to 1e-6). Using the raw curvature would make SPARC dominate
everything by a factor 8 in σ, which is exactly the error A51 identifies; the bootstrap is the
honest statistical error and it is what enters here. The raw χ² is still reported (below) and a
mutation (`no_boot`) shows what the formal error would do.

**SLACS is compressed to B(κ) ± 0.0143 dex, and that is exact where it matters.** The 70-lens model
gives `mean ln(R_E,pred/R_E,obs) = m0(κ)`, and `B_req(κ) = exp(−m0/0.7775)` with
`dlnR/dlnB = 0.7775 ± 0.083` (per-lens scatter). The response route reproduces the root-found boost
to **1e-4** (B_response = 1.1737 vs B_root = 1.1738, K9), and the per-lens response scatters by 11%
about its median, which is why the compression is used for the *mean* only. Two independent routes to
σ(log B) agree: **0.0143 dex** (mean/SEM) and **0.0155 dex** (full per-lens curvature), 8.5% apart
(K11). The task-specified 0.0143 is used.

## 3. The joint fit

| channel | χ² at the joint best fit (raw) | dof | χ²/dof | compressed contribution |
|---|---|---|---|---|
| SPARC | **7136.35** | 3204 | **2.2273** | 0.372 |
| SLACS | **61.75** | 68 | **0.9081** | 0.701 |
| clusters | 0.080 (1 datum, u profiled) | 1 | 0.08 | 0.140 |
| IMF prior | — | 1 | — | **4.473** |
| **total** | | | | **5.686** |

**Posterior.** The (κ, B) surface is a mildly correlated Gaussian (K28):

```
kappa_P3 = 0.37765 +- 0.02579 (stat)          [Delta-chi2 = 1, profile]
         = 0.37765 +- 0.11790 (stat + the declared 31.2% coherent floor)
95% stat   [0.32806, 0.42907]      95% total  [0.14110, 0.61421]
B        = 1.1916 +- 0.0364 (3.2%)   sigma(lnB) = 0.03155, corr(ln kappa, ln B) = -0.255
1 sigma ellipse: kappa 0.3405-0.4189, B 1.1360-1.2500
2 sigma ellipse: kappa 0.3187-0.4475, B 1.1018-1.2888
kappa_DE = 0.4564 +- 0.0312 (the same fit in the rho_DE convention, K27)
```

The systematics are A51's, recomputed from their components: estimator/error model 0.2084 (verified
at two of its endpoints: the 3% and 10% floors give a0 = 7.3419e-11 and 8.5639e-11 against A51's
7.3417e-11 and 8.5464e-11, K24), distance zero point 0.161, H0 footing 0.125, law choice 0.100,
Υ window 0.050 → **0.3122** combined.

## 4. The pulls, and the global tension

| channel | its own best fit | joint value | pull |
|---|---|---|---|
| SPARC | κ = 0.35721 ± 0.03354 | 0.37765 | **−0.61σ** |
| clusters | κ = 0.39347 ± 0.04287 | 0.37765 | **+0.37σ** |
| SLACS (κ direction) | κ = 1.0417 ± 0.3379 | 0.37765 | **+1.97σ** |
| IMF normalisation | B = 1.00 (prior mean) | 1.1916 | **+1.97σ** |

The SLACS κ ridge runs over **[0.72, 1.40]** at Δχ² = 1 — a 1/6.5 lever (see §8). The pull that
matters is not in κ at all: **the joint fit needs an IMF normalisation 1.97σ above Treu's mean**.

**Global tension.** `χ²_joint − Σ χ²_channel,min = 5.686` for the 2 shared parameters (κ, B):
**p = 0.058, 1.89σ**. Decomposition: SPARC 0.372 + SLACS 0.701 + clusters 0.140 + **IMF prior 4.473**.
With the prior term removed (i.e. asking only whether the three *data* channels agree), **T = 1.213,
0.6σ**. So:

> **The three data channels are consistent. The tension is between the data and the IMF
> normalisation, and it is 2σ — not a falsification, and not nothing.**

## 5. Task 3(b) — is κ = ½ inside the joint 95% region?

**This question has two answers because "κ = ½" is two different a0's, and the record uses both.**
K27 resolves it: for a0 = 9.36e-11,

```
kappa_DE = a0 sqrt(8 pi)/(c H0 sqrt(3 Omega_L)) = 0.499983   <- 1/2 in the rho_DE convention
kappa_P3 = a0 sqrt(8 pi/3)/(c H0)              = 0.413719   <- A51's rho_crit convention
ratio 1.2085 = 1/sqrt(Omega_L) exactly
```

and for a0 = 1.1312e-10, κ_P3 = 0.500000 / κ_DE = 0.604254. The falsifier band `y_t ∈ [60,140]`
recomputes to **κ_DE ∈ [0.3415, 0.5267]**, i.e. it is stated in the `ρ_DE` convention (A28's
[0.3415, 0.5265] reproduced to 3.3e-4).

| target | its κ in P3 | distance (stat) | distance (total) | inside the 95% region? |
|---|---|---|---|---|
| **a0 = 9.36e-11** (canonical; κ_DE = ½) | 0.41372 | **1.40σ** | **0.30σ** | **yes, comfortably** |
| **a0 = 1.1312e-10** (P3; κ_P3 = ½) | 0.50000 | **4.74σ** | **1.01σ** | **no statistically; yes in total** |

Both rows are convention-independent: converting the joint fit to κ_DE = 0.4564 ± 0.0312 gives
exactly the same 1.40σ and 4.74σ (K27 asserts the identity).

Supporting numbers: Δχ²(κ = ½ with B profiled) = **20.92**; the theory's *own* parameter point
(κ, B, u) = (0.5, 1.00, 0.45) has **Δχ² = 47.23** on statistical errors (**30.50** with the floor),
of which 18.13 is SPARC, 23.86 is SLACS and 5.24 is clusters.

**So: yes, κ = ½ is inside the joint 95% region — but only for the canonical a0 = 9.36e-11, and only
by 0.3σ, and only because the fit sits there. The P3 value 1.1312e-10 is excluded at 4.7σ
statistically and admitted only by the 31% systematic floor.** The channel that drives the exclusion
is SPARC (18.13 of the 47.23); the channel that drives the *opposite* pull (toward higher κ) is SLACS,
whose B-requirement is 1.97σ high.

## 6. Task 3(a) — do SPARC's κ and SLACS's B agree once the IMF prior is applied?

**They agree in κ and disagree in B.** Precisely (K26):

```
at SPARC's kappa = 0.3572   SLACS demands B = 1.2339 = +0.0913 dex = 2.36 sigma
                            (above Treu's 95% upper bound 1.1767)
at the joint kappa = 0.3777 SLACS demands B = 1.2248 ; the joint compromise is 1.1916 (1.97 sigma)
at kappa = 0.5 (P3)         SLACS demands B = 1.1738 = +0.0696 dex = 1.80 sigma   (A70's headline)
```

- The κ channels agree: 0.3572 (SPARC), 0.3935 (clusters), 1.0417 ± 0.3379 (SLACS ridge) — the
  largest discrepancy is **1.97σ**.
- The IMF normalisation does **not** agree: 2.36σ at SPARC's κ, 1.97σ at the joint κ.
- **The joint fit makes the IMF requirement worse, not better.** A70's escape works at κ = 0.5
  (B = 1.174, inside Treu's 95% bound by 0.25%); at the joint κ = 0.378 it requires B = 1.22 and the
  joint posterior lands at **B = 1.1916, which is OUTSIDE the 95% bound 1.1767**.
- To bring the required B back to the 95% bound the joint fit would need **κ = 0.4928**, i.e.
  **+4.5σ** from the joint value. That is the same statement as "the data would like the P3 footing
  for lensing and the canonical footing for rotation curves".

## 7. Where this contradicts A51 or A70 — explicitly

**(a) A70's "Δχ² = 0.26 over κ ∈ [0.20, 0.80] with a free IMF" is a *mean-only* statement, and the
full per-lens likelihood is not flat.** Computed here on the same 70 lenses (K25): with B profiled,
the mean term is **exactly zero** at every κ (by construction — 2.5e-31), while the scatter term
runs **63.29 → 56.94**, i.e. **Δχ² = 6.35** over the same band, monotonically favouring *higher* κ
(10.15 over the wider grid κ ∈ [0.2, 1.7]).
The cause is physical: a larger a0 raises R_pred more for the lenses that are currently
under-predicted, which is exactly the `R_E/R_e` residual A70 itself measured at +0.172 ± 0.060. It is
degenerate with the assumed Sérsic n = 4, so **this lane does not use it** — the primary likelihood
uses the mean term (B at fixed κ) only. But A70's 0.26 is neither the mean term (0.000) nor the full
likelihood (6.35 over A70's own band), and the claim "κ is unconstrained" holds only for the mean.

**(b) A70's verdict stands but its number does not transfer to the joint fit.** "Allowed at the 95%
boundary, 1.80σ" is correct at κ = 0.5. At the joint κ it is 1.97σ and outside the bound. The joint
fit aggravates the IMF tension by 0.17σ; it does not relieve it. A70 is right that this is not a
falsification; the capstone sharpens the number.

**(c) Against A51: no contradiction, one shift.** κ = 0.3708 ± 0.0265 (A51, SPARC + clusters) →
0.37765 ± 0.02579 (this lane, + SLACS). The shift is **+0.0068 (0.26σ)**, and the joint fit without
the SLACS channel reproduces A51's number at 0.37148. A51's central claim — that the error is set by
the error model, not by the data — survives intact and is now quantified with B in the fit.

**(d) A51's "lensing has zero Fisher information on κ" is true of A44's isolated-lensing stack and
false of SLACS.** SLACS does carry κ information — Δχ² = 6.35 over the band through the scatter
term — but 6.5× less per unit than it carries on B, so it is still not a κ measurement. Both
statements are in this lane's output and they are not the same statement.

## 8. Task 4 — what the joint fit cannot say

**Degeneracies.**

| parameter | constrained by | with a lever of | unconstrained by |
|---|---|---|---|
| κ | SPARC (±9.4% stat) | — | SLACS alone (ridge 0.72–1.40, 1/6.5), lensing (zero), BAO/SNe/CMB (zero), closure (identity) |
| B | SLACS (±3.3% on B) | dlnR/dlnB = 0.7775 | **every other channel** — SPARC's Υ_i are free and are not the same parameter (different band and IMF zero point) |
| u | the A18 prior (±6.7%) | dlnR/dlna0 = +0.928 | the data: u and R_req come from the same amplitudes |

`dlnR/dlnκ = 0.1205` against `dlnR/dlnB = 0.7775`: **6.45×** (K9). That single ratio is the whole
structure of the lensing channel — it measures a mass normalisation and reports it in κ units only
because κ is what we asked for.

**Non-independence.**

- SPARC and A65's L\* use the same galaxies, the same 3.6 μm photometry and the same distances; the
  L\* anchor is 24 pc *by construction* from σ_c, and at the joint a0 the formula predicts
  **26.32 pc** — a 9.6% discrepancy that is a statement about σ_c, not about κ (K24).
- SLACS's prior (Treu+2010) is measured on 56 lenses of the same survey, most of them in the 70.
- The cluster `R_req` and `u` come from the same stack; the cluster channel is a consistency band,
  not a measurement (A18 says so and A51 flags it).
- The 31.2% coherent floor is attached to the SPARC measurement, not to κ itself — which is why an
  independent channel is worth more than more SPARC galaxies (below).

**Error budget** (fraction of the total variance of κ):

| term | σ(κ) | share | removable by |
|---|---|---|---|
| statistical (joint) | 0.02579 | 4.6% | more galaxies |
| **estimator / error model** | **0.07870** | **42.5%** | analysis, not data |
| **distance zero point** | **0.06080** | **25.4%** | a distance-scale measurement |
| H0 footing | 0.04721 | 15.3% | a conversion decision |
| law choice | 0.03777 | 9.8% | a law decision |
| Υ window | 0.01888 | 2.4% | — |

Remove-one: estimator → 0.0915 (24% tighter), distance → 0.1043 (14%), H0 → 0.1111 (8%).
And what each candidate next measurement would do to the **joint** error (0.1207 now):

```
wide binary, one 18-22 kAU bin (2,223 pairs)        sigma(kappa) 0.142  ->  joint 0.0995
wide binary, full 30,000-pair catalogue (7 bins)    sigma(kappa) 0.040  ->  joint 0.0605
SPARC at N = 1000, same systematics (replaces it)   sigma(kappa) 0.118  ->  joint 0.1184
distance zero point fixed to 2.5%                   --                  ->  joint 0.1043
```

> **ERRATUM (2026-10-22, doors push D2):** σ(κ) = 0.040 and joint 0.1207 → 0.0605 are overstated. An independent FFT-QUMOND solve gives dγ_v/dκ = 0.41 (not 0.51; A71 rescaled 1.1811 by √ν instead of solving), the shared σ_sys = 0.020 cannot be divided by √7, and γ_v depends almost only on g_ext/a₀ (the two frozen g_ext values add σ(κ) = 0.031, tying a wide-binary κ to Galactic R₀ and v_c). Corrected: **σ(κ) ≈ 0.073, joint 0.1207 → 0.077** (infinite-N floor from σ_sys alone 0.048). See `doors_push_2026_10_22/D2_wide_binary_fork/README.md`.

**The single number: σ(κ) = 0.040, and the observation that delivers it is a wide-binary γ_v
measurement at 18–22 kAU** — the only channel with no Υ, no IMF and no distance ladder in the
measurement itself.
At the full DR4 catalogue (~30,000 pairs over 2–30 kAU, the 18–22 kAU bin alone holding ~2,223 pairs
at σ_tot = 0.0726) it would cut the joint error from **0.1207 to 0.0605** — 3.7× the reduction of the
best SPARC-side fix (0.1043) — because it does not share SPARC's systematics (the H0 conversion it
does share is re-added in the forecast). `dγ_v/dκ = 0.510` (EFE-present) /
0.675 (EFE-blind) at 20 kAU, so the same measurement is simultaneously a 4.5σ test of the EFE
(A24's registered arm, 0.3286/0.0726 = 4.5σ). **More SPARC galaxies are worth 2%: N = 1000 gives 0.1184. Do not buy them.**

> **ERRATUM (2026-10-22, doors push D2):** σ(κ) = 0.040 and joint 0.1207 → 0.0605 are overstated. An independent FFT-QUMOND solve gives dγ_v/dκ = 0.41 (not 0.51; A71 rescaled 1.1811 by √ν instead of solving), the shared σ_sys = 0.020 cannot be divided by √7, and γ_v depends almost only on g_ext/a₀ (the two frozen g_ext values add σ(κ) = 0.031, tying a wide-binary κ to Galactic R₀ and v_c). Corrected: **σ(κ) ≈ 0.073, joint 0.1207 → 0.077** (infinite-N floor from σ_sys alone 0.048). See `doors_push_2026_10_22/D2_wide_binary_fork/README.md`. The bin size ~2,223 is also overstated (~208 at DR3 occupancy).

## 9. Checks (28/28 PASS, exit 0) and mutations

| id | what it proves | measured |
|---|---|---|
| K1 | SPARC vector: 175 files → 171 galaxies / 3375 points, byte-identical to A51's | sha 469f4f556dc813b2 |
| K2 | SLACS census: 85 rows → 70 usable lenses | sha d78d7627d6bbcc07 |
| K3 | the likelihood is the record's (three χ²/dof) | 6.8651 / 6.6312 / 2.4714 |
| K4 | the κ identity and the DE convention | 0.500000000 / 0.604254 / rt 0 |
| K5 | SPARC-only fit vs A51's stored values | a0 8.081465e-11, κ 0.357207 |
| K6 | bootstrap vs formal error, and vs A51 | 9.389% vs 1.127%, ratio 8.3 |
| K7 | the 70 per-lens ratios vs A55's stored ones | median 0.885232, max dev 0.0 |
| K8 | B_req and A55's 1/median² error | 1.1738 vs 1.2761 |
| K9 | the two responses and their ratio | 0.7775 / 0.1205 / 6.45 |
| K10 | κ\* with Salpeter fixed | 1.0279 ± 0.1297 |
| K11 | σ(log B) two routes | 0.0143 vs 0.0155 dex |
| K12 | Treu+2010 reproduces its abstract; 95% = [0.850, 1.177] | mean −0.0005, hi 1.1767 |
| K13 | A18's cluster anchor | 1.6863 Mpc / 3.7702 / 2.6179 |
| K14 | cluster-only κ and its u-circularity | 0.3934 ± 0.0432 |
| K15 | the closure reproduces A28 | 66.299937 / 66.380331 / 0.500311 |
| K16 | two integral forms agree; elasticity | 5.3e-14 / −1.9462 |
| K17 | BAO/SNe/CMB are κ-blind; exact ΛCDM reparametrisation | 0.0 / 2.2e-16 |
| K18 | joint profile vs an independent 3-D minimiser | 0.377651 / 1.191631 / 0.442670 |
| K19 | joint κ vs A51 | 0.37765 ± 0.02579 vs 0.37083 ± 0.02648 |
| K20 | the four pulls | −0.61 / +0.37 / +1.97 / +1.97 |
| K21 | the global tension | T = 5.686, 1.89σ |
| K22 | κ = ½ in the joint 95% | 4.74σ stat / 1.01σ total |
| K23 | wide-binary prediction, no data | 1.5316 / 1.1811 |
| K24 | error budget, remove-one, the next measurement | estimator 42.5%, WB 0.040 |
| K25 | the SLACS "flatness" claim | mean 0.000, scatter Δχ² = 6.35 |
| K26 | SPARC-κ vs SLACS-B with the prior | 2.36σ; κ needed 0.4928 (+4.5σ) |
| K27 | the convention trap | 0.499983 / 0.413719, same distance |
| K28 | the (κ, B) posterior: covariance and correlation | σ(lnB) 0.03155, corr −0.255 |

**Mutations:** 16 (`imf_prior`, `kappa_de`, `newton`, `no_boot`, `u_prior`, `closure_4pi`,
`kappa_in_E`, `floor10`, `treu`, `cluster_a`, `drop_gal`, `drop_lens`, `b_marg`, `est_span`,
`closure_kernel`, `err045`), each changing one input, each exit **1**, each breaking a named check;
**28/28 checks are killed by at least one** (matrix in `MUTATE.md`). No check had to be deleted.

## 10. What this does not do

1. **It does not re-derive the declared systematics.** The 20.8% estimator half-span is A51's
   measurement of a 7-estimator ensemble; two of its endpoints are verified here (3% and 10% floors)
   but the ensemble itself is not re-run. Neither is the 16.1% distance floor.
2. **It does not model the SLACS shape residual.** The R_E/R_e trend (+0.172 ± 0.060) carries
   Δχ² = 6.35 of κ information that is degenerate with Sérsic n; this lane reports it and refuses to
   use it. That is conservative for κ and it is the largest un-modelled term in the lensing channel.
3. **The cluster channel is circular.** `u` and `R_req` both come from CFG687's amplitudes. Removing
   the channel moves κ from 0.3777 to 0.3715 — inside the statistical error, so nothing here depends
   on it, but it is not an independent measurement and is not counted as one.
4. **`B` is one number for 70 lenses of one survey.** The cross-method IMF spread is 0.103 dex
   (A70's τ), three times the 0.036 prior used here. With that width the IMF pull is 0.86σ and the
   global tension is 1.23 (0.61σ) — the `imf_prior` mutation. **The lane's only 2σ statement is a statement
   about the IMF error model.**
5. **The wide-binary forecast is a rescaling of A24's numbers**, not a new solve: σ(γ) ∝ N^-1/2 from
   A24's 2,223-pair bin, and the EFE-present κ-sensitivity is a leading-order rescaling of A24's
   1.1811 by √ν(y_ext(κ)), not a re-run of the quadrature.
6. **No new data.** Nothing downloaded; every file is read-only and hashed.

---

## VERDICT

**One parameter set fits all three channels at 1.89σ, and the fit is κ = 0.3777 ± 0.0258 (stat) ±
0.1179 (syst) = 0.3777 ± 0.1207, B = 1.1916 ± 0.0364, u = 0.4427 — with no channel pulled in κ
(SPARC −0.61σ, clusters +0.37σ, the SLACS ridge +1.97σ) and the whole of the global tension
(T = 5.69 for 2 dof) sitting in one place: the joint fit needs an IMF normalisation 1.97σ above
Treu's 1.00 ± 0.036 dex, which is outside his 95% bound of 1.177, and this is worse than A70's 1.80σ
because SPARC's low κ demands an even heavier IMF.** κ = ½ is inside the joint 95% region for the
**canonical a0 = 9.36e-11 at 0.30σ in total (1.40σ statistical)** and for the **P3 a0 = 1.1312e-10 at
1.01σ in total but 4.74σ statistically** — the two differ by 1/√Ω_Λ = 1.2085, the record uses both,
and the two footings are 3.35σ apart at the joint precision; the statistical side of that statement is carried
by SPARC (18.13 of the 47.23 Δχ² at the theory's own point), and the residual pull toward higher κ is
SLACS's mass normalisation, not a0. **The single most valuable next measurement is a wide-binary γ_v
at 18–22 kAU (Gaia DR4, ~30,000 pairs over 2–30 kAU): σ(κ) = 0.040, joint error 0.1207 → 0.0605,
with no Υ, no IMF and no distance ladder in the measurement — and it doubles as A24's 4.5σ test of the EFE;
more SPARC galaxies, by contrast, are worth 2% and should not be bought.**
