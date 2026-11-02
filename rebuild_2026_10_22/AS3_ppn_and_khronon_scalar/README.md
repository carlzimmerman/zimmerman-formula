# AS3_ppn_and_khronon_scalar: (1) v9's alpha_1 = -2(K_B+2) is an ARTEFACT for a moving source, and its ladder rests on a broken unit constraint. (2) The khronon + scalar + (D^2 chi)^2 corner is v3's scalar pair: order disagreement resolved for H1, Q2 and Ostrogradsky pass, FRW growth and H4 fail

**Part 1, frozen label ARTEFACT.** For a source moving through the aether, the exact solution of v9's linear system is linear GR with G = G~: alpha_1 = alpha_2 = 0, for every K_B, J_Y, K2, Q0 and v != 0. Physical branch: moving. `-2(K_B+2)` is real arithmetic, 8(G~/G_static - 1): bare gravitomagnetism over a static potential. It describes no moving solution, because the static charge can't ride the source. **That doesn't make v9 viable.** The failure moves: G_static/G~ = 2.00 to 2.29 at J_Y = 1, K_B <= 1/4 (not graded), and the law goes for moving systems, as in O1's velocity screening [REC, khronon family].

**PAPER67's sentence needs a correction, as does STANDING line 298.** I edited neither. Wording to offer, owner's call: "v9, an AeST embedding, is recorded with alpha_1 = -2(K_B+2), but that is a static-branch ratio. A source moving through the aether has alpha_1 = alpha_2 = 0 at G = G~ (AS3), and v9 then loses the law for moving systems."

**Part 2.** Not a candidate. AS2's reading that this corner reshapes the "untwisted fails growth" horn doesn't survive: its growth is M1's kernel exactly.

| gate | result | margin, both footings where a0 enters |
|---|---|---|
| Order n against n^2 | **Resolved: H1 is right, as2_indep's I3b block is wrong** | Gamma^2(k -> 0) = 4 pi G rho, 0.99990 at k = 0.01 mu; 0.999975 with the missing term |
| Ostrogradsky | **PASS, candidate** | one root pair, Krein +; control (box phi)^2 gives degree 6 and Krein - |
| Q2 with stiffness | **PASS, candidate** | \|Q2\|/Hees at most 3.5e-8 canonical, 2.5e-8 alt at the floors (margin 2.8e7, 4.0e7); 2.0e9, 2.5e9 at 90 pc. Second implementation within 0.18 % |
| FRW background, literal K | **FAIL** | needs mu >= 1.76e8 h/Mpc; stiff/one neutrino at 1 MeV 8.4e18, 7.6e17 at mu 0.03, 0.1 /Mpc (line 0.5). DBI carries Q7's cure [REC] |
| FRW growth | **FAIL** | sigma8 ratio 0.0757, 0.0817 at the guard (line 0.95, ODE upper bound; Boltzmann 0.0032, 0.0052 [REC X4]); 0.959 at 411 h/Mpc. Linear FRW has no a0: same on both footings |
| H4, literal | **FAIL** | same unbounded rate. MW-M31 lobe, lambda 1 pc: 180 / 199 e-folds in 10 Gyr. Switched form 0.19 / 0.20, reported only |

Planets at the floor: Mars 0.212 / 0.190 of C6's bound. The floor is D10's AQUAL number, not re-derived for this equation.

kappa = 1/2 FITTED. Footings never pooled. No dark matter particle. The cold sector stays retired; nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. Foster-Jacobson formulas and bounds from memory, PROVISIONAL; only the paper's title and reference were web-read. Criteria 9581518967, alone first, not blind, with my hand expectations in them, so nothing here is a blind find.

## Part 1, derivation
On Minkowski every extra term is a product of two quantities that vanish on the background, so first-order pieces give the exact quadratic action (`as3_block.py`, no shared code). L = R - (K_B/2)F^2 + 2c a.V - c(1+J)V^2 + K2 dQ^2, c = 2 - K_B, V_i = d_i pi + Q0 A_i, a_i = d_t A_i + d_i Phi. Source T^ab of moving dust, omega = k.v, gauge B = e = 0 after variation.

**Known answer.** At 6 random rational points Einstein-aether gives Foster-Jacobson alpha_1, alpha_2 and gamma = 1 with residual exactly 0, all six field equations satisfied. The response's pole is exactly the spin-0 speed s0^2, so FJ's 1/c123 is the v^2/s0^2 term of a Taylor series valid for v < s0. That is the key: FJ's formulas assume a subsonic source.

