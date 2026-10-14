# CFG768 FROZEN CRITERIA: the NGC 1052 trail with alpha taken from the record's own dissipation and formation physics

Committed alone, before any CFG768 script exists. Block CFG760–769 (owner chat; CFG768 confirmed free: no LEDGER row, no
directory). Owner request (owner chat, 2026-10-14): "derive it then based on my framework", route chosen: "derive alpha from
P-waves".

kappa = 1/2 FITTED; both footings (9.3603e-11 / 1.1312e-10), never pooled; no-EFE nu_mono as in CFG655/657; the cold energy's
mass is required; no particle species; not "theory closed".

## Question
CFG657 left the trail KNOB (alpha): the drift coefficient alpha (CFG541 V5, free O(1)) decides it, and channel D (drift capture)
carries > 99% of every captured fraction. Can the framework fix the supply of DF2, DF4, DF9 (collision debris) and LEDA 4014647
without alpha or the van Dokkum+22 label, using only what the record already derived?

## Inputs (read only, no new data)
- Galaxies, bounds, f_min: CFG657's GAL table and CFG655 R2 bounds (DF2 0.36/0.33, DF4 0.29/0.26, DF9 0.52/0.46, can/alt);
  LEDA f_min 0.2263/0.2025 (CFG657 results). f is the same quantity in every lane: sigma^2 = sigma_N^2 [1 + f (nu - 1)].
- CFG657 capture code (function definitions copied by exec of the file's text above its estimator section; no edits).
- P-wave gap: CFG760 geometry (r_M = sqrt(G M_b/a0), ell = L*^2/(2 r_M), s0 = r/ell, V = 2 V_f, L* = 5.754 pc), CFG767's
  certified deep-limit c_P,max = V/(x_e sqrt(2 s0)), CFG761's generous x_e = 0.71, c_P,min = r/13.8 Gyr (CFG760's lenient rule).
- One-c_P constraint: CFG762 (SPARC needs c_P >= 7.67 km/s can, max c_P,min; the record has no shared c_P).
- Clocks: CFG763 universal tau in [0.72, 3.47] Gyr can / [0.83, 3.47] alt; CFG764 orbital tau = k t_orb, k in [0.46, 1.20] can /
  [0.52, 1.20] alt, t_orb = 2 pi r / V at the measured radius. Here r = r_1/2 (CFG655 estimator, 4/3 R_e) and V = sqrt(3) sigma_obs
  (Wolf). Lenient end for debris = the LONGEST orbit (sigma_obs - lower error, floored at 1 km/s); for LEDA = the
  shortest orbit (sigma_obs + upper error).
- Ages: CFG657 SED ages (DF2 8.28 -2.07, DF4 10.68 -1.38, DF9 10.36 -1.61, LEDA 11.54); lenient debris age = age - 1 sigma, and
  also CFG657's collision-time low end 6 Gyr if smaller; LEDA lenient = age + 1 sigma.

## Part A: alpha from P-wave dissipation
A1. Per galaxy and footing, at r = r_1/2 and r = R_c (CFG657 capture radius): c_P,max, c_P,min, window OPEN iff c_P,max >= c_P,min.
A2. One c_P (the record's rule: c_P is one constant for every system). The trail windows are compared with CFG762's SPARC
    requirement. If every trail c_P,max < the SPARC c_P,min (7.67 km/s can; alt from CFG762 json), P export is unavailable in the
    trail for any c_P that serves SPARC => **alpha_P = 0 (DERIVED, conditional on one c_P)**.
A3. With alpha_P = 0, channel D vanishes; f_cap = S + F at CFG657 primary inputs, and the maximum over CFG657's one-at-a-time
    brackets (alpha excluded). Verdict A:
    - **REPRODUCES** iff each debris f_cap <= its bound AND LEDA f_cap >= f_min, both footings;
    - **LEDA UNSUPPLIED** iff debris pass but LEDA f_cap < f_min at every bracket end (both footings);
    - **NOT DERIVED** if A2 does not close (some trail window overlaps an allowed shared c_P).
    Hand estimate (written before any run): S + F <= 2e-3 everywhere -> LEDA UNSUPPLIED.

## Part B: formation at rest (the record's surviving assembly picture, CFG760 Reading 4)
B1. f = 1 - exp(-t/tau). Universal clock: debris f_lo uses tau_max = 3.47 and the lenient (smallest) age; LEDA f_hi uses tau_min and
    the lenient (largest) age. Orbital clock: same with k_max/k_min and the lenient orbit.
B2. Per clock and footing: **CONSISTENT** iff every debris f_lo <= its bound AND LEDA f_hi >= f_min; **EXCLUDED (debris
    overfilled)** iff any debris f_lo > its bound. Report the Z of each debris galaxy at f_lo (CFG655 estimator, sigma only for
    scoring).
    Hand estimate: universal f_lo(DF2) ~ 1 - exp(-6.2/3.47) = 0.83 > 0.36; orbital t_orb(DF2) ~ 1.1 Gyr, f ~ 1 -> both EXCLUDED.

## Overall
- If A = LEDA UNSUPPLIED and both clocks EXCLUDED: **the framework's own assembly physics does not reproduce the trail**: it
  predicts the old debris should hold the law's cold energy, and the data say they do not (CFG655: law fails DF2/DF4 at 4.4–4.9
  sigma). Then name what would be needed (a formation condition the debris lack), without fitting one.
- Any other combination is reported as found.

## MUTATE (separate outputs, CFG768_MUTATE=1; exit 1 iff both teeth bite)
- M1: vacuum curvature off (no gap): c_P,max -> infinity for every trail case; A2 must then fail to close.
- M2: all four ages set to 0.3 Gyr: the universal clock must then give every debris f_lo <= bound (verdict B flips for it).

## Not tested
EFE variants (CFG655 frame kept), non-first-order formation, the FG001 ownership reading (named in the README, not scored),
formation microphysics (astra F1/F5).
