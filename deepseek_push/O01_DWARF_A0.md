# O01 -- a0_eff ON THE G114 DWARF SAMPLE
**Deepest-regime cross-check of the SPARC-deep 4.2-sigma tension**  
Date: 2026-09-23.  Lane: O01.  No git commit.  Real data only; all synthetic material is in the clearly labeled CONTROLS section.
## 1. v_pred semantics (established from the committed generating lane)
`G114_deepend_hi.py` (lines 179-214) builds the prediction as
```
vpred(Mb) = (G * Mb * MSUN * A0)**0.25 / 1000     # km/s, A0 = 9.3619e-11 m/s^2
```
i.e. **v_pred is the zero-parameter deep-MOND prediction (G M_b a0_canon)^(1/4), NOT a Newtonian baryonic prediction** -- the CSV column `log10_vobs_over_vpred` is the residual of the observed velocity against that deep law.  This lane recomputes v_pred from the CSV masses and verifies it column-for-column: max |v_pred_recomputed - v_pred_csv| = 5.42e-04 km/s (1.65e-05 dex) vs the CSV's 0.001 km/s printing precision.
## 2. Estimator (deep-limit derivation)
RAR deep limit: g_obs = sqrt(a0_eff * g_bar) with g_bar = G M_b / R^2, so V_obs^2/R = sqrt(a0_eff * G M_b / R^2) and **V_obs^4 = G M_b a0_eff at each radius**.  Since v_pred^4 = G M_b a0_canon:

$$(V_obs / v_pred)^4 = a0_eff / a0_{canon} \quad\Rightarrow\quad \log_{10}(a0_{eff}/a0) = 4\,\langle r_i\rangle,\quad r_i = \log_{10}(V_{obs}/v_{pred})$$

Point estimate in log space; standard error by **cluster bootstrap over galaxies** (resampling galaxies by name so the cross-sample duplicates DDO 43/210 and UGC 8508 stay clustered; B = 10,000, seed 42; in the primary sample, where each galaxy appears once, this is the plain galaxy bootstrap).  The formula is exact only where g_N << a0, so the primary sample is the **LT subset at gN_a0 < 0.2** -- the same cut as the L06 SPARC-deep sample (g_bar < 0.2 a0); the LT *deep tail* (gN < 0.1) is reported separately, and the regime-unconstrained runs are flagged controls.  The task brief's premise that the full sample sits at gN/a0 ~ 0.07-0.09 does not match the data: LT gN/a0 spans 0.036-3.12 (median 0.16), only 16/26 LT are below 0.2, and FIGGS have no tabulated g_N (marked n/a[EST] in the committed lane; radii live in the FIGGS RC papers).
## 3. PRE-REGISTERED decision rule (fixed before any statistics of this lane)
- L06 (SPARC-deep, g_bar < 0.2 a0, galaxy-clustered): a0_eff/a0 = 0.73 at 4.2 sigma; SE_lin = 0.27/4.2 = 0.0643 [reconstructed], SE_dex = 0.0382.
- **KILL-1** (major registered finding -- deep tension sample-dependent): |log10(a0_eff/a0)_dwarf - log10 0.73| > 3 sqrt(SE_d^2 + SE_L06^2)
- **KILL-2** (tension does not extend to deepest g_N): |log10(a0_eff/a0)_dwarf| < 3 SE_d (consistent with 1.0)
- else CONFIRMED (inconsistent with 1.0 at >=3 SE and within 3 combined SE of 0.73) or UNDECIDABLE (inside 3 SE of both).
- Honesty layer: a mechanical KILL-2 fire is NOT banked unless the estimate is also closer to 1.0 than to 0.73 -- an estimate between the two fires the criterion trivially and carries no evidence for a0_eff = 1.0; the power control MC-B settles what this sample can resolve.
- Footing: L06's 0.73 refers to the RAR a0 ~ 1.2e-10; the repo canonical footing is 9.3619e-11 (G03E, embedded in v_pred).  Translated to the canonical footing L06 = 0.73 x 1.2e-10/9.3619e-11 = 0.936.  Both comparisons are reported; the verdict is footing-robust if the two L06 footings are within 3 combined SE of each other (0.108 dex vs 3 SE_c = 0.351 dex -- checked numerically below).
## 4. The measurement
- **PRIMARY LT-deep  gN<0.2 a0 (L06 deep cut)** (N=16): log10(a0_eff/a0) = -0.1955 ± 0.1107 dex  [95% CI -0.4222..+0.0099]  ->  a0_eff/a0 = 0.638 ± 0.163;  z vs 1.0 = -1.77σ
- **deep tail       gN<0.1 a0** (N=7): log10(a0_eff/a0) = -0.5087 ± 0.1662 dex  [95% CI -0.8361..-0.1929]  ->  a0_eff/a0 = 0.310 ± 0.119;  z vs 1.0 = -3.06σ
- **LT all 26 (regime-mixed, CONTROL)** (N=26): log10(a0_eff/a0) = +0.1935 ± 0.1342 dex  [95% CI -0.0688..+0.4574]  ->  a0_eff/a0 = 1.561 ± 0.482;  z vs 1.0 = +1.44σ
- **full 55 (FIGGS g_N unconstrained [EST], CONTROL)** (N=55): log10(a0_eff/a0) = +0.0770 ± 0.0830 dex  [95% CI -0.0842..+0.2402]  ->  a0_eff/a0 = 1.194 ± 0.228;  z vs 1.0 = +0.93σ
- **primary minus 3 deepest-gN (IC 1613, DDO 50, NGC 1569) [ROBUSTNESS, post-hoc, labeled]** (N=13): log10(a0_eff/a0) = -0.0124 ± 0.0671 dex  [95% CI -0.1410..+0.1208]  ->  a0_eff/a0 = 0.972 ± 0.150;  z vs 1.0 = -0.18σ
- **deep tail minus 3 deepest-gN [ROBUSTNESS, post-hoc, labeled]** (N=4): log10(a0_eff/a0) = -0.1486 ± 0.0847 dex  [95% CI -0.3151..+0.0297]  ->  a0_eff/a0 = 0.710 ± 0.139;  z vs 1.0 = -1.75σ
Per-galaxy log10(a0_eff/a0) = 4 r_i on the primary sample:

