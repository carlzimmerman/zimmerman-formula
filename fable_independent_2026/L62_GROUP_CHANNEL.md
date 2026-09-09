# L62 — the group channel: it cannot decide, and the reason is structural

2026-09-09. Lane L62. Script: [`L62_group_channel.py`](L62_group_channel.py) →
[`L62_group_channel.out`](L62_group_channel.out). **24 checks, 10 PASS / 14 FAIL; all 8 controls PASS.**
Both a₀ footings (9.3619e-11 / 1.1279e-10 m s⁻²) on every dimensional number. 42 s.

L57 left the nonlocal (smoothed-density) trigger **undecidable on current data** and named two open channels
rather than banking either. This lane settles the one existing measurements could plausibly close: **X-ray
groups**, where L57 E3 predicts a 20–45% lensing-versus-hydrostatic mass discrepancy and refused to score it
because this repository's own group estimators disagree by more than the effect.

Method: nothing under `closure_2026/` or the lead agent's directories was imported or executed. The
Whittle–Matérn kernel tower, the spherical convolution, the projection integrals and the group model were
rebuilt in this file. L57's group band, the 9σ shear failure, the measured cluster mass ratio and L56's
convention-free crux are **re-derived as controls, not inherited**. The literature numbers were found by
search and are quoted with their samples and uncertainties.

---

## The verdict, first

**The group channel cannot decide, and it cannot be made to decide by a better measurement of the same
observable.** Three separate things close it, and only the first is about precision.

1. **The predicted band is smaller than the measurement's calibration floor.** The best existing group-scale
   lensing-to-hydrostatic ratio is **1.34 ± 0.20 (stat)** (Umetsu et al. 2020, 105 XXL systems). The
   **common-mode** systematic floor is **17.3%** using only literature-quoted entries and **28.0%** on the
   full stated budget. Seeing the bottom of the band at 3σ needs **5.9%** total. The band lies entirely
   inside the errors — **0.42–0.62σ**, nothing excluded at even 1σ.
2. **It is systematics-limited, so more groups do not help.** The floor is common-mode — one shear
   calibration, one photo-z calibration, one Chandra-versus-XMM offset, one halo model applied to every
   system — and does not average down. At N = 105 the wrong (independent-error) treatment would claim 2.7%
   and "exclude" the whole band at 6.5σ; the right treatment gives 28.1% and excludes nothing. **That factor
   of 10.3 is the fourth burn this lane was told not to add, and it is written into the script as a check.**
3. **And a perfect measurement still would not decide it, because the ΛCDM baseline for that ratio is not
   1.00.** Non-thermal pressure biases hydrostatic masses low: FLAMINGO gives b_HSE ≈ −0.10 at group mass,
   i.e. an expected **M_WL/M_HSE ≈ 1.11 with no new physics**, and Kettula et al. 2013 infer 1.3–1.5 at
   1 keV from the data themselves. **A metric slip and a hydrostatic bias enter this observable with the
   same sign and overlapping magnitude.** The measured value sits 1.29σ from unity, 0.87σ from the ΛCDM
   baseline and 0.21σ from the mechanism's median. Improving the measurement does not separate them.

**The pincer.** The one route that would *not* be degenerate is lensing against a **collisionless** tracer —
galaxy kinematics, caustics, the escape edge — where ΛCDM predicts exactly 1.00. That is precisely the route
whose estimator is worst at group mass: **≥ 20% substructure bias at ≤ 10^13.5 M⊙** and recovered-mass
scatter rising toward an order of magnitude below 10^14 M⊙ (Old et al. 2015, 2018). **The precise channel is
degenerate; the degeneracy-free channel is imprecise.** That, not sample size, is what closes the group
channel as a decider.

**So the mechanism survives this channel** — in the same weak sense L57 left it: nothing measured excludes
it. Its length is still fitted, its operator order is still fitted, its weight is still a free function, and
at its ceiling it still halves the 9σ rather than curing it. **Nothing in this lane makes it more likely to
be right**, and one adjacent number (D4) runs against it.

---

## 1. Controls (A1–A6, C3, E1 — eight, all PASS)

