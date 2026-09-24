# O02 — HeCS low-z lane of the G236/G237 virial-T a0(z) test: z-invariance of log T_vir on 58 real clusters

*Lane: O02. Repo: zimmerman-formula. Date: 2026-09-23. Data: HeCS (Rines+2013, ApJ 767, 15), committed under `deepseek_push/G203_data/` (table1.dat = 58 clusters with z and σ_p; hecs2013_table4.tsv = paper Table 4 radii/masses). Sibling lanes: G236 (eRASS:3 pre-registration; E1 sharp null Δlog10 T = 0.000 vs M-RISE +0.134 dex @ z=0.5) and G237 (Case A identity Δlog10 T = [a0(z2)/a0(z1)]^{1/2} EXACT = 0.0000 vs M-RISE +0.0996 dex @ 0.1→0.5). This lane runs the SAME test at low z with kinematic data available today; no WG products involved. Reproducible: `python3 deepseek_push/O02_hecs_ztest.py > deepseek_push/O02_hecs_ztest.out`. No git commit (subagent lane).*

---

## 0. PRE-REGISTRATION (written before the verdict was read; also in O02_results.json)

**The identity under test (G237 L5 Case A, fixed baryonic mass).** T_X(z2)/T_X(z1)|_{M_b} = [a0(z2)/a0(z1)]^{1/2} with a0(z)/a0(0) = 1 − 3e−5 z (S3-05, z ≤ 3) ⇒ framework predicts **Δlog10 T = 0.0000 (±1e-5)** over any HeCS z-gap. All structure factors (c0, q, u, β, cap) cancel at fixed mass. Rival M-RISE (Ciocan MUSE-DARK III, 1.59e-10 m/s² per unit z = 1.6986 a0 per unit z): Δlog10 T = 0.5·log10[(1+1.6986 z_hi)/(1+1.6986 z_lo)] — +0.0996 dex at z 0.1→0.5, and only **+0.024 dex over the actual HeCS arm gap** (this scaling is the honest rival prediction at low z; the +0.1 dex figure of speech is not what the rival predicts over Δz ≈ 0.084).

**Primary estimator & SE.** ANCOVA: log10 T ~ log10 M200 + z-flag, pooled on the two arms after truncating both to the joint M200 overlap window (mass-matching guard). SE = **jackknife-over-cluster**: delete one cluster from the pooled in-overlap sample, *re-derive the overlap window on every draw*, refit. Bootstrap-over-cluster (4000 reps, within-arm resampling, overlap re-derived per rep) as cross-check; per-cluster σ_p measurement errors propagated separately (adds ~0.021 dex to the Δ SE, same order as the jackknife).

**Kill rules (registered before reading the result):**
- **K1 (framework falsifier):** |Δlog10 T_meas| > 3·SE_jk from the framework's 0.000 ⇒ the framework's virial-T z-invariance is **violated at low z on real clusters** — a real-data kill, reported honestly if it fires.
- **K2 (M-RISE exclusion):** M-RISE is excluded at low z only if Δ is < 2 SE from 0.000 **AND** > 3 SE from the M-RISE prediction scaled to the arm median z's.
- **K3 (adjudication guard, pre-registered):** the HeCS sample is **LX flux-limited** (BCS/eBCS/REF). At fixed flux, higher z requires higher LX at fixed mass ⇒ over-bright → over-hot → over-dispersed systems are preferentially selected at high z — a *positive* bias on Δlog10 T at fixed mass. A positive Δ that (a) overshoots the M-RISE low-z prediction and (b) shows mass-dependent structure (selection acts raggedly in mass) is the **selection signature, not a growth law**. Such an outcome = kill-CANDIDATE with the confounder flagged, verdict **NOT adjudicative**; the WG high-z leg (X-ray/SZ masses + temperatures) decides.

---

## 1. DATA — what is used, and the σ_v identification

| File | Content | Use |
|---|---|---|
| `table1.dat` (58 rows, pipe-separated CDS deposit) | Name \| RA \| Dec \| z \| LX \| Cat \| **σ_p \| +err \| −err \| N_m** (byte-by-byte ReadMe: σ_p = projected velocity dispersion, km/s) | z, σ_v = σ_p, member counts |
| `hecs2013_table4.tsv` (58 rows + header; paper Table 4) | r500Mpc, r200Mpc, r56Mpc, rmaxMpc, M200e14, M200err, Mvir, M56, Mmax/M200 | M200 (matching variable), r500 (M500 check) |

