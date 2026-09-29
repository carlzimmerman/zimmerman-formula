# CFG68 — the ΛCDM control for CFG40/CFG56: is the super-spiral miss specific to the law?

- **Criteria:** frozen before any script or ΛCDM prediction existed, in `CFG68_FROZEN_CRITERIA.md` (1808d8bee).
- **Script:** `CFG68_lcdm_super_spirals.py`, about 5 s.
  - It executes CFG56's galaxies, baryons (Hernquist bulge + Freeman disc), radii, `stat()` and `floor()` read-only, up to CFG56's scoring loop.
  - ΛCDM enters only as new branches of the `pred()` hook.
- **Outputs:** `.out` / `_results.json` and the MUTATE pair.
  - The main run **exits 1**, because H1 failed.
  - The MUTATE control (v_obs × 0.25) **exits 1** as required.

## Bottom line

**Under the frozen reading, CFG40/56's marginal miss is generic, not specific to the law. H1 FAILED.**
- **ΛCDM misses too.** It was run through exactly the same galaxies, baryons, radii and error model, with Mandelbaum+2016's measured blue halo masses and NFW halos, and nothing tuned. It also under-predicts the nine fastest super spirals:
  - ΛCDM: **+0.121 ± 0.054 dex (2.26σ)**;
  - B's law: +0.164 ± 0.070 (2.34σ).
- **The two models nearly coincide here.** Galaxy by galaxy, ΛCDM's predicted speeds are only 0.043 dex faster than the law's, and the offsets track each other. With these inputs the super spirals barely tell the two apart.
- **The ΛCDM verdict depends on the halo mass at the top of the blue relation, as the frozen reading requires us to say.**
  - Colour-blind Moster+13 halos (10^13.4–10^14.9 M☉) over-predict and pass: −0.108 (−1.39σ).
  - Mandelbaum's +1σ blue halos pass: +0.047 (0.77σ).
  - The −1σ bound fails badly: +0.321 (5.8σ).
  - From log M_* = 11.47 up, the blue relation is flat (⟨M_200m⟩ = 10^12.79 h⁻¹ M☉) and poorly measured (+0.43/−1.01 and +0.58/−2.23 dex). The inputs cannot decide.
- **The test has leverage.** With the halo switched off, the nine sit at +0.333 (3.17σ). The halo moves mean₉ by 0.212 dex, which is 4.0σ₉.

| statistic (canonical) | B's law (CFG56, committed) | **ΛCDM headline** (blue, M_200c − M_b) | R1 Moster+13 | R5 no halo |
|---|---|---|---|---|
| all 23, mean offset | +0.105 ± 0.063 (1.67σ) | **+0.061 ± 0.047 (1.30σ)** | −0.105 ± 0.076 (−1.39σ) | +0.258 ± 0.095 (2.73σ) |
| slope against log M_b | +0.166 ± 0.092 (1.80σ) | **+0.179 ± 0.082 (2.20σ)** | −0.114 ± 0.069 (−1.65σ) | +0.199 ± 0.128 (1.55σ) |
| the nine fastest | +0.164 ± 0.070 (2.34σ) | **+0.121 ± 0.054 (2.26σ)** | −0.108 ± 0.077 (−1.39σ) | +0.333 ± 0.105 (3.17σ) |
| nine, own floor (R6) | 2.36σ | 2.60σ | — | — |

ΛCDM has no a₀, so it has one set of numbers. The law's alt footing gives +0.090 (1.46σ) for all 23 and +0.149 (2.17σ) for the nine fastest.

## The rest (as run)

**H2 passed:** all 23 at +0.061 ± 0.047 (1.30σ), where the law is at 1.67σ. Both models fit the sample as a whole.

**The trend is steeper for ΛCDM.** Its offsets rise with baryonic mass at 2.20σ, against the law's 1.80σ. CFG56's three-clause H2, the test the law failed on one clause, **fails for ΛCDM on two** (the slope and the nine fastest; R3).

**R4, the halo brackets:**

