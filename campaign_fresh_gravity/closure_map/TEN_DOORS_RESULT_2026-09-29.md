# Ten doors: result (documentary, no new physics; 2026-09-29)
Gates G1-G5 as in TEN_DOORS_GATES_2026-09-29.md (5ef77ea09). F = FAIL, P = PASS, U = UNDEFINED, N = NOT ADDRESSED. "p*" = passes only as a statement or trivially. Every FAIL is a scoped no-go on the frozen model class only; nothing here says the theory is closed or that any data favour it.

| Door (lane, commit) | G1 | G2 | G3 | G4 | G5 |
|---|---|---|---|---|---|
| 1 Mashhoon kernel (CFG120, 9e4757627) | F | F | F (Bianchi); a,b p* | F | F (Solar System); b U |
| 2 Verlinde (CFG117, bb504274c) | F | U | U | P (count only) | F |
| 3 dipolar DM (CFG121, 16fca9acd) | F | F | F | F | mixed: V_U P only via a cap that fails G1c; V_B F (literal rule) |
| 4 superfluid (CFG122, b7d41c302) | F | U | F | F | F |
| 5 f(E,L) (CFG130, c1d719fbf) | realisable, not a mechanism | N | N | P | N |
| 6 secondary infall (CFG118, d0baef700) | F | p* | p* | P (no new constant) | p* |
| 7 fuzzy DM soliton (CFG119, 435cb43e9) | F | F | p* | F | p* |
| 8 interacting vacuum (CFG131, aa0d95aef) | F | F | p* (trivial; energy F beyond x=6.29) | F | p* |
| 9 Deser-Woodard/RR (CFG123, 9e4757627) | F | F | p* (vacuous) | F | F |
| 10 mimetic (CFG124, 9e4757627) | F | class A P; others F | A-D p* (no coupling); contact coupling F | F | F for C, D, E1; class A P |

## Binding failure per door
1 R proportional to M_b (kernel is linear): a sqrt(1000) mass spread. 2 Point mass gives C_V/C_target=(1+x)/x, not within 10% anywhere. 3 Medium budget needs Q^2/kappa_I >= ~140 vs <= 0.16 (V_U) / 1.2 (V_B) from growth. 4 Both branches miss the target; the MOND branch has c_s^2<0. 5 f>=0 exists but is fixed by the target, so it encodes C(r), not derives it. 6 Radial scale follows the turnaround (M^0.33), not r_M (M^0.5). 7 Cores are flat vs the target's 1/r; growth needs m >= 1.28e-20 eV. 8 Forced EOS p(rho_c) differs 32-353x from the required one across 1e9-1e12 Msun. 9 Localised RR response is a negative density ~10 orders too small, signature (2,2). 10 No stationary state; c_s^2=gt/(2-3gt) is a ghost for 0<gt<2/3.

## Not tested (each lane's README has the full list)
Relativistic completions (1, 3, 5, 6, 10), non-spherical baryons (all), nonlinear/post-caustic cosmology (4, 6, 8, 9, 10), a non-Lorentz-invariant vacuum or derivative coupling (8), self-interactions (7), Hossenfelder's covariant Lagrangian (2), whether f(E,L) is reached or stable (5), Boltzmann-code CMB (3, 8), a Schwinger-Keldysh completion (9), rotational dust (10).

## Cross-door pattern (a READING, not a theorem)
Where cold matter is dynamical (6, 8, 10), its scale comes from the turnaround, the particle mass, or a free time scale, never r_M proportional to M^(1/2). One reading: the missing object must itself carry an acceleration scale. Doors 1, 3, 4 and 9 fail for different reasons and are not covered by this reading.

## Caveats
- The menu of doors was written knowing the target, so the doors are not a blind sample of the theory space.
- Door 5 shows realisability only; it says nothing about mechanism, reachability or stability.
- Doors 5 and 8: the frozen question preceded the scripts by file times but was not committed first.
- Literature facts in the lanes are from memory and unverified.
- The seven independent referee lanes CFG150-156 are pending; an appended note will say what reproduced.
