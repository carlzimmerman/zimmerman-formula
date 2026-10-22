# E3_dwarf_excess — FROZEN CRITERIA (written before any script or number of this lane)

Wave E audit item (2): ultra-faint / dwarf satellites below M_crit sit "+2.15 dex above Newton" (A26 K6, `a26_rar.csv`)
and "+1.25 dex above the EFE-present law" (D2 Q3). In the screened theory (PAPER49 action, L* >= 24 pc, CFG820) these
systems are screened toward Newton, so they need **real bound cold mass** (CFG820/821). This lane (A) audits every input
of the +2.15 dex under the raw-data rule and recomputes it with clean choices, and (B) asks whether the framework's own
rules can supply the required bound cold mass.

κ = ½ FITTED. Footings canonical a0 = 9.3603e-11, alt 1.1312e-10 m/s², never pooled. Cold energy, no particle.
Not "theory closed". Nothing here says the data favour the framework.

## Record checked before freezing
A26 report/script/csv; D2 README Q3 + R7; CFG820 (S(s) screening recipe from CFG691), CFG821, CFG822 (H-EX; f_ret census),
CFG823 (placement-free cold budget, classical dSphs, the template for Part B), CFG809 `fret_of` (CFG416/556 census),
CFG838 (tides), CFG842 (host capture, Liouville), CFG51/CFG861/CFG892 (multi-epoch binaries), CFG257 scoping (Arroyo-Polonio,
Geha II), CFG870–889 (clump lanes; CFG888 record equations give extra cold no law self-boost / no self-gravity in S3;
CFG889 not retained), CFG920 (baryon loss underdetermined), CFG959 (H-UNR fails on dSphs). This lane adds no mechanism.

## Sample
A26's 45 sub-threshold systems (`below_Mcrit = 1`, canonical M_crit = a0 L*²/G = 3.867e5 M☉), rebuilt from
`real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv` with A26's code path. The alt footing's M_crit (larger) is
reported as a second sample; numbers per footing.

## Part A — inputs and clean recompute
Statistic E_N = median over systems of log10(g_obs/g_bar), g_obs = 3σ²/r12, g_bar = G(M*/2)/r12², r12 = (4/3) R_e.
Errors: per-system Monte Carlo (σ asymmetric em/ep, R_e em/ep, distance-modulus em/ep with M* ∝ D², R_e ∝ D) combined
with a bootstrap over systems (seeded; 4000 draws).

Declared choices:
- **raw (A26):** LVD σ, Υ_V = 2 (LVD mass_stellar), σ upper limits used as values.
- **clean primary:** LVD σ × binary ratio b_i, where b_i = Arroyo-Polonio free-f ratio sig_f/sig_fz (same data) for the
  systems in that table, else the median of that ratio over its 12 systems; σ upper-limit systems reported both as values
  and dropped; Υ_V = 2.
- **brackets:** Υ_V ∈ {1, 4} (the record's CFG823 bracket); binaries f = 0.7 ratio (sig_f7/sig_fz); Geha 2026 II
  (DEIMOS, multi-epoch variables removed) σ in place of LVD where resolved; Wolf normalisation 3 vs 1 (σ²/r, reported,
  not "clean": the 3 is the Jeans result at r12).
- **worst-clean W:** Υ_V = 4, f = 0.7 ratios, the lower of LVD/Geha σ, upper-limit systems dropped.
- **non-equilibrium:** no on-disk measurement corrects it. Bound reported as: (i) the σ inflation factor each system
  would need to reach the screened prediction, compared with the largest measured dataset-to-dataset σ change on disk;
  (ii) informational: fraction of satellites whose r12 exceeds the baryon-only Newtonian Jacobi radius at the present
  host distance (host masses: MW 6.0e10 from CFG332, M31 1.0e11 labelled external, as in D2).

**Part A lines (frozen):**
- A-SURVIVES if W − 2σ_W ≥ 1.0 dex (the screened theory still needs ≥ 10× Newton after binaries + M/L + UL removal).
- A-REDUCED-BUT-LARGE if 0.5 ≤ W − 2σ_W < 1.0; A-COLLAPSES if W − 2σ_W < 0.5.
- Report the surviving fraction W / E_N(raw).

## Part B — framework-native capacity
Per system, clean primary choices, both footings, L* = 24 pc (least screening allowed by CFG820; also 90 pc reported):
- Screened prediction (CFG820 recipe, isolated, no EFE): B_scr = 1 + S(s)(ν(y) − 1), s = r12 / (L*²/(2 r_M)),
  r_M = sqrt(G M*/a0), S from CFG691's table, ν(y) = ½(1 + sqrt(1 + 4/y)) (A26's canonical law). This already contains
  the tethered (screened) phantom; the EFE would only lower it.
