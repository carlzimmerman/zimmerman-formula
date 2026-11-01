# HS1_hsb_lsb_residual_slope: N1 TILTED, LAW FLAT. Every version of route E's mass-only halo misses with surface brightness at fixed V_flat; the a₀ law doesn't. Argon's sign was wrong, its test was right

Criteria: `FROZEN_CRITERIA.md` (f40b664795), committed alone before any script or number. `hs1_slope.py`, `hs1.out`, `hs1_results.json`, MUTATE `hs1_MUTATE.out`. Post-result, reported only: `hs1_stress.py`, `hs1_stress.out`, `hs1_stress.json`. κ = ½ FITTED; footings never pooled; not theory closed.

## Frozen grade
SPARC, V_flat 60–120, Q ≤ 2, Inc ≥ 30°, Υ 0.50, n 47 (1 dropped). δ = V_model/V_obs − 1 at 2 R_d, slope b on lg SBeff.

| Model | b per dex | σ | class | Spearman | rms δ |
|---|---|---|---|---|---|
| N1 | −0.227 | ±0.069 (−3.3σ) | TILTED − | −0.54 | 0.229 |
| N0 | −0.173 | ±0.064 (−2.7σ) | TILTED − | −0.44 | 0.232 |
| N2 | −0.266 | ±0.072 (−3.7σ) | TILTED − | −0.60 | 0.251 |
| F (FC1's floor), canonical | −0.262 | ±0.070 (−3.8σ) | TILTED − | −0.60 | 0.237 |
| F, alt | −0.288 | ±0.073 (−3.9σ) | TILTED − | −0.63 | 0.269 |
| **Law, canonical** | **−0.016** | **±0.061 (−0.3σ)** | **FLAT** | −0.04 | 0.195 |
| Law, alt | −0.023 | ±0.063 (−0.4σ) | FLAT | −0.04 | 0.197 |

Background B moves route E's slopes by 0.006 or less. Verdict on background A: **N1 TILTED, LAW FLAT.** F is tilted too, so there's no [F DIFFERS].

**The sign.** b < 0 means route E over-predicts low-surface-brightness galaxies and under-predicts high-surface-brightness ones at 2 R_d. The halo depends on M_b alone, so at fixed mass it can't follow the discs.

**Argon's numbers.** N1 +0.085 ± 0.020: measured −0.227, MISS, wrong sign. Law 0.00 ± 0.015: measured −0.016, CLOSE. Its reason (the floor survives, N1 dies) also fails: the floor is tilted as much as N1.

## Is it real? (post-result, reported only)
| Cut | N1 | F | Law |
|---|---|---|---|
| at fixed lg V_flat | −0.162 ± 0.077 (−2.1σ) | −0.163 ± 0.077 (−2.1σ) | +0.079 ± 0.066 (+1.2σ) |
| at fixed lg M_b | −0.257 ± 0.070 (−3.7σ) | −0.277 ± 0.073 (−3.8σ) | −0.024 ± 0.067 |
| on lg SBdisk | −0.241 ± 0.061 (−3.9σ) | −0.259 ± 0.061 (−4.3σ) | −0.041 ± 0.055 |
| on lg SBdisk at fixed lg V_flat | −0.195 ± 0.065 (−3.0σ) | −0.193 ± 0.062 (−3.1σ) | +0.005 ± 0.059 |
| V_flat 60–90 (n 28) | −0.269 ± 0.093 (−2.9σ) | −0.287 ± 0.099 (−2.9σ) | +0.007 ± 0.093 |
| V_flat 90–120 (n 19) | −0.108 ± 0.113 (−1.0σ) | −0.126 ± 0.104 (−1.2σ) | +0.053 ± 0.083 |
| Q = 1 (n 32) | −0.284 ± 0.099 (−2.9σ) | −0.319 ± 0.096 (−3.3σ) | −0.045 ± 0.080 |
| Inc 45–80° (n 31) | −0.222 ± 0.068 (−3.3σ) | −0.262 ± 0.070 (−3.8σ) | −0.014 ± 0.064 |
| without the 5 largest \|δ\| | −0.134 ± 0.052 (−2.6σ) | −0.168 ± 0.057 (−3.0σ) | −0.023 ± 0.048 |

The law stays flat on every cut. Route E stays tilted on all but the smallest bin, weakest at fixed V_flat on SBeff (−2.1σ). Leave-one-out moves N1 only between −0.262 and −0.199. So it isn't one galaxy, and the trend survives the cuts, though at 2–4σ from 47 galaxies and not more.

**Free Υ hides it.** With each galaxy's best Υ, as in the SPARC line, N1's fitted Υ runs ×1.65 per dex of SBeff (Spearman +0.50, p 4e-4) and F's ×1.86 (p 6e-5). The law's runs ×1.12 (p 0.32). That's why the SPARC line never showed this: Υ absorbs most of the tilt. Half or more of these fits sit at the grid's edge, so the size of that slope is rough.

**What S would be needed.** Matching V_obs at 2 R_d with each galaxy's own M200 needs lg S_need to rise +0.315 ± 0.079 per dex of SBeff (Spearman +0.60, p 9e-6), median 109 M☉/pc², 16–84 % 68–218, scatter 0.27 dex. The rule's median there is 93.

**Contraction goes the right way and costs the normalisation.** N1 with Blumenthal at strength f, Υ 0.50:
| f | slope | mean δ | rms δ |
|---|---|---|---|
| 0 | −0.227 ± 0.068 | −0.019 | 0.229 |
| 0.5 | −0.159 ± 0.069 | +0.050 | 0.230 |
| 1 | −0.100 ± 0.070 | +0.114 | 0.254 |

A response that depends on the baryons does reduce the tilt, and full contraction leaves −1.4σ. But then the model runs 11 % high on average, the same over-prediction CN1 found as Υ 0.31. LC1 measures what f really is.

**Could the zooms' own scatter supply it?** `hs1_scatter.py`, `hs1_spin.py`. The rule has no scatter in S at fixed mass, and the zooms do: 0.150 dex at 10¹², 0.102 at 10¹³ and 10¹⁴ (X77, ng 48 at the two cluster masses). If lg S ranked with lg SBeff at correlation r, N1 reads:
| r | slope | mean δ | rms δ |
|---|---|---|---|
| 0 | −0.227 ± 0.068 | −0.019 | 0.229 |
| 0.5 | −0.102 ± 0.066 (−1.6σ) | −0.028 | 0.208 |
| 1 | +0.032 ± 0.066 (+0.5σ) | −0.034 | 0.202 |

So the size of the scatter is enough at r near 0.9, and rms comes close to the law's 0.195. What's missing is a reason for the ranking. A disc's surface density at fixed mass goes roughly as λ⁻², so I set a line before measuring: this needs ρ(S, λ′) at or below −0.8 at fixed mass. In the 27 ng 64 zooms at z_f: **ρ = −0.453, p 0.018, bootstrap 68 % [−0.62, −0.26]. RANKING NOT NATIVE**, but it has the right sign and is real at that sample size, and low-spin zooms do have higher S. Even taken at full value it gives about half the needed slope, since SBeff doesn't rank perfectly with spin. Limit: these are isolated spheres with no external tidal torque, median λ′ 0.011 where real halos have about 0.035, so their spins are internal asymmetry and may not rank as real ones do.

**Where the tilt lives.** Gas-dominated galaxies (n 31): N1 −0.311 ± 0.112 (−2.8σ), law −0.014 ± 0.114. Star-dominated (n 16): N1 −0.041 ± 0.070, law +0.041 ± 0.053. So Υ can't be the cause: it's in the galaxies where Υ hardly matters. Those are the ones with V_flat at the low end.

**How this reads.** The mass-only rule fails this test and the law passes. That doesn't kill route E's physics: the zooms' scatter, tied to spin, gives up to about half, and contraction goes the same way. Neither is derived for this purpose, and together they'd have to be shown to work without spoiling the SPARC line's normalisation.

## Checks
K1 slope against `polyfit` 1e-16. K2 this path against NF1's table: Υ exact, ΔV 0. MUTATE δ + 0.1 x: every slope +0.1 to 8e-17; N1 goes TILTED to FLAT.

## Limits
47 galaxies, fixed Υ. All route E versions take M200 from EM1's fitted relation, with no scatter. Only V_flat 60–150 was looked at, and 2 R_d is about where a cored halo's mass is growing fastest. The law's kernel here is the simple ν.
