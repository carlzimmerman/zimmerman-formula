# OQ1: one action-native scalar for both walls. NO VERDICT as frozen (M1 power check fails); S1 reads DEAD on both footings

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (3d8e38ffb2), committed alone before any
script or number. Script: oq1.py (one thread, nice 15, about 15 min, well under 1 GB). Outputs: oq1.json / oq1.out (main),
oq1_MUTATE_M1.json (planted law), oq1_MUTATE_M2.json (planted step), oq1_MUTATE_M3.json (Newton).

**Label as frozen: NO VERDICT.** Section 6 says that if M1 (a planted true one-quantity law) does not pass S1 and S3, "the run
says NO VERDICT". M1 reports false conflicts on both footings, so the frozen label is NO VERDICT, not DEAD.

**S1 reading: DEAD on both footings, every start (F0 = 0, 1, 10), both group f* (0, 1).** In every run, SPARC and the hot classes
share q bins with disjoint F intervals. The widest conflicts are 3-5x wider than any false conflict the planted law produced
(post-freeze margin reading below).

The step sits at fixed q, as stated in advance. QX20 found it at fixed g_N, and the AC2q charge does not lift it. The web arm is
not where it dies: at the lensing-allowed F the web's q stays below 4, while every host point sits above 10^2.3.

## Known answers (all PASS; nothing was graded until they did)

