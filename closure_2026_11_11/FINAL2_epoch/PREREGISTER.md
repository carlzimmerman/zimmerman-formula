# FINAL-2 (EPOCH) — pre-registration, before any number is computed in this lane

Lane: **LANE FINAL-2 (EPOCH)**. TEST lane: adopts nothing, relabels nothing, registers nothing.
Footings never pooled: canonical a0 = 9.3603e-11 m/s^2, alt a0 = 1.1312e-10 m/s^2.
Cold dark energy is a gravitating field component, never a particle.
kappa = 1/2 FITTED; not theory closed.

## Honesty flag on the pre-registration

This file was written **after** reading DD1's `RESULT.md` summary, which prints the measured per-class
residuals. It is therefore **not a blind pre-registration**. The predicted signs and sizes below were
derived from (i) the formation redshift each candidate assigns to each class and (ii) FRZ2's bound on
any a0(z). The risk that they were shaped by DD1's printed numbers is real and is stated here rather
than hidden. What *is* independent is the arithmetic of the scoring: the prediction table was frozen
in this file before `final2_epoch.py` was ever run, and the script reads the prediction table from a
separate frozen file (`predictions_frozen.csv`) that was not edited afterwards.

## Statistic (SHP1's, as DD1 froze it)

    X      = g_obs / g_bar - 1                 (enclosed non-baryonic over enclosed baryons)
    Y      = log10(1 + X) = log10(g_obs/g_bar) (dex in g_obs at fixed g_bar)
    resid  = Y_meas - Y_law(g_bar; a0)

DD1's KA4 pins the law's algebraic form: `g_bar (g + a0) = g^2`, i.e. `g_bar = g^2/(g + a0)`,
the simple interpolation `mu(x) = x/(1+x)`. Solving for g:

    g_obs_law(g_bar; a0) = 0.5 * ( g_bar + sqrt(g_bar^2 + 4 a0 g_bar) )
    Y_law                = log10( g_obs_law / g_bar )
    equivalently         X_law = a0 / g_obs_law   (so the phantom pull is a0 g_obs/(g_obs+a0) < a0)

Two footing consequences used below, both exact for the frozen form:
- deep regime (`g_bar << a0`): `g_obs -> sqrt(a0 g_bar)`, so `X_law -> sqrt(a0/g_bar)` ∝ a0^{1/2}.
  **A change of a0 by a factor f moves Y_law by 0.5 log10 f.**
