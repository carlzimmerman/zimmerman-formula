# CFG71 — the universal-fraction question with dynamical SLUGGS masses: the answer stays NO, and SLUGGS drops out of [0, 1]

Script: `CFG71_universal_fraction_dynamical_sluggs.py` (about 4 minutes). Outputs: `.out`, `_results.json`, and the MUTATE pair. Written by a delegated agent with the question declared first and re-run here (main passes 10 of 10; the MUTATE run fails the headline). It copies CFG59's harness and swaps only the SLUGGS population for CFG55's per-galaxy JAM-calibrated estimator (16 galaxies), with the debris scaled by φ in both the calibrating mass and the prediction. The other nine populations are CFG59's, unchanged.

## Question

CFG59 answered NO to "does one φ reconcile ten populations?" with SLUGGS (φ ≥ 0.81) against M31 LVD (φ ≤ 0.30) binding. CFG55 then found that with dynamical stellar masses the SLUGGS deficit grows (law +0.097 dex, 4.0σ; rule +0.046, 2.6σ). Does the answer survive?

## Result

| SLUGGS, dynamical masses | canonical | alt |
|---|---|---|
| offset at φ = 0 (the law) | +0.097 (+3.99σ) | +0.088 (+3.65σ) |
| offset at φ = 1 (the sum) | +0.046 (+2.58σ) | +0.047 (+2.60σ) |
| φ_needed in [0, 1] | **none** | **none** |
| extended root on [0, 6] | none (the offset flattens near +0.02 and never crosses zero; by φ = 6 the calibration excludes 8 of 16 galaxies) | none |
| 1σ interval on [0, 1] | **empty** (smallest \|o/e\| = 2.58 at φ = 1) | empty (2.60) |

CFG59's original SLUGGS interval was [0.81, 1] | [0.68, 1] (the same 16 galaxies with SLUGGS's own masses: [0.77, 1] | [0.63, 1]). **The dynamical masses remove SLUGGS from every φ in [0, 1]**: the conflict is sharper, not resolved. **The universal-φ answer stays NO on both footings.** The empty-interval populations are now SLUGGS and the X-ray ellipticals; the remaining binding pair among populations that do have intervals is the ultra-faints against M31 LVD (gaps 0.087 | 0.164).

## Disclosure

The pre-declared classification rule ("SURVIVES iff the SLUGGS interval, or its extended root, lies entirely above 0.30") was **undefined when SLUGGS has neither an interval nor a root**, and the harness printed **MIXED**. The code had an extended-band fallback (a canonical band starting at 3.198, none for alt) that the docstring did not declare; it is disclosed in the script. R2 (the o/e values above) was added after the first run and before interpretation, reported only. Substantively: no φ in [0, 1] fits SLUGGS within 1σ, so it cannot meet the LVD interval.

## Controls and caveats

C1a: φ = 0 and 1 reproduce CFG45's L and S for the nine unchanged populations (90 comparisons, exact); C1b: SLUGGS at φ = 1 and 0 reproduces CFG55's committed rule and law per-galaxy offsets, means and errors, both footings (16 comparisons, exact); C1b′: the nine unchanged populations reproduce CFG59's committed table including intervals (126 comparisons, exact); C2: every offset is non-increasing in φ. MUTATE (collapse masses ÷ 100): the headline fails as required (the ultra-faints have no solution; SLUGGS stays at +0.097). Fragile: the JAM calibration (CFG33's convention); putting φ into the calibrating mass is the agent's reading of "as CFG59 scales the debris" (CFG59 scales only the prediction); the 16-of-19 sample; red-only collapse masses; isotropic Jeans with hot gas omitted (as CFG55); any φ above 1 rests on a shrinking sample.

## Standing

**Under dynamical stellar masses no single fraction of the sum's debris helps SLUGGS at all, and the low-mass satellites want a quarter of it.** Nothing here says the theory is closed.
