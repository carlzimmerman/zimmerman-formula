# EXR1R (BLIND RE-GRADE OF EXR1, WIDE-LENS X-RAY CUSP): RESULT

**Blind re-grade; does not relabel EXR1.** 2026-11-12. κ = ½ FITTED. Canonical / alt, never pooled. No outcome here
favours the framework.

**Frozen word: NOT EVALUABLE / NOT EVALUABLE**, as in EXR1: check K8 fails (null mean +1.614 against a limit of
1.328, units 10⁻¹⁵ erg s⁻¹ cm⁻²). **Amendment A1 reading: EXCLUDED / EXCLUDED; reading R: EXCLUDED / EXCLUDED**, no
bracket moves either, as in EXR1. **Part C:** frozen NOT EVALUABLE; A1 reading WIDE LENSES ARE BRIGHTER IN X-RAYS,
as in EXR1. **One caveat EXR1 does not have:** K6, which I could only run after unblinding because it needs ESZ1's
outputs, misses its 0.1 % tolerance by 0.036 percentage points. ESZ1's stored mass-weighted gas temperature is 0.136 %
above my converged integral (canonical). My solver run on ESZ1's own radial grid reproduces it to 6e-6. Read strictly,
my protocol makes the A1 and R readings and the A1 Part C reading NOT EVALUABLE / NOT EVALUABLE. Read on ESZ1's grid,
they stand as above. The difference is quadrature in the reference value, not physics.

Commits (local): protocol `fd3e928e0f` (alone, before any script); script and blind outputs `aac182870d` (before
opening any EXR1 file); this result with the K6 script.

## Comparison with EXR1 (units 10⁻¹⁵ erg s⁻¹ cm⁻², catalogue-equivalent 0.2–2.3 keV)

| | EXR1R (mine) | EXR1 | Difference and traced cause |
|---|---|---|---|
| Lenses tested | 263 of 316 | 263 of 316 | same 263 identifiers; C, B, T identical |
| Measured stack, frozen | +5.801 ± 1.771 | +5.801 ± 1.771 | identical; σ = null rms |
| Measured stack, A1 | +4.187 ± 0.853 | +4.187 ± 0.852 | σ +0.03 %: bootstrap SD with ddof 1 (mine) or 0 |
| Least prediction pred_min | 141.84 / 121.45 | 141.67 / 121.32 | +0.12 / +0.11 %: absorption (see below) |
| Margin A1, (pred − meas)/σ | 161.5 / 137.5 | 161.3 / 137.4 | from the two rows above |
| pred / (meas + 2σ), A1 | 24.1 / 20.6 | 24.0 / 20.6 | same |
| Z = 0, A1 | 78.00 / 67.30 (13.2 / 11.4 ×) | 77.98 / 67.28 | absorption |
| r_in = 1 kpc; Z = 1; z_s ≈ 2; b★ = 0 | 602.6, 429.7, 377.3, 190.3 | 602.3, 429.4, 377.0, 190.0 | absorption |
| f_M at 2σ, A1 | 0.204 / 0.220 | 0.20 / 0.22 | same |
| f_T (frozen threshold 9.34) | kT × 0.164 / 0.171 | × 0.158 / 0.158 | EXR1 grid of 41 factors, step ×1.12 |
| Part C, wide − control | +3.107 [+1.210, +5.019] | same | identical pairs and interval |

**Per lens.** Gas masses agree to a median 7e-5 (largest 0.4 %); n_e and kT at R_E to the quoted digits. The least
prediction differs by a median +0.05 %; of the 242 lenses neither run clips or zeroes, 98 % lie within −0.1 % and
+1.7 %, the largest +2.9 % (lenses at z_l ≈ 0.37). EXR1 multiplies each ARF bin by the absorption at the bin's mid-energy; I absorb each photon on a fine
grid (Δ ln E = 2.7e-4) before binning. Redone with mid-bin absorption, my six largest differences fall to ≤ 0.2 %.
Mine is the finer integral; the stack moves by 0.1 %.

