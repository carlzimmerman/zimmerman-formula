# KAPPA_LEDGER.md -- every kappa=1/2 derivation attempt, one line each (T010)

Assembled 2026-08-17 by runs/t010_kappa_ledger.py.  kappa=1/2 is ADOPTED/FITTED (measured 0.551+/-0.043), NEVER 'derived'.  CONFIRMED/CANDIDATE rows carry an adversarial refutation re-check.

Window: kappa in [0.5080, 0.5940] (fit+/-1sigma); kappa^2 in [0.2581, 0.3528].
Footings (dimensionless numbers are footing-invariant; a0 spread shown per R3): can a0=9.3619e-11, alt a0=1.1279e-10.

## Committed history (pre-T001 corpus)
- **hist-TT-gauge** (KILL) -- TT-gauge route :: committed corpus: TT-gauge route to kappa=1/2 killed
- **hist-5var-span** (KILL) -- 5-variant span :: 5 kappa variants span 161.6x -> not a single pin
- **hist-BE-mirror** (REFUTED) -- BE mirror (pre-T005) :: Bose-Einstein mirror route 11.1sigma low; no q in [0.5,2] reaches 1/2

## T001-T009 (task-based)
| id | title | verdict | one-line status | refutation status |
|----|-------|---------|-----------------|-------------------|
| T001 | route catalog | CONFIRMED | every published dS-thermo route forces q!=1/2 or none; Milgrom2020 q=1/2pi=0.159 closest near-miss, outside the window | RE-CHECKED t010: 0/4 forced route coeffs in [0.508,0.594]; closest q=1/2pi=0.159 -> SURVIVES |
| T002 | eps_tot=1/(32pi) enumeration | NULL | not special: 3 matches vs 2.23 expected in the +-15.6% window, typical | - |
| T003 | graviton-bath cancellation, 1-assum. | UNGRADED | 7/7 form-assumptions LOAD-BEARING (count=7 != 1); SCRIPT-GREEN, needs grading | - |
| T004 | response-function scan | UNGRADED | SCRIPT-RED; no Boltzmann/Wigner/Gaussian-linear response yields untuned 1/2; needs fix | - |
| T005 | q-deformed Deser-Levin mirror | REFUTED | q* out of range for both deformations over q in [0.5,2]; route stays ~5x low | - |
| T006 | first-law smearing catalog | UNGRADED | 5 smearings each fix kappa per choice; SCRIPT-GREEN, needs grading | - |
| T007 | boundary-term (GHY/bulk) ratios | CONFIRMED | kappa^2 not a GHY-to-bulk ratio at <=3 combos; 0/3 in window; Bekenstein-Hawking S/A=1/4 is CONVENTION-grade, excluded | RE-CHECKED t010: 0/3 GHY/bulk etas in kappa^2 window [0.258,0.353] -> SURVIVES |
| T008 | two-temperature interpolation | UNGRADED | no n gives a0-line AND kappa=1/2; SCRIPT-RED, needs grading | - |
| T009 | pi-free theorem | UNGRADED | kappa pi-free AND a pure horizon-geometry ratio is trivial (M=1) or carries a free geometric/curvature parameter; SCRIPT-GREEN, needs grading | - |

## Refutation re-check detail (CONFIRMED/CANDIDATE)
- T001 forced coeffs: {'Milgrom1999 q=2 (=2cH, EXCLUDED 15.6sigma)': 2.0, 'Milgrom2020 q=1/2pi': 0.15915494309189535, 'Verlinde q=2pi': 6.283185307179586, 'Pikhitsa/KK O(1)/2pi': 0.15915494309189535} ; in-window=none ; closest Milgrom2020 q=1/2pi=0.1592 (gap 0.3488)
- T007 GHY/bulk etas: {'0.5000': 0.06666666666666667, '0.5774': 0.09090909090909094, '0.7071': 0.14285714285714282} ; in-window=none ; min rel dist to 0.3036=0.529
- Verdict: both CONFIRMED rows SURVIVE the adversarial re-check (no forced coefficient / ratio lands in-window).
