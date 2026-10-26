# IJ1_isothermal_jeans_halos — RESULT: IJ FAILS (both footings); the BU1 cross-section gives cores too small to matter, so IJ ≈ the outer NFW

Frozen criteria + ledger **46979ae8db** (committed alone). **AMENDMENT A1** f98a1b0072 (memory chunking only; committed after
run 1 had printed canonical PRIMARY SPARC / cluster / group lines). **AMENDMENT A2** 3c7e2ea891 (the variant moved to its own
invocation; committed after PRIMARY). κ = ½ FITTED. Footings computed and graded separately, never pooled. Cold dark energy,
not matter. Nothing here says the data favour the framework or ΛCDM. Not "theory closed". One thread; nothing downloaded.

**Provenance.** The edits made before any graded number:
- P4's kpc constant;
- the isothermal series start in `ij1_lib.py`;
- a `KeyError` fix in loading GR1's helper names.

In those runs only K2 / K0 / K4a had printed. Run 1 then printed canonical PRIMARY SPARC, clusters and groups, and was stopped
on memory (A1). The A1 rerun's PRIMARY lines equal run 1's printed digits. The final normal run (after A2) reproduces the A1
rerun's PRIMARY lines exactly (diffed). The A1 rerun's full log is kept as `ij1_isothermal_jeans_A1rerun_STOPPED.out`. Its
`_PARTIAL` files were deleted by mistake; the log holds every line they held.

## Hypothesis IJ

The standard isothermal-Jeans halo replaces OS1's fixed Burkert core:
- **Inside r₁:** isothermal σ₀ in the total potential (cold dark energy + baryons).
- **Outside r₁:** EM1's NFW (Bullock c, M200(M_b)).
- **r₁:** where ρ s v t = 1, with BU1's fully fixed s(v) = 0.155 / 0.106 cm²/g at 159 km/s.
- **Matching:** ρ and M continuous at r₁.

PRIMARY has zero free parameters. The solver uses the exact Lane–Emden cored branch, continued in baryon strength by 2-D
Newton (`ij1_lib.py`).

## Result (PRIMARY, `ij1_isothermal_jeans.out`)

| class | canonical | alt | OS1 / GR1 reference | class (both) |
|---|---|---|---|---|
| SPARC A rms @ median Υ (B) | 0.0654 @ **0.37** (0.0653 @ 0.36) | 0.0657 @ **0.37** (0.0656 @ 0.36) | 0.0605 @ 0.79 / 0.0591 @ 0.63 | **FAILS** (Υ leg) |
| clusters (15 cells) | **14 fail**, all over-predicted ~1.5–3×; G-IN-Mall Z −3.48; OUT-all −7.4; MID T3 −4.8 | same 14 | 14/15 pass | **FAILS** |
| groups (63) | mean +0.0686, Z +1.64, CONSISTENT | same | Z +1.94 / +1.85 | **PASS** |
| SLUGGS centrals | mean **+0.168**, 1/4 cleared | +0.168, 1/4 | +0.127 | **FAILS** (worse than OS1) |
| dwarfs (89) | frac_up 0.607, median S 3.99, frac_over 0.03 (CD1: EXCLUDE) | 0.607, 3.97, 0.03 | 0.652 / 0.483 | **FAILS** |

Motivating targets on both footings:
- T-IC (INNER band): not met; INNER is now over-predicted more than OS1.
- T-GR (SLUGGS): not met.
- T-DW (dwarfs): not met.

**Lane class: IJ FAILS on both footings (verdict IJ FAILS).**

Solved scales (medians):

| system | r₁ | σ₀ |
|---|---|---|
| SPARC | 3.0 / 2.1 kpc | 53 / 50 km/s |
| groups | ≈ 10 kpc | 149 / 143 km/s |
| SLUGGS | 9–11 kpc | 210–300 km/s |
| clusters | 25–31 kpc | 330–380 km/s |
| dwarfs | 0.15 / 0.07 kpc (0.53 / 0.22 r₁₂) | ≈ 3 km/s |

Every λ = 0 problem had a single cored root.

**Checks 5/7:**
- K0 PASS: the solver vs IC1's Lane–Emden table, 5e-8; own table identical.
- K1 PASS: independent LSODA matching on 128 lanes, 8.5e-5 ≤ 1e-4.
- K2 PASS: s(v) vs BU1, 7e-16.
- K4 PASS: OS1 cells, GR1 groups / SLUGGS, OS1 dwarfs and EM1 c(M) reproduced.
- **K3 FAIL:** 1 of 89 alt dwarfs had no λ = 0 root (1.1 % > 1 %); it is graded with its pure NFW, as frozen.
- **K5 FAIL:** peak RSS 1.28 GB > 1 GB.

**MUTATE** (baryons removed from the Jeans potential, `_MUTATE`): **the tooth does NOT bite.** SLUGGS moves ≤ 0.0002 dex and
G-IN-Mall moves 0.00 %. So, as frozen, **baryons do not control the graded IJ cores.** Exit 0 as frozen; checks 3/5 (MUT FAIL,
K5 FAIL).

