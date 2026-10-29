# GX1_infall_shape_measured_budget: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "lets work on the failures then.. we have to have answers that work
everywhere".

**Why.** Two record lanes fixed opposite ends of the cluster halo, and were never combined:
- **GC3** (5726142b8a): X43's **self-similar infall shape**,
  ρ ∝ 1/[(1 + x)(1 + x²)^{5/8}] (outer slope −9/4, core from X43's rule). It **fixes the cluster centres**: G-IN-Mall
  −2.37 → −0.90. But it was normalised to the fair share of the baryons **inside R500**, and the gas-rich outskirts
  stayed short (G-OUT-M3 +2.4).
- **GS1** (01f6dd977d): the **measured-gas budget**. X-COP gas slope 2.777 beyond R500, counted to the self-consistent
  r_ta, times the native fair share. All 15 keys pass at c_f = 4 with the **Burkert** shape (R4).

HO1(a) and BC1 show the X-COP shape failure is the cluster halo's shape: cores too light, outskirts too heavy (BC1
7f78af6e40). GX1 combines the derived shape with the measured budget. There is **no new constant**.

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

## 1. The halo (frozen)

For every cluster (and every system above the switch that the graded lines treat as a cluster):

    M_h(<r) = 4π Σ r0² I(min(r, r_ta)/r0),     I(X) = ∫₀^X x² f(x) dx,  f(x) = 1/[(1+x)(1+x²)^{5/8}]   (GC3's I)
    4π Σ r0² I(r_ta/r0) = M_fair = 5.2715 × M_b(< r_ta)                      (GS1's budget)

- **Core:** Σ is the CL2 picture's core (S9 shape, L = 4).
- **r0** is the compact root, saturating at the peak, as in GC3 A1 / X43.
- **Variant:** truncation at splashback, 0.364 r_ta, with the same total M_fair (GC3's edge).

## 2. Grade

**Stage A, X-COP (held out; the failure being repaired).**
- **Harness:** HO1(a)'s frozen rule and machinery (`xcop_cl2`, 35 points, no hydrostatic normalisation), with
  HO1's Burkert profile replaced by the halo above. The baryons are unchanged.
- **PASS** iff |mean Δ| ≤ 0.05 and rms ≤ 0.10. The inner points (x = 0.1, 0.2) and outer points (x = 0.5, 0.7) are
  reported.

**Stage B, the lensing line set (calibration; must not break).**
- **Harness:** GS1's own harness. The R4 budget is kept; the Burkert profile is replaced by the halo above.
- **Graded:** the 15 eRASS1 × KiDS keys in both h cells, plus GS1's full line set.
- **PASS** iff every key has |Z| ≤ 2 on canonical.

Stage B is run as the second part of this lane, under these same criteria.

**Verdict (frozen, canonical primary):**

| verdict | condition |
|---|---|
| **INFALL + MEASURED BUDGET REPAIRS THE CLUSTERS** | A PASS and B PASS |
| **REPAIRS X-COP, BREAKS LENSING: <keys>** | A PASS, B FAIL |
| **KEEPS LENSING, X-COP STILL FAILS** | A FAIL, B PASS (the inner and outer residuals reported) |
| **FAILS BOTH** | otherwise |

## 3. Checks and twin

- **K0 (Stage A).** With the Burkert profile restored, the run reproduces HO1(a) (mean −0.002, rms 0.126).
- **K0 (Stage B).** With the Burkert profile, the run reproduces GS1's R4 (all 15 keys pass at c_f = 4).
- **K1.** For every cluster, 4π Σ r0² I(r_ta/r0) = M_fair to 1e-8 (unsaturated), or saturation is counted.
- **K2.** Peak RSS < 1 GB per process.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`GX1_MUTATE=1`, separate outputs).** The outer slope is set to −3 (q = 3 in f) on the graded path, while K3
  checks that q = 2.25 was used, so K3 fails and the run exits 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gx1_stage_a.py` (and `gx1_stage_b.py`).