| control | L57 / L51 | here |
|---|---|---|
| A1 L57's group band, read from its own `.out` | 21.5–45.0%, median 30.8%, n4 at ℓ_rms = 1 Mpc | read back verbatim |
| A2 the kernel tower and spherical convolution, rebuilt | — | ∫K d³r = 1 to 5e-15, rms = ℓ√(6n) to 2e-16, uniform fixed point 1.2e-5 |
| A3 the suppression law | q = 0 / 2 / 3 for n = 1 / 2 / ≥3 | **q = −0.00 / 1.99 / 3.00**, and the end-to-end convolution of a compact source agrees to 0.017 |
| A4 the 9σ shear-shape failure | +0.516 ± 0.058 / +0.521 ± 0.058 | **+0.516 ± 0.059 (8.8σ) / +0.521 ± 0.058 (8.9σ)** |
| A5 the measured cluster `M_WL/M_HSE` | 1.148 ± 0.146 | **1.148 ± 0.146** |
| A5b L56's crux `M_P/M_fw` | 0.803 / 0.666 | **0.806 / 0.669** |
| A6 L57's group response, recomputed | 21.5–45.0%, median 30.8% | **21.6–45.2%, median 30.9% — worst deviation 0.5%** |
| C3 the correlated-error trap | — | the floor is common-mode; the wrong treatment inflates significance by 10.3× at N = 105 |
| E1 a real per-object lensing-vs-dynamics comparison | — | 74 SLACS lenses, median M_Ein/M_SIS = 1.109, 27% per-lens scatter |

**A6 is the load-bearing control**: the band this lane confronts was rebuilt from the Lovisari 2015
catalogue with this file's own kernel, its own X-COP smoothing and its own reference response, and it lands
on L57's published band to **0.5%**. Both footings: canonical **21.6–45.2%**, alt **17.7–37.2%**, so the
band used throughout is **18–45% (median 28%)** — slightly wider at the bottom than L57's canonical-only
20–45%.

**One caveat that runs FOR the mechanism and is recorded as such.** L57's group model is a stated isothermal
sphere normalised to `M_gas500 × 1.30`, chosen because it *maximises* the group's own trigger gradient. The
20–45% band is therefore an **upper bound** on the prediction. A smaller true prediction makes the channel
less decisive, not more.

---

## 2. What is actually measured for groups (B1–B3)

Fourteen published entries are carried in the script with sample, mass range, quoted uncertainty and a note.
**Nothing is averaged across them** — they measure different things with different estimators, and combining
them would be exactly the error this repository has been burned by. The load-bearing ones:

