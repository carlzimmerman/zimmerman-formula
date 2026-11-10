# KO2 FROZEN CRITERIA: does each galaxy type carry its own lensing signal out to Mpc radii?

Committed alone, before any KO2 script exists in this folder and before any KO2 lensing number has been computed.
TEST lane, quarantined. Adopts nothing, relabels nothing, not registered. Footings never pooled (canonical a0 9.3603e-11,
alt a0 1.1312e-10 m/s^2). kappa = 1/2 FITTED; not theory closed.

## Why

The law read as a field around every galaxy says a disc galaxy's lensing profile keeps its 1/R shape out to 3 Mpc, like an
early type's. The one surviving construction (lane HE1) needs the opposite for discs: no extended field of their own beyond a
few hundred kpc, with what KiDS sees at Mpc radii carried by early types and neighbours. The only evidence so far is a post hoc
sub-split of KO1 (10,282 host-free late lenses, after a veto that carves a tapered edge). KO2 keeps all 181,477 lenses and
**models every catalogued neighbour instead of vetoing it**, then asks of each type whether its own projected mass profile
continues beyond the inner window.

## What I have seen before freezing (disclosure)

- KO1 in full as text: `FROZEN_CRITERIA.md`, `AMENDMENT_A1-A3.md`, `RESULT.md` (every number in it), and the scripts `ko1.py`,
  `ko1_extra.py`, `ko1_shape.py`, `ko1_neighbours.py`. The header of `ko1.out` (known-answer lines and the pool size
  888,795; no amplitude). No other KO1 output file.
- Numbers from KO1's RESULT that bear on this lane (canonical; outer | middle | inner window amplitudes of the stack against
  the law): host-free late (10,282) -0.19 +- 0.39 | 1.53 +- 0.40 | 1.58 +- 0.27; host-free early (30,385) 1.34 +- 0.18 |
  1.90 +- 0.15 | 1.84 +- 0.11; W30 late 0.53 +- 0.23 | 1.54 +- 0.26 | 0.92 +- 0.16; W30 early 1.19 +- 0.21 | 1.92 +- 0.20 |
  1.92 +- 0.14; hosted late 1.50 +- 0.16 | 1.12 +- 0.19 | 1.28 +- 0.11; hosted early 2.45 +- 0.13 | 2.48 +- 0.12 |
  1.81 +- 0.10; W10 all 1.71 +- 0.09 | 1.87 +- 0.09 | 1.65 +- 0.06. Shape ratios R_s: host-free late -0.12 +- 0.25, early
  0.73 +- 0.11; the late deficit shrinks as the veto edge moves out (0.01 +- 0.49 at 1.3 R_h, 0.13 +- 0.68 at 1.6 R_h). E8: the
  catalogued neighbours' point-mass term around host-free lenses. KO1's W10 numbers split by type over all lenses have NOT
  been seen.
