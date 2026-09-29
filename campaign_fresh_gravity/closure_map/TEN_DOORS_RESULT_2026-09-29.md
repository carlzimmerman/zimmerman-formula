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

## Appended note: what the independent referee lanes reproduced (2026-09-29)
This note supersedes the last caveat above (referee lanes pending); the caveat is left as first written.
Each referee re-derived one headline per door from the frozen criteria and README with its own code, opened the original lane's scripts only after its own runs were saved, and was re-run in place by a second session. None changed a verdict. Referees were not blind to the README numbers.
- Door 1 CFG151 (db335c0e7), door 4 CFG154 (2f6845de3), door 5 CFG155 (bdbcf3fe1), door 8 CFG156 (bb7bd135d), door 9 CFG153 (9ce8b61c5), door 10 CFG152 (7cb9ba39e): reported by the calc chat as reproducing their headlines, each with README-level corrections (for example door 4 counts about 237 independent tests, not about 36; door 9's A4 carries a background term A2/A3 omit; door 10's T0.4a label). Not re-verified here.
- Door 3 CFG157 (0bbd62cd7): reproduces T1.2 (1.310 / 1.016 / 0.434 / 0.063), B1 and T1.5; does not test T1.3, T1.4, Q1, G1c B2-B4, G2-G5 or O1, on which the scoped no-go mostly rests.
- Door 6 CFG158 (c868ad276): reproduces the cumulative-mass envelopes and the M^(1/3) exponent; three of the referee's own controls (EdS slope, shell-count and time-step convergence at a ~10% chaotic floor) fail and are kept.
- Door 7 CFG159 (a1fb4a128): every rule-(ii) miss agrees with CFG119 to 1e-7 to 1e-6; three of the referee's own frozen lines failed on definitions and rounding.
- Door 2 (CFG117): no referee lane.
- Door 11: the four time-flow sub-variants CFG172 (f1585212e) and CFG172D (249fa4ec8) are scoped no-gos; CFG188 (058296d6f) re-derived the field-equation core of 11C-a, b and c (21 AGREE, 5 CONDITIONAL, 1 NOT DONE, 0 DISAGREE). 11C-a and 11C-c pass the G1 law only through the declared kernel. 11C-d (CFG172D) has no independent re-derivation.
- The matrix above is unchanged. What the referees changed is how much weight the cells carry: several rest on definitions or on sub-lines the referees did not test.