**AeST moving response (k = 1, 16 pi G~ = 1):**
- Phi = (2v^2 - 1)/4, Psi = -1/4: GR's, all six rows zero; block determinant nonzero, so unique.
- Aether: A_z = Phi/v, so d_t A_z + d_z Phi = 0. It falls freely. Size U/v, not the U v of FJ's expansion.
- Scalar: pi = i Q0 A_z, so V = 0, dQ = 0: phi = Q0 tau.
- Vector sector: B_x = -4 U~ v, A_x = 0.

**Why.** The aether equation makes Sigma = div(K_B a + c V) (with its K(Q) companion) a conserved, transported charge with zero sound speed: the double zero root in the dispersion. A source moving through the aether leaves its charge behind. Time-domain check C1: Phi at the source is bare + frozen pattern to 1e-6. Control C2: with c2 > 0 and v < s0 the source keeps the static value (-1.487 vs -1.497).

**Exact, beyond linear.** F_munu = 0, phi = Q0 tau with tau geodesic gives zero value and zero first variation of F^2, a.V, Y under arbitrary perturbation, checked on Schwarzschild at E = 1, 13/12, 5/3 (B1), given F_Q(0, Q0) = 0 and finite F_Y. So GR plus a geodesic aether is an exact branch while the congruence is single-valued. Mutated congruence fails (B2).

**Static limit.** At omega = 0 the block drops to rank 3 of 4, and U_static gives alpha_1 = -4(2 + K_B J)/(1 + J) from bare B_x over U_static, exact; -2(K_B+2) at J = 1; -4 K_B at J -> oo. So omega -> 0 and omega = 0 differ: the limit isn't uniform.

