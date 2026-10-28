# SG1_sluggs_imf_gas: the IMF is at its bound; SLUGGS passes only with hot gas beyond the measured X-ray edge

Criteria: `FROZEN_CRITERIA.md` (e93b338fa2, committed alone, before any script or number); no amendment.
Machinery: HO2's committed script, executed read-only, with one edit inside its SLUGGS child that adds the `trunc`
reading and K1. HO2's own readings are unchanged.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen): **ONLY EXTRAPOLATED GAS RESOLVES SLUGGS** (canonical and alt)

| reading (frozen CL2 picture) | class mean | cleared | class |
|---|---|---|---|
| no gas (HO2, Step 0) | +0.152 | 1/4 | FAILS |
| **measured gas, truncated at the X-ray edge (PRIMARY)** | **+0.105** | **2/4** | **FAILS** |
| CFG331 extrapolated gas (HO2's reported reading) | −0.002 | 3/4 | **PASS** |

**Per galaxy (trunc):** M87 (NGC 4486) +0.008, NGC 4365 +0.149, NGC 4374 +0.103, NGC 5846 +0.160.

The footings coincide: above the switch, route E carries no a₀ beyond the floor (as in HO2).

## The IMF lever is at its bound (§1, stated before the run)

**M★/M_JAM** (the JAM analogue, i.e. the largest M★ the measured dynamics allows): NGC 4486 0.95, NGC 4365 0.87,
NGC 4374 0.95, NGC 5846 0.89.

An IMF-heavy M★ capped at M_JAM cannot raise the prediction. **The IMF is not the missing piece.**

## Reading

- **SLUGGS is a hot-gas question.** M87, which has a deep, wide X-ray map, closes on measured gas alone.
- For the other three, the record's measured X-ray fields stop short of the outer GC radii:
  - NGC 4374: 18 kpc against 22 kpc;
  - NGC 5846: 30 kpc against 54 kpc.
- CFG331's extrapolation of the measured gas beyond those edges closes them.

**This is a prediction, not a pass.** In this picture, deeper X-ray data must find hot gas around NGC 4374, NGC 5846 and
NGC 4365 beyond the current fields, with the mass CFG331's extrapolation assigns. If eROSITA or Chandra/XMM outskirt
profiles show the gas truncating instead, SLUGGS fails.

## Checks: 5/5

- **K0 (both footings):** HO2's +0.152 and −0.002 are reproduced.
- **K1 (both footings):** the truncated gas equals the extrapolated gas inside r_meas.
- **K2:** child RSS 0.66 GB.
- **Rerun:** byte-identical.

**MUTATE twin** (trunc gas × 0): it exits 1, but by a crash, not by K1 (disclosed). CFG528's `gas_profile` returns None
at a multiplier of 0, and the SLUGGS child then fails.

**Development runs before any SG1 number (disclosed):**
- `run1_pickle_error.log`: the forked pool needed the read-only namespace registered as a module.
- A KeyError: gas metadata had to be read from `gas_profile`'s own namespace.

Both were code fixes with no rule change.
