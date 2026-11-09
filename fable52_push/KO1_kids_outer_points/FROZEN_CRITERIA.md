# KO1 FROZEN CRITERIA: are KiDS's outer points the lens's own field?

Committed alone, before any KO1 script exists and before any host-split lensing number has been computed.
TEST lane, quarantined. Relabels nothing. Not registered. Footings never pooled (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2).

## Why

SWT1 reduced every action-based switch on the law to one conflict. Keeping the law on over KiDS's full range needs the
law-on regions to fill 0.29 of space; the CMB-lensing line allows 0.0231, which reaches g_bar >= 7.5e-15 m/s^2. The 16 KiDS
points below that (the four lowest g_bar bins of each of the four mass bins) decide the class.

The record already holds two facts about those points that have never been turned into a gate:

- CFG502: the record's "isolated" lenses are not isolated. The isolation window is |Delta chi_phot| < 10 Mpc, while two
  galaxies at one true redshift differ in photo-z distance by about 115 Mpc. A satellite's central vetoes it 7 % of the time.
- CFG903: of the catalogue's neighbour term around the isolated lenses at 1 Mpc, 40 to 87 % comes from neighbours more
  massive than the lens ("hosts").

So the question is put to the data directly: **remove the lenses that have a more massive galaxy inside their own measured
range, along a line-of-sight window wide enough to catch photo-z scatter, and ask whether the outer signal is still at the
law's level.**

## What I have seen before freezing (disclosure)

- B21's Fig. 9 points (used in SWT1 E3; the law's chi2 over the 59 points with per-point errors is 279).
- The README numbers of CFG109, CFG110, CFG116, CFG502, CFG903 and CFG912, including: the isolation windows W10 / W20 / W30
  hold 181,477 / 93,020 / 57,265 lenses; CFG502's environment term E is 0.50 / 0.86 Msun/pc^2 at 2.17 / 1.04 Mpc for W10 and
  0.35 at 2.2 Mpc for W30; "the outer signal drops with stricter isolation" (CFG502 N1, not quantified for these bins).
- The array names and shapes of the staged files. No lensing statistic split by host count, host mass or any projected
  isolation has been computed or seen. The B21 files for GAMA, the all-galaxy sample and the hot-gas variant have not been
  opened.
- Hand estimate (mine, before freezing, to be checked and not trusted): if hosts carry 30 to 50 % of the W10 outer signal,
  the host-free amplitude is about 0.5 to 0.8 of the law with an error near 0.2. I expect NOT SEPARATED or BELOW THE LAW.
- A limit of the design, known before freezing: CFG903 found that for the most massive bin 60 % of the catalogue neighbour
  term at 1 Mpc comes from neighbours less massive than the lens. The cut below removes more massive hosts only, because a
  veto on every comparable galaxy over a 460 Mpc line of sight leaves no lenses.

## Inputs (all on disk; nothing is downloaded; the staged files are git-ignored)

In `real_research/data/lensing_rar/`:

- `lr_lenses.npz`: the record's 181,477 isolated lenses (ra, dec, z, logM, Mgal, typ, chi).
- `cfg110_perlens.npz`: per-lens tangential sums `WG`, weights `WW`, counts `NN` in the 15 g_bar bins
  (edges `gbar_edges`, 1e-15 to 5e-12 m/s^2, each lens's radii set by its own Mgal; pairs within 3 Mpc physical; sources with
  Z_B > z_l + 0.2). ESD = sum WG / sum WW in SI (kg/m^2); g_obs = 4 G ESD.
- `cfg116_perlens.npz`: cross sums `WX`, near / far source sums.
- `cfg96_isoflags.npz` (f20, f30) and `cfg96_stack.npz` (the 50 jackknife patch labels and the W10 / W20 / W30 patch sums).
- `KiDS_DR4_brightsample.fits` with `KiDS_DR4_brightsample_LePhare.fits`: the galaxy catalogue. Conventions are the
  record's (CFG502 / CFG903): r = MAG_AUTO_CALIB, z = zphot_ANNz2, log M* = MASS_MED + 0.15, chi from the record's DC
  (flat, Omega_m 0.3, H0 70), early type = u - r > 2.0, Mgal = M* (1 + 10^(-0.69 log M* + 6.63)).
- `brouwer2021_rar/`: B21's published tables and covariances (isolated, GAMA isolated, mass bins, all-galaxy mass bins,
  hot gas), with the multiplicative bias applied as its README states.

## Definitions

