# CL1_combined_threshold_budget: FROZEN CRITERIA (committed alone, before any CL1 script or number)

**Why.** Three frozen lanes each solved one piece.

- **CF2** (frozen 7881b642f8; partial results seen at write time) is the decoupled switch, where a halo applies if the
  system is a satellite or M > 10^T, independent of c_f. At T = 12.2 and c_f = 4.75, on the canonical footing, lensing,
  groups, SPARC and every dwarf class pass. Only G-OUT-M3 (the cluster-budget line) fails.
- **GS1** (01f6dd977d) is the measured cluster budget: X-COP gas at slope s = 2.777 beyond R500, counted to the
  self-consistent r_ta, with the native fair share. All 15 cluster keys pass at c_f = 4 on both footings. Groups fail.
- **CL1 combines the two:** CF2's switch with GS1's cluster budget, over a small (T, c_f) grid, on X62's **full** line
  set (SPARC, groups, 15 cluster keys, LG dwarfs, KiDS lensing).

**What CL1 is, stated plainly.** T is located by CF2's map of the same lensing and group lines, and the budget slope is
measured. CL1 is therefore a **consistency test of the combined picture**: does any single (T, c_f) pass every line?
**It is not a derivation of T or of c_f.** A pass would define the target a first-principles threshold and concentration
must hit. CF2's higher-T points were not yet seen when this was written; that is disclosed.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. Harness

CF2's generated X62 harness (scalar c_f, decoupled flag M > 10^T), plus **GS1's cluster budget**, applied inside the X43
copy exactly as GS1 does it:

- native normalisation (Ω_c/Ω_b 5.2715, native h and Ω_m) in X30's `prep` and `r_ta_com`;
- gas counted to the self-consistent r_ta, with ρ ∝ r^{−2.777} beyond R500.

Galaxies, groups, lenses and dwarfs use the unchanged paths.

**Grid.** T ∈ {12.2, 12.3, 12.4} × c_f ∈ {4.0, 4.25, 4.5, 4.75}, run on both footings.

## 2. Step 0 (stop rule)

- **S0a.** With the flag set to "always halo" (T = 0), c_f = 4 and the GS1 budget, the cluster cells reproduce GS1's
  committed R4_meas to 0.01 in Z on all 15 keys, on both footings.
- **S0b.** With the GS1 budget off, T = 12.2 and c_f = 4.75, the grade reproduces CF2's committed T 12.2 / c_f 4.75 point.
  Fail lists must match; groups Z and lensing Δχ² must match to 0.01.

## 3. Verdict (frozen)

- **COMBINED PICTURE PASSES (canonical) / (alt) / (both):** at least one grid (T, c_f) passes every line on that footing.
  All passing points are listed.
- **COMBINED PICTURE FAILS:** no grid point passes every line on either footing. The binding lines are named.
- **Reported, and stated separately:** the alt footing's MW ultra-faint class and its SPARC line fail independently of
  T, c_f and the budget in CF1/CF2. An alt failure on only those lines is labelled as such and does not mask a canonical
  pass.

## 4. Checks and twin

- **K1.** The switch property holds at every grid point.
- **K2.** The budget patch is active: the cluster Mfair under GS1 differs from the cut budget for more than 90 % of
  clusters.
- **K3.** Peak RSS < 1 GB, per process.
- **MUTATE (`CL1_MUTATE=1`, separate outputs).**
  - m1: the flag is inverted.
  - m2: the S0a target × 1.01.
  - The twin must fail S0a and K1.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I cl1_combined.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects.
