# CFG492: which objects are seen by several independent datasets on disk, and what does combining them decide?

On-disk data only; no downloads. Part A is an inventory and cross-match (`cfg492_inventory.py`). Part B runs the most decisive synthesis the overlaps allow (`cfg492_gc_vs_pn.py`). Its criteria, `FROZEN_CRITERIA.md`, were committed alone first (8bfa284dc).

Fixed throughout: kernel ν_mono, κ = ½ FITTED, both footings (9.36e-11 | 1.13e-10), never pooled.

## Bottom line
1. **High z (the a0(z) question): no on-disk overlap can bypass the gas-calibration wall.**
   - Only 2 objects meet CFG385's specification (AO inner + deep outer + measured gas): zC 400569 and zC 406690.
   - zC 406690's CO is integrated, with no resolved shape, so CFG400's lesson rules it out. Effectively N = 1, against the ≥ 10–20 needed.
   - The richer overlaps (27 objects with observed kinematics + measured gas + M*) carry one PSF-limited or one-radius velocity each. Per CFG385, that gives zero a0 information once each galaxy's calibration is free. With the calibration fixed, they inherit the α_CO/M* wall.
2. **Local discs (inner disc to lensing edge): not possible on the same objects.**
   - 1 SPARC galaxy is in the KiDS bright sample, and per-object lensing is far below noise. FP21's 2,036 stacked z ≈ 0.026 lenses gave S/N 0.1.
   - No dynamical (σ_z) disc mass is on disk: 1 SPARC galaxy is in the DiskMass parent sample, and the DiskMass masses themselves are not on disk.
3. **Clusters:** of the 12 X-COP clusters, 1 has weak lensing (A2142, two literature fits) and 8 have galaxy-dynamics masses (literature compilation and WINGS members). This is too heterogeneous for a decisive test; it is listed, not run.
4. **Early types: 8 galaxies carry three independent mass tracers.** Each has SLUGGS GC velocities, PN velocities and an ATLAS3D JAM inner anchor. No lane had ever read the PN files. **This is the synthesis that was run.**
   - **Frozen verdict: MASS PROPERTY on both footings.** The PNe on the same six paired galaxies show the same outer deficit as the GCs: D = PN − GC = +0.001 ± 0.031 dex (canonical) / +0.003 ± 0.031 (alt).
   - The PN offset alone is +0.105 ± 0.041 (2.6σ) / +0.096 ± 0.040 (2.4σ).
   - **The robust part is the agreement, not the PN significance.** The PN-alone 2σ fails under several attacks: leave-one-out (removing NGC 1023, 4374 or 5846), a ρ ∝ r⁻³ PN tracer, or a 2.5σ clip. D stays within ±0.035 in every variant.
   - **Reading.** The SLUGGS outer deficit is not a GC-tracer artefact. A starlight tracer on the same galaxies sees it too. It lives in the potential, or in the mass model that both tracers share (JAM-calibrated Hernquist stars, no gas). It is not a new detection: PN significance stays at about 2.5σ.

## Part A: inventory and overlap counts (`cfg492_inventory.out`, `cfg492_overlap_*.csv`)
**Match rules (stated in the script before counting):**
- High z: alias-normalised names, or ≤ 1.0″ with |Δz| ≤ 0.01(1+z), joined by union-find.
- Local: SPARC names, or ≤ 30″ with |Δcz| ≤ 300 km/s.
- Early types: NGC number.
- Clusters: name, or ≤ 3′ with |Δz| ≤ 0.01.

**MUTATE (+60″ in Dec):** high-z coordinate edges drop from 937 to 3. The remaining overlaps are name matches, as designed.

### High z (22 catalogues; ALMA archive rows = coverage only, not counted as a source)
| combination | objects |
|---|---|
| in ≥ 2 catalogues | 285 |
| ≥ 3 / ≥ 4 catalogues | 60 / 22 |
| kinematics + measured gas + M* (any kinematics / observed, not model-only) | 29 / 27 |
| kinematics + ALMA archive coverage only (gas not yet measured) | 49 |
| two kinematic tracers (CO/[CII] with Hα or a model) | 14 |
| AO/JWST inner + deep outer | 4 |
| **AO/JWST inner + deep outer + measured gas (CFG385 spec)** | **2** (zC 400569, zC 406690) |
| deep outer + measured gas + M* | 4 (+ KURVS 12, 22 with GOODS-ALMA dust) |