**Outer bins.** O = the four lowest g_bar bins of the staged grid (edges 1.00, 1.76, 3.11, 5.49, 9.69 x 1e-15 m/s^2). They
are B21's four lowest bins, the 16 points SWT1 E3 put outside the wall. Bracket: the three lowest only.

**Law model for a stack.** For lens l and bin k the pairs lie between R_lo = sqrt(G Mgal / g_hi) and
R_hi = min(sqrt(G Mgal / g_lo), 3 Mpc). The model for that cell is the area-weighted mean over that annulus of
g_law(g) = nu(g / a0) g with g = G Mgal / R^2 and nu(y) = 1/2 + sqrt(1/4 + 1/y). The stack model for a lens set S is
M_k(S) = sum_l WW[l,k] m[l,k] / sum_l WW[l,k]. No free constant.

**Amplitude.** A(S) = sum_k (D_k M_k / s_k^2) / sum_k (M_k^2 / s_k^2) over the bins of O, with D_k = 4 G ESD_k(S) and s_k
the delete-one-patch jackknife error of D_k for that same set. The error of A is the delete-one-patch jackknife of A itself
(50 patches, s_k held fixed). A = 1 means the stack sits on the law.

**Hosts.** Neighbour pool: catalogue objects with r < 20, 0.02 <= z <= 0.8, finite log M* > 7, masked 0 or 1 (a veto by a
masked object is kept: it costs lenses, not purity), the lens itself excluded. A host of lens l is a pool object j with

- log M*_j >= log M*_l + Delta,
- projected physical separation d = theta chi_l / (1 + z_l) <= R_h,l, where R_h,l = min(3 Mpc, sqrt(G Mgal_l / 1e-15 m/s^2))
  is the lens's own outermost measured radius,
- |chi_j - chi_l| < W.

**Host-free** = no host. **Hosted** = at least one. Primary: Delta = 0.3 dex, W = 230 Mpc (twice CFG502's measured pair
scatter). Inside R_h a uniform absence of projected hosts makes no shear, so the selection carves no hole inside the range it
is graded on.

**Choice of the cut, from weights only.** Let f_w be the host-free share of sum WW over O. Use the first setting in the
order (0.3, 230), (0.3, 115), (0.5, 230), (0.5, 115) with f_w >= 0.20; if none reaches 0.20 use the one with the largest
f_w. WW holds no shear. All four settings are reported.

**Two-phase exterior (what a variational switch predicts for a truly isolated lens outside its wall).** Wall at the upper
edge of O (g_bar 9.69e-15, inside SWT1's allowance). By SWT1 T1 the region inside shows exactly M_b from outside; the swept
share X M_b is put in a thin shell at the wall, which is the placement that gives the largest exterior signal (a share spread
further out encloses less). For R outside, 4 G DeltaSigma = (4 / pi) (1 + X) G Mgal / R^2, area-averaged as above. Two
values: X = OD / OB = 5.562 (SWT1's share, as in `swt1.py`) and X = 53.64 (ten times 5.364, the census cap on the catchment
supply in CFG804, the largest share the record has used). A_II is this model's amplitude against the law model on the same
lens set, on each footing.

**Selection control (mass scatter).** A lens whose stellar mass is estimated too high is more likely to be host-free
(fewer galaxies exceed it) and its model is then too high, which lowers A. The size of this is measured, not assumed: the
host-free flags are recomputed with every lens's log M* shifted by +0.1 and -0.1 dex (threshold and R_h both follow the shifted
mass), giving the slope b = d ln P(host-free) / d log M*, per lens-mass tercile. For a mass error sigma_M the mean
overestimate of the selected lenses is e = b sigma_M^2 dex, and the corrected amplitude is A_hf^c = A_hf 10^(e / 2)
(deep regime, model proportional to sqrt(Mgal)). sigma_M = 0.2 dex is used for the gate, 0.1 dex is reported.

## Primary statistic and labels (per footing)

A_hf = A(host-free), all types together, bins O, with its jackknife error s. The label is computed twice, with A_hf and with
the corrected A_hf^c (sigma_M = 0.2 dex, same s scaled by the same factor). If the two differ, the label is NOT SEPARATED.

| condition | label |
|---|---|
| a known answer or the cross-shear null fails | NO VERDICT |
| s > 0.20 | NO POWER (readings reported, no label) |
| A_hf + 2 s >= 0.891 and A_hf - 2 s > A_II(X = 53.64) | **LAW LEVEL HOLDS** |
| A_hf + 2 s < 0.891 and A_hf - 2 s <= A_II(X = 53.64) | **BELOW THE LAW, TWO-PHASE WINDOW** |
| A_hf + 2 s < 0.891 and A_hf - 2 s > A_II(X = 53.64) | **BELOW THE LAW, BETWEEN** |
| otherwise | NOT SEPARATED |