## Reported only

- **Pure NFW (no core)** gives SPARC 0.0659 @ 0.37 (EM1's own R1 NFW row: 0.0656 @ 0.36), the same 14 cluster fails (G-IN-Mall
  −3.48), the same groups and the same dwarfs. **The IJ core changes almost nothing graded.** IJ is the outer NFW.
- **Clusters with OS1's fair-share mass** (5.364, ΛCDM-derived, comparator only): 13 fail (G-IN-Mall −3.14, OUT-all −6.2). The
  over-prediction is not the EM1 mass relation alone. It is the cuspy, concentrated NFW mass profile carried to r_ta, compared
  with X38's compact Burkert holding the same mass.
- **No BCG:** G-IN-Mall prediction identical to 4 decimals. A 6e10 M☉ BCG cannot reach a 25 kpc core's effect at ≥ 150 kpc.
- **Dwarfs by class** (canonical, median S): MW ultra-faints 10.1, MW classicals 3.1, bright M31 2.3, LG field 1.5. EM1's
  relation extrapolated to M★ ~ 10⁵–10⁷ gives halos far too light. That is the M200(M★) input, not the core.
- **Variant** (s amplitude once on SPARC, n kept): **still running** (A2; one child process per SPARC evaluation; about 10 min
  each at large amplitude). So far the SPARC A rms is flat to noisy, 0.0644–0.0674 at Υ 0.37–0.44, for log₁₀ A from −2 to
  +1.3. No amplitude reaches the Υ ≥ 0.50 leg yet. The variant result will be added to this README and committed when it
  lands. It is reported only, never class-setting.

## What it means

1. **With the record's own cross-section, the isothermal-Jeans core is inert.** BU1's s ≈ 0.02–0.15 cm²/g puts r₁ well
   inside the NFW scale radius: about 3 kpc in galaxies, about 10 kpc in groups and ellipticals, and 25–30 kpc in clusters.
   In clusters that is inside every graded band (≥ 150 kpc). In SPARC it covers only the inner points, and moves rms by
   0.0005 against the pure NFW. Each class therefore grades essentially the outer NFW, and NFW with Bullock c fails as
   EM1 / IC1 found:
   - SPARC wants cores (Υ falls to 0.37);
   - clusters are over-concentrated;
   - SLUGGS centrals get more halo mass at r₁₂, so the JAM-analogue M★ drops and the offset grows.

   The isothermal construction cannot rescue a halo whose matching radius sits inside the region being tested.
2. **The three IC1 / GR1 / OS1 misses are not addressed by this route at fixed s.** OS1's successes came from a posited
   compact Burkert that ties the core to a₀ / (2πG). They did not come from a self-interaction scale that dynamically
   produces such a core. With s fixed by the same core law (Γt = 1 at the anchor), the dynamical cores in clusters
   come out ~10× smaller in radius than X38 / OS1's Burkert r₀ (0.27–0.44 Mpc). In galaxies r₁ is comparable to the Burkert
   r₀ (≈ 5 kpc), but it sits on a cuspy NFW, so the core is shallow.
3. **Baryons cannot deepen these cores in the graded bands** (MUTATE does not bite; the BCG has no effect). The "baryons
   deepen the cores" mechanism needs r₁ comparable to the graded radii.
4. **Inherited ΛCDM leaks** (NFW, Bullock c, EM1's M200 relation, X30's `DA_lcdm`): flagged as OPEN in the ledger. The
   failure is largely the outer NFW's, so this lane is also a test of those borrowed inputs. It is not evidence about
   cold dark energy cores as such.

## Files

| file | content |
|---|---|
| `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `AMENDMENT_A1.md`, `AMENDMENT_A2.md` | criteria, ledger, amendments |
| `ij1_lib.py` | isothermal-Jeans solver (vectorised Lane–Emden init + λ-continuation Newton) |
| `ij1_isothermal_jeans.py` | lane script (normal / `--mutate` / `--variant` / `--sparc-eval`) |
| `ij1_isothermal_jeans.out`, `_results.json` | PRIMARY + reported + checks |
| `ij1_isothermal_jeans_MUTATE.out`, `_results_MUTATE.json` | control |
| `ij1_isothermal_jeans_A1rerun_STOPPED.out` | A1 rerun log (stopped during the variant; A2) |
| `ij1_variant_sparc_cache.json` | variant SPARC evaluations so far |
| `ij1_x30_machinery*.log` | X30 machinery logs (gitignored, local only) |

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ij1_isothermal_jeans.py            # ~15 min, exit 1 (K3, K5 fail)
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ij1_isothermal_jeans.py --mutate   # ~2 min, exit 0 (tooth does not bite)
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ij1_isothermal_jeans.py --variant  # hours (reported only)
