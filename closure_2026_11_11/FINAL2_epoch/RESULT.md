# FINAL-2 (EPOCH) RESULT: which formation event fixes the halo's amount (2026-11-11)

**Label: (e) BEST-RANKED / NO POWER (canonical), (e) BEST-RANKED / NO POWER (alt).**
No epoch among the six candidates reproduces the measured pattern. The end of active star formation /
last major merger is the least wrong; it beats the no-epoch floor by 0.056 dex, which is inside the
class errors (se 0.045-0.132 dex) and inside DSB1's minimum detectable offsets (0.59-1.23 dex).

TEST lane, quarantined. Adopts nothing, relabels nothing (DD1's, DSB1's, VSH1's and FLD1's labels
stand as recorded), registers nothing. Footings never pooled: canonical a0 = 9.3603e-11,
alt a0 = 1.1312e-10. Cold dark energy is a gravitating field component, never a particle.
Pre-registration `PREREGISTER.md` and the prediction numbers `predictions_frozen.csv` were frozen
before `final2_epoch.py` was run; the script reads the prediction table, it does not compute it.

## KA1: the lane's arithmetic reproduces DD1's frozen table

`g_obs_law(g_bar;a0) = ½ ( g_bar + sqrt(g_bar² + 4 a0 g_bar) )` from DD1's KA4 identity
`g_bar (g + a0) = g²`, i.e. the simple interpolation `mu(x) = x/(1+x)`. Residual
`= (lgo − lgb) − log10(g_obs_law/g_bar)`, median over each class' main-table points
(3419 of 3621 rows). Against DD1's published class offsets:

| class | this lane, can | DD1's L0 range (A->B / B->A / LOCO), can | agree |
|---|---|---|---|
| SPARC | +0.026 | +0.00 / +0.02 / +0.00 | yes |
| KiDS | +0.133 | +0.13 / +0.14 / +0.14 | yes (DD1: alt +0.09-+0.10) |
| ATLAS3D | +0.070 | +0.07 / +0.08 / +0.07 | yes |
| X-COP | +0.504 | +0.57 / +0.48 / +0.50 | yes |
| MW ultra-faints | +0.592 | +0.51 / +0.60 / +0.59 | yes |
| tidal dwarfs | −0.687 | −0.61 / −0.87 / −0.69 | yes |
| NGC 1052 UDGs | −0.843 | −0.94 / −0.74 / −0.84 | yes |
| faint rotators | −0.239 | −0.27 / −0.24 / −0.24 | yes |

Footing split: `resid(alt) − resid(can) = −0.0411 dex` in the deep regime (exact:
`−0.5 log10(1.1312/0.93603)`), and −0.035 dex for X-COP, which sits near the Newtonian branch.
This reproduces DD1's "alt within 0.04". The lane's per-class numbers are DD1's own numbers.

## Measured residual, the six target classes, both footings

Median over the class' main-table points, dex in Y = log10(1 + X). `se` from the robust scatter of the
residuals over systems (`1.2533 · 1.4826 · MAD / sqrt(n_sys)`).

| class | pts | sys | med lg g_bar | med Y | **resid CAN** | **resid ALT** | se |
|---|---|---|---|---|---|---|---|
| tidal dwarfs | 6 | 6 | −11.454 | 0.067 | **−0.687** | **−0.725** | 0.100 |
| NGC 1052 UDGs (DF2/DF4) | 2 | 2 | −11.673 | 0.012 | **−0.843** | **−0.881** | 0.132 |
| MW ultra-faints | 31 | 31 | −13.123 | 2.075 | **+0.592** | **+0.552** | 0.098 |
| bright M31 dwarfs | 33 | 33 | −12.497 | 1.364 | **+0.090** | **+0.051** | 0.088 |
| faint LSB field rotators | 20 | 20 | −11.260 | 0.393 | **−0.239** | **−0.274** | 0.045 |
| X-COP clusters | 129 | 7 | −10.700 | 0.917 | **+0.504** | **+0.471** | 0.048 |

Measured order, most deficient to most excessive:
DF2/DF4 (−0.84) < tidal dwarfs (−0.69) < LSB rotators (−0.24) < M31 (+0.09) < X-COP (+0.50) < UFD (+0.59).

**Measured class-to-class spread: 1.435 dex (canonical), 1.433 dex (alt).**

Caveat on X-COP: the all-point median (+0.504) and the outermost-point median (+0.154) differ by
0.35 dex, so X-COP's residual is aperture-dependent in a way no other class here is. Both are printed.

