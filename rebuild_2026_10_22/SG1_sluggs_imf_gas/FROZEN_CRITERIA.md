# SG1_sluggs_imf_gas: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "freeze and run the SLUGGS lane with the IMF-heavy stellar mass variant
bounded by M_JAM."

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

## 1. The IMF lever is already at its bound (stated before any run)

HO2/GR1's SLUGGS M★ is the **JAM analogue**: the M★ that solves 0.5 M★ + M_halo(< r₁₂; M★) = 0.5 M_JAM (GR1 criteria
§, K2). It is the largest stellar mass the measured dynamics allows once the model's halo is included.

An IMF-heavy M★ capped at M_JAM can therefore **only equal or fall below** the graded value. It cannot raise the
prediction.

**The lane reports:**
- each central's M★/M_JAM (HO2: 0.87–0.95);
- GR1's committed Salpeter reading (+0.093, 1/4 cleared, under OS1).

No IMF variant is graded, because none can exceed the JAM analogue.

## 2. The remaining baryon lever: measured hot gas (graded)

**Gas source.** The ellipticals' X-ray gas is on disk via CFG331 / CFG528:
- Lakhchaura+18;
- Fukazawa+06;
- Churazov+08 and Urban+11 for M87.

**Graded under the frozen CL2 picture (HO2's harness, executed read-only):**
- **PRIMARY `trunc`:** the measured gas profile truncated at each source's measured edge. This is data only, with no
  extrapolation.
- **Variant `extrap`:** CFG331's frozen extrapolation. This is HO2's reported reading (−0.002, 3/4).

**Grade:** GR1/HO2's frozen SLUGGS rule. The class is PASS iff the reading "closes" (GR1's `closes`). Otherwise it is
IMPROVES ON X38 (|mean| ≤ ½ |X38 q = 0 mean| and none reversed) or FAILS.

**Verdict (frozen, canonical primary):**

| verdict | condition |
|---|---|
| **MEASURED GAS RESOLVES SLUGGS** | `trunc` PASS |
| **ONLY EXTRAPOLATED GAS RESOLVES SLUGGS** | `trunc` not PASS, `extrap` PASS |
| **GAS DOES NOT RESOLVE SLUGGS** | otherwise |

**Disclosed:** the extrapolated gas lies beyond the measured X-ray fields (CFG331: 18 against 22 kpc for NGC 4374, and
30 against 54 kpc for NGC 5846). That is why `trunc` is primary.

## 3. Checks and twin

- **K0 (Step 0).**
  - HO2's committed SLUGGS CL2 grade (+0.152, 1/4) is reproduced.
  - Its `extrap` reading (−0.002, 3/4) is reproduced, to 1e-6.
- **K1.** The `trunc` gas at r ≤ r_meas equals the `extrap` gas there, to 1e-12.
- **K2.** Peak RSS < 1 GB per process.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`SG1_MUTATE=1`, separate outputs).** The `trunc` reading is fed the gas × 0 on the graded path, while K1
  still compares it with `extrap`, so K1 must fail and the run must exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I sg1_sluggs_imf_gas.py`