| KA | canonical | alt | line |
|---|---|---|---|
| KA1 GB1 L0 class means X, E, S | +0.467499, +0.209888, +0.027383; max \|d\| 2.9e-7 | +0.434523, +0.188763, -0.000603; 4.5e-7 | 1e-6 |
| KA2 L1 ellipticals vs QX26 D_imf | +0.093043, 2.5e-7 | +0.074252, 3.2e-7 | 1e-6 |
| KA3 web lensing amplitude at F = 1 vs SV5 iter_1 | 74.7424, rel 0 | 89.3630, rel 0 | 1e-3 rel |
| KA4 Sigma_* / rho_DE and web fractions F_f(z) vs SV5 iter_2 | 7.9690, max \|dF\| 0 | 5.9983, max \|dF\| 0 | 1e-3 |
| KA4 deep-MOND point-mass phantom (this lane's rho_ph, 100 r_M) | ratio 0.99999 | | 1e-4 |

## Inputs read from the JSON

| | canonical | alt |
|---|---|---|
| F_web,max (largest uniform F with lensing r <= 1.0722 on SV5 iter_1's statistic) | **0.00481** (r 1.0722, shape dchi2 0.001) | **0.00435** (r 1.0722, dchi2 0.001) |
| SPARC uniform-F band, \|Z\| <= 0.057 (all 2696 points) | 0.828-1.336 | 0.738-1.189 |
| Class mean F_need: X-COP / groups f*0 / ellipticals / Coma UDGs / bright M31 / LG field | 3.92 / 2.64 / 1.61 / 17.1 / 3.02 / 1.37 | 3.50 / 2.38 / 1.42 / 15.4 / 2.74 / 1.24 |
| log10 rho_ph/rho_DE at F = 1 (min / median / max): SPARC; X-COP; groups; ellipticals; Coma UDGs; bright M31; LG field; Solar System | 3.01/4.74/6.81; 2.47/3.02/3.63; 2.26/2.61/2.92; 4.02/4.73/5.22; 4.09/4.49/4.65; 3.76/5.28/5.71; 5.08/5.60/5.92; 13.4/13.8/14.4 | 2.89/4.62/6.72; 2.35/2.90/3.51; 2.14/2.49/2.80; 3.90/4.62/5.12; 3.96/4.37/4.53; 3.64/5.14/5.61; 4.96/5.48/5.81; 13.3/13.7/14.3 |

No point has rho_ph <= 0. All 38 bright M31 + LG field dSphs carry GB1's inverted x (0 missing).

## q range per class at the self-consistent fixed points (log10 q, min-max; groups f* = 0)

| Class | canonical F0 = 1 | canonical F0 = 10 | alt F0 = 1 | alt F0 = 10 |
|---|---|---|---|---|
| SPARC | 0.30-7.72 | 0.30-7.72 | 0.30-7.64 | 0.30-7.58 |
| X-COP | 2.83-4.27 | 2.94-4.37 | 2.67-4.09 | 2.79-4.21 |
| groups | 2.53-3.42 | 2.53-3.42 | 2.36-3.27 | 2.31-3.58 |
| ellipticals | 4.32-5.22 | 4.49-6.06 | 4.01-5.12 | 4.31-5.57 |
| Coma UDGs | 4.51-5.46 | 5.09-5.65 | 4.33-5.20 | 4.96-5.53 |
| bright M31 | 3.76-5.75 | 4.72-6.63 | 3.64-5.76 | 4.56-6.49 |
| LG field | 5.08-5.95 | 5.14-6.14 | 4.93-5.77 | 4.93-5.98 |
| Solar System | 13.43-14.41 | 14.43-15.41 | 13.34-14.32 | 14.34-15.32 |
| linear web (z 0.25-3, 128^3 x 5) | < 0.6 (99.87 % of mass in 0.2-0.4) | same | < 0.6 (100.0 %) | same |

The F0 = 0 start is a degenerate fixed point. Every class whose band at q = 2 contains 0 (groups, which have an empty band
there, and the Solar System) stays at F = 0, q = 2. It is graded and reads DEAD for the same SPARC / hot-class bins.

## S1 bin table (the conflicts; the full table per run is in oq1.json `bins`)

Every run is DEAD. The number of empty bins and the widest gap, per run:

| Run | canonical: empty bins, widest gap (dex) | alt: empty bins, widest gap |
|---|---|---|
| f*0, F0 = 0 / 1 / 10 | 14, 0.595 / 14, 0.830 / 15, 0.774 | 17, 0.961 / 13, 0.597 / 15, 0.688 |
| f*1, F0 = 0 / 1 / 10 | 14, 0.595 / 15, 0.830 / 15, 0.774 | 17, 0.961 / 13, 0.597 / 15, 0.688 |

The conflicts are the same in every run:

- **SPARC vs X-COP at log q 2.8-4.4.** This is the multi-point conflict, with 6-7 bins in every run and 2-7 X-COP points against
  up to about 260 SPARC points per bin.
  - Canonical F0 = 1, bin 3.8-4.0: SPARC (169) 0.918-1.313 against X-COP (6) 4.127-5.359, gap 0.497 dex.
  - Alt F0 = 1, bin 3.6-3.8: SPARC (136) 0.828-1.18 against X-COP (6) 3.67-4.77, gap 0.493.
  - Gaps range 0.35-0.53 canonical and 0.37-0.52 alt.
- **SPARC vs groups at log q 3.0-3.6.** Gaps are 0.31-0.50 where the groups' 80 % band lands there.
- **SPARC vs Coma UDGs at log q 4.4-5.6.** Gaps are 0.27-0.85 dex. The UDGs need F 2.5-95 where SPARC allows 0.2-1.5.
- **SPARC vs bright M31 at log q 5.4-6.0.** Gaps are 0.05-0.96. Coma UDGs vs LG field at 4.8-5.2 gives 0.35-0.41.
- **Linear web vs hosts: no shared bin.** The web shares its bins (log q 0-0.6) only with the few SPARC points pinned at F = 0,
  and there the intersection {0} with [0, F_web,max] is non-empty. The web arm does not produce a conflict.

## MUTATE (power)

| Twin | Required | canonical | alt | Verdict |
|---|---|---|---|---|
| M1 planted law F = 1 + 3 (q/q_med)^0.5 + noise at measured errors | S1 no conflict, S3 pass, every start | S1 EMPTY in 2-4 bins (max gap 0.157) | S1 EMPTY in 1-3 bins (max gap 0.369) | **NO POWER TO FIND, as frozen** |
| M2 planted step (+0.3 dex on X-COP, groups, ellipticals at fixed q) | S1 DEAD | DEAD, 11-15 bins, max gap 0.252 | DEAD, 10-11 bins, max gap 0.369 | BITES |
| M3 Newton (F = 0) | G1 fails | Z +0.431 | Z +0.431 | BITES |

Why M1 fails:
- Every M1 false conflict except the zero-gap pairs comes from one or two noisy points in a bin, for example one bright M31 dSph
  against 42 SPARC (canonical log q 8.2-8.4, 0.157).
- The rest: one LG field dwarf (0.011-0.013), two Coma UDGs (0.007), and X-COP vs groups (gap 0.000, touching ends).
- On alt the widest (0.369) is one bright M31 against one LG field dwarf, with no SPARC involved.
- The per-bin class intervals have no floor for single-point bins, so measurement noise at high planted F produces disjoint
  intervals. That is a defect of the frozen method, not of the planted law.

M2's widest gap does not separate from the M1 null on alt (both 0.369). So M2's "power to kill" is shown only in bin count
(10-15 empty bins against 1-4), not in gap size.

## Post-freeze margin reading (reported, not a label)

`post_freeze_margin_reading` in oq1.json counts the conflicts wider than the widest false conflict the planted law produced on
the same footing:

| | M1 null max gap | runs with a conflict above it | conflicts above it per run | widest |
|---|---|---|---|---|
| canonical | 0.157 dex | 6 / 6 | 11-13 (SPARC vs X-COP / groups / UDGs / bright M31; Coma UDGs vs LG field) | 0.830 |
| alt | 0.369 dex | 6 / 6 | 8-13, of which 6-7 are SPARC vs X-COP bins in every run | 0.961 |

On this reading the data's SPARC-X-COP conflict (6-8 bins per run, 0.35-0.53 dex, multi-point on both sides) is not the M1
artefact. It is 2-3x the canonical null, and above the alt null (0.369) in every SPARC-X-COP bin (0.370-0.517). This is the DEAD the
criteria predicted. It is not the frozen label, because the frozen power rule failed.

## Side tables (reported, no label)

q_b = rho_b,local / rho_DE and q_t = |E| / (4 pi G rho_DE), log10 min / median / max. Galaxy and cluster rows are from the
local baryon profile. Web rows give the 5 / 50 / 95 percentiles (linear, not log), per z.

| Class | canonical log q_b | canonical log q_t | alt log q_b | alt log q_t |
|---|---|---|---|---|
| SPARC | -1.41 / 4.40 / 8.39 | 1.99 / 4.53 / 8.76 | -1.58 / 4.24 / 8.22 | 1.82 / 4.36 / 8.60 |
| X-COP | 1.92 / 2.70 / 3.47 | 1.94 / 2.51 / 3.42 | 1.75 / 2.53 / 3.31 | 1.78 / 2.34 / 3.25 |
| groups (f*0) | 1.18 / 1.71 / 2.10 | 1.06 / 1.44 / 1.97 | 1.01 / 1.55 / 1.93 | 0.89 / 1.27 / 1.81 |
| ellipticals | 2.74 / 4.30 / 5.60 | 4.00 / 5.27 / 6.29 | 2.58 / 4.13 / 5.43 | 3.84 / 5.10 / 6.12 |
| Coma UDGs | 2.75 / 3.29 / 3.53 | 2.90 / 3.43 / 3.68 | 2.59 / 3.12 / 3.37 | 2.73 / 3.27 / 3.51 |
| bright M31 | 1.73 / 3.89 / 4.43 | 1.87 / 4.04 / 4.58 | 1.58 / 3.70 / 4.29 | 1.72 / 3.85 / 4.43 |
| LG field | 3.92 / 4.52 / 5.19 | 4.07 / 4.66 / 5.33 | 3.74 / 4.34 / 5.06 | 3.89 / 4.48 / 5.20 |
| Solar System | (0: point mass) | 19.35 / 20.55 / 22.30 | (0) | 19.19 / 20.39 / 22.13 |
| web z 0.25 (q_b; q_t, linear) | 0 / 0.135 / 0.346 | 0.33 / 0.64 / 1.02 | 0 / 0.093 / 0.237 | 0.22 / 0.44 / 0.70 |
| web z 3 | 1.95 / 4.43 / 6.90 | 3.84 / 7.49 / 11.96 | 1.34 / 3.03 / 4.72 | 2.63 / 5.13 / 8.19 |

Both side scalars put X-COP and the groups below the SPARC median and overlapping SPARC's range, as q does. No labels are
attached.

## Disclosed (implementation readings and post-freeze changes)

1. **Section 3 iteration.** The criteria's "q_k+1 = q[F_k(q_k)]" is implemented as follows. At each step every point's F is
   moved to the nearest value its class allows in the point's current bin; q = F rho_ph/rho_DE + 2 is then recomputed. Starts
   F0 = 0, 1, 10.
   - Several runs hit the 200-iteration cap while cycling between bin memberships: canonical f*0 F0 = 1 and F0 = 10, f*1 F0 = 1;
     alt f*0 F0 = 10.
   - They are graded on their final state. Every start reads DEAD, so the "worst" rule gives the same answer.
2. **Per-bin class intervals.** The class's own gate statistic is applied to its points in each bin.
   - SPARC \|mean\| <= 0.057, X-COP <= 0.05, ellipticals <= 0.15, UDGs <= 2 sigma_U.
   - Groups: >= 80 % (G3's 16 of 20) of the bin's group points inside 2 sigma_log.
   - Bright M31: the class bootstrap sigma (10,000, seed 21), scaled by sqrt(N/n_bin).
   - LG field: bootstrap CI of the median relative to the SPARC anchor. The anchor is the SPARC mean residual at the midpoint of
     the all-SPARC band.
3. **IMF b fills.** GB1 L1 needs a stellar sigma that SPARC, X-COP and the groups do not carry. GB1's frozen bracket middles are
   used: SPARC bulge 150 / disc 60, X-COP BCG 300, groups 250 km/s.
4. **2X = 2 rho_DE everywhere** (X/X_bg = 1/(1+Phi)^2 is about 1). It enters hosts and the web alike.
5. **rho_ph construction.** SV5 iter_2's spherical host formula is applied to a local power law of each class's baryon mass
   profile.
   - SPARC: M = vb2 r / G, with the slope from the galaxy's own points.
   - X-COP: QX5's gas + stellar FITS profiles, log-interpolated.
   - Groups: the frozen power law between R2500 and R500.
   - Ellipticals: Hernquist.
   - UDGs and dSphs: Plummer at r_h, with the mass normalised to GB1's x.
   - Solar System: the Sun's own point-mass phantom plus the Galaxy's at the Sun (6e10 Msun at 8.2 kpc), summed.
6. **Bins** are anchored at multiples of 0.2 dex in log10 q.
7. **M1 / M2 are static-only.** The web arm is excluded, because a planted law cannot be planted into the lensing statistic.
   - Noise per point at the measured error: SPARC eV, X-COP eM, groups sigma_log, UDG esig, dSph sdMC[Newton]. Ellipticals carry
     no errors on disk, so 0.05 dex is used.
   - The Solar System's planted band is F_true +- 1 %.
   - "Hot" for M2 means X-COP, groups and ellipticals (the X-ray classes).
   - q_med is the median q of the static points at the main F0 = 1 fixed point.
8. **Label step (post-freeze code change, disclosed).** The first full run's script printed "DEAD" from S1 alone and did not
   apply section 6's M1 rule (that line is still in oq1.out). `finalize()` was added to apply the frozen rule and the margin
   reading. It was run with `python3 oq1.py --label` on the same outputs, with no recomputation. The main path now calls it too.
   The same commit also fixed an empty-list crash in the side table (the Solar System's q_b is 0).
9. **S2 and S3 were not run on the data,** because S1 is empty. S3 is implemented (leave-one-class-out, 0.5 dex extrapolation
   rule) but is reached only by S1-holding runs, and none occurred, M1 included.
10. The web is SV5's 128^3 / 2000 Mpc Gaussian realisation (seed 5). Finer cells raise web charge peaks (SV5), so the web q
    range is a floor. At F_web,max about 0.005 a web cell would need rho_ph of about 4e4 rho_DE to reach the lowest host q
    (10^2.3). That is not checked at finer resolution.

## What it says

1. **The web arm works.** At the lensing-allowed multiplier (F_web <= 0.0048 / 0.0044), the self-consistent charge keeps the
   linear web at q < 4. Every host sits at q >= 10^2.3, so the AC2q charge does separate hosts from the law-off web by about
   2 dex. This is SV5 iter_2's conditional A-web branch, now made self-consistent.
2. **The hot arm fails, as predicted.** At fixed q, X-COP needs F 2.1-5.8 where SPARC allows 0.7-1.3, and the Coma UDGs need
   2.5-95. The charge q is set by g_N and its slope, like the depth, density and support keys before it, so it inherits QX20's
   step at fixed g_N.
3. **The run is not a clean DEAD,** because the frozen power twin M1 fails on single-point bins. A rerun under new criteria
   with a per-bin floor (for example n >= 3 per class per bin) would be needed to turn the S1 reading into a graded label.

Kappa = 1/2 FITTED; not theory closed.
