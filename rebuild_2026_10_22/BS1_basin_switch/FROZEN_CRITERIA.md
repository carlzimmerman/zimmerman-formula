# BS1_basin_switch: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-27.

**Why this lane.** The frozen CL2 picture (b57ed8751f) passes every canonical calibration line, but its held-out tests
fail (HO1 91cc5c3bd4, HO2 a3bb1e781f, HO3 1cf7d31d67). The sharpest failure is a contradiction **in mass**:
- The Milky Way needs a cold dark energy halo, which under a mass switch needs T < 10^11.9 (HO2).
- KiDS isolated lenses of the same M200 must follow the law, which needs T > 10^12.15 (CF2).

No switch keyed on a system's own mass can satisfy both.

**The geometric hypothesis.** Evaluate the same switch on the **gravitational basin** a system belongs to, not on the
system alone. The basin is the set of galaxies bound inside one zero-velocity (turnaround) surface.
- The Milky Way shares the Local Group basin with M31.
- A KiDS isolated lens is, by its selection, alone in its basin.
- A satellite is inside its host's basin. X62's satellite clause becomes a special case, not a separate posit.

**No new constant.** T, L, the c_f(M) shape, the cluster budget and every scorer are CL2's, frozen. The basin is a
**posit** (nonlocal, no action written), disclosed as such.

**Standing rules.**
- κ = ½ FITTED.
- Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled; canonical is primary.
- Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a particle; ΛCDM appears only as the rival.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

## 1. The rule

    route E (Newtonian baryons + CL2's route-E halo at the system's OWN M200)   if  M_basin > 10^T
    law (ν(g_N/a₀) g_N on baryons, no halo)                                    otherwise

The basin mass and the basin membership are defined as follows.

- **Basin mass.** M_basin = Σ_i M200,i over the basin's members, with each M200,i from EM1 A_c2b_refit R1 on the
  member's baryons:
  - log M200 = 11.18 + 0.90 (log M_b − 10), the same relation CL2's switch uses;
  - M_b = M★ (1 + f_cold), with F2's cold-gas relation where the record has it, else M_b = 1.2 M★ (the record's
    star factor).
  - The sum over members, not the relation applied to the summed baryons, is primary. The summed-baryon variant is
    reported.
- **Halo of each system.** A switched system carries the halo of its own M200 and its own c_f(M200). The basin only
  decides the branch; it adds no mass.

**Basin membership (frozen, data only):**
- **(a) Local Group.**
  - **Barycentre and projected V_r:** CFG548's frame (UNGC, Karachentsev et al. 2013, on disk). This uses the
    barycentre at f31 = 2/3 and V_r = Vlg (D − D_c cos θ)/R. These are geometry only; no ΛCDM model enters.
  - **R0_data:** the zero crossing of a straight-line least-squares fit of V_r on R over 0.6 ≤ R ≤ 2.5 Mpc, on
    CFG548's frozen selection. It uses no dynamical model, so it is NOT CFG548's model-based 830 kpc.
  - **Membership:** an LG system is a member iff R < R0_data.
  - **Reported:** R0_data with a bootstrap error (400 resamples, seed 20261027); membership at R0_data ± 1σ.
  - **LG members' masses:** MW and M31 baryons are taken from the record values CFG522 uses (read from its JSON).
    M33 and the LMC are included as members.
- **(b) Outside the LG (SPARC).** Kourkchi & Tully 2017 groups (J/ApJ/843/16, on disk: `kt2017_galaxies.tsv`,
  `kt2017_groups_full.tsv`).
  - **Matching:** each SPARC galaxy is matched to its KT2017 group with the record's matcher
    (`match_kt2017_host`: 0.05°, 350 km/s).
  - **Member masses:** M★,i = Υ_K L_K,i, from member Ks magnitudes at the group distance. Υ_K = 0.6 is primary;
    0.5 and 0.8 are reported.
  - **Unmatched or Nm = 1:** the basin is the galaxy alone, so the SPARC galaxy keeps its CL2 flag.
  - **Disclosed:**
    - KT2017's grouping uses its own luminosity-based radii (a borrowed algorithm). Only its membership is used; its
      group masses (logMK, logMd) are NOT used.
    - Members fainter than the Ks = 11.75 limit are missed. That makes M_basin a lower bound.
