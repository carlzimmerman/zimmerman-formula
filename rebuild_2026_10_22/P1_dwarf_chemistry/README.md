# P1_dwarf_chemistry — SUPPLY CONFIRMED at the median, both footings, but E6's ζ = 1 premise itself fails, 10 systems are short, and the result is not robust at 2σ in the MDF widths

**Verdict (frozen lines; F2 graded, both footings, never pooled).**
1. **SUPPLY CONFIRMED (median).** E6 assumed ζ = 1 and no pre-enrichment. This lane replaces both with the satellites' own
   metallicity distributions (MDFs). The median cold-supply ratio stays below 1.
   - Median q = L_req / L_MDF = **0.463** [0.298, 0.620] canonical and **0.445** [0.284, 0.588] alt (F2, log y −0.5, central width).
   - On the same systems, E6's premise gives 0.269. So the MDF raises the median need-to-supply ratio by about ×1.7. It stays below 1.
   - The class holds when Simon 2019 widths replace LVD's (R1: 0.286 / 0.283), and when Walker 2023 per-star widths do (R2: 0.366 / 0.301).
2. **E6's premise fails as a description.** A homogeneous leaky box with ζ = 1 and Z0 = 0 must have an intrinsic MDF width of
   0.434–0.557 dex, whatever its outflow (analytic; K6).
   - **10 systems are too narrow** on LVD widths (Boötes I, Carina II, Coma Berenices, Crater II, Eridanus IV, Hercules, Leo IV,
     Pictor II, UMa I, UMa II). The count is 3 on S19 widths and 2 on Walker widths.
   - The ζ = 1 MDF shape is rejected (AD test, p < 0.05) in **4 of 6** systems with ≥ 10 Walker stars (Boötes I, Crater II, Hydrus I, Tucana II).
3. **Why the supply survives anyway.** For any ζ ≥ 1, L = y · f(0+). The catchment is set by the MDF's metal-poor end, not by its
   mean (A1). A narrow MDF does lower L. But the width still bounds L, even with ζ unbounded: a broad spread needs either a low k or an
   early stop, and both leave a large L.
   - The minimum sits in a flat valley toward metal-only winds (η → 0, ζ ≫ 1; ζ spans 15–9609 within 1% of L).
   - So the MDF bounds L but does not fix ζ.
4. **Pre-enrichment raises L; it does not lower it.** At a fixed mean, external metals leave less self-enrichment per unit gas, so
   more gas must leave (K3: L_min 37.0 → 61.7 at [Fe/H] −2.5 with Z0 = 0.3 Z_g).
   - Pristine inflow also raises L.
   - So attributing a narrow MDF to ζ, as graded here, is the lowest-L reading.
5. **Not robust at 2σ in the widths.** With every system at its 2σ-low width at once, the median q is **1.12** canonical / **1.08**
   alt (16–84%: 0.86–2.32).
   - Only 14/31 (canonical) and 15/32 (alt) systems are supplied at their 2σ-low width.
   - No system is short robustly (2.5% need, +0.1 yield, 2σ-high width): 0 on both footings.
6. **Supply is not mechanism.** Even where the supply holds, no binding mechanism puts the cold energy inside r12. G2 failed. This
   lane says nothing about binding.

κ = ½ FITTED. Cold energy, no particle. Not "theory closed". Nothing here says the data favour the framework.

## Shortfall systems (q > 1, F2, log y −0.5, central LVD width; same 10 on both footings)
Aquarius II, Carina II, Columba I, Eridanus IV, Horologium I, Leo VI, Segue 1, Ursa Major I, Ursa Major II, Willman 1.

**E6's six, one by one** (q canonical, from `p1_per_system.csv`):

