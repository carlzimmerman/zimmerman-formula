# CFG903: the framework's own catalogue two-halo term for the KiDS isolated lenses. PARTIAL on both footings: it closes about 58% of CFG804's all-radii shortfall (+100.1 → +40.7 canonical, +123.1 → +52.8 alt), but not to the threshold, and the class is not robust

**What was done.**
- Every isolated lens in the record's reconstruction (I0 = `lr_lenses.npz`, 181,477 lenses, rebuilt exactly) gets a
  neighbour sum.
- **Neighbours:** every observed KiDS-bright galaxy within 4.61 Mpc (physical, projected) and |Δχ_phot| < 500 Mpc.
- **Mass of each neighbour:**
  - its own baryons, as a point mass;
  - its own framework catchment cold energy, 5.364 N M_b, with N from CFG902's declared fixed point;
  - the cold energy is laid out on CFG804's truncated law profile.
- **Stacking:** in B21's 15 bins with B21-like Σ_crit⁻² lens weights, minus the same sum around random clones placed off
  the mask.
- **Exclusion:** neighbours less massive than the lens are dropped inside the D model's own catchment edge. That edge is
  recomputed for every trial mass inside the fit. More massive neighbours (hosts) are kept.
- **Score:**
  - The two-halo term is added to CFG804/CFG902's one-halo D_der.
  - It is scored with CFG804's own χ², covariance and per-bin mass profiling (CFG804's script is exec'd read-only).
  - B stays CFG804's fixed reference, with nothing added.

**No free amplitude.**
- CFG805's two-halo term came from T1x's P_grav with a free bias per bin, and narrowed the pre-unit-fix +149 to +11.
- This lane's term is fixed by the catalogue and the framework's supply rule.

Criteria: `FROZEN_CRITERIA.md` (bb665cf4f, committed alone before any script).
- `AMENDMENT_A1.md` (26ecb00ce): completeness. Made before any pair or lensing computation.
- `AMENDMENT_A2.md` (a6449299a): kernel numerics. **Post hoc**: made after the first score run, whose numbers had been
  seen. Disclosed below.

## Result (all radii = CFG804's failing range; class threshold Δχ² ≤ 4; PARTIAL = at most half of CFG902's shortfall left)

| footing | CFG902, no two-halo | **CFG903, D_der + catalogue two-halo** | shortfall closed | class | primary R ≤ 0.31 Mpc | χ²(D+2h), p |
|---|---|---|---|---|---|---|
| canonical (9.3603e-11) | +100.10 | **+40.72** | 59% | **PARTIAL** (≤ 50.05) | −5.00, still SUFFICES | 203.9 / 56 dof, 1e-18 |
| alt (1.1312e-10) | +123.12 | **+52.80** | 57% | **PARTIAL** (≤ 61.56) | −7.19, still SUFFICES | 208.1 / 56 dof, 2e-19 |

- Footings are never pooled.
- Jackknife over 50 sky patches (delete-one, refit): σ(Δχ²) = 1.5 / 1.65. No class threshold is within 2σ.
- Profiled masses (log M_b): 10.38 / 10.82 / 10.96 / 11.18 (canonical), 10.26 / 10.76 / 10.89 / 11.10 (alt).
- Exclusion edges: 324 / 537 / 553 / 531 kpc (canonical), 256 / 456 / 516 / 491 kpc (alt).
- B itself fits poorly (χ²_B = 163.1 / 155.3). The absolute misfit is shared, as CFG805 found.

### What the two-halo term supplies against what the one-halo model leaves (canonical, Msun/pc², at the D+2h masses)

