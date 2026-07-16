# Cluster Lensing Kink — Realistic Target Spec (Door 2, prep 2026-07)

**One-line verdict (honest): on realistic cluster baryon profiles the y_c throttle kink does NOT sit at ~150 kpc. It sits at r_kink ≈ 8–23 kpc — inside the BCG (≤ ~1.3 R_e), 96–100 % BCG-dominated, 10–20× below the usable weak-lensing floor, with an amplitude 2.3–3.5× below the banked 0.06 dex systematics floor. It is not an actionable Euclid weak-lensing target. The actionable statement for wide surveys is the NULL side: everywhere they can measure (R ≳ 100 kpc), the throttled and uncut framework laws agree exactly.**

Every number below is printed by `kink_target_spec.py` (exit 0, gates at bottom of script; full console dump in `run_output.txt`). No hard-coded passes; the script re-verifies the banked fingerprint numbers before using them.

---

## 1. The prediction being specced

Branch-B elastic-medium throttle (Verlinde entropy-budget pin; banked in
`zimmerman-formula/real_research/papers/ELASTIC_MEDIUM_YC_Z2_2026.md` and
`zimmerman-formula/real_research/reviews/cluster_rar_throttle_2026/lane1_predict.py`):

- Framework law (uncut): g_obs = g_bar·ν(y), ν(y) = √(1+1/y), y = g_bar/a0 (the framework's own dS-Unruh interpolation, not McGaugh's).
- Throttle: T(y) = min(1, (y_c/y)^n), y_c = Z/2 = 2.894 (dimensionless, footing-free), n=1 minimal / n=2 bracket; g_obs = g_bar·[1 + (ν−1)T].
- The kink locus in acceleration: **g_bar = y_c·a0 = 2.709e−10 m/s² (canonical a0 = 9.36e−11) / 3.271e−10 m/s² (alt a0 = 1.13e−10)**.
- Universal (footing-independent) amplitude, re-verified by the script against the banked lane1 numbers:
  - peak RAR deviation **0.017 dex at y ≈ 6.1** (n=1); **0.026 dex at y ≈ 5.2** (n=2);
  - RAR slope discontinuity at y_c: dlog g_obs/dlog g_bar drops from 0.872 to **0.734 (n=1) / 0.597 (n=2)** — a slope break of −0.14 / −0.27.
- Deviation exists **only at y > y_c (inside r_kink)**; outside, T = 1 and the throttled law is *exactly* the uncut law.

## 2. Why Gemini's 150 kpc was optimistic

Gemini's committed mock (`zimmerman-formula/real_research/reviews/open_doors_2026_07/cluster_throttle_lensing_mock.py`) put **1e14 M☉ of baryons inside a 50 kpc Hernquist** — i.e. the entire baryon budget of an M500 ≈ 1e15 cluster compressed to BCG scales. The script reproduces its r_kink = 150.3 kpc exactly (gate, ±15 kpc). Real clusters hold ~90 % of their baryons in ICM gas spread over ~r500 (Mpc) scales, where the gas contributes g_bar ~ 1e−11 m/s² — 30× below the kink threshold. Only the BCG reaches y_c.

## 3. Realistic baryon models (parameters cited)

| Component | Model | Parameters | Source |
|---|---|---|---|
| BCG stars | Hernquist (R_e = 1.8153 a) | M*_BCG = 5e11·(M500/1e14)^0.4 → 5.0e11 / 9.5e11 / 1.5e12 M☉; R_e = 12 / 20 / 30 kpc | Hernquist 1990, ApJ 356, 359; Kravtsov, Vikhlinin & Meshcheryakov 2018, Astron. Lett. 44, 8 (slope 0.4 ± 0.1); Kluge+ 2020, ApJS 247, 43 (BCG R_e tens of kpc) |
| ICM gas | β-model, β = 0.65, r_c = 0.12 r500, normalized to M_gas(r500) = f_gas·M500 | f_gas = 0.09 / 0.12 / 0.13 for M500 = 1e14 / 5e14 / 1.5e15 M☉ | Vikhlinin+ 2006, ApJ 640, 691 (outer slopes β ≈ 0.6–0.7; f_gas(r500) ≈ 0.08–0.13 rising with mass); Mantz+ 2014, MNRAS 440, 2077 (f_gas ≈ 0.125, massive relaxed) |
| Cool-core variant | + inner β component: r_c = 25 kpc, β = 0.60, n_e(10 kpc) = 0.05 cm⁻³ (total gas renormalized) | typical Vikhlinin+ 2006 cool-core central densities | Vikhlinin+ 2006 |
| 2×BCG variant | M*_BCG doubled | brackets IMF/aperture-ICL systematic | Newman+ 2013, ApJ 765, 24/25; Conroy & van Dokkum 2012, ApJ 760, 71 |