- **σ_v identification:** table1's `sig` column *is* σ_p (projected LOS velocity dispersion), per the VizieR byte-by-byte description (`sig [404/1261] km/s, E_sig +, e_sig −, Nm [61/461]`). Sample ranges reproduce the published HeCS values (e.g., A267 972 km/s, A1689 1197, A1835 1151). All 58 clusters carry σ_p.
- **Temperature proxy:** T_vir = (μ m_p/k_B) σ² = **72.7 K/(km/s)² at μ = 0.6** (≈ σ₁₀₀₀² · 73 MK). The framework claim is a ratio at fixed mass, so the constant — and the σ_3D² = 3σ_p² factor — cancel exactly: **log10 T_vir = 2·log10 σ_p**.
- **N = 58**, not 59 (the task line's "59" counts the TSV header row). 0.1023 ≤ z ≤ 0.2894, **median z = 0.1632** (the task's "~0.13" guess is off; the true median is used).
- **Mass columns:** tabulated M200e14 = the paper's **caustic mass** (all masses from the same pipeline — internally homogeneous). It is ~2× the Δ=200 definitional mass ((500/200)(r500/r200)³ median 0.751 vs implied M500/M200 = 0.369) — stated, not hidden; both columns are single-survey products so the matched comparison is self-consistent. M500 robustness leg: definitional M500 = (4π/3)·500ρ_c(z)·r500³ from r500Mpc (paper cosmology H0 = 100h, Ωm = 0.3, ΩΛ = 0.7; h = 0.7 for display; h cancels in the matched ratio test).

---

## 2. METHOD — the z-split and the mass matching

1. **Z-split** at the sample median z = 0.1632 → low-z arm: 29 clusters (med z = 0.1333), high-z arm: 29 clusters (med z = 0.2173). Gap Δz ≈ 0.084.
2. **Mass truncation (selection guard):** both arms restricted to the joint M200 window **M200 ∈ [0.74, 10.70] × 10¹⁴ M☉** → 55 of 58 clusters survive (dropped: Zw1478, Zw3179 — low-z low-mass tail; A1763 — high-z high-mass tail). *The M-overlap is reported and is the entire mass support of the Δ estimate — nothing outside it is compared.*
3. **Primary Δ:** ANCOVA z-flag offset at fixed log10 M200 within the overlap (pooled slope 0.715; arm slopes 0.79/0.65 — the slope mismatch is itself evidence of mass-dependent selection and is handled by the robustness estimators, not hidden).
4. **SEs:** jackknife-over-cluster (primary), bootstrap-over-cluster (cross-check), σ-error propagation (secondary). Everything quoted with SEs.

---

## 3. RESULTS — measured Δlog10 T at fixed mass, with SEs

| Estimator | Δlog10 T (dex) | SE | z vs framework 0.000 |
|---|---|---|---|
| **ANCOVA, median split (PRIMARY)** | **+0.0620** | **0.0198 (jackknife)** | **+3.13** |
|  — bootstrap cross-check | +0.0620 | 0.0197 (95% CI [+0.016, +0.093]) | +3.1 |
|  — N_m-weighted ANCOVA | +0.0416 | — | +2.1 |
| NN matching k=1 (paired, jackknife) | +0.0556 | 0.0285 | +1.95 |
| NN matching k=3 | +0.0418 | 0.0300 | +1.40 |
| M500-matched ANCOVA (r500 def.) | +0.0596 | 0.0247 | +2.41 |
| Split at z = 0.15 | +0.0775 | 0.0180 | +4.31 |
| Split at z = 0.18 | +0.0746 | 0.0191 | +3.90 |

**Predictions over the arm gap (med z 0.1333 → 0.2170):** framework **−0.000001 dex** (flat to 1e-5); M-RISE (scaled) **+0.0238 dex** (the +0.0996 dex reference applies to z 0.1→0.5; over this narrow gap the honest rival prediction is +0.024 dex).

