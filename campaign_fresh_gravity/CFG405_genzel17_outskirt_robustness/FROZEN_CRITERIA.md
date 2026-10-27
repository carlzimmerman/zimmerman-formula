# CFG405 FROZEN CRITERIA: does the Genzel+2017 residual tension survive outskirt cuts and inclination shifts?

Committed alone, with its LEDGER row, before any script exists. κ = ½ FITTED; not theory closed. No dark-matter particle. This lane sizes a recorded tension. It is not an a0(z) measurement, and no output says the data favour the framework. Owner (2026-10-27): "Yes, write frozen criteria for a CFG401 robustness rerun (drop outermost point, fold sides, inclination variants)". ID CFG405 is a spare in the owner's 10-06 reserved block 400–409, and the owner chose it.

## Why
- CFG401 (230413b75c): G-CONSISTENCY failed, and three discs reached the grid edge at a0 → 0.
- CFG402 (frozen 1d58728ee): summed DE-law penalty 7.99 canonical (WEAK) / 9.63 alt (REAL), on the 9 line. Post-freeze, it is one galaxy: without zC 406690 the other five sum to 2.05 / 2.46. zC 406690 costs 4.0–5.9 across inclinations 13 / 25 / 37°, and zC 400569 costs only 0.50.
- de Araujo-Carvalho+2025 (arXiv:2507.10544; reading note `data_assembly/timeline/READING_deAraujoCarvalho2025_2507.10544.md`) simulates cosmic-noon IFU observing and finds three things: dimming removes the high-velocity outskirt values, asymmetry grows outward, and inclinations are biased face-on. It gives no slope-bias number, so it is used here only to choose which selections to test, never as a correction.

## Not blind (disclosed)
Before freezing, I have seen the beyond-FWHM point lists of two galaxies (cfg400_points.csv, observed major-axis v):
- **zC 406690:** +0.622″ 105.0, +0.772″ 98.8, +0.922″ 81.9, −0.628″ 117.2, −0.737″ 105.2, −0.897″ 89.1, **−1.018″ 68.0, −1.207″ 38.1**. The steep fall is on the approaching side only, beyond the receding side's last point (0.922″).
- **zC 400569:** five points at 205–223 km/s and **+0.982″ 183.5**, one-sided.

I have also seen CFG402's per-galaxy penalties. **Expectation:** V1 and V2 lower zC 406690's penalty, because both remove its −1.207″ point and V2 also removes −1.018″. The null controls N1/N2 exist because of this expectation: dropping any points lowers a penalty somewhat, so the outermost points must be shown to be special. The other four galaxies' point lists have not been looked at for this lane.

## Inherited, unchanged (comparability with CFG402)
Everything below is exec'd read-only from `CFG401_genzel17_gas_shape/cfg401_gas_shape.py`, using the same pre-`LF` split as cfg402_tension.py:
- the CFG401 primary shape (stars exponential + 1-kpc bulge, gas disc at 2 R_d, Table 1 gas priors)
- the 0.6″ FWHM cut
- Genzel's drift term 3.36 σ0² R/R_1/2
- the 0.05 dex error floor
- ν_mono from CFG4_common
- f profiled on LF = linspace(−4, 3, 701)
- the a0 grid SC = logspace(−3, 2, 251) × a0_footing
- both footings (canonical 9.3603e-11, alt 1.1312e-10)

**Disclosed inherited inputs, not native and not changed here:**
- Table 1 kpc/″ (the paper's cosmology)
- the DE-law w0/wa (−0.838, −0.62)
- the rival E(z) with Ω_m = 0.315 (a comparator only)

Changing them is out of scope. The graded quantity is the DE-law penalty.

## Statistic (CFG402's, unchanged)
Per galaxy: Δχ²_DE = χ²(a0 = a0_foot · de(z)) − min over SC of χ², with f profiled. Graded: **S = Σ over galaxies of Δχ²_DE**, on the primary shape, for each footing. Also reported per variant: the per-galaxy rows, the rival and pure-Newton penalties, and zC 406690's penalty alone.

CFG402's classes are reused: **REAL if S ≥ 9, WEAK if 4 ≤ S < 9, NOISE if S < 4.** A galaxy left with fewer than 4 beyond-FWHM points is DROPPED (CFG401's rule). It contributes 0, and the dropped count is printed in every row.

