# PA1 AMENDMENT_A1: forward-model reanalysis. Stated before any number from the catalogue

Committed alone, before the three files are fetched. **Post-PA1, not blind.** PA1's verdict and forecast are on record: this likely can't decide (my estimate 85 %), since the A - R gap is 0.40-0.45 mm/s/yr at minimum against per-pulsar scatter of order 1.6 published. I know the catalogue's column names and sizes from its README and server only. FROZEN_CRITERIA stands except where changed here. Downloads relayed as approved by the coordinator, exactly three files; logged in FETCH_LOG.md. Untrusted data: parse only, python -I, scripts outside data/.

## Data and heights
Primary: v3/binary_only.csv, ALOS_PB, ALOS_PB_ERR, GL, GB, DIST. Secondary: v3/data.csv, ALOS_PB where present else ALOS_PS. Cut: DIST <= 3 kpc, non-null acceleration and error. No outlier cut. Each pulsar at its own height: this replaces PA1's height range. Sun at R0 8.122, z 0.

## Model
a_los = (a(x_p) - a(x_sun)) . n, n from Sun to pulsar, positive away. a from UX5's solver, axisymmetric, mirrored in z, on UX5's grid. Forms A, Q: grad Phi. Form R, as UX5's core: a_R = a_R,N + g_c(R), a_z = a_z,N - g_c(R) z / R, with g_c from in-plane Newtonian g_b at R. Cells: in-prior, v_c in line for both A and R, same baryons; A solved on all of them.

## Nuisances
N1, primary: Solar acceleration offset, 3 vector, plus an even vertical term b1 |z| n_z, all linear and profiled. No term odd in z, which could absorb the form gap. N0: none, reported.

## Statistics
For each cell, form, footing: Gaussian lnL with per-pulsar variance err^2 + s^2, s free and profiled per fit. Lorentzian with xi free as check. dL = 2(lnL_A - lnL_R) same baryons; also Q - R.
K estimate: scale lambda on the form's vertical field only, K_est = lambda K_form(1.1), with profiled error. Compare with 66.4 +- 2.2 and line top 70.8.

## Labels, per sample and footing, on N1
- **SEPARATED**: |dL| >= 9 in every cell, same sign; same sign under Lorentzian; survives dropping any one pulsar at |dL| >= 9 at the median cell; mock power below >= 50 %.
- **LEAN**: median |dL| >= 4, not SEPARATED. No claim.
- **NOT SEPARATED**: otherwise.
Overall: **DECIDED** only if binary-only is SEPARATED, same sign, on both footings. Otherwise **CANNOT DECIDE**. A decision bears on these two forms at these baryons only; it reinstates nothing.
K_est against the line: TENSION if |K_est - 66.4| >= 3 sigma with both errors in quadrature, else NO TENSION. Per form, footing. Family dependence stated.

## Mock power
200 mocks per footing at the median cell: form A or R plus Gaussian noise with its fitted s and the real errors, same positions. Fraction reaching |dL| >= 9 right sign.

## Checks
- Geometry known answer: a log potential plus a linear a_z through the model code, against the textbook planar formula a_los = -cos b (V^2/R0)(cos l + beta/(sin^2 l + beta^2)) - alpha z sin b, beta = (d/R0) cos b - cos l. To 1e-6, on an analytic field.
- ALOS_PB recomputed from PBDOT, SHK, GR, PB where columns allow: report the worst difference relative to error. Report, not a gate on the data; any large mismatch is published.
- Sign check: the correlation of data with form A, N0, must be positive, or the sign is wrong.
- UX5 K(1.1) recovered.
- Rerun byte-identical.
- MUTATE twins: shuffled ALOS_PB among pulsars with fixed seed: must lose signal; K_est error similar, K_est must fall by at least half or be consistent with zero. Planted A data, error / 20: must give SEPARATED. Form Q nu = 1: must equal Newton.
- **Fix for PA1's unmet form A MUTATE:** run AQUAL with the density times 1e8 and potential divided by 1e8. That is the nu -> 1 limit with no edit to P4's solver. Form A must equal Newton to 0.5 %, so the gap changes. No separate flag if it passes.

Post-result, no label: distance scaled coherently by +- DIST_ERR; two listed outliers J0125-2327, J1400-1431 removed; Sun at z 20 pc; round rule with r instead of R.

kappa = 1/2 FITTED. Footings never pooled. Not theory closed.
