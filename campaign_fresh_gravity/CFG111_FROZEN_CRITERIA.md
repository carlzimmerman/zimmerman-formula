# CFG111 — does the SLUGGS deficit survive published per-galaxy GC density slopes? FROZEN CRITERIA

Written 2026-09-29, before any number of this lane was computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

CFG76 (276c78784, post hoc) showed that the size of the SLUGGS deficit rests on one fixed GC density slope, γ = 3, used for every galaxy:
- the law's JAM-calibrated offset is zero at γ ≈ 1.83;
- the rule's is zero at γ ≈ 2.45.

CFG82 found that per-galaxy slopes cannot be measured from on-disk data. But the SLUGGS team's own mass-estimator paper sets each galaxy's slope from an empirical relation.

## The slopes (declared once)

- **The relation:** Alabi et al. 2017 (MNRAS 468, 3949; arXiv:1701.05904), γ = (−0.63 ± 0.17) log10(M*/M☉) + (9.81 ± 1.94), valid for 2 ≤ γ ≤ 4. They derived it "from a compilation of GC density profiles from the literature" (Alabi et al. 2016).
- **How it was obtained:** the relation and the paper's Table 1 values were read on 2026-09-29 from the paper's ar5iv HTML rendering. No file was downloaded into the repository.
- **Check before freezing:** the relation, applied to the SLUGGS log M* already on disk (`real_research/data/sluggs_forbes2017_galaxies.tsv`), reproduces all 18 quoted Table 1 values to 0.01:

| NGC | 720 | 821 | 1023 | 2768 | 3377 | 3607 | 4278 | 4365 | 4374 |
|---|---|---|---|---|---|---|---|---|---|
| γ | 2.71 | 2.88 | 2.89 | 2.75 | 3.20 | 2.63 | 2.91 | 2.56 | 2.56 |

| NGC | 4459 | 4473 | 4486 | 4494 | 4526 | 4649 | 4697 | 5846 | 7457 |
|---|---|---|---|---|---|---|---|---|---|
| γ | 2.89 | 2.91 | 2.49 | 2.87 | 2.72 | 2.50 | 2.79 | 2.59 | 3.43 |

- **What is used:** γ_i = clip(−0.63 log M*_SLUGGS,i + 9.81, 2, 4). This is a literature calibration, not a fit to the dispersions.
- **Disclosure.** An unsuccessful attempt to read the PDF left a copy of the paper (735.7 KB) in this session's tool-results folder, outside the repository. It is not used.

## Machinery

- CFG55's JAM-calibrated pipeline, executed read-only: h50's GC bins and isotropic Jeans solution, CFG55's calibration, and the rule's debris.
- The only change is γ in the Jeans solution (`sigma_r2`, `sigma_los`), which becomes γ_i per galaxy instead of the global γ = 3.
- The calibrated masses do not depend on γ. The sample is CFG55's 16.

## Checks

- **C1 CONTROL:** with γ_i = 3 for every galaxy, the per-galaxy machinery reproduces CFG55's committed offsets per galaxy (law and rule, canonical) to 1e-9, and the means +0.0970 / +0.0456.
- **C2 CONTROL:** the relation reproduces the Table 1 values quoted above to 0.01 for all 18 galaxies.
- **H1 [HEADLINE; MUTATE must fail]:** with the literature slopes, the law's JAM-calibrated SLUGGS deficit survives: the mean offset exceeds 2σ (galaxy to galaxy) on both footings.
- **H2:** with the same slopes, the rule fits: |mean| < 2σ on both footings.

## Reported rows

- **R1:** the same with SLUGGS's population masses (CFG55's R1 sample).
- **R2, the relation's uncertainty:** every γ_i shifted by ±0.2 and ±0.4. These are declared brackets; the relation's coefficient errors are large and correlated.
- **R3, per galaxy:** the γ that would null the law's offset, set beside the galaxy's literature γ_i.
- **R4:** the four group and cluster centrals (M87, NGC 4365, NGC 4374, NGC 5846) excluded.

## MUTATE

MUTATE=1: γ_i = 1.83 for every galaxy, CFG76's zero point for the law. The deficit should then vanish, so H1 must fail and the script must exit 1.

## Readings (declared)

- **H1 PASS:** the γ caveat does not rescue the law. The published slopes (2.5–3.4) are far from the ≈ 1.8 the law would need, and the deficit remains.
- **H1 FAIL:** with the published slopes the deficit falls below 2σ. The SLUGGS failure was an artefact of the fixed γ = 3.
- **H2** says whether the rule fits once the slopes are realistic.
- **Caveat:** isotropic orbits are still assumed. Anisotropy is the other half of the mass–anisotropy degeneracy, and it is not tested here.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
