# DR8_pressure_core_response: BLUMENTHAL OVER-PREDICTS ON A CORE, PARTIAL, f_B 0.753 [0.729, 0.777]. The claimed 5-10× is about 1.5, both live and in the rule. The rule MOVES, FAILS on SPARC's line, and so does the measured response carried across masses

Criteria: `FROZEN_CRITERIA.md` (a2310702c0), committed alone first. A: `dr8.py`, `dr8_rule.py`, `dr8_tail_add.py`, `dr8.out`, `dr8_PRIMARY_results.json`, `dr8_FQ_results.json`. B: `dr8_ic.py`, `dr8_live.py`, `run_dr8.sh`, `dr8_action.py`, `dr8_read.py`, `dr8_post.py`, `dr8_checks_b.py`, `dr8_live.out`, `dr8_post.out`, `dr8_checks_b.out`, `dr8_live_results.json`, `dr8_fr_table.json`. κ = ½ FITTED, unused. Gravity only, no a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind:** NR3, DR3, DR7, LC1, RM1, UR1 and X81 were read; the live outcome was not known.

**Already tested?** No. The rule is in no lane, and no live response of a cored equilibrium halo was on record (DR7 says so; LC1 and PZ1 grow discs in cusps).

## Part B: the first live response of a cored halo
Graded smooth core at 10¹², NR2 MEDIAN: **r₀ 15.49 kpc**, R200 199.3 kpc, a 12.86, Σ 123.7 M☉/pc², M(<r₀)/M200 0.077. Eddington inversion, isotropic, tapered beyond R200. N 60,000, ε 0.7 kpc (3ε 0.59 R_d, 0.135 r₀), about 4,000 particles inside r₀, rough central t_relax 30 Gyr. LC1's disc (6.72e10, a 3.565 kpc, b 0.2 a), linear over 7.7 Gyr, x48_fast's kernel, same-seed pairs. **Isolated: no accretion, no Λ term, no expansion, no disc back-reaction. One mass.** 5 core pairs, 3 NFW (c 12.95). Wall about 4 s a step, 3,450 steps with a disc on a core, 6 h for all 17 runs at load.

**Core, end of growth, medians:**
| r/R_d | 1 | 2 | 2.2 | 3 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|---|---|
| Q live | 4.52 | 2.85 | 2.65 | 2.14 | 1.76 | 1.42 | 1.26 | 1.18 |
| Blumenthal | 9.66 | 4.04 | 3.58 | 2.52 | 1.92 | 1.41 | 1.24 | 1.15 |
| Gnedin | 6.68 | 2.92 | 2.66 | 2.01 | 1.64 | 1.32 | 1.19 | 1.13 |
| RULE as stated | 4.41 | 2.78 | 2.59 | 2.06 | 1.70 | 1.35 | 1.22 | 1.15 |
| RULE_F | 4.22 | 2.67 | 2.48 | 1.95 | 1.61 | 1.29 | 1.16 | 1.10 |
| Exact isotropic actions | 4.79 | 2.91 | 2.72 | 2.14 | 1.74 | 1.40 | 1.25 | 1.17 |
| (Q−1)/(Q_B−1) | 0.41 | 0.61 | 0.64 | 0.75 | 0.84 | 1.00 | 1.10 | 1.14 |

By r/r₀ (0.25, 0.5, 1, 2, 4, 8): Q 4.26, 2.66, 1.68, 1.23, 1.08, 1.03; f_B 0.43, 0.64, 0.88, 1.10, 1.42, 1.91. So Blumenthal is too strong inside about r₀ and slightly too weak outside it.

| Over r/R_d 2, 3, 4 (5 seeds, 95 %) | f | frozen reading |
|---|---|---|
| Blumenthal | **0.753 [0.729, 0.777]** | **PARTIAL, OVER-PREDICTS** |
| Exact actions (J_r, L, disc monopole) | 1.019 [0.965, 1.134] | tracks live |
| RULE | 1.087 [1.059, 1.127] | **not MATCHES** on the frozen line: its interval excludes 1 |
| RULE_F | 1.188 [1.151, 1.253] | not MATCHES |
| Gnedin | 1.133 [1.091, 1.203] | under-predicts |

**(Q_B − 1)/(Q − 1) at 2.2 R_d: 1.55 [1.52, 1.61]. The 5-10× fails live.** At 1 R_d it is about 2.4. R_live 1.81 [1.79, 1.81], STRONG on LC1's line: a core does not escape contraction, because it starts with less central mass and gains by a larger factor.

**NFW control, same setup: f_B 0.825 [0.809, 0.860], R_live 1.76, LC1's class (0.872, 2.15).** f_A 0.987. So the same machinery reproduces Blumenthal's small over-prediction on a cusp, and it grows on a core. The intervals reflect particle sampling only, not halo-to-halo scatter.