- Lines of `fable52_push/HE1_held_out_envelope/FROZEN_CRITERIA.md` that mention late types, G4 and the wall (skimmed).
- **A model-only design check, run before this file, reading no data file** (`ko2_design_toy.py`, kept in the session
  scratchpad and committed after this file, labelled pre-freeze). It takes the deep-regime band kernels below, gives each
  window the shape-noise information density per log g_bar, and sets the noise of each window so that a one-amplitude fit there
  has a chosen error. With window errors 0.13 / 0.13 / 0.09 (outer / middle / inner, a guess for all late lenses) it gives
  0.37 on a[outer] / a[inner] (the brief's statistic) and 0.19 on the tied ratio R_ext defined below; with KO1's host-free
  late errors (0.39 / 0.40 / 0.27) it gives 1.12 and 0.58. Neighbour columns will cost more power than this toy shows.

## The flaw in the brief's statistic, and the change

The brief proposes R_own = a[outer] / a[inner]. In DeltaSigma a band of mass shows up mainly as **enclosed mass outside its own
outer edge**; inside the band it adds only a weak, sign-changing term. For the law's profile in the deep regime the outer band's
own term in the outer bins is (1 - 2 sqrt(g / e_4)) of the law, from +0.36 at the outermost edge to -1 at the innermost, while
the enclosed mass of the bands inside it supplies 2 sqrt(g / e_4). The outermost measured band is therefore weighed almost only by
its shape across four bins, and its own mass appears beyond 3 Mpc, where nothing is measured. That is why the toy gives it three
times the error of a window amplitude.

**Change.** The primary statistic ties every band beyond the inner window into one amplitude ("ext": middle + outer + the far
band), which is weighed both by its shape in bins 4-6 and by its enclosed mass in bins 0-3. It asks the brief's question at
"beyond a few hundred kpc" (the inner window's outer edge sits at 0.26 Mpc for a log M* 10.3 late type and 0.43 Mpc for a log M*
10.8 early type) rather than "beyond about 1 Mpc". The brief's four-band R_own is kept as a frozen **secondary label**, reported
beside the primary and never in place of it.

## Inputs (all on disk, git-ignored; nothing is downloaded; the shear catalogue is not read)

In `real_research/data/lensing_rar/`: `lr_lenses.npz` (181,477 lenses: ra, dec, z, logM, Mgal, typ, chi), `cfg110_perlens.npz`
(`WG`, `WW`, `NN` in the 15 g_bar bins, `gbar_edges` e_0 ... e_15 from 1e-15 to 5e-12 m/s^2), `cfg116_perlens.npz` (cross
sums `WX`), `cfg96_stack.npz` (`patch`, the 50 jackknife patches), `cfg96_isoflags.npz`, `KiDS_DR4_brightsample.fits` with
`KiDS_DR4_brightsample_LePhare.fits`. Conventions are KO1's: r = MAG_AUTO_CALIB, z = zphot_ANNz2, log M* = MASS_MED + 0.15,
chi from the record's DC (flat, Omega_m 0.3, H0 70), Mgal = M* (1 + 10^(-0.69 log M* + 6.63)), early type = u - r > 2.0 with
u - r = MAG_ABS_u - MAG_ABS_r. Data = 4 G WG / WW in m/s^2 per lens and bin (KO1's g_obs = 4 G DeltaSigma). Code is copied from
the KO1 scripts into this folder, not imported.

## The mass model

**The law's profile of one galaxy** (each footing, exact nu, KO1's convention). With g = G Mgal / R^2:
4 G DeltaSigma_law(R) = D(g) = g nu(g / a0), nu(y) = 1/2 + sqrt(1/4 + 1/y). Its surface density, vanishing at infinity, is
4 G Sigma_law = S(g) = Q(g) - D(g), with Q(g) = int_0^g nu dg' = g/2 + (sqrt(g)/2) sqrt(g + 4 a0) + 2 a0 asinh(sqrt(g / (4 a0)))
(4 G times the mean surface density inside R). With every amplitude 1 the model reproduces KO1's law cells exactly (KA-1b).

**Bands**, in each galaxy's own g (so in its own radii): centre g >= e_13 (everything inside the innermost measured radius,
as one point of 4 G M_c = pi G Mgal Q(e_13) / e_13); inner [e_7, e_13) (bins 7-12); middle [e_4, e_7) (bins 4-6); outer
[e_0, e_4) (bins 0-3); far g < e_0, out to infinity. Data bins used: 0-12 (bins 13, 14 unused, as in KO1).

**A lens's own bands, in its own cells.** For a band [g1, g2): zero for g >= g2; D(g) - g Q(g2) / g2 inside the band;
g (Q(g1) / g1 - Q(g2) / g2) outside it (enclosed mass). The centre point gives g Q(e_13) / e_13 everywhere. Area-averaged over
each cell (R_lo = sqrt(G Mgal / e_{b+1}), R_hi = min(sqrt(G Mgal / e_b), 3 Mpc)) with KO1's 24-node Gauss-Legendre in R^2. The
own far band touches no own cell.