| R (Mpc) | 0.41 | 0.76 | 1.04 | 1.41 | 1.92 | 2.60 |
|---|---|---|---|---|---|---|
| bin 1: two-halo / data − D_1h | 0.32 / −0.94 | 0.31 / 1.34 | 0.28 / 0.89 | 0.20 / 0.51 | 0.11 / 0.21 | −0.10 / 0.19 |
| bin 2 | 0.46 / 2.31 | 0.44 / 0.87 | 0.38 / 1.59 | 0.30 / 0.53 | 0.19 / 0.33 | −0.04 / 0.09 |
| bin 3 | 0.49 / 0.69 | 0.41 / 1.12 | 0.38 / 1.63 | 0.32 / 1.00 | 0.20 / 1.20 | −0.01 / 0.39 |
| bin 4 | 0.32 / 1.33 | 0.25 / 0.98 | 0.30 / 1.54 | 0.29 / 1.54 | 0.21 / 0.73 | 0.03 / 0.52 |

- The catalogue two-halo is a smooth 0.2–0.5 Msun/pc² out to about 1.5 Mpc, and it turns slightly negative at 2.6 Mpc
  (the isolation hole).
- The data want 3–5 times more at about 1 Mpc.
- The **amplitude scan** (reported only) puts the best multiplier on the catalogue term at **A = 3.5 / 3.6**. Δχ² ≤ 4
  needs A between **1.9 and 5.2** (canonical) or **2.1 and 5.1** (alt).
- **Hosts dominate.** Of the unexcluded two-halo at 1.04 Mpc, 87% / 72% / 60% / 40% (bins 1–4) comes from neighbours more
  massive than the lens. These are hosts of lenses that are really satellites and leak through the photo-z isolation (the
  effect CFG502 measured).

## Brackets (one at a time from the primary; all-radii Δχ², class)