**One-mass carry, MEASURED AT ONE MASS, not a rule:** M_f = M₀ + f(r/r₀)(M_f,blum − M₀), table above, flat beyond the ends, on NR3 MEDIAN's path: **Υ 0.42/0.43**, rms 0.0685, tilt +0.21/+0.22, bins 0.63, 0.63, 0.50, 0.36, 0.45, 0.57, keys 14, X-COP −0.102, 0.141, groups +1.51, LT +0.110/+0.103. **SPARC's line stays missed, and no gate newly passes.** This carries f from f_B's 1e12 path to SPARC's masses by r/r₀, without DR3's geometry factor (about 0.9), which stacks on top. Real but not enough: 150-250 km/s rise only from 0.30, 0.36 to 0.36, 0.45.

## Part A: the rule on NR3 MEDIAN's path
| Row | Υ A/B | rms A | tilt A/B | Υ by V_flat (A) | keys, failing | Groups Z | X-COP | LT A/B |
|---|---|---|---|---|---|---|---|---|
| EM1, off | 0.75/0.76 | 0.0690 | +0.59/+0.59 | 1.20, 1.18, 0.90, 0.57, 0.62, 0.77 | 12 | +1.47 | −0.160, 0.186 | +0.153/+0.147 |
| EM1, Blumenthal = NR3 | 0.35/0.36 | 0.0670 | +0.17/+0.18 | 0.49, 0.53, 0.46, 0.30, 0.36, 0.47 | 14, G-IN-Mall | +1.50 | −0.097, 0.146 | +0.116/+0.109 |
| **RULE as stated** | **0.44/0.46** | 0.0684 | **+0.26/+0.26** | 0.69, 0.67, 0.52, 0.37, 0.46, 0.56 | 12, G-IN-Mall, G-IN-all, G-MID-T3 | +1.43 | −0.181, 0.205 | +0.118/+0.112 |
| **RULE_F** | **0.48/0.49** | 0.0651 | **+0.32/+0.33** | 0.76, 0.75, 0.57, 0.38, 0.47, 0.58 | 13, G-IN-Mall, G-MID-T3 | +1.49 | −0.127, 0.159 | +0.128/+0.121 |
| BLUM0 (no F, no P; not fully converged, see Checks) | 0.30/0.31 | 0.0735 | +0.12/+0.13 | 0.41, 0.43, 0.39, 0.30, 0.34, 0.45 | 11 | +1.41 | −0.199, 0.218 | +0.102/+0.095 |

**Labels: RULE MOVES, FAILS. RULE_F MOVES, FAILS.** Υ, tilt, LITTLE THINGS, keys and X-COP fail on both. LOW and HIGH were not run, as frozen, since no row reached the line.

**The claim's numbers against the repo:**
| V_flat | n | R_d | r₀ | r₀/R_d | r_i/r₀ landing at 2.2 R_d, Blum / RULE | (Q_b−1)/(Q_r−1) at 2.2 R_d | at r₀ |
|---|---|---|---|---|---|---|---|
| 20-60 | 12 | 0.76 | 2.42 | 2.97 | 0.96 / 0.89 | 1.52 | 1.31 |
| 60-100 | 35 | 1.73 | 4.30 | 2.48 | 1.07 / 1.05 | 1.30 | 1.24 |
| 100-150 | 23 | 2.43 | 7.13 | 3.19 | 1.03 / 0.93 | 1.42 | 1.24 |
| 150-200 | 25 | 3.20 | 13.21 | 3.85 | 0.93 / 0.82 | 1.50 | 1.24 |
| 200-250 | 18 | 5.18 | 18.05 | 3.40 | 1.02 / 0.92 | 1.42 | 1.22 |
| 250-400 | 10 | 6.47 | 20.71 | 3.43 | 1.06 / 0.97 | 1.37 | 1.21 |

- **5-10× fails: 1.4-1.5 at 150-250 km/s.** Its inputs are off too: R_d is 3.2-5.2 kpc, not 2.5, so r₀/R_d is 3.4-3.9, not 6-10. Shells landing at 2.2 R_d start near r₀, not deep inside it.
- **"Dwarfs stay strong" fails.** The cut is the same size in dwarfs (1.3-1.5), so the tilt worsens.