**Checks.** K1: mine −0.38 % / +1.10 %, EXR1 −1.41 % / +2.11 %. EXR1 interpolates E·f linearly between AtomDB's
continuum nodes, which under-integrates a concave product by 1.1 %; I integrate E times the linearly interpolated f.
It touches only K1 and the cooling time (EXR1's 0.7 % longer). The band fluxes use the same convention in both. K2:
1.034 / 1.013 / 1.008 of the catalogue ratios, identical. K3: 4,933 of 4,933, median ratio 1.00075. K4: 0.982 / 1.034
/ 2.51, identical; my own known answer KA1: catalogue Lbol500/L500 over my APEC ratio, median 1.003. K5: 1.7e-5 (my
shell integrator, three shells). K7: 60.8 σ, and 60 of 60 in my own seeded draw; 58 of its cones were fetched live.
K8: identical null stacks. K6: above. My further known answers: pure-hydrogen free-free at 10⁸ K implies a mean Gaunt
factor 1.155 (expected 1.1–1.5); MM83 σ(1 keV) = 2.42e-22 cm²; projection point mass 8e-11, SIS as truncation predicts.

**Twins (mine, separate outputs), all exit 1.** `inject` ALLOWED / ALLOWED. `a1inject`: A1 ALLOWED / ALLOWED. `newton`:
pred_min 348.6 (EXR1 348.3). `shift`: K7 fails on recovery, 3 of 60 (EXR1 4 of 60; different draws), stack 7.1 σ in
both runs.

**Parts L and D.** A Main source within 30″ of 16 lenses, chance rate 1.9 %: identical. eRASS1's own bound below the
least prediction for 127 / 112 lenses (EXR1 127 / 111); an empty aperture would do it for 142 / 130 (EXR1 142 / 129).
Each difference is one alt-footing lens whose two predictions straddle the bound (L005272, 1.6 % apart; L005495,
0.15 % apart); the cause is the absorption treatment. Part D medians agree: gas mass 3.15 / 2.73 × 10¹² M☉, kT(R_E) 0.481 keV, n_e(R_E)
0.198 / 0.176 cm⁻³, L(r ≥ R_E) 1.57 / 1.28 × 10⁴⁴ and L(r ≥ 1 kpc) 1.97 / 1.61 × 10⁴⁵ erg/s, cooling time
43.6 / 48.5 Myr (Z 0.1) and 26.1 / 29.2 Myr (Z 0.3), stack 5.44 × 10⁴² erg/s, classes 3.29 / 2.77 / 2.41. Median
pred_i: mine 40.9 / 32.0 over all tested lenses, EXR1 46.2 / 38.9 over lenses that need gas (definition only).

**Live check.** 20 cached upper-limit records (seed 20261112) re-queried in one POST: 20 of 20 identical, field by
field. Positions, N_HI and cones were parsed from the raw cache by my own code, not EXR1's tables.

## Ambiguities that could move a word

1. **K6 against a discretised reference** (above). This is the only one that moves a word on the numbers I have:
   EXCLUDED to NOT EVALUABLE for A1 and R, Part C's A1 reading to NOT EVALUABLE. It does not touch the frozen word.
2. **What "kT" in K6 means.** EXR1 and I read it as ESZ1's stored mass-weighted median. Read as kT at R_E, it misses
   ESZ1's value by about 18 % and K6 fails outright, with the same consequence.
3. **K8 under A1 is half automatic.** A lens's 8 leave-one-out nulls sum to zero when all 8 positions are valid, so
   the null mean is 0.000 by construction (every tested lens has ≥ 6 valid). Only the scatter half tests anything:
   largest |null| 1.36 against 3.5σ = 2.98.
4. **K8 scatter half under R.** I measure each null from the null mean (largest 1.19). Measured from zero it still
   passes, but only by 2 %: 2.80 against 2.87. A slightly smaller σ would make R NOT EVALUABLE on that reading.
5. Moves no word: selection, clipping, ddof, the bootstrap generator, channel edges, N_H source, shifted-position
   geometry (cache matched within 1″ at every position), absorption treatment and the K1 convention.

## What it means

The independent build reproduces EXR1's physics and measurement: the hydrostatic r⁻² gas law S would need around the
wide lenses would put about 142 / 121 × 10⁻¹⁵ into eRASS1's apertures at its least, and the stack holds 4–6. As EXR1
says, that rests on a post hoc reading because a frozen check failed. This re-grade adds one more condition: whether
K6 passes depends on how its 0.1 % is applied to ESZ1's own discretised temperature. Not tested here, as in EXR1: gas
below about 0.08 keV, multiphase or clumped gas, other profiles. No part of a₀ or κ is tested.

Outputs: `exr1r.out`, `exr1r_results.json`, `exr1r_per_lens.csv`, twins `exr1r_MUTATE_*`, `exr1r_live_check.json`,
`exr1r_fetch_manifest.json` (live requests: URL, time, sha256; raw files outside git), `exr1r_k6_posthoc.{py,out,json}`.
Seen before my numbers: listed in `PROTOCOL.md`; nothing further.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