| bracket | canonical | alt |
|---|---|---|
| primary (I0, W500, C1′, P1, E1, unmasked, B21 weights) | +40.72 PARTIAL | +52.80 PARTIAL |
| C0, no completeness correction | +45.42 PARTIAL | +58.48 PARTIAL |
| C2′, whole neighbour sum scaled for completeness | +26.15 PARTIAL | +36.93 PARTIAL |
| W300 / W1000 photo-z window | +46.94 / +34.99 PARTIAL | +60.24 / +45.99 PARTIAL |
| **I1, f30 isolation (57,265 lenses)** | **+83.15 DOES NOT CLOSE** | **+100.40 DOES NOT CLOSE** |
| I2, physical 3 Mpc isolation radius (118,994) | +29.66 PARTIAL | +41.28 PARTIAL |
| I5, count-matched to B21 (W 6.1 Mpc: 259,963 vs B21's 259,383) | +30.58 PARTIAL | +41.28 PARTIAL |
| **P0, neighbour cold energy as a point** | **+55.03 DOES NOT CLOSE** | **+69.89 DOES NOT CLOSE** |
| P2, diffuse (law shape to 2× edge) | +49.86 PARTIAL | **+62.33 DOES NOT CLOSE** (0.8 above the line) |
| E0, no exclusion (double counts the lens's satellites) | +10.28 PARTIAL | +22.67 PARTIAL |
| **E2, all neighbours inside r_x dropped (hosts too)** | **+80.23 DOES NOT CLOSE** | **+96.79 DOES NOT CLOSE** |
| uniform lens weights | +41.21 PARTIAL | +53.21 PARTIAL |
| M1, masked-flag objects added as neighbours | +31.33 PARTIAL | +41.53 PARTIAL |
| W100 / W200 (reported only) | +72.24 / +54.22 DOES NOT CLOSE | +89.95 / +68.68 DOES NOT CLOSE |
| v7, lenses z ≥ 0.17 only (A1 diagnostic) | +40.39 | +52.16 |

**No bracket closes, on either footing.** The closest is E0 at +10.3 / +22.7, and it double counts.

**The class flips to DOES NOT CLOSE under:**
- stricter isolation (I1);
- point-like neighbour cold energy (P0);
- dropping the hosts inside the edge (E2);
- on alt only, the diffuse profile (P2).

So **PARTIAL is the primary class, not a robust one.**

## Reading

1. **The framework's own neighbours lens, and the term matters.** With no free parameter, the catalogue two-halo term
   removes 57–59% of the all-radii shortfall that CFG804/CFG902 left beyond the catchment edge. It also improves the
   primary range: SUFFICES gets stronger (+0.84 → −5.0 canonical, −0.27 → −7.2 alt).
2. **It does not close the outer-halo problem.**
   - The data want about 3.5 times the catalogue term.
   - Doubling every neighbour's baryons (the MUTATE, with N re-derived) still leaves +20.2 / +27.1.
   - No completeness, window, isolation, profile, mask or weight bracket reaches Δχ² ≤ 4.
3. **The direction of the remaining biases.**
   - Per-galaxy catchments are not shared (CFG522), which over-assigns supply in groups. Sharing can only lower it. So the
     primary is an upper bound in that respect.
   - Faint neighbours missing from the catalogue push the other way. The upper completeness bracket C2′ gives
     +26.2 / +36.9, still PARTIAL.
   - The most massive neighbours of lenses at z ≲ 0.15 are absent from the bright sample (nothing brighter than r ≈ 15.3;
     see A1). Restricting to z ≥ 0.17 lenses changes Δχ² by < 1 (v7).
4. **What the result depends on most.** It depends on how the isolated sample is defined and on where the hosts' cold
   energy sits:
   - most of the term comes from hosts of leaked satellites;
   - the stricter f30 sample loses most of the gain;
   - dropping the hosts inside the edge (E2) or shrinking their cold energy to a point (P0) removes it.

   B21's actual sample (259,383) is looser than the record's 181,477. The count-matched I5 gives +30.6 / +41.3.
5. Status of the outer-halo problem (no claim beyond this):
   - CFG804: SUFFICES inside 0.31 Mpc.
   - CFG902: the units fix (+100 / +123 all radii).
   - CFG903: the framework's catalogue two-halo term brings it to +41 / +53, PARTIAL. The remaining gap is a factor of
     about 2–5 in the two-halo amplitude, or something not attached to catalogued galaxies' catchments.

   Nothing here says the data favour the framework. B is not beaten.

## Controls (all PASS in the reported run)

| control | result |
|---|---|
| K0a: isolation rebuild = lr_lenses | 181,477 lenses; ra, dec, z, logM, Mgal, chi identical |
| K0b: I1 on I0 = cfg96 f30 | 57,265, identical |
| K0c: candidates | 605,531 (CFG502) |
| K0d: lens M_b in the neighbour pool = Mgal | rtol 1e-12 |
| K0e: completeness factors finite (A1 definitions) | f_C1′ 0–1.76, R_C2′ 1–2.47 |
| K1a: CFG804 exec'd with R1/R2 = CFG902's declared JSON | max \|Δ\| 0, both footings |
| K1b: this lane's D+2h fit with two-halo ≡ 0 = CFG902 | max \|Δ\| 0: +100.10 / +123.12 all radii, +0.84 / −0.27 primary |
| K2a: projected cold profile vs CFG804 `profile()` | 3.1e-4 (tolerance 5e-3) |
| K2b: kernel limits; off-centre F vs independent brute-force polar integration | 0; 6.7e-5 (tolerance 1e-3) |
| K2c: uniform neighbour field gives ΔΣ = 0 | 5.9e-5 Σ₀ (tolerance 2e-3) |
| K3: random halves A − B, 28 outer points | −0.0033 ± 0.0066 Msun/pc² (−0.5σ) |
| MUTATE: neighbour M_b × 2 (N, r_M re-derived) | +40.72 → +20.17 canonical, +52.80 → +27.13 alt. **Bites** (both still PARTIAL) |
| CFG804 and CFG902 directories | untouched |

The random-only term, the catalogue's mask and edge signal that the subtraction removes, is 0.15–0.21 Msun/pc² at
0.4–2.6 Mpc. That is comparable to the two-halo term itself, so the subtraction is essential. K3 shows the random
machinery itself is unbiased.

## Amendments and disclosures

**A1, before any pair or lensing number.**
- The frozen completeness reference slices (z_phot 0.10–0.12 and 0.06–0.08) contain no massive galaxies: none with
  log M★ ≥ 11 in 35,976. Nothing brighter than r ≈ 15.3 is in the bright sample.
- So the frozen C1 gave R_c of 17 at z = 0.4 and 106 at z = 0.5, and C2 was undefined (K0e FAIL).
- They were replaced by a complete-slab mass function, with:
  - C1′: up-weighting of the faintest observed neighbours (primary);
  - C0: none;
  - C2′: the whole sum scaled.
- First-run stage outputs are kept: `cfg903_stage_run1_K0e_fail.*`.

**A2, post hoc.**
- Run 1 failed K2a, K2b and K2c (1.15e-2, 3.2e-3, 1.7e-2) because of a lookup table that was too coarse, plus a fixed
  q grid. Its numbers had been seen: PARTIAL, +40.68 / +52.78, same flips.
- The kernel is now evaluated directly, with no table. Run 1's script and outputs are kept (`cfg903_score_run1*`).
- Run 1 → run 2: every Δχ² moved by ≤ 0.06, and no class changed. The kernel errors cancel against the randoms.

**Other disclosures.**
- **Not modelled:**
  - the true-z lensing efficiency of neighbours (correlated neighbours sit at the lens redshift; uncorrelated ones cancel
    against the randoms);
  - neighbour mass errors from photo-z;
  - the lens's own share of a host's catchment;
  - mass not attached to any catalogued galaxy's catchment;
  - correlated neighbours beyond 4.61 Mpc (P2 extents reach 2.1 Mpc for the rarest neighbours).
- The two-halo term is bin-averaged. The one-halo term stays point-evaluated, as in CFG804.
- Neighbour masses use the record's LePhare + 0.15 dex and f_cold recipe. f_cold is large below log M★ ≈ 8.5, but such
  neighbours carry little mass.
- The census f_ret is an observational input carried in the record, not derived (CFG804, CFG806).
- The one-halo masses stay profiled per bin (CFG804). The neighbours' masses are catalogue values. The profiled lens
  masses sit about 0.3 dex above the lens catalogue means; neighbours are not given that offset (MUTATE shows its size).
- B21's isolated sample is not public. I0 is the record's reconstruction, and I5 brackets B21's count.

**Compute.** One core, nice 10.
- Stage A: 13 s, at most 1.06 GB.
- Stage B: 8–18 s per bin, at most 0.81 GB, full samples (no subsampling).
- Score: 112 s, at most 0.49 GB. MUTATE: 25 s, at most 0.44 GB.

## Files and rerun

- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `AMENDMENT_A2.md`
- `cfg903_lib.py`: shared definitions.
- `cfg903_stage.py`: isolation, randoms, weights, completeness. Output → `cfg903_stage.out`, `cfg903_stage_results.json`.
- `cfg903_pairs.py BIN`: neighbour-pair histograms. Output → `cfg903_pairs_bin{1-4}.out`, `.json`.
- `cfg903_score.py`: kernels, fits, brackets, jackknife, K checks. Output → `cfg903_score.out`, `cfg903_results.json`.
  With `CFG903_MUTATE=1` it writes `cfg903_score_MUTATE.out` and `cfg903_results_MUTATE.json`.
- `cfg903_k1_cfg804exec{,_alt}.{json,out}`: CFG804 exec'd with R1/R2 (K1a).
- Large arrays live in `../../../_external_data/cfg903_work/` (not committed).
- Rerun from this directory, in this order:
  1. `OMP_NUM_THREADS=1 nice -n 10 python3 cfg903_stage.py`
  2. `... cfg903_pairs.py 1` (then 2, 3, 4)
  3. `... cfg903_score.py`
  4. `CFG903_MUTATE=1 ... cfg903_score.py`

κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10, never pooled; raw KiDS data, framework-native neighbours (no ΛCDM halo-model two-halo term); not theory closed.
