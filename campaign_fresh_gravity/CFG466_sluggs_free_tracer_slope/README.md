# CFG466: do the four SLUGGS centrals still fail with the GC tracer slope free?

**Frozen criteria:** `FROZEN_CRITERIA.md`, commit 03b9e83e1. It was committed alone, before any CFG466 number was computed.

**Fixed inputs:**
- Law and baryons exactly as CFG330 K0 / CFG331. The script execs CFG331's source read-only.
- Kernel ν_mono, κ = ½ FITTED, both footings (9.36e-11 | 1.13e-10).
- On-disk data only. No knob scans.

## Bottom line

**Headline by the frozen rule: ROBUST FAIL.** In all four decision cells, 3 of the 4 centrals stay excluded at ≥ 2σ with the tracer slope free. The cells are K0 (stars only) and R-own (CFG331's ownership reading), each on both footings.
- **The three that fail:**
  - M87, with its measured GC profile;
  - NGC 4365 and NGC 5846, with γ marginalised over the declared prior U[2, 4].
- **NGC 4374 is FRAGILE in every cell.** The Gaussian test gives 2.1–2.3σ, but the empirical bootstrap tail has p = 0.026–0.039, which is below 2σ. It has 41 GCs and one outer bin.

**The fixed slope γ = 3 did not create the fail.** The ledger's slope-artefact flag (row 12) is not supported.

**The margin depends on the reading.** Under R-own it is thin, and it holds only for isotropic orbits (see "Qualifiers").

### Per central (Z_free = Gaussian-equivalent significance with γ free; outcome by the frozen rule)

| central (tracer) | K0 canonical | K0 alt | R-own canonical | R-own alt |
|---|---|---|---|---|
| M87 (measured, Agnello+14, MC 300) | >8, FAIL | 7.5, FAIL | 2.52, FAIL | 2.27, FAIL |
| NGC 4365 (prior U[2,4]) | 6.0, FAIL | 5.6, FAIL | 5.25, FAIL | 4.84, FAIL |
| NGC 4374 (prior U[2,4]) | 2.33, FRAGILE (p_E 0.026) | 2.18, FRAGILE (0.034) | 2.24, FRAGILE (0.030) | 2.09, FRAGILE (0.039) |
| NGC 5846 (prior U[2,4]) | 6.4, FAIL | 6.0, FAIL | 2.98, FAIL | 2.59, FAIL |
| **class** | ROBUST FAIL | ROBUST FAIL | ROBUST FAIL | ROBUST FAIL |

The reported readings R-bar, R-barN and R-efe are also ROBUST FAIL on both footings. R-efe has 4 of 4 failing.

### Offsets (dex, canonical) and the slope the law would need

| central | γ = 2 | γ = 3 (= committed) | γ = 4 | per-galaxy σ_Δ | γ_null, K0 | γ_null, R-own |
|---|---|---|---|---|---|---|
| M87 (power law) | +0.197 | +0.275 | +0.332 | 0.017 | none ≥ 1 | 1.80 |
| M87 measured profile | — | — | — | 0.017 | Δ_c = +0.218 | Δ_c = +0.133 |
| NGC 4365 | +0.122 | +0.205 | +0.265 | 0.023 | 1.07 | 1.63 |
| NGC 4374 | +0.117 | +0.201 | +0.262 | 0.074 | 1.12 | 1.57 |
| NGC 5846 | +0.129 | +0.213 | +0.274 | 0.022 | 1.05 | 1.92 |

The γ = 2–4 columns are K0. For comparison:
- M87's measured profile has local slopes of 1.87–2.34 at its outer bins.
- The Alabi+16 relation gives 2.54–2.62 for these four galaxies.
- Under K0 the law needs γ ≈ 1.05–1.2. Under R-own it needs 1.57–1.95.

The centrals' mean, with an independent γ draw per galaxy (reported): +0.209 ± 0.021 (Z 7.8) under K0 and +0.178 ± 0.021 (Z 5.7) under R-own, canonical.

## Qualifiers (reported rows; the frozen class rule is applied to each)

- **Radial anisotropy, β = +0.5, with free γ.**
  - K0 stays ROBUST FAIL. NGC 4374 clears.
  - **R-own becomes NOT DIAGNOSTIC: all four clear.** That includes M87, at 1.64 / 1.40.
  - With the host gas truncated at its measured X-ray edge (a post-freeze diagnostic), R-own at β = +0.5 still has only 2 of 4 failing (NGC 4365, NGC 5846), so it stays NOT DIAGNOSTIC.
  - So under the ownership reading the fail rests on isotropy. Isotropy is the record's assumption: no β table for these galaxies is on disk (CFG323).
  - β = −0.5 gives ROBUST FAIL in every cell.
- **Wide prior U[1.87, 4]**, i.e. down to M87's own measured minimum slope.
  - K0: ROBUST FAIL.
  - R-own: NOT DIAGNOSTIC. NGC 5846 drops to 1.8–2.0σ.
- **Alabi relation prior** N(γ_rel, 0.29), truncated to [2, 4]: ROBUST FAIL in all four cells.
- **NGC 5846 under R-own** depends on the extrapolated host gas.
  - At shallow slopes its prediction is dominated by host gas extrapolated beyond the 30 kpc X-ray edge: Δ(2) = +0.031, against +0.129 for stars only.
  - Truncating the gas at the edge (post-freeze) raises its Z_free from 3.0 to 5.8.
  - The extrapolation helps the law, so the fail survives it.
- **M87 under R-own.**
  - The Monte Carlo over Agnello+14's published errors (taken as independent) widens Δ to +0.044..+0.241 (2.3–97.7%).
  - With the central profile alone, Z is 7.6. The MC is what brings Z_free down to 2.5.
- **Systematics not propagated:** JAM M/L, distance and Hernquist scale. A post-freeze headroom estimate gives the extra per-galaxy error in σ_los that would clear each central at its most favourable admissible slope:
  - K0: 0.05–0.075 dex for M87, NGC 4365 and NGC 5846.
  - R-own: 0.013 for M87, 0.045 for NGC 4365, and 0 for NGC 5846 at the γ = 2 edge.

**Honest reading.**
- Under K0, free slopes do not rescue the law. The centrals would need tracer slopes near 1.1, and nothing on disk is that shallow.
- Under R-own the excess is still there at γ free and β = 0, but at only 2.3–3σ for M87 and NGC 5846. Radial anisotropy or a slope as shallow as M87's could remove it.

## MUTATE (`_MUTATE.out`; 2/2 pass)

- **M1 PASS.** γ = 3 forced for all four reproduces the committed CFG330 K0 and CFG331 R-own/R-bar/R-barN/R-efe offsets to 1.1e-16 (40 values).
- **M2 PASS.** γ = 1.5 forced moves the headline from ROBUST FAIL to NOT DIAGNOSTIC. How it moves:
  - **K0 canonical stays ROBUST FAIL even at γ = 1.5.** M87, NGC 4365 and NGC 5846 sit at Z = 8.3, 2.8 and 3.2.
  - The headline moves because of K0 alt, where NGC 4365 becomes FRAGILE.
  - It also moves because of R-own. There a ρ ∝ r^−1.5 tracer integrates the host gas out to Mpc scales, the law over-predicts, and the result is REVERSED.
  - Reported: "every Z is lower at γ = 1.5" is FALSE, only for M87 under K0: 8.33 vs 8.21 canonical, 7.55 vs 7.47 alt. That comparison is a fixed-slope Z against the MC-marginalised Z_free. M87's offset itself falls from +0.218 to +0.145.

## Controls (main run, 6/6 pass)

| ID | Result |
|---|---|
| C1 | The γ = 3, β = 0 path reproduces the committed CFG330 K0 and CFG331 own/bar/barN/efe offsets to 1.1e-16. |
| C2 | The general-ρ Jeans code with ρ = r^−γ equals the power-law path to 1.1e-16. |
| C3 | Abel deprojection of a Plummer profile: slope error 5.7e-6. |
| C4 | The Agnello central profile with the K0 field reproduces CFG323's "M87 no gas" offset, +0.21780 / +0.20620, with difference 0.0. |
| C5 | The bootstrap SD on a synthetic NGC 5846 is 0.0264, against an SD of 0.0251 over 300 independent realisations (ratio 1.05). |
| C6 | The bootstrap binning code reproduces CFG331's bins exactly. |

All 4000 bootstrap resamples were usable for each central. The table-interpolation error is 6e-5 dex or less.

## Method (summary)

- **Tracers.**
  - M87 uses the Agnello+14 three-population Sérsic sum, from CFG323's script-parsed values. It is Abel-deprojected, with 300 MC draws from split normals.
  - NGC 4365, 4374 and 5846 have no GC density profile on disk. Pota+13 shows its fits only in Fig. 6. The Alabi+16/17 γ values are relation outputs. The spectroscopic positions are biased (CFG82). These three get the prior γ ~ U[2, 4] on a single power law, marginalised on 101 points.
- **Per-galaxy error.** A bootstrap over the GCs (N_B = 4000, seed 466) runs through the full CFG331 pipeline: cut, 3σ clip, equal-number bins, ML σ and the outer-bin rule.
- **FAIL** requires both a Gaussian p ≤ 0.02275 and an empirical bootstrap p ≤ 0.02275, averaged over the prior. An empirical p printed as 0 means < 1/4000.

## Disclosures

1. **Test runs before the full run.** After the freeze, reduced-size runs (N_B 200, N_MC 6) were made in a scratch directory to debug the script. The decision rule was not changed. Changes made after them:
   - the Gaussian tail is computed as Φ(−x) instead of 1 − Φ(x) (precision only);
   - Z ≥ 8 prints as ">+8";
   - three post-freeze diagnostics were added: the reported-row classes, R-own with gas truncated at the X-ray edge, and the systematic headroom. The test run had shown R-own's sensitivity to extrapolated gas at shallow slopes, which prompted them. None of them is a decision row.
2. **Abel grid.** The deprojection is evaluated on 0.3 kpc to 1e6 kpc. All GC bins lie inside that range. C4 reproduces CFG323's full-grid value exactly.
3. **Shortcuts in the reported rows.** The β = ±0.5 rows and the M87 β rows reuse the β = 0 bootstrap, with Δ* shifted by Δ_obs(β) − Δ_obs(0).
4. **Split normal.** The split normal puts equal probability on each side of the published value. Independence between parameters is declared.
5. **Not changed by this lane:** the frozen CFG323/CFG330/CFG331 verdicts, the LEDGER, and STANDING.

This is not an a0 measurement. κ = ½ is fitted.

## Files and run

| File | Content |
|---|---|
| `FROZEN_CRITERIA.md` | the frozen rule (03b9e83e1) |
| `cfg466_free_slope.py` | the lane script: about 7 min for the main run, about 1 min for MUTATE, one process |
| `cfg466_free_slope.out`, `_results.json` | main run, 6/6 checks |
| `cfg466_free_slope_MUTATE.out`, `_MUTATE_results.json` | MUTATE M1 + M2, 2/2 |

```
python3 campaign_fresh_gravity/CFG466_sluggs_free_tracer_slope/cfg466_free_slope.py
CFG466_MUTATE=1 python3 campaign_fresh_gravity/CFG466_sluggs_free_tracer_slope/cfg466_free_slope.py
```

Run the main run first: MUTATE reads its headline.
