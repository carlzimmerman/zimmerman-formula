# CFG58 — the cold-mass rule on more populations: the sum switches itself off above M_b ≈ 2 × 10⁷ M☉

Script: `CFG58_rule_more_populations.py` (about 5 s). Outputs: `.out`, `_results.json`, and the MUTATE pair (collapse masses ÷ 100). Written by a delegated agent (readings and criteria declared before the first run; only the bare law L and the sum S, no new readings) and re-run here. **The main run exits 1: control C1 failed and is kept** (below).

## What was scored (canonical | alt, offset in σ, positive = data above the prediction)

| population | L (bare law) | S (the sum) | verdict |
|---|---|---|---|
| Coma ultra-diffuse galaxies (CFG31) | +1.33 \| +1.11 | +0.69 \| +0.61, f_ex = 0 | spared (S = L; the lower σ is the declared collapse-mass floor) |
| NGC1052-DF2 / DF4 | Newtonian-exempt by FG001; blind: −3.28 / −1.51 | same, change 0.000 dex | L and S both fail the blind version; the rule adds nothing |
| tidal dwarfs (six Lelli+15 objects) | χ² 1.09 exempt; blind χ² 131 \| 152 | same, f_ex = 0 | L and S both fail the blind version; the rule adds nothing |
| LV dwarfs "statistic C" | +1.41 \| +1.42 | +1.02 \| +1.13 | both pass; Δslope 0.013 |
| **LV field dwarfs (n = 13)** | −0.60 \| −0.85 | **−3.47 \| −2.70** | **S breaks** (change 0.061 dex; in L's error the significance is only −1.4 \| −1.3σ) |
| SPARC low-surface-brightness (n = 85) | 100% < 0.03 dex | 100% (f_ex = 0) | spared |

## The structural finding

**S switches itself off when f_ex = 0**, that is when the law's edge phantom already exceeds (1 − f_b) M_c. That holds above M_b ≈ 2.3 × 10⁷ M☉ (canonical; 1.5 × 10⁷ alt) for M_* = M_b/2, and above 5.5 × 10⁷ for M_* = M_b. **Every population except the lowest-mass Local Volume dwarfs lies above this mass, so S equals L there by the rule's own arithmetic.** The rule breaks only the sub-3 × 10⁷ M_b dwarfs, the same signature as CFG42's classical-satellite failure. It spares everything heavier.

## Controls and caveats

- **C1 failed, kept.** One comparison (XR27's statistic-C observed slope and error) differs by 2–5 × 10⁻⁹ against a 1 × 10⁻⁹ tolerance, because the campaign footing `C.A0_SI` is the rounded FP0 pair. A reported diagnostic added after the first run (C1b) reproduces it exactly with FP0's exact a₀; the other 32 comparisons pass.
- C2 passes (with M_c ≈ 0, S = L everywhere). MUTATE (collapse masses ÷ 100): every change is below 0.01 dex and the headline "S changes at least one population by more than 0.05 dex" fails as required.
- Fragile: the Moster relation clamped at 10⁹ M☉ below M_* ≈ 1.6 × 10⁴ (only the statistic-C dwarfs); the ×0.1/×10 collapse-mass floor for the UDGs and statistic C is my declaration (CFG31 had none); M_c is set by stellar mass only; the field-dwarf significance depends on the error model; the SPARC test is CFG36's point-mass proxy; the DF2/DF4 and tidal-dwarf exemptions come from FG001, not from the rule.

## Standing

**The sum is harmless above M_b ≈ 2 × 10⁷ M☉ and harmful below it.** This adds nothing new for the sub-3 × 10⁷ M_b regime beyond CFG42: the rule's problems live where the law's own phantom is smaller than the collapse mass. Nothing here says the theory is closed.

**Kernel note (CFG64).** This lane's estimator uses the exponential RAR kernel (`hunt_lib.nu_s`, ν = 1/(1 − e^{−√y})), not ν_mono as the text above says; the two agree to 3 × 10⁻⁹ for y ≤ 0.1. Swapping the kernel to P2 leaves the headline verdict unchanged (see `CFG64_kernel_robustness/README.md`).
