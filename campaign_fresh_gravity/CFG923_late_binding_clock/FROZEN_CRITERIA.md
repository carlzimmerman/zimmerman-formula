# CFG923 FROZEN CRITERIA: does the framework's own formation clock put cold-energy binding late enough for the dwarfs?

Date: 2026-10-20. Block CFG920–929 (LEDGER row "CFG920–929 RESERVED", CFG923 named there). Committed ALONE, before any CFG923
script or number. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are kept apart and never pooled. Raw data and
framework-native quantities only. Cold energy is real gravitating mass; no particle species. Not "theory closed". Nothing here
says the data favour the framework. **Label: CONDITION TEST** of the late-binding escape found by CFG920.

## 1. Why

CFG920 (criteria a229bb78c) tested route D-i of CFG915/916 (cold energy bound at a dwarf's formation, baryons lost later, cold
energy retained) against each dwarf's chemistry. Its timing map (central values, Weisz+14 SFHs, onset 13.3 Gyr) found that at
yield log y = −0.5 seven gas-free dSphs (canonical; six alt) hold their required loss L_req only if the cold energy was bound
after a fraction F_need = 0.51–0.999 of their star formation ("LATE"). That contradicts D-i's "bound at formation", but late
binding could be a posit of its own. The record already has a formation clock for cold energy formed at rest: CFG763 (universal,
f = 1 − e^{−t/τ}, F2 window OPEN) and CFG764 (orbital, τ = k·t_orb, O1 OPEN). This lane asks whether that clock, with its frozen
bracket and no per-dwarf fit, puts the binding epoch at or after each dwarf's F_need.

## 2. Prior-work check (done before this file)

Read: CFG763–CFG769 READMEs (+ CFG763/764 criteria, scripts, JSONs), CFG920 README, criteria §6 and JSON (rows, timing,
timing_summary), CFG920 script (loaders, chemistry functions, timing map), CFG827 README, CFG915 README (D-i), CFG916 LEDGER row,
CFG838/839 READMEs and JSON row format, CFG873/874/875 READMEs, THEORY_CANONICAL_2026-10-18.md (dwarf sections, closing notes),
LEDGER rows for CFG763–769, 916, 920, 920–929. Targeted greps of those files and of LEDGER.md for "CFG763", "clock",
"late binding", "formation clock". No lane compares the CFG763/764 clocks with dwarf SFHs or with CFG920's F_need. CFG666's
"dark-energy clock" is a different object (SHAPE DISFAVOURED) and is not used. **Not done before; this lane proceeds.**

## 3. What was seen before freezing (not blind; disclosed)

- CFG920 central timing values for all 20 tested dwarfs: F_need, t_need, reading, τ50, τ90 (both footings, both yields).
- CFG763 τ_min,95 (0.724 can / 0.832 alt, ages at −1σ) and τ_max = 3.47 Gyr; CFG764 k_min,95 (0.457 / 0.525), k_max 1.196.
- The Weisz+14 table layout (first node log t = 10.1, i.e. 12.59 Gyr). No per-dwarf SFH value, t_orb, F_bind or class was computed.
- **Hand estimate (made before this file, from the numbers above):** under the universal clock the binding epoch is
  13.3 − τ = 12.58 (12.47 alt) to 9.83 Gyr lookback. Canonical: And VII LATE ENOUGH; Leo IV, CVn II BRACKET-DEPENDENT;
  Hercules, And I, Tucana, Cetus TOO EARLY (4 of 7). Alt (Hercules has no excess, reading NONE): And VII LE; Leo IV, CVn II BD;
  And I, Tucana, Cetus TE (3 of 6, **exactly half**). The orbital clock (t_orb ~ 0.1–0.3 Gyr) binds inside the first SFH bin, so
  all are expected TOO EARLY. **The alt footing sits exactly on the sample-class threshold of §7.** The threshold below (a strict
  majority) is the plain meaning of "majority" and is fixed here; the "at least half" reading will also be reported, with no
  class weight.

## 4. Inputs (read only)

- `CFG763_formation_clock/cfg763_results.json`: τ_min,95 (lower_1sigma_ages) per footing. τ_max = 8 Gyr / ln 10 = 3.4743 Gyr
  (CFG763 F2, CFG767 C5).
- `CFG764_orbital_clock/cfg764_results.json`: k_min95 per footing; k_max (SPARC).
- `CFG920_dwarf_baryon_loss_chemistry/cfg920_results.json` rows: feh, s, Ms, Mg, E, sE, L_req, τ50, τ90, timing (F_need, t_need,
  reading). `cfg920.py` (committed text; its chemistry functions are exec'd read-only with CFG4_common.exec_slices for K2b and
  V-1σ; its sha256 is printed).
