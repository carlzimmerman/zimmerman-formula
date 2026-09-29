# CFG111 — does the SLUGGS deficit survive published per-galaxy GC density slopes?

- **Criteria:** frozen in `CFG111_FROZEN_CRITERIA.md` (d36b680bb), before any number.
- **Script:** `CFG111_sluggs_literature_gamma.py`, about 5 s, both footings.
- **Runs:**
  - The main run passes 8 of 8 and exits 0.
  - The MUTATE run (γ = 1.83 for every galaxy) fails H1 and H2 and exits 1.
  - The two runs fail different checks, so the control is informative.

## Bottom line

**The γ caveat does not rescue the law.** CFG76 found that the SLUGGS deficit's size rests on a fixed GC density slope, γ = 3 for every galaxy, and that the law's offset vanishes at γ ≈ 1.83. Here each galaxy instead gets its published slope, from the SLUGGS team's own literature relation (Alabi et al. 2017: γ = −0.63 log M* + 9.81; 2.49 to 3.43 for these galaxies, mean 2.79).

- **The law.** Its JAM-calibrated deficit stays at **+0.082 ± 0.023 dex, 3.6σ** (alt +0.073, 3.2σ). With γ = 3 it was +0.097 (4.0σ).
- **What nulling would take.** The slope that would null each galaxy's offset is far below its published value for the massive centrals: NGC 4365 needs 1.06 (published 2.56), NGC 4374 1.13 (2.56), NGC 4649 1.53 (2.50). For M87, no γ ≥ 1 nulls it.
- **B's derived rule** fits with the same slopes: **+0.028 ± 0.018 dex, 1.55σ** (alt 1.64σ). With γ = 3 it was 2.6σ. With SLUGGS's population masses it is −0.013 (−0.66σ).

| | γ = 3 (CFG55) | published slopes, JAM masses | published slopes, population masses | published slopes, no centrals (N = 12) |
|---|---|---|---|---|
| law | +0.097 (4.0σ) | **+0.082 (3.6σ)** | +0.063 (2.4σ) | +0.046 (2.2σ) |
| rule | +0.046 (2.6σ) | **+0.028 (1.55σ)** | −0.013 (−0.66σ) | +0.016 (0.7σ) |

**The brackets on the slopes (R2)** move every galaxy's γ by the same amount.

| shift in γ | law | rule |
|---|---|---|
| −0.4 | 2.3σ | −0.4σ |
| −0.2 | 3.0σ | 0.6σ |
| +0.2 | 4.2σ | 2.5σ |
| +0.4 | 4.7σ | 3.3σ |

The law stays above 2σ across ±0.4. The rule fits for any shift up to +0.2.

## Controls

- **C1:** with γ = 3 for every galaxy, the per-galaxy machinery reproduces CFG55's offsets exactly (deviation 0.0), and the committed means +0.096982 / +0.045640.
- **C2:** the relation, applied to the SLUGGS stellar masses on disk, reproduces all 18 of Alabi+2017's Table 1 values to 0.000.
- **MUTATE:** with γ = 1.83 for every galaxy, the law's deficit vanishes (+0.0004, 0.02σ), so H1 fails as required. The rule then over-predicts (−3.5σ).

## Caveats

- **Orbits are assumed isotropic.** Anisotropy is the other half of the mass–anisotropy degeneracy, and it is not tested.
- **The slopes are a mass-based literature calibration,** not per-galaxy measurements. The relation's coefficient errors are large and correlated (±0.17, ±1.94); R2 brackets them.
- **The relation's source.** It was read from the paper's ar5iv HTML and verified against its Table 1 (C2). An earlier attempt to read the PDF left a copy (735.7 KB) in this session's tool-results folder, outside the repository. It is not used.
- **The sample** is CFG55's 16. With h50's key fixed (CFG55's key-fix variant) there are 17; that case is not recomputed here.

## Reading

With realistic GC density slopes, the SLUGGS row reads:
- **B's bare law under-predicts the outer GCs by 3.6σ** (JAM masses; 2.2σ without the four centrals). So the γ = 3 caveat does not explain the deficit away.
- **B's derived rule fits** (1.55σ). That restores the rule's one supporting population, which dynamical masses at γ = 3 had put at 2.6σ.
- **The rule's other failures stand:** the satellites and the KiDS split.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
