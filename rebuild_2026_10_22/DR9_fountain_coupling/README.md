# DR9_fountain_coupling: FAILS AT ALL THREE normalisations, and the order does NOT reverse. The coupling rises 4.7× toward spirals, but the cost of undoing rises 5.0×, so they cancel

Criteria: `FROZEN_CRITERIA.md` (c00c9f6ed7), committed alone first. `AMENDMENT_A1.md` (b4176c98a3). `dr9.py`, `dr9_tail.py`, `dr9.out`, `dr9_results.json`, `dr9_energy.json`, `dr9_constants.json`, `dr9_clusters.json`, `dr9_row_*.json`. NR3's path; UR1, NR2, NR3 read only. κ = ½ FITTED, unused. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind.** The idea came from an outside AI's text, tested as a claim. **First run's frozen MUTATE missed its line, so that run was NOT DECIDED; the label stands on A1's replacement mutation** (below).

## Is it zero-parameter? No
ΔW = C η_PG R E_SN. C lumps three unnamed numbers: share of E_SN reaching gas, gas-to-cold transfer, and number of cycles. Only C = 1 adds no number, and it's a ceiling. The form is posited, not derived. **Attribution, from memory, PROVISIONAL, papers not opened:** Pontzen & Governato's impulsive gain is second order in the potential change, so it scales with gas actually moved over the enclosed mass, and it is gravitational, with no E_SN in it. Read & Gilmore 2005 is a two-stage mass-loss expansion. Neither, as I recall, gives (M_b/(M_b + M_c))² × E_SN. I can't confirm the text's "Eq. 9".

## Budget, NR3 MEDIAN, Υ 0.50, background A
| V_flat | n | f_local (UR1, on NR1) | after response | M★/M_b | f_ret | η_PG | η f_ret | η M★/M_b | ε_full | ER1 ε_full (OP3) | ΔW/E_undo, C 1, f_ret | M★/M_b |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20–60 | 12 | 0.48 (0.44) | 0.32 | 0.16 | 0.36 | 0.107 | 0.038 | 0.016 | 0.014 | 0.012 | 2.73 | 1.32 |
| 60–100 | 35 | 0.37 (0.38) | 0.27 | 0.30 | 0.45 | 0.074 | 0.033 | 0.021 | 0.018 | 0.014 | 1.82 | 1.30 |
| 100–150 | 23 | 0.67 (0.66) | 0.41 | 0.44 | 0.50 | 0.161 | 0.083 | 0.074 | 0.027 | 0.022 | 2.57 | 2.28 |
| 150–200 | 25 | 1.06 (1.08) | 0.56 | 0.70 | 0.57 | 0.264 | 0.151 | 0.194 | 0.067 | 0.050 | 2.16 | 2.56 |
| 200–250 | 18 | 1.09 (1.08) | 0.56 | 0.69 | 0.63 | 0.273 | 0.167 | 0.192 | 0.097 | 0.075 | 1.73 | 1.95 |
| 250–400 | 10 | 1.23 (1.24) | 0.61 | 0.75 | 0.66 | 0.304 | 0.194 | 0.235 | 0.125 | 0.096 | 1.56 | 1.80 |

ER1's ε_full column is on OP3's shape; on NR3's it runs about 30 % higher. E_undo here is a minimum virial cost at perfect delivery.

- **Mass order, frozen ratio, 150–250 over 20–100:** ΔW/E_undo **0.96** with f_ret: **NOT REVERSED**. 1.78 with M★/M_b.
- **"10× larger in spirals":** η f_ret **4.7×**; η M★/M_b 11.4×. Only the double-counting form reaches it, and E_SN already scales with M★. ε_full rises 5.0×.
- **Which direction?** At C = 1 energy exceeds the need in every bin (1.3–2.7), so it undoes everything; the rule has no room to spare dwarfs. The right shape needs ΔW/E_undo near 0.8 at 150–200 and near 0 in dwarfs; f_ret gives a flat profile, M★/M_b about 2× in the right direction.