Cosmology: H0 = 70, ρ_crit = 9.204e−27 kg/m³; r500 = (3M500/4π·500ρ_c)^⅓ = 706 / 1206 / 1740 kpc.

## 4. Where the kink actually lands (the table)

r_kink = radius where g_bar crosses y_c·a0; r_peak = radius of maximum deviation (y ≈ 5.8, canonical); BCG frac = BCG share of M_bar at r_kink.

| Model | r500 (kpc) | r_kink canon (kpc) | r_kink alt (kpc) | r_peak canon (kpc) | r_kink/R_e | BCG frac | y at 200 kpc |
|---|---|---|---|---|---|---|---|
| 1e14 fiducial | 706 | **9.5** | 8.0 | 4.4 | 0.79 | 99.7 % | 0.073 |
| 5e14 fiducial | 1206 | **11.2** | 9.2 | 4.2 | 0.56 | 99.5 % | 0.166 |
| 1.5e15 fiducial | 1740 | **11.1** | 8.6 | 2.4 | 0.37 | 99.5 % | 0.238 |
| 1e14 cool-core | 706 | 9.7 | 8.1 | 4.4 | 0.81 | 97.0 % | 0.090 |
| 5e14 cool-core | 1206 | 11.6 | 9.4 | 4.2 | 0.58 | 96.1 % | 0.209 |
| 1.5e15 cool-core | 1740 | 11.6 | 8.9 | 2.5 | 0.39 | 95.9 % | 0.301 |
| 1e14 2×BCG | 706 | 16.1 | 14.1 | 9.0 | 1.34 | 99.5 % | 0.090 |
| 5e14 2×BCG | 1206 | 20.4 | 17.6 | 10.5 | 1.02 | 99.1 % | 0.197 |
| **1.5e15 2×BCG (max case)** | 1740 | **22.7** | 19.1 | 10.3 | 0.76 | 98.9 % | 0.285 |

Notes:
- r_kink is nearly **mass-independent** (9.5→11 kpc across a 15× range in M500): it is set by the BCG alone, and M*_BCG grows only as M500^0.4 while R_e also grows.
- The **footing fork moves r_kink by only ~15 %** (canon vs alt) — both footings land the kink inside the BCG; the fork is not decision-relevant here.
- Even the most favorable honest case (1.5e15, 2× BCG mass) gives 23 kpc. To recover Gemini's 150 kpc you need ~1e14 M☉ of baryons within ~200 kpc — no real cluster has that.

## 5. Amplitude in the lensing observable

Full Abel projection of the effective density (throttled n=1 vs uncut, canonical footing). Because the two laws share the same effective enclosed mass at r_kink and are identical outside it, the throttle only **redistributes** effective mass interior to r_kink. The projected signature in Σ(R) (≡ convergence κ up to Σ_cr — what strong-lensing maps measure at these radii) is **bipolar and confined to R < r_kink**:

| Cluster (fiducial) | Σ-deficit lobe (R inside zero-crossing) | Σ-excess lobe (just inside r_kink) | Signal at R > r_kink |
|---|---|---|---|
| 1e14 | +2.9 % (peak at ~1 kpc, crossing ~5.0 kpc) | −3.1 % at 8.2 kpc | exactly 0 (checked: <0.001 % at 2 r_kink) |
| 5e14 | +2.8 % (crossing ~5.9 kpc) | −2.1 % at 9.5 kpc | 0 |
| 1.5e15 | +2.6 % (crossing ~5.8 kpc) | −1.4 % at 9.5 kpc | 0 |

**ΔΣ (the stacked weak-lensing observable) at R > r_kink carries NO signal at all** — the interior redistribution nets to zero inside the cylinder. There is nothing for a shear survey to see outside ~12 kpc even with perfect precision.

RAR-space equivalents (footing-free): 0.017 dex (n=1) / 0.026 dex (n=2) peak deviation; slope break −0.14 / −0.27 at g_bar = y_c a0.

## 6. What a measurement would need

Statistical requirement (script section 3; signal template = fractional Σ deficit, 0.1-dex bins over 0.1–1.5 r_kink, i.e. **~1–14 kpc**):

| Cluster | window | per-bin Σ precision for 3σ | for 5σ | N clusters at 5 %/bin (SL-quality), 5σ |
|---|---|---|---|---|
| 1e14 | 0.9–12 kpc | 2.5 % | 1.5 % | ~12 |
| 5e14 | 1.1–14 kpc | 2.1 % | 1.3 % | ~16 |
| 1.5e15 | 1.1–14 kpc | 1.7 % | 1.0 % | ~24 |

