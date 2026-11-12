# EUC7 (SLOW-TAIL KERNEL ON THE LENS GATES): RESULT

2026-11-12. Criteria f4d4b5ae46 (committed alone, before any script or number). A test lane; it adopts nothing.

## Verdict: INSIDE THE WINDOW / INSIDE THE WINDOW (canonical / alt), on SLACS lensing at the true source redshifts

The Codex phase-2 kernel `μ★(x) = 1 − 1/√(1 + 2x)`, unscreened, with nothing fitted, makes the 70 SLACS lenses with
**1.04 × (canonical) / 1.00 × (alt) their Salpeter stellar mass**: `b_lens` = +0.015 [−0.005, +0.039] / +0.001
[−0.019, +0.026]. Law S on the same lenses needs +0.082 / +0.070 (1.21 × / 1.17 ×), the shortfall A55 and A70 recorded.
The stars' dispersions agree: `b_dyn` = +0.039 / +0.030, and lensing and dynamics differ by +0.04 dex (ONE POTENTIAL
HOLDS). All four instrument checks pass; the mutation twin exits 1.

It does not make Euclid's wide lenses: 58 % / 52 % of them still exceed the ceiling with the source at infinity
(WIDE LENSES BREAK THE CEILING on both footings). That residual does not depend on the kernel.

**This is not a pass of the kernel.** As written it adds 5.27e-7 m/s² at 1 AU, which the Solar System excludes by many
orders of magnitude; it has no rotation-curve test; and screening it changes the field in exactly the regime tested
here. What the lane shows is narrower: at lens-core accelerations the data ask for a cold pull that keeps growing with
acceleration, as the slow tail does, more than one that saturates at a₀.

κ = ½ FITTED. Footings never pooled. No outcome favours the framework.

## 1. Numbers

`b` = log₁₀ factor on the Salpeter stellar mass. Window: −0.25 (Chabrier) to +0.10.

| Test | Slow tail, canonical / alt | Law S on the record | Word |
|---|---|---|---|
| T1 SLACS lensing, true source redshifts (N = 70) | +0.015 [−0.005, +0.039] / +0.001 [−0.019, +0.026] | +0.082 / +0.070 | INSIDE THE WINDOW |
| T2 SLACS dynamics | +0.039 [+0.003, +0.079] / +0.030 [−0.010, +0.072] | +0.085 | INSIDE THE WINDOW |
| T2 dynamics minus lensing | +0.039 / +0.045 | +0.032 | ONE POTENTIAL HOLDS |
| T3 Euclid ceiling, sample P, source at infinity: f₂₅ | 0.105 [0.095, 0.116] / 0.094 [0.085, 0.104] | 0.156 / 0.139 | NO VERDICT (at the floor) |
| T3 median `b∞` | −0.095 / −0.120 | −0.019 / −0.044 | |
| T4 Euclid wide lenses (grade B, θ_E ≥ 1.7″): f₂₅ | 0.581 [0.492, 0.669] / 0.516 [0.427, 0.605] | 0.758 / 0.702 | WIDE LENSES BREAK THE CEILING |
| T4 median `b∞` | +0.290 / +0.268 | +0.364 / +0.343 | |
| T5 Euclid dynamics (DESI dispersions on the SLACS scale, N = 55) | +0.085 [+0.009, +0.147] / +0.076 [+0.003, +0.138] | +0.135 / +0.128 | AT AN EDGE (reading) |

On SLACS, 1 % / 3 % of lenses would need stars lighter than Chabrier: the kernel does not overshoot.

## 2. Checks (all pass)

| Check | Result |
|---|---|
| S1 kernel inversion, g_N/a₀ from 1e-6 to 1e8 | max error 1.3e-13 |
| S2 deep limit and tail | 1.0008 ; 1.0000 |
| S3 unscreened Solar correction at 1 AU, canonical | 5.268e-7 m/s² (Codex: 5.27e-7) |
| S4 law S through the same code | radius ratio 0.8852 ; `b_dyn − b_lens` +0.032 |
| MUTATE newton | T1 median +0.015 → +0.159 and +0.001 → +0.159; exit 1 |

## 3. What this says

1. **The galaxy-scale lens amplitude is sensitive to the kernel's tail, and prefers the slow one.** Law S misses SLACS
   by 0.07–0.08 dex. Replacing the saturating cold pull with one that grows as √(g a₀/2) removes the miss with no
   parameter. The difference between the kernels is 0.07 dex in stellar mass, against a 0.02 dex statistical error.
2. **It is IMF-degenerate, as A70 said of the whole gate.** Both kernels sit inside any honest stellar-mass window
   (law S near the top, the slow tail at Salpeter). The result does not exclude law S; it says a Salpeter stellar
   population plus the slow tail needs nothing further on SLACS.
3. **Lensing and dynamics still agree** under the slow tail (0.04 dex), as under law S (0.03): one potential.
4. **The wide-lens residual stays.** Half or more of Euclid's wide lenses exceed the ceiling under the slow tail too.
   EUC4's finding is not an artefact of the kernel choice.
5. **Euclid's own galaxy-scale lenses sit lower with the slow tail** (median `b∞` −0.10 / −0.12; dynamics +0.08).
   EUC1-F and the sealed forecast EUC5-F were frozen for law S and are not regraded here.
6. **For the action search.** The Codex lane reached this kernel from a health condition (non-negative clock curvature
   in its unscreened parent class), not from data. Here it meets a data gate it was never tuned to. That is one
   independent point in its favour and no more: the same kernel fails the Solar System unscreened and is untested on
   rotation curves, where its transition is stronger than law S's (at g_N = a₀ it gives g = 1.86 a₀ against 1.62).

## 4. Next gates for this kernel (not run here)

- Rotation curves: the radial-acceleration relation and per-galaxy fits with the slow tail, same stellar-mass rules as
  the law S record.
- A screened static solution, then these lens gates again on it.

## 5. Files

`euc7.py`, `euc7.out`, `euc7_results.json`, `euc7_MUTATE_newton.out` / `_results.json` (exit 1). Imports EUC1's and
EUC5's code. Kernel source: `research_closure_2026_11_12/euclid_desi_phase2/theory/THEORY_CHECKPOINT.md` §4.


## Dated note (2026-11-12, evening): the Euclid dynamics row (T5) was one lens short

T5 reads EUC5's amended per-lens file, which held 55 lenses; one DESI spectrum (EUCL-DR1-L016656) arrived after that
file was made (see EUC5 RESULT.md §3e). Re-run in a copy of the lane folders with the 56-lens file in place
(`euc7_final56.out`):

| T5, slow-tail kernel, sample S | 55 lenses (above) | 56 lenses |
|---|---|---|
| canonical | +0.085 [+0.009, +0.147] | +0.076 [+0.008, +0.147] |
| alt | +0.076 [+0.003, +0.138] | +0.067 [+0.001, +0.131] |

The reading keeps its label (AT AN EDGE). T1–T4 and the lane word (SLACS lensing, INSIDE THE WINDOW / INSIDE THE
WINDOW) do not use that file and are identical in the re-run.
