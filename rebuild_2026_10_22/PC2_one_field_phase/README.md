# PC2_one_field_phase: KILLED AT GATE 1 AS A DERIVATION. No zero-constant condition lands at T (smallest miss -0.89 dex). With one counted mass it lands by fit, and a local line separates discs from clusters only marginally (+0.09 dex), then FRW condenses: the record's superfluid closure, reproduced with this lane's numbers

Criteria `FROZEN_CRITERIA.md` (f2beb77a4a), alone first; `AMENDMENT_A1.md` (ba70c9c8b5), alone, post-first-run. `pc2.py`, `pc2.out`, `pc2_results.json`; twin `pc2_MUTATE.*`. Not blind. kappa = 1/2 FITTED. Footings never pooled. Cold dark energy, a gravitating field component, never a particle. The retirement of 2026-11-01 stands, and nothing here reinstates it. No LCDM input. Not theory closed. Nothing here says the data favour the framework.

## Verdict
| Gate | Label | Margin |
|---|---|---|
| 1 derived switch | **KILLED AS A DERIVATION** | Best row Z3 -0.89 dex, and it's an acceleration key; then CSM1 -0.97, Z1 R500 +1.05 |
| 1, m counted | FIT, NOT DERIVED | m 3.74 eV at R200 [3.55, 3.98 across W]; 11.8 eV at 0.1 R200 |
| 2 selector | **MARGINAL** on rho_tot, +0.09 / +0.07; SEPARATED on rho_x, +0.53 / +0.52 | POST-HOC: -1.15 with X-COP x 0.03 |
| 3 abundance | **FAIL** thermal; not interlocked otherwise | z_nr 4.3e3, short of 3e4 x7.0; non-thermal +1 number |
| 4 discs | NOT RECOVERED in the only computed form | CFG122 0.414 at x = 1; Branch S spread 31.6 |
| 5 mergers | **CLOSED** by the frozen rule | Open at R_last; x57 / x392 over at 0.31 Mpc |
| 5 FRW | **background thermalises** | Gamma/H 1.1e2 to 5.9e6 at z 1090, estimate |
| 6 inherited | 9 / 10 non-cluster law rows FAIL; fixes none | |
| 7 action | c_s^2 = 2X/m < 0 on the law branch | transition, growth NOT COMPUTED |
| 8 acceptance | **NOT RUN** | no defined g |

**The first gate to kill it is gate 1.** I continued because you allow one counted constant, and because gate 2 didn't fail where I expected.

## Which closure applies
| Closure | Same reason? |
|---|---|
| STANDING item 4, superfluid route | **Yes, and it's the decisive one.** A rate that thermalises halos thermalises the background earlier. Reproduced below |
| STANDING item 3, mu-pincer | **Yes for a law phase on FRW.** A phase change evades it only if FRW stays out of equilibrium, and the rate says it doesn't |
| CFG122, UX1 K10 | Yes for the BK form: law form, ghost branch, Solar System. Unchanged. CFG122 did not test clusters or the Bullet, this lane does a rate estimate |
| V3S one mechanism, X6 | Partly. It's about one single-stream field at alpha = 1. A phase change isn't covered, and `coupling_one_is_law` says what the law phase needs, not what switches it |
| X19 no selector | **No.** It tested single variables and axis-aligned pairs. Q = rho/sigma^3 is a diagonal: new here |
| X60 | No. Dust against w = -1. Its R0 doesn't apply |
| TD1 | No. It excluded a0 and hbar. Allowing both still doesn't land |
| MC1 P1a, Bullet | Conditional. It fails a shocking fluid. A collisionless cluster phase escapes it only if gate 5 opens |

So it wasn't closed for quite the same reason on selection, and that part is new. It is closed for the same reason on FRW.

## Gate 1: landing, W [12.19, 12.39], tolerance max(0.12, spread)
| Row | log M | Miss | Note |
|---|---|---|---|
| Z1 law fills share, R200 | 14.238 (alt 14.485) | +1.85 | DT1 G reproduced |
| Z1, R500 | 13.442 (13.689) | +1.05 | |
| Z2 g200 = a0 | 16.429 (16.676) | +4.04 | |
| Z3 peak g_b = a0 | 11.297 (11.397) | **-0.89** | V_flat 131 |
| Z4 X43 crossover, native c_f | 9.828 (10.140) | -2.36 | READ DT1 |
| Z4b CSM1 corrected | 11.223 | -0.97 | READ |
| Z5 m = rho_DE^(1/4), 2.27e-3 eV | 25.16 | +12.8 | |
| Z6 m = Lambda_BK, alpha 1, 7.07e-4 eV | 27.19 (27.03) | +14.8 | |
| Z7 pi/mu = R200: v3s 0.1; forest 56.6; crossing 2e4; BBN 1.24e8 per Mpc | 18.52; 10.26; 2.59; -8.76 | +6.1; -1.93; -9.6; -21.0 | floors and ceiling, not values |