Radial resolution: the deficit and excess lobes are separated by ~0.3 dex in R; bins ≤ 0.1 dex at R = 1–15 kpc are required. At z = 0.2–0.4 that is 0.25–3 arcsec — angular resolution is *not* the obstacle (JWST/HST resolve it trivially; Euclid's PSF marginally).

**The obstacle is systematic, and it is decisive:**

1. **Weak lensing cannot reach the radii.** Usable stacked-WL information starts at R ≈ 100–200 kpc (miscentering, BCG light, cluster-member contamination, source blending). r_kink is 10–20× below that floor. And at the radii WL does measure, y ≤ 0.3 ≪ y_c — the throttle predicts *exact* agreement with the uncut law there (T=1).
2. **At 1–15 kpc the mass budget is 96–100 % BCG stars.** Detecting the kink means knowing g_bar there to better than the signal (≲ 0.01 dex ≈ 2 %). The BCG stellar-M/L (IMF) systematic in massive early-type cores is ~0.1 dex (factor ≈ 1.5–2; Conroy & van Dokkum 2012; Newman+ 2013, 2017) — **4–6× the entire signal**. The banked known-systematics floor of 0.06 dex is itself 2.3–3.5× the signal.
3. Strong lensing + BCG kinematics (Newman-style decompositions, 3–300 kpc) are the only probes with access, and their per-bin Σ precision (~5 %) meets the *statistical* bar with ~12–24 well-modeled clusters — but their g_bar error is the same BCG M/L that is 4–6× the signal. A radial IMF/M-L gradient (observed in massive ETGs at the 0.05–0.2 dex level) mimics exactly the smooth curvature into which a 0.1-dex-binned kink smears.

**One honest caveat in the framework's favor:** the kink is a *slope discontinuity at a fixed g_bar*, not an amplitude offset. A constant M/L error shifts the apparent kink location (by Δlog r ≈ Δlog Υ/2) but cannot erase a genuine break; only M/L *gradients* mimic/mask it. A future spec for BCG-core stellar kinematics with spatially resolved IMF-sensitive spectroscopy (per the banked SPARC-fingerprint requirement, external M/L priors at ~0.005 dex) is the only route we can articulate — that is beyond any current or funded program at cluster-core radii.

## 7. The actionable table for an Euclid/JWST team

| Question a survey team would ask | Answer from this spec |
|---|---|
| Where is the break? | g_bar = 2.71e−10 (canon) / 3.27e−10 (alt) m/s²; in radius: **8–23 kpc** for every realistic cluster (all masses 1e14–1.5e15, cool-core and 2×BCG variants, both footings) |
| How big? | 0.017–0.026 dex in the RAR; bipolar ±2–3 % in Σ(R), confined to R < r_kink; **zero signal in ΔΣ at R > r_kink** |
| Can Euclid WL see it? | **No.** r_kink is 10–20× below the usable WL floor; at measurable radii the prediction is exact agreement with the uncut law (a consistency null, not a detection channel) |
| Can JWST/HST strong lensing see it? | Access yes (1–15 kpc, sub-arcsec), statistics yes (~12–24 well-modeled clusters at 5 %/bin), but **g_bar is 96–100 % BCG stars and the IMF/M-L systematic is 4–6× the signal** — not detectable with current stellar-population priors |
| What would change the verdict? | External BCG M/L priors at ~0.005–0.01 dex at r < 15 kpc (spatially resolved IMF spectroscopy), or a cluster class with y_c-crossing baryons outside the BCG — which the gas budget (f_gas profiles, Vikhlinin+ 2006) shows does not exist |

## 8. Reproducibility

- `kink_target_spec.py` — exit 0; gates re-verify: y_c = Z/2, both kink accelerations, the banked 0.017 dex @ y≈6 fingerprint (lane1), the n=2 bracket, Gemini's 150 kpc reproduction, finiteness + interiority of every r_kink, bipolar %-level projection with exterior agreement < 0.5 %. **No detectability is asserted anywhere.**
- `run_output.txt` — full console output of the exit-0 run (2026-07-16).
- Banked inputs: `real_research/reviews/cluster_rar_throttle_2026/lane1_predict.py` (throttle + fingerprint), `real_research/papers/ELASTIC_MEDIUM_YC_Z2_2026.md` (y_c = Z/2 derivation, DOI-backed), `real_research/reviews/open_doors_2026_07/cluster_throttle_lensing_mock.py` (the optimistic mock this spec corrects).

*Frozen-repo rule honored: nothing in `zimmerman-formula/` was modified; all outputs live in `prep_2026/cluster_kink_spec/`.*