- Required extra bound cold inside r12, record Class-A accounting (CFG888: extra cold energy gets Newtonian self-gravity,
  no law boost): M_c,req = M_dyn − (M*/2)·B_scr, M_dyn = 3σ² r12/G. Reported variant (not in the record, H-LINK self-boost,
  favourable): M_dyn/B_scr − M*/2.
- Framework ceiling (placement-free, CFG823 form): C = 5.364 · M_b / f_ret, M_b = M* (+ LVD M_HI if given).
  f_ret = 0.10 (CFG416/556 census floor — ΛCDM-PROCESSED, halo-mass census relative to Planck f_b) as the record value;
  f_ret = 1 (present baryons only) as the census-free value. 5.364 = Ω_c/Ω_b is itself a ΛCDM (Planck) fit
  (CFG886: recovered from BAO+BBN, not pinned); flagged, verdict linear in it.
- q = M_c,req / C (fraction of the WHOLE catchment's cold energy that must sit bound inside r12).
- L_req = M_c,req / (5.364 M_b): the catchment-to-present baryon ratio (= 1/f_ret) needed for q = 1.

**Part B outcome lines (frozen, evaluated on the clean primary, both footings):**
- **CANNOT (shortfall N dex):** median q at f_ret = 0.10 has its bootstrap 16th percentile > 1 on both footings.
  N = log10(median q).
- **UNDECIDABLE (ingredient: catchment baryon mass / f_ret, not native):** not CANNOT, but median q at f_ret = 1 > 1
  (the supply suffices only through the ΛCDM-processed census).
- **CEILING ALLOWS:** median q at f_ret = 1 ≤ 1.
- In every case, the "can supply" outcome additionally requires a record mechanism that binds extra cold energy inside
  r12. The record inventory (CFG822 too far out, CFG842 capture 1e-8–1e-5, CFG888 no law self-boost / no self-gravity
  in S3, CFG889 not retained, CFG959 H-UNR fails dSphs) is restated, not re-tested; if none, the headline says
  "NO MECHANISM IN THE RECORD" alongside the class.
- Also reported: number of systems with q > 1 at 2σ (MC lower 2.5%), and the worst-clean W version of q.

## Checks (script `e3_dwarf_excess.py`, one line each)
- K1 A26 reproduced: N below = 45 and raw E_N = 2.147 ± 0.01.
- K2 Wolf mass identity: median |log10(M_dyn / LVD mass_dynamical_wolf)| ≤ 0.05 over systems with both.
- K3 Screening limits: B_scr → 1 as L* → ∞ (≤ 1e-3 dex) and → ν(y) as L* → 0 (≤ 1e-3 dex), on the sample.
- K4 Arroyo ratios: median log10(sig_f/sig_fz) over 12 within 0.02 of −0.068; f = 0.7 within 0.02 of −0.104 (CFG257 scoping).
- K5 Ceiling code reproduces CFG823 Draco q (Υ 2) within 2%.
- K6 Pipeline sees the excess: raw E_N ≥ 1.0 dex.
`--mutate`: σ of the 45 replaced by the screened (L* = 24 pc) prediction σ_scr; K1 and K6 must FAIL.
Outputs: `e3_dwarf_excess.out`, `e3_dwarf_excess_results.json`, `e3_inputs_ledger.csv`, per-system `e3_per_system.csv`;
mutate to `*_MUTATE.*`. OMP_NUM_THREADS=1, nice 10, seconds, no network.

## What each outcome means
- A-SURVIVES + CANNOT: the screened theory fails on dwarfs with its own supply rules; the failure is not a data artefact.
- A-SURVIVES + UNDECIDABLE: the verdict rides on a ΛCDM-processed catchment size; a native catchment rule is the gap.
- A-COLLAPSES: the dwarf item is a data problem, not a theory problem.