Counted fits: C2 m 5.7e-26 eV. C3 mu 11.8 per Mpc, below the forest floor x4.8 and the literal BBN floor x1e7.

**A degeneracy line isn't a mass switch.** At fixed Q_c, Q at radius f R200 goes as 1/(M f^2). So landing T depends on the radius chosen, 3.7 or 11.8 eV. Every halo above T keeps a degenerate core, R_c/R200 about (M/T)^(-1/2), hand arithmetic. FG1's C3 is per-system and sharp. This doesn't reproduce it.

**V_flat.** T maps to log M_b 11.12-11.34, law flat speed 215 km/s, SPARC median 241 there; 9 of 175 above T, matching FG1. V200(T) 180.

## Gate 2: log Q, Msun/pc^3/(km/s)^3
| Law side | canonical | | Cold side | canonical |
|---|---|---|---|---|
| LITTLE THINGS | -6.95 | | X-COP x 0.1 rho_tot | **-11.50** |
| SPARC 60-100 | -8.18 | | x 0.2 rho_x | -11.94 |
| SPARC 150-200 | -9.39 | | x 0.3 | -12.66 |
| SPARC 200-250 | -9.83 | | Bullet main, sub M300 | -12.59, -12.49 |
| KiDS 10.5, 0.31 Mpc | **-11.41** | | x 0.7 | -13.41 |

SPARC alone clears X-COP x 0.1 by +1.67. **This is better than I expected: it's the first local variable I've seen order discs below clusters on these inputs.** At V_c it's 1/(V r^2), so it's mostly radius; there's no microphysics in that ordering by itself.

**Why I don't read it as a pass.**
- **The mass at x 0.1 is inside x 0.1.** POST-HOC, X-COP: x 0.03 at 41 kpc, log Q -10.26, observed/law 3.50; x 0.05 -10.74, 3.54; x 0.07 -11.08, 3.44. The excess needs cold mass at Q above KiDS's -11.41, by 1.15 dex, and above KiDS at 0.1 Mpc, -10.43. That's the wrong sign, the one BK's picture carries: degenerate cores in clusters. Against SPARC 200-250 it stays +0.43.
- **KiDS might not bind.** A cold envelope with M proportional to r gives the law's shear. Then Q_c could sit near -10, and discs clear x 0.03. Lens rows become cold mass past about 70 kpc. Not computed.
- **The gap's landing isn't independent.** Its midpoint -11.46 maps to log M 12.37, inside W. Since 0.31 Mpc is close to R200(T), 266 kpc, the lens row is nearly the T row.

**Selector failures.** Potential, acceleration, environment, epoch, gas state: Q uses none of them directly, so those failures don't carry formally. Sigma's does in part: it's sigma with radius. C3's R2 and R3 are lost: dwarfs have the highest Q (-2.72 to -4.41), so hosted dwarfs get the law, which is C4's Dw row, FAIL (UFD +5.22), not C3's pass. Isolated and hosted MW-mass galaxies share a Q. Same-mass red and blue lenses share a Q.

**FRW ordering.** Q can't rise under Liouville and the second law. A thermal-like field non-relativistic at z 3e4 has log Q_bg -10.48, below SPARC 200-250's -9.83. Reaching disc Q needs z_nr 4.9e4 to 3.3e5; the dwarf classes need 1.2e7. **So FRW sits on the degenerate side of any line below disc Q**, the same side as discs, and away from clusters. The hypothesis wants FRW with clusters. That order can hold only out of equilibrium.

## Gate 3
Thermal relic at C1: T_x 3.22 K, 1.18 T_gamma; z_nr 4.28e3, short x7.0 (g 2 x5.6). At 0.1 R200, x1.5 (x1.2). Its Q_bg -13.01 falls 3.18 dex below disc Q (-11.01, 1.18 dex). Non-thermal: integration constant, so one more number. The abundance and cluster share are set twice, not interlocked. Nothing here reads the cosmic ratio; BK1's reading stays COINCIDENCE.

## Gate 4
Mass reading: M_ph(R200)/M_b 44.8 at V 60, 16.5 at 200, 11.6 at 300, against 5.35. So it needs retention about 0.14 to 0.50 (hand), and 1.4 to 2.8 x EM1's cold share (3.2 to 1.6 alt). Not a kill: that's about X53's lens-mass gap, read not computed. The profile is: Branch S fails by 31.6 in BK. Force reading: CFG122's lens ratio 4.35 at 40 kpc, 233 at 2.2 Mpc (canonical), so lensing needs another coupling. Tilt, surface brightness and LITTLE THINGS inherit from the law only if the law is exact, and the BK form isn't. A pressure phase with c_s 0.6-0.8 V clears MC1's room on MC1's own row.