- Weisz+14 tables 5/6 (`real_research/data/dsph/weisz2014_dl`), read with CFG920's reader (code copied).
- `CFG824_dwarf_age_fossil/cfg824_results.json` (σ_obs = `so`) and the LVD MW/M31/field CSVs (M_V, R_e = `rhalf_sph_physical`
  or `rhalf_physical`, pc), exactly as CFG920 reads them.
- Ungraded reports only: CFG838/839 result JSONs (rows), CFG873/874/875 README/JSON numbers.
- For K1b only: CFG763's own inputs (Lelli+2015 TDG CSV, CFG441 Arp 72c CSV and CFG441 results JSON) and CFG4_common (ν_mono, A0).

## 5. Clock → binding epoch (declared rules; nothing fitted per dwarf)

- **Origin.** t_0 = 13.3 Gyr lookback (CFG827/CFG920 SF onset). The clock runs from baryon assembly; baryons are assembled before
  they form stars, so the onset is the LATEST origin the clock allows. Any earlier origin binds earlier (the choice favours LATE).
- **Formation law.** f(s) = 1 − e^{−s/τ}, s = time since t_0 (CFG763).
- **Primary binding epoch: s_bind = τ** (the mean formation time of the cold mass under the first-order law, f = 1 − 1/e). Lookback
  t_bind = 13.3 − τ. If s_bind ≥ 13.3 Gyr, t_bind := 0 and F_bind := 1 (flag NOT BOUND BY TODAY; favourable).
- **C-U (universal, CFG763; the PRIMARY clock):** one τ for all dwarfs, τ ∈ B_U(f) = [τ_min,95(f), 8/ln 10] Gyr.
- **C-O (orbital, CFG764):** τ_i = k·t_orb,i, k ∈ B_O(f) = [k_min95(f), k_max]; t_orb,i = 2π r_1/2/V_c with r_1/2 = (4/3) R_e and
  V_c = √3 σ_obs (the Wolf relation CFG827/920 use), present-day measured values.
- **F_bind** = the Weisz+14 cumulative SFH fraction at t_bind, using the forward form of CFG920's `t_of_F` mapping: piecewise
  linear in log t between the onset (13.3 Gyr, F = 0) and the Weisz nodes (running maximum of the cumulative fractions); below the
  youngest node F = the last value.
- **Rescue rule.** A dwarf is rescued at τ iff F_bind(τ) ≥ F_need (equivalently t_bind ≤ t_need). CFG920's post-binding loss
  L_post(F) falls with F and unseen loss only raises L, so any binding at or after F_need holds L_req; CFG920's condition sets no
  upper limit on lateness. F_bind is non-decreasing in τ (later binding), so the two bracket ends decide the class.

## 6. Per-dwarf classes (per clock, per footing; primary yield log y = −0.5, CFG920's quoted corner)

Test set S(f) = the dwarfs whose CFG920 central reading at −0.5 on footing f is EARLY or LATE (F_need > 0).
- **LATE ENOUGH:** rescued at both bracket ends (so across the whole bracket).
- **TOO EARLY:** rescued at neither end (not even by the slowest clock).
- **BRACKET-DEPENDENT:** rescued at the slow end only.

Outside S (reported, no class weight): AT FORMATION → NO TIMING REQUIREMENT (any epoch holds L_req); NONE → NO TIMING RESCUE (no
epoch holds it; an amount failure, not a timing one). Also reported per dwarf: t_bind and F_bind at both ends beside τ50, τ90,
t_need and F_need, and f_pre = 1 − e^{−(13.3 − t_need)/τ} (the fraction of the cold energy the clock has already formed before
the required binding moment) at both ends.

## 7. Sample class (per clock, per footing; N = |S(f)|)

