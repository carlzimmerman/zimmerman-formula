# GATES 0-3 VERDICT  (2026-08-21)

## 1. DHF reproduction status — PASS, exact
| item | mine | DHF 2024 |
|---|---|---|
| Q2 pipeline, Table 1 n-family, all 5 fiducial rows | max diff **0.24%** | — |
| tension significances | 8.5 / 8.5 / 8.8 / 8.5 / 8.7 | 8.4 / 8.4 / 8.7 / 8.4 / 8.6 |
| q(e~) vs DHF Fig.1 (nu_RAR) | 0.09471 / 0.15949 / 0.22100 | 0.094 / 0.159 / 0.221 |
| q vs Milgrom 2009 Table 1, mu_3 at eta=1.5 | 0.07916 | 0.079 |
| SPARC sample | **147 galaxies / 2696 points / 31 bulges** | 147 / 2696 / 31 |
| H0 universal-n fit | n=1.000, a0=1.100e-10, sig_int=0.0350 dex | 1.02+-0.04, 1.08+-0.04, 0.034 |

No fitted factor anywhere. `Q2 = -(3/2) a0^{3/2}/sqrt(GM) q(e~)` is **DHF Eq.10 verbatim**, not a convention choice.

## 2. Universal-n vs environment-dependent-n
`ln n_i = ln n0 + beta ln(T_i/T0)`, `T = a0^{3/2}/sqrt(G M)`.
- beta-hat = **+0.10**, Delta chi2 = **+8.7** (grid) / +11.8 (fixed a0), Delta AIC +6.7, Delta BIC +0.8
- **Permutation null (3000 shuffles): sd 0.078, p(beta) = 0.19, p(Dchi2) = 0.23. NOT SIGNIFICANT.**
- The profile error bar was **2.23x too small**; chi2_1 does not apply here.

## 3. SPARC constraint on beta
**beta_SPARC = +0.10 +- 0.078 (permutation-calibrated).  Consistent with zero.**
Controls, all permutation-calibrated on the same footing — *nothing* is significant:

| proxy | beta | Delta chi2 | perm p |
|---|---|---|---|
| M_bar (the theory variable) | +0.100 | 8.68 | 0.203 |
| surface brightness | -0.115 | 10.78 | 0.171 |
| has bulge | -0.055 | 10.71 | 0.198 |
| V_flat^-2 (M/L-independent) | +0.100 | 2.97 | 0.537 |

Predictors are 0.34-0.66 correlated, and **no proxy is significant**, so there is no signal to partition
multivariately. The Sigma/bulge pattern is DHF's own known systematic (8.7 sigma -> 1.9 sigma on removing bulges).

## 4. Solar-System required beta
`n_SS` from the Cassini likelihood with DHF's priors (flat on Q2, uniform a0, Gaia EDR3 g_ext):
- full posterior: median **5.56**, 95% lower credible bound **2.92**
- hard 95% upper-limit sense: **2.78 - 3.90**
- lever `ln(T_SS/T_gal) = 0.5 ln(M_gal/M_sun) = 11.51` at 1e10 Msun — **exact, a0-independent**

**beta_req = 0.087 - 0.15** (n_SS 2.78-5.56 against n_gal 1.02).

## 5. GO / NO-GO — **Case B: VIABLE BUT UNSUPPORTED**
`beta_req = 0.087-0.15` sits **inside** `beta_SPARC = +0.10 +- 0.078`, at well under 1 sigma.
So SPARC **permits** the required environmental dependence but **does not require it**;
beta = 0 remains a perfectly acceptable fit (p = 0.19-0.23).

**Not Case A** — the escape is not excluded. **Not Case C** — there is no detection.
The mechanism is a hypothesis, not an empirical clue. Do not build an action on it.

### What would decide it
SPARC's internal lever is only `ln T = 4.91` (2.13 decades) against the 11.51 needed to reach the Sun,
and only 126/147 galaxies constrain n at all (per-galaxy n-hat 16-84 pct = [0.54, 34.65]).
The test is **power-limited, not null**. A decisive test needs either per-galaxy n constrained far
better, or a sample extending the mass lever — not a reanalysis of these 147.
