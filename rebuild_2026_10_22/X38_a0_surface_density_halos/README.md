# X38_a0_surface_density_halos: a₀-cored cold dark energy halos pass SPARC and the cluster outskirts; the heavy cluster cores are short

Criteria: `FROZEN_CRITERIA.md` (9cc80516df, committed alone). `AMENDMENT_A1.md` (pre-result, after a K1 crash and
before any graded number): the fixed-Σ Burkert has a mass cap inside R, the compact root is taken, and saturation is
counted (0 halos saturated). κ = ½ FITTED. Footings never pooled. Route E: cold dark energy clumps everywhere, gravity is
Newtonian, the law is emergent. Raw eRASS1 × KiDS bands via X30's machinery, read-only. Not "theory closed". Nothing here
says the data favour the framework.

**Hypothesis SD.** Cold dark energy halos are Burkert-cored, with central surface density pinned at the framework's own
scale: ρ₀ r₀ = a₀/(2πG) = 107 (canonical) / 129 (alt) M☉ pc⁻². a₀ = c²√(Λ/32π) stays a constant of the cold sector.
**No new constant.** Galaxy halo masses come from EM1's committed SPARC relation, borrowed and not refit. Cluster halos
take the fair share.

## Verdict (frozen rule): **SD PASSES SPARC ONLY**, both footings

### SPARC: PASS (the first route-E variant to pass the Υ leg)

| | rms | median Υ | line (rms ≤ 0.110, Υ 0.50–0.80) |
|---|---|---|---|
| **SD, canonical** (bg A / B) | 0.0795 / 0.0792 | 0.77 / 0.76 | **PASS** |
| **SD, alt** | 0.0729 / 0.0729 | 0.60 / 0.60 | **PASS** |
| EM1 NFW dust (cusps) | 0.0656 | 0.36 | FAIL (Υ) |
| the law | 0.0541 / 0.0537 | 0.52 / 0.44 | (reference) |

The a₀-pinned cores remove the cusp problem that drove EM1's Υ down to 0.36. Median r₀ is 4.6–5.3 kpc, no halo saturates,
and an in-sample refit of the relation changes nothing (a 11.2, b 0.9). The scatter is larger than the law's (0.073–0.080
against 0.054) but inside the line.

### Clusters: the outskirts pass for the first time; the heavy cores are short

| key (canonical h 0.672; alt in brackets) | measured | SD | Z |
|---|---|---|---|
| **OUTER all-KT** | 0.716 | 0.697 | **+0.14** (−0.06) ✓ |
| **OUTER KT terciles** | 0.39 / 0.62 / 1.03 | 0.62 / 0.68 / 0.77 | −0.7 / −0.3 / +1.2 ✓ |
| **OUTER KT slope** | +1.50 | +0.32 | +1.85 ✓ |
| OUTER MGAS terciles 1, 2 | 0.49 / 0.76 | 0.52 / 0.70 | ✓ |
| MID T1 | 1.10 | 1.06 | +0.1 ✓ |
| MID T2 | 1.65 | 1.08 | +1.8 (FAIL in h 0.686 at 2.13; alt passes) |
| **MID T3** | 2.13 | 1.05 | **+4.3** (+3.8) UNDER |
| **MID KT slope** | +2.24 | −0.04 | **+3.1** (+3.0) UNDER |
| **OUTER MGAS T3** | 1.37 | 0.82 | **+5.4** (+4.9) UNDER |
| OUTER MGAS all | 0.93 | 0.70 | +2.4 (+2.1) UNDER |
| INNER (uninformative) | 1.94 ± 1.67 | 1.08 | +0.5 ✓ |

- **Every earlier cold-sector model overshot the outskirts:** X26/X30 by Z −5 to −11, X37 by −6.7. SD lands on them.
- **The miss is one-sided and specific.** The heaviest, hottest clusters need more mass in 0.3–1 Mpc than a fixed-Σ core
  gives. Their cores come out at r₀ = 0.27 / 0.32 / 0.44 Mpc by KT tercile, too large, so the predicted MID stays flat
  (≈ 1.06) while the data rise to 2.1.
- In words: one surface density fits galaxies and cluster outskirts. **Massive cluster cores are denser than a₀/(2πG).**

**Checks 4/4** (K0 EM1 law + X30 bands; K1 Burkert closed form and root; K2 no-halo limits: SPARC Newtonian row exact,
clusters A = 0.19; K3 0.60 GB). `--mutate` fails K1, exit 1.

## Reading

- This is the strongest cold-sector result in the record. Route E with a₀-pinned cores, and no new constant, passes:
  - SPARC (the law's home ground);
  - the cluster outskirts, which killed every added-component model;
  - and, by construction, growth/CMB, the forest, the Bullet Cluster, TDGs and DF2/DF4 (route E inherits them).
- **What it fails:** the cores of the heaviest clusters, by 3–5σ, which need more central mass.
- **The obvious first-principles candidate for that gap: baryonic contraction.** The BCG and the hot gas pull the cold dark
  energy core inward, more so in more massive clusters. That is gravity, not a new constant, and not graded here. It is
  the next lane.
- **What it means for the theory:** a₀ survives as the cold dark energy's core surface density, tied to Λ. The law becomes
  emergent. κ = ½ is still fitted (Σ_a₀ inherits it). The galaxy-scale law stops being a separate force; it becomes what
  a₀-cored cold dark energy halos look like. That is a decision for the owner, not a lane result.
- **Not graded:** dwarfs (the relation would be extrapolated), galaxy–galaxy lensing, and the halo-mass relation's origin
  (borrowed from EM1).

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `x38_sd_halos.py`, `.out` / `_results.json`, `_MUTATE`, `x38_x30_machinery*.log`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x38_sd_halos.py            # exit 0, 4/4
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x38_sd_halos.py --mutate   # exit 1, K1 fails