| system | LVD width (dex) | P-W | q (MDF) | q (E6 premise) | q with S19 / Walker width | reading |
|---|---|---|---|---|---|---|
| Columba I | 0.71 +0.49 −0.24 | consistent | 1.34 | 2.03 | — / — | broader than the box: L at the W1 edge; better than E6, still short |
| Segue 1 | 0.59 ± 0.06 | consistent | 1.14 | 1.73 | 1.14 (S19 0.95 also above) / — | broader than the box; still short |
| Tucana IV | < 0.64 (UL) | undetermined | NOT TESTED | — | — | only an upper limit: no lower bound on L |
| Ursa Major I | 0.24 +0.07 −0.05 | **narrow** | 3.73 | 1.16 | **0.76** / — | flips on the width compilation (S19 0.62) |
| Ursa Major II | 0.22 +0.09 −0.07 | **narrow** | 4.30 | 1.13 | **0.74** / 1.12 | flips on the compilation (S19 0.67, Walker 0.44) |
| Willman 1 | 0.30 +0.15 −0.11 | consistent (central narrow) | 2.17 | 1.03 | — / — | worse than E6 |

New shortfalls relative to E6's premise: Aquarius II, Carina II, Eridanus IV, Horologium I, Leo VI (all narrow MDFs).

## Numbers (from `p1_dwarf_chemistry_results.json`; median q [bootstrap 16–84%])
| footing, need | N | log y −0.5 | −0.2 | +0.1 | 2σ-low width, −0.5 |
|---|---|---|---|---|---|
| canonical F2 (graded) | 31 | **0.463** [0.298, 0.620] | 0.232 | 0.116 | 1.124 [0.860, 2.323] |
| canonical F1 | 31 | 0.275 [0.200, 0.520] | 0.138 | 0.069 | 1.048 |
| alt F2 (graded) | 32 | **0.445** [0.284, 0.588] | 0.223 | 0.112 | 1.078 [0.860, 2.323] |
| alt F1 | 32 | 0.242 [0.195, 0.457] | 0.121 | 0.061 | 0.824 |

- Υ_V sensitivity (F2 need ∝ ~1/Υ; gas-free L does not depend on M*): median q 0.62 / 0.46 / 0.37 canonical at Υ_V 1.5 / 2 / 2.5.
- Unmixed-ejecta escape (A4) is the one premise no MDF can test. Its price, f_break, is the escape fraction that would close each
  supplied system. Median 0.74; minimum 0.07 (Leo T) canonical, 0.06 alt.

## Premise tests
- **P-W (width):** LVD 23 consistent, 10 narrow, 0 broad at 2σ, 2 undetermined, 11 none. Central width above the family (ABOVE):
  Columba I, Segue 1, And XXIX and Leo T (its gas-bearing family); alt also And XXVIII. The compilations disagree by ×2–3 for the same systems: UMa I is 0.24 in LVD (Geha 2026) and 0.62 in S19;
  UMa II is 0.22 and 0.67; Boötes I is 0.28 (LVD), 0.44 (S19) and 0.40 (Walker).
- **P-S (shape, Walker per-star, N_Fe ≥ 10):** 4 of 6 fail (p 0.005–0.025). Reticulum II (p 0.78) and UMa II (p 0.58) pass.
- **P-A ([Mg/Fe], Walker):**
  - Boötes I shows a DECLINE (slope −0.36 ± 0.09): SN Ia iron during star formation.
  - Boötes III is on the PLATEAU (+0.48 ± 0.10).
  - Crater II is LOW (−0.40 ± 0.03): its α-anchored Fe yield lies above the CFG317 bracket, so the bracket is conservative there.
  - The other 5 are undetermined.
  - No system's α-anchored yield lies below −0.5. The [α/Fe] data do not push the yield below the graded corner.
- **P-0 (pre-enrichment):** raises L (K3). Extremely metal-poor members ([Fe/H] + 2e < −3): 1 in Boötes I, 1 in Tucana II.

## Inventory (`p1_inventory.csv`, all 46 systems)
- **Mean [Fe/H] and width.** LVD gives a mean [Fe/H] for 37 systems. It gives a central width for 32 (31 spectroscopic,
  1 photometric) and only an upper limit for 3 (Grus I, Pictor II, Tucana IV).
- **Other width sources.** S19 gives a width for 19 (+1 upper limit). Geha 2026 gives N_stars for 16.
- **Walker 2023 per-star.** 14 E3 systems have a Walker target. Member counts come from this lane's own rule and agree with CFG51
  within 0–1, except Segue 1 (2 vs 6): flagged spectra are excluded here. 6 have ≥ 10 [Fe/H] members; 8 have ≥ 5 [Mg/Fe] members.
  Median per-star [Fe/H] errors are 0.21–0.74 dex.
