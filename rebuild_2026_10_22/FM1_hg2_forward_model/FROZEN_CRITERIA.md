# FM1_hg2_forward_model: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, continuing the owner's instruction "keep mutating ideas until we get the answer".

**Why.**
- AP1 found that HG2's negative sign survives a common physical aperture.
- At a common aperture, g_obs = 3σ²/r depends **only on σ**. HG2's statistic bins groups in σ, i.e. it **conditions on
  the observed pull itself**. At fixed observed pull, the arm with more counted baryons (BRIGHT) must sit at higher g_bar
  and so *below* any rising reference curve: a negative D.
- HO1(b)'s D_pred, and every predicted D since, computed Δ_pred = log g_pred − ref(g_bar) while binning on the
  *observed* σ. That never applies the same conditioning to the model.

A fair test forward-models the observable: generate model pulls with realistic scatter, derive the model σ, bin on it as
HG2 does, and compare the resulting D distribution with the measured D.

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

## 1. Forward model (frozen)

**Rows:** GA1's PRIMARY rows (own (4/3) R_h apertures, as in HG2/GA1). AP1's 0.5 Mpc aperture rows are a reported
variant.

**Model per group, footing f:**

    log g_mod,i = log g_pred,i(f) + ε_i,      ε_i ~ N(0, s_int)
    σ_mod,i     = √(g_mod,i r_i / 3)                    (HG2's own estimator, inverted)
    Δ_mod,i     = log g_mod,i − log ref(g_bar,i)

- **g_pred** is the base picture (HO1(b)'s `group_pred`).
- **The scatter s_int** is data-driven and frozen: 1.4826 × the median absolute deviation of
  (log g_obs − log g_pred) over all supported groups, per footing. That covers intrinsic scatter, σ errors and
  membership noise together.
  - **Variants:** the FAINT-arm-only scatter, and 0.5× and 1.5× s_int.
- **D_mod** = HG2's `D_stat` on rows whose σ is replaced by σ_mod, so that the binning uses the model σ.
- **Realisations:** 2000, from default_rng(20261028).

## 2. Verdict (frozen, canonical primary)

Let q be the fraction of realisations with D_mod ≤ D_meas, where D_meas = −0.3623 is GA1 PRIMARY's measured D.

| verdict | condition |
|---|---|
| **CONDITIONING EXPLAINS THE SIGN** | 0.025 ≤ q ≤ 0.975, i.e. the measured D is typical of the model observed HG2's way |
| **CONDITIONING PARTLY EXPLAINS** | q < 0.025, but the median D_mod is below 0, i.e. the bias has the right sign but is too small |
| **CONDITIONING DOES NOT EXPLAIN** | otherwise |

**Reported:**
- the median and 95 % range of D_mod per footing and variant;
- the noise-free D_pred, re-binned on noise-free σ_mod (s_int = 0).

## 3. Checks and twin

- **K0.** Step 0 reproduces GA1's PRIMARY D_meas (−0.3623) and D_pred (+0.3059 / +0.2821).
- **K1.** With s_int = 0 and the binning on the **observed** σ (no σ replacement), D_mod equals HO1(b)'s D_pred on
  these rows (+0.3059 / +0.2821) to 1e-9.
- **K2.** s_int > 0 for both footings, and the realisation list is reproducible from the seed.
- **K3.** Peak RSS < 1 GB.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`FM1_MUTATE=1`, separate outputs).** s_int is forced to 0 everywhere, so K2 fails and the run exits 1.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I fm1_hg2_forward_model.py`
