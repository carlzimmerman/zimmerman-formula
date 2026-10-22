# A26 mutations — do the checks have teeth?

Two mutations, both deterministic, both run from `a26_checks.py`. The **required** one is M1: it injects
the rival hypothesis and every fork check must fail. M2 is the record's own sensitivity control
(CFG828's `sigma/1.45`) and is declared to break only the reproduction check.

    python3 a26_checks.py --mutate      # M1: medium-first injected
    python3 a26_checks.py --mutate2     # M2: every sigma / 1.45

Baseline for comparison: `A26 COMPLETE: 11/11 checks PASS.`, exit 0, verdict `LAW-FIRST`.

## M1 — medium-first injected (`g_obs := g_bar` for every `M_star < M_crit`)

This writes the medium-first world into the data: sub-threshold systems become exactly Newtonian and
nothing else changes. If the analysis is honest it must now return MEDIUM-FIRST and every discriminating
check must flip.

```
*** MUTATION M1: medium-first INJECTED (g_obs := g_bar for every M_star < M_crit) ***
  below M_crit  N= 45  median log g_bar -12.99  median Delta -1.490 +- 0.054  median log(g_obs/g_bar) +0.000 +- 0.000
  above M_crit  N= 47  median log g_bar -12.12  median Delta +0.132 +- 0.053  median log(g_obs/g_bar) +1.171 +- 0.089
  within +-0.5 dex of the LAW: 0/45    within +-0.5 dex of NEWTONIAN: 45/45

K1  PASS  N=92 N_below=45                       threshold: N>=80 and N_below>=40
K2  PASS  M_crit=3.8669e+05 Msun (0.08%)        threshold: 1%
K3  PASS  CFG828 control mean Delta=+0.438      threshold |mean-0.44|<=0.06
K4  FAIL  median log10(g_obs/g_bar)=+0.000      threshold >=0.70
K5  FAIL  median Delta=-1.490+-0.054            threshold >0 at 95%
K6  FAIL  distance to Newtonian +0.000+-0.000   threshold >=1.0 dex
K7  FAIL  step c=-1.656+-0.070, separation -0.5 sigma   threshold >=5 sigma
K8  FAIL  matched-bin difference -1.748 dex     threshold >-1.0
K9  FAIL  near-law 0 vs near-Newton 45          threshold >=10 and <=2
K10 FAIL  all variants lose Delta(below)>0      threshold: all
K11 FAIL  after the largest correction -0.59 dex survive   threshold >=1.0 dex

VERDICT: MEDIUM-FIRST
A26 COMPLETE: 3/11 checks PASS.
```

Exit code 1. **8 of 11 checks break**, and the verdict flips to the rival reading. K1/K2/K3 survive
because they test the sample, the theory identities and the record reproduction — none of which the
injection touches. This is the mutation that proves the fork checks are load-bearing: they fail exactly
when the data are made medium-first and the step statistic lands on medium-first's required value
(`c = -1.656` against the required `-1.622`, separation `-0.5 sigma`).

## M2 — `sigma / 1.45` everywhere (CFG828's control)

```
K3  FAIL  CFG828 reproduction: mean Delta=+0.115 dex   threshold |mean-0.44|<=0.06
K4  PASS  median log10(g_obs/g_bar)=+1.825 (66.8x)
K5  PASS  median Delta=+0.328+-0.090 (95% lo +0.150)
K6  PASS  distance to Newtonian +1.825+-0.084 dex
K7  PASS  step c=+0.453+-0.099 -> 17.7 sigma from -1.299
K8  PASS  matched-bin difference +0.417 dex
K9  PASS  near-law 23 vs near-Newton 0
K10 FAIL  the sigma^2/r variant drops to med Delta below -0.149
K11 PASS  1.24 dex survive

VERDICT: LAW-FIRST
A26 COMPLETE: 9/11 checks PASS.
```

Exit code 1. K3 breaks as declared: a uniform `sigma` rescaling moves the record's `+0.44` to `+0.115`,
i.e. `-0.32` dex, exactly the shift CFG828 reports for the same control. K10 also breaks, and that is
the most informative line in this file: the K10 sweep carries the conservative `sigma^2/r` normalisation
(no Wolf factor 3), so `sigma/1.45` plus the conservative estimator moves the sub-threshold median from
`+0.651` to `-0.149` dex. **The residual-from-the-law part of the result is normalisation-limited at
about 0.8 dex; the Newtonian exclusion is not** (`Delta_N = -1.49`, still 1.34 dex away in the same
variant).

Note what does not move: the step `c` is bit-identical at `+0.453` because a global `sigma` offset is
absorbed by the intercept `a` in eq. (6). That invariance is the reason `c`, and not the raw median, is
the deciding number — it is immune to any global calibration error in `sigma` or `Upsilon`, including the
M/L zero-point.

## What these mutations establish

- The kernel-free boost check (K4), the sign check (K5), the Newtonian-distance check (K6), the step (K7),
  the matched-bin check (K8), the census (K9) and the robustness sweep (K10) all fail when the rival
  hypothesis is written into the data, and none of them fails for a global `sigma` recalibration.
- The verdict is not hard-coded: it is read off K4–K7 and returns `MEDIUM-FIRST` under M1.