**Richest objects (≥ 5 catalogues):**
- **Q2343-BX610:** ALPAKA CO, PHIBSS13 CO, RC100/RC41, SINS seeing-limited + AO.
- **K20-ID7 / K20-ID6 / GMASS-2363 (= GS4 42930):** KMOS3D fit, SINS AO, RC100/RC41. No measured gas.
- **zC 406690:** Genzel+17 deep curve, SINS AO, PHIBSS13 CO, RC100/RC41.
- **zC 400569:** Genzel+17 deep curve, SINS AO, Lelli+23 CO/[CI], RC100/RC41.
- **D3a 6397, D3a 15504:** Genzel+17, SINS AO, RC100/RC41. No gas.
- **BX389, BX482:** PHIBSS13 (an upper limit for BX389; BX482's CO is the companion's, per CFG196).

**Not previously cross-matched; found here:**
- ACE CO(3–2) × our KMOS3D cube fits: 7 discs at z 2.1–2.5 (COS4_03324, 05094, 06750, 08515 = zC 410041, 13701, 24763, 25229).
- GOODS-ALMA 1.1 mm × KMOS3D fits: 6.
- PHIBSS2 × ALPAKA: 1 (XV53).

All are single-point kinematics, so they do not bypass the wall (see the bottom line). RC100, RC41, Genzel+17 and our KMOS3D fits re-use the same Hα cubes, so they are not independent kinematics.

### Local discs (SPARC reference, 175)
| SPARC × | matches | supplies |
|---|---|---|
| ALFALFA a100 × SDSS | 47 | independent HI flux and width, M* |
| UNGC | 68 | TRGB/Cepheid distances, L_K |
| CF4 | 175 (positions; distances in table2) | distances |
| S4G | 105 | 3.6 µm morphology |
| LITTLE THINGS | 9 | independent HI curves (CFG442 used them: +0.196 dex overlap failure) |
| Di Teodoro+23 / WALLABY DR2 kin / xGASS | 1 / 1 / 1 | |
| DiskMass sample / DMS XI | 1 / 0 | σ_z disc masses NOT on disk |
| KiDS bright | 1 | per-object lensing unmeasurable |
| MIGHTEE DR1 / ATLAS3D | 0 / 0 | |

11 SPARC galaxies have a second, independent rotation curve.

### Early types (by NGC)
| combination | N | galaxies |
|---|---|---|
| GC + PN + JAM | **8** | 821, 1023, 3377, 3608, 4374, 4494, 4564, 5846 |
| GC + X-ray (Humphrey) | 3 | 720, 1407, 4649 |
| GC + PN + X-ray | 0 | |
| HI ring + JAM | 15 | (den Heijer+15) |

### Clusters (X-COP reference; the json also carries Hydra A)
| combination | N |
|---|---|
| X-COP × lensing (WL, Groener+16 compilation) | 1 (A2142), +Hydra A |
| X-COP × galaxy dynamics (LOSVD/caustic/WINGS members) | 8 |
| X-COP × lensing × dynamics | 1 (A2142) |
| X-COP × PSZ2 / eRASS1 (≤ 3′) | 11 / 5 |

## Part B: same-galaxy GC vs PN (`cfg492_gc_vs_pn.out`, `_results.json`)
Paired N = 6: NGC 821, 1023, 3377, 4374, 4494, 5846. NGC 3608 and 4564 have too few clean GCs and are reported as PN-only rows: +0.150 and +0.042.

**Setup.**
- The mass model and the GC side are the audit's code path. C1 reproduces AUDIT_SLUGGS to 0.00000 dex.
- The PN tracer density is the Hernquist starlight profile. The Jeans solver was checked analytically after the freeze (D1: 8e-6 dex).

