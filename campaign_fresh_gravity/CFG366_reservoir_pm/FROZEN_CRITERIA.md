# CFG366 FROZEN CRITERIA: the reservoir rule in the nonlinear PM run (does local mass conservation remove the excess growth?)

Committed alone, before any script. kappa = 1/2 FITTED and fixed. nu_mono. No dark-matter particle species: the cold MASS is
still required and is kept. No knob scans (R_c is a declared two-value bracket). Never "theory closed". Owner
(2026-10-06, chat "Nobel Prize and neutrinos"): "run the min-rule PM simulation here". The orchestrator owns CFG361; this
lane copies its engine (not imported) and changes only the ON-cell source.

**Why the literal min rule is not run.** In the engine the real cold fluid already gravitates through the Newtonian term
(1.5 Om delta/a). Options only ADD an extra source. T5 adds f max(s_ph - s_c, 0). A LOCAL cap (dark <= real cold present
in the cell) adds exactly 0, which is the Newtonian control S0 (sigma8 ratio 1 by construction). That is a non-test, and
it is stated as such, not run.

**The run (the reservoir reading, CFG365).** The phantom's excess over the local cold share is MADE OF cold fluid drawn in
from the surroundings (the reservoir), so it must be removed from there. In ON cells add T5's excess
e = f max(s_ph - s_c, 0), and subtract the same mass spread over a catchment of radius R_c:

    extra = e - W_Rc * e,   with W_Rc a Gaussian of comoving width R_c (in Fourier: e_k (1 - exp(-k^2 R_c^2/2))).

Real plus dark gravitating mass is then conserved on scales above ~R_c (the k -> 0 limit is exactly zero). The cold
removed from the surroundings is NOT moved as particles (no mechanism; disclosed). This is a gravity-level bookkeeping test
only.
- R_c in {1, 3} Mpc/h. A host's Lagrangian catchment (~1-2 Mpc/h for 1e12-1e13 Msun/h) sits inside this bracket.
- Limits as controls: R_c -> infinity gives T5 (box-wide compensation = CFG361's k = 0 convention); R_c -> 0 gives S0.

## Engine (identical to CFG361 except the switch "RES")
GR + Lambda background, L352 parameters, nu_mono, baryon-only phantom, T1 switch eps = 0.077, EH ICs at z_i = 49 (the only
LCDM input), seed 359, L = 200 Mpc/h, 256^3 on 256^3, 150 KDK steps, 2 FFT threads, os.nice(10), 4 processes.
Work data go to ../_external_data/cfg366_work/. S0 256^3 is read READ-ONLY from CFG359's work JSON; the T5 256^3 JSONs
from CFG361's work dir (read-only, comparison only).

Runs: RES x R_c {1, 3} x {canonical, alt}, A0-FLAT, 256^3 (4 runs).

## Measurements (as CFG361)
- sigma8 ratio and P(k) ratio to S0 at z = 1, 0.5, 0. ON fractions. The phantom-dominated share of ON mass.
- **Overdraw (reported):** the mass fraction of cells where s_c - W_Rc * e < 0, i.e. the catchment would need more cold
  than is locally present.
- **Lensing translation (reported):** S8 shift = sigma8 ratio at z = 0 (fixed Om).

## Decision (CFG361's cuts verbatim; per footing; never pooled)
- **GROWTH OK:** |sigma8 ratio - 1| <= 5% on BOTH footings AND max over k <= 1 h/Mpc of |P ratio - 1| <= 10% on both.
- **TENSION:** the sigma8 shift is in (5%, 20%], or the P shift is > 10% with sigma8 within 20%.
- **FAIL:** the sigma8 shift is > 20% on either footing.
Verdict per R_c. Lane verdict = R_c = 1 (primary, the smaller catchment, closest to a single host); R_c = 3 separate.

## Controls (frozen)
- **C1 (compensation):** at every snapshot, the band-averaged |extra_k|/|e_k| for k < 0.1/R_c is <= 0.01, and
  sum(extra) = 0 to float precision.
- **C2 (limits, field level, first snapshot):** with R_c = 1e6 Mpc/h the extra equals T5's minus its mean, to 1e-4
  relative. With R_c = 1e-6 it is 0 to 1e-6.
- **C3 (S0 read):** the CFG359 S0 JSON exists and its z = 0 sigma8 is reproduced from its stored P(k) (identity check).
- **MUTATE** (CFG366_MUTATE=1): the compensation is disabled inside C1's check only (extra := e). C1 must FAIL, rc 1.
  It is a field-level check on one 128^3 snapshot; no full MUTATE run.

Local compute only. No downloads.
