# X1_hosted_recount: literature look-up record (PROVISIONAL; written before any script or number of this lane)

The published MOND predictions used as the step-1 controls are **not on disk** (`real_research/cross_thread_review_2026_09_26/XR27_efe_favouring.py`
line 31 says so for McGaugh & Milgrom's table). They were read through WebFetch on 2026-10-23. WebFetch returns a small model's
reading of the page, not the page itself, so every value below is **LITERATURE-INPUT, PROVISIONAL**.

How they were read (the record's rule for web look-ups):
- arXiv HTML renderings only (ar5iv). No PDF was fetched and no binary was saved. Nothing was downloaded into the repo.
- No candidate value or name was put in any prompt. Each prompt asked for table rows or sentences verbatim, in printed order.
- Each paper was read **twice, from two different URLs** (`/html/<id>` and `/abs/<id>` on ar5iv.labs.arxiv.org), with different
  prompts. The two reads agree in every value transcribed here.
- Firm-up route (not taken): read the published tables directly from the journal PDFs. That needs the owner's approval of a download.

## McGaugh & Milgrom 2013a, ApJ 766, 22 (arXiv:1301.0822), "Andromeda dwarfs in light of MOND"

Method, as read:
- Eq. (2), isolated: σ_iso ≈ (4/81 · G M a₀)^(1/4).
- Eq. (3), external-field dominated: σ_efe ≈ (G_eff M / 3 r_{1/2})^(1/2), with G_eff = G/μ(g_ex/a₀).
- g_ex = V²_M31/D_M31, V_M31 ≈ 230 km/s (Chemin+2009); D_M31 = the dwarf's distance from M31's centre (not printed in the tables).
- a₀ = 1.21e-10 m/s² (Begeman+1991). M = Υ★ L_V with Υ★ = 2 (range 1–4).
- r_{1/2} = 4 R_e/3, the 3-D half-light radius from published major-axis R_e.
- μ's functional form is not named. (Pre-result note, from the printed numbers only: And I's printed σ_efe = 8.0 km/s is what
  Eq. (3) gives with μ = x/(1+x) at the LVD host distance 44.39 kpc; μ = x gives 7.0. This lane therefore reads μ = x/(1+x),
  and backs the field out of each printed σ_efe with that μ, so the control does not depend on this reading; see FROZEN_CRITERIA §2.)
- Paper II states: "In general, the case that applies is the one that returns the lower value for σ."

Table 1 of 1301.0822 (17 dwarfs; L_V in 1e5 L☉, r_{1/2} in pc, σ in km/s, Υ★ = 2 central values; "…" = no σ_efe printed). The
summariser flagged the L_V and r_{1/2} cells as fragmented in the HTML (for example "045.", "0832"); they are read here as 45. and 832.
This reading is checked independently by C0 (σ_iso recomputed from L_V must match the printed σ_iso).

| dwarf | L_V | r_{1/2} | σ_iso | σ_efe |
|---|---|---|---|---|
| And I | 45. | 832 | 9.2 | 8.0 |
| And II | 93. | 1660 | 11.0 | … |
| And III | 10. | 525 | 6.3 | 5.4 |
| And V | 5.9 | 292 | 5.5 | 7.0 |
| And VI | 34. | 440 | 8.6 | … |
| And VII | 178. | 977 | 13.0 | … |
| And IX | 1.5 | 552 | 3.9 | 1.5 |
| And X | 0.76 | 309 | 3.3 | 2.3 |
| And XI | 0.49 | 145 | 3.0 | 3.2 |
| And XII | 0.31 | 289 | 2.6 | 1.7 |
| And XIII | 0.41 | 203 | 2.8 | 2.5 |
| And XIV | 2.1 | 537 | 4.3 | 3.6 |
| And XV | 7.1 | 355 | 5.8 | 6.1 |
| And XVI | 4.1 | 178 | 5.0 | … |
| And XVIII | 6.3 | 417 | 5.6 | … |
| And XXI | 4.6 | 1023 | 5.2 | 3.7 |
| And XXII | 0.35 | 340 | 2.7 | 2.3 |

## McGaugh & Milgrom 2013b, ApJ 775, 139 (arXiv:1308.5894), "Andromeda dwarfs in light of MOND. II. Testing prior predictions"

Its Table 1 reproduces Paper I's a-priori predictions for 13 dwarfs; its Table 2 gives 3 new predictions. Rows not already in
1301.0822's Table 1 (same conventions; σ_efe "…" = not printed):

| dwarf | table | L_V | r_{1/2} | σ_iso | σ_efe |
|---|---|---|---|---|---|
| And XVII | 1 | 2.6 | 381 | 4.5 | 2.5 |
| And XIX | 1 | 4.1 | 2244 | 5.0 | 2.6 |
| And XX | 1 | 0.28 | 165 | 2.6 | 2.1 |
| And XXIII | 1 | 10. | 1372 | 6.4 | 4.4 |
| And XXIV | 1 | 0.94 | 489 | 3.5 | 2.8 |
| And XXV | 1 | 6.5 | 945 | 5.7 | 3.5 |
| And XXVI | 1 | 0.59 | 296 | 3.1 | 2.0 |
| And XXVII | 1 | 1.2 | 579 | 3.7 | 1.8 |
| And XXVIII | 1 | 2.1 | 284 | 4.3 | … |
| And XXIX | 1 | 1.8 | 481 | 4.1 | 3.8 |
| And XXX (Cassiopeia II) | 2 | 1.4 | 356 | 3.8 | 3.5 |
| And XXXI (Lacerta I) | 2 | 41. | 1216 | 9.0 | … |
| And XXXII (Cassiopeia III) | 2 | 71. | 1941 | 10.3 | 10.3 |

The rows for And XVIII, XXI and XXII in 1308.5894's Table 1 repeat 1301.0822's values (checked: identical).
1308.5894 gives a₀ only as "a₀ ≈ 1e-10"; its tables reproduce Paper I's predictions, so Paper I's a₀ = 1.21e-10 is used for all 30 rows.

## McGaugh 2016, ApJL 832, L8 (arXiv:1610.06189), "MOND prediction for the velocity dispersion of the 'feeble giant' Crater II"

As read (both reads agree):
- Inputs: r_h = 1066 ± 84 pc, M_V = −8.2 ± 0.1 (Torrealba+2016); L_V = 1.6e5 L☉; Υ★ = 2 (+2/−1); M★ ≈ 3.3e5 M☉.
- D_GC = 120 kpc; V_MW = 184 km/s at that distance; g_ex ≈ 282 km² s⁻² kpc⁻¹ = 0.076 a₀.
- a₀ = 1.2e-10 m/s² = 3700 km² s⁻² kpc⁻¹.
- Eq. (1) σ_iso ≈ (4/81 a₀ G M★)^(1/4); Eq. (2) σ_efe ≈ (a₀ G M★ / 3 g_ex r_{1/2})^(1/2); r_{1/2} = 4 r_h/3; "μ(g/a₀) ≈ g_ex/a₀ is an
  excellent approximation" for Crater II.
- Predictions: σ_iso ≈ 4 km/s; **σ_efe = 2.1 (+0.9/−0.6) km/s** (Eq. 5; the range is the Υ★ factor-of-two range).

## Measured Crater II dispersion (reported only)

- On disk: LVD `vlos_sigma` 2.34 (+0.42/−0.30) km/s, ref Ji+2021 (`real_research/data/dsph/lvd_dwarf_mw.csv`). This is the lane's data value.
- Caldwell+2017 2.7 ± 0.3 km/s: on disk in `campaign_fresh_gravity/CFG257_ufd_kinematics_scoping/arroyo_polonio2026_tableA1.csv`
  (row "Cra II", `sig_lit`), with Arroyo-Polonio's binary-corrected free-f value 2.17 there. Reported as a variant only.
