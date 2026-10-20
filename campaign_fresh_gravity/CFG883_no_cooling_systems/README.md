# CFG883 — do systems that never cooled their own gas carry the CFG877 cold clump?

Criteria: `FROZEN_CRITERIA.md` (986230665, committed alone before the script; owner block 880–889). Run:
`OMP_NUM_THREADS=1 python3 cfg883.py` (`CFG883_MUTATE=1` → clump injected into the data, `_MUTATE` outputs). A few seconds,
numpy only. κ = ½ fitted; ν_e; footings never pooled; not theory closed.

**Hypothesis under test** (CFG878 Part C, route 2; post-hoc candidate): each faint dwarf carries one bound cold-energy clump
(σ_x 7.53 km/s, M_cl 5.25e6 M_⊙ canonical / 4.24e6 alt, r_c 104 pc; CFG877) because it formed as one of the first systems
able to cool gas by atomic hydrogen. **Kill prediction:** globulars, tidal dwarfs, collision debris and UCDs/stripped nuclei
carry no clump.

## Which systems can say anything at all
The clump is diffuse: its central density is only ~0.6 M_⊙/pc³, and inside r ≪ 104 pc it holds M_x ≈ 2σ_x² r³/(G r_c²)
(~300 M_⊙ inside 5 pc, ~2e4 inside 20 pc, ~1e5 inside 40 pc). It is visible only where the system's own mass inside the tracer
radius is ≲ 1e5 M_⊙ and the tracers reach ≳ 15–20 pc. Diagnostic power is the Asimov Δχ²_A (data := the no-clump prediction);
≥ 9 counts.

| class | data in the repo | diagnostic? |
|---|---|---|
| **Globulars** | Baumgardt measured σ profiles (145 clusters with RV bins) + CFG332's four | **yes, for 13 diffuse outer-halo clusters** |
| Tidal dwarfs (Lelli+2015, 6) | V_c at R_out 2.6–7.7 kpc | **no**: clump adds V_x ≈ 1.5–3 km/s in quadrature to 15–37 km/s; Δχ²_A ≤ 1.5e-3 |
| UCDs / compact Cen A + Sombrero objects (LVD: KV19-212/271/329/442, SUCD1) | global σ, r_h 4–16 pc | **no**: Δχ²_A ≈ 0.00 (clump term 0.3–1.2 km/s against 12–25 km/s) |
| Fluffy (Cen A, r_h 30 pc) | σ 5.89, no error (20 % used) | no (Δχ²_A 0.19); its class (cluster or dwarf) is unknown anyway |
| NGC 1052 trail DF2/DF4/DF9 (CFG655 inputs) | global σ | **no**: Δχ²_A ≤ 0.008 |
| NGC 5557 E1 (CFG448) | no resolved kinematics | no data |
| Open clusters (Hunt+2024) | PM dispersions | not run: the binary floor (~0.55 km/s, hunt_2026) and super-virial dispersions are the size of the clump term (0.2–0.6 km/s); needs its own lane |

So **only globular clusters test the prediction.** Tidal dwarfs, UCDs and the NGC 1052 trail are NOT DIAGNOSTIC, by factors
of ≥ 10³ in Δχ².

