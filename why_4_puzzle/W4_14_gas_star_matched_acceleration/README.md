# W4-14: gas versus stars at the same acceleration. ACCELERATION (the gap is not about baryon type)

**Bottom line.** Inside galaxies, gas-dominated points imply a lower a₀ than star-dominated points (p64: −0.41 dex). Compared at
the **same g_bar**, pooled across SPARC, the two classes agree:

- **Δ_match = −0.096 ± 0.111 dex** (z −0.87, 4 usable bins, log g_bar −12 to −11).
- On the same galaxies and acceleration range, the within-galaxy gap is −0.441 ± 0.059.
- The two differ at about 2.7σ. The RAR inversion gives the same bins.

So **the gap is a position or acceleration effect within galaxies, not a baryon-type effect.** Inferred a₀ falls outward inside
each galaxy, whichever baryon dominates there. Gas points simply sit further out. This is a Simpson's-paradox pattern: the
within-galaxy and the matched comparisons pool different galaxies at a given g_bar.

**What this changes.** The 2026-10-20 "cold-energy clue" (gas-dominated galaxies imply 1.5–2.4× lower a₀) and p64 (A) were
both read as possibly "cold energy tracks stars". W4-14 points instead to something that depends on position or low internal
acceleration:
- an external-field effect, which the κ assumption list currently excludes ("no EFE anywhere");
- outskirts kinematics (warps, non-circular motions, pressure support);
- or outer-disc geometry.

W4-13 already showed it is not the law's transition shape. **The lensing red/blue split (W4-10) is a different fact.** It is
measured at fixed g_bar, so it remains a type effect (or a type-dependent M★/IMF).

**κ = ½ is FITTED.** Not theory closed.

## Results (`w4_14.out`)

| log g_bar bin | n_gas | n_star | Δ_bin (gas − star) |
|---|---|---|---|
| [−12.00, −11.75) | 7 | 8 | −0.085 ± 0.601 |
| [−11.75, −11.50) | 21 | 12 | +0.147 ± 0.235 |
| [−11.50, −11.25) | 29 | 28 | +0.027 ± 0.156 |
| [−11.25, −11.00) | 12 | 59 | −0.310 ± 0.150 |
| **Δ_match** (inverse-variance) | | | **−0.096 ± 0.111** |

**Verdict as frozen: ACCELERATION** (|Δ_match| < 2σ, at least 3 usable bins). There is a power caveat: the matched statistic is
noisier (σ 0.11) than the within-galaxy one (σ 0.06), but it excludes the within-galaxy value at about 2.7σ.

## Controls

- **M1 (label shuffle within bins):** Δ_match +0.070 ± 0.083, within 2σ of 0. PASS.
- **M2 (planted acceleration-only world, as frozen): FAILED** (`w4_14_MUTATE.out`, exit 2). Both failures come from my control
  design, and both are reported unchanged:
  1. With the within-galaxy gap restricted to the matched range, the planted 0.25-slope effect compresses to −0.044 ± 0.033,
     below 2σ.
  2. The noiseless plant leaves a −0.010 dex within-bin residual against an artificially small σ (0.003).
- **Post-hoc control** (`w4_14_posthoc_control.py`, `.out`; **no verdict weight**): the same planted world, with measurement
  noise and the full-range within-galaxy gap. It gives a within-galaxy gap of −0.110 ± 0.037 while Δ_match stays at
  −0.016 ± 0.016. The method does separate an acceleration-only world from a type effect. The data's within-galaxy gap
  (−0.44) is four times the planted one, so the outward decline in the data is steep.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | 9ffc65ac7 |
| `w4_14.py` | numpy, 1 s, 97 MB |
| `w4_14.out`, `w4_14_results.json` | normal run |
| `w4_14_MUTATE.out`, `w4_14_results_MUTATE.json` | M1 PASS, M2 FAIL as frozen; exit 2 |
| `w4_14_posthoc_control.py`, `.out` | post-hoc control, no verdict weight |

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_14_gas_star_matched_acceleration/w4_14.py > why_4_puzzle/W4_14_gas_star_matched_acceleration/w4_14.out