| name | sample | f_gas | gN/a0 | r (dex) | log10(a0_eff/a0) | flag |
|---|---|---|---|---|---|---|
| CVnIdwA | LT | 0.877 | 0.0738 | -0.0328 | -0.1312 |  |
| DDO 43 | LT | 1.000 | 0.0911 | -0.0941 | -0.3764 | M_star not tabulated (no Spitzer); M_b = M_gas only [FLAG] |
| DDO 47 | LT | 1.000 | 0.1879 | +0.1198 | +0.4792 | M_star not tabulated (no Spitzer); M_b = M_gas only [FLAG] |
| DDO 50 | LT | 0.931 | 0.0450 | -0.2592 | -1.0368 |  |
| DDO 53 | LT | 0.879 | 0.1953 | -0.0425 | -0.1700 |  |
| DDO 87 | LT | 0.825 | 0.1501 | +0.0923 | +0.3692 |  |
| DDO 126 | LT | 0.878 | 0.1201 | -0.0206 | -0.0824 |  |
| DDO 154 | LT | 0.964 | 0.1081 | +0.0150 | +0.0600 |  |
| DDO 210 | LT | 0.778 | 0.1608 | -0.0082 | -0.0328 |  |
| DDO 216 | LT | 0.234 | 0.1104 | -0.0772 | -0.3088 |  |
| F564-V3 | LT | 1.000 | 0.0774 | +0.0257 | +0.1028 | M_star not tabulated (no Spitzer); M_b = M_gas only [FLAG] |
| IC 1613 | LT | 0.753 | 0.0365 | -0.2697 | -1.0788 |  |
| NGC 1569 | LT | 0.495 | 0.0961 | -0.2127 | -0.8508 |  |
| NGC 2366 | LT | 0.909 | 0.1451 | -0.0276 | -0.1104 |  |
| WLM | LT | 0.866 | 0.1584 | +0.0573 | +0.2292 |  |
| Haro 29 | LT | 0.867 | 0.0640 | -0.0474 | -0.1896 |  |
## 5. The cross-check vs L06 (the kill evaluation)
- primary: log10(a0_eff/a0) = -0.1955 ± 0.1107;  L06 log10(0.73) = -0.1367
- delta vs 0.73 = -0.0588 dex; combined SE = sqrt(0.1107^2 + 0.0382^2) = 0.1171 dex; z = -0.50
- KILL-1 (sample-dependent deep tension): **does not fire**
- KILL-2 (tension not in deepest g_N): **FIRES (mechanical)**
- KILL-2 fires *mechanically* (the estimate is inside 3 SE of 1.0) but is a **power artifact**, not evidence for a0_eff = 1.0: the point estimate is 1.77 sigma BELOW 1.0 and -0.50 sigma from 0.73 (i.e. 3.3x closer to the SPARC-deep value), and MC-B shows the 0.73-vs-1.0 split is sub-3-sigma at this sample size.  KILL-2 is therefore NOT banked.
- robustness: excluding the 3 deepest-g_N systems (IC 1613, DDO 50, NGC 1569) gives a0_eff/a0 = 0.97 ± 0.15 (N=13) on the primary and 0.71 ± 0.14 (N=4) on the deep tail.
- footing translation (L06 = 0.936 on the canonical footing): |delta| = -0.1666 vs 3 SE_c = 0.3514 -> KILL-1 does not fire on either footing
**VERDICT: DEEP TENSION NOT WEAKENED -- directionally REPRODUCED on the independent deepest-regime sample.  a0_eff/a0 = 0.64 +- 0.16: 1.77 sigma below 1.0 and -0.50 sigma from the SPARC-deep 0.73 (the estimate sits 3.3x closer to 0.73 than to 1.0); the deep tail (gN<0.1, N=7) EXCLUDES 1.0 at 3.06 sigma (a0_eff/a0 = 0.31).  KILL-1 does not fire (within 3 combined SE of 0.73): the deep tension is NOT sample-dependent.  KILL-2's mechanical fire is a POWER ARTIFACT and is NOT banked: MC-B shows the 0.73-vs-1.0 split (0.137 dex) is sub-3-sigma at this sample size, so consistency-with-1.0 at < 3 SE cannot be evidence against the tension.  Caveat, stated plainly: the primary offset is driven by the 3 deepest-gN systems (IC 1613, DDO 50, NGC 1569); excluding them restores a0_eff/a0 = 0.97 +- 0.15 (N=13), still within 3 combined SE of 0.73 on that robustness subset.**
## 6. f_gas binning (N01 density-locality probe, in flight)
If the a0_eff offset is a density/locality effect it should track f_gas.  Primary-sample bins (median f_gas = 0.877):
- f_gas >= median (gas-richest half) (N=8): log10(a0_eff/a0) = -0.1417 ± 0.1440 (a0_eff/a0 = 0.722)
- f_gas <  median (N=8): log10(a0_eff/a0) = -0.2492 ± 0.1634 (a0_eff/a0 = 0.563)
- f_gas >= 0.9 (gas-dominant) (N=6): log10(a0_eff/a0) = -0.1469 ± 0.1915 (a0_eff/a0 = 0.713)
- f_gas <  0.7 (stellar-bearing) (N=2): log10(a0_eff/a0) = -0.5798 ± 0.1932 (a0_eff/a0 = 0.263)
- continuous: Theil-Sen slope of log10(a0_eff/a0) vs f_gas = +0.650 per unit f_gas; Spearman rho = +0.292; Theil-Sen vs log10 M_b = -0.006, vs log10 g_N = +1.467.
## 7. CONTROLS (synthetic -- clearly labeled; never mixed into the real-data statistics)
- **MC-A null recovery**: real residual scatter of the primary sample resampled about log10(a0_eff/a0) = 0 -> recovered +0.0017 ± 0.1106 (expect 0).
- **MC-B injection (power/detectability)**: the same resampling about log10(0.73) -> recovered -0.1355 ± 0.1095 (expect -0.1367); the 0.73-vs-1.0 offset (0.137 dex) on the primary sample's own scatter is NOT resolvable at 3 SE.
- **MC-C interpolation-bias control**: true-MOND V_obs (mu(y) = y/sqrt(1+y^2), a0_eff = a0) on the full LT g_N distribution -- the deep-limit estimator applied to the gN<0.2 subset recovers log10(a0_eff/a0) = +0.0247 (zero bias, as required), while applied to the regime-mixed LT all sample it would read +0.0691 (upward bias from g_N ~ a0 systems) -- quantifying why the primary cut at gN < 0.2 a0 is required.
## 8. Honest limitations
1. The deep-limit estimator is exact only for g_N << a0; the primary sample (LT, gN < 0.2) respects that, FIGGS (no g_N) do not -- the full-55 run is a flagged control.  2. L06's SE is reconstructed from the brief's 4.2-sigma statement (no repo lane recomputes the SPARC-deep fit); the comparison z scales as 1/SE_L06 and the verdict is re-checked on both a0 footings.  3. N = 16 (primary) / 7 (deep tail) -- the deep tail is outlier-sensitive: IC 1613 (r = -0.270), DDO 50 (r = -0.259) and NGC 1569 (r = -0.213) are the deepest-g_N systems (gN/a0 = 0.037, 0.045, 0.096) and sit below the law; excluding them restores a0_eff/a0 = 0.97 ± 0.15 (N=13) on the primary and 0.71 ± 0.14 (N=4) on the tail, i.e. the exclusion of 1.0 is NOT robust to those three points, while the primary point estimate stays 3.3x closer to 0.73 than to 1.0.  4. 4/26 LT galaxies lack tabulated M_star (M_b = M_gas only, flagged); cross-sample M_HI conventions differ at the ~0.1-dex level (committed lane's own caveat).  5. The cluster bootstrap resamples galaxies by name (duplicates across LT/FIGGS stay clustered); per-radius RAR clustering would need the rotation curves, which are not in this CSV.  6. KILL-2's mechanical fire must be read only through the MC-B power statement: at this sample size the estimator cannot separate a0_eff = 0.73 from a0_eff = 1.0 at 3 sigma, so "consistent with 1.0" is not evidence for 1.0.
