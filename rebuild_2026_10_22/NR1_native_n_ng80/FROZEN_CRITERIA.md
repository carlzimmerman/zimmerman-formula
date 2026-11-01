# NR1_native_n_ng80: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Version N's SPARC pass (Υ 0.68–0.71, X80, NF1) uses η(10¹²) from ng 64, 25.94. At ng 80 the same estimator reads 21.53 [14.55, 24.89] on nine seeds (AQ1). Does N still pass?

**Standing.** κ = ½ FITTED. No a₀ in the cold sector, so canonical and alt coincide. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. Not blind: AQ1's η is known, and no SPARC number at it is.

## Rule
N as NF1 grades it: `nf1_x74.py`, X74's grader with FC1's conversions, contraction off, no floor, core shape by hand. Only the η inputs change. f★ 0.034, as `nf1_native_read.py`. Stars are fitted per galaxy, so SPARC's line doesn't use f★.

## η inputs
| Run | η(10¹⁰) | η(10¹¹) | η(10¹²) | ρ₁₀, ρ₁₁ |
|---|---|---|---|---|
| **PRIMARY** | 29.26 (X80, ng 64) | 24.34 (X80, ng 64) | **21.53** | 1.359, 1.131 |
| **ALT, ratios held** | scaled with the anchor | scaled with the anchor | 21.53 | 1.128, 0.938 |
| **Band low** | as PRIMARY | as PRIMARY | 14.55 | 2.011, 1.673 |
| **Band high** | as PRIMARY | as PRIMARY | 24.89 | 1.176, 0.978 |

PRIMARY holds what was measured at each mass. ng 80 hasn't run at 10¹⁰ or 10¹¹, so resolution is mixed across the seam, disclosed. ALT assumes those masses would fall by the same factor. η(10¹³) 23.54 and η(10¹⁴) 22.10 stay CE1's A4 values. The band varies the anchor only, so it is not a full error budget. The grader takes c_f, so η(10¹²) is converted by CE1's own map.

## Verdict
- **N PASSES AT NG 80:** PRIMARY rms ≤ 0.110 and Υ 0.50–0.80 on both backgrounds.
- **N FAILS AT NG 80:** otherwise.
- **[ANCHOR-DEPENDENT]** if ALT's line differs from PRIMARY's. **[NOISE-LIMITED]** if either band run's line differs from PRIMARY's.

## Reported, not graded
Υ, ΔV and S against ET1 by V_flat, groups Z, and the failing list, as NF1's read.

## Expected, on record before running
PRIMARY Υ 0.70–0.78, line passes. The band-low run may leave the line, so [NOISE-LIMITED] is possible.

## Checks
- **K1:** CE1's map inverted at 25.937 returns 8.0503 within 1e-3.
- **K2:** with η(10¹²) 25.937 and ρ 1, 1 this path reproduces `NF1_N0`: Υ, rms and cluster predictions |d| ≤ 1e-9.
- **MUTATE:** η(10¹²) × 0.5, ρ held, separate output: Υ must move more than 0.02.
- Any failure: no verdict, exit 1.

κ = ½ FITTED. Not theory closed.
