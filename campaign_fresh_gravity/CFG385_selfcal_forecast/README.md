# CFG385: self-calibrated a0(z ~ 2.5) forecast. What sample decides the DE-tracking law vs a0 proportional to H(z)?

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 0c47e8505. A FORECAST: no data are scored. Model: CFG240's Fisher, with the calibration f left free.

**Headline: the absolute-calibration wall can be bypassed.** If each galaxy's rotation curve spans BOTH regimes, its inner (Newtonian) points fix its own baryon mass scale and its outer (deep) points fix a0. No gas or stellar absolute calibration is needed.

**Target:** the DE-tracking law (a0(2.5) about 0.8x today) vs the rival (about 3.8x) is 0.67 dex apart, so 3 sigma needs sigma(log a0) <= 0.22 dex (flat vs rival 0.19).

**Frozen grid (one common f free):** 140/192 (P2) and 121/192 (exp-RAR) designs reach 0.22 dex. At 0.1 dex per point (5% in velocity) and y = 0.1-5, the minimum is N = 7 (P2) / 12 (exp-RAR) points. Archetypes: KURVS-like 0.11/0.16; NEEDED-z2.5 0.10/0.13; CRISTAL-like (y 1-5, 0.15 dex) 0.40, does NOT decide. The "RC100-like" row (0.196) assumes one shared f and is misleading; see below.

**POST-FREEZE (labelled, `cfg385_pergalaxy.py`): every galaxy with its OWN free calibration (the realistic case).** With replicated per-galaxy designs this costs NOTHING, because the a0 information simply adds. The binding requirement is therefore that EACH galaxy spans the regimes itself. Twenty discs with 6 points each over y = 0.1-5 at 0.1 dex give 0.05-0.06 dex. A sample with about one point per galaxy (RC100-like, at R_e) carries ZERO a0 information once each galaxy's calibration is free (CFG240 T2: one point cannot break the degeneracy).

## THE SPECIFICATION (the deliverable)
At z ~ 2-2.5, **>= 10-20 individual discs, each with rotation-curve points from y = g_bar/a0 >~ 3 (inside about R_e) out to y <~ 0.3 (about 3-5 R_e), at about 5% velocity precision**, plus:
- the outer velocity-dispersion profile (pressure support is the next wall: CFG140/141/160);
- the baryon profile SHAPES (stars from rest-frame NIR imaging; gas from CO / [CI] / dust maps). Their normalisations are fitted per galaxy, so the absolute calibration drops out.
Kernel-shape systematics (P2 vs exp-RAR) are about 0.03-0.05 dex at this precision and are reported, not removed.

## Where such data may exist (no fetch performed; each needs the owner's go)
- On disk already: KMOS3D cube fits (CFG270), SINS/zC-SINF AO cubes (CFG196/280), KURVS (CFG140, z ~ 1.5, which reaches y 0.06-0.67 outside). A pre-flight can count which INDIVIDUAL galaxies span y >= 3 to <= 0.3 at 5% (local, no download).
- Literature: Genzel+2017 (six individual deep outer curves, z 0.9-2.4); Lang+2017 (stacked to about 4 R_e; a stack mixes per-galaxy calibrations, so it is usable only if stacked in y); newer JWST/NIRSpec and ALMA kinematics (to be scoped).
Sources: [Lang+2017 ApJ](https://iopscience.iop.org/article/10.3847/1538-4357/aa6d82), [arXiv:1703.05491](https://arxiv.org/abs/1703.05491), [arXiv:2006.03046](https://arxiv.org/pdf/2006.03046).

Controls: C1 reproduces CFG240's break-even (0.0999 dex) and C2 (the T4 floor) holds on all 384 cells. MUTATE (deep-only, b = 0.5) makes f and a0 degenerate, rc 1.
