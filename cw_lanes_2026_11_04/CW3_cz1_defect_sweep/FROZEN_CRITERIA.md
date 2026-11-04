# CW3_cz1_defect_sweep: FROZEN CRITERIA

Written 2026-11-04. These criteria are committed alone, before any sweep output, rerun or table. Lane proposed 11-04 as CW3 in a local planning brainstorm. It is a **correctness audit, not a physics verdict.** κ = ½ FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the data favour the framework.

## Question
CZ1 found that KT15–KT28 put the host's observed (MOND) field into QUMOND's ν, where the Newtonian field belongs, and CZ2 re-graded those lanes. **Which other lanes on record carry the same defect, or its mirror image, and which verdicts move once the field is right?**

## Definitions (frozen)
- **QUMOND / quasi-linear forms**, including every 1D form ν(√(g_e² + g_N²)/a0), ν(|g_N + g_e|/a0) and shortcuts such as M = ν((g_N + g_e)/a0) M_b. ν's argument is the **Newtonian** total field, so the external input must be the host's Newtonian field g_Ne. An observed or MOND-total field there is **DEFECT-Q**.
- **AQUAL / μ forms.** μ's argument is the total MOND field, and the external boundary condition is the observed total field g_e. A Newtonian field there is **DEFECT-A**.
- **Modified inertia, or any form whose declared variable is the kinematic (observed) acceleration.** An observed field is correct. Label **NOT-QUMOND**.
- **Field values on record, for orientation only.**
  - Observed or total: 1.778e-10 (1.9 a0 canonical, the DR4 primary); 1.9e-10 (the BN11 g_e); 2.078e-10 (V_c²/R0); 2.32e-10 (KT16); (200 km/s)²/D.
  - Newtonian: G M_b/D² from a host baryon model, or the observed value inverted through the lane's own ν, as CZ1/CZ2 did.
  - A value's label in a README or comment counts only if the code agrees with it.

## Scope and priority (frozen)
1. **Named lanes.**
   - KT20 and KT21.
   - CFG843 (MW vs M31 satellites), CFG478, UX4, CFG447.
   - The directional-EFE lanes.
   - The 09-03 Local Group dwarf item (MW +0.64, M31 +0.29).
   - IC 1613's closed lever. CZ1 Part D already closed it, so confirm only.
2. **Lanes the current record cites:** `rebuild_2026_10_22/REQUIREMENTS_2026-11-01/`, `rebuild_2026_10_22/CLOSING_LEDGER_2026-11-01_DRAFT.md`, and the lanes behind PAPER67.
3. **Everything else the frozen grep finds.** Triage it and flag it. Rerun it only if cheap.

KT15–KT19 and KT22–KT28 were fixed by CZ1/CZ2. They are listed as **FIXED** and not re-audited.

## Frozen grep (run from the repo root; any later extension is a dated amendment)
```
git ls-files '*.py' | xargs grep -l -i -E "external.?field|\bg_?ext\w*\b|\bgext\w*\b|\bge\s*=|\bg_e\s*=|\bGE\s*=|\bETA0?\b|\befe\b|1\.9e-10|2\.32e-10|1\.778e-10|2\.078e-10|200\s*\*\*\s*2|200e3\s*\*\*\s*2"
```
A hit becomes an audit row only if the same file also calls ν or μ: `nu(`, `nu_`, `mu(`, `mu_`, `ν`, `μ`, or a named interpolating function.

## Labels per row (frozen)
- DEFECT-Q
- DEFECT-A
- CORRECT
- NOT-QUMOND
- AMBIGUOUS (code and README together can't settle it)
- FIXED (CZ1/CZ2)

Each row records file:line evidence, the formulation, the field value used and its source.

## Reruns (frozen)
- **Which lanes.** A DEFECT row is rerun only if all of these hold:
  - its script runs in ≤ 15 min wall on 1 thread with ≤ 1 GB RSS;
  - it needs no download;
  - its inputs are on disk.
- **How.** The script is copied into this folder and the original is never edited. Only the external-field input changes, to the Newtonian value:
  - the lane's own host baryon model where it has one;
  - otherwise the observed value inverted through the lane's own ν.
- **K1 (known answer).** The copy, run with the original field, reproduces the lane's committed headline numbers to their printed precision. Without K1 a rerun is NOT RERUN (K1 failed).
- **MUTATE twin.** With ν ≡ 1, the external-field dependence must vanish (the Newtonian answer for every field). It bites if the corrected and original runs then agree.
- **Verdict-change classes:**
  - FLIPS: the lane's frozen label changes.
  - MOVES: a headline number changes by more than the lane's own stated tolerance (10 % if it states none) and the label holds.
  - UNCHANGED.
  - NOT RERUN, with the reason.
- A rerun is a **reading of the lane under the corrected field, not a re-grade.** A FLIPS row needs its own frozen re-grade before anyone cites it, as CZ1 → CZ2.

## DR4 pre-registration (frozen)
- `prep_2026/gaia_dr4_prep/` and its banked target scripts are read only and never edited, run, or rehashed.
- If its frozen pipeline or banked target puts an observed field into a QUMOND ν (DEFECT-Q), write `OBSERVATION_DR4_2026-11-04.md` in this folder for the owner.
- Otherwise its row in the table records CORRECT or NOT-QUMOND, with the evidence.

## Outputs
- `CW3_TABLE.md`: lane, file:line, formulation, field used, label, verdict-change class.
- The rerun copies and their `.out` / `.json`.
- `README.md`.

No file outside this folder is edited.