## Result — CLASS: **MIXED** (both footings)
T1 primary: isotropic Jeans, King tracer matched to the catalogue rh_l and rt, Newton baseline (the record's class E), Υ_V
1.6 ± 0.15 dex profiled, 5 % floor, 31 tidally safe clusters (R_GC ≳ 15 kpc).

| cluster | R_GC (kpc) | RV stars | outermost bin: R (pc), σ_obs / Newton / clump term (km/s) | Δχ²_A | Δχ² (can / alt) | class |
|---|---|---|---|---|---|---|
| Pal 14 | 68.5 | 16 | 27.5: 0.71 / 0.54 / 2.34 | 41.5 | **+26.8 / +26.5** | **NO CLUMP** |
| Pyxis | 38.6 | 43 | 34.3: 0.87 / 0.62 / 2.40 | 51.1 | **+19.7 / +19.4** | **NO CLUMP** |
| NGC 5466 | 16.5 | 68 | 32.3: 1.07 / 1.11 / 1.80 | 14.6 | **+16.7 / +16.5** | **NO CLUMP** |
| NGC 5024 | 19.0 | 338 | 55.1: 2.24 / 2.26 / 3.11 | 22.6 | **+13.8 / +13.5** | **NO CLUMP** |
| NGC 5053 | 18.0 | 55 | 26.1: 1.12 / 1.04 / 1.85 | 16.4 | **+12.9 / +12.6** | **NO CLUMP** |
| Ter 8 | 20.4 | 73 | 24.6: 1.24 / 1.14 / 1.95 | 15.5 | **+10.3 / +10.2** | **NO CLUMP** |
| NGC 1851 | 16.7 | 6520 | 74.4: 2.35 / 1.41 / 2.52 | 17.7 | **−18.5 / −18.5** | **CLUMP PRESENT** |
| Pal 5 | 17.3 | 39 | 36.3: 1.12 / 0.36 / 1.26 | 57.7 | −13.0 / −13.1 | CLUMP PRESENT (binary-vulnerable) |
| Pal 13 | 24.6 | 20 | 5.0: 0.99 / 0.37 / 0.98 | 20.4 | −12.6 / −12.6 | CLUMP PRESENT (binary-vulnerable) |
| Pal 3 | 98.2 | 22 | 11.1: 1.70 / 0.76 / 1.52 | 14.7 | −9.3 / −9.3 | CLUMP PRESENT (binary-vulnerable) |
| NGC 1261 | 18.3 | 345 | 35.4: 2.25 / 1.88 / 2.44 | 11.8 | −3.0 / −3.1 | UNDECIDED |
| NGC 5694 | 29.2 | 136 | 38.9: 2.52 / 2.11 / 2.92 | 11.5 | +3.6 / +3.5 | UNDECIDED |
| NGC 2419 | 95.9 | 183 | 91.6: 1.64 / 2.39 / 4.56 | 36.5 | +76.8 / +74.3 | MODEL INADEQUATE (both models fail; not counted) |

Columns show the canonical footing; alt differs by ≤ 2 % in every number. The other 18 tidally safe clusters are NOT
DIAGNOSTIC (Pal 4: Δχ²_A 9.0, just short, Δχ² +11.8; Crater 7.3, −5.6). The Newton and clump columns are at Υ = 1.6.

**Reading.**
- **Six diagnostic globulars exclude the clump** at Δχ² +10 to +27, on both footings. In Pal 14, Pyxis and NGC 5466 the clump
  term alone already exceeds the measured σ (Υ-free floor χ² 26.6, 20.1, 10.2). That holds for any stellar M/L. Binaries can
  only inflate σ, so they cannot fake these exclusions. A universal clump in every old stellar system is therefore excluded;
  globulars, as the hypothesis needs, carry none.
- **One cluster prefers the clump robustly: NGC 1851** (Δχ² −18.5, 6520 stars). The preference comes only from the outer bins
  (9–74 pc), where σ falls more slowly than the isotropic King–Newton shape. Even with the clump the fit is χ² 42 for 22 bins.
  *(Post-hoc, not used in the class:)* this is the classic outer σ flattening that the globular-cluster literature attributes
  to potential escapers. NGC 1851 also has a documented extended stellar halo and is discussed as a possible stripped
  nucleus. No test here separates those readings from a clump.
- **Three small-N clusters prefer it but are binary-vulnerable:** Pal 3, Pal 5 and Pal 13, with 20–39 stars. Pal 3's excess is
  the one CFG334 reproduces with ordinary binaries in 26 % of draws. Pal 5 is tidally disrupting.
- **Frozen rule:** 1 robust CLUMP PRESENT is fewer than 6 NO CLUMP → **MIXED**, not KILLED.

## T2 (CFG332's four, Wolf estimator; agrees in sign with T1)
Newton baseline, canonical (alt within 0.01 km/s and 0.2 in Δχ²):
- **Pal 14 NO CLUMP**: Δχ² +23.5. The clump term 2.05 km/s against σ_obs 0.71 ± 0.16.
- Pal 3 CLUMP PRESENT (binary-vulnerable): −9.8.
- Pal 4 NOT DIAGNOSTIC: Δχ²_A 4.4, but Δχ² +6.9.
- NGC 2419 NOT DIAGNOSTIC: 0.1.

Under the law+EFE baseline all four are NOT DIAGNOSTIC: the baseline already over-predicts, though Pal 14's Δχ² is still +23.

## Variants (reported, not deciding; all MIXED on both footings)
| variant | diagnostic | NO CLUMP | CLUMP PRESENT robust / vulnerable |
|---|---|---|---|
| all R_GC, no tidal cut (145) | 15 | 6 | 2 (NGC 1851, NGC 3201 at 8.9 kpc) / 3 |
| all bin types (PM bins as σ_los) | 12 | 6 | 2 (NGC 1851, NGC 1261) / 3 |
| floor 0.10 | 10 | 5 | 1 (NGC 1851) / 2 |
| Plummer tracer | 10 | 5 | 1 (NGC 1851) / 2 |
| law+EFE baseline | 6 | 2 | 1 (NGC 1851) / 0 |

Pal 14 is the one cluster the King solver cannot match: R_h/rt = 0.60, above the King maximum of 0.454. Per the criteria it
used Plummer. With the most extended truncated King instead (every star inside rt) it is still NO CLUMP (Δχ² +10.8 / +10.6).

## Controls
- **K1 PASS:** T2's Newton σ reproduces CFG820's printed values (max |diff| 0.004 km/s).
- **K1b PASS:** M_x(∞) = CFG877's M_cl, and the cap scale equals CFG877's r_t (rel ≤ 2e-16).
- **K2 PASS:** the Jeans code against the analytic Plummer σ_los, max deviation 1.5e-5.
- **K3 PASS:** King projected R_h = rh_l to 2.3e-4 over 144 clusters; 1 Plummer fallback (Pal 14).
- **MUTATE (clump injected into every σ) → overall KILLED on both footings**, with sum Δχ² −267 (was +47). No NO CLUMP
  survives: of the 6, four flip to CLUMP PRESENT and two to UNDECIDED.
  - **The frozen "≥ 80 % CLUMP PRESENT" requirement FAILED, kept: 10/13 = 77 %.** NGC 2419, NGC 5053 and Ter 8 read
    UNDECIDED. Their measured σ already sits at or below the Newton prediction, so the injected data land between the two
    models.
  - T3 stays NOT DIAGNOSTIC, as required.

## Disclosures
- **Pre-freeze hand estimates** were made for Pal 14, Pal 4, Pal 3 and NGC 2419 (listed in the criteria). Pal 3 was kept, with
  the binary flag.
- **Two numerical bugs were fixed after the first run.** Neither is a rule change.
  - The King solver's upper bracket (1e3 rt) hit float cancellation and sent 26 clusters to the Plummer fallback. It is now
    30 rt, and only Pal 14 falls back.
  - The K3 check started its projection at 1e-3 rt and missed core light in concentrated clusters. That check failed at 29 %;
    it now passes.
  - The first run's class was the same: MIXED, 6 NO CLUMP, 1 robust CLUMP PRESENT (NGC 1851), 3 binary-vulnerable.
- **Weak novelty for globulars:** the record already holds them Newtonian (CFG332, CFG820). The NO CLUMP results are what the
  hypothesis needs, but they do not single out the first-cooling story. Any rule that keeps clumps out of globulars passes.
- **What could fake NO CLUMP:**
  - radial anisotropy in the outskirts, which lowers the clump's σ_los term;
  - tracers more truncated than the catalogue rt;
  - clump stripping at pericentres smaller than the assumed R_GC/3 (current R_GC only);
  - the ~10 % low bias of small-N σ estimators (CFG334 C2).
- **What could fake CLUMP PRESENT:** binaries, escapers near rt, and tidal heating (Pal 5).
- **Stripped nuclei.** Massive clusters are non-diagnostic, so the possible-nucleus caveat matters only for NGC 1851 and
  NGC 2419. NGC 2419 is inadequate under isotropy, but its outer bins sit far below the clump term alone (floor χ² 62).
- **Not modelled:** EFE on the clump; mass segregation; rotation.
- **Other limits:**
  - The 20 % σ error for KV19/Fluffy follows CFG877's convention.
  - The "cap radius" printed is CFG877's asymptotic G M_cl/V_x² (199 pc). Per the CFG877 audit the coded profile reaches M_cl
    at 237 pc. This is irrelevant here: every T1 bin is at ≤ 92 pc.
- **Not established:** that the framework explains DF2/DF4/DF9. Their label is external (CFG655/CFG768); here they are only
  NOT DIAGNOSTIC for the clump.