- **Not tested (14):** And XI, XIII, XV, XVII, XX, XXII, XXVI, XXVII; Carina III; Cassiopeia II; Grus I; Pictor II; Tucana II; Tucana IV.

## Checks and mutation
| check | result |
|---|---|
| K1 quadrature vs exact (k = 0 closed form + adaptive quad; u = ∞ digamma/trigamma) | PASS, max error 4e-14 / 3e-13 |
| K2 E6's L_min reproduced by independent code (36 systems, two corners) | PASS, 1.1e-14 |
| K3 pre-enrichment raises L; the ζ reading ≤ true L (9 synthetic pre-enriched MDFs) | PASS (ratio ≤ 0.037) |
| **K4** Gaussian σ estimator vs the skewed family | **FAIL as frozen**: median ratio 0.78 at σ 0.25 (N 30). Small-sample bias (0.97 at N 100). It biases q **toward shortfall**, so the graded result is conservative (A1) |
| K5 Walker membership: member median velocity vs LVD | PASS, ≤ 2.67 km/s (6 systems) |
| K6 band edges | PASS, [0.4343, 0.5570] dex |

- 5/6 checks pass; the normal run exits 1 because of K4, which is kept as frozen.
- **MUTATE** (k ≡ 0: E6's ζ = 1 imposed while the width is honoured): K1 FAILS. The narrow systems then have no bound, and the class
  turns to SUPPLY FAILS (median q 6.6 canonical). With E6's premise, the observed widths would break the supply.
- **A1 (post-result) bug fix:** Leo T was compared with the gas-free maximum width. RUN1 is kept (`*_RUN1.*`). The class is the same.

## The rebuild brief's changes (ledger §D)
AQUAL, native H₀ and the BS-dust abundance do not touch the chemistry. Screening enters only F1's need (F2 is graded). SPS M*
moves q as ~1/Υ (line above). No ΛCDM halo machinery and no standard-MOND machinery is used. 5.364 (ΛCDM-processed) enters
only through L_req, as in E6.

## Record errors found
- `doors_push_2026_10_22/E6_native_fret/FROZEN_CRITERIA.md` L59 and `README.md` L116: "pre-enrichment lowers L".
  - In E6's own model it **raises** L_min (K3; A3).
  - Only unmixed ejecta escape (a lower retained yield) lowers it.
- E6's conservative minimiser (closed box plus strip at small u) implies an MDF width of 0.434 dex. Systems measured broader (Segue 1,
  Columba I) cannot sit there, so their floor is higher than E6's. Systems measured narrower cannot be ζ = 1 boxes at all.

## What this does not show
- **Homogeneous mixing and unmixed ejecta escape are untested.** They need an absolute retained-yield anchor; none is on disk.
- **The width compilations disagree by ×2–3** for UMa I and UMa II. Their individual verdicts flip on which is used. Willman 1,
  Columba I and Tucana IV have no second width source.
  - **Most valuable next step:** one homogeneous per-star [Fe/H] set (errors ≤ 0.15 dex, N ≥ 30) for UMa I, UMa II, Willman 1,
    Columba I, Tucana IV and Segue 1. It would settle the short list and the 2σ fragility.
- **Walker [Mg/Fe] is low-resolution template fitting** on an APOGEE zero point, with 0.2–0.7 dex per-star [Fe/H] errors in the faint
  systems.
- **No dynamics, no binding, no catchment per satellite** (E6 Part D stands).

## Files and commits
- Criteria and ledger, committed alone first: 526a565dec.
- `p1_dwarf_chemistry.py` writes `p1_dwarf_chemistry.out`, `p1_dwarf_chemistry_results.json`, `p1_per_system.csv` and
  `p1_inventory.csv`. `--mutate` writes the `*_MUTATE.*` files. RUN1 is kept.
- One thread, nice 15, about 25 s. Max RSS 0.66 GB. Nothing was downloaded.
