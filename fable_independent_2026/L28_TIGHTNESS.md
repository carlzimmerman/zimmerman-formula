# L28 — the tightness claim, attacked

`L28_tightness.py` / `L28_tightness.out`. **29 checks, 14 FAIL.**

The claim under test is HANDOFF_CONTRACT **A17** / L16, the only substantive empirical claim the programme
still has: *"with zero free parameters on each side, the framework's kernel at fixed a₀ describes SPARC
rotation curves more tightly than an abundance-matched ΛCDM halo does: 0.142 dex against 0.171 dex, and
0.198 dex once the halo population's own M₂₀₀ and concentration scatter is switched on."*

**It reproduces exactly, and it does not survive as stated.** The number is right; the sentence around it
is not. What survives is narrower, and is a statement about *prediction*, not about fit quality.

## The fair statement

> On the 155 SPARC galaxies and 2786 points that survive the standard accuracy cut, the framework's kernel
> with a₀ frozen and Υ\* frozen — nothing fitted per galaxy — reproduces log₁₀ g_obs to **0.142 dex**, against
> **0.171 dex** for an NFW halo whose M₂₀₀ and c are *predicted* by abundance matching and **0.198 dex** for a
> random draw from that halo population; the advantage is stable across nine selections (ratio 1.20–1.37),
> holds for all three candidate readings of the frozen kernel on both a₀ footings, survives out of sample in
> both directions, and sits at **1.05× the scatter the quoted observational errors alone would produce**, so
> there is almost no room left in it. It is **not** a demonstration that the kernel beats ΛCDM and must not
> be written as one: abundance matching predicts a halo *population*, never an individual rotation curve, and
> allowed to do what it does claim — each galaxy's halo lying somewhere in a population of width 0.25 dex in
> log M₂₀₀ and 0.11 dex in log c — a fitted NFW halo reaches **0.085 dex**, comfortably tighter than the
> kernel, with a within-galaxy shape residual of 0.070 dex that is a dead heat with the kernel's 0.072 dex.
> The kernel's real and defensible content is therefore predictive rather than descriptive: it delivers that
> shape-channel performance with **zero** parameters per galaxy where the halo needs two, and at equal
> per-galaxy freedom it wins every held-out comparison — fitted on half of each curve it predicts the other
> half to 0.079 / 0.115 dex against the halo's 0.129 / 0.117 with the same nuisances *plus* M₂₀₀ and c.

## Scatter table — every variation

rms of log₁₀ g_obs − log₁₀ g_pred, same points on both sides throughout.

### Zero parameters per galaxy (L16's comparison, reproduced)

| model | par/galaxy | rms [dex] |
|---|---|---|
| framework kernel, a₀ = 1.1279e-10 (alt) | 0 | **0.1421** |
| framework kernel, a₀ = 9.3619e-11 (canonical) | 0 | 0.1453 |
| abundance-matched NFW halo (Moster+2013 × Dutton–Macciò 2014) | 0 | **0.1711** |
| the same halo population with its 0.25 / 0.11 dex scatter switched on | 0 | **0.1980 ± 0.0077** |
| cosmic-ratio halo (lower bound) | 0 | 0.2449 |
| one global free a₀ (log a = −9.9455) | 1 global | 0.1421 — the frozen a₀ buys nothing back |

### Per-galaxy fits — the like-for-like attack

| model | par/galaxy | rms [dex] |
|---|---|---|
| halo, M₂₀₀+c within ΛCDM priors (0.25 / 0.11 dex) | 2 | **0.0659** |
| halo, M₂₀₀+c free | 2 | 0.0599 |
| halo, M₂₀₀+c+Υ+offset with priors | 4 | 0.0520 |
| kernel, Υ+offset with priors | 2 | 0.0602 |
| kernel, Υ+offset free | 2 | 0.0513 |

### The width-matched halo — the decisive fair test

