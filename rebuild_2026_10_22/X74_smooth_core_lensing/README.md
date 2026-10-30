# X74_smooth_core_lensing

> **Lane-ID collision.** A peer session's `X74_all_measured_native_cf` (criteria c3e69578c5, 19:02) took the X74 id
> first. This lane (bc08edb85a, 19:10) is a different lane. Always cite it by its full directory name,
> `X74_smooth_core_lensing`, never as bare "X74".

**Question.** X73 passed the X43 line set on the canonical footing with the smooth core and every input measured. It did
not regrade galaxy lensing. Does X70/X73's smooth core change X53's KiDS-1000 isolated-lens grade (Brouwer+21, 4 bins,
full covariance)?
- **Method:** X53's committed script, with one change, the halo shape: B_S, with η scaled by B1/B_S(1), so η = 10.82 at
  c_f = 4.
- Criteria were frozen first (bc08edb85a), including the expectation that Δχ² would move by less than 20.

## Verdict: SHAPE DOES NOT MOVE THE LENSING GRADE. OUTER LENSING DISCRIMINATES: LAW, both footings

Δχ²(H2H − L2H), all radii, with 2h:

| footing | Burkert (X53) | smooth | change |
|---|---|---|---|
| canonical, all radii | +429.6 | **+423.7** | −5.9 |
| canonical, R ≤ 0.31 Mpc | +133.1 | +127.2 | −5.9 |
| alt, all radii | +455.6 | **+458.4** | +2.9 |
| alt, R ≤ 0.31 Mpc | +144.5 | +147.4 | +2.9 |

The change was within the pre-registered |Δ| < 20. **Route E's halos still fail galaxy lensing by Δχ² ≈ 420–460**,
whatever the core shape.

## With the halo mass freed (X53 AMENDMENT A1 profile, reported only)

Best common shift in log M200, truncated at R200, Δχ² vs L2H:

| | Burkert (X53 A1) | smooth |
|---|---|---|
| canonical, R ≤ 0.31 Mpc | −12.5 (shift +0.35) | **+27.7** (+0.30) |
| canonical, all radii | +87.8 (+0.50) | **+157.1** (+0.45) |
| alt, R ≤ 0.31 Mpc | +12.5 (+0.35) | **+76.9** (+0.25) |
| alt, all radii | +129.8 (+0.50) | **+251.3** (+0.40) |

Untruncated, smooth: +27.9 / +101.2 canonical, +76.0 / +196.2 alt.

- At the frozen SPARC masses the shape does not matter: the normalisation gap (+0.3 to +0.5 dex in M200) swamps it.
- **Once the mass is freed, the smooth core fits the lensing shape worse than Burkert,** by about 40 (inner) to 120
  (all radii) in χ².
  - Freed inside 0.31 Mpc, Burkert can tie the law. The smooth core cannot (+28 / +77).
  - This is the first line where the smooth core is worse than Burkert. On the X43 lines it was strictly better.
- So shape does not rescue lensing. The lensing problem is the halo mass relation (SPARC M200 too low by ~0.3–0.5 dex
  for these lenses), plus the edge, plus, for the smooth core, the profile shape. Leakage of non-isolated lenses (X53's
  caveat) still limits the outer part.

## Reading for the flagship

X73's canonical all-measured pass covers SPARC, the groups and the clusters. **Galaxy-scale lensing remains a hard
fail for route E halos** (Δχ² ≈ +424 canonical), and the smooth core makes the freed-mass fit worse, not better. Any
claim about the X70/X73 halo must carry this line. κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy
is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.

## Checks

- **K1:** with the Burkert switch, the script reproduces X53's committed χ² exactly (L, H, L2H, H2H, primary and all,
  both footings; max |d| = 0). X53's own 10/10 internal checks pass in every run.
- **K2:** B_S(1) = 0.69707. The smooth closed form matches quadrature: X53's K_B check, re-pointed at the smooth
  density, passes.
- **MUTATE:** X53's mutate (no truncation, law ν = 1) flips the class to HALOS for the smooth shape too, as for Burkert
  (−862 / −854 all radii), so the harness is sensitive.
- One thread, peak RSS 0.16 GB, ~2 min per run. X48 A4 was undisturbed.

## Files and reproduction

- `FROZEN_CRITERIA.md`
- `x74_lensing.py`: runs X53's source with the shape patch and writes `x74_lensing_{S,B,S_MUTATE}.out`,
  `x74_lensing_results_*.json` and `x74_grade_*.json`.
- `x74_diag_A1.py`: X53's A1 profile on the smooth source; writes `x74_diag_A1_S.out` and `_results.json`.

Run:

    X74_SHAPE=S PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x74_lensing.py      # X74_SHAPE=B -> K1; X53_MUTATE=1 -> MUTATE
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x74_diag_A1.py
