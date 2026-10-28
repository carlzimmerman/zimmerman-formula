# TH1_turnaround_basins: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "freeze and run TH1: recompute the basins from the measured velocity-flow
zero crossing (UNGC) and regrade BS1's lines."

**Why.** The candidate field equation (e03863663b) keys cold dark energy condensation on the sign of the matter flow's
expansion, θ < 0 inside turned-around regions. BS1 (979363d820) built SPARC basins from KT2017 **catalogue membership**.
TH1 rebuilds them from the field's own variable: the **measured zero crossing of the radial velocity field** around each
group's main body, exactly as BS1 did for the Local Group.

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

**Scope, disclosed.** UNGC (Karachentsev+13, on disk) covers the Local Volume, D ≲ 11 Mpc. 67 SPARC galaxies have a
UNGC counterpart (match within 0.05°). BS1's 13 changed galaxies are mostly Ursa Major, at about 18 Mpc, **outside**
UNGC. TH1 therefore tests the flow criterion where it can be measured. It does not re-test those 13.

## 1. Flow-defined basins (frozen)

**Groups.** Each distinct UNGC main disturber (MD) of a matched SPARC galaxy is a candidate group centre. For each:

1. **Frame.** The centre is at the MD's position, distance D_c and V_c = its Vlg. For every UNGC galaxy with an
   accurate distance (f_Dist ∈ {TRGB, Cep, RR, HB, SBF, BS, CMD, geom}, CFG548's list):
   - R = the 3-D distance from the centre;
   - V_r = V_g (D − D_c cos θ)/R − V_c (D cos θ − D_c)/R, the Karachentsev–Makarov projection.
2. **Fit.** A straight line V_r = H_loc (R − R0) over 0.2 ≤ R ≤ 3.0 Mpc.
   - **Determinable** iff N ≥ 8 points and H_loc > 0.
   - R0 is the flow's zero crossing (the turnaround surface).
3. **Basin and mass.**
   - The basin is every UNGC galaxy with R < R0, with or without an accurate distance.
   - M_basin = Σ M200,i, the EM1 R1 relation on M_b,i = 1.2 × 0.6 L_K,i (UNGC KLum), as in BS1.

**SPARC galaxy flag.**
- **Halo** iff the galaxy lies inside a determinable flow basin with log M_basin > T, or its own M200 > T (CL2's
  clause).
- **PRIMARY:** T = 12.3 (BS1).
- **Variant:** T = 12.236 (CL3 at L = 3.75).
- Galaxies whose group is not determinable keep BS1's flag (counted).

## 2. Grade

For the 67 matched SPARC galaxies, compare the flow flag with BS1's flag (BS1 `primary_basins`).

**Verdict (frozen):**

| verdict | condition |
|---|---|
| **FLOW BASINS REPRODUCE BS1** | no matched galaxy changes branch. BS1's SPARC lines then stand unchanged, and the field variable agrees with the catalogue |
| **FLOW BASINS CHANGE n GALAXIES** | otherwise. The changed galaxies are listed, with R0, M_basin and both flags. The SPARC regrade is then a frozen follow-up (TH2) and is not run in this lane |

**Reported:**
- R0 and H_loc per determinable group, with a bootstrap error (400 resamples, seed 20261028);
- membership at R0 ± 1σ.

## 3. Checks and twin

- **K0.** The same machinery, centred on the LG barycentre (CFG548 frame, f31 = 2/3), reproduces BS1's R0_data
  (794.7 kpc) to 1 kpc.
- **K1.** Each fit's R0 lies inside its window. A determinable group must have R0 ∈ [0.2, 3] Mpc, otherwise it is
  re-labelled not determinable.
- **K2.** Peak RSS < 1 GB.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`TH1_MUTATE=1`, separate outputs).** V_c's sign is flipped in the projection, and K0 must still pass for
  the LG (V_c = 0 there). A K3 check then fails: K3 requires ≥ 1 determinable non-LG group with H_loc within a factor 3
  of the LG's.

**Run:** `PYTHONHASHSEED=0 python3 -I th1_turnaround_basins.py`