The prior-constrained fit reaches 0.066 dex only by landing on a halo population **1.7× / 1.8× wider** than
ΛCDM's own (fitted sd 0.426 dex in log M₂₀₀ against a predicted 0.25; 0.200 against 0.11; F1d FAILS). Shrink
the priors until the *fitted population* has ΛCDM's width and read off the tightness there:

| prior shrink | σ_M | σ_c | fitted sd(log M) | fitted sd(log c) | rms [dex] |
|---|---|---|---|---|---|
| 1.0 | 0.250 | 0.110 | 0.426 | 0.200 | 0.0659 |
| 2.0 | 0.125 | 0.055 | 0.306 | 0.144 | 0.0743 |
| 3.0 | 0.083 | 0.037 | 0.246 | 0.115 | 0.0828 |
| 6.0 | 0.042 | 0.018 | 0.162 | 0.072 | 0.1037 |
| ∞ | 0 | 0 | 0 | 0 | 0.1711 ← returns the zero-parameter halo, an internal control |

**Interpolated: a fitted halo population carrying ΛCDM's own width reaches 0.082–0.085 dex.** The comparison
is conservative towards ΛCDM (MAP estimates carry estimation noise *on top of* the true population scatter,
so matching the fitted width to the predicted width lets the true width be smaller still). This is the number
that kills the claim as stated.

### Held-out prediction — the criterion that needs no convention

| model | fit inner → score outer | fit outer → score inner |
|---|---|---|
| framework kernel, 0 par | **0.1181** | 0.1538 |
| abundance-matched halo, 0 par | 0.1730 | 0.1617 |
| halo, 2/gal (ΛCDM priors) | 0.1289 | **0.1172** |
| halo, 2/gal (width-matched) | 0.1290 | 0.1270 |
| halo, 2/gal (free) | 0.1591 | 0.1237 |
| halo, 4/gal (priors) | 0.1182 | 0.1205 |
| kernel, 2/gal (priors) | **0.0793** | **0.1145** |

133 galaxies, 1319 / 1375 held-out points. At **zero** parameters both sides the kernel wins both directions
(F2e PASS). At **equal freedom** the kernel wins both directions against a halo carrying the same nuisances
*plus* M₂₀₀ and c (F2d PASS). At zero-versus-two the halo wins the outer→inner direction (F2b, F2c FAIL).

### Error budget

| | observed | floor | obs/floor | excess (quad) |
|---|---|---|---|---|
| kernel, SPARC's quoted errors | 0.1421 | 0.1349 | **1.05** | 0.045 |
| abundance-matched halo, quoted errors | 0.1711 | 0.1288 | 1.33 | 0.113 |
| kernel, distance errors ×0.6 (h117D) | 0.1421 | 0.1154 | 1.23 | 0.083 |
| halo, distance errors ×0.6 | 0.1711 | 0.1082 | 1.58 | 0.133 |

The kernel is **at** its floor; the halo is not. The two floors differ by only 0.006 dex, so the floor is not
what separates the observed numbers. Cross-checked against `hunt_2026/h117_rar_intrinsic_scatter.py`: on the
Lelli cut (Q≤2, i≥30, eV/V<0.10) both scripts select **the same 2684 points**, and h117's 0.1327 / 0.1326 dex
(canonical / alt) sits within 0.0035 dex of this lane's 0.1362 / 0.1319 — two independent loaders, same
answer (C5 PASS).

### The two channels (h117's split)

| model | between-galaxy | within-galaxy (shape) |
|---|---|---|
| framework kernel, a₀ fixed, 0 par | 0.1505 | **0.0718** |
| abundance-matched halo, 0 par | 0.1582 | 0.0944 |
| halo + 2/gal, width-matched | 0.0667 | **0.0701** |
| halo + 2/gal, ΛCDM priors | 0.0325 | 0.0612 |
| kernel + 2/gal, priors | 0.0286 | 0.0581 |

Against the *predicted* halo the kernel wins both channels (shape by 1.32×). Against the *width-matched
fitted* halo the shape channel is a dead heat, 0.0718 against 0.0701 — the halo marginally ahead, with two
parameters per galaxy against the kernel's zero.

### Selection