## Variants (data selection and geometry only)
- **V0 BASELINE:** CFG402 primary, exactly.
- **V1 DROP-OUTERMOST:** per galaxy, remove the one beyond-FWHM point with the largest |offset| (either side).
- **V2 FOLD-COMMON:** per galaxy, set r₊ and r₋ to the largest |offset| among *all* digitised v points on the receding and approaching sides, including those inside the FWHM. Keep only beyond-FWHM points with |offset| ≤ min(r₊, r₋). This drops one-sided outskirt points.
- **V3− / V3+ INCLINATION:** all six galaxies at i_T1 − 10° and at i_T1 + 10°, clipped to [10°, 85°]. The data are rebuilt from the points, with V and eV divided by sin i, exactly as CFG401 does at i_T1. σ0 and the drift term are unchanged.
- **V4 LELLI-i (reported only, not graded):** zC 400569 at 54.5° (Lelli+2023 CO 3-D fit, CFG278), the others at i_T1.

## Controls (all must pass, or the lane is INVALID and nothing is read)
- **K1 reproduction:** V0 reproduces CFG402's committed per-galaxy Δχ²_DE to ≤ 0.01 each (printed to 2 decimals), and S = 7.99 / 9.63 to ≤ 0.01. Because of CFG402's HERE override, its outputs live in `CFG401_genzel17_gas_shape/cfg402.out` and `cfg402_results.json`. CFG405 must write only inside its own directory.
- **K2 identity:** the rebuild path at Δi = 0 equals V0 bit for bit.
- **K3 planted outskirt defect:** each galaxy's g_obs is replaced by the canonical DE-law curve at its own V0 best f (noiseless, same errors), then the outermost beyond-FWHM point's g_obs is multiplied by 0.6. Required: V0 S_plant ≥ 4, and V1 S_plant ≤ 0.5.
- **N1 null for V1:** 200 draws (numpy default_rng(405)). Per galaxy, drop one beyond-FWHM point chosen uniformly from all but the outermost. Report the percentiles of S per footing. **V1 is SPECIAL** if V1's S is below the 5th percentile of N1 on both footings.
- **N2 null for V2:** 200 draws (default_rng(4052)). Per galaxy, drop as many beyond-FWHM points as V2 drops, chosen uniformly from those V2 keeps. If a galaxy has too few kept points, drop all its kept points except what CFG401's 4-point rule needs, and print it. **V2 is SPECIAL** if V2's S is below the 5th percentile of N2 on both footings.
- **MUTATE=1** (exit 1): errors are halved in V0, and S must scale ×3 to ×5 (CFG402's mutation).

## Reading (frozen; graded variants V1, V2, V3−, V3+; both footings)
- **OUTSKIRT-DRIVEN** requires all three:
  - V1 and V2 are both NOISE on both footings.
  - V1 and V2 are both SPECIAL.
  - V0 still reproduces (K1).

  STANDING's Genzel line then becomes: "the residual zC 406690 tension rests on one-sided outermost points, the regime arXiv:2507.10544 flags; no tension at the level these data support."
- **ROBUST:** none of V1, V2, V3−, V3+ is NOISE on either footing. STANDING keeps "one ~2σ outlier (zC 406690)" and adds "robust to outskirt cuts and ±10° inclination".
- **FRAGILE, NOT ATTRIBUTED:** anything else. The README names which variant(s) reach NOISE and whether they are SPECIAL. If only V3± reach NOISE, it reads "inclination-sensitive". If V1/V2 reach NOISE but are not SPECIAL, it reads "point-count-sensitive, not outskirt-specific".

**Statement-change rule:** only the STANDING Genzel line and the reading note may change. No a0(z) value is quoted, no footing pooling, and no "favours".

## Compute and files
Single thread (nice), CPU only, a few minutes per pass, RSS < 1 GB, no downloads. This is allowed under the small-job rule while a large run is live. The script will be `cfg405_robustness.py` (exec'd CFG401 head as in CFG402; vectorising the f profile is allowed only if K1 passes). Outputs: `cfg405.out`, `cfg405_results.json`, `_MUTATE` siblings. README after the run.
