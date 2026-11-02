# VW1_velocity_window: FROZEN CRITERIA, committed alone before any script or number

Launched under the owner's 2026-11-02 instruction to launch search lanes without asking. It runs under `OWNER_DECISION_2026-11-02_FERMION_EXPERIMENT.md` as a side read of HF1's model; it adopts nothing and changes no HF1 line or label. κ = ½ FITTED. No ΛCDM input in a grade. Not theory closed. Nothing here says the data favour the framework.

**Not blind.** HF1's Fermi-Dirac cells at m 7 to 11.8 eV are read (all fail gate 1). My hand estimate before this file: the disc limit needs a velocity today near 2 km/s, thermal 11 eV has about 14 km/s, and the primary CMB may survive near 2 km/s while small scales don't. Rough, order of magnitude, and on record so it can be wrong.

## Question
HF1 scans m on one thermal spectrum. But a phase-space limit and linear growth depend on two things only: the peak phase density Q, and the velocity today v0, tied at fixed abundance by Liouville. Is there any v0 that keeps the fermion out of massive discs by its phase-space limit and also passes gate 1? This doesn't depend on m, spin or production, apart from the spectrum's shape.

## Stage A: the slowest v0 discs allow
- HF1's R4 profile and solver, on SPARC with lg M_b >= 10, same quality cuts as CRG1's SPARC set, canonical footing primary, alt beside, Υ disc 0.5, bulge 0.7, fair share 5.2715.
- Requirement, from RM2: M_f(<R_last) <= f_hi x 5.2715 x M_b(<R_last), f_hi = 0.2. RM2's bound is on a different halo form, stated as a liability. f_hi 0 can't be solved; 0.4 and 0.1 are reported beside.
- For each galaxy, the m at which equality holds, on a log grid of m, g_f = 2, gives Q_i = m^4 g_f / (2 h^3). Q_max is the median; 16th and 84th percentile are reported.
- Liouville: the primordial peak phase density can't sit below what the halo needs to be capped at, so the exclusion needs Q_primordial <= Q_max. With a Fermi-Dirac shape of parameter u = T/m and peak Q, rho_mean = 45.3 Q u^3 (the integral stated in the script), v0 = 3.15 u. So **v_min = 3.15 (rho_mean / (45.3 Q_max))^(1/3)**, omega_f from Stage B's best cell; the dependence on omega_f is printed. The Maxwellian and top-hat shapes are reported beside it as the shape bracket.

## Stage B: the fastest v0 gate 1 allows
- HF1 gate 1's machinery and line unchanged (A1 R2: RF5's p >= 1e-3 gates, G-A0, S - S_min <= 25 against 2324.03). Fermi-Dirac spectrum at fixed u, with degeneracy free to carry omega_f, so number isn't thermal. m 100 eV sets only CLASS's numerics, since at fixed u and omega_f the result doesn't depend on m.
- Grid in v0: 0.25, 0.5, 1, 2, 4, 8 km/s, slow to fast, each starting from the last. v_pass is the largest v0 passing, read between grid points only as a range. Grid stated before any cell.
- YHe follows HF1's CLASS default; a cell that stops on the helium table is UNDETERMINED.
- Reported, not graded: P(k) ratio to the slowest cell, the k where it halves, at z 0, and the raw forest's k range beside it. Gate 4 is what would grade this; no forest verdict here.

## Labels
- **WINDOW EMPTY**: v_min above the upper edge of every passing range, at the median Q_max and also at the 84th percentile's v_min bracket stated beside it. The family "light fermion kept from massive discs by its phase-space limit, on this fair share and RM2's f_hi" fails gate 1 for any m and any spectrum of this shape. A family result on these inputs, not a no-go theorem.
- **WINDOW OPEN at [v_min, v_pass]**: both hold at once. It isn't a pass of anything: clusters, galaxies and structure are still ungraded there, no production mechanism exists, and MW and IC 1613 stay with the law. It names what a spectrum has to do.
- **NOT SEPARATED**: the 16th-84th bracket on v_min straddles the edge.
- Any failed control: NO VERDICT.

## Controls
Known answers: slowest cell near RF5's R1 (S - S_min small, its own number printed; line |Δ| <= 25). The m independence: at one fixed point, m 100 and m 400 eV at the same u and omega_f agree in plik within 1.0. HF1's FD m 11.8 eV u, thermal, reproduces HF1's plik at its own parameters within 1.0. Rho_mean's integral against numerical quadrature within 1e-4. Stage A at a planted Q returns it within 1 %. MUTATE: f_hi wrong by 16 must move v_min by the expected 16^(1/3) only if the cap binds in the same way, printed; written to separate outputs.

## Rules
Post-result changes go in an amendment, disclosed as such. No data downloads. Nice 10, one thread per fit, no more than two fits at once while the searches run; delete nothing; disk about 20 GB free.