**Significance summary:** Δ_meas − framework = **+3.13 SE** (primary); Δ_meas − M-RISE_scaled = **+1.93 SE**; Δ_meas − (+0.1 dex) = −1.92 SE. Linear-z regression on the pooled overlap: dlog10T/dz = +0.64 ± 0.18 per unit z (t = 3.5).

**Influence:** no single cluster drives the result (largest leave-one-out shift 0.009 dex; dropping the most massive low-z anchor A1437 leaves Δ = +0.065). N_m balanced between arms (median 165 vs 174 — no membership-completeness confounder of first order).

---

## 4. THE FALSIFIER — pre-registered K1/K2 verdicts, reported honestly

> **K1 — FIRED (kill-candidate).** |+0.0620| = 3.13 SE > 3 SE from the framework's 0.000. By the letter of the pre-registration, **the framework's virial-T z-invariance is violated at low z on real clusters.** This is the honest reading of the primary estimator, stated without spin: the high-z HeCS arm is warmer at fixed M200 than the low-z arm.

> **K2 — NOT met.** The measured Δ is 3.1 SE from 0 (fails the "< 2 SE from framework" leg) and only 1.9 SE from the scaled M-RISE prediction (fails the "> 3 SE from M-RISE" leg). **M-RISE is NOT excluded at low z** — the data overshoot M-RISE's own low-z prediction by ~2×, so they are consistent with *neither* the flat framework line (3.1 SE) *nor* the M-RISE growth (1.9 SE).

**The honest tension:** the excess is positive (same sign as M-RISE) but **twice as large** as M-RISE predicts over this z-gap, and its mass-dependence (arm-line gap: +0.147 dex at the low-mass edge → +0.068 at mid → −0.012 at the high-mass edge; the excess concentrates in the mid-mass bin, +0.11 dex) is the structure of **LX flux-limited selection at fixed mass** (K3, pre-registered): fixed flux ⇒ higher-z systems must be over-luminous ⇒ systematically over-hot/over-dispersed at fixed M200. A truly mass-independent growth law would show a flat mass-dependence. The measured pattern is therefore reported as a **kill-CANDIDATE on the framework with the selection confounder flagged — NOT as an adjudication.**

**Robustness verdict:** the *direction* (+0.04 to +0.08 dex) is robust across all 7 alternative estimators; the *significance* is not (1.4–4.3 SE across estimators; NN k=3 gives 1.4 SE, M500-matching 2.4 SE). The spread of the z-statistic across estimators is the honest measure of how close to the 3-SE line this result sits: it is a 2–4 SE effect depending on how you match, surviving every matching scheme in direction.

---

## 5. VERDICT

**KILL-CANDIDATE FIRED, NOT adjudicative.** On 55 real HeCS clusters (median-z split, M200 overlap [0.74, 10.70]×10¹⁴ M☉), Δlog10 T_vir(high−low z) at fixed mass = **+0.062 ± 0.020 dex (jackknife SE)**, **3.1 SE** from the framework's 0.000 — the pre-registered 3-SE falsifier fires on the primary estimator. The excess is robust in direction, marginal-to-significant in magnitude, overshoots the M-RISE low-z prediction (+0.024 dex) by 1.9 SE, and is mass-dependent in exactly the way the pre-registered LX-flux selection confounder predicts. **M-RISE is not excluded (K2 failed); the framework's flat line is in tension at 2.4–4.3 SE depending on the estimator.** This is one survey, low z, kinematic T only, with a known positive selection bias on the measured axis — the WG high-z leg (X-ray/SZ masses + temperatures, eRASS:3 cluster products) is required to adjudicate framework vs M-RISE. No overclaim: this lane does not kill the framework outright (selection confounder unresolved), and it does not save M-RISE (measured slope overshoots its prediction).

**Checks: 7/8 PASS** (`O02 COMPLETE: 7/8 checks PASS.`; the honest FAIL is K2 — M-RISE not excluded).

---

*Deliverables: `deepseek_push/O02_hecs_ztest.py`, `O02_hecs_ztest.out`, `O02_results.json`, `O02_HECS_ZTEST.md`. No git commit. All numbers reproducible with one command.*