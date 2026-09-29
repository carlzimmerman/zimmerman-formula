# CFG64 — is any headline verdict kernel-sensitive? ν_mono against P2

Script: `CFG64_kernel_robustness.py` (about 50 s). Outputs: `cfg64_kernel_robustness.out`, `_results.json`, and the MUTATE pair (every lane under ν = 1, Newtonian). The harness writes `lane_copies/` and `runs/` at run time (git-ignored). Written by a delegated agent with the question declared first and re-run here (identical outputs). **The main run exits 1: control C3 failed as declared and is kept.**

## The frozen question

Is any headline verdict of CFG40, 41, 42, 45, 46, 51, 56, 58 and 59 (the pass/fail of each declared hypothesis, and the σ of each headline offset) sensitive to the interpolating kernel, ν_mono (the campaign default) against P2 (ν = √(1+1/y); CFG14 found P2 disfavoured at about 2σ by the SPARC transition shape, not excluded)? KERNEL-SENSITIVE if the pass/fail flips or the offset moves by more than 0.05 dex or more than 1σ.

## Result: every headline is KERNEL-ROBUST (H1 passes)

| lane | headline | verdict under ν_mono → P2 | offset |
|---|---|---|---|
| CFG40 | H2 | FAIL → FAIL | +0.107 (1.42σ) → +0.134 (1.75σ) |
| CFG41 | H2 | PASS → PASS | −0.057 → −0.036 |
| CFG42 | H1 | PASS → PASS | rule −0.059 → −0.058; law +3.77σ → +3.90σ |
| CFG45 | H1 | PASS → PASS | (S) −0.41σ both |
| CFG46 | H1 | FAIL → FAIL | +0.206 → +0.210 |
| CFG51 | H1 | PASS → PASS | Boötes I +2.46σ → +2.52σ |
| CFG56 | H2 | FAIL → FAIL | +0.105 (1.67σ) → +0.132 (2.06σ) |
| CFG58 | H1 | PASS → PASS | field dwarfs 0.061 → 0.070 dex |
| CFG59 | H1 | PASS → PASS | φ_needed 0.740 → 0.741 |

The largest move anywhere is 0.027 dex and 0.39σ; the ultra-faint lanes move by at most 0.012 dex. **Of the 22 declared hypotheses exactly one is kernel-sensitive: CFG56 H1** (the bare law fits the 23 super spirals, |mean| < 2σ) flips PASS → FAIL under P2, crossing the 2σ line by a 0.027-dex move; it is not a headline (CFG56's own H2 fails under both kernels). Under P2 the super spirals are a **2.06σ** mean offset, slightly worse than under ν_mono. No alt-footing companion flips.

## A finding about our own lanes

**Several lanes never used ν_mono.** CFG42, 46, 51 and the FG001-derived parts of CFG45, 58 and 59 use `hunt_lib.nu_s`, the exponential RAR form ν = 1/(1 − e^{−√y}), and CFG58's Local Volume dwarfs use `k_contrarian_dwarfefe.nu` (also RAR), **despite their docstrings and READMEs saying ν_mono.** Swapping only `C.nu_mono` left these lanes at zero change, and the harness's bite gate failed as designed on its first run. ν_RAR and ν_mono agree to 3.3 × 10⁻⁹ for y from 10⁻⁴ to 0.1 (the ultra-faint regime) and to 2.3% up to y = 30, so the numbers are unaffected, but the descriptions were wrong. The harness now replaces the kernel functions at code level (covering `nu_mono`, `hunt_lib.nu` and `nu_s`, `k_contrarian.nu` and L23's exec'd ν), so every reference is swapped, and every swap is disclosed in its docstring. **Every lane ran under P2; none was unswappable.**

## Controls and caveats

- **C1 passes:** the ν_mono copies reproduce all nine committed lane results exactly. **C2 passes:** ν_mono(1) = 1.582, P2(1) = √2 = 1.414, and ν(1) equals the swapped value inside every lane copy (the swapped kernel was called 161 to 382,925 times per lane). CFG4's P2 is √(1+1/y), not the brief's √((1+√(1+4/y))/2), which gives 1.272.
- **G1 passes:** every lane changes by more than 10⁻⁶ under the swap.
- **C3 failed, kept as declared:** the control I declared before the first run was CFG41 H2 flipping under ν = 1. It stays PASS (−1.43σ) because with no phantom the rule adds the whole collapse halo, and Newtonian-plus-halo fits the 15 massive spirals. That was a badly chosen control, not a harness fault. **C3b (added after seeing C3, disclosed) passes:** under ν = 1, CFG46 H1 (a headline) flips FAIL → PASS, and CFG40 H1, CFG42 H4 and CFG56 H1 also flip. MUTATE (all lanes under ν = 1): H1 fails as required. Under ν = 1 CFG45 and CFG58 crash (their controls divide by the zero edge phantom), which the harness counts as bite.
- **Fragile:** "P2" is the kernel swapped with everything else frozen, not a self-consistent refit (SPARC Υ = 0.61 came from a ν_mono fit and was not refit). Numbers read from committed results files (CFG42, 58, 59 controls) are not recomputed. Classification is regex over each lane's own detail strings. Verdicts near the 2σ line (CFG40 H1: +1.42 → +1.75σ) would flip under a slightly larger shift.

## Standing

**No headline verdict of CFG40–CFG59 depends on the kernel choice**; the one sensitive hypothesis is a non-headline row crossing the 2σ line by 0.4σ. The kernel description error in six lanes' docstrings is recorded here and in each lane's README. Nothing here says the theory is closed.