## Score of each candidate

rms = RMS(pred − meas) over the six classes, dex (primary pre-registered key). Floor: the constant
predictor (every class at the measured class median), rms 0.548 on both footings.
rho is a supplementary, post hoc Spearman rank correlation; `nan` where a candidate predicts no
spread at all.

| candidate | rms CAN | rms ALT | sign/6 | <=0.15 dex | spread | rho | rank |
|---|---|---|---|---|---|---|---|
| (e) end of SF / last major merger | **0.492** | **0.506** | 5.0 | 1 | 0.32 | 0.943 | **1** |
| (f) recombination / fixed early z | 0.556 | 0.563 | 3.0 | 1 | 0.00 | nan | 2 / 3 |
| (b) first caustic / shell crossing | 0.589 | 0.560 | 3.0 | 1 / 2 | 0.78 | 0.600 | 2 / 3 |
| (a) turnaround of the baryon shell | 0.636 | 0.608 | 3.0 | 1 | 0.75 | 0.600 | 4 / 5 |
| (c) the shock (VSH1) | 0.634 | 0.652 | 3.0 | 1 / 0 | 0.21 | 0.371 | 4 / 5 |
| (d) last epoch internal g > a0 | 0.907 | 0.891 | 4.0 | 3 | 1.75 | −0.029 | **6** |

(The two ranks per row are canonical / alt.)

Per class, measured (canonical) against each pre-registered prediction:

| class | measured | (a) | (b) | (c) | (d) | (e) | (f) |
|---|---|---|---|---|---|---|---|
| tidal dwarfs | −0.687 | −0.90 | −0.90 | +0.20 | −0.75 | −0.05 | 0.00 |
| DF2 / DF4 | −0.843 | −0.90 | −0.90 | +0.20 | −0.85 | 0.00 | 0.00 |
| MW ultra-faints | +0.592 | −0.70 | −0.60 | +0.25 | −1.55 | +0.27 | 0.00 |
| bright M31 dwarfs | +0.090 | −0.40 | −0.35 | +0.21 | +0.20 | +0.04 | 0.00 |
| faint LSB rotators | −0.239 | −0.45 | −0.40 | +0.20 | +0.07 | +0.02 | 0.00 |
| X-COP clusters | +0.504 | −0.15 | −0.12 | +0.04 | +0.02 | +0.10 | 0.00 |

## What the scoring says

**1. Not one candidate reproduces the spread.** The data span 1.435 dex across the six classes. The best
candidate's predictions span 0.32 dex — a factor 4.5 too narrow. (d) is the only candidate that
predicts a wider span than the data, and its rank correlation with the data is −0.03, i.e. none.

**2. The a0-channel is capped and cannot be the whole story.** FRZ2 closed every framework a0(z) it
froze (P0 Delta chi² 9916 / 9009; P0.5 252 / 167; P1 13338 / 23421; H 20943 / 34390; gate <= 4). The
forest wants a0 to rise with z, and P1 already overshoots, so the surviving window is roughly
`0.3 <~ d log a0 / d log(1+z) <~ 0.7`. In the deep regime `X ∝ a0^{1/2}`, so the a0-channel is worth
at most `0.5 log10(3.2) ~ +0.25 dex` even at a formation redshift of 12. **The measured deficits
(−0.69, −0.84 dex) and excesses (+0.50, +0.59 dex) are two to four times larger than any
epoch-keyed a0 effect can reach.** No choice of event date, acting through a0 alone, gets there.

**3. The failure is structural, not a matter of the date.** The measured pattern is **bipolar** at
matched formation-epoch ordering: the most recently processed systems (tidal dwarfs, DF2/DF4, made of
stripped and recycled material) are the most *deficient*, while the oldest systems (ultra-faints) and
the deepest wells (X-COP) are the most *excessive*. Under any single monotone map from formation
redshift to residual, the ultra-faints and the clusters must land on *opposite* sides, because the
clusters are the latest-assembling systems in the sample and the ultra-faints are the earliest. Both
are measured at ≈ +0.5 dex. **A single monotone function of the event date is falsified by that
pair alone**, independently of the epochs' absolute normalisation. This is the sharpest result in the
lane.

