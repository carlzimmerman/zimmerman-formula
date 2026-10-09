# CFG528 FROZEN CRITERIA: the four SLUGGS centrals -- data re-check, missing baryons, derived mechanisms

Written 2026-10-09, before any CFG528 code was written or any CFG528 number computed. On-disk data only; no downloads.
κ = ½ is FITTED. Footings 9.36e-11 / 1.13e-10, never pooled. Kernel ν_mono, ν(y) = 1/(1 − exp(−√y)). The cold energy's mass is
still required. Not "theory closed". No knob is fitted; every "needed" value below is post hoc and reported only.

## The fail being examined
The four group/cluster centrals M87 (NGC 4486), NGC 4365, NGC 4374, NGC 5846: the law under-predicts the outer GC dispersions
(CFG330 K0 stars only: centrals mean +0.224 / +0.213 dex; CFG331 R-own +0.198 / +0.187; CFG466 ROBUST FAIL with γ free;
CFG492 PN tracer agrees). The owner's rule: a mechanism or a scope statement, plus a data re-check.

## Machinery (fixed)
- CFG331's source is exec'd read-only up to its `# ---- run` block (exactly as CFG466 does): raw Forbes+17 GC velocities, cut,
  3σ clip, equal-number bins, ML σ, outer bins R > max(R_e, 2 kpc), ATLAS3D JAM calibration, Hernquist a = R_e/1.8153,
  CFG331 host gas (Lakhchaura+18 D1, Fukazawa+06, Churazov+08 + Urban+11 for M87), members, g_e.