**Why the record got a regular series: a defect.** `route2_v2_build.py` imposes the unit constraint to O(eps) only. That drops the Q0^2 A_L^2 term in Y (record's a1b*a1k = 0; must be -144/125 at its test point) and gives its block rank 10 of 10, lifting the flat direction artificially. Repaired in a copy (O(eps^2) A_0), the same code gives rank 9, null vector the flat direction, **no solution at orders 0 and 1 for w along k**, and U = 16 pi/5, which is my U_static at q = 2/5. This is why K3b fails. FC_AEST_STATUS had named that piece as the blocker for the FC chassis, but the v9 build didn't carry it. So the record's alpha_2 values and its c_-2/q^2 term on this action are void. Its novel-channel alpha_2 (wf2_target2) I did not rerun; on the moving branch dQ = 0, so that channel carries nothing there.

**Margins at the Sun.** Moving alpha_1 = alpha_2 = 0 exact on both footings (a0 absent). Charged-background (Jeans) correction estimated with an upper local density 0.1 Msun/pc^3, as alpha ~ fraction/w^2: at most 4.5e-10 at 220 km/s, 9.58 AU; 6e-13 at 369 km/s, 1 AU (bounds 4e-5, 2e-9). Capture radius GM/w^2: 0.018 AU at 220, 0.0065 AU at 369.

## Part 1, limits
- **The aether's local rest frame isn't fixed by v9.** At 20 km/s (aether co-moving with the disc) capture is 2.2 AU and planets may sit inside it. The source then has w near 0 in the aether frame, so a preferred-frame test has no lever, but this is an argument, not a solve. The frozen rule was set at 220 and 369 km/s.
- **Unsolved:** the wake caustic behind each mass, where the congruence crosses (O1 flags it); interiors and strong-field bodies inside capture, so isolated-pulsar and solar-spin alpha_2 bounds aren't covered; comparable-mass binaries, where capture is about the separation.
- **K3b FAILED on the record's own action,** explained above. Frozen label kept.
- **Not v9: FC-AeST + c2*.** There s0 is about 0.37 at K_B = 1/5, J = 1, so the static branch is real for v << s0: alpha_1 = -22/5, alpha_2 = 11/2 at Q0 = 0, exact. So that chassis's kill stands in kind. The record's numbers there (11, 10) differ from 11/2 by about 2; unresolved, and I didn't chase it.
- AS2's G5 requires the static branch too, so its K_B = 1/2 FAILs on G5 are too strict for rows with no sound speed. Not rerun.

## Part 2, details
**Order.** Newtonian-gauge reduction, 16 pi G = 1: omega^2 = (rho_tau/4)(2k^2/Z - 1), Z = 2mu^2 + 4k^2/D, D = 2(1+S) + L^2 k^2 - nu, nu = n/(2 Q0^2).
- as2_indep's committed determinant is reproduced by hand (ratio constant). Adding -(n/2)(grad B)^2 gives 0.999975.
- Exact L2 on EdS dust FRW in unitary gauge, mapped to Newtonian variables, produces that term: coefficient of theta^2 at fixed chi is -(rho/2) a k^2, relative difference 5e-5 at k/aH = 300. Tadpoles vanish on Friedmann. So I3b's Minkowski swindle dropped the second-order image of a tadpole, and its n^2 isn't the k -> 0 answer. Real n^2 appears only at k >> mu, through nu.
- At nu -> 0, S = 0 the bracket is exactly H4's k^2/chi and M1's s = mu^2/(k^2 + mu^2); k_c = 242.75 mu at L = 24 pc, H1's number. On EdS the reduced action's equation is M1's ODE, worst 4.5e-10.
- as2_indep's I4b factor 2 also resolves: its ODE carried L^2 where the action gives L^2/2.

**Ostrogradsky.** D^2 phi in unitary gauge has no time derivative, so no phi_ddot, h_ddot. At large k omega^2 -> c^2 k^2, hyperbolic. The record's ghost comes from the time partner, reproduced as a control.

**Q2.** chi-hat = -4 pi GM/(S_perp k_perp^2 + S_par k_z^2 + (L^2/2) k^4), so Q2 = sqrt(2) GM/L^3 x Int_-1^1 (1/2 - 3u^2/2) sqrt(S_perp(1-u^2) + S_par u^2) du, E0-E3. Linear to 5.6e-6. Second implementation: axisymmetric finite differences, ell = 2 projection. It computes a static branch; a moving Sun sees less.

**FRW.** Stiff/dust = d/2, independent of Q0. Q6's line reproduced, 1.76e8 vs 1.84e8 h/Mpc. M1's 0.391 reproduced (0.3908) and X4's ODE numbers, on the record's own background and P(k), used as a known answer only, not a yardstick. Static mass term has the H2/S4 form, and my pole estimate gives mu <~ 0.12, 0.11 /Mpc at 1 Mpc. That guard stays [REC S4]; not re-graded on lensing.
- **nu door closed.** nu > 2 puts a pole in the bracket (kinetic term through zero). Staying below 2 back to 1 MeV leaves nu today under 1e-29, no effect. Pole argued from the formula; only the nu term itself is block-checked (F3a, 1.1 %).
- **C7's mechanism** has no field here: K_B = 0, no transverse aether. A full Boltzmann run with this row's terms: NOT RUN, so runaway is ND.

**H4.** Rate = L k sqrt(2 pi G |rho|), exact block agrees. Lobes exist analytically: deep field is div(|h| h) = 0, and at a saddle div h = -2b on the axis (leading-order argument). Densities taken from H4's README, because the deep equation coincides; not re-solved for this row. Phantom rides the khronon, dust rides the scalar flow; the combined rho_tau form was shown with one charge at a time and in the limit omega << Q0. H5's flow reading not evaluated here.

## Failed checks, as run
`as3_part1` 16/17, K3b. `as3_part2` 25/28: F1c, F2b, H3 are the gate results. Both reruns byte-identical. MUTATE (EH and a.V signs): part 1 9/17 (K1a, K1b, A3 and others), part 2 20/27, exit 1. Earlier failures in `AMENDMENTS.md` and the RUN logs. R0a's test and three check lines changed after results, listed there.

## Reproduce
`OMP_NUM_THREADS=1 nice -n 19 python3 -W ignore as3_part1.py`, `as3_part2.py`; twin `AS3_MUTATE=1`. `as3_part2.py` needs CLASS for the known answer. Record's action: copy `route2_v2_build.py` with its SC pointed at a scratch folder, or `as3_record_repair_route2.py <dir>/`; then `as3_record_ladder.py <pkl>` (`as3_record_ladder.out`, `as3_record_ladder_repaired.out`). Pickles not committed.

No deposit, no push. PAPER67, STANDING, ledger, outside summary and other lanes untouched.
