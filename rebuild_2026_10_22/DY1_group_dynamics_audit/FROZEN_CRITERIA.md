# DY1_group_dynamics_audit: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "freeze and run a data-only audit of the bright and faint groups' dynamical
side (sigma, membership, the 3 sigma^2/r estimator) and regrade HG2's sign."

**Why.**
- GA1 (133f61510d) showed that HG2's negative D is not a gas over-count. With audited gas, D_meas moved to −0.362 and
  the base D_pred to +0.306.
- Four of the 12 bright groups have galaxy σ inconsistent with their gas kT.
- HG2's g_obs = 3σ²/r uses KT2017's catalogue `sigmaV`, which for small groups may not be a direct dispersion.
- **Data-only:** KT2017's galaxy table (on disk) gives each member's own velocity, so σ can be recomputed. No model
  enters.

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

## 1. Audit rules (frozen)

**Base:** GA1's PRIMARY rows: duplicates resolved, Lovisari-audited BRIGHT gas.

**(a) Measured σ (PRIMARY).**
- For each group, σ_aud is the **gapper** estimator (Beers, Flynn & Gebhardt 1990) of its KT2017 members' HRV, after
  iterative 3σ clipping about the median.
- Members are galaxies with PGC1 equal to the group's PGC1 and a finite HRV.
- No (1 + z) correction is applied; z < 0.02 throughout (disclosed).

**(b) Membership floor.** Groups with fewer than 5 velocity members after clipping are dropped from both arms (HG1's own
Nm ≥ 5).

**(c) Estimator.** g_obs = 3 σ_aud² / r at HG1's r = (4/3) R_h, unchanged. The groups are binned in σ_aud for D_stat.

**Variants (reported with the same classes, not promoted):**
- V-10: Nm ≥ 10 velocity members;
- V-kT: PRIMARY minus GA1's four kT–σ MISMATCHED groups, re-tested with σ_aud;
- V-cat: GA1 PRIMARY with the catalogue σ (this is GA1's PRIMARY run, reproduced).

**Reported per group:**
- σ_cat, σ_aud and their ratio;
- the number of members before and after clipping;
- for BRIGHT groups, β_spec recomputed with σ_aud.

## 2. Regrade

On the audited rows:
- **Measured:** D_meas,aud with its 95 % interval (HG2's power, then bootstrap, from one generator; GA1 A1's order).
- **Predicted:** D_pred,aud under the base picture (HO1(b)'s `group_pred`) and under all-law.

**Verdict (frozen, canonical primary):**

| verdict | condition |
|---|---|
| **DYNAMICS AUDIT RECONCILES THE SIGN** | D_pred,aud (base) lies inside D_meas,aud's 95 % interval |
| **DYNAMICS AUDIT MOVES THE SIGN BUT DOES NOT RECONCILE** | not reconciled, but the gap is at least 30 % smaller than GA1's 0.668 (canonical) / 0.644 (alt) |
| **DYNAMICS AUDIT DOES NOT HELP** | otherwise |
| **UNDERPOWERED** | overrides any class above when fewer than 6 BRIGHT groups share σ bins |

**Reported:** HG2's power on the audited sample.

## 3. Checks (all must pass) and twin

- **K0 (Step 0).** With catalogue σ, the run reproduces GA1's PRIMARY measured D (−0.3623) and D_pred (+0.3059 /
  +0.2821), to 1e-9.
- **K1.** The gapper estimator reproduces the Gaussian σ of a synthetic sample (N = 2000, σ = 300 km/s, seed 20261028)
  to within 3 %.
- **K2.** Every audited row's g_obs equals 3 σ_aud²/r to 1e-12.
- **K3.** Peak RSS < 1 GB, one thread.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`DY1_MUTATE=1`, separate outputs).** σ_aud is multiplied by 1.5 in the row, but K2 still checks the
  unmutated σ_aud, so K2 must fail and the run must exit 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I dy1_group_dynamics_audit.py`
