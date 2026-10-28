# FD1_field_dwarf_audit: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "park HG2's sign as an open underpowered tension and freeze a lane on IC
1613, the law's worst field-dwarf over-prediction."

**Status of HG2 (parked).** HG2's negative sign survives every data-only audit:
- DS1 fcc40606a6;
- GA1 133f61510d;
- DY1 6a9bd71696.

It is parked as an **open, underpowered tension**: 6–11 bright groups, power ≤ 0.45.

**Why IC 1613.** Under the law on baryons (HO3, the CL2 picture), IC 1613 sits at E = −0.535 dex, Z −6.75: the law
over-predicts its pull by 3.4×. Under BS1 it takes a halo and sits at Z −7.62.

The record already carries two data flags (disclosed; seen before freezing):
- `hunt_2026/f14_isolated_dwarf_msigma_law.py` lists IC 1613, WLM and NGC 6822 as **rotators**: "gas discs with
  v_rot ≳ σ; stellar σ alone under-counts KE".
- The on-disk UNGC (Karachentsev+13) gives IC 1613 a log L_K of 8.07 and a log M_HI of 7.77, with rotation amplitude
  vAmp 10 km/s. X1 uses log M★ 8.28 and counts no gas.

**To avoid cherry-picking, the audit is applied to all 13 LG field dwarfs (X1's class), not to IC 1613 alone.**

**Standing rules.**
- κ = ½ FITTED.
- Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled; canonical is primary.
- Cold dark energy is not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

## 1. Model and audit (frozen)

**Law prediction (the record's convention, X1 / HO3):**
- g_N = G (M_b/2) / r₁₂², with r₁₂ = (4/3) r_h;
- g_pred = ν(g_N/a₀) g_N, with ν(y) = ½ + √(¼ + 1/y);
- g_obs = 3σ² / r₁₂;
- E = log g_obs − log g_pred, and Z = E/s, where s is X1's per-system sdMC for the iso-AQUAL column.

**Audit components.** Each takes its values from the UNGC row matched by name. Where a UNGC value is missing, the X1
value is kept and that is disclosed per object.
- **(M) Stellar mass from K:** M★ = Υ_K L_K with Υ_K = 0.6 (the record's convention, as in BS1/HG1). This replaces X1's
  M★.
- **(G) Gas counted:** M_b = M★ + 1.33 M_HI (helium factor), with the gas inside r₁₂ taken as half of it, the same
  half-mass convention as the stars. This is disclosed: HI discs are more extended than the stars, so this over-counts
  inner gas and is conservative for the law.
- **(K) Rotation in the kinetic term:** g_obs = (3σ² + v_rot²) / r₁₂, with v_rot = UNGC vAmp (km/s). Galaxies without
  vAmp keep v_rot = 0.

**PRIMARY = M + G + K.** The variants M only, G only, K only, M+G and Υ_K 0.5 / 0.8 are reported.

## 2. Grade (HO3's frozen rules on the 13 field dwarfs; law branch)

- **S1:** the count with |Z| ≥ 2 (binomial p ≥ 0.01).
- **S2:** median |Z| below the null 99th percentile (HO3's value, 1.24).
- **S3:** the worst object, p ≥ 0.01.

The objects IC 1613, Leo T and Phoenix are reported. Under BS1, Leo T and Phoenix carry halos; their law-branch E is
reported for comparison.

**Verdict (frozen, canonical primary):**

| verdict | condition |
|---|---|
| **IC 1613 RESOLVED BY DATA** | IC 1613 has \|Z\| < 2 under PRIMARY |
| **IC 1613 REDUCED** | IC 1613's \|Z\| falls by at least half (from 6.75), but stays ≥ 2 |
| **IC 1613 STANDS** | otherwise |
| **FIELD HOLDS (law)** | reported alongside: S1, S2 and S3 all pass |

The BS1 halo branch is **not regraded** here, because it would need X51's halo machinery (disclosed). The verdict
concerns the law's prediction, as the owner asked.

## 3. Checks and twin

- **K0 (Step 0).** With no audit, the recomputed E reproduces HO3's law-branch E for all 13 field dwarfs to 0.02 dex
  (HO3 used X51's executed copy; small convention differences are stated). IC 1613's E must come out at −0.535 ± 0.02.
- **K1.** All 13 names match a UNGC row, or the misses are listed and their X1 values kept.
- **K2.** Peak RSS < 1 GB.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`FD1_MUTATE=1`, separate outputs).** The rotation term's sign is flipped (3σ² − v_rot²) on the K1 path, and
  K0's IC 1613 target is compared against the mutated no-audit E × 1.1, so K0 must fail and the run must exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 -I fd1_field_dwarf_audit.py`
