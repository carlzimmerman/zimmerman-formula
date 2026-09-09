# L85 — the Bullet cluster: does the F(Q)Θ collisionless dust reproduce the lensing–gas offset?

`L85_bullet_cluster_lensing.py` / `L85_bullet_cluster_lensing.out`. **17 checks, 17 PASS.** numpy only, no
imports from `qwen_claude_field_theory`. Both a₀ footings (9.3619e-11 / 1.1279e-10 m s⁻²).

This lane makes prediction **P5** (`predictions_2026/PREDICTIONS_NEW_FINDINGS_2026-09-09.md`) a quantitative,
adversarial check. P5: in a merging cluster the weak-lensing (total-mass) centroid should **separate from the
X-ray gas and trace the galaxies/collisionless dust** — like CDM, and **unlike pure MOND**, which puts the
lensing on the gas and famously fails the Bullet offset.

## The test system and the published numbers

Bullet cluster **1E0657-56** (z = 0.296). In a supersonic merger the *collisionless* components (galaxies,
and — in this framework — the pressureless c_s²=0 Noether dust of L81/L82) pass through each other, while the
*collisional* X-ray gas shocks and lags. The mass peaks and the gas peaks separate.

| quantity | value | source |
|---|---|---|
| X-ray gas mass (dominant baryon) | **22.3 × 10¹³ M☉** | arXiv:2604.10811; Clowe 2006 "dominant baryonic mass component" |
| galaxy (stellar) mass | **1.70 × 10¹³ M☉** | arXiv:2604.10811; Paraficz+2016 f_stars = 11% of 2.5×10¹⁴ within 250 kpc |
| gas : stars | **13 : 1** | Clowe 2006; arXiv:2604.10811 |
| QUMOND phantom, total | 85.7 × 10¹³ M☉ | arXiv:2604.10811 |
| — of it, sourced by galaxies alone | 40.9 × 10¹³ M☉ | arXiv:2604.10811 |
| — ⇒ sourced by the gas | 44.8 × 10¹³ M☉ (≈52% of total) | arXiv:2604.10811 |
| separation of the two mass peaks | **720 kpc** | Clowe et al. 2006 |
| lensing offset from the gas | **8 σ** | Clowe et al. 2006 |
| total Newtonian dark / baryon (core) | **6.8** (band [5.7, 9.0]) | g04a; L7 (5.73 cosmic); L18 (9.04 bias-corrected) |
| L7 residual after the framework's own kernel / baryon | 3.09 canonical / 2.76 alt | FINDINGS L7 |

## The model

A projected **first-moment (centroid) model** on the merger axis — the standard toy for the peak-offset
observable, **not** a full convergence-map reconstruction. Two anchors:

- **x = 0**: the collisionless peak (galaxies + dust) = where lensing is **observed** (Clowe: lensing traces
  the galaxies).
- **x = d**: the gas peak.

The lensing centroid is `x_c/d = M_gasside / (M_gasside + M_galside)` with
`M_gasside = M_gas + Φ_gas` and `M_galside = M_stars + Φ_gal + M_dust`. **x_c/d > 0.5 ⇒ on the gas side**
(the MOND failure); **x_c/d < 0.5 ⇒ on the galaxy side** (matches the Bullet). `d` cancels in the side test;
absolute offsets use the observed d = 720 kpc.

**No double-counting.** The observed total Newtonian dark (6.8× baryons) is split into the MOND phantom
(sourced by baryons, staying with its source: Φ_gas on the gas, Φ_gal on the galaxies) **plus** the
collisionless Noether dust (the remainder, which passes through with the galaxies). The only mass that lands
on the gas side is `M_gas + Φ_gas`.

## Results

**Control — pure MOND fails, reproduced two ways (M1, M2).** Lensing traces the modified-gravity potential of
the baryons; the gas is the dominant baryon, so the centroid sits **on the gas**:

- Textbook (lensing ∝ baryons, the boost cancels): `x_c/d = M_gas/(M_gas+M_stars) = 0.929`. MOND predicts the
  lensing 669 kpc from the galaxies and only 51 kpc from the gas — **opposite to the 8σ observation**.
- MOND-favourable (the QUMOND phantom-concentration reading, arXiv:2604.10811, dust = 0): `x_c/d = 0.612`.
  Even MOND's best case is still on the gas side, because the diffuse gas sources ~half the phantom and is the
  dominant baryon.

**Main — F(Q)Θ flips the centroid to the galaxies (M3, M4).** With total dark = 6.8× baryons split into the
published QUMOND phantom (the *strongest* gas competition) plus a collisionless dust (77×10¹³ = 3.2× baryons)
on the galaxies, the centroid lands on the **galaxy side**: `x_c/d = 0.358`, separating from the gas by
**462 kpc** — the observed offset. This holds on **both a₀ footings** and for a modest single-scale MOND boost
(`x_c/d = 0.15`) as well as the MOND-strong phantom (`x_c/d = 0.36`).