- **(c) KiDS isolated lenses (B21).** No neighbour above 10 % of the lens stellar mass lies within 3 Mpc, so the
  basin is the lens alone. The lensing line is unchanged by construction (disclosed, not regraded per lens).
- **(d) Groups (63) and clusters (15 keys).** Each graded system is its own basin's central. Its catalogue mass already
  is the basin, so these lines are unchanged by construction (disclosed). HO1's hot-gas sign failure is therefore NOT
  addressed by BS1 (stated in advance).
- **(e) SLUGGS centrals.** Already route E under CL2, so unchanged; HO2(a)'s failure stands (stated in advance).
- **(f) Satellites.** Every satellite lies inside its host's basin, and the MW and M31 basin is the LG. The satellite
  flag is therefore recovered iff the LG passes the switch (reported). If the LG does NOT pass, the satellites switch
  to the law: this is BS1's own consequence and is graded, not patched.

## 2. Grading

**(A) Calibration lines re-graded where flags change** (canonical primary, alt reported):
- SPARC (bg A and B), with switched galaxies on CL2's route E (X43 copy, S9, L = 4);
- the five LG dwarf classes.

Every other CL2 line is carried, and Step 0 must reproduce it exactly.

**CALIBRATION KEPT** iff every CL2 line still passes on canonical.

**(B) Milky Way (held out):** HO2(b)'s frozen rule and X5 box, GD2 lines L1, L2a and L2b, with the branch decided by
the LG basin. **MW FIXED** iff at least one box cell passes L1 + L2a + L2b on canonical, and the McMillan point is
reported.

**(C) LG field dwarfs one by one (held out):** HO3's frozen rules S1, S2 and S3 on the 13 field dwarfs, with each
branch from (a). Leo T and Phoenix are flagged per HO3. **FIELD HOLDS** iff S1, S2 and S3 all pass on canonical.

**Satellites:** HO3's satellite grade is re-run only if their flag changes. It is reported either way.

## 3. Verdict (frozen; canonical primary, alt reported with its own)

| verdict | condition |
|---|---|
| **BASIN SWITCH HOLDS** | A and B and C |
| **BASIN SWITCH RESOLVES THE MW CONTRADICTION** | A and B, not C (C's failures listed) |
| **BASIN SWITCH FAILS: <lines>** | otherwise |

Context, stated in advance: in HO3, IC 1613 already sits 6.8σ below the law, so adding a halo can only move it further.

**Reported:**
- the CL3 one-number variant (L = 3.75, T = 12.236);
- the Υ_K and summed-baryon variants;
- R0_data ± 1σ membership;
- the list of SPARC galaxies whose flag changes, with their M_basin.

## 4. Checks (all must pass) and twin

- **K0 (Step 0).**
  - With the basin set to each system alone, BS1 reproduces CL2's committed grade (all lines, both footings).
  - It reproduces HO2's MW result (INFEASIBLE, McMillan K_z z +12.0) and HO3's 13 field residuals, all to 1e-6.
- **K1.** Every system's branch equals its basin flag. Violations are counted.
- **K2.** R0_data is reproducible from the committed selection and seed; the KT2017 match count is stated and
  reproducible.
- **K3.** Peak RSS < 1 GB per process, one thread.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`BS1_MUTATE=1`, separate outputs).** The basin flags are inverted, so K1 must fail and the run must exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I bs1_basin_switch.py`

**Held out, disclosed:**
- The writer knows HO2's numbers: the MW is feasible with a CL2 halo (HO2's MUTATE twin, wide priors only).
- The writer knows HO3's field residuals.
- The rule was fixed from the geometry, not tuned on them. A reader should weight B and C accordingly.
