# W4-13: is the within-galaxy gas/star gap a law-shape effect? GAP NOT LAW-SHAPE

**Bottom line.** p64's finding stands under every declared law form. Inside the same galaxies, gas-dominated points imply a
lower a₀ than star-dominated points:

| law | Δ_g (dex) |
|---|---|
| L₀.₅ (softer than simple) | −0.377 ± 0.103 |
| L₁ (simple, canonical) | −0.408 ± 0.085 |
| L₁.₅ | −0.394 ± 0.073 |
| L₂ (AG4's quadratic a₀-line) | −0.376 ± 0.066 |
| RAR (exponential) | −0.406 ± 0.083 |

No law closes it. The planted-world control shows why it cannot. When the truth is L₀.₅ and the data are read with simple μ,
the law-shape mismatch produces a gap of only −0.022 ± 0.006 dex, about twenty times smaller than the observed −0.41. So the
gap is not about how the law bends between the regimes. It is a property of the baryons, or of how their masses are counted:
- gas-dominated points carry less "cold energy per baryon" than star-dominated ones;
- or the stellar and gas masses inside discs are wrong in a position-dependent way (W4-12: a universal correction cannot do it).

**κ = ½ is FITTED.** Not theory closed.

**My disclosed hand expectation was wrong in one detail.** I expected the sharper n = 2 to widen the gap; it narrows it
slightly (−0.376). The verdict, GAP NOT LAW-SHAPE, matched the expectation.

## The SPARC RAR fit per law (frozen; weak)

| law | χ²_min | Δχ² | best a₀ | κ_Λ |
|---|---|---|---|---|
| L₀.₅ | 117 753 | 0 | 8.38e-11 | 0.448 |
| L₁ (simple) | 121 482 | +3 729 | 1.33e-10 | 0.708 |
| L₁.₅ | 127 476 | +9 723 | 1.61e-10 | 0.861 |
| L₂ | 134 150 | +16 397 | 1.79e-10 | 0.955 |
| RAR | 122 681 | +4 928 | 1.37e-10 | 0.730 |

**Caveat.** This is the frozen one-parameter fit with Υ fixed at 0.5 for every galaxy. χ²/point is about 37, so per-galaxy
M/L and distance dominate and the Δχ² ranking is not reliable. AG4b, which fits Υ per galaxy, finds n = 1 and n = 2 equivalent
on SPARC. The verdict does not depend on this fit, because no law closes the gap at all. The κ values here are dominated by
high-acceleration points and are not κ determinations.

## Checks and control

- **K1:** n = 1 and RAR reproduce p64 (−0.4075, −0.4065).
- **MUTATE (planted L₀.₅ world at κ = ½):** L₀.₅ closes exactly (+0.000), and L₁ shows a gap (−0.022 ± 0.006). Exit 1 by design.

## Disclosure

The first MUTATE run (`w4_13_MUTATE_firstrun_sigma0.out`, kept) exited 2. My control check used a strict |Δ| < 2σ, which fails
on a noiseless plant where σ = 0. It now uses ≤ 2σ + 10⁻⁹. The physics output was identical; the normal run was redone with the
same values.

## Files

`FROZEN_CRITERIA.md` (117727995), `w4_13.py` (numpy, 1.7 s, 88 MB), `w4_13.out` / `_results.json`, `w4_13_MUTATE.out` /
`_results_MUTATE.json`, `w4_13_MUTATE_firstrun_sigma0.out`.

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_13_gap_vs_law_shape/w4_13.py > why_4_puzzle/W4_13_gap_vs_law_shape/w4_13.out