- Primary tracer: γ = 3, β = 0 (the record's base). Slope freedom is CFG466's result and is quoted from its JSON, not re-run.
- Per-galaxy error σ_i: CFG466's GC bootstrap at γ = 3 (`reported[NGC|K0|foot]["sig_g3.0"]`), used for every row
  (declared approximation: the GC-sampling error does not depend on the mass model).
- Z_i = offset_i / σ_i (one-sided; offset = mean outer log σ_obs/σ_pred). A central is CLEARED if Z_i < 2, REVERSED if Z_i < −2.
- A row CLOSES the fail if ≥ 3 of 4 centrals are CLEARED and none REVERSED, on BOTH footings.
- Class statistic (reported): mean offset of the four, error sqrt(Σσ_i²)/4, Z_class.

## Item 1 -- data / assumption re-check (each row: offsets per central, Z_i, CLOSES yes/no, both footings)
1a **Stellar M/L and IMF.** Rows: (i) JAM-law ceiling (record; IMF-neutral, calibrated to each galaxy's own JAM mass inside r_½);
   (ii) Salpeter population, M* = 10^(logML_Salp + logL) (ATLAS3D XX, on disk), distance-rescaled as Mjam;
   (iii) Chabrier population = Salpeter − 0.25 dex (declared convention);
   (iv) bottom-heavy "2× Chabrier" = Salpeter + 0.051 dex (the brief's "up to ~2×"; Cappellari+12, Conroy & van Dokkum 2012,
   recalled, PROVISIONAL as literature context only).
   Each row reports the INNER excess ε_in = log[M_law-pred(<r_½)/(½ M_JAM)] under the law.
   **Admissible** only if ε_in ≤ +0.06 dex (≈ 2 × a 7% JAM M/L error; declared). An IMF row that closes but is inadmissible
   does not count as DATA-ISSUE. Post hoc (reported): the M* multiplier on the JAM ceiling that nulls each central, and its ε_in.
1b **Distances.** Rows: SBF (record); ATLAS3D distance (Dist_Mpc, on disk); SBF × 0.9 and × 1.1 (declared admissible ±10%,
   ≈ 2× a 5% SBF error). Distance enters GC radii, R_e, r_½, M_JAM (∝ D) and the gas exactly as CFG331 does.
   Post hoc: the distance factor that nulls each central.
1c **Anisotropy.** β = −0.5 and β = +0.5 at γ = 3 (admissible edge = +0.5, the record's bound). CFG466's free-γ classes quoted.
1d **Radial range.** All bins; outermost bin only; innermost outer bin only. Reported; "all bins" is the admissible lever.
1e **Round rule vs phantom disc.** The prediction must be the round enclosed-mass rule (CFG516 RM). Check R1: the phantom mass
   rebuilt from its own density, M_ph(<r) = ∫4πr²ρ_ph dr with ρ_ph from d/dr[r²(ν−1)g_N]/(4πG r²), reproduces the field used to
   ≤ 1e-3 relative inside the outermost GC bin. (Spherical QUMOND = algebraic law, so round and QUMOND coincide here.)
1f **EFE-free.** R-efe (CFG331) recomputed; EFE can only raise the offsets (check E1: no offset lowered).
**DATA-ISSUE row** = any single admissible item-1 row that CLOSES.

## Item 2 -- missing baryons (hot gas)
2a R-bar with the measured gas TRUNCATED at each source's measured edge. 2b R-bar with CFG331's frozen extrapolation (record).
2c R-own (host centres carry host gas + members; NGC 4365 / 4374 own baryons), = CFG331 (check K2 reproduces it to 1e-9).
2d Post hoc: the gas multiplier x (on the measured profile shape, extrapolated) that nulls each central.
No new gas profile exists on disk for the NGC 5846 group beyond 30 kpc or for NGC 4365 at group scale; if needed, it is LISTED,
not fetched. The cm05 L_X correlation (partial ρ +0.47 given mass; cm07: carried by group centrals) is quoted, not re-run.

## Item 3 -- derived mechanisms only
3a **Census edge / supply cap.** For each central, M_b = JAM-law stars + gas inside the outermost GC bin (2b profile). f_ret from
   CFG515's `fret_census` (imported read-only), edge r_edge = r_M/ln(1 + f_ret f_b/(1 − f_b)), supply 5.364 M_b/f_ret.
   Also with the host baryons for the host centres (M87: Virgo gas to 1.2 Mpc + stars; NGC 5846: gas to 3 × the outermost bin).
   The cap BINDS if r_edge < R_out or M_ph(<R_out) > supply. If it binds, the capped field is used (can only lower σ_pred).
   Candidate B puts exactly the law's phantom inside the edge, so the census can add no mass inside it (stated, then checked).
3b **Round rule.** = item 1e (the prediction already is RM).
3c **Host ownership** = row 2c (derived reading of PAPER35 §2).
**MECHANISM FOUND** = a derived row (2a, 2b, 2c, 3a) that CLOSES.

3d **Template row (NOT derived; reported with its own label, never a MECHANISM FOUND):** the host's UNSETTLED cold energy, from
   the X-COP measured profile (CFG432 JSON): M_u(<r) = Q(r/R500) M_gas,host(<r), Q(x) = Q01 (x/0.1)^s_gas with Q01 = median of
   CFG432 per-cluster Q_01 and s_gas = the cell median slope (canonical b = 0 for the canonical footing, alt b = 0 for alt), power-law
   continued inward of 0.1 R500 (primary); flat Q inward (bracket). Newtonian (unsettled cold energy does not source the law).
   Host centres only (M87, NGC 5846). R500 recalled, PROVISIONAL: Virgo 0.70 Mpc, NGC 5846 group 0.38 Mpc; bracket × 0.7 / × 1.3.
   Its label is TEMPLATE CLOSES / TEMPLATE PARTIAL (only host centres cleared) / TEMPLATE NO.

## Joint best case (for NOT DIAGNOSTIC)
All admissible levers in the law's favour at once: R-own (2c) with extrapolated gas, β = +0.5, the heaviest ADMISSIBLE IMF row,
distance × 1.1, outer bins. Template excluded (reported separately as "joint + template").

## Headline verdict (applied in order, both footings)
1. DATA-ISSUE if an admissible single item-1 row CLOSES.
2. MECHANISM FOUND if a derived row (2a/2b/2c/3a) CLOSES.
3. NOT DIAGNOSTIC if the primary does not close but the joint best case CLOSES (the fail rests on assumptions at their edges).
4. GENUINE TENSION otherwise, with σ = Z_class of the joint best case (and of the primary K0 / R-own, reported).
Footings disagreeing: the less favourable to the law is the headline; both printed.

## Controls (main run)
K1 the K0 path reproduces CFG330 K0 per central to 1e-9 dex, both footings. K2 R-own / R-bar reproduce CFG331's JSON to 1e-9.
K3 σ_i loaded from CFG466 JSON for all 4 × 2. R1 (item 1e). E1 (item 1f). K4 `fret_census` equals CFG515's (import, not copy).

## MUTATE (`CFG528_MUTATE=1`, separate `_MUTATE` outputs; each must behave as stated or the MUTATE FAILS and is kept)
MA Chabrier population M*, gas × 0, members × 0, β = 0: must NOT close, with ≥ 3/4 centrals Z ≥ 2 and every offset ≥ its K0
   value on both footings (the pipeline detects the fail when the levers are removed).
MB planted mass, M* × 8 on the JAM ceiling (K0): must CLOSE on both footings (the criterion can fire).
MC template × 0: must reproduce row 2c exactly (1e-9).

## Outputs
`cfg528_mechanism.py` → `cfg528_mechanism.out`, `cfg528_mechanism_results.json`; MUTATE → `*_MUTATE.out`, `*_MUTATE_results.json`;
`README.md`. Frozen text is never edited; anything decided later is a dated disclosure in the README.