**4. Why (e) ranks first, and why that is nearly empty.** (e) is the only candidate that puts the
ultra-faints positive and large while keeping the actively star-forming classes near zero. It gets
5 of 6 signs and rho = 0.943. But it does that by predicting *small* numbers everywhere (spread
0.32 dex); it wins on rms mainly because it declines to make the large predictions that (a), (b) and
(d) make and get wrong. Its 0.056 dex edge over the constant floor is smaller than the smallest class
se (0.045-0.048 dex for two classes, 0.088-0.132 for the rest), and DSB1's frozen power line says the
hosted dwarf classes cannot see a 0.30 dex departure in either direction (MDO 0.59-1.23 dex). So the
ranking distinguishes (e) from (f) by less than one class error.

**5. Where the formation reading would have to go.** (a), (b) and (c) all date a *collapse* event.
Their common failure is on the ultra-faints, which they push down (to −0.6 or below) while the data
push them up to +0.59. The one channel that can reverse that sign — and the one that is not capped
by FRZ2 — is the baryon-assembly channel: `X_today = X_f · f_b(t_f)` with
`f_b = M_b(present at t_f)/M_b(enclosed today)`. Ultra-faints quenched at reionization and are
gas-free today, so `f_b >> 1` for them and the sign flips positive; still-accreting gas-rich LSB
rotators have `f_b < 1` and go negative; tidal dwarfs and DF2/DF4, made of material that had already
settled inside a parent and then was stripped, arguably have **no collapse event of their own at
all**, which sends them to the all-or-nothing floor `resid = −Y_law` (−0.75 and −0.85, both close to
the measured −0.69 and −0.84). That composite — *epoch sets the sign through baryon loss or gain
after the event, not through a0* — is the only reading in the pre-registered set that gets all six
signs, and it is not one of the six candidates as stated; it is (e) with the assembly channel wired in.
**It was not pre-registered as a candidate. Reporting it, not grading it.**

## Pre-registered prediction record versus outcome

| pre-registered claim | outcome |
|---|---|
| (a) would push UFDs most negative (−0.7) | **wrong in sign**, by 1.29 dex. Biggest single miss in the lane. |
| (b) is nearly degenerate with (a), separable only where a class has a turnaround but no caustic | held: (a) and (b) differ by 0.05 dex or less on every class; no class separates them |
| (c)'s falsifiable cell is X-COP (+0.04) | **wrong in sign**, by 0.46 dex |
| (d)'s falsifiable cell is UFD (−1.55) | **wrong in sign**, by 2.14 dex; (d) ranks last |
| (f) predicts zero spread | held: it is a pure control and is unbeatable only because the floor is the same construction |
| any a0-only epoch is capped at ~0.25 dex | held: measured range is 1.435 dex |
| LSB rotators and TDGs would be negative | held for both (measured −0.24, −0.69) |
| no candidate would beat the constant floor decisively | held: best margin 0.056 dex |

## Honesty flag, restated

`PREREGISTER.md` was written after DD1's `RESULT.md` had been read, so the pre-registered signs and
sizes were **not** produced blind to the measured pattern. They were derived from the epoch
assignments plus FRZ2's a0(z) bound, but the possibility that DD1's printed class numbers steered
them cannot be excluded. The prediction table was frozen in its own file before the scoring script ran
and was not touched afterwards, so the arithmetic is not circular; the *hypotheses* may be.

## Not computed, not checked

- No new data were taken; every number comes from DD1's frozen table. This lane adds no measurement.
- The epoch assignments (`PREREGISTER.md`) are order-of-magnitude literature values, not computed
  from any collapse model in the record. VSH1's are the exception: its settling epochs are its own
  computed numbers, and only for log M_b 9 / 10.5 / 11.5. The extrapolation of `z_sh ∝ M_b^-0.21`
  to ultra-faint masses (log M_b 4.5) gives z > 20, which is unphysical and is flagged as such
  wherever it is used.
- The composite in §5 is reported, not graded. It has four moving pieces (event date, `f_b`, the
  all-or-nothing floor for recycled material, and the a0-channel cap) against six classes.
- Per-class aperture effects were not modelled. X-COP's 0.35 dex difference between all-point and
  outermost-point medians is the visible case; SPARC's 2700 points span radii of 0.26-63 kpc and the
  residual varies with radius inside a class.
- No Lean file: no structural claim is made.
- Mutants were not run for this lane (it scores, it does not hypothesise).

## Files

`PREREGISTER.md`, `predictions_frozen.csv`, `final2_epoch.py`, `final2_measured.json`, this file.
Re-run: `python3 final2_epoch.py` from this folder (about 1 s, stdlib only, fixed table and predictions).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
