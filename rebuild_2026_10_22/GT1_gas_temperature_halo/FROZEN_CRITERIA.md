# GT1_gas_temperature_halo: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28.

**Why this lane.** After BS1 (979363d820), the canonical picture keeps every calibration line and resolves the Milky
Way. What remains fails wherever **hot gas** is present:
- **HO1(b) / HG2:** X-ray-bright groups show *less* extra pull than X-faint groups at matched σ (D = −0.294
  [−0.511, −0.076]). The CL2 picture predicts +0.23.
- **HO1(a), X-COP:** the cores are under-pulled and the outskirts over-pulled.
- **HO2(a), SLUGGS:** the centrals, all hot-atmosphere ellipticals, are under-predicted by +0.15 dex.

The record already names the missing rule. IB1 (README, part 2) says: "the data want a cluster halo whose **core
follows the gas temperature** (HG) and whose **outskirts follow the baryon mass**. No rule tested so far gives both."
- HG alone (the gas's hydrostatic total mass) fixed IB1's inner and middle cells, but failed G-OUT-M3 (+5).
- The GS1 budget (native fair share of measured gas to r_ta) fixes the outskirts.

GT1 freezes the combination.

**The hypothesis GT.** Where a hot atmosphere fills the potential, cold dark energy settles into the **same isothermal
potential as the gas**. Inside the gas-measured radius, the total pull is set by the gas temperature, not by
baryons + an additive halo. Beyond it, the halo carries the remaining native fair-share budget.

**No new constant.** The posit is that the halo shares the gas's potential where the gas is hot; it is disclosed and has
no action written.

**Standing rules.**
- κ = ½ FITTED.
- Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled; canonical is primary. HG's mass has no a₀, so the footings
  differ only through non-hot systems and units (IB1).
- Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a particle; ΛCDM appears only as the rival.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

## 1. The rule

**Base picture.** The CL2 picture plus BS1's basin switch (S9 shape, L = 4, T = 10^12.3, GS1 budget), unchanged for
every system **without** a hot atmosphere.

**For a system WITH a hot atmosphere** (definitions in §2):

    r ≤ R_g :   M_tot(r) = M_HG(r) = 3 β σ² r³ / [G (r² + r_c²)]        (IB1's HG, σ² = kT/(μ m_p), μ = 0.6)
    r > R_g :   M_tot(r) = M_HG(R_g) + k [M_CL2(r) − M_CL2(R_g)],   k ≥ 0 chosen so that M_tot(r_ta) = M_budget

- **M_CL2:** the CL2/GS1 picture's own total-mass profile for that system.
- **M_budget:** its GS1 total, measured gas plus the native fair share to the self-consistent r_ta.
- **k:** if M_HG(R_g) ≥ M_budget, then k = 0 and the excess is reported. The continuity-offset variant,
  M_tot = M_CL2(r) + [M_HG(R_g) − M_CL2(R_g)], is reported.
- **R_g:** the gas-measured radius, R500 for clusters (primary); 0.7 R500 and r_ta/2 are reported.
- **β, r_c:** each system's own β-model, as IB1 (clusters, X30) and HG2 (groups) use them.

## 2. Which systems are "hot" and where σ comes from (frozen)

**Clusters (15 eRASS1 × KiDS keys):** every eRASS1 cluster is X-ray detected, so all are hot.
- σ from the catalogue kT where KT > 0 (106 clusters).
- For the rest, σ comes from IB1 RF's own fill, log σ = 0.9186 + 0.1393 log Mgas500, the record's regression
  (disclosed as inherited). IB1's tercile fill is reported.

**HG2 groups:**
- **BRIGHT** (eRASS1-matched, 14) are hot. σ = σ_LOS, so σ² stands in for kT/(μ m_p) with β_spec = 1 (disclosed: no
  group kT on disk).
- **FAINT** groups keep the base picture.
- β and r_c are HG2's.

**The 63 graded groups (P4 T3):** no hot-atmosphere flag or kT is on disk, so they keep the base picture. The groups
line is carried unchanged (disclosed).

**SLUGGS centrals:** **NOT A TEST.** No X-ray kT is on disk. Using the stellar σ would make the hydrostatic mass a Jeans
mass of the same kinematics that are graded (circular). They are reported under the base picture, with the reason.

**X-COP (HO1(a)):** **NOT A TEST inside R500.** The graded masses are hydrostatic gas masses, and GT's inner mass *is*
the gas's hydrostatic mass, so agreement there is by construction. It is reported as a construction check (K4), not
graded.

**Everything else (SPARC, dwarfs, the Milky Way, lensing):** no hot atmosphere, so unchanged from BS1 (Step 0).

## 3. Grading (canonical primary; alt reported with its own verdict)

**(A) Cluster lensing, the 15 eRASS1 × KiDS keys, both h cells.** These are lensing data, independent of the hydrostatic
masses. Pass iff |Z| ≤ 2 in every key and cell. This explicitly includes:
- G-IN-Mall, which OS1 failed and IB1 fixed;
- G-OUT-M3, which IB1 failed at +5;
- G-OUT-all and G-OUT-M1, which IB1 failed marginally.

**(B) HG2's statistic.** D_pred is computed with HG2's own machinery under GT (BRIGHT on GT, FAINT on the base).
**PASS** iff D_pred ∈ [−0.511, −0.076]. This is not blind: the measured D is in the record, and the writer expects GT to
predict D ≈ the gas-count shift.

**(C) All other base lines** (SPARC, the 63 groups, the dwarf classes, lensing, the Milky Way): they must reproduce
BS1's committed values (Step 0) and still pass on canonical.

**Verdict (frozen, canonical primary):**

| verdict | condition |
|---|---|
| **GAS-STATE RULE HOLDS** | A, B and C |
| **GAS-STATE RULE FIXES CLUSTERS ONLY** | A and C, not B |
| **GAS-STATE RULE FIXES GROUP SIGN ONLY** | B and C, not A |
| **GAS-STATE RULE FAILS: <lines>** | otherwise |

**Reported:**
- the per-bin pred/meas in the cluster cells, compared with IB1 HG and CL2;
- k per cluster and the number clamped at k = 0;
- the R_g and continuity-offset variants;
- the tercile σ fill;
- X-COP's construction residual;
- SLUGGS under the base picture.

**The open item, stated in advance:** IC 1613 (BS1 S3, −7.62σ) has no hot atmosphere, so GT cannot change it.

## 4. Checks (all must pass) and twin

- **K0 (Step 0).** With GT switched off, the run reproduces BS1's committed canonical grade (every line) and HO1(b)'s
  D_pred (+0.229 / +0.201). With R_g = r_ta and k unused, the inner rule reproduces IB1's HG cluster Z (G-OUT-M3
  +5.02 / +4.36), all to 1e-6.
- **K1.** Every hot system's M_tot(R_g) equals M_HG(R_g) to 1e-9. Every non-hot system's profile equals the base.
- **K2.** For every system with k > 0, M_tot(r_ta) = M_budget to 1e-6.
- **K3.** Peak RSS < 1 GB per process, one thread.
- **K4 (construction, reported).** The X-COP residual inside R500 under GT.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`GT1_MUTATE=1`, separate outputs).** σ² is doubled on K1's analytic side, so K1 must fail and the run must
  exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gt1_gas_temperature_halo.py`
