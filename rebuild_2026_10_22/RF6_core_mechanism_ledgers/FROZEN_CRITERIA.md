# RF6_core_mechanism_ledgers: FROZEN CRITERIA (committed alone with the ledgers, before any script or re-run number)

**Question (THEORY_PROGRESS_SUMMARY_2026-10-31 §4).** Which "NOT REACHED" core-mechanism verdicts survive when the astrophysical inputs are ledgered and the need is stated on the framework's footing? CE1/BE1's converged-η failure is not touched and remains the governing result.

**Disclosed.** I have read the seven lanes' READMEs, criteria and committed R values, and RF3. So the inputs below are chosen knowing what those numbers do. From X-COP's gas profiles (data only): M_g(< 0.1207 R₂₀₀)/M₂₀₀ is 0.0043–0.0093 across 7 clusters, against CL5's round model, whose gas cap is 2 × 0.01415 = 0.0283. No re-run has started.

**Standing.** κ = ½ FITTED. Footings never pooled; the dynamics are footing-free and the need isn't. Cold dark energy, never a particle. No downloads. No new mechanism. No scan past the ledgered range. "Published range" entries are from memory unless marked on disk, and are PROVISIONAL. Not "theory closed". Nothing here says the data favour the framework.

## (a) Ledgers
`ledgers/ASSUMPTION_LEDGER_{CM1,CM2,CM3,BH1,BH2,CL5,SH1}.md`, dated 2026-10-31, after the fact, in this lane. The seven lanes' files aren't edited. Each row: input, value, class, range.

## (b) The single input per lane that moves the verdict most (from committed numbers)
| lane | input | why |
|---|---|---|
| CM1 | moved gas per burst M_f at CM1's cadence | R 0.932 at M_gas today, R 0.293 at all baryons; E_SN sets how much can move |
| CM2 | cadence | R 0.898 at 250 Myr, 0.573 at 1 Gyr |
| CM3 | coupling ε_c | at 1 Gyr, R 0.573 at 1, 0.894 at 0.3 |
| BH1 | central gas available | energy isn't binding in G1; UNCAPPED hot gas still misses |
| BH2 | central load L | the lane's own axis; existence untested |
| CL5 | gas in the core, M_f's cap | at 1e14 the gas cap binds; a_f 0.02 and fewer bursts don't reach |
| SH1 | R at 10¹³–10¹⁴ | scenario A fails, B passes only at R 0.685, granted not derived |

## (c) Re-runs: CM1 and CL5 only
**CM1.** CM1's ICs, integrator, 40 bursts, 250 Myr, ramps 5/200 Myr, STATIC reference (committed). Only M_f changes, with M_f taken out of stars so M_b stays the same at a★, as BOUND does. Cells:
| cell | M_f | meaning |
|---|---|---|
| GASHI | M_gas/M₂₀₀ at the 84th percentile of CM1's 74 active galaxies | measured gas, upper end |
| E1 | largest M_f with 40 e_lift(M_f) ≤ E_SN | CM2's energy cap, fiducial E_SN |
| E3 | largest M_f with 40 e_lift(M_f) ≤ 3 E_SN | top of the ledgered E_SN range |

Ledgered E_SN range × 0.35–3.0: 0.7–1.2 SN per 100 M☉ formed, 0.5–1.5 × 10⁵¹ erg, a return-fraction factor up to 1.67 on stars formed. **Inside range** at coupling 1: ε_SN ≤ 3.0 and M_f ≤ M_b. **Inside at coupling 0.3:** ε_SN ≤ 0.9. PROVISIONAL.

**CL5.** Part A's harness: N 10, a_f 0.05, ramps 50/400 Myr, M_g 0.10, a_g 0.20, frozen STATIC. M_f fixed, not capped; energy share reported. At 10¹⁴ and 10¹³:
| cell | M_f | meaning |
|---|---|---|
| XC | 0.0186 | 2 × the largest X-COP M_g(< 0.1207 R₂₀₀)/M₂₀₀, measured gas; X-COP sits above these masses |
| CEIL | 0.0283 | CL5's committed run (M14_e1, M13_e1), not rerun |
| X2 | 0.0566 | 2 × CL5's cap |

**Inside range:** M_f ≤ 0.0186 and energy ≤ 2 × E_AGN (M_BH/M★ up to 0.01). Above 0.0186 is **outside** the measured gas. Each new cell also gets CL5's same-gas control, so R is quoted both ways; the frozen STATIC R is the graded one, as in CL5, and the same-gas R is reported beside it. Reached is read on both.

## Need, as a band
**SPARC, per footing.** Piecewise-linear Υ(η) at 10¹² from committed grades on background A: SH1's A rows (η 14.86, 17.77, 21.19), CE1's median (25.94), X73's c_f 4 row (10.82). R_need(Υ) = η(Υ)/25.94 for Υ floor 0.44, 0.50, 0.57 (X78, LS1). Also on FC1's cold-share bookkeeping, R = η(Υ)/21.80. If the floor sits below Υ(25.94): **"no softening needed"**. If above every graded Υ: **"unreachable by softening"**.

**Clusters.** Υ doesn't enter. Limit 14.3 over four bookkeepings of η: CL5's ng 48 (16.91, 17.67), FC1's ng 64 (22.10, 23.54 at 10¹⁴, 10¹³), each with and without f_c 0.8405. Limit 14.3 is itself G-IN-Mall's on eRASS1's gas.

## Verdict wording, per lane
- **"NOT REACHED, robust to the ledgered ranges"**, if no cell inside the range reaches the fiducial need.
- **"NOT REACHED only at the fiducial input; reached at <input> = <value>, which is <inside/outside> its published range"**, otherwise.
- Beside each: where the need band makes the question moot.
- For the five lanes not re-run, the verdict reads committed numbers only.
- SH1 isn't a NOT REACHED lane; its entry says what its FAIL depends on.

## Checks
- **K1:** the wrapper at M_f = M_gas reproduces CM1 PRIMARY's η at its first mark (5 cycles), and at CL5's M14_e1 at its first mark, |d| ≤ 1e-9.
- **K2:** work balance < 1 % in every run.
- **K3:** M_f values and ε reported; E1's ε_SN within 1 % of 1.
- **K4:** Υ(η) table matches the committed JSONs exactly.
- **K5:** STATIC refs read from the committed runs, unchanged.
- **MUTATE (`RF6_MUTATE=1`, separate outputs):** E3 × 0.1 at CM1 and X2 × 0.1 at CL5, 10¹⁴. Each must move R less than its base cell (|1 − R| smaller), else NOT INFORMATIVE. Grading must call neither mutated cell reached.
- Any K failure: no verdict for that lane, exit 1.

One thread, nice 15, at most three processes, RSS ≤ 1 GB. Runs save at each mark; a SIGTERM saves a partial and the run restarts, as in CM1 and CL5.

## Limits fixed now
Same as CM1 and CL5: one spherical halo, one seed, prescribed gas histories, no cooling or gas physics simulated, halo formed at t = 0, R measured at x_c ≈ 0.013–0.017 and applied to x_c 0.001 values. The native-N rule of 10-31 removed the floor; Υ(η) rows here come from X74's grader with the floor, the only committed set across this range.
