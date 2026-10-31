# RF1_mw_halo_free_baryons: FROZEN CRITERIA (committed alone with ASSUMPTION_LEDGER.md, before any script or RF1 number)

Written 2026-10-31 under THEORY_PROGRESS_SUMMARY_2026-10-31.md section 3 and section 4 (RF1), and the owner decision
`OWNER_DECISION_2026-10-31_NO_FLOOR.md`. κ = ½ FITTED. Footings graded separately, never pooled. Cold dark energy is a
gravitating field component, never a particle. Not "theory closed". No download; no web look-up.

**Disclosed first.** I have read GD1, GD2, GD3, X5 and RG1's log for P2 (X5 box, native N, 7 cells, FEASIBLE (WIDE PRIORS
ONLY), best at R_d 1.933). I have searched the repository: **no value of Kent 1992, Dwek+95 or pre-M2M clump-giant
bulge mass is on disk, and no HI/H₂ radial survey table is on disk.** So I expect the headline below to be UNDETERMINED
before running anything. The numbers that are new here are the bracket rows and the lookup.

## Question

Does route E miss V_c(R₀), K_z(R₀, 1.1 kpc) and the Ou+24 curve when the baryons carry no halo in their derivation?

## Rules graded (no free number)

- **OS1:** Burkert, ρ₀r₀ = Σ_a₀ (σ/σ_ref)^q_f, Σ_a₀ 106.879 / 129.165 M☉ pc⁻², σ_ref 70.50, q_f 0.892 / 0.748. PRIMARY
  V_last 172.98, VARIANT V_last 229.05 (own row, as GD2).
- **Native N (working rule):** smooth core, S_cold(M200) = f_c η(M_t) ρ(M_t) Σ_coll(M_t), M_t = M200/f_c, built once from
  ND1's `RULE_NAT` (ND1 commit 73805754b6). No a₀, so the footings coincide; shown once, with a check that they do.
  RG1 is another session's lane and is not edited or imported. Its P2 number is quoted for comparison only.
- M200 from EM1's R1 relation at the cell's baryon mass, as GD2. Background A PRIMARY, B reported on the same row.

## Baryons

Family: X5's (`x5_lib.Family`), Newtonian solve as GD2.

| axis | values | class |
|---|---|---|
| Σ_b(R₀) | X5's 5 values, 47.1 ± 2σ(3.4), McKee+15 | LITERATURE-INPUT, no dynamics |
| R_d | X5's 7 values, 2.6 ± 2σ(0.5), BH&G16, one R_d for both discs; LN16 tag 2.38–2.90 carried | LITERATURE-INPUT |
| gas | **PRIMARY: McKee's 13.7 M☉ pc⁻² at R₀**, on McMillan's HI and H₂ radial forms; stars = Σ_b − gas | column LITERATURE-INPUT; radial forms held, labelled |
| M_bb | **no halo-free value on disk.** BRACKET: X5's 5 Portail+17 values | ΛCDM-PROCESSED, PROVISIONAL |

## Rows

- **Halo-free bulge rows.** One row per candidate: Kent 1992, Dwek+95, pre-M2M counts, each with its M/L assumption. A
  row is usable only if its value and M/L are read from the paper or its TeX on disk. Memory is never a source. The
  script holds this as a list (`HALO_FREE_BULGE`), empty at this commit, with the reason per candidate.
- **BRACKET rows (never graded).** 175 cells on Portail's M_bb: GD2's classes, cell counts, and fractions of the whole
  box and of the cells inside both LN tags. Per rule, footing, V_last, background.
- **LOOKUP (DIAGNOSTIC, not a prior).** M_bb ∈ {0.5, 0.8, 1.0, 1.3, 1.64, 1.88, 2.12, 2.5, 3.0} × 10¹⁰ M☉ against the 7 R_d:
  how many of the 5 Σ_b pass all four lines. This lets a value read later be graded without new machinery. It selects
  nothing and is not a scan for a passing mass.
- **Sensitivity (on the BRACKET box, reported):** gas ±2σ of McKee (13.7 ± 3.2); both z_d × 0.8 and × 1.2 (declared, not
  a prior); McMillan's own gas column.
- **External field.** Graded at e_N = 0. Route E is Newtonian with no EFE, so a uniform external pull does not enter.
  Reported: the largest tidal change in V_c(R₀) from M31 and the LMC, using h81's baryon masses and distances (770 kpc,
  1.3e11; 49.9 kpc, 3e9) and M200 from the EM1 relation as an upper bound on the enclosed mass. The 2M++ reconstruction is
  not used.
- **McMillan 2017 row:** reported, labelled ΛCDM-PROCESSED.
- **GD2's short disc:** report whether each of its R_d, Σ_b and M_bb lies inside McKee ±2σ, BH&G16 ±2σ, LN16 ±2σ, and
  the labelled Portail box, for OS1's passing cells and native N's.

## Lines (GD2 result 47b63b765c, frozen 78f30f7368; GD1 keys, A1 commit ce2cb587cf)

L1 |v_c − 229.1| ≤ 9.2 and |v_c − v_E| ≤ 2e_E. L2a χ²_Kz ≤ 67.459. L2b |K_z(R₀) − 66.4| ≤ 4.4. L3 χ²_Ou ≤ 59.893. Classes first
match: FEASIBLE IN PRIORS, FEASIBLE (WIDE PRIORS ONLY), V+K ONLY, INFEASIBLE.

## Verdict (frozen; per rule and footing)

1. `HALO_FREE_BULGE` empty, or no usable row: **UNDETERMINED: no halo-free bulge mass on disk.** The summary's wording is
   "exists". I cannot claim that a value does not exist, only that none has been read. So the verdict says "on disk".
2. A usable row: at that M_bb, on the Σ_b × R_d box with McKee's gas: **PASS on halo-free baryons** if a cell inside
   McKee ±2σ and BH&G16 ±2σ passes all four lines; **FAIL on halo-free baryons** if none does. The LN16 tag is stated in
   either case.
3. BRACKET classes are printed with the word BRACKET and may never be quoted as the RF1 verdict.
4. Whatever the verdict, list exactly what would be needed to close it.

A radial gas table and vertical shapes are named as open inputs. They do not change the class rule unless the
sensitivity rows move a class, which is then stated.

## Checks

- **K0:** McMillan on this path: V_b(R₀) 177.234, K_z,b 62.024, within 1 %.
- **K1:** X5's family with McMillan's gas and OS1 reproduces GD2's canonical and alt PRIMARY class, n_all and best D (1e-9).
- **K2:** the OS1 factors 1.635 / 1.510 / 2.100 / 1.863, 1e-3.
- **K3:** the native table gives ND1's 51.8, 78.4, 149, 236, 380 at M_t 1e10…1e14 within 1 %, and 29.4 at lg M200 9.
- **K4:** the halo raises v_c and K_z in every cell.
- **K5:** cell masses against analytic, 2e-3, including the gas rescale.
- **K6:** native N is identical on both footings.
- **K7:** RSS < 1 GB.
- **Rerun:** byte-identical JSON. **Grep:** no 5.364 and no Planck value in the script.
- **MUTATE (`RF1_MUTATE=1`, separate outputs):** q = 0 for OS1, S × 0.5 for native N. K2 and K3 must FAIL, exit 1.

Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf1_mw.py`, one thread, under 1 GB, minutes.

Rule 7: a verdict that flips because an outside input left reads "not a framework failure", never "the framework passes".
Nothing here says the data favour the framework.
