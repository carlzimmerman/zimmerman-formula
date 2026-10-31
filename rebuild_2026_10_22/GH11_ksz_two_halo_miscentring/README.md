# GH11_ksz_two_halo_miscentring

**Question.** On GH10's published-DR2 bin (CIGALE log M★ 10.5–11): does miscentring remove the inner deficit, can a data-built two-halo shape explain the rise past 0.9 Mpc, and could the remaining gas supply route E's budget?

**Result.** The inner deficit mostly survives realistic miscentring. The two-halo question stays open, because my template doesn't work. **The frozen Q3 class prints BUDGET SUPPLIED, but I read it as NOT SHOWN:** the fit removed no two-halo signal (b = 0), so all of the outer signal was credited to gas. The stop rule does not fire.

## Q1, miscentring: BELOW at the realistic value, removed at the extreme

| Miscentring | A(1.8) | A + 2σ (with 10 % r) |
|---|---|---|
| None (GH10) | 0.45 ± 0.11 | 0.68 |
| **f_s 0.24, σ_off 300 kpc** | **0.54 ± 0.13** | **0.81, BELOW** |
| Extreme: f_s 0.5, σ_off 500 kpc | 0.85 ± 0.19 | 1.27, not below |

f_s 0.24 is derived from the paper's threshold values, which I read through a summariser. Host gas is ignored, which would add signal. The primary value gives A(1) 0.75 ± 0.18 (A + 2σ 1.14 with r, not below), so **GH10's low A(1) does not survive miscentring.** Zhang's normalisation at R_vir is no longer in tension here.

## Q2, two-halo: NOT SHOWN, template unusable

The fit with R_hole 1 Mpc gives b = 0 at every k. But the template's shape depends on the hole: T_n is negative to 7′ with 1 Mpc, shallower with 0.5 Mpc, and A(1.8) moves from 0.54 to 0.84 between them. The negative part is my exclusion, not physics. This is the same failure as GH4's. **This says nothing about whether the two-halo term is small.**

## Q3, budget

Need: M_gas(<1.8 R_vir) = 4.9e11 M☉ (Zhang's profile at the bin's mass).

| k (b = 0 in all) | A | M_gas (M☉) | χ² (13 points) | p (11 dof) |
|---|---|---|---|---|
| 1 | 0.75 ± 0.18 | 1.3e11 ± 0.3e11 | 20.3 | 0.04 |
| 1.8 | 0.54 ± 0.13 | 2.7e11 ± 0.6e11 | 18.2 | 0.08 |
| 3 | 0.61 ± 0.13 | 7.1e11 ± 1.5e11 | 14.1 | 0.23 |
| 5 | 0.70 ± 0.15 | 2.0e12 ± 0.4e12 | 14.2 | 0.22 |
| 8 | 0.68 ± 0.15 | 4.3e12 ± 0.9e12 | 15.8 | 0.15 |

- **Why the frozen label over-reads:** k = 5 and 8 pass the frozen rule, but with b = 0 the signal from neighbouring halos counts as this galaxy's gas. The frozen lock warned of this degeneracy, and the rule still allowed it. My rule was too weak.
- **What holds:** k isn't discriminated, every k is acceptable. Zhang's profile cut at 1.8 R_vir supplies half the need. Cut at 3 R_vir, the mass is above the need by about 1.5σ (M − 2σ 4.2e11, short of the 2σ rule). Above that, the data can't separate gas from neighbours.
- The need itself assumes GH2's k* framing. None of this is a lensing pass; GH2's best route E χ² of 141 stands.

## How this was run

Three runs. **Runs 1 and 2 are discarded** (`AMENDMENTS.md`): a projected hole that removed line-of-sight neighbours, a broken null, a normalisation fault, then a half-grid shift in my convolution. The 500 km/s same-halo cut was chosen after failure 1. The T(θ) points were already seen in GH10, so nothing here is blind.

## Limits

GH10's limits apply: all galaxies, past Zhang's bin, derived bin, points not native. Satellites are modelled as the same gas with a Gaussian offset, a crude form. DR1 neighbours stand in for DR2's, without the M_r cut. Paper values are provisional.

**For the theory.** Route E's extended-gas rescue is neither supplied nor excluded by these points. Zhang's profile to 1.8 R_vir is about half the need, even with realistic miscentring; gas beyond that can't be separated from neighbours. A(1) no longer signals a problem at R_vir, so the earlier reading that points to normalisation weakens. κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework or that the law wins.

## Checks

Run 3: K1 GH10 reproduced 0.4480; K2 σ_off → 0; K3 injection; K4 rotated null max |z| 1.09; MUTATE flip. All PASS, yet the template is unusable: K4 didn't test hole dependence.

## Files

`FROZEN_CRITERIA.md` (30091d4a1c), `AMENDMENTS.md`, `gh11.py`, `gh11.out`, `gh11.json`.