## What the rule is
- **Not derived.** It rearranges to r_i[M_i + P(r_i)] = r_f[M_i + M_b(r_f) + P(r_i)]. P is frozen at the shell's start, so r_f P(r_i) isn't r² σ². It is not an adiabatic invariant. It conserves nothing a Jeans argument gives, and the Jeans argument gives no such form.
- **The real invariants** for a spherical isotropic system are J_r and L for each orbit; in a harmonic core only 2J_r + L sets the energy (`dr8_action.py`, Young's scheme). Gnedin's ⟨r⟩ form uses a power law calibrated on cusps, and it over-predicts inside about 1.5 R_d here (f 0.45-0.63 at 0.135 r₀ and R_d) while under-predicting outside.
- **Mass and monotonicity:** M_f(r_f) = M_i by construction, no crossings in 33,390 graded calls, converged to 3e-4. **As stated it drops the repo's (1+F):** the edge moves in (r_f/r_i 0.988 on a test) and clusters can't expand, which is why keys and X-COP worsen. RULE_F restores this, by my minimal choice, and live shows a price outside (f 1.64 at 2 r₀, 3.28 at 8 r₀).
- **P grows linearly in r_i,** so the term doesn't switch off outside r₀; RULE still has Q − 1 close to live out there only because F is missing.
- **The unexpected part.** With no fitted number, the stated rule tracks a core live at 1e12 within 4-20 % from 1 to 10 R_d, far better than Blumenthal. In the point-mass limit, 0.1 M(<r₀): ρ slope exact −1.41, RULE −1.27, Blumenthal −2.21; M(<0.008 r₀) over the exact, RULE 0.57, Blumenthal 50. At 0.001 M(<r₀): slopes −0.21, −0.39, −2.17; RULE 3.3×, Blumenthal 497×. So it's a decent interpolation in shape at this mass and F. That is one mass, not a law, and it doesn't rescue SPARC.

## Expectation against result
Held: Υ rises, tilt worsens, keys and X-COP worsen, no clearance, actions track live, 5-10× fails, partial relief at 150-250. Mine was ×1.5-3 near R_d, read ×2.4 at R_d and ×1.55 at 2.2 R_d. Not expected: how closely the stated rule tracks the live core.

## Checks
**A.** K1 EM1|blum vs NR3 MEDIAN: 0, SPARC and cluster preds. K2 RULE_F at P → 0 vs `contract` 2e-15; M_b 0 identity 0. K3 r₀ inferred 5e-15 on test, 7e-13 in the path. K4 monotonic. MUTATE M_b × 2: Υ 0.44 → 0.33, bites.
**B.** K5 Hernquist 1.5e-4; f > 0 everywhere; ρ recovered 2.6e-4. K6 sampled N(<r) within Poisson, 2T/|U| 0.9957. K7 below. Energy to 13.8 Gyr −8.8e-5, 2T/|U| 0.9994. K8 0. K9 6.2e-7. K10 0, exit 75. K11 LC1's reader on LC1 s1 0; identity 0; moved to Blumenthal's radii f_B 1.000. K12 null 0.019; Young's slope −1.41, coefficient 0.89. MUTATE M_d × 2: Q(3 R_d) − 1 +75 %.
**K7, core stable with no disc.** Median Δ ln M(<r) over seeds at 7.7 Gyr: +0.077, −0.015, −0.033, +0.006 at r/r₀ 0.25, 0.5, 1, 2, all within line. **At 13.8 Gyr (one seed): −0.037, −0.085, −0.012, +0.019: over the 0.05 line at 0.5 r₀.** About 2σ in Poisson (N 801). Per the frozen clause, this is under the signal by more than ×5 (ln Q 0.98), so the verdict stands and it's stated. Below 0.135 r₀ counts are too few to read.

## Departures, all disclosed
1. **Centre:** LC1's shrinking-sphere centre jumped 0.87 kpc rms on a core against the 0.36 kpc line, so the frozen fallback (centre of mass inside r₀) ran on all runs, before any disc reading. Its rms is 0.22-0.24 kpc. On NFW, r < 5 r_s.
2. **K3 failed on the first A run:** r₀ inference used the first truncated grid point on clusters, an error about 1e-3. Fixed and all rows rerun. Graded rows read the same at printed precision before and after; the run-1 file was removed.
3. **K12b first failed by design:** my M_p's cusp lived inside G M_p/σ², below the fit range. Changed to 0.1 M(<r₀) after seeing that, with an analytic check that the solver is right (Kepler J to 5e-4). So that line was reset post hoc.
4. Energy in the reader sorted t7.70 as last; `dr8_post.py` reads 13.8.
5. BLUM0's iteration has not converged in some calls (0.54, crossings), reported row only. The action solver's last pass changed by 3 % at its noisiest shell.
6. Keys on UR1's gas inputs, without GS4's +0.005, as frozen.

## Limits
One mass. Isolated, no accretion; LC1's zooms have it. Smooth steady disc, no clumps, no feedback, no back-reaction. Taper is by hand. Core shape is by hand (owner's rule N): an isotropic equilibrium core has no known origin (X81), so this tests the response of the assumed core, not its existence. Isotropic start: real halos are radially biased outside. The grader's M_b is v² r/G, not the monopole (DR3). KiDS, Local Group, MW not run. Literature from memory, unchecked: Young 1980 (checked numerically here), Gnedin+ 2004.

κ = ½ FITTED. Not theory closed.