- therefore `resid(alt) - resid(can) = -0.5 log10(1.1312/0.93603) = -0.0411 dex`, uniform to first
  order, and smaller in the Newtonian-ish regime. (DD1's own text says "alt within 0.04".)

## The two channels an epoch can act through

Under the formation reading the halo's amount is fixed at the event and conserved afterwards.
Whatever the event, its *date* can only enter the residual through two channels:

**(i) The a0-channel.** If the amount frozen is the law evaluated with the a0 of that epoch, then for a
deep system `X ∝ a0(z_f)^{1/2}`, so

    resid_a0 = +0.5 * log10[ a0(z_f)/a0(0) ].

**This channel is bounded.** FRZ2 closed every framework a0(z) it tried against the forest gate
(P0 9916 / 9009; P0.5 252 / 167; P1 13338 / 23421; H 20943 / 34390; gate <= 4). The deficit needs a0
to *rise* with z; P1 already overshoots. So the surviving window is roughly
`0.3 <~ d log a0 / d log(1+z) <~ 0.7`, giving `a0(z)/a0(0)` of about 1.7 at z = 3, 2.7 at z = 8,
3.2 at z = 12. Hence

    resid_a0  <~  0.5 log10(3.2)  ~  +0.25 dex      even for a formation redshift of 12.

**An epoch that works only through a0 cannot reach the observed amplitude range (-0.9 to +0.6 dex).**
It is capped a factor ~2-4 below the data. This is a hard, pre-registered constraint that any
epoch candidate must beat.

**(ii) The baryon-assembly channel (dilution / concentration).** The phantom mass is frozen, so the
baryons that arrive, or that are expelled, after the event change the denominator:

    X_today = X_f * f_b(z_f),      f_b(z_f) = M_b(present at t_f) / M_b(enclosed today)

With `X_f ∝ sqrt(a0_f/g_bar_f)` and `g_bar_f ≈ g_bar_0 f_b` (mass scales as f_b at fixed profile),
the log-residual is

    resid = 0.5 log10(f_b) + 0.5 log10(a0_f/a0_0).

`f_b > 1` (a system that *lost* baryons after the event) gives a **positive** residual; `f_b < 1` (a
system still assembling, or that grew by gas accretion after the event) gives a **negative** residual.
Unlike channel (i), this channel is **not** capped: it can run to -large for a system with no event at
all, and to +large for a system stripped of most of its baryons.

## Pre-registered formation redshifts z_f per class

Order-of-magnitude literature values, frozen here, no fitting.

| class | log10 M_b / M_sun | z_ta (a) | z_fold (b) | z_shock (c, VSH1) | z(>a0) (d) | z_quench (e) | fixed (f) |
|---|---|---|---|---|---|---|---|
| tidal dwarfs | ~8.5 | none of its own (recycled) | none (high-L debris) | ~5.2 (by mass) | none (g ~ 3e-12 << a0) | ~0 (still forming stars) | 1100 |
| DF2 / DF4 | ~8.4 | none of its own (collision debris) | none | ~5.2 | none | ~0.5-1 (gas-free now) | 1100 |
| MW ultra-faints | ~4.5 | 12-20 | 8-14 | >20 (extrapolated, unphysical) | never | 6-10 (reionization) | 1100 |
| bright M31 dwarfs | ~8.0 | 4-8 | 3-6 | ~5.5 | ~5.7 | 0.3-1 (quenched at infall) | 1100 |
| faint LSB field rotators | ~8.5 | 2-4 | 1.5-3 | ~5.2 | ~1.6 | ~0 (still forming stars) | 1100 |
| X-COP clusters | ~13.5 | 0.2-0.5 | 0.15-0.4 | ~0.4 (extrapolated) | ~1 | 1-2 (BCG quenched early) | 1100 |

VSH1's computed settling epochs (canonical / alt): log M_b 9 -> z 4.96 / 5.08; 10.5 -> 3.45 / 3.65;
11.5 -> 1.46 / 1.65. Power-law fit `z_sh ∝ M_b^-0.21`, used for the extrapolation column. Note the
extrapolation to log M_b 4.5 is meaningless (z > 20): the mass scaling cannot extend there.

## Predicted SIGN and rough SIZE of the residual, per candidate

Sizes in dex. "+" = excess over the law (too much non-baryonic mass), "-" = deficit.
`--` marks a class for which the candidate supplies **no event**, so I pre-register the
all-or-nothing value `resid = -Y_law(class)` (no halo at all), whose size I give numerically.
Y_law at the class' median g_bar is pre-computed by hand here as the no-event floor:
TDG 0.75, DF2/DF4 0.85, UFD 1.55, M31 1.36, LSB 0.67, X-COP 0.43.

| class | (a) turnaround | (b) caustic | (c) shock | (d) >a0 | (e) quench | (f) fixed z |
|---|---|---|---|---|---|---|
| tidal dwarfs | -0.9 `--` | -0.9 `--` | +0.20 | -- -0.75 | -0.05 | 0 |
| DF2 / DF4 | -0.9 `--` | -0.9 `--` | +0.20 | -- -0.85 | 0.00 | 0 |
| MW ultra-faints | **-0.7** | **-0.6** | +0.25 | **-- -1.55** | **+0.27** | 0 |
| bright M31 dwarfs | -0.4 | -0.35 | +0.21 | +0.20 | +0.04 | 0 |
| faint LSB rotators | -0.45 | -0.40 | +0.20 | +0.07 | **+0.02** | 0 |
| X-COP clusters | **-0.15** | **-0.12** | **+0.04** | +0.02 | +0.10 | 0 |

Reasoning per candidate, all written before the scoring run:

- **(a) turnaround.** Events date with collapse epoch: UFDs earliest, clusters latest. The dilution
  channel dominates and grows with the fraction of baryons that arrive after turnaround, so early
  formers are pushed *down*: UFDs most negative, clusters least. TDGs and DF2/DF4, made of material
  that had already turned around inside a parent and then was stripped, have no event of their own:
  `--`. Highest-risk cell: UFDs, pre-registered **-0.7**.
- **(b) first caustic / fold (0.52 R_ta).** Same ordering as (a) at slightly lower z, so a slightly
  weaker copy. Nearly degenerate with (a); the two can only be separated if a class has a turnaround
  but no caustic (gas-rich, rotating systems) — I pre-register LSB rotators and TDGs as that case.
- **(c) the shock.** VSH1 dates the event by mass: more massive settles later. Both channels then say
  late = low, so this candidate's sharp signature is that **clusters come out lowest and UFDs highest**.
  Pre-registered X-COP **+0.04**: this is the candidate's falsifiable cell.
- **(d) last epoch internal g exceeded a0 everywhere.** Systems whose present internal field is far
  below a0 (UFDs ~ 8e-4 a0, DF2/DF4, TDGs) have no such epoch within any sane assembly history, so
  they get `--`. The falsifiable cell is **UFDs at -- -1.55**, the single most extreme prediction in
  the table.
- **(e) end of star formation / last major merger.** Ordered by quenching date: UFDs quenched at
  reionization (z 6-10) and so take the largest a0 boost; the still-star-forming classes (TDGs, LSB
  field rotators) quench "today" and so sit at 0. Clusters split: BCG stars quenched early (z 1-2) but
  the gas is still falling in, so the baryon channel, not the date, should set them; pre-registered
  **+0.10**.
- **(f) recombination / any fixed early z.** The date is the same for every class, so the prediction is
  a single constant across all six. Zero discrimination by construction. Control row.

## Pre-registered scoring rule

For each candidate, over the six target classes:

1. **sign_hits** — count of classes where sign(pred) == sign(meas), with `|meas| <= 0.05` treated as
   "no sign" and scored 0.5 for a prediction within +/-0.10 dex, else 0. (Max 6.)
2. **size_rms** — RMS of (pred - meas) over the six classes, dex. Lower is better.
3. **size_hits** — count of classes with `|pred - meas| <= 0.15` dex.
4. **rank** — 1 = best. Primary key: **size_rms**; tie-break: sign_hits, then size_hits.

Reference floor for comparison: predicting every class at the measured global median residual
(a constant) gives an rms that I will compute and print; a candidate must beat it to count.

Decision rule pre-registered now: **the best epoch is the candidate with the lowest size_rms; if
no candidate beats the constant floor, the lane's label is NO EPOCH AMONG THE CANDIDATES.**

## Files

- `PREREGISTER.md` (this file, frozen first)
- `predictions_frozen.csv` (the 6x6 prediction numbers, read by the script, never edited after)
- `final2_epoch.py`
- `RESULT.md`