| cut | Ngal | Npt | kernel | halo | ratio | halo+2 | kern+2 |
|---|---|---|---|---|---|---|---|
| L16 baseline (Q≤3, no i cut, ≥3 pts, eV/V<0.10) | 155 | 2786 | 0.1421 | 0.1711 | 1.20 | 0.0659 | 0.0602 |
| Lelli+2016/17 (Q≤2, i≥30) | 141 | 2684 | 0.1319 | 0.1637 | 1.24 | 0.0631 | 0.0582 |
| Q≤1 only | 95 | 1820 | 0.1292 | 0.1673 | 1.29 | 0.0594 | 0.0596 |
| i ≥ 45° | 128 | 2417 | 0.1395 | 0.1724 | 1.24 | 0.0681 | 0.0613 |
| ≥ 6 points | 133 | 2694 | 0.1375 | 0.1673 | 1.22 | 0.0648 | 0.0594 |
| ≥ 10 points | 100 | 2449 | 0.1356 | 0.1677 | 1.24 | 0.0643 | 0.0583 |
| eV/V < 0.05 | 113 | 1946 | 0.1186 | 0.1603 | 1.35 | 0.0476 | 0.0420 |
| no accuracy cut | 175 | 3382 | 0.1912 | 0.2374 | 1.24 | 0.1281 | 0.1137 |
| strictest stack | 94 | 1860 | 0.1183 | 0.1618 | 1.37 | 0.0468 | 0.0419 |

The zero-parameter ratio is stable at 1.20–1.37 (F4 PASS). The *equal-freedom in-sample* margin is only
0.006 dex and **reverses** on the Q≤1 cut (0.0596 against 0.0594) — a tie, not a win (F4c FAIL). Only the
held-out version of the equal-freedom statement survives.

### Which kernel, both footings

The two governing documents disagree (HANDOFF_CONTRACT D1), and L6/L16 code a *third* thing — ν_RAR with the
boost held at its maximum 0.6476 a₀ above y = 2.540 instead of dying. On these data that saturation touches
342 of 2786 points and moves them by at most 0.0092 dex, so the coded kernel and ν_RAR are the same model
here; the exponential carrier differs from ν_RAR by up to **0.0726 dex** (rms 0.045), independently
confirming the 0.073 dex D1 quotes.

| kernel | footing | rms | vs halo 0.1711 | vs halo+2 fitted |
|---|---|---|---|---|
| saturated (L6/L16 coded) | alt | 0.1421 | 1.20× | 0.46× |
| saturated | canonical | 0.1453 | 1.18× | 0.45× |
| ν_RAR (THE_ACTION §3) | alt | 0.1421 | 1.20× | 0.46× |
| ν_RAR | canonical | 0.1453 | 1.18× | 0.45× |
| exp carrier μ = 1−e^(−y) (RECIPE I1) | alt | 0.1507 | 1.14× | 0.44× |
| exp carrier | canonical | **0.1613** | **1.06×** | 0.41× |
| "simple" μ (external yardstick) | alt | 0.1422 | 1.20× | 0.46× |

The advantage over the zero-parameter halo holds everywhere (F5a PASS). **But D1 is not cosmetic for this
claim** (F5c FAIL): the kernel/footing spread is 0.019 dex against a kernel–halo gap of 0.029 dex, so which
document is authoritative moves two thirds of the effect being argued. On the recipe's own frozen kernel at
the canonical footing the margin is 1.06×, not 1.20×. **The user's D1 call has to be made before this is
written up.**

## The PASS/FAIL lines

