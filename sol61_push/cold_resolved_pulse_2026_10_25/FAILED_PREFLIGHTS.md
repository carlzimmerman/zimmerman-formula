# Failures retained

The 48x96 polar/azimuth refinement preflights were observed outside the bounded runner. The exact scripts and stdout JSON/stderr are retained; they did not record full before/after hashes/UTC provenance, so they are memory feasibility diagnostics rather than full v2 production evidence. They measured 907591680, 795066368, 794329088 and 794836992 bytes, all below1GB but above the unchanged750MB headroom gate. No48x96 production followed. Allocation-only changes were tested against the existing formulas. The preregistered48x80 fallback measured718258176 and passed; actual production has its own complete producer pins/metadata.

The first eta.2 Gauss refinement control reached roundoff and failed its ratio assertion at the smallest dt. Its source/output/error remain gauss_control_initial.*. The eta2 rerun exposes truncation error and shows fourth-order ratios without changing the assertion. Do not report the first failure as a successful convergence result.

The initial smooth-profile support screen used phase labels that could be read as universal for a coarse-grained granular halo. Its exact source/output remain support_screen_initial.*. The current support_screen.py keeps the formulas and explicitly conditions the phase-only inference on the exact instantaneous smooth density.

The first chain implementation could exit0 after8 segments without reaching its target. The ACTUAL seven-segment coarse Draco case reachedT20; the robust generic continuation code is chain_v2.py/evolve_v2.py, with checkpoint mutation controls. Do not infer target completion merely from an exit code.

Refined producer v1's resume path verified source/grid/unit/seed but omitted an explicit dt-match assertion. Its actual first pulse has no resume. v2 adds the assertion for all subsequent unchanged-dt segments; old source is preserved, and timestep comparisons use separate local pulses/references.