| galaxy | O_GC | O_PN | Δ |
|---|---|---|---|
| NGC 821 | +0.142 ± 0.044 | +0.055 ± 0.032 | −0.087 |
| NGC 1023 | +0.104 ± 0.031 | +0.193 ± 0.020 | +0.089 |
| NGC 3377 | +0.064 ± 0.024 | +0.010 ± 0.038 | −0.055 |
| NGC 4374 | +0.201 ± 0.072 | +0.219 ± 0.020 | +0.017 |
| NGC 4494 | −0.103 ± 0.037 | −0.013 ± 0.022 | +0.090 |
| NGC 5846 | +0.213 ± 0.021 | +0.165 ± 0.033 | −0.048 |

Values are canonical, in dex, with per-galaxy bootstrap errors.

**Summary statistics.**
- r(O_GC, O_PN) = +0.76.
- Centrals (4374, 5846): GC +0.207, PN +0.192.
- Non-centrals: GC +0.052, PN +0.061.

**MUTATE (shuffled PN–galaxy pairing).** rms(Δ) rises from 0.070 to 0.332 and the verdict becomes UNDECIDED. The pairing carries the information, so the MUTATE fires.

**Post-freeze attacks** (`cfg492_postfreeze_diag.out`, labelled):

| attack | effect |
|---|---|
| D2: ρ_PN ∝ r⁻³ | M_PN +0.071 (1.7σ), D −0.033 |
| D2: ρ_PN ∝ r⁻³·⁵ | M_PN +0.102, D −0.001 |
| D3: leave-one-out | M_PN 1.94–3.15σ; below 2σ without 1023, 4374 or 5846; D within ±0.02 |
| D4: 2.5σ clip | M_PN +0.068 (NGC 3377 −0.077, NGC 5846 −0.054) |
| D5: matched radii | D +0.006 ± 0.035 |

**What it decides.**
- **Decided: TRACER SYSTEMATIC is disfavoured.** If the PNe showed no deficit, D would be about −0.10, which is excluded at about 3σ (σ_D 0.031). This holds in every variant.
- **Not decided: whether the shared deficit is a law failure.** It could also be the shared mass model: Hernquist shape, no hot gas (CFG323's measured gas barely moved the GC offset), rotation counted in σ, or distances. Any of these moves both tracers together, so D cannot see them.

The PN-alone significance (2.4–2.6σ) is a lean, not a detection.

**Expected power (frozen).** About 1.4σ for a full removal of the deficit. The realised σ_D (0.031) is better than forecast because the paired offsets correlate.

## Needs owner go (downloads that would make the other syntheses decisive)
- **High z:** AO/JWST inner + deep outer + resolved CO for ≥ 10 discs. The Genzel+20 RC41 curves (arXiv:2006.03046) and Übler/NOEMA3D resolved CO maps are figure-only. New ALMA products exist for COS4_05433 and GS4_45068 (CFG403); the KMOS3D–ALMA overlaps with archive coverage only are listed (49).
- **Local:** DiskMass σ_z disc masses (Martinsson+13, DMS VI/VII tables). They would put a stellar-dynamical M* under 1 SPARC galaxy, and under all DMS XI discs once those discs have HI curves.
- **Early types:** Chandra deprojected gas profiles for the 8 GC+PN galaxies. That would add a third tracer and the hot-gas mass the shared model lacks. ePN.S survey PN catalogues for the other SLUGGS galaxies would give N > 6.
- **Clusters:** per-cluster weak-lensing profiles for the X-COP clusters (e.g. Herbonnet+20 or LoCuSS), for a hydrostatic-bias test on the same clusters.

## Files
- `FROZEN_CRITERIA.md`
- `cfg492_inventory.py`, `.out`, `_results.json`, `_MUTATE.*`, `cfg492_overlap_{highz,sparc,etg,clusters}.csv`
- `cfg492_gc_vs_pn.py`, `.out`, `_results.json`, `_MUTATE.*`
- `cfg492_postfreeze_diag.py`, `.out`, `_results.json`

**Runs:**
- `python3 cfg492_inventory.py` (1 s) and `MUTATE=1 …`
- `python3 cfg492_gc_vs_pn.py` (9 s, rc 0, 4/4 checks) and `MUTATE=1 …` (rc 0, 5/5)
- `python3 cfg492_postfreeze_diag.py`; it re-runs the main script internally, and the main outputs stay byte-identical.

κ = ½ is fitted. Never cite this as a framework win.
