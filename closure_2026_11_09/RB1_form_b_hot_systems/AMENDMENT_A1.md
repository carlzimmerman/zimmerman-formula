# RB1 AMENDMENT A1 (POST HOC): KA-2's definition, one reported Bullet row's normalisation, one reported X-COP bracket

Criteria ef53f5512f. Committed alone, before the final run. Relabels nothing. kappa = 1/2 FITTED; not theory closed.

**Timing, disclosed.** Two full runs of `rb1.py` exist (not committed). I have seen every number and label they print. Under the
frozen text they read, on both footings: gate 1 CONSISTENT; gate 2 CONSISTENT; **gate 3 NO VERDICT** (KA-2 failed in its last bin;
gate 3's own graded bins were -0.007 / +0.033 / +0.006 / -0.030 / -0.041, which would be CONSISTENT); gate 4 CONSISTENT
[STRIPPING-DEPENDENT]; overall NOT FALSIFIED (ONE-SIDED). Everything below is decided after seeing that. RESULT.md states both readings.

## 1. KA-2 (TR1's fractions): the definition of TR1's table

- My loader reproduced TR1's four inner bins and missed the last one: 0.309 against 0.32 (canonical), 0.250 against 0.26 (alt).
- **Cause, checked from TR1's own printed rows** (`TR1_cluster_tracer/tr1.out`, "tot per-cluster residuals", reading D): the per-cluster
  fraction in a bin is A x 10^residual. In the last bin those rows give A1795 0.287, A2029 0.329, A2142 0.300, A644 0.100 (the -1.0
  marker for M_X <= 0), A85 0.319, ZW1215 0.520. With A644's marker the median of the six is 0.309; without A644 it is 0.319. Alt gives
  0.250 and 0.261. **TR1's RESULT table dropped M_X <= 0 points; its per-cluster rows kept the marker.** My loader matches the rows.
- **KA-2 becomes two checks, same tolerances:**
  - **KA-2a:** TR1's per-cluster rows reproduced. For each of the 7 clusters and 5 bins, my per-cluster median of log10(M_X / M_dyn)
    (marker -1.0) equals TR1's log10 A + residual, to 0.002 dex (the printed rounding), reading D, both footings. This is the stricter
    test of the loader.
  - **KA-2b:** TR1's table, with M_X <= 0 points dropped (a cluster with none left in a bin drops out of that bin), to 0.005:
    0.71 / 0.66 / 0.58 / 0.46 / 0.32 and 0.68 / 0.63 / 0.54 / 0.41 / 0.26.
- Gate 3's printed TR1-statistic fractions (model and data) use KA-2b's definition. **Gate 3's graded statistic, bins, line and label
  rule are unchanged.** Under the frozen KA-2, gate 3 is NO VERDICT; RESULT.md says so beside the amended reading.

## 2. Reported Bullet row with ZN4's native shape: the normalisation

- The frozen text: "the cold with ZN4's native shape centred on each cluster's galaxies ... truncated at x_edge". My first
  implementation normalised the total R x M_b at 7.4 R200, spreading a cluster's cold out to about 10 Mpc. That is not ZN's rule.
- **Now reported:** ZN's rule (M200 = (1 + R) M_b, so R x M_b of cold inside R200; the shape continued to x_edge), the same truncated at
  R200, and the first implementation, marked superseded. Reported only; it never entered gate 4's label.

## 3. A post-hoc reported bracket on gate 1's X-COP class

- An independent check with X-COP's own published FGAS column (gas over the NFW-fit hydrostatic mass) gave a median f_ret at R500 of
  0.96 (per cluster 0.94, 0.96, 1.09, 1.33, 0.88, 1.00, 0.68). The forward-fitted mass M_FORW used in the graded row gives 1.06 there.
- **Added, reported and never graded:** C-X with M_NFW (the fgas file's NFW-fit hydrostatic mass) in place of M_FORW, at R500 and at
  the last radius. The graded row stays M_FORW, as frozen.

No class, aperture, line, tolerance, bracket of the frozen text or label rule changes. kappa = 1/2 FITTED; not theory closed. Relabels nothing.