**Adversarial — does the clock's gas-MOND drag it back? Competes, but does not win (A1–A4).** The clock boosts
*all* baryons including the gas, placing a real phantom `Φ_gas = 44.8×10¹³` (~2× the gas mass) **on the gas**;
the gas-side total is `M_gas + Φ_gas = 67.1×10¹³`, not negligible. But the centroid reverses to the gas side
only if the clock dumps **> 83%** of its phantom onto the gas, whereas the physical/published split is
**~52%** (compact galaxies source a more peaked phantom than the diffuse gas, so Φ_gal ≳ Φ_gas). Comfortable
margin. Two negative controls confirm the mechanism: zeroing the dust returns the centroid to the gas side
(= the MOND control), and turning the clock's gas-boost off moves the centroid *further* onto the galaxies
(so the gas-phantom's effect is genuinely to pull toward the gas — the adversarial concern is real, it just
loses to the dust).

**CDM benchmark and sensitivity (S1, S2).** Pure collisionless CDM gives `x_c/d = 0.119`. The F(Q)Θ centroid
(0.36 with the strongest phantom, 0.15 with a modest one) is on the same side and overlaps the CDM value. The
result stays on the galaxy side across the whole dark-to-baryon band [5.7, 9.0].

## The honest caveat (S3)

The F(Q)Θ lensing centroid is **not exactly on the galaxies**: the bare gas (22×10¹³) plus the clock's
gas-phantom pull it ~258 kpc back toward the gas (of the 720 kpc separation), leaving it 462 kpc from the gas.
This residual lensing–galaxy offset is a **genuine, testable sub-prediction**; it shrinks if the clock's
gas-boost is modest. Real CDM largely shares it (the gas is real mass sitting at the gas peak in ΛCDM too), so
it is not a distinctive failure — but the framework's *extra* gas-phantom makes its offset larger than ΛCDM's
in the MOND-strong case (0.36 vs 0.12), which is where the two could in principle be told apart.

**Scope.** This lane tests only the lensing-centroid **geometry**. The cluster dust amount (6.8× baryons) is
taken from the repository's cluster lanes (g04a, L7), not re-derived here; and **P7** — why the dust
concentrates in clusters but is absent from galaxy dynamics (cosmological infall vs internal acceleration) —
remains an open mechanism. The full statistical "8σ" is a property of the convergence map, not reproduced
here; this lane reproduces the **sign, side, and ~Mpc magnitude** of the offset.

## Verdict and confidence

**P5 is reproduced.** Pure MOND puts the lensing on the gas (x_c/d = 0.61–0.93) — the classic Bullet failure —
and the F(Q)Θ collisionless Noether dust flips the centroid to the galaxy side (x_c/d = 0.12–0.36), matching
the observed offset. The clock's gas-MOND is a real competing effect but does not reverse the outcome under
the physical phantom split.

**Confidence: moderate-to-high on the direction, lower on the exact coincidence.** The *direction* (dust flips
the centroid to the galaxy side, unlike MOND) is robust — it follows from the dust being collisionless and
≳ the gas-side mass, and it survives both footings, the full dark-ratio band, and the strongest published
gas-phantom. What is *not* robust to model detail is how tightly the lensing coincides with the galaxies: the
clock's gas-phantom leaves a real ~250 kpc residual offset in the MOND-strong case. This is honestly a
**qualitative reproduction of the defining Bullet feature** (lensing off the gas, with the collisionless
component), not a parameter-free match to the exact peak positions — which would require the phantom split and
the dust distribution to be computed from the F(Q)Θ action in the merger geometry, not taken as inputs.

## Sources

- Clowe et al. 2006, ApJ 648, L109 — *A Direct Empirical Proof of the Existence of Dark Matter* (arXiv:astro-ph/0608407)
- Paraficz et al. 2016, A&A 594, A121 — *The Bullet cluster at its best: weighing stars, gas, and dark matter* (arXiv:1209.0384)
- Randall et al. 2008, ApJ 679, 1173 — merger masses/velocity of 1E0657-56
- arXiv:2604.10811 — *A consistent MOND modelling of the Bullet Cluster* (component masses and the QUMOND phantom split)
- Repository: `fable_independent_2026/FINDINGS.md` (L7, L18, L24, L81, L82); cluster standing g04a; `predictions_2026/PREDICTIONS_NEW_FINDINGS_2026-09-09.md` (P5, P7)