**A neighbour's bands, seen off-centre.** For a band of neighbour j at projected physical separation d from lens i (d = theta
chi_i / (1 + z_i)), the cell average is 4 G [int_{R_lo}^{R_hi} 2 M_B(R) / R dR - (M_B(R_hi) - M_B(R_lo))] / (pi (R_hi^2 -
R_lo^2)), with M_B(R) the band's mass inside the circle of radius R about the lens. This is the azimuthal mean of the tangential
signal (mean inside minus mean on the circle), area-averaged; an axisymmetric mass wholly outside the circle gives zero. Lengths
scale with l_j = sqrt(G Mgal_j / e_0); M_B = (Mgal_j / 4) m_B(R / l_j, d / l_j) with m_B universal per band and footing. The
script tabulates J_B(r, delta) = int 2 m_B dln r - m_B on a log grid (r and delta from 1e-3 to 60) and interpolates bilinearly in
the logs; the cell value is (e_0 / pi) [J(r_hi) - J(r_lo)] / (r_hi^2 - r_lo^2). The centre point is analytic (KO1 E8's formula).
The neighbour's mass sits at the lens's distance; the ratio of critical densities between a neighbour's redshift and the lens's
is not modelled (limit L2).

**Neighbours.** KO1's pool (r < 20, 0.02 <= z <= 0.8, finite log M* > 7, masked 0 or 1), any mass, excluding the lens itself
and anything at d < 5 kpc (blends and duplicates), with |chi_j - chi_i| < W (primary 230 Mpc; bracket 115) and
d < R_h,i + 2 Mpc, R_h,i = min(3 Mpc, sqrt(G Mgal_i / e_0)). Neighbours beyond that reach are left out; their mean is removed
with the rest by the next step.

**Chance projections.** As KO1 E8: the same columns are computed around shuffled sky positions (five shuffles, seeds 52 to 56;
each lens keeps its chi, z, mass and cells and borrows another lens's position; the pool object at the borrowed position is
excluded), and the neighbour columns used are real minus the mean of the five.

**Classes.** Type: early if u - r > 2.0, else late; pool objects with non-finite u - r count as late (if they are more than 1 %
of the pool, the bracket "untyped as early" is run and reported). Mass halves per type at the threshold m_t: the median of
log M* over type-t lenses weighted by sum_{b <= 12} WW_ib (weights only), moved up to the midpoint between that value and the next
larger distinct log M* in the pool, **so no object sits on a threshold** (the tie rule; the count within 1e-4 dex of each
threshold is reported). Giants: log M* >= 11.0 (the record's lens cut is log M* < 11.0), any type, neighbour-only. Five classes:
late-low, late-high, early-low, early-high, giant. Every galaxy of a class, lens or neighbour, carries the same amplitudes.

## The fit

Weighted least squares over all lenses and bins 0-12: minimise sum_i sum_b WW_ib (4 G WG_ib / WW_ib - sum_k X_ibk a_k)^2,
X = own columns of the lens's class plus every neighbour's columns of its class. Normal equations accumulated per jackknife patch;
every quantity below gets its error from the delete-one-patch jackknife over the 50 patches (ratios computed per jackknife
sample).

- **Primary design (tied, continued closure):** 15 amplitudes a[class, centre / inner / ext], ext = middle + outer + far.
- **Secondary design (the brief's):** 20 amplitudes a[class, centre / inner / middle / outer], far tied to outer.
- **Gate brackets:** (B1) window 115 Mpc; (B2) far-band closure zero (each neighbour's profile ends at g = e_0); (B3) untied:
  own amplitudes per lens class and separate neighbour amplitudes per class (27).

## Statistics

Class weights per type: W_tm proportional to sum_{i in (t, m)} sum_{b <= 12} WW_ib (own law cell_ib)^2, normalised (weights only).

- **Primary:** R_ext(t) = sum_m W_tm a[(t, m), ext] / sum_m W_tm a[(t, m), inner]. The law as the galaxy's own field gives 1;
  a galaxy with no field of its own beyond the inner window gives 0.
- **Secondary:** R_own(t) = sum_m W_tm a[(t, m), outer] / sum_m W_tm a[(t, m), inner] from the secondary design.
- **The law's floor**, per type, design and footing: the smallest R over k in {0.5, 0.7, 1, 1.4, 2, 2.8, 4, 5.6, 8} when the
  own-only version of the design is fitted (WW weights, no noise) to the law's own cells at mass k Mgal. Expected near 0.99.
- s_tot = sqrt(s_jk^2 + 0.05^2). The 0.05 covers the kernel tables (KA-2 allows 1 %), the unmodelled critical-density ratio of
  neighbours, and the floor's residual model dependence. Set now; not widened afterwards.

## Labels (per type, per footing; the primary decides, the secondary is reported beside it)

| condition, in order | label |
|---|---|
| a known answer or the cross-shear null fails | NO VERDICT |
| s_tot > (floor - 0.30) / 2 | NO POWER (readings reported) |
| R + 2 s_tot >= floor and R - 2 s_tot > 0.30 | **PRESENT** |
| R + 2 s_tot < floor and R - 2 s_tot <= 0.30 | **ABSENT** |
| R + 2 s_tot < floor and R - 2 s_tot > 0.30 | **REDUCED** (an extended field below the law's own level) |
| R + 2 s_tot >= floor and R - 2 s_tot <= 0.30 | NOT SEPARATED |

- REDUCED is added to the brief's four labels because "below the law and above absence, both at 2 sigma" fits none of them.
- If R + 2 s_tot < 0 the label stays ABSENT and RESULT.md must say first that the outer bins fall below even the enclosed-mass
  term, so the model does not describe them.
- **Bracket rule.** B1, B2 and B3 are labelled the same way. If any of them gives a definite label (PRESENT, ABSENT, REDUCED)
  different from the primary's definite label, the final label is NOT SEPARATED. A bracket that reads NO POWER or NOT SEPARATED
  does not override.

**What each label would mean (a reading; it relabels nothing).** Late ABSENT with early PRESENT: the type split HE1 needs is what
the staged data show once neighbours are modelled. Late PRESENT: disc galaxies carry their own field beyond the inner window at
the law's level, against that split. REDUCED: a field that falls short of the law's own level. NOT SEPARATED or NO POWER: the
staged data cannot decide. **Direction of the main limit:** the catalogue is flux-limited, so unseen neighbours stay in the own
term and every own amplitude is an upper bound. ABSENT is robust to that; PRESENT is not.

## Reported, not gated

R1 every amplitude per class, both designs; R_mid = a[middle] / a[inner] from the secondary design. R2 early minus late,
R_ext(early) - R_ext(late), with the joint jackknife. R3 redshift halves (lenses split at the median z): R_ext per half and the
difference; if the high-z half exceeds the low-z half by more than 2 sigma, RESULT.md flags unseen neighbours in the own term.
R4 outer window cut to bins 0-2 (the brief's "three lowest bins") and, separately, bin 0 dropped (its cells are capped at 3 Mpc).
R5 the neighbour share of the model in bins 0-6 at the fitted amplitudes. R6 the same fit with the lens set restricted to KO1's
host-free flags (the KO1 lead, now with neighbours modelled). R7 KO1-style plain stacks for all late and all early lenses (window
amplitudes and R_s). R8 the untyped-as-early bracket if it runs. R9 the cross-shear fit's amplitudes.

## Known answers (all must pass, else NO VERDICT)

- **KA-0** KO1's KA1 (per-lens sums reproduce `cfg96_stack` to 1e-9); every lens found in the pool by position with equal log M*;
  the catalogue type of every lens equals `typ`.
- **KA-1** (a) KO1's host-free scan (Delta 0.3 dex, W 230 Mpc, radius R_h, KO1's comparisons) gives 40,667 lenses, and KO1's
  plain-stack window amplitudes for host-free late and early (outer, middle, inner, A and s, both footings) are reproduced to 1e-6
  relative against KO1's `ko1_extra.json` (E1; these are the RESULT-table numbers at full precision). (b) The own columns with every amplitude 1 equal
  KO1's law cells in all 13 bins to 1e-6 relative, both footings. (c) Coverage: no cell with WW > 0 lacks a model value.
- **KA-2** (a) the centre-point kernel against KO1 E8's closed form to 1e-9; (b) the tabulated band kernels against a brute-force
  evaluation of the definition (the band drawn as 200,000 point masses, each with E8's exact annulus formula) at 300 random
  (band, cell, separation) configurations per footing: |table - brute| <= 0.01 |brute| + 0.003 max|brute| of that band;
  (c) a uniform sheet of finite bands and points scattered around a lens out of the bands' reach gives a mean kernel within
  3 Monte Carlo errors of zero; (d) at separation 1e-3 l_j the table equals the concentric closed form to 0.5 %.
- **KA-3** (a) planted neighbours: 2,000 synthetic pool objects (seed 52) near random lenses at known offsets, windows and
  classes; the change in every lens's columns (cross-talk between lenses included) equals a brute-force loop over all
  (lens, synthetic object) pairs to 1e-6 relative. (b) Plant and recover: data replaced by the model at chosen amplitudes plus
  the measured cross-shear sums as noise, for (i) every amplitude 1 and (ii) late types truncated (ext = 0 for both late
  classes, all else 1); every recovered amplitude within 3 jackknife sigma of the planted one. The plants' labels are reported
  (expected PRESENT / PRESENT and ABSENT / PRESENT wherever the type has power).
- **KA-4** 100 random halvings of the lenses (seed 52): z = (A_1 - A_2) / sqrt(s_1^2 + s_2^2) of the weighted ext amplitude
  sum_m W_tm a[(t, m), ext] has a standard deviation in [0.8, 1.2] for each type.
- **Null** the fit with WX in place of WG: sum_m W_tm a[(t, m), inner] and sum_m W_tm a[(t, m), ext] within 2.5 sigma of zero
  for each type, both footings.

## MUTATE (separate outputs `ko2_MUTATE.json` / `ko2_MUTATE.out`; each must bite)

- **M1** lens type labels permuted within cells of lens-mass tercile x redshift half (seed 52); own columns follow the permuted
  labels, neighbours keep theirs. R_ext(early) - R_ext(late) must fall within 2 sigma of zero. If the true difference is itself
  within 2 sigma, M1 has no power: say so.
- **M2** neighbour positions shuffled: shuffle 1 in place of the real positions, the mean of shuffles 2-5 subtracted. The
  neighbour share of the model in bins 0-6 must fall within 2 sigma of zero. If the true share is itself within 2 sigma, M2 has
  no power: say so.
- **M3** late lenses' WG in bins 0-6 multiplied by 0.4: R_ext(late) must fall by more than 2 sigma (joint jackknife) below its
  unmutated value.

## Hand estimates (mine, before freezing; to be checked, not trusted)

- The brief's estimate of 0.2 on R_own(late) is too optimistic for a[outer] / a[inner] (toy: 0.37 before neighbour columns). I
  expect the secondary R_own to read NO POWER for late types and possibly for early types.
- Primary: s_tot near 0.25 for late and 0.15 for early. Hosted late lenses in KO1 carry more outer signal than inner
  (1.50 against 1.28), so neighbours matter; after modelling them I expect R_ext(late) 0.3 to 0.8 and R_ext(early) 0.8 to 1.1.
  Most likely labels: late NOT SEPARATED, early PRESENT.

## Limits known before running

L1 flux limit (own amplitudes are upper bounds; R3 shows the size). L2 neighbours are placed at the lens's distance with the
lens's critical density. L3 photo-z: the window holds many chance projections; their mean is removed, their realisation stays
in the columns. L4 the reach R_h + 2 Mpc leaves out correlated neighbours further away. L5 no boost or random subtraction in
the staged estimator (KO1's R7 compares with B21's points). L6 B21's hot-gas variant: unmodelled gas mass at Mpc radii would
sit in the own term. L7 a satellite's tidal truncation is not modelled; B3 (untied) is the bracket for it.

## Compute

One thread, under 2 GB; tables and per-lens neighbour columns cached in the session scratchpad (outside the repo) and deleted at
the end. Expected tens of minutes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
