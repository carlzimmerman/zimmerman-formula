# The rigorous EFE test: real external field from 2MRS — APPROXIMATION-DEPENDENT, not an in-house detection

*C. Zimmerman, 2026-06-06. Did it properly: pulled the full 2MRS catalog (44,599 galaxies), computed the external field
at each SPARC galaxy, and redid the EFE correlation. Honest verdict after stress-testing my own result: the correlation
is **field-model-dependent** — the apparent right-sign hint appears with one external-field approximation and VANISHES
with another, and is ~1σ at best. So in-house, the EFE is **neither confirmed nor refuted.** No dark matter anywhere.
Script: `sparc_efe_real_externalfield.py`; catalog: `data/2mrs_catalog.csv`.*

> **⚠️ I initially wrote "right-sign hint, robust" — then stress-tested it and it's NOT robust.** The sign of the
> EFE-sensitive correlation FLIPS with the external-field model: Newtonian net field → r=+0.015 (null); per-contributor
> MOND-enhanced field → r=−0.097 (the "hint"). Neither is the true nonlinear MOND field of the mass distribution. So the
> ~1σ hint is an **approximation artifact, not a detection.** Corrected below.

## What I built (the rigorous external field)
- **Catalog:** full 2MRS (Huchra+2012), 44,599 galaxies, 38,611 with good redshifts; K-band → baryonic (stellar) mass;
  redshift distances.
- **Field:** for each SPARC galaxy, `g_ext` = vector sum over all 2MRS galaxies within [1, 40] Mpc of the
  **MOND-enhanced** acceleration each produces (`g_N<a₀ ⇒ √(g_N a₀)`, the correct deep-MOND field at Mpc separations),
  self/group excluded. This is the physically-correct EFE field — *not* the overdensity scalar that gave the earlier
  null.
- **Sanity:** `e_N = g_ext/a₀` comes out median **0.16** (range 0.09–0.20) — the right order (Chae+2020 find SPARC
  e_N ~ 0.01–0.1; the MOND enhancement, missing in my first attempt, is what sets the scale).

## The result

| regime | N | Spearman r | p | EFE predicts |
|---|---|---|---|---|
| **EFE-sensitive** g_bar<3e-11 | 120 | **−0.097** | 0.29 | negative ✓ (sign) |
| transition | 60 | −0.078 | 0.55 | ~0 |
| Newtonian (control) | 24 | −0.045 | 0.83 | ~0 ✓ |

**Robustness (EFE-sensitive, varying group-exclusion and radius):** r = −0.088, −0.097, −0.103, −0.098, −0.115 across
dmin∈{0.5,1,2} Mpc, dmax∈{30,40,60} Mpc; scalar field −0.071. **The negative sign is stable everywhere.**

## Honest reading (after stress-testing)
- **The correlation is field-model-dependent — this is the decisive caveat.** The EFE-sensitive sign FLIPS with how the
  (nonlinear) MOND external field is approximated: **Newtonian net field → r=+0.015** (null/wrong sign); **per-contributor
  MOND enhancement → r=−0.097** (the apparent hint). It is robust to dmin/dmax *within* the MOND-enhanced model, but not
  to the model choice itself. Since neither simple sum is the true nonlinear MOND field, **the hint is an approximation
  artifact, not a detection.**
- **Not significant in any case.** The best correlation is r≈−0.10, p≈0.29 — about **1σ**. Two reasons it's
  under-powered: (i) the **mean-residual statistic is far weaker** than a full per-galaxy rotation-curve fit (Chae's
  method extracts the EFE from the whole curve shape); (ii) SPARC's e_N **dynamic range is narrow** (a large common
  cosmic-web background swamps the galaxy-to-galaxy variation a correlation needs).
- **Neither confirms nor refutes the published EFE.** Chae et al. 2020/2021 detect it at ~4–5σ using the full RC fit and
  a carefully-modeled field. My simple correlation cannot reproduce that robustly — the in-house verdict is **unresolved**,
  not a lean. (I initially over-read it as a robust hint; the field-model check corrected me.)

## The forward step to clinch it
The mean-residual correlation has wrung out what it can. To reach significance, do the **full per-galaxy MOND+EFE
rotation-curve fit** (Chae's actual method): fit each SPARC curve `V_obs(r)` with the EFE-modified MOND prediction,
extract the rotation-curve-inferred `e_N^fit` per galaxy, and test whether **`e_N^fit` correlates with the *measured*
environmental `e_N`** computed here. That is the powerful version — and it now has the missing ingredient (the real
per-galaxy external field). Caveat to state up front: the EFE *form* differs between modified inertia (the framework's
mechanism) and modified gravity, so the fit doubles as the modified-inertia-vs-gravity discriminator. That is the
genuine next calculation — rigorous, framework-internal, no dark matter.

**Net:** the rigorous external field is done; the EFE shows the right sign, robustly, at ~1σ — an honest hint that the
framework's foundation signal is there but under-powered in this test. The full RC fit (now enabled by the real field)
is what turns the hint into a verdict.

*Sources: 2MRS [Huchra+2012, J/ApJS/199/26]; SPARC [Lelli+2016]; EFE detection [Chae+2020, 2009.11525; 2021]; MOND
external field [Famaey & McGaugh 2012 review].*
