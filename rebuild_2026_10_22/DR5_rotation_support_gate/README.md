# DR5_rotation_support_gate: REDUCES TO EXISTING ROWS, on the frozen line exactly. The gate is posited, not derived; at σ 10 km/s it returns NR3's off row on SPARC and its response row on clusters, and both fail

Criteria: `FROZEN_CRITERIA.md` (17b9d33134), `AMENDMENT_A1.md` (c84d3f238e). `dr5.py`, `dr5_tail.py`, `dr5.out`, `dr5_results.json`, `dr5_g1200.json`, `dr5_verdict.json`. UR1, NR2, NR3 read only. κ = ½ FITTED, unused. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind.** Rule and σ are BY HAND. **Criteria commit landed after the first run** (index.lock); the text didn't change. The idea came from an outside AI's text, tested as a claim. The σ 10 km/s value is a look-up, PROVISIONAL; SPARC has no σ.

## Rule, M_f = M₀ + (1 − S)(M_contract − M₀), EM1, NR2's medians, canonical
| σ | 1 − S, bin centres | Υ A/B | rms A | tilt A/B | Υ by V_flat, A | LITTLE THINGS A |
|---|---|---|---|---|---|---|
| NR3 off (K1) | 0 | 0.75/0.76 | 0.0690 | +0.59/+0.59 | 1.20, 1.18, 0.90, 0.57, 0.62, 0.77 | +0.153 |
| **10 km/s, primary** | **0.20, 0.048, 0.020, 0.010, 0.006, 0.003** | **0.73/0.74** | **0.0686** | **+0.54/+0.57** | **1.20, 1.14, 0.89, 0.57, 0.62, 0.77** | **+0.147** |
| σ = V/3 | 0.25 everywhere | 0.60/0.61 | 0.0649 | +0.43/+0.44 | 1.06, 0.93, 0.74, 0.47, 0.54, 0.68 | +0.143 |
| 30 km/s, FITTED ask | 0.69, 0.31, 0.15, 0.08, 0.05, 0.03 | 0.64/0.65 | 0.0669 | +0.30/+0.31 | 0.82, 0.89, 0.82, 0.53, 0.60, 0.76 | +0.130 |
| NR3 response (K2) | 1 | 0.35/0.36 | 0.0670 | +0.17/+0.18 | 0.49, 0.53, 0.46, 0.30, 0.36, 0.47 | +0.116 |

Every row on Υ's line fails the tilt (≤ 0.15) and LITTLE THINGS (≤ 0.10).

## The three questions
**(a) Dwarfs are rotation-supported too.** At σ 10, S is 0.80 or more at every V_flat. The gate's difference is real in sign, since 1 − S ∝ σ²/V² acts more on dwarfs, but only the 20–60 bin has much, and that bin stays pinned at the Υ cap 1.20. A scale-free σ/V gives no difference at all. Even 30 km/s, three times HI in gas-dominated discs, stops at +0.30.

**(b) S → 1 returns NR2's off row.** Yes: Δ Υ 0.02, Δ tilt 0.05 at σ 10.

**(c) Clusters, S → 0, read NR3's response row, not regraded:** 14 keys, G-IN-Mall −2.05, X-COP −0.097, 0.146, groups +1.50. X-COP fails on that row at any galaxy σ, and the response there is outward (UR1), so "full contraction" in clusters is the wrong sign.

So the rule is the off row in discs joined to the response row in clusters. No result here could clear it.

## Energy, EM1 smooth core, Υ 0.50, medians by V_flat
| V_flat | n | M_c/M_b | inside 5 R_d | T_rot/E_undo | T_rot/E_bind | T_rot/E_in | (v_L/V)² | m, φ_v = 1 (eV) | φ_v at 2e-19 eV |
|---|---|---|---|---|---|---|---|---|---|
| 20–60 | 12 | 17.4 | 3.63 | 1.2 | 0.089 | 0.26 | 0.042 | 1.1e-23 | 5.7e-5 |
| 60–100 | 35 | 14.0 | 3.58 | 1.4 | 0.105 | 0.27 | 0.044 | 2.8e-24 | 1.4e-5 |
| 100–150 | 23 | 12.5 | 2.73 | 1.2 | 0.121 | 0.35 | 0.087 | 1.3e-24 | 6.4e-6 |
| 150–200 | 25 | 11.0 | 1.33 | 0.6 | 0.104 | 0.45 | 0.204 | 6.7e-25 | 3.4e-6 |
| 200–250 | 18 | 10.0 | 1.69 | 0.8 | 0.121 | 0.37 | 0.141 | 3.2e-25 | 1.6e-6 |
| 250–400 | 10 | 9.5 | 1.47 | 0.9 | 0.163 | 0.42 | 0.187 | 2.1e-25 | 1.0e-6 |

- **Expel: SHORT in every bin.** The claim's M_c/M_b of 10–20 is about right (9.5–17). All the disc's rotation energy is 6 to 11× under the halo's binding, and 2 to 4× under clearing just inside 5 R_d.
- **Undo: not affordable in every bin; my expectation was wrong here.** T_rot/E_undo is 0.6–0.9 above 150 km/s, the bins that most need it, and only 1.2–1.4 below. This counts all of T_rot at perfect delivery, while T_rot isn't free at fixed angular momentum.
- **Angular momentum.** If the fluid inside 5 R_d took all the disc's L, centrifugal support is 4–20 % of gravity, and the disc would have none left.
- **Vortex cores** fill the volume only at m ≈ 2e-25–1e-23 eV, the same class as CR1's 5.6e-24 eV wave match and 1e4–1e6 below the record's floor. At the floor they remove 1e-6 to 6e-5 of the volume. φ_v = 1 means ξ about R: one disc-sized core, not a lattice.

## Desk results (criteria)
- **Vortices without quanta.** A shift-symmetric non-compact phase has no vortices. A compact phase has them classically, with no quanta, at the price of one new constant, the period Γ₁: FITTED. On CR1's rows, the irrotational class (C, D, I) lacks stream crossing, so route E's zoom η isn't native to it; the classes that cross (E–H) carry quanta, which the owner's rule forbids as a particle. No row carries the vortices the door needs.
- **No torque.** Gravity is a gradient, so by Kelvin it gives a barotropic field no circulation, bars included. LC1's contraction comes from a non-rotating analytic disc potential.
- **Vortices don't expel.** They displace by core volume only, as above. The word borrowed from superconductors doesn't describe this.
- **Prior art:** `two_state_mechanism_2026_10_24/vorticity_gate` has a covariant-looking cousin and hit (a) too: small rotating objects stay protected. Its β and L were selected, it has no formation route, and its manifests fail current validation.

## Label
Frozen: **REDUCES TO EXISTING ROWS**, on the line. A background's tilt moves by 0.05 at 1200 points (line ≤ 0.05), and 0.06 at 300. The tilt reads on Υ's 0.01 grid, so the comparison rounds float noise at 1e-9; before that rounding the script printed NEW SPARC ROW on a difference of order 1e-16. Disclosed: the label is a knife edge, the physics isn't. On either label SIG10 fails the tilt at +0.54 and LITTLE THINGS at +0.147, and clusters fail. **Energy: EXPEL SHORT; undo not affordable in every bin.** Stopped; nothing further regraded. My expectation held on the row (I wrote tilt near +0.55) and on expel, and missed undo, as above.

## Checks
K1 f ≡ 0 against NR3 off: 5.6e-6 at 300 points, **missing the frozen 1e-6**, from the grid (A1); 3.9e-7 at 1200. K2 f ≡ 1 against NR3 response: 0. K3 1.1e-16. MUTATE swap S: Υ 0.73 → 0.36, bites.

## Limits
σ is one number per row with no measured value per galaxy; stellar dispersions aren't in SPARC. A mass-weighted σ is not run, and would need data this lane didn't download. V = V_flat, not a local v_rot. Partial S in clusters and groups isn't computed; both endpoints fail. KiDS, Local Group, MW not run. Energies are bookkeeping, not a mechanism. Noise band of NR2's η not propagated.
