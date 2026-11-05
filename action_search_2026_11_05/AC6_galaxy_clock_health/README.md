# AC6: AC2's dark-energy clock inside galaxies — AC2 (unswitched) ILL-POSED; switched AC2s bounded

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (4ae1062cfc),
frozen before any graded number. Script: ac6.py. Runtime 24 s (12 parallel workers, H4's solver).

## Result

**The clock's khronon charge is rho_eff = div P + phidot^2** (A1, exact sympy identity: the sigma
equation is a continuity equation with time density div P + s^2(1+sigma_t)/(1+phi)^2 and flux density
div P + s^2; the clock also gravitates with density s^2(1+sigma_t)^2/(1+phi)^3).

**Dispersion** (A2-A3, H4's frozen-background WKB system with the clock in place of the dust):
the UV limit is omega^2/k^2 -> gamma rho_0/(1 + gamma s^2). Wherever rho_0 = div P + s^2 < 0 the
growth rate is Gamma ~ k: Hadamard ill-posed, exactly H4's mechanism. Known answers: H4's dust system
rebuilt here reproduces H4's A4 dispersion identically; s -> 0 reproduces H4's mu_K = 0 form identically.

**The clock cannot fill the negative regions.** Framework-native rho_DE = a0^2/(kappa^2 c^2 G) is
8.63e-8 (canonical) / 1.26e-7 (alt) Msun/pc^3, and a canonical clock with V >= 0 has phidot^2 <= 2 rho_DE.
With H4's own solver (known answer: H4's stored S2 medians reproduced to 0.0), negative-charge regions
remain at 1+w = 2, on both footings with converged maps, in 6 of 7 systems: MW-M31, a galaxy pair, a
cluster pair, the MW-like and dwarf discs in an external field, and a single galaxy in a field. Medians
4.4e-8 to 1.0e-4 Msun/pc^3. Isolated discs with no external field have none, as in H4.

**Switched form AC2s** (stiffness off where D.P < 0): omega^2 -> K rho_0 (M_theta - 1), k-independent
(A4). Illustrative bounded rates at x = 1: 0.09-0.79 e-folds per Gyr; at the deep-MOND x of real lobes
the rate scales as sqrt(2x) and is smaller (H4: 0.006-0.20 e-folds over region lifetimes). Not graded.

## Checks

Main: A1, A2, A3, A4, B0 PASS. Label by the frozen lines: **AC2 ILL-POSED (unswitched); AC2s bounded.**

MUTATE (AC6_MUTATE=1, sign of the first-order term flipped, separate outputs): the isolated discs,
clean in the main run, become ill-posed, so the control bites. Its B0 known-answer check FAILS (0.224):
my stats() applies the mutated sign to region selection, so it reads positive regions while H4's stored
medians are negative-region ones. That is a defect of the control's implementation, recorded as run;
it does not enter the main result. The Solar-System row (H4's S7) was not recomputed here; H4 has it at
D.P >= 0.045 Msun/pc^3, far above phidot^2, so it is healthy in AC2 as well.

## What this means for the action route

AC2 as written (smooth, unswitched stiffness) repeats v3's saddle ill-posedness: replacing the dust by
a dark-energy clock does not help, because the clock's inertia is about rho_DE and the phantom's negative
regions are deeper. The switch is required. The next question is where AC2s puts the switch: on D.P
(as v3s) leaves a knife edge on FRW, where D.P = 0 exactly; on D.P + phidot^2 keeps AC2's FRW results
but adds a phidot-dependent term. Neither is graded here.