| source | what | value | sample |
|---|---|---|---|
| **Umetsu et al. 2020** (ApJ 890, 148) | WL mass vs the X-ray T–M relation | **mean mass offset 34 ± 20% (1.5σ)** | 105 XXL systems, 0.031 < z < 1.033 |
| **Kettula et al. 2013** (ApJ 778, 74) | hydrostatic bias vs temperature | **30–50% at 1 keV**, no uncertainty quoted | 10 COSMOS groups + 55 clusters; individual WL masses 20–40% |
| **Kugel et al. 2024** (FLAMINGO) | ΛCDM baseline | **b_HSE ≈ −0.10 at group mass**, −0.20 at cluster mass; σ(b) ≈ 0.1 at 10^14 rising rapidly | simulation |
| **Schellenberger et al. 2015** (A&A 575, A30) | instrument systematic | **M_HSE(Chandra) = 1.14 ± 0.02 × M_HSE(XMM)** | 64 HIFLUGCS clusters |
| **George et al. 2012** (ApJ 757, 2) | lensing systematic | stacked group WL masses biased low by **5–30%** with a wrong centre | X-ray groups |
| **Old et al. 2015 / 2018** | dynamical estimator | scatter ≈ ×2 above 10^14, rising toward an **order of magnitude** below; substructure **bias ≥ 20% at ≤ 10^13.5** | mocks, 25 techniques |
| **Viola et al. 2015** / GAMA+HSC 2022 | WL mass vs σ | **M ∝ σ^1.89±0.27** and **M ∝ σ^1.52±0.10** against the virial σ³ | GAMA groups (1587 with ≥ 5 members) |
| **Logan et al. 2022** (arXiv:2202.08569) | HSE vs caustic | **M_X/M_C = 1.12 (+0.11/−0.10)**, systematics 10–15% both sides | 14 clusters, ≥ 210 members each |
| **arXiv:2507.20938** (2025) | lensing vs escape-velocity mass | **0.02 ± 0.02 dex** | 46 clusters, log M = 14.4–15.4 — *cluster*, not group |
| this repo (L57 E3's own reason) | estimator spread | **+0.42 dex** | 19 shared group hosts, KT2017 vs g06 |

- **B1 PASS.** A direct group-scale lensing-to-hydrostatic ratio *does* exist, with a quoted uncertainty.
  The XXL sample spans groups *and* clusters, so a group-only number is weaker than the one quoted, not
  stronger.
- **B2 FAIL.** A direct group-scale **lensing-to-galaxy-dynamical** ratio to better than 20% total **does
  not exist**. The one precise collisionless-tracer comparison is an order of magnitude above group mass,
  and the two group-scale lensing-versus-σ relations disagree with the virial expectation and with each
  other in slope by more than a factor of two.
- **B3 FAIL, and it is the most important line in the lane.** The ΛCDM baseline for this ratio is **not 1**.

---

## 3. The systematic floor (C1–C4)

Every entry is classified **COMMON-MODE** (a calibration or modelling choice shared by every system in a
sample — does not average down) or **per-system** (does). Entries are marked `[lit]` where a literature value
is quoted and `[stated]` where this lane supplied a conservative placeholder, and **the floor is quoted both
with and without the placeholders** so that no conclusion rests on a number this lane made up.

| side | entry | % | mode | class |
|---|---|---|---|---|
| WL | shear multiplicative calibration | 2 | common | `[lit]` HSC-Y1 / KiDS-1000 budgets |
| WL | photo-z / Σ_crit | 5 | common | `[stated]` |
| WL | miscentring residual | 10 | common | `[lit]` George+2012, 5–30% uncorrected |
| WL | halo model: concentration, 2-halo, triaxiality | 8 | common | `[stated]` |
| WL | selection / Eddington bias on X-ray-selected groups | 10 | common | `[stated]` |
| HSE | Chandra vs XMM cross-calibration | 14 | common | `[lit]` Schellenberger+2015 |
| HSE | ICM modelling at ~1 keV | 10 | common | `[stated]` |
| HSE | extrapolation to R500 | 12 | common | `[stated]` |
| HSE | clumping / asphericity | 7 | common | `[stated]` |
| both | projection / triaxiality per system | 25 | **per-system** | `[lit]` |

**Literature-only common-mode floor: 17.3%. Full stated budget: 28.0%.**

- **C1 FAIL.** 3σ on the bottom of the band needs **5.9%**; the literature-only floor alone is **2.9× that**.
- **C2 FAIL.** 3σ on the *top* of the band needs 15.1%; the literature-only floor is already above it.
- **C3 PASS (control), and it is the anti-burn check.** With N = 105, treating the floor as independent
  would claim 2.7% and "exclude" the band at 6.5σ. The correct treatment gives 28.1%. **Factor 10.3.**
- **C4 FAIL.** Statistical 20% against a floor of 17–28%: the comparison is **systematics-limited**. Every
  future sample shrinks the statistical term and leaves the floor exactly where it is.

---

## 4. The confrontation (D1–D5)

    measured:   M_lens/M_dyn - 1  =  34%  +/- 20% (stat)  +/- 17% to 28% (common-mode sys)
                                  =  34% +/- 26% (lit floor)   or   34% +/- 34% (full budget)
    predicted:  18% - 45%  (median 28%), both footings

| the same measurement against | separation (lit floor) |
|---|---|
| no slip **and** no hydrostatic bias (ratio 1.00) | 1.29σ |
| **ΛCDM hydrostatic bias alone** (FLAMINGO, 1.11) | **0.87σ** |
| the mechanism's median (1.28) | 0.21σ |

- **D1 FAIL — the group data do NOT exclude the mechanism.** 0.42–0.62σ. The measured central value in fact
  sits *inside* the predicted band, which is **not** evidence for the mechanism, because that is also where
  the astrophysical hydrostatic bias puts it.
- **D2 FAIL — and this closes the hydrostatic route independently of precision.** Slip and hydrostatic bias
  are the same observable with the same sign. **Zero measurement error would not decide it.**
- **D3 FAIL — the pincer.** The collisionless route has the statistics already (103 groups suffice for 3σ on
  18% at 60% per-system scatter; DESI-class surveys have 10⁴–10⁵), but carries a **20% common-mode estimator
  bias at 10^13.5 M⊙**, calibrated only against mocks whose galaxy-formation physics is an assumption.
- **D4 FAIL — an adjacent number that runs AGAINST the mechanism, reported because the standard is both
  directions, and NOT BANKED.** L51/L57's gate 1 — the constraint that actually caps the lensing phantom —
  uses the cluster-scale ratio 1.148 ± 0.146, which is `M_WL/M_HSE`. The cleaner collisionless comparison
  (0.02 ± 0.02 dex → **1.047 ± 8.8%** with a 7.5% method systematic) would move the cap from **f ≤ 0.73
  (4.9σ)** to **f ≤ 0.40 (5.8σ)**. *Not banked*: different sample (46 clusters at log M = 14.4–15.4 versus
  the 5 X-COP hosts), different estimator, and the same paper records the prior caustic comparison off by
  0.25 ± 0.05 dex with essentially zero correlation — two collisionless estimators disagreeing by 0.23 dex
  on overlapping data.
- **D5 FAIL — what would change the verdict, in full.** A group-scale lensing-to-dynamical ratio
  (i) on a **collisionless** tracer, so the ΛCDM baseline is 1.00 rather than 1.11; (ii) to better than
  **5.9% total**; (iii) with that tracer's own estimator bias **validated below 5.9%** against Old+2018's
  20% at 10^13.5 M⊙. **All three are required. None is met today, and (iii) is the blocker** — the
  statistics already exist.

---

## 5. The decisive test L57 named, priced against a real catalogue (E1–E4)

L57 E4 predicts **0.024%–2.3%** for galaxies at cluster radii against essentially none in the field, and
calls it decidable at **0.1%**. The best existing per-object lensing-versus-dynamics measurement is
strong lensing, so the price was taken from the SLACS catalogue on disk (Auger et al. 2009) rather than
asserted: **74 lenses, median M_Ein/M_dyn(SIS) = 1.109, 27% per-lens scatter.** That 27% is crude — a bare
isothermal sphere on the raw SDSS fibre σ with no aperture correction and no Jeans model — so **every
number below uses the optimistic 10%** a proper joint analysis reaches (Barnabè et al. 2011, ~5% intrinsic
slope spread). *A conclusion that survives the optimistic scatter is the only one worth stating.*

| target | matched lenses needed (3σ) at 27% | at 10% |
|---|---|---|
| top of the band, 2.3% | 2 507 | **340** |
| **L57's stated 0.1%** | 1 326 397 | **180 000** |
| bottom of the band, 0.024% | 2.3e7 | 3.1e6 |

Available: Collett 2015 forecasts 2 400 (DES), 120 000 (LSST), 170 000 (Euclid) galaxy-galaxy strong lenses.
A generous 5% in cluster environments gives **≈ 14 500** cluster-arm lenses.

- **E2 FAIL — no existing or approved survey reaches 0.1%.** Short by **12×** in sample (91× on the crude
  scatter), and — decisively — a matched cluster-versus-field differential has a systematic floor of order
  **1.5%**, **15× the target**, which no sample removes.
- **E3 FAIL (half) — but this is the sharpening the lane can offer.** The absolute lensing-to-dynamical
  calibration of an early-type galaxy is limited at the few-per-cent level by the IMF, the density slope and
  the anisotropy. Those are **population** properties and they cancel in a differential between samples
  matched in σ, R_e, redshift and stellar mass. **The right measurement is not an absolute calibration but**

      < M_Ein / M_dyn >_(lenses in clusters)  -  < M_Ein / M_dyn >_(matched field lenses)

  whose floor is set only by residual cluster-versus-field population differences — age, compactness at
  fixed mass, environmental quenching. **Statistics: yes**, 340 matched lenses against ≈ 14 500 available.
  **Margin: no** — 2.3% is only 1.5× the 1.5% floor, a **1.5σ** measurement at best. So the *top* of the
  band becomes a marginal Euclid/LSST-era test and the rest of the band, four orders of magnitude wide,
  becomes nothing.
- **E4 FAIL — the binding constraint is the floor, not the survey.** The 1.5% is this lane's own `[stated]`
  number, so the conclusion is checked against optimistic values: at a 0.5% floor the target is still out of
  reach by 5×; even assuming the systematics away entirely (0.1% floor), the statistical requirement of
  180 000 matched lenses still exceeds what Euclid+LSST supply by 12×. **The conclusion survives assuming
  the systematics away.** Today's samples do not even have a cluster arm: SLACS's only environment proxy
  flags 3 of 86 lenses.

---

## 6. What this changes in the standing record

1. **L57's refusal to score the group channel was correct, and this lane can now say why.** It is not that
   the estimators happen to be poor: the hydrostatic route is **degenerate with the astrophysical
   hydrostatic bias by construction**, and the degeneracy-free route is **estimator-limited by ≥ 20% exactly
   at group mass**. That pincer is the finding, and it does not lift with better data of the same kind.
2. **Quote the number that would change it, in all three parts:** a collisionless-tracer group-scale
   lensing-to-dynamical ratio, **better than 5.9% total**, with the estimator's own bias validated below
   that at M500 ~ 10^13–10^14 M⊙. The statistics already exist (≈ 100 well-sampled groups suffice); the
   **estimator-bias calibration is the blocker**.
3. **L57's second decisive measurement is not measurable at the precision L57 named.** Galaxies inside
   clusters at 0.1% is 15× below the matched-differential floor and 12× short in sample even at optimistic
   scatter. What *is* proposable is the **matched cluster-versus-field strong-lensing differential**, which
   reaches the 2.3% top of the band at ≈ 1.5σ with Euclid/LSST lens samples. That is a real proposal and a
   weak one.
4. **A liability flagged, not banked (D4).** The framework's gate 1 at cluster scale compares lensing to a
   *hydrostatic* mass, whose ΛCDM expectation is not 1.000 either. The cleaner collisionless cluster-scale
   ratio (1.047) would tighten L51/L57's ceiling from 4.9σ to 5.8σ. Cross-sample and cross-estimator, so it
   is recorded as pressure, not as a result.
5. **The mechanism's status is unchanged: conditionally alive, on no positive evidence.** The group channel
   neither excludes it nor clears it.

---

## 7. Honesty ledger, in both directions

- **Three findings run FOR the mechanism surviving and are recorded as such:** the group data do not exclude
  it (D1); the measured central value sits inside the predicted band; and L57's group model maximises the
  trigger gradient, so the 20–45% band is an upper bound (A6) — a smaller true prediction makes the channel
  even less decisive.
- **Three run against it:** the degeneracy with hydrostatic bias is structural and not fixable by precision
  (D2); the collisionless cluster-scale ratio would tighten the repair ceiling (D4, **not banked**); and the
  environmental test L57 called decisive is not reachable at the precision L57 named (E2).
- **The measured central value sitting inside the predicted band is explicitly NOT counted as support.** It
  is where the astrophysical hydrostatic bias puts it, and the lane says so at D1 and D2.
- **Six of the ten systematic-budget entries are this lane's own conservative placeholders.** They are
  labelled, and the floor is quoted both with and without them; **every conclusion in the lane holds on the
  literature-only floor of 17.3%.**
- **The 1.5% differential floor in Part E is likewise this lane's own number**, and the conclusion is shown
  to survive at 0.5% and even at 0.1%.
- **The 27% SLACS per-lens scatter is a crude estimate that would flatter this lane's conclusion**, so the
  optimistic 10% is used throughout instead.
- **No statement anywhere that data favour this framework over ΛCDM.** The NFW haloes, the concentration
  relation and the FLAMINGO baseline are ΛCDM's, imported.

---

## 8. Scope — what is not done here

- No new group sample was reduced. The group-scale ratio is taken from published measurements; this lane
  computes the **floor** and the **degeneracy**, not a new central value.
- The XXL 34 ± 20% spans groups *and* clusters. A group-only re-analysis would have a larger statistical
  error, not a smaller one, so using it is generous to the test's power.
- The matched cluster-versus-field strong-lensing differential is priced, not forecast in detail: no
  selection-function or lens-modelling simulation was run.
- The cosmological channel L57 left open (0.3% slip on 10 Mpc) is untouched; it is a separate calculation.
- Nothing was written into `PREREGISTRATION_DR4.md`, any `*_HASH.txt`, `FINDINGS.md`, `HANDOFF_CONTRACT.md`
  or anything under `papers_2026/`. No file outside `fable_independent_2026/` was created or modified.

---

## 9. The PASS/FAIL lines

```
[PASS] A1 [control] L57's group prediction, working point and floor are read back verbatim from its own output and are the 20-45% band this lane has to confront   (20 groups, 21% - 45% (median 31%), kernel n4 at l_rms = 1000 kpc)
[PASS] A2 [control] the smoothing machinery built in this file is exact: every kernel is normalised, has rms radius l sqrt(6n), leaves a uniform density exactly where it is, and returns M K(R) for a compact source   (worst normalisation error 5.00e-15, worst rms error 2.22e-16, worst uniform error 1.23e-05, worst point-source error 4.34e-06)
[PASS] A3 [control] the suppression law reproduces: q = 0 for n = 1, q = 2 for n = 2, and q = 3 -- the CUBE of the scale ratio -- for every n >= 3 and for the Gaussian, so no kernel order and no length beats (R_p/r_cl)^3.  Checked twice: from K'(r) analytically, and end-to-end through the full convolution of a compact source   (q = gauss 3.00, n1 -0.00, n2 1.99, n3 2.99, n4 3.00, n6 3.00; the end-to-end convolution exponents agree to 0.017)
[PASS] A4 [control] the 9-sigma cluster shear-shape failure reproduces independently (L51 C2 / L56 A3 / L57 A2: +0.516 +/- 0.058 canonical, +0.521 +/- 0.058 alt)   (canonical +0.516 +/- 0.059 (8.8 sigma), alt +0.521 +/- 0.058 (8.9 sigma))
[PASS] A5 [control] the measured cluster lensing/hydrostatic mass ratio reproduces   (1.148 +/- 0.146)
[PASS] A6 [control] L57's group prediction is reproduced independently -- this file's own kernel, own X-COP smoothing, own reference response -- to better than 10%   (canonical 21.6% - 45.2% (median 30.9%) against L57's 21.5% - 45.0% (median 30.8%); worst deviation 0.5%. Alt footing 17.7% - 37.2% (median 25.4%))
[PASS] B1 [test] a DIRECT published measurement of the lensing-to-hydrostatic mass ratio exists at group scale, with a quoted uncertainty   (YES -- Umetsu+2020 give 1.34 +/- 0.20 (mean mass offset 34 +/- 20 per cent, 1.5 sigma) on 105 XXL systems, and Kettula+2013 give 30-50% at 1 keV on 10 COSMOS groups with no quoted uncertainty.  The XXL sample spans groups AND clusters, so the group-only number is weaker than the one quoted here, not stronger)
[FAIL] B2 [test] a DIRECT published measurement of the lensing-to-GALAXY-DYNAMICAL mass ratio exists at group scale (M500 ~ 1e13 - 1e14 Msun) with better than 20 per cent total uncertainty   (NO -- none was found.  The precise collisionless-tracer comparison (0.02 +/- 0.02 dex) is at log10 M/Msun = 14.4-15.4, an order of magnitude ABOVE the Lovisari groups, and the group-scale dynamical estimator is exactly where Old+2015 finds the recovered-mass scatter rising toward an order of magnitude and Old+2018 finds a >= 20% substructure BIAS at <= 1e13.5 Msun.  The two existing group-scale lensing-vs-sigma relations (Viola+2015 slope 1.89 +/- 0.27, GAMA+HSC slope 1.52 +/- 0.10) disagree with the virial expectation of 3 and with each other)
[FAIL] B3 [test] the LambdaCDM baseline for the group-scale lensing-to-hydrostatic ratio is 1.00, so any measured excess can be attributed to a metric slip   (NO, and this is the single most important fact in the lane.  FLAMINGO gives b_HSE ~ -0.10 at group mass, i.e. an expected M_WL/M_HSE = 1.11 with NO new physics (1.25 at cluster mass); Kettula+2013 infer 1.3-1.5 at 1 keV from the data themselves.  The baseline is therefore uncertain over a range of about 34 percentage points -- comparable to the ENTIRE predicted band of 18-45%.  The two are not merely hard to separate; they are the same observable with the same sign)
[FAIL] C1 [test] the systematic floor, using ONLY literature-quoted entries, is small enough to see the BOTTOM of the predicted band at 3 sigma   (NO -- 3 sigma on a 18% slip needs a total uncertainty of 5.9%, and the literature-only COMMON-MODE floor alone is 17.3%, 2.9x too large.  The bottom of the band is smaller than the irreducible calibration uncertainty of the measurement meant to find it, before a single conservative placeholder is added and before any statistical error)
[FAIL] C2 [test] the full stated systematic floor is small enough to see the TOP of the predicted band at 3 sigma   (NO -- 3 sigma on the top of the band (45%) needs 15.1% total, against a full-budget floor of 28.0% and a literature-only floor of 17.3%.  Even the most favourable corner of the prediction, measured with a perfect statistical sample, sits 1.1x inside the calibration floor)
[PASS] C3 [control] the systematic floor is common-mode and does NOT beat down as 1/sqrt(N); this lane's arithmetic treats it that way   (at the size of the largest existing sample (N = 105, XXL) the wrong treatment would claim 2.7% and 'exclude' the whole band at 6.5 sigma; the right treatment gives 28.1%, which excludes nothing.  That factor of 10.3 IS the fourth burn this lane was told not to add)
[FAIL] C4 [test] the group comparison is STATISTICS-limited, so that a bigger sample would decide it   (NO -- it is SYSTEMATICS-limited.  Statistical 20% against a common-mode floor of 17.3% (literature only) to 28.0% (full budget).  The two are already comparable at N = 105, and every future sample makes the statistical term smaller while leaving the floor exactly where it is.  More groups do not decide this channel)
[FAIL] D1 [test] the predicted 20-45 per cent slip lies OUTSIDE the measured group ratio's total uncertainty -- i.e. the group data EXCLUDE the mechanism   (NO -- the band is INSIDE the interval on both floors.  The bottom of the band is 0.62 sigma from the measured value and the top is 0.42 sigma, using the more generous literature-only floor.  Nothing is excluded at even 1 sigma.  The measured central value (34%) in fact sits INSIDE the predicted band -- which is NOT evidence for the mechanism, because that is also where the astrophysical hydrostatic bias puts it (D2))
[FAIL] D2 [test] the predicted slip is SEPARABLE from the astrophysical hydrostatic bias in this observable   (NO -- and this closes the hydrostatic route independently of any precision argument.  A metric slip and a non-thermal-pressure hydrostatic bias enter M_WL/M_HSE with the SAME SIGN and OVERLAPPING magnitude (18-45% predicted against 11% from FLAMINGO and 30-50% inferred by Kettula+2013).  The measured value is 1.29 sigma from unity, 0.87 sigma from the LambdaCDM baseline and 0.21 sigma from the mechanism's median.  Improving the measurement to zero error would NOT decide it, because the baseline it must be compared against is itself uncertain by about the size of the effect)
[FAIL] D3 [test] a degeneracy-free group channel (lensing versus a COLLISIONLESS tracer) exists at the precision the test needs, today   (NO -- the statistics are already there (103 groups suffice for 3 sigma on 18% at 60% per-system scatter, and DESI-class surveys have 10^4-10^5 groups), but the estimator BIAS is 20% at 1e13.5 Msun (Old+2018), common-mode, and calibrated only against mock catalogues whose galaxy-formation physics is an assumption.  The precise channel is degenerate and the degeneracy-free channel is imprecise.  That pincer, not the sample size, is what closes the group channel as a DECIDER)
[FAIL] D4 [test] an independent, collisionless-tracer, cluster-scale lensing-versus-dynamics measurement leaves L51/L57's 4.9 sigma ceiling unchanged   (NO -- it TIGHTENS it, from f <= 0.73 (4.9 sigma) to f <= 0.40 (5.8 sigma), because 1.047 +/- 8.8% leaves less room for a lensing phantom than 1.148 +/- 0.146 does.  NOT BANKED: different sample (46 clusters at log10 M = 14.4-15.4 vs the 5 X-COP hosts), different estimator, and the same paper records the prior caustic comparison off by 0.25 +/- 0.05 dex with essentially zero correlation.  Recorded because the standard is both directions, and because it says the group channel is not the only place this mechanism is under pressure)
[FAIL] D5 [test] the group channel can be made decisive by an achievable improvement in the measurement   (NOT BY PRECISION ALONE.  To exclude the WHOLE band at 3 sigma the total uncertainty on a group-scale lensing-to-dynamical ratio must reach 5.9% -- 2.9x better than the literature-only common-mode floor and 4.7x better than the full budget -- AND the tracer must be collisionless, so that the LambdaCDM baseline is 1.00 rather than 1.11, AND that tracer's own estimator bias must be validated below 5.9%, against Old+2018's 20% at 1e13.5 Msun.  THAT is the number that would change this verdict, and all three parts of it are required)
[PASS] E1 [control] a real per-object lensing-versus-dynamical mass comparison is available on disk and behaves as the strong-lensing literature says it does (near-isothermal, ratio near unity)   (74 lenses, median M_Ein/M_SIS = 1.109 with 27% per-lens scatter -- consistent with SLACS's published near-isothermal slope (gamma' = 2.078 +/- 0.027 with intrinsic dispersion 0.16).  The per-lens SCATTER, not the per-lens statistical error, is what sets the achievable precision)
[FAIL] E2 [test] an existing or approved survey can decide L57's environmental prediction at the 0.1 per cent it names   (NO, and it fails on both counts even with the optimistic scatter.  Statistically, 0.1% needs 180000 matched lenses against about 14500 available from Euclid+LSST -- short by 12x (91x on the crude scatter).  Decisively, a matched cluster-vs-field differential has a systematic floor of order 1.5% (E3), which is 15x the target and does not shrink with any sample.  0.1% is not reachable by any current or approved instrument)
[FAIL] E3 [test] the TOP of L57's environmental band (2.3 per cent) is a comfortable matched cluster-versus-field differential in the Euclid/LSST era -- statistics AND a 3 sigma margin on the differential floor   (HALF.  Statistics: YES -- 340 matched lenses needed (2507 on the crude scatter) against about 14500 available, so the sample is not the obstacle.  Margin: NO -- 2.3% is only 1.5x the 1.5% differential floor, i.e. a 1.5 sigma measurement at best, not 3.  So the TOP of the band becomes a MARGINAL Euclid/LSST-era test and the rest of the band, four orders of magnitude wide, does not become anything.  That is a real proposal and it is a weak one; both halves are stated)
[FAIL] E4 [test] the environmental test is limited by something a bigger survey can fix   (NO -- the differential SYSTEMATIC floor is what stops it, and no survey removes that.  With an unlimited sample the matched cluster-versus-field differential still cannot resolve better than about 1.5%, which is 15x L57's 0.1% target and 62x the bottom of its band.  The sample shortfall (12x) is the fixable half of the problem and it is the smaller half.  L57 E4 therefore remains, as L57 said, NOT MEASURED -- and this lane adds that it is not MEASURABLE at 0.1% by anything now approved, and that the SLACS catalogue's own environment proxy flags only 3 of 86 lenses, so the cluster arm does not exist in today's samples either)
[FAIL] F1 [VERDICT] the group channel closes L57's nonlocal functional -- either by excluding it or by clearing it   (NO, it CANNOT DECIDE, and for a structural reason.  (a) The prediction reproduces independently at 18-45%.  (b) The measurement's common-mode floor is 17-28%, so the band is inside the errors at under 1 sigma (0.62-0.42 sigma).  (c) It is systematics-limited, so sample size does not help.  (d) The LambdaCDM baseline for the hydrostatic route is 1.11, not 1.00, so the effect is degenerate with the hydrostatic bias even at zero measurement error.  (e) The degeneracy-free collisionless route carries a 20% estimator bias at group mass.  What would decide: 5.9% total on a collisionless-tracer group ratio with a validated estimator.  The decisive test L57 named second (galaxies in clusters, 0.1%) is NOT reachable by any approved survey -- the matched-differential floor is 15x too high and the sample 12x too small -- though its TOP end (2.3%) becomes a marginal (1.5 sigma) Euclid/LSST-era test)
[PASS] F2 [VERDICT] this lane's confrontation is honest in both directions -- it reports what runs against the mechanism as well as what runs for it   (the group channel does NOT exclude the mechanism (D1), the measured central value happens to sit inside the predicted band, and L57's group model is the one that MAXIMISES the group's trigger gradient so the band is an upper bound (A6) -- all three run FOR the mechanism surviving and are recorded as such.  Against it: the degeneracy with hydrostatic bias is structural and not fixable by precision (D2); the collisionless cluster-scale ratio 1.047 tightens L51/L57's ceiling from 4.9 to 5.8 sigma if it is adopted, and is reported NOT BANKED (D4); and the environmental test L57 named as decisive is not reachable at the precision L57 named (E2).  No statement anywhere that data favour this framework over LambdaCDM)
```

The complete, untruncated lines are in [`L62_group_channel.out`](L62_group_channel.out).
