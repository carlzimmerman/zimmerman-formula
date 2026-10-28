# AP1_hg2_common_aperture: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "freeze and run the HG2 common-aperture regrade (same physical aperture for
bright and faint groups) to test whether the negative sign is estimator geometry."

**Why.** HG2's negative D survives the gas audit (GA1 133f61510d) and the σ audit (DY1 6a9bd71696). The literature
check (2c6b17d683) flagged the one un-audited piece, the aperture:
- HG2 evaluates g_obs = 3σ²/r and g_bar at each group's own r = (4/3) R_h, the projected half-number radius of its
  galaxies;
- g_bar ∝ 1/r² falls faster than g_obs ∝ 1/r, so a systematic R_h difference between the arms can create a D sign.

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.
- **Inherited and disclosed:** HG1's group distances use d = HRV/67.70. They are kept unchanged so that Step 0
  reproduces HG2.

## 1. Common aperture (frozen)

**Base rows:** GA1's PRIMARY rows (duplicates resolved, Lovisari-audited BRIGHT gas).

For every group, at a **fixed physical radius r_ap**:
- **Stars:** M★(<r_ap) = Υ_K Σ L_K,i over the members with projected separation R_i < r_ap from HG1's light-weighted
  centroid, with Υ_K = 0.6 (HG1's). This is a projected (cylinder) count, the standard aperture estimate (disclosed).
- **Gas:**
  - BRIGHT groups: M_gas(<r_ap) = Mgas500 × the β-model fraction(r_ap, R500), with GA1's audited Mgas500 and R500.
  - FAINT groups: zero gas (HG1's convention).
- **Baryonic acceleration:** g_bar = G (M★(<r_ap) + M_gas(<r_ap)) / r_ap².
- **Observed acceleration:** g_obs = 3σ² / r_ap, with σ = KT2017's catalogue σ (DY1 found it sound).

**Apertures:**
- **PRIMARY:** r_ap = 0.5 Mpc.
- **Variants:** 0.3 and 0.8 Mpc, plus HG2's original rows at the common aperture.

**Rows** whose member light inside r_ap is zero are dropped (count reported).

## 2. Regrade

On the aperture rows:
- **Measured:** D_meas,ap and its 95 % interval from HG2's statistic, power and bootstrap, with GA1 A1's order.
- **Predicted:** D_pred,ap from the base picture (HO1(b)'s `group_pred`, evaluated at r = r_ap with the aperture
  g_bar) and from all-law.

**Verdict (frozen, canonical primary):**

| verdict | condition |
|---|---|
| **GEOMETRY EXPLAINS THE SIGN** | D_pred,ap (base) lies inside D_meas,ap's 95 % interval |
| **SIGN SURVIVES A COMMON APERTURE** | D_meas,ap's 95 % upper end is < 0 **and** D_pred,ap lies above it |
| **APERTURE MOVES THE SIGN** | otherwise (e.g. D_meas,ap's interval straddles 0 while D_pred stays outside) |
| **UNDERPOWERED** | overrides the above when fewer than 6 BRIGHT groups share σ bins |

**Reported:**
- the median R_h of each arm (the geometric lever);
- the variants;
- the power.

## 3. Checks and twin

- **K0 (Step 0).** With the aperture switched off (each group's own (4/3) R_h and HG1's baryons), the run reproduces
  GA1's PRIMARY D_meas (−0.3623) and D_pred (+0.3059 / +0.2821).
- **K1.** For every row, the aperture stellar mass at r_ap = 10 Mpc (effectively all members) equals Υ_K Σ L_K over all
  members to 1e-9.
- **K2.** Peak RSS < 1 GB.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`AP1_MUTATE=1`, separate outputs).** Member light is counted *outside* r_ap instead of inside, so K1 must
  fail and the run must exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ap1_hg2_common_aperture.py`
