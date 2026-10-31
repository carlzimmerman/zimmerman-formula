# RF1_mw_halo_free_baryons: AMENDMENTS (dated; each states whether before or after the numbers it concerns)

**A1, 2026-10-31, after the UNDETERMINED result (fed5cbfee6) and before any graded number at the new row.**

A halo-free bulge mass is now on disk. The README's closing list (item 1) and the frozen criteria (verdict item 2,
9468ee04b2) say what follows: add the row to `HALO_FREE_BULGE`, wire the frozen grade, run. Nothing in the frozen lines,
grids, gas column, shapes or classes changes. Committed text above this file is left as written.

**The row.** Valenti, Zoccali, Gonzalez, Minniti, Alonso-García, Marchetti, Hempel, Renzini, Rejkuba 2016, A&A 587, L6
(arXiv:1510.07425). On disk: `_external_data/rf1_valenti2016/valenti2016.pdf` (sha256 77250ff5…95be1, the arXiv PDF) and its
extracted text `valenti2016.txt` (sha256 e395606d…8ed9f0c74b); both untracked, as the record keeps downloads. The script reads
the value from the text file, not from this note.

- Value: "The Milky Way bulge stellar mass within (|b| < 9.5°, |l| < 10°) is 2.0 ± 0.3 × 10¹⁰ M☉" (§3.2 and abstract).
- What it is: mass in stars and remnants, from VVV red-clump counts scaled to the Zoccali+03 SOFI luminosity function and the
  Zoccali+00 NICMOS main-sequence IMF measured down to 0.15 M☉; Salpeter above 1 M☉ and slope −0.3 below 0.15 M☉ assumed;
  Zoccali+00 initial-to-final mass relation for remnants; 18 % disc decontamination near the red clump.
- Class: **LITERATURE-INPUT, photometric star counts; no dynamics, no halo.** The paper: previous estimates were "all model
  dependent"; theirs is "the first fully empirical estimate".
- Error: ±15 % "including disk contamination, extrapolation of the IMF, mass of the remnants, and stellar population gradients".
- Caveats carried into the ledger: the window is a projected box ~2.8 × 2.7 kpc not limited along the line of sight, so it
  holds bar mass beyond the bulge's dynamical extent (the authors give this as the reason it sits above dynamical values); the
  RF1 bulge *shape* is still McMillan's rescaled, labelled; the IMF above 1 M☉ is assumed, not measured.

**Grade, as frozen (item 2).** At M_bb = 2.0 × 10¹⁰ on the Σ_b (McKee ±2σ, 5 values) × R_d (BH&G16 ±2σ, 7 values) box with
McKee's gas 13.7, background A, PRIMARY V_last: **PASS on halo-free baryons** if any cell passes L1, L2a, L2b, L3; **FAIL on
halo-free baryons** if none does; the LN16 tag (R_d in 2.38–2.90) is stated either way. Every cell of that box is inside both
±2σ ranges by construction. Graded keys: OS1|canonical|PRIMARY, OS1|alt|PRIMARY, N (footings coincide, K6).

**Reported, not graded:** the same box at 1.7 and 2.3 × 10¹⁰ (±1σ), VARIANT V_last, background B.

**New check K8:** the parsed value and error equal the sentence on disk, and the text file's sha256 equals the one above.

**Expectation on record, from the committed LOOKUP at 1.88 and 2.12 × 10¹⁰ (not a prior):** passes only at R_d 1.93 on OS1 alt
and native N; none at R_d ≥ 2.6; OS1 canonical PRIMARY none. So PASS (WIDE PRIORS ONLY, outside LN16) on alt and N, FAIL on
OS1 canonical. If the run differs, the run stands.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed.
Nothing here says the data favour the framework.