## Gate 5, s = sigma_x/m_x, Q_c at the top cold row
| Radius | s_min, cm^2/g | N | Over tau 1 (8.64) | Over Randall 1.25, PROVISIONAL |
|---|---|---|---|---|
| R_last, 200-250 | 0.06 | 44 | clear | clear |
| KiDS 0.1 Mpc | 5.3 | 12 | clear | x4.2 |
| KiDS 0.31 Mpc | **490** | 1.2 | **x57** | **x392** |

A real result: at R_last the field can thermalise and still pass the Bullet. **Frozen rule: CLOSED, on the lens radius**, which KiDS's envelope caveat softens. Keys, X-COP, MG1 aren't computable: no g.

**FRW, the row that decides.** At s_min(R_last) 0.066 and N_bg from Liouville, Gamma/H at z 1090: 1.1e2 (Q_bg at SPARC 200-250), 4.8e3 (20-60), 5.9e6 (dwarfs). Gamma/H crosses 1 between z 100-1090, 20-100, 0-3 respectively. Since the background is degenerate and equilibrating before recombination, it's in the law phase.

**Law phase on FRW, parameter-free.** With K set by c_s 0.6-0.8 V at disc density: w = 1/3 at z 302-520 for P = K rho^3 (w at z 1090 of 28 to 730); z 3100-7200 for K rho^2. Short of dust by z 3e4 by **x58-99, x4-10**.

## Gate 6, inherited (`RQ2 results/law.json`)
Canonical FAIL: A5, A6, A7, A10, A11, A12, A13, A30, C1; alt adds A2. A15, A16 stay FORM-DEPENDENT. The phase structure fixes none: discs are the law. Milky Way, IC 1613, stellar-mass rows and planets are unchanged, and CFG122's G5.4 has phase-boundary screening impossible. Only B rows could move.

## Gate 7
`L = (2 Lambda (2m)^(3/2)/3) X sqrt|X| - alpha Lambda theta rho_b/M_Pl`, CFG122's. c_s^2 = 2X/m both signs (sympy, known answer). X < 0, the law-carrying branch, is negative. So the record's c_s^2 < 0 (BOLTZ1, step) has a second home here. No stable transition is written. NOT COMPUTED.

## Gate 8
NOT RUN. Neither gate 1 nor 2 defines a g: the cold side needs a profile and the switch a radius. Inventing one would grade my choice.

## No-particle finding
**The only microphysics here that lands is particle-like:** quanta of about 4-12 eV with self-scattering, 0.06 cm^2/g or more. Reported plainly, not adopted. C3's field-only mu has no phase, and misses its floors.

## What would have to be true for it to live
All of these:
1. A forced m, or a non-thermal condition, landing T with no fit.
2. FRW staying out of equilibrium at N_bg >= 42, with a rate at least 110 x lower at z 1090 than the discs need, or a law phase that is dust at 43 Msun/pc^3 and has c_s about V at 1e-3. The record has neither.
3. Cold mass inside 136 kpc of clusters at Q above the discs' lens region, or KiDS read as a cold envelope, computed.
4. An exact law from that phase, on a stable branch, with lensing.
5. An answer for rows A5-A13 and C1, which it doesn't touch.

## Errors and limits
- **Bug, mine:** gate 5's unit factor, s_min 1e6 too large in the first run. It would have read closed at R_last, falsely. Caught by hand. First output not kept; A1 records it.
- **Post-freeze:** all POST-HOC rows, after seeing +0.09. The -1.15 is hand subtraction from `pc2.out`. X-COP x 0.03 rests on forward hydrostatic fits near the data's inner edge, n 7, with HSE's 0.12 dex.
- **Estimates:** Gamma = s rho v N is a rate estimate with Bose enhancement, no kinetic solve, t = 1/H0. Velocity-dependent s isn't tested. Interaction shift of T_c isn't computed. Ideal-gas Q_c.
- **Row choices:** KiDS uses M_b = M* at one mass, the flat rule on every class. I picked rho_tot as primary from the criteria's "one definition" sentence; on rho_x the label reads SEPARATED. Mapping uses EM1's line, from the retired sector; alt has no T target. Grades in the closure table and the "live" list are my reading.
- **Not done:** second implementation, outside review, any simulation. Literature: Randall's limit from memory, PROVISIONAL.

## Expectation against result
Killed at gate 1, 85 %: yes. Counted m failing gate 2 on the lens row, 70 %: **no**, MARGINAL, and it's the surprise here. It takes the post-hoc rows to reach a failure.

## Checks and twin
K1 4He T_c 3.134 K. K2 Z1 14.238, 14.485, DT1's exactly. K3 MC1's 6.7303, n 7. K4 43.14. K5 142.71 km/s, 211.2 kpc. K6 2X/m. **All 6 pass.** Rerun byte-identical. MUTATE, hbar x 2: K1 12.54 K, FAIL, exit 1, separate outputs. It bites on K1 only.

kappa = 1/2 FITTED. Not theory closed. Never pushed; no deposit.
