# CFG379 FROZEN CRITERIA: does the working model's supply limit set the cluster retention level? (zero new constants)

Written and committed ALONE before any script exists. Nothing below may change after this commit; later choices go in a labelled POST-FREEZE section of the README.

## Question
The working model (WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md, eq. 4): a host settles only the cold fluid its catchment supplies, and only up to its phantom target. Does

    r_pred = min( M_ph(<R_ap), S_catch ) / (5.364 M_b(<R_ap))

reproduce the measured retention levels (clusters 0.576, groups 0.60, Milky Way-like galaxy 0.14) with no new constant? kappa = 1/2 is FITTED. No dark-matter particle is added; the cold fluid's amount (Omega_c/Omega_b = 5.364) is still free, not derived.

## Inputs (on disk only; no downloads)
- **Clusters:** X-COP, all 12 in real_research/data/xcop (Ettori+2019 R500/M500 json; FGAS profile; HYDRO_MASS M_FORW; MSTAR_SMOOTHED where present, else M_star = 0.10 M_gas, as CFG371). Aperture R_ap = R500. M_b = M_gas(R500) + M_star(R500); M_tot = M_FORW(R500).
- **Groups:** Lovisari+2015, 20 groups, loaded exactly as cm02 (h7 slices, read-only): M_b = Mg500 + mstar500(M500), R_ap = R500, M_tot = M500 (b = 0).
- **Galaxy:** Milky Way-like, M_b = 6.5e10 Msun treated as enclosed inside R_ap = 30 kpc (the L191 / C003 anchor). M_b = 5e10 and 8e10 are reported as a sensitivity, not scored.
- **Phantom target (monopole, as CFG4/cm02):** M_ph(<R) = (nu_mono(y) - 1) M_b(<R), y = G M_b(<R)/(R^2 a0). Kernel nu_mono from cfg100_lib (copied, not edited).
- **Footings:** a0 = 9.3603e-11 and 1.1312e-10 m/s^2, run separately, never pooled.

## Supply (two catchments, both from the record; no new constant)
- **TA (turnaround catchment):** r_ta from cfg100_lib.r_ta_law(M_b, a0, z=0) (Delta_ta from the LCDM-background turnaround solver, z = 0). The matter that has turned around is M_ta = M_b nu(y(r_ta)) = (4 pi/3) r_ta^3 Omega_m rho_c Delta_ta; its cold share is S_TA = (5.364/6.364) M_ta. M_b is the aperture baryon mass (a declared lower bound on the host's baryons).
- **RC (CFG366/372 reservoir catchment):** a Gaussian catchment of comoving width R_c = 3 Mpc/h, at the cosmic mean cold density: S_RC = Omega_c rho_c0 (2 pi)^{3/2} R_c^3, Omega_c = Omega_m 5.364/6.364, Omega_m = 0.3153, h = 0.6736 (cfg100_lib values). A top-hat (4 pi/3) R_c^3 variant is REPORTED only.

## Measured levels and tolerance
- Class prediction = median over hosts of r_pred (MW: the single value).
- Targets: clusters 0.576, groups 0.60, MW 0.14.
- A class PASSES if |median r_pred - target| <= 0.10, OR (clusters, groups only) the median r_pred lies inside the 16-84% range of the per-host measured fraction f_A = (M_tot - M_b - M_ph)/(5.364 M_b) computed here at the same footing.
- Per catchment and footing: count of passing classes (0-3).

## Verdict
- **PREDICTS:** at least one catchment passes 3/3 on BOTH footings.
- **PARTIAL:** best catchment passes >= 2/3 on both footings, or 3/3 on one footing only.
- **FAILS:** otherwise.
- Two catchments are tried; a pass under one is labelled with that catchment (look-elsewhere disclosed).

## Reported, not scored
- **Binding constraint per host:** TARGET if M_ph < S, else SUPPLY; counts per class, catchment and footing.
- **Bookkeeping check B (the working model's own accounting).** In the working model the gravitating mass beyond the baryons is all cold fluid, and the target caps it: M_tot - M_b <= min(M_ph, S). The measured f_A is the mass BEYOND the law (definition A, cm02). Report the fraction of hosts with f_A > 0 (cap violated by the data) and the measured total cold content r_tot = (M_tot - M_b)/(5.364 M_b). If the cap is violated in most clusters and groups, the README must say that the literal comparison (r_pred vs the definition-A levels) compares different quantities and that the cap, read in the model's own bookkeeping, is contradicted by the data.
- A mass sweep of r_pred over M_b = 1e10 .. 1e15, with the MOND radius sqrt(G M_b/a0) as the aperture, reported only.

## Controls (must pass)
- C1: X-COP median f_A (canonical) at R500 reproduces the ledger's 0.576 within 0.10.
- C2: Lovisari median f_A (canonical, b = 0) reproduces cm02's 0.549 within 0.02.
- C3: turnaround identity M_b nu(y_ta) = (4 pi/3) r_ta^3 Omega_m rho_c0 Delta_ta(0) to 1e-6 relative, both footings.
- C4: the min rule's limits: S -> infinity gives r_pred = M_ph/(5.364 M_b) exactly; S = 0 gives 0.

## MUTATE (CFG379_MUTATE=1, separate outputs *_MUTATE)
- Supply x10 in both catchments, everything else identical.
- **Declared flip:** at least one catchment's verdict (pass count, either footing) must change, OR the binding constraint of the cluster class must change. If the lane headline does not change, that is disclosed (as CFG370 did), not hidden.
- MUTATE exits rc 1.

## Caveats declared now
Hydrostatic masses (no bias); monopole phantom; MW enclosed baryons as a point mass; definition-A levels are aperture values; Delta_ta from the LCDM background solver as in CFG100; supply at the cosmic mean density (no prior clustering of the cold fluid). This is not "theory closed".