| halo | nine fastest | z₉ | all 23 | z |
|---|---|---|---|---|
| blue, M_200c − M_b (headline) | +0.121 | 2.26 | +0.061 | 1.30 |
| blue +1σ (the table's ep) | +0.047 | 0.77 | +0.012 | 0.21 |
| blue −1σ (the table's em)* | +0.321 | 5.82 | +0.184 | 4.77 |
| full M_200c (CFG67's accounting) | +0.112 | 2.06 | +0.054 | 1.13 |
| (1 − f_b) M_200c (= B's rule's debris at f_ex = 1) | +0.134 | 2.33 | +0.076 | 1.47 |

\* At −1σ the halo falls below the galaxy's own baryons in the nine galaxies with log M_* ≥ 11.59, so their dark mass is clipped to zero (the frozen rule). Eight of those are among the nine fastest, so this row is close to R5 (no halo). This count is a post-run check, not in the committed output; see the departures section.

The bookkeeping choice does not flip the verdict. The halo relation and its +1σ lensing error do.

**The nine fastest, galaxy by galaxy (R2):**

| galaxy | v_obs (km/s) | law offset | ΛCDM offset | log M_200c | halo share of v² at r |
|---|---|---|---|---|---|
| 2MFGC 12344 | 568 | +0.260 | +0.232 | 12.84 (clamped) | 0.60 |
| OGC 0139 | 483 | +0.276 | +0.217 | 12.84 (clamped) | 0.67 |
| 2MFGC 08638 | 465 | +0.284 | +0.188 | 12.84 | 0.82 |
| OGC 1304 | 453 | +0.130 | +0.110 | 12.84 | 0.46 |
| OGC 0441 | 444 | +0.181 | +0.142 | 12.84 | 0.58 |
| 2MASX J11232039+0018029 | 436 | +0.206 | +0.146 | 12.82 | 0.72 |
| 2MASX J16184003+0034367 | 384 | +0.125 | +0.081 | 12.84 | 0.65 |
| OGC 1312 | 344 | +0.030 | +0.006 | 12.84 | 0.47 |
| OGC 0926 | 342 | −0.018 | −0.032 | 12.84 | 0.43 |

- **Where the offsets come from:** ΛCDM's two largest offsets are the two galaxies above the blue relation's top bin, whose halo masses are clamped.
- **Signs:** 18 of 23 ΛCDM offsets are positive, including 8 of the nine.
- **Halo share of v² at r:** 0.43–0.82 over all 23 (median 0.60).
- **The paper's own dark mass (diagnostic only; never an input):** it fitted dark masses inside r that exceed the comparator's by a median 0.36 dex, and 0.47 dex for the nine. That fit used its own baryon model.

**Controls pass exactly.**
- **C1:** CFG56's own three controls pass in the executed slice. Its committed law numbers are reproduced with zero deviation (canonical +0.104625, 0.062785, +0.163638, z₉ 2.3407; alt +0.090247, +0.148809).
- **C2:** CFG36's committed red-relation M_200c for its seven X-ray ellipticals is reproduced with zero relative deviation, and the 200m → 200c identity holds to 2.9 × 10⁻¹⁵.
- **C3:** the NFW gives M(<R_200c)/M_200c − 1 = 2.2 × 10⁻¹⁶, and the Moster inversion round-trips to 8.1 × 10⁻⁹.

**MUTATE (every v_obs × 0.25, through CFG56's VF):**
- Every offset shifted by exactly −0.602 dex, and every σ was unchanged.
- H1 failed at z₉ = −8.99 and H2 at z = −11.46, so the script exits 1.
- The same nine galaxies were selected.

## Departures from the frozen file (disclosed)

- **None in any check, threshold, statistic or reading rule.** The outputs are from the first run of each mode, and no bug was found or fixed.
- **Additions to the reported output only:**
  - a Moster log M_200c column in the per-galaxy table;
  - a printed line confirming that the selected nine match the frozen list;
  - the law's statistics recomputed with the run's own speeds, printed beside the others (identical to CFG56's committed numbers in the main run; shifted by −0.602 under MUTATE);
  - in R5, how far the halo moves mean₉.
- **One post-run check (not in the committed output):** which galaxies the −1σ bracket clips to zero dark mass. It was evaluated with the script's own `halo()` function after both runs, and it changes no number.
- **Derived here from the committed JSON:** the 0.043-dex mean difference between the two models' offsets, the sign counts and the median halo share (TABLE in `_results.json`).

## Standing

**The super spirals no longer count against the law specifically** (the declared reading of an H1 fail with mean₉ > 0).
- Standard ΛCDM with a measured halo also under-predicts the fastest of them, by nearly the same amount.
- The suspects are therefore:
  - the shared inputs: the W1 stellar masses (the ±0.2-dex floor term dominates both models' error), the inclinations, the maxima of noisy Hα curves, and the gas estimate made without HI;
  - or physics that both models lack.
- **This does not favour either model.** Both miss marginally (2.3σ) in the same direction, and ΛCDM's verdict turns on a halo mass that lensing does not pin down at log M_* ≳ 11.5.

## Caveats (frozen up front)

- **Pure NFW.** Adiabatic contraction would raise ΛCDM's speeds and feedback cores would lower them; neither is scored.
- **z = 0 halo relations.** They are applied as in the machinery; the galaxies sit at z = 0.06–0.28.
- **Mean relation.** The mean stellar-to-halo relation is applied to individual galaxies, with no scatter drawn.
- **Stellar masses.** The W1 masses stand in for Chabrier masses.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.


## Corrections from the referee sweep (appended 2026-09-29; no result changed)

- **"The MUTATE control exits 1 as required" says nothing here.** The main run also exits 1, because its headline H1 fails (ΛCDM also misses the nine fastest). The MUTATE adds a failure of H2 and shifts the statistics (above), but the exit code does not tell the two runs apart.