## Grade
Normalisations: C 1; **C_CM1** = 0.00284 (CM1's net work / E_SN) / median η R in 35 galaxies within 0.3 dex of CM1's mass; **C_FIT, FITTED,** closed form on the 150–200 bin, background A, f_req 0.175.
| Row | C | Υ A/B | rms A | tilt A/B | LT A/B | Υ by V_flat, A | Fails |
|---|---|---|---|---|---|---|---|
| NR3 response (C0) | 0 | 0.35/0.36 | 0.0670 | +0.17/+0.18 | +0.116/+0.109 | 0.49 0.53 0.46 0.30 0.36 0.47 | Υ, tilt, LT |
| NR3 off (CINF, 1e9) | | 0.75/0.76 | 0.0690 | +0.59/+0.59 | +0.153/+0.147 | 1.20 1.17 0.90 0.57 0.62 0.77 | tilt, LT |
| **f_ret, C 1** | 1 | 0.73/0.75 | 0.0695 | +0.50/+0.52 | +0.144/+0.143 | 1.15 1.11 0.90 0.57 0.62 0.77 | tilt, LT |
| **f_ret, C_CM1** | 0.0186 | 0.37/0.37 | 0.0675 | +0.21/+0.21 | +0.117/+0.110 | 0.52 0.54 0.46 0.30 0.37 0.48 | Υ, tilt, LT |
| **f_ret, C_FIT** | 0.382 | 0.70/0.70 | 0.0704 | **+0.33/+0.39** | +0.130/+0.129 | 0.48 1.10 0.90 0.51 0.49 0.77 | tilt, LT |
| M★/M_b, C 1 | 1 | 0.70/0.70 | 0.0692 | +0.30/+0.34 | +0.136/+0.136 | 0.52 1.07 0.90 0.57 0.62 0.77 | tilt, LT |
| M★/M_b, C_CM1 | 0.0136 | 0.37/0.37 | 0.0671 | +0.21/+0.21 | +0.117/+0.109 | 0.52 0.54 0.46 0.30 0.37 0.48 | Υ, tilt, LT |
| M★/M_b, C_FIT | 0.322 | 0.66/0.68 | 0.0694 | **+0.24/+0.32** | +0.121/+0.114 | 0.73 0.83 0.90 0.53 0.51 0.72 | tilt, LT |

**Label: FAILS AT ALL THREE.** Lines: tilt ≤ 0.15, LITTLE THINGS ≤ 0.10. Every row with Υ on the line fails both. The double-counted form is the best row and it also fails; it never sets the label. C_FIT does what it was fitted to: 150–200 reads 0.51. It lifts 60–150 to 0.90–1.10 as well. Compare ER1's best tilt on the line, +0.58: M★/M_b at C_FIT is a real improvement on ER1, and still short.

The 20–60 bin at C_FIT is unstable: 0.48 with f 0 at Υ 0.50. E_SN grows with Υ, so a higher Υ undoes more, which wants a higher Υ. n is 12. Don't read that one bin as a success.

**My expectation:** three-row fail held, and tilt +0.2 to +0.45 held, C_FIT "tens of times" C_CM1 held (20.6). **I expected the order to reverse; it didn't** on the primary form.

## Before or after response
Primary reads f_local before. After full response f_local halves in spirals (1.06 → 0.56), since M_c is what grows. At the same C: Υ 0.70 → 0.56, tilt +0.33 → **+0.50**, LT +0.130 → +0.123; 150–200 goes back to 0.32. So "before" is the favourable reading. The true state lies between, and a self-consistent solve would land there; it isn't run.

## Does it reduce to CM1? Yes in physics, and it needs 21×
The real channel for this form is CM1's: gas cycles, gravity only. C_FIT is 20.6× what CM1 measured, and CM1-sourced C changes nothing: f 0.95–0.97, Υ 0.37. **Attribution of the brief:** "coupling about 1 with rare bursts" is CM3, not CM1. CM1 is the fiducial channel, insufficient; CM3 reaches only at coupling 1 with 10–20 bursts, and misses at 30 % at every cadence. Carrying C_CM1 across (softening a cusp to undoing contraction) is BY HAND.

**Diagnostic, BY HAND, form from memory, not graded:** moved gas, η_gas = (M_g/(M_b + M_c))² at r₀, 40 cycles, order-one constant. Gas share at r₀ falls 0.72 → 0.03 with mass. ΔW_PG/E_undo: 2.8, 0.43, 0.22, 0.10, 0.046, 0.016, so 150–250 over 20–100 is **0.13: strongly dwarf-first**. ΔW_PG/E_SN at 150–200 is 0.5 %, the same order as CM1's 0.28 %, unforced. So the form with moved gas, which I recall as the actual argument, recovers CM1's size and ER1's wrong order, and agrees with ER2's dwarf-first finding. The text's M_b swaps in stars that don't move; that swap is what makes it rise with mass.

**Hazard, look-up from memory, PROVISIONAL:** feedback-core simulations (FIRE, NIHAO) peak near M★/M200 of a few 1e-3, dwarfs, and contract at L★. f_local about 1 means a deep baryon potential, where gas moved is a small part of the well. This rule puts its strongest coupling exactly there. That's the opposite of what those runs report, as I recall them.

## Clusters
Not regraded, NR3's: 14 keys, G-IN-Mall −2.05 fails, X-COP −0.097, 0.146 fails. So no row could be a full pass. Median over every fourth cluster: f_local at 0.05 Mpc **0.020, 0.038 with the BCG**. So "small" holds even with it, though the BCG doubles it. **X-COP's inner rows are BCG cores, and NR3's X-COP row carries no BCG (XH1); the keys' do.** Response is outward (M_f/M_0 0.74 at 0.05 Mpc, W change of opposite sign), so "undo" has no plain meaning there. η E_SN at C 1 is 1.7e-4 of that energy change: negligible, as claimed. AGN energy isn't in this rule (CL5).

## Groups: NOT TESTED under the rule (A1)
Z +1.4979 in every row, including C 1e9. For groups my frozen E_undo comes out 0, so "nothing to undo, f = 1" fires. Likely cause: central point mass on that grid and W's inner cutoff; traced on one group, not proved. Endpoints: f 0 +1.47, f 1 +1.50, both inside |Z| ≤ 2. Groups don't decide any row, and the ± is a bracket, not a grade. The verdict doesn't rest on them.

## Checks
K0 C 0 vs NR3 response 0. K1 C 1e9 vs NR3 off 5.6e-6 (line 1e-5, DR5 A1's grid effect, stated at freeze); groups 3.0e-2, inert as above. K2 1 + R_nat 6.2715, 4.6e-4. K3 f within [0, 1]. K4 energy vs DR5 0. K5 ε_CM1 3.4e-3. E_undo 0 in SPARC: 0 galaxies. GB linear in Υ 3.3e-16. f_ret capped 0 of 123.
**MUTATE as frozen: MISSED**, overall Υ 0.70 → 0.68, exactly 0.02 against "more than 0.02"; tilt moved +0.33 → +0.69. **MUTATE_A1** (C × 0.01, line set before it ran): Υ 0.70 → 0.36, passes. A1 was written after all rows were seen.

## Limits
Outflow holds baryons fixed; real outflows remove gas. Self-consistent f_local isn't solved. C_FIT is one bin, one background, not iterated. Noise band of NR2's η not propagated. KiDS, Local Group, MW not run. E_undo is a virial cost, not a delivery calculation. PG12, RG05, FIRE, NIHAO all from memory; nothing downloaded.