```
[PASS] C1  L16's fixed-a_0 kernel scatter 0.142 dex reproduces
[PASS] C2  L16's abundance-matched halo scatter 0.171 dex reproduces
[PASS] C3  L16's halo-population-scatter number 0.198 dex reproduces
[PASS] C5  an INDEPENDENT script (h117) gets the same parameter-free scatter on the same cut, <0.005 dex
[PASS] C4  the FROZEN a_0 is not a hidden per-sample fit
[FAIL] F1d the fitted halo population is no broader than the LambdaCDM population it was drawn from
[FAIL] F1a the zero-parameter kernel is tighter than a halo floating within its REAL priors
[FAIL] F1b ... and tighter than a FREELY fitted NFW halo
[PASS] F1c at the SAME two prior-constrained parameters per galaxy, the kernel is tighter
[FAIL] F1e [DECISIVE] ... tighter than a fitted halo population carrying LambdaCDM's OWN width
[FAIL] F2a with the parameter count charged for (BIC), the zero-parameter kernel is preferred
[FAIL] F2b the zero-parameter kernel out-predicts ANY fitted halo, both directions
[FAIL] F2c fit outer, predict inner: the zero-parameter kernel beats a freely fitted NFW
[PASS] F2e held-out, zero parameters both sides: kernel beats halo in both directions
[PASS] F2d held-out at EQUAL FREEDOM: kernel+2 beats halo+2 and halo+4, both directions
[PASS] F3a the kernel's residual is AT the observational error floor (1.05x)
[PASS] F3b the halo's residual is NOT at its floor, so the two are distinguishable
[PASS] F3d against the PREDICTED halo the advantage is in both channels
[FAIL] F3e ... the SHAPE-channel advantage survives against a width-matched FITTED halo
[PASS] F4  the zero-parameter kernel is tighter than the zero-parameter halo under EVERY cut
[FAIL] F4b ... and still tighter than the prior-constrained FITTED halo under every cut
[FAIL] F4c at equal freedom the kernel is tighter under every cut (reverses on Q<=1)
[PASS] F5a the advantage over the zero-parameter halo holds for all three kernels, both footings
[FAIL] F5b ... and over the prior-constrained fitted halo
[FAIL] F5c the D1 documentation conflict does not matter for this claim
[FAIL] V1  the tightness claim is publishable AS STATED
[PASS] V2  the CONDITIONED zero-parameter claim survives every attack in this lane
[FAIL] V3  the equal-freedom claim survives in-sample AND out-of-sample AND across cuts
[PASS] V4  the PREDICTIVE equal-freedom statement survives, in both directions
```

## What this does to A17

`HANDOFF_CONTRACT` A17's second sentence — *"What survives: at zero free parameters the fixed-a₀ kernel is
still tighter than the halo — 0.142 dex vs 0.171, and 0.198 with halo-population scatter"* — is **numerically
correct and reproduces to the fourth decimal**, but it needs the condition attached that the halo's
parameters were *predicted, not fitted*, and it needs the counterweight that a ΛCDM-width fitted halo reaches
0.085 dex. Suggested replacement wording for A17:

> **A17′.** With nothing fitted per galaxy the kernel reaches 0.142 dex against 0.171 for an
> **abundance-matched** halo and 0.198 for a draw from that population; the advantage is cut-stable
> (1.20–1.37×), kernel- and footing-robust, survives out of sample, and sits at 1.05× the observational error
> floor. **Against a *fitted* halo it does not hold**: a halo population carrying ΛCDM's own 0.25 / 0.11 dex
> width reaches 0.085 dex, and its shape-channel residual ties the kernel's. The surviving claim is
> predictive: at equal per-galaxy freedom the kernel predicts held-out halves of rotation curves better than
> an NFW halo does (0.079 / 0.115 dex against 0.129 / 0.117), and it needs two fewer parameters per galaxy to
> reach the same shape accuracy.

Two consequences for the programme:

1. **This is not a ΛCDM-versus-framework discriminant and must never be published as one.** It is a
   parsimony/predictivity argument, which is the argument MOND has always actually had. `h117` reached the
   same place from the other side: in the channel where the two theories differ they are degenerate at 0.1σ.
2. **D1 must be resolved before publication.** The exponential carrier at the canonical footing gives 1.06×,
   not 1.20×. Which kernel is frozen changes two thirds of the margin.

Everything here is `L28_tightness.py`; nothing was taken on trust from L16 beyond its loader conventions,
which were re-derived and re-checked against an independent script (C5).
