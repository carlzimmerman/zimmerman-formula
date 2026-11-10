# KO2 AMENDMENT A3 (declared before any fitted amplitude of the main run has been opened): form B's predicted values

Committed alone, before the outputs of the main run (`ko2.out`, `ko2.json`, `ko2_MUTATE.*`) are opened. Requested by the lead
session after the owner chose the final form of the theory ("form B": the a0 law plus cold dark energy counted once, the law
being how the cold component sits around each galaxy). It adds one reported comparison. **It changes no frozen label, line,
bracket, design or tolerance, and relabels nothing.**

## What has been seen when this is written

- From the main run (two attempts): only known-answer lines and progress/memory lines. KA-0a, KA-0b, KA-1a, KA-1b, KA-1c,
  KA-2a to KA-2d and KA-3a pass. KA-1a reproduces KO1's host-free numbers, which were already disclosed in the criteria. The
  first attempt was stopped at 67 % of the neighbour pass because it held 2.4 GB, over the lane's 2 GB rule; the script now
  re-launches itself with macOS's `MallocMediumZone=0 MallocLargeCache=0`. The second attempt is running.
- **No fitted amplitude, ratio, plant recovery, null fit, MUTATE outcome or label from KO2 has been opened.** The monitor on
  the run log is filtered to known-answer failures, pass milestones and the runtime line.
- PD1: `RESULT.md` section "The share, per halo", the share and halo functions of `pd1.py` (lines 26-118 and its KiDS model),
  and the z = 0 share tables stored in `pd1.json`.

## Form B, as PD1's frozen rule (copied, not imported, not changed)

- Each galaxy has M_b = the record's Mgal (stars plus cold gas), for lenses and neighbours alike.
- The share is PD1's z = 0 Lagrangian share (the "ta" rule): 59.49 M_b canonical and 59.50 M_b alt. R_ms is the turnaround
  radius today from PD1's shell solver, with M_b (1 + R) and the footing's background from `qx15.json`.
- The phantom runs out to R_trunc, where M_ph(R_trunc) = share, with M_ph(r) = M_b (sqrt(1/4 + 1/y) - 1/2) and
  y = G M_b / (a0 r^2). If M_ph(R_ms) < share, R_trunc = R_ms and the leftover (share - M_ph(R_ms)) is spread as PD1's
  m_left(r) = leftover min(r, R_ms) / R_ms. Beyond, the galaxy is Newtonian with M_b + share. Interpolation in log M_b uses
  PD1's `halo_of`.
- Uncapped galaxies (log M_b below about 11.1) are truncated at one g_bar: g_t = a0 / (s (s + 1)) with s = share / M_b,
  about 2.6e-14 m/s^2 on the canonical footing. That is inside the middle band (bins 5-6).
- **Lensing convention:** PD1's own KiDS model, 4 G DeltaSigma_B(R) = G M_B(<R) / R^2. That is the same convention in which
  KO1 and KO2 write the law (4 G DeltaSigma_law = g nu(g / a0)). The projected surface density follows from it with
  Sigma -> 0 at infinity: 4 G Sigma_B(R) = -G M_B(R) / R^2 + 2 int_R^inf G M_B(R') / R'^3 dR'. For an uncapped galaxy this is
  the law's Sigma minus its value at R_trunc inside R_trunc, and zero outside.

## How the prediction is computed (script `ko2_formB.py`, reading the main run's cached columns)

1. Own form-B cell values for every lens: the cell average of G M_B(R) / R^2, with the quadrature split at R_trunc and R_ms.
2. Neighbour form-B columns built exactly as the main columns are: the same pool, reach R_h + 2 Mpc, window 230 Mpc, d >= 5 kpc,
   real positions minus the mean of the same five shuffles. The kernels come from J tables of form B's projected profile, with
   the same off-centre definition. There is one universal table for uncapped galaxies and tables at capped-mass nodes every
   0.25 dex, with the kernel interpolated linearly in log M_b. The resolution is 801 x 561, as frozen for the main tables
   before A1; it is checked by KA-B3.
3. Planted sums: WG = WW m_B / (4 G), with m_B = own + neighbours. They are used (i) without noise and (ii) with the measured
   cross-shear sums WX added as noise, as in KA-3b. They are fitted with the primary design, and with the secondary design,
   with the main run's normal matrix and jackknife.
4. **Form B's prediction** of R_ext(t) and R_own(t), per type and footing, is the noiseless recovered value. The noisy recovery
   is reported beside it with its jackknife error. Also reported: the per-class a[ext] / a[inner], and the planted truth (the
   rule's parameters: share, g_t, the capped fraction of lenses and of the pool, and R_trunc at the class medians).

## Known answers for this part (a failure here voids only this comparison, not the frozen labels)

- KA-B1: the transcribed share tables equal `pd1.json`'s z = 0 tables (share, R_ms, R_trunc, leftover at every node) to 1e-6
  relative, on both footings.
- KA-B2: with the truncation off (R_trunc infinite, no leftover), the own form-B cells equal the law's own cells to 1e-6. The
  universal form-B table equals the law's full profile (centre + inner + middle + outer + far, from the main tables) within
  KA-2b's tolerance at 300 configurations.
- KA-B3: the form-B kernels against A1's direct quadrature about the lens at 300 configurations (uncapped, and capped at three
  masses), under KA-2b's tolerance.

## What RESULT.md will report

For each type and footing:

- the measured R_ext with s_jk and the frozen s_tot;
- the law as the galaxy's own field: 1, and the frozen floor;
- form B's predicted value;
- the distance of the measurement from each prediction, in units of s_tot (and of s_jk);
- the same for the secondary R_own.

If the two predictions differ by less than 2 s_tot, RESULT.md says plainly that the data cannot tell them apart for that type.

## Hand estimate (before computing)

Form B truncates every uncapped galaxy inside the middle band and removes a uniform sheet S(g_t) inside R_trunc. That lowers
the ext band most. I expect form B to predict R_ext of about 0.1 to 0.4 for both types and R_own near zero or below. Form B
should then read like the "absent" end for late **and** early types alike.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
