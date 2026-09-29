# CFG73 -- independent re-derivation of CFG69's ultra-faint LCDM gate

**Question (declared before the first run).** Does CFG69's LCDM ultra-faint result reproduce from code written independently (own Moster inversion, own Kaplan-Meier, own NFW; no CFG69/CFG42 analysis code executed; the only committed code touched is the 6-line h48 `halo_mass` snippet, run as the control comparator)?

**Result: the numbers reproduce; the exact "x0.1 to x100" non-discrimination window is Duffy-full-specific; the MUTATE gate-fail control is not met for Duffy full.** 11 of 12 checks pass; the runner exits 1 because the one load-bearing failure (the broader non-discrimination test) is real.

- KM medians: Duffy full +0.080 (+0.60 sigma), Duffy relaxed +0.015 (+0.11 sigma), Dutton-Maccio -0.043 (-0.35 sigma; CFG69 quotes -0.4 sigma, the difference is in the bootstrap error: 2000 resamples here against CFG69's 1000). Floor scan, total error (0.133), the x0.01..x1000 ladder, and the bare-law pipeline check (+0.325/+0.304 against CFG42) agree to three decimals.
- The stricter non-discrimination test (gate passes for x0.1..x100 under all three concentrations) FAILS: Dutton-Maccio fails at x100 (-2.28 sigma) because its whole window shifts. Under each concentration the pass window is 3.5 to 5 decades wide, so the qualitative claim holds; CFG69's exact edges do not transfer.
- MUTATE (every observed dispersion x0.5) shifts each median by exactly log10(0.5); the gate still PASSES for Duffy full (-1.66 sigma), fails for Duffy relaxed (-2.20) and Dutton-Maccio (-2.75). This was predicted in the docstring before running. The LCDM gate cannot detect a factor-2 error in every observed dispersion under the declared Duffy-full concentration.
- Where the looseness comes from: 0.121 of the 0.133 total error is the collapse-mass floor scan (M_h 1e8 to 1e10 for 39 of 40 objects); the Upsilon_V term is exactly 0 (halo mass held at its Upsilon_V=2 value); adding 1.33 M_HI changes nothing; the estimator is a single-radius sigma^2 = g r / 3 with no Jeans model. Read as a true floor, max(Moster, f) gives +0.080, +0.080, +0.080, +0.023, -0.037.

Scope: this checks CFG69's ultra-faint row only, not its other 15 rows, and CFG42's S value (needs the phantom machinery) was not re-derived. It supports CFG69's reading that the ultra-faint LCDM gate is non-discriminating at these dispersions, which weakens any use of that row as an LCDM pass in the comparison. Not a model comparison.

Files: `CFG73_lcdm_uf_rederive.py`, `.out`, `_MUTATE.out`. Run: `python3 CFG73_lcdm_uf_rederive.py` (rc 1 by design); `MUTATE=1 python3 ...` (rc 1). Re-run in place by the orchestrating session; output identical to the agent's apart from timing lines.