- **LATE BINDING SUPPORTED BY THE CLOCK:** no dwarf TOO EARLY and at least half LATE ENOUGH.
- **CONTRADICTED:** more than half of S TOO EARLY (a strict majority of the dwarfs that need late binding cannot get it anywhere
  in the clock's frozen bracket).
- **UNDERDETERMINED:** otherwise.

**Headline:** the C-U class on each footing. **Record level, per footing:** if C-U and C-O agree, that class; if not,
UNDERDETERMINED (the record keeps both clocks open; CFG765/766: no public sample decides between them). **OVERALL:** the
record-level class if both footings agree; otherwise UNDERDETERMINED, with each footing stated (never pooled).

## 8. Variants (reported; no class weight)

Binding-epoch rule (each graded with §6–7; a clock/footing class is **RULE-ROBUST** if all four agree with the primary, else
**RULE-FRAGILE**, naming the variants that flip):
- **V-MED:** s_bind = τ ln 2 (f = ½).
- **V-90:** s_bind = τ ln 10 (f = 0.9).
- **V-STEP:** CFG827's `bins()` convention for the first bin (all first-bin stars at the onset): for 12.59 < t_bind < 13.3 Gyr,
  F_bind = the first-node fraction (favourable to LATE).
- **V-DIST:** distributed binding: F_eff = ∫₀^{13.3} F(13.3 − s) e^{−s/τ} ds/τ ÷ f(13.3 Gyr) (cold mass formed by today), compared
  with F_need. Exact only if the post-binding loss were linear in F; approximate (disclosed).

Measurement uncertainty (own class, reported):
- **V-1σ:** F_need at the favourable end (L_req = e^{4(E+sE)}, [Fe/H] + s) and the unfavourable end (e^{4(E−sE)}, [Fe/H] − s),
  from CFG920's own functions. TOO EARLY(1σ) iff even the favourable F_need is not rescued at the slow end; LATE ENOUGH(1σ) iff the
  unfavourable F_need is rescued at the fast end (an unfavourable NONE is not LATE ENOUGH); else BRACKET-DEPENDENT. Sample class
  by §7 on the same S.

Other:
- **V-Y02:** the same grading at yield −0.2 (CFG920's second timing corner; its own S).
- **V-HALF:** §7 with "at least half" in place of "more than half" (the threshold sensitivity disclosed in §3).

## 9. Controls

- **K1 (CFG763 bracket from its JSON).** τ_min,95 read per footing; F2_window OPEN on both; stored f_at[t] = 1 − e^{−t/τ_min} to
  1e-12 for t = 1, 2, 3, 8 Gyr; |8/ln 10 − 3.47| < 0.005.
- **K1b (CFG763 recomputed).** CFG763's χ² code (copied) on its own inputs reproduces τ_min,95 on both footings exactly (same
  0.01-dex grid point) and its τ → 0 / τ → ∞ χ² equal CFG441's 34.018 / 40.290 / 1.105 within 0.01.
- **K2 (CFG920 required fractions from its JSON).** (a) t_need = t_of_F(F_need) from the copied Weisz reader equals the stored
  t_need within 1e-9 Gyr for every EARLY/LATE entry (2 footings × 2 yields); (b) F_need recomputed with CFG920's exec'd functions at
  the stored central L_req and [Fe/H] equals the stored F_need within 1e-5 with identical readings, all 20 × 2 × 2; (c) the reading
  counts equal CFG920's timing_summary.
- **K3 (orbital-clock inputs).** E recomputed from CFG824 σ_obs, LVD M_V and R_e and CFG920's stored Υ equals CFG920's stored E
  within 1e-9 (both footings, all 20); CFG764's k_max = 8/(ln 10 · torb_max) from its JSON within 1e-9.
- **K4 (numerics).** The forward F(t) inverts t_of_F: F(t_of_F(F)) = F within 1e-9 on F ∈ {0.05, …, 0.95} for all 20 dwarfs
  (plateaus excepted); F_bind non-decreasing in τ on a 200-point grid for every dwarf and both clocks.
- **MUTATE** (`CFG923_MODE=MUTATE`, separate `cfg923_MUTATE.out` / `cfg923_results_MUTATE.json`): every bracket end ×0.1 and ×10
  (τ for C-U, k for C-O). **Bites iff, on both footings, under C-U the ×0.1 run and the ×10 run each change at least one per-dwarf
  class and at least one of them changes the C-U sample class.** C-O scaled classes are reported (no bite requirement: the hand
  estimate puts C-O inside the first SFH bin, where ×0.1 cannot move an already-TOO-EARLY class). Exit 1 iff it bites.
- Main run (`CFG923_MODE=MAIN`) re-runs K1–K4 and exits 0 iff all pass. `CFG923_MODE=K` runs the controls alone (`cfg923_K.out`).

## 10. Ungraded reports (asked for; no class)

- **R1, tides (CFG838/839).** For S: host (MW / M31 / field), CFG838 present-day log T and CFG839 pericentre log T_p where they
  exist, and whether the clock's binding precedes τ90 (where CFG920 places the W2 terminal loss). Reading: does late binding need a
  host-driven post-binding loss, which CFG838/839's no-tide result would not support?
- **R2, field dwarfs (CFG873–875).** The field dwarfs' timing requirement and clock classes (Cetus, Tucana gas-free; Aquarius,
  Phoenix, Leo T gas-bearing) beside CFG873 (E_F, D), CFG874 (c, E) and CFG875 (k). Reading only.

## 11. Not tested

Formation laws other than first order; a time-dependent target with retention (each parcel binding to the baryons present when it
forms); orbital times at the formation epoch (present-day σ_obs and R_e are used); Weisz+14 SFH uncertainties (central cumulative
SFH only); clock origins other than the onset; the 8 dwarfs CFG920 could not test (no LVD [Fe/H]) and its V-TR training dwarfs (no
timing map); yield +0.1 (CFG920 gives no timing there); any formation microphysics. κ derived: not claimed. "Theory closed": never.

## 12. Compute

One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, < 1 GB, seconds; beside the live 1024³ job, which is not touched.
Nothing downloaded. No other lane's file is edited.
