# CFG345: does candidate B's cold component clump like CDM on the scales CFG344 needs? FROZEN CRITERIA

Owner: "check if the cold component clumps like CDM". Written before any script exists. Paths are relative to the repository root.
The cold mass (Omega_c h^2 = 0.120) is still required. No dark-matter particle species is added; the cold component is described only as the record describes it. kappa = 1/2 is FITTED.

## 1. What CFG344 needs (read, not re-derived)
- `campaign_fresh_gravity/CFG344_postreion_cold_accretion/cfg344_accretion_results.json`, key HIST: M_cool(z_f = 8) = 3.83e7 Msun (primary threshold M_need), growing to 5.75e8 Msun by z = 2. M_cool(z_f = 10) = 2.84e7 and M_cool(z_f = 6) = 5.59e7 are reported as sensitivity, not decision rows.
- CFG344 used collisionless-CDM sigma(M) (colossus planck18, EH98). Its caveat (3) is the question here.

## 2. Inventory (from the record only)
Sources: `campaign_fresh_gravity/STANDING_2026-09-29.md`, `campaign_fresh_gravity/CFG4_README.md` (T5), `campaign_fresh_gravity/CFG288_one_field_dark_sector/` (README, FROZEN_CRITERIA), `campaign_fresh_gravity/CFG293_wavefield_cores_satellites/README.md`, and the record's memory notes on FL1-FL3/FK1, the condensate mu-pincer (v9 DBI), GP0-GP5, and the Ly-alpha forest b-cutoff correction.
For each specification the README records: (a) status for B: CURRENT (what B as frozen says), CONSTRUCTION (live, not adopted by B), or DEAD/SUPERSEDED; (b) small-scale behaviour (cutoff scale/mass or none); (c) the parameter that sets it and whether the record fixes it.

## 3. Computations (standard formulas; PROVISIONAL where transcribed from memory)
Cosmology: Planck-2018 (Omega_m = 0.315, h = 0.674, Omega_c h^2 = 0.120); mean comoving matter density rho_m = 2.775e11 h^2 Omega_m Msun/Mpc^3. A wavenumber k maps to mass M(k) = (4 pi / 3) rho_m (pi / k)^3 (half-wavelength radius).

**Wave field (CFG288 road W = FL1's order parameter), mass m, m22 = m / 1e-22 eV:**
- Transfer: Hu, Barkana & Gruzinov (2000) T(k) = cos(x^3)/(1+x^8), x = 1.61 m22^(1/18) k / k_J,eq, k_J,eq = 9 m22^(1/2) Mpc^-1 (as transcribed in CFG288's frozen criteria).
- Half-mode mass, DECISION convention: k at which T^2 = 1/2 (power halved; the more suppressive, i.e. larger-mass, of the two common conventions). Reported alongside: T = 1/2 (Schive+2016 convention).
- Jeans mass at z = 6, 8, 10 from the comoving quantum Jeans scale k_J(a) = a (16 pi G rho_m(a))^(1/4) (m c / hbar)^(1/2) (physical, then times a; reported, not deciding: the half-mode mass is the history-integrated cutoff).
- Bound: the m at which M_1/2(T^2 = 1/2) = M_need; checked against the record's window [2e-20 eV (Ly-alpha floor, Rogers & Peiris 2021 as quoted in CFG288), 37 eV] and the record's L383 dwarf-heating floor 2-5e-19 eV (reported by CFG288 / FL2).

**Pressure-supported condensate dust (CFG288 road S, ghost-condensate P(X), scale M):**
- c_s^2 = rho_d / (4 M^4) (CFG288 README line on road S), rho_d = cold density at z; comoving k_J(z) = a sqrt(4 pi G rho_d) / c_s.
- Decision quantity, conservative: M_J at z_eq = 3400 (the mode must be free to grow through the whole matter era to match CDM), and lenient: M_J at z = 8. Bound on M from M_J(z_eq) <= M_need. Checked against the record's own requirements on M (G-DUST M >= 4.24 eV; G-ONSET M >= 3.3 keV).

## 4. Decision (verdict on B, read across every non-dead specification)
- **CDM-LIKE:** B as frozen specifies no cutoff, AND every live construction's cutoff mass (decision convention) is below M_need = 3.83e7 Msun for every parameter value the record allows.
- **CONDITIONAL:** CDM-likeness at M_need holds only if an unfixed parameter of some live construction satisfies a stated bound, and that bound is not excluded by the record (it lies inside the record's allowed range).
- **SUPPRESSED:** the record's own specification (for B as frozen, or for every allowed value of every live construction that B would need) forces a cutoff above M_need, so CFG344 fails.
A DEAD specification is listed but never decides.

## 5. Ly-alpha forest reading (record only, no downloads)
State what the record's forest content constrains about small-scale power at z = 2-5 under B: the Rogers & Peiris floor as quoted, CFG288's loose forest criteria (T^2(10 h/Mpc, z = 3) >= 0.5; c_s(z = 3, 10 h/Mpc) <= 5 km/s), and the b-cutoff lane (which concerns diffuse gas, withdrawn 6-8 sigma -> 0.4-0.9 sigma calibration). Convert the forest's reach (k = 10 h/Mpc) into a mass with M(k) and compare with M_need. This section does not change the verdict.

## 6. Controls (main run must pass all; failures kept and disclosed)
- C1: the HBG transfer with T^2 = 1/2 reproduces Hu+2000's k_1/2 = 4.5 m22^(4/9) Mpc^-1 within 5% (PROVISIONAL reference, from memory).
- C2: the T = 1/2 convention reproduces Schive+2016's M_1/2 = 3.8e10 m22^(-4/3) Msun within 10% (PROVISIONAL reference, from memory).
- C3: the Jeans formula of section 3 at z_eq reproduces CFG288's k_J,eq = 9 m22^(1/2) Mpc^-1 within 15%.
- C4: the road-S formula reproduces CFG288's committed k_J(z = 1100) = 2.2 h/Mpc at M = 4.24 eV within 10%.
- C5: M_need read from the CFG344 JSON equals 3.83e7 Msun to 1%.
- MUTATE (env CFG345_MUTATE=1, outputs with suffix _MUTATE): the wave-field mass set to the record's most suppressive allowed value, m = 2e-20 eV, and road S to its record minimum M = 4.24 eV (G-DUST). If either then gives M_1/2 or M_J(z_eq) > M_need, it is FLAGGED as suppressing at that value (expected for road S at 4.24 eV; for m = 2e-20 eV it is the question).

## 7. Lean
Certify, over rationals with Mathlib and no sorry: (i) the wave-field bound as m22^4 vs (A / M_need)^3 for the computed coefficient A (rounded outward), including whether m22 = 200 (2e-20 eV) passes or fails and that the L383 floor m22 = 2000 passes; (ii) the road-S bound on M relative to the record's 3.3 keV onset requirement.

## 8. Hand expectations (mine, before any code)
- HE1: B as frozen (T5 identity; STANDING) specifies no microphysics, hence no cutoff.
- HE2: the wave-field half-mode mass at 2e-20 eV is a few e7 Msun, comparable to M_need; the bound sits near 2-3e-20 eV, inside the window, below L383's floor.
- HE3: road S at 4.24 eV suppresses heavily; at the record's 3.3 keV onset requirement it is far below M_need.
- HE4: expected verdict CONDITIONAL. The forest reaches only ~1e9 Msun at k = 10 h/Mpc, so it cannot by itself confirm CDM-like power down to 3.8e7.