0.891 is the record's KiDS gate line, 0.05 dex, as a factor.

**What each label would mean.**
- LAW LEVEL HOLDS: a law-level signal survives the removal of more massive hosts, and it is above the two-phase exterior
  at the census cap. Leaked satellites then do not carry KiDS's outer points. With SWT1's allowance the variational switch
  class stays in conflict with KiDS. The cut does not remove neighbours of comparable or lower mass, so this label is an
  upper bound on the lens's own field, not a measurement of it; that loophole is reported (R3), not closed.
- BELOW THE LAW: the law over-predicts the outer signal of host-free lenses. Because the cut only removes mass, this
  direction is robust. The agreement of KiDS's outer points with the law in the record's gate is then carried in part by
  hosts, and the gate as used is not a clean test of a lens's own field. TWO-PHASE WINDOW: the switch class is open at the
  allowance. BETWEEN: neither the law nor the two-phase exterior at the census cap describes the host-free signal.
- NOT SEPARATED / NO POWER: the staged data cannot decide; say what would.

No label here relabels any lane in the record. Affected lanes would be listed as a pointer only.

## Reported, not gated

- R1: A for the disjoint isolation shells (W10 not W20; W20 not W30; W30) and A(hosted); the difference A(hosted) - A_hf
  with its joint jackknife error.
- R2: A_hf per type (late, early), per lens-mass tercile, per redshift half, and with the three lowest bins only.
- R3: A against the number of hosts (0, 1, 2, 3 or more).
- R4: the |Delta chi| histogram of hosts inside R_h out to 500 Mpc: the excess over the level at 300 to 500 Mpc measures the
  true-host share and the fraction the window catches.
- R5: near-source and far-source A_hf (`cfg116_perlens.npz`).
- R6 (published tables, full covariance): the outer amplitude of B21's GAMA isolated sample (spectroscopic isolation)
  against B21's KiDS-bright isolated sample; the isolated against the all-galaxy sample per mass bin; the hot-gas variant.
- R7: the W10 stack against B21's published isolated points in O (the record's sample is stricter than B21's and the
  estimator has no random subtraction, so this is a comparison, not an identity).

## Known answers (all must pass, else NO VERDICT)

- KA1: the per-lens sums, summed by patch and type, reproduce `cfg96_stack.npz` for W10, W20 and W30 to 1e-9 relative.
- KA2: the catalogue loader and the pair finder, run with the record's isolation (more massive than log M* - 1, comoving
  3 Mpc, window 10 / 20 / 30 Mpc), reproduce `lr_lenses.npz` exactly (605,531 candidates, 181,477 lenses, equal ra, dec, z,
  Mgal) and the flags f20 and f30 exactly. The host flags use the same function.
- KA3: WG x 1.3 gives A x 1.3 to 1e-12; WG = WW x the law model gives A = 1 to 1e-12 on both footings; WG = WW x the
  two-phase model gives A = A_II.
- KA4: jackknife calibration: for 200 random halvings of W10 (seed 52), z = (A_1 - A_2) / sqrt(s_1^2 + s_2^2) has a
  standard deviation in [0.8, 1.2].
- KA5: a synthetic host planted at a known offset and photo-z distance around 1,000 lenses is flagged for exactly those
  lenses.
- Null: the cross-shear amplitude of the host-free set over O (WX in place of WG, same weights and model) is within 2.5 s
  of zero.

## MUTATE (separate output files; each must bite)

- M1: host-free flags permuted within cells of type x mass tercile x redshift half (seed 52). The difference
  A(hosted) - A_hf must fall inside 2 s of zero. If the true difference is itself inside 2 s, M1 has no power: say so.
- M2: host-free lenses' WG over O multiplied by 0.4. The label must be BELOW THE LAW.
- M3: host-free lenses' WG replaced by WW x the law model. The label must be LAW LEVEL HOLDS.
- M4: the isolation rebuild with the mass threshold changed to log M* - 0.5. KA2 must fail.

## Lean

`KO1.lean`: the two-phase exterior against the law. With c = (4 / pi)(1 + X) > 1 the ratio is c / nu(y); it is below 1
exactly when y < 1 / (c (c - 1)); it increases with y; and it is at most c sqrt(y). A mutate twin must fail.

## Independent regrade

A second session re-derives the primary statistic and the label from this file alone, with its own code, before opening
any KO1 script or output. Its numbers are reported beside these.

## Compute

One thread, under 1.5 GB, minutes. The shear catalogue is not read.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
