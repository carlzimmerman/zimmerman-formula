# CFG687 — 318 eROSITA clusters: raw KiDS shear vs the law from their X-ray gas (criteria 12cb826e8; block CFG680–689)

KiDS-1000 shear (CFG686 estimator, BAO-raw distances, ν_mono, no NFW/ΛCDM halo) stacked around 318 eRASS1 clusters (z 0.05–0.50) in
the KiDS footprint; gas = β-model normalised to eRASS1 Mgas500 (R500 used only as the aperture); jackknife over 30 sky patches.
Stack ΔΣ (M☉/pc²) at R = 0.18 … 2.49 Mpc: 92 ± 37, 72 ± 18, 77 ± 10, 57 ± 8, 52 ± 5, 36 ± 3, 17 ± 3, 17 ± 2.
| band | A, law canonical | A, law alt | A, Newtonian baryons |
|---|---|---|---|
| INNER 0.15–0.5 (not used) | 2.51 ± 0.32 | 2.31 ± 0.30 | 10.4 ± 1.4 |
| MID 0.5–1.2 Mpc | **1.91 ± 0.12** | **1.75 ± 0.11** | 10.2 ± 0.7 |
| OUTER 1.2–3 Mpc | **1.01 ± 0.09** | **0.93 ± 0.08** | 7.3 ± 0.6 |
**T1 (frozen): CORE EXCESS** on both footings (51 of 54 brackets; 1 EXTENDED, 2 LAW OVERPREDICTS). The law's own lensing from the gas
matches the outer shear to ~10%; inside ~1 Mpc there is an extra ×1.75–1.9 at 7σ — the cold-energy mass sits where the gas is.
Consistent with CFG686 (8 ACCEPT clusters): OUTER −0.04σ.
**T2 (frozen): FOLLOWS NEWTON — against the law.** ΔΣ_OUTER ∝ Mgas500^s with s = 0.90 ± 0.21 vs the law's s = 0.47 and Newton's 0.84.
A_OUTER by gas tercile: 0.57 (Mgas 3.7e12, z 0.15) → 0.96 (1.2e13, z 0.24) → 1.38 (2.9e13, z 0.31).
POST-HOC mechanism check (cfg687_posthoc_t2.py, not frozen): X-ray neighbours do NOT explain it (≈ 10% of clusters have an eRASS1
neighbour within 0.5–3 Mpc and |Δz| < 0.02, flat with mass, Spearman −0.03); ISOLATED clusters alone give s = 0.85 ± 0.17 (law 0.47,
Newton 0.83). Open mechanisms, untested: (a) Eddington/selection bias in eRASS1 Mgas500 at low mass (flux-limited sample; would push
low-mass A below 1); (b) environment below X-ray detection (galaxy/group 2-halo), which grows with mass in any theory; (c) a real
failure of the law's √M outskirts — the outer lensing mass scaling like M, as a cold-energy component proportional to the baryons would.
MUTATE: M1 cross-shear OUTER 0.05 ± 0.07 ✓, MID 0.16 ± 0.11 (1.5σ), INNER −0.44 ± 0.27; M2 random-minus-random OUTER +0.13 ± 0.06
(2.2σ — a small additive systematic, ~2 M☉/pc², disclosed), MID −0.06 ± 0.13 ✓; Newtonian (a0 → 0) A = 7–10 ✓.
κ fitted; cold energy mass required; not theory closed.
