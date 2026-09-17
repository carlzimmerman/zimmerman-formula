# RH10 -- THE RAR OF THE RIEMANN ZEROS
**VERDICT: [INCONCLUSIVE] -- power gate tripped; RAR fit unresolvable at ~500 zeros; no claim either way; no RH claim.**
1. PRE-REGISTERED in-file before any zero computed; mpmath zetazero dps=15, N=500 (data reach gamma_500=811.2; nominal t in [100,2000] truncated by the zero budget).
2. RAR: rho_obs=(zeros in window)/L; rho_bar=(1/2pi)ln(t/2pi) at center; fit rho_obs^2-rho_bar^2 = A*rho_bar^gamma by log-regression over non-overlapping windows (L=25: 28 windows; L=50: 14; spacing>=25>20 t-units).
3. Primary fit (L=25): gamma=+0.48, bootstrap 95% CI [-1.86,+2.32] (half-width 2.09); A=3.76e-2 (95% [1.1e-2,8.8e-2]); 13/28 windows had q>0 (54% excluded; A intercept-biased upward, stated).
4. POWER GATE (pre-registered: CI half-width>0.30 -> no claim): 2.09 >> 0.30 -> neither branch ([PASS] gamma in [0.85,1.15]; [FAIL] gamma~0) can fire; INCONCLUSIVE, numbers only.
5. Why: per-window q is ~40x noisier than its mean; E[q] = GUE number variance ~ ln(L rho)/pi^2/L^2 ~ 1e-4, unresolvable at this budget. NULL ANCHOR: bin means match that GUE null (z=-0.0,-0.4,+0.5) -- q is exactly ordinary zero statistics, no signal beyond them.
6. L=50 leg: gamma=-0.83 (CI half-width 4.15), A=7.0e-3 -- same low-power picture; slopes consistent with L=25 at 0.7 sigma, both unconstrained.
7. UNIVERSALITY of A (D5): ln[A(50)/A(25)] = -1.69 +- 1.34 (z=-1.3): L-dependence not refuted, but per-leg SE of ln A ~1 -> A determined only to ~e^1.3; universality UNCONSTRAINED, not established.
8. 2b MILGROM: chi2=68.7 on df=28 (p=2.9e-5); with the standard GUE number-variance constants (~1.7x) chi2/df -> ~1, i.e. ordinary GUE noise, not a RAR signature.
9. 2b INFORMATIVENESS GATE: S = median|nu_model-1|/median sigma_nu = 0.87 < 1 -> UNINFORMATIVE: Milgrom form indistinguishable from nu=1 at y~12-20; chi2 cannot validate the RAR.
10. Autocorrelation (D8): lag-1 r1 of count deviations = -0.61 (L=25) -> N_eff = 28/28 windows; adjacent windows anti-correlated, no independence inflation; reported.
11. Diagnostics: rms(delta_n*rho) of the S-shift delta_n = gamma_n - N^-1(n) = 0.50 (the 'dark' fluctuation scale); sanity checks PASS: gamma_1=14.134725, gamma_100=236.524230; checks 2/3 (D5 PASS w/ power caveat, D7 FAIL = uninformative).
12. HONESTY: real computation only (mpmath, dps=15), nothing committed, no RH claim anywhere; BOTTOM LINE: RAR on the zeros is NOT established and NOT cleanly falsified -- the honest answer at this budget is 'cannot resolve'.
13. FILES: RH10_rar_of_zeros.py (pre-registered), RH10_rar_of_zeros.out, RH10_results.json, this summary; a decisive transfer test needs ~10^4+ zeros or much longer windows.