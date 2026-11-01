# HB1_barotropic_hydrostatic: ARGON'S PREDICTION MISSES on all 8 items, and both forms fail: MOVES, FAILS. Form B has a wide rms miss (0.505), with no continuous branch from the uncontracted core and no universal P(ρ)

Criteria: `FROZEN_CRITERIA.md` (24c36c74bc), committed alone first. `AMENDMENTS.md` A1–A4. `hb1_solve.c`, `hb1_core.py`, `hb1_test.py`, `hb1.py`, `hb1_tail_add.py`, `hb1_zn4.py`, `hb1_read.py`, `hb1.out`, `hb1_results.json`, `hb1_*_results.json`. NR3 MEDIAN's path, δ 0, EM1, f★ 0.034, canonical. The solve contains no a₀ and no particle. κ = ½ FITTED, unused. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind:** the lanes in the criteria were read.

**Correction to the record:** commit f60df2cfcc holds a `hb1_test.out` and `hb1_test.json` with a failed K4. The corrected outputs are in this commit; K4 was changed by A2 before any graded number.

## Argon's prediction (Form A, background A, its definition of c_s0²)
| Item | Solve | Predicted | Label |
|---|---|---|---|
| Global Υ | 0.30 | 0.58 ± 0.05 | MISSES |
| Tilt | −0.07 | +0.38 ± 0.08 | MISSES |
| Υ 20–60 | 0.30 | 0.95 ± 0.08 | MISSES |
| Υ 60–100 | 0.30 | 0.92 ± 0.08 | MISSES |
| Υ 100–150 | 0.31 | 0.74 ± 0.08 | MISSES |
| Υ 150–200 | 0.35 | 0.44 ± 0.08 | MISSES |
| Υ 200–250 | 0.35 | 0.50 ± 0.08 | MISSES |
| Υ 250–400 | 0.485 | 0.66 ± 0.08 | MISSES |

Its withdrawal condition (|tilt| ≤ 0.15 and Υ(150–200) ≥ 0.50) **DOES NOT FIRE**: the tilt clears, Υ(150–200) doesn't.

Sensitivities, not scored as its prediction. The P/ρ reading of c_s0 (K halved, against Argon's written h = c_s0² ρ/ρ₀) holds 3 of 8: 60–100, 100–150, 250–400; global 0.67, tilt +0.50 miss. Argon's text also writes c_s0² ≈ 2.15 G M(r₀)/r₀, but its own definition gives 3.80–4.62 on N's halos. That coefficient reads Υ 0.30, 8 of 8 miss, rms 0.353.

## Gates
| Row | Υ A/B | rms | tilt A/B | Υ by V_flat (A) | Groups Z | LT A/B | Keys +0.005 | X-COP |
|---|---|---|---|---|---|---|---|---|
| EM1, off | 0.75/0.76 | 0.0690 | +0.59/+0.59 | 1.20 1.18 0.90 0.57 0.62 0.77 | +1.47 | +0.153/+0.147 | 12 | −0.160, 0.186 |
| EM1, Blumenthal | 0.35/0.36 | 0.0670 | +0.17/+0.18 | 0.49 0.53 0.46 0.30 0.36 0.47 | +1.50 | +0.116/+0.109 | 14, G-IN-Mall | −0.097, 0.146 |
| **Form B E1 (PRIMARY)** | **0.33/0.35** | **0.5053** | **+0.22/+0.25** | **0.81 0.50 0.36 0.30 0.30 0.30** | **+1.52** | **+0.198/+0.196** | **14, G-OUT-all −2.42** | **+0.311, 0.387** |
| **Form A** | **0.30/0.30** | **0.2372** | **−0.07/−0.07** | **0.30 0.30 0.31 0.35 0.35 0.48** | **−0.35** | **−0.260/−0.257** | **2** | **−0.605, 0.645** |
| B, E2 (wall hit in 59 % of calls) | 0.33/0.33 | 0.8579 | +0.22/+0.23 | 0.81 0.49 0.36 0.30 0.30 0.30 | +1.52 | +0.242/+0.236 | NR3 gas: 14 | +0.311, 0.387 |
| B, E3 | 0.33/0.33 | 0.8575 | +0.21/+0.23 | 0.81 0.49 0.36 0.30 0.30 0.30 | +1.52 | +0.242/+0.236 | NR3 gas: 14 | +0.311, 0.387 |
| B E1, lowest root | 0.50/0.52 | 0.5145 | +0.64/+0.67 | 1.20 0.74 0.43 0.30 0.30 0.30 | +4.02 | +0.862/+0.860 | NR3 gas: 4 | +0.917, 0.920 |
| B E1, highest root | 0.30/0.30 | 0.5534 | 0.00/0.00 | all 0.30 | −1.19 | −0.409/−0.428 | NR3 gas: 2 | −1.140, 1.181 |
| B E1, DR3 monopole | 0.43/0.44 | 0.4187 | +0.39/+0.44 | 1.06 0.68 0.51 0.34 0.31 0.30 | as E1 | as E1 | as E1 | as E1 |
| B E1, gas inverted | 0.43/0.44 | 0.4167 | +0.46/+0.48 | 1.04 0.67 0.48 0.33 0.30 0.30 | as E1 | as E1 | as E1 | as E1 |

Keys are from `hb1_G5_results.json`, gas +0.005, S-core, edge r_ta, BCG as NR3, where the row was run there. Rows marked NR3 gas used NR3's inputs. The Form B and off rows have the same failing keys on both gas inputs.

**Frozen labels:** Form B E1 **MOVES, FAILS** (line, tilt, keys, X-COP, LITTLE THINGS; groups pass). The move from 0.35 is exactly 0.02, at the line, and it says little: rms is what breaks. Form A **MOVES, FAILS** (line, keys, X-COP, LITTLE THINGS; tilt and groups pass). **[EOS-ABOVE-CENTRE DEPENDENT] does not fire** (spread 0.000 at 150–250 km/s). **[BRANCH-DEPENDENT] does not fire** (spread 0.000). Both lines were read at bins pinned to the grid floor 0.30, so neither "not dependent" is informative. Outside those bins both choices matter: rms 0.505 vs 0.858 by EOS; by branch, global Υ 0.33, 0.50, 0.30, keys 14, 4, 2 (the last two on NR3's gas), X-COP +0.311, +0.917, −1.140. The frozen labels are as they are; I don't move them after the result.

Baryon potential: primary is the path's GB r²/G, as Blumenthal's. DR3's monopole raises Υ to 0.43/0.44 and rms stays above 0.41, still failing.

## Against ZN4 separately (native shape, Form B numeric, gas +0.005)
ZN4 base 12 of 15, G-OUT-M3 +4.41, X-COP +0.013, reproduced, |d| 0. With Form B: **7 of 15 at f★ 0.034, 8 of 15 at 0.0615; G-OUT-M3 +6.83/+6.23 and +6.67/+6.07; X-COP +0.595, 0.610 and +0.592, 0.607: FAIL, and worse than ZN4 without it.** Baryons without BCG, as ZN4's path. **This row isn't held to K2:** null median 3.7 %, max 8.9 (×), over 1318 calls, so some systems leave the null even with no baryons, and it reads at the median only. Median H_c is 1.47 × the table's top: it sits on the extrapolation, which is by hand. The first version of this row failed its null badly and was discarded (A4).

## Effective f, (Q − 1)/(Q_Blum − 1) at 2, 3, 4 R_d, Υ 0.5, A; NR4 asks about 0–0.2 at 150–250 km/s and low-mass η × 1.5
| V_flat | Form B E1 f | Q | Form A f | Q |
|---|---|---|---|---|
| 20–60 | −0.40, −0.63, −1.00 | 0.54–0.57 | 1.15, 2.41, 4.71 | 1.87–2.82 |
| 60–100 | −0.76, −1.34, −1.74 | 0.40–0.45 | 1.65, 3.98, 7.73 | 2.01–3.02 |
| 100–150 | 12.3, 14.9, 14.0 | 18.5–6.6 | 0.80, 1.60, 3.44 | 2.03–2.80 |
| **150–200** | **7.3, 11.8, 11.7** | **22.4–12.0** | **0.42, 0.93, 1.90** | **2.14–2.57** |
| **200–250** | **9.5, 12.4, 12.1** | **20.5–9.4** | **0.53, 1.25, 2.62** | **2.23–2.68** |
| 250–400 | 8.9, 11.5, 11.3 | 20.5–9.6 | 0.54, 1.25, 2.46 | 2.31–2.84 |

**Neither reaches NR4's ask at 150–250 km/s; Form B is about 40 or more times over it.** Form A's Q is largely its own null, below. Form B's low-mass Q < 1 lowers the halo there, which is the same direction as a low-mass need, but it comes from the dilute branch, not a clean effect, and not the η × 1.5 that NR4 mapped.

## How this reads
- **The fluid doesn't relieve the pinch. It over-contracts spirals and dilutes dwarfs.** Spirals land on the concentrated root (median H_c 3.4, H_c to 6.0, central density several tens ×, Q 10–20) and dwarfs on the dilute one. A Form with one continuous response doesn't exist here.
- **Form A at Φ_b = 0 isn't the core.** Sinc radius 2.56–2.82 r₀ = 0.15–0.31 R₂₀₀, against the halo to R₂₀₀. Mass held: M(<r₀) × 1.77–1.94, M(<3 r₀) × 2.10–3.00, central density × 1.08–1.15. So "fixed by the uncontracted halo" is off by about a factor 2–3 in the inner mass before baryons, and a large share of Form A's low Υ is that. Its bare K unheld returns 0.87–0.93 of the edge mass.
- **Form B at Φ_b = 0 is the core, and a poor equilibrium.** Null to 4.9e-6 in the path. But three roots at fixed mass and edge at every N halo (H_c about 0.4–0.6, 1, 2.6–3.3); dm(x_e)/dH_c at the null is −0.68 to −1.00 at all six masses. Local Γ = dlnP/dlnρ stays below 4/3 (0.98 centre, 1.19 at x 10, 1.26 at x 100). These point to radial instability by the standard criteria. No dynamical run tests it. (γ = 2 in the criteria means c_s² ∝ ρ near the centre, not Γ = 2.)
- **No continuous path.** On 25 sampled SPARC galaxies, 15 have a step > 0.3 in ln H_c as Φ_b grows from 0 to its value. On a test profile the null branch ends at M_b about 3e-4 M_t. So the graded equilibrium is usually not reachable by adiabatic baryon growth from the core: the "nearest root" is a label, not a history. Keys 14 of 15 for Form B therefore shouldn't be read as near-success: X-COP fails by +0.311, and the root picked varies across systems.
- **No universal P(ρ).** Label: **NO UNIVERSAL P(ρ).** c_s²(ρ) differs by 3.1–3.4 dex between 10¹⁰ and 10¹⁵ on overlapping densities. 10¹²'s EOS on other masses at Φ_b = 0: M(<r₀)/core 0.0025, 0.0041, 12.5, 11.4, 10.5. One K has one radius, r₀ runs 2.3 to 238 kpc. So Form B's "no new number" is one function per halo: the EOS would have to remember the halo's mass, with no carrier. The same applies to Form A's K. And above central density it's an extrapolation, a function choice.

## Physical consistency, no gate
- c_s centre: Form B 26, 53, 107, 226, 464, 960 km/s; Form A 69, 140, 278, 581, 1161, 2346 km/s at 10¹⁰…10¹⁵.
- Form B at mean density, z 3: 16, 35, 75, 161, 345, 741 km/s, all above X22's ≤ 6. These apply a halo's EOS to the background, which only shows that it doesn't carry over.
- Form A μ = 479, 193, 75, 32, 13, 5 /Mpc: below BOLTZ1's crossing (2.04e4) and BBN (1.24e8) floors at every mass, and below the forest floor (56.6) from 10¹³ up. BOLTZ1's "pressure core excluded in this family" applies directly; the BBN floor is for this quadratic form.
- η and the core normalisation come from pressureless zooms, and a fluid with these c_s wouldn't collapse the same way. So Form A and B feed a collisionless number into a pressure fluid. Inconsistent, named, not fixed. CR1's R5 stays open: hydrostatic equilibrium assumes crossing was cured. DR2's point holds: this is pressure, not charge. No a₀, no particle.

## My expectation on record
Held: Form A null off, Υ below Argon's, bins miss; Form B line and tilt fail, f above NR4's; NO UNIVERSAL P(ρ); low-density c_s far above 6 km/s. Wrong: I expected f near or above 1, and it is about 10; I expected dwarfs contracted, and they dilute. I expected clusters ≤ 13 keys with G-IN-Mall worse, and Form B on the S-core gets 14 with G-IN-Mall +0.49. "E1, E2, E3 differ" holds in rms, not in the frozen line.

## Limits
Spherical; baryons fixed, no back-reaction. Bins at 0.30 are the grid floor, so Form B's 150–250 miss is understated. M_b inside the first grid point r², as the path has it. Edge held with no fluid outside, as the grader. Keys at gas +0.005 on the S-core are a different path from ZN4's. Form A's mass-held choice is mine, from the criteria. KiDS, Local Group, Milky Way not run. LOW, HIGH and independent grid not run, because they were required only for a win.

## Checks
K1 EM1 off and Blumenthal vs NR3 MEDIAN, SPARC and preds, 0. K2 Form B null: test ≤ 7e-7 and 7e-9 at a truncated edge; path sample 4.9e-6; whole row M_b × 0 vs off 5.6e-6. K3 substeps × 2: 2.0e-7, 2.4e-6. K4 per A2: frozen form failed; 1e-4 to 1e-6 linear, off by 1.7 %. K5 hydrostatic 5.4e-5, Poisson 4.5e-4, mass 4e-12. K6 sinc mass and profile, solve_ivp cross-check 1e-5. K7 r₀ 2e-14. No-root 0 in every row. Gas patch bites, up to 0.57 % in preds. ZN4 base |d| 0. MUTATE Φ_b × 2: Υ 0.33 → 0.30, rms moves 0.061; |dΥ| 0.030 passes, Υ hits the floor.

**Process:** MAIN crashed once on an empty-list bug in my stats code after its first row, with no effect on any number; it resumed from the checkpoint. A3 and A4 came after some results, disclosed there.

κ = ½ FITTED. Not theory closed.
