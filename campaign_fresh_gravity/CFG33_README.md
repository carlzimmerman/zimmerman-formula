# CFG33 — the SLACS Einstein radii under candidate B: lensing against dynamics

Script: `CFG33_slacs_lensing_vs_dynamics.py`, about 6 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Every Einstein mass is doubled, and the headline H2 fails (4.8–4.9σ, rc = 1).
- The main run exits 1: H3 failed (2.7σ against a declared 3σ). That is reported as run.

κ = ½ is fitted. Both footings are used.

## Question

The failures summary carried the SLACS lenses as liability B7. Under the law, 70 SLACS lenses (Auger+2009) get only 79–85% of their Einstein mass at a Salpeter IMF (`hunt_2026/h53_h54_slacs_lenses.py`). The Einstein radius comes out 14–18% short.

At the Einstein radius (~4 kpc) g_N ≈ 10 a₀, so the phantom adds only 14–20%. B's prediction is the law:
- T5 makes galaxies phantom-dominated. CFG32 showed the cluster max rule over-predicts an elliptical's inner mass.
- Ownership gives no external field.

h53 itself called this a liability "at the level of the stellar-mass systematic". So the right question is not whether Salpeter fits. It is **whether the stellar mass the lenses need under B equals the stellar mass B's own law needs for the dynamics of galaxies at the same velocity dispersion.**

## Method (declared before the first run)

- **Lensing:** h53's machinery (de Vaucouleurs stars, the law's projected phantom, Auger's measured f_*), exec'd read-only with B's kernel ν_mono. Per lens, α_lens is the stellar-mass normalisation (relative to Auger's Salpeter masses) at which B's law gives mean convergence 1 at the observed Einstein radius.
- **Dynamics:** ATLAS3D. Per early type (JAM quality ≥ 1), α_dyn is the stellar mass at which B's law reproduces the published JAM mass inside the half-light sphere, relative to ATLAS3D's Salpeter population M/L. This is h9's convention: M_JAM ≈ 2 M_1/2.
- **Match:** log α_dyn is fitted linearly in log σ_e and evaluated at each lens's dispersion. The statistic is the median difference, with a bootstrap over both samples.
- **Floor:** 0.10 dex, declared before the first run. It covers two population libraries, two bands, two IMF implementations and the aperture difference.

## Results

**Controls.**
- C1: h53's committed κ̄ is reproduced (0.8246 / 0.7938 canonical; 0.8542 / 0.8124 alt).
- C2: h9's ATLAS3D sample (258) and its Wolf/JAM offset (+0.207 dex) are reproduced.

| | canonical V | canonical I | alt V | alt I | verdict |
|---|---|---|---|---|---|
| H1: κ̄ at Salpeter under ν_mono | 0.834 | 0.807 | 0.859 | 0.825 | PASS: the shortfall stands at Salpeter |
| α_lens (× Salpeter) | **1.23** | 1.27 | 1.20 | 1.24 | |
| α_dyn at the lenses' dispersions | **0.86** | 0.86 | 0.85 | 0.85 | |
| H2 (headline): difference, with the floor | **+0.159 ± 0.102 → 1.56σ** | +0.171 → 1.68σ | +0.152 → 1.49σ | +0.168 → 1.64σ | PASS |
| … statistical only (R2) | 7.6σ | 7.8σ | 6.9σ | 7.5σ | |

**H3 FAILED.** Under B's law, ATLAS3D's stellar-mass normalisation rises with dispersion at 2.7σ, against a declared 3σ: slope +0.20 ± 0.08, from 0.72× Salpeter at 100 km/s to 0.83× at 200 and 0.90× at 300. The lenses' own slope is steeper (+0.45).

**Reported.**
- In dispersion bins, the lenses need 1.19–1.26× Salpeter where ATLAS3D gives 0.83–0.86×.
- The P2 kernel gives the same picture (difference +0.165 dex).
- The lenses' 1.23× Salpeter is about 2.2× a Chabrier IMF.

## Standing

**B7 formally passes the pre-declared test, but narrowly, and the margin is the floor.**
- Under B's law the lenses need about 1.23× Salpeter stellar mass.
- B's own dynamics, at the same dispersion, need about 0.86×.
- The gap is 0.16 dex, a factor 1.45. With the declared 0.10-dex floor for the two surveys' different stellar-population zero points it is 1.5–1.7σ. On statistics alone it is 7–8σ.

So the recorded "14–18% short at Salpeter" is not by itself a failure of the law; a heavier IMF absorbs it. But B's own dynamics do not supply that heavier IMF at the same dispersion. The consistency holds only if Auger's and ATLAS3D's Salpeter zero points differ by about 0.1 dex or more in the needed direction.

**What decides it:** lensing and dynamics of the same galaxies with one stellar-population model. SLACS's own dispersions are the natural route, but h54 found them limited by the V/I effective-radius ambiguity. The alternative is putting both surveys on one population library.

Nothing here says the theory is closed.
