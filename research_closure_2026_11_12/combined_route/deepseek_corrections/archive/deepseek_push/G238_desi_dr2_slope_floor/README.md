# G238 — the slope floor re-read on DESI DR2 III: the decider G157 named has arrived

**Pre-registration:** G157's own (`deepseek_push/G157_slope_floor.py`, committed 2026-09): P-A `γ = −2.00 ± 0.02`
constant over 20–100 kpc, **KILL** if the measured total slope is steeper than `−2.05` at `r ≥ 3 r_M = 30.63 kpc`.
This lane does not re-register that rule; it applies it to new data and reports what happens.

**Data:** DESI DR2 Results III (arXiv:2611.05518), Table 4 — the joint enclosed-mass profile at 13 radii,
20–80 kpc, from 10,036 RRL+BHB halo stars with 6D phase space. This is the "DESI-DR2/H3-class K-giant+BHB
sample at 30–100 kpc" that G157's own `.out` named as the flip.

**Convention** (G157 eq. G157-1): `γ = dlnρ/dlnr = dlnM/dlnr − 3`; `M ~ r^p` → `γ = p − 3`. Flat curve = −2,
point mass = −3.

## Result

| statistic | measured (DESI DR2 III) | framework kernel | NFW (paper's own) | P-A |
|---|---|---|---|---|
| γ(20–40 kpc) | −2.16 ± 0.26 | −2.12 | −1.88 | −2.000 |
| γ(40–60 kpc) | −2.02 ± 0.78 | −2.09 | −2.08 | −2.000 |
| γ(60–80 kpc) | −2.28 ± 1.86 | −2.07 | −2.19 | −2.000 |
| **γ(20–80 kpc)** | **−2.097 ± 0.147** | **−2.100** | −2.002 | −2.000 |

**Verdict: the decider arrived and did not decide.** γ(20–80) = −2.097 ± 0.147 is 0.7σ from P-A's constant and
0.0σ from the framework's own kernel; G157's 3σ kill does not fire (−0.42σ in the bin containing 3 r_M). On
this data set the slope floor is **untested at its own registered precision** — not passed, not failed.

## The finding that does not depend on the data

**P-A's ±0.02 band is the asymptote, not the value at the radius it was registered for.** The committed
kernel's deep limit is `ν ~ 1/√y + 1/2`, so `M_dyn = M_b(r/r_M + 1/2)` and

```
γ(r) = −(2 + r_M/(2r))  =  −2.167 at 3 r_M (30.63 kpc)  →  −2.051 at 100 kpc
```

That is **8× the registered band** at 3 r_M and **6× past P-A's own "never steeper than −2.07" ceiling** — so
G157's kill line (−2.05) sat *inside the framework's own prediction* at the radius where the kill was to be
applied. As registered, the test could have killed the framework for landing on its own kernel. The Milgrom
kernel gives −2.100 at the same radius, so the correction is kernel-independent: it is a registration error,
not a kernel choice.

## What would decide it

Not more slope precision at 20–80 kpc (the diagonal errors already span 0.15, and the table's errors are
correlated in a way the paper does not publish). A **100–200 kpc enclosed-mass profile** separates cleanly:

| 100–200 kpc | γ |
|---|---|
| framework kernel (canonical / alt) | −2.034 / −2.031 |
| NFW with the paper's own M200c, c = 12 | −2.388 |

a 0.35 separation, i.e. ~7σ at a 5% enclosed-mass measurement at 150 kpc — the same observation that decides
the DW1 plateau falsifier.

## Honest limits

- The 13 table errors are **correlated** (all points come from smooth joint fits). Every σ here treats them as
  diagonal, so the quoted significances are **upper bounds on the evidence** — which is why no kill is claimed
  and no exclusion of P-A is claimed.
- The 60–80 kpc bin has a 1.86 error: five points on a narrow lever arm. It is reported for completeness, not
  as a result.
- The framework's prediction uses the same McMillan 2017 baryons and Route A kernel as DW1/h34; `A = 1`, no
  amplitude nuisance (the amplitude question is DW1's).
- `κ = 1/2` remains **FITTED**; nothing here derives the kernel or `a₀`.

## Files

`g238.py`, `g238.out`, `g238_results.json`. Check count `G238 COMPLETE: 8/9 checks PASS`; the one FAIL is
G238a ("the DESI profile is steeper than P-A at ≥2σ"), which is the honest negative: the data are not
precise enough to exclude the registered constant.
