# GX2_infall_corrected_gas: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "freeze and run GX2: regrade the cluster lensing with the infall halo and the
eRASS1 gas masses raised by the matched +0.111 dex offset."

**Why.** SM1 (d743311e4a) found that for the same five clusters, eRASS1's Mgas500 runs a median **0.111 dex** below
X-COP's, while R500 agrees within 0.035 dex. The lensing harness builds every cluster's gas and cold dark energy budget
from eRASS1's Mgas500. GX1's lensing failures for the infall halo were UNDER in MID/OUT (edge r_ta), the direction a
low gas budget gives.

**PRIMARY halo (chosen and disclosed).** GC3's derived infall shape with **GC3's own derived edge**, splashback at
0.364 r_ta, on GS1's measured-gas budget.
- **Its X-COP grade is already known.** It passed in GX1 Stage A (mean −0.035, rms 0.079). It is not re-run here,
  because X-COP uses its own gas.
- The lensing grade with corrected gas has **not** been seen. That is this lane's test.

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

## 1. Run (frozen)

**Harness:** GX1 Stage B (GS1's harness: R4, native, measured slope 2.777), with one added edit. Every lensing
cluster's eRASS1 Mgas500 is multiplied by 10^0.111.

**This correction:**
- is calibrated on 5 X-COP / eRASS1 matches, **none of which is in the lensing sample** (disclosed);
- is applied uniformly;
- changes the gas, the baryons and the fair-share budget consistently.

**Halos graded:**
- **PRIMARY:** infall, edge 0.364 r_ta;
- **V1:** infall, edge r_ta;
- **V2:** Burkert, edge r_ta (GS1 R4) with the corrected gas, to check that the record's pass survives the correction.

**Reported:** the corrections at ±1σ of the five matched offsets (std of the dlog Mgas500 values).

## 2. Verdict (frozen, canonical primary)

| verdict | condition |
|---|---|
| **INFALL HALO + CORRECTED GAS PASSES CLUSTERS** | PRIMARY passes all 15 lensing keys in both h cells (the X-COP pass from GX1 stands) |
| **LENSING STILL FAILS: <keys>** | otherwise |

**Reported:** whether V1 and V2 pass.

## 3. Checks and twin

- **K0.** With no correction and the Burkert halo, the run reproduces GS1 R4 (all 15 keys pass).
- **K1.** The correction factor applied equals 10^0.111 to 1e-12, in one place (asserted).
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`GX2_MUTATE=1`, separate outputs).** The factor is applied twice; K1 must fail and the run must exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gx2_corrected_gas.py`
