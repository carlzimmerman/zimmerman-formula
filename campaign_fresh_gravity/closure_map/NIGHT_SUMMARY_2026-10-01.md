# Night summary, 2026-10-01

Every lane below was re-run by the orchestrator from the committed state before it was recorded; the details and caveats are in `campaign_fresh_gravity/STANDING_2026-09-29.md`. κ = ½ is FITTED. Nothing here says the theory is closed or that the data favour the framework. The cold mass (Ω_c h² ≈ 0.12) is still required, and no dark-matter particle is added.

## Bottom line
- **Closure.** Four owner-directed swings (CFG242–245) are scoped no-gos, and PAPER39 maps 25 routes. The requirements are a READING of the scored classes, not a theorem: an early cold fluid present before structure forms, ownership that remembers boundness, a distribution that carries the M^½ scale itself, and no created rest mass.
- **The 32π / κ = ½.** No door was closed wrongly (CFG263), and three fresh routes failed for named reasons, including the owner's horizon-quarter idea (CFG264). In any units, a mechanism whose only scales are an acceleration and H cannot give κ = ½. The open target: an a₀-sector energy density coupled to gravity with a coefficient that a principle fixes at 4.
- **a₀(z).** Twelve public high-z samples were scored. None measures a₀: each is limited by missing or uncalibrated gas, or sits in CFG240's ill-conditioned regime. The two conditioned samples (the Danhaive 41 and KMOS3D) lack gas, and 38 of the Danhaive 41 lie beyond ALMA's declination limit (CFG266).
- **Satellites.** B's ultra-faint failure (3.5–3.9σ) survives the 2026 dispersions (CFG259), and the corrigendum to their source changes nothing.
- **DR4 (2 Dec 2026).** Ready: Amendment 18 is filed and the pipeline has been rehearsed end to end on DR3. For B it is a survival test against the merged law: decisive against Arm A's ν_RAR kernel, 2.3–3.7σ (canonical) against the P2 kernel.

## Lanes recorded today
| lane | what | verdict | commit |
|---|---|---|---|
| CFG240 | the calibration wall as Lean theorems + Fisher | conditioning, not non-identifiability; σ(log a₀) ≥ 3σ/√N | 7b73ef6a0 |
| CFG241 | hostile referee of PAPER38 | 2 MAJOR, wording only → v1.2 deposited | a95c318e3 |
| CFG242 | closure: ownership latch; foliated BIMOND | scoped no-gos (no memory; not hyperbolic) | e04b22b5a |
| CFG243 | closure: dust created at turnaround (owner lineage CFG251) | no-go: 10^−1376.8 of Ω_c h² at z = 1100 | e8b702457 |
| CFG244 | closure: bound part of an early cold fluid | no-go: M^0.33, not M^½; satellites lean to bound cores | 50c8c7267 |
| CFG245 | closure: vacuum-rate relaxation | no-go: Γτ ≤ 0.79 against ≈ 4.1 | 48ef9f534 |
| CFG255 | KiDS lens-z split | NOT POSSIBLE; non-discriminating | ec1a9bffc |
| CFG256 | samples against the CFG240 requirement | none at z ≳ 1; SKA is the route | fba22ef48 |
| CFG257 | newest UFD kinematics + table transcriptions | binary corrections ⅕–⅓ of B's offset | 721804f97 |
| CFG258 | MIGHTEE anchored-5σ pre-flight | NOT POSSIBLE; the 5σ is consistent with selection | cdedfca46 |
| CFG259 | B's UFD offset with the 2026 dispersions | unchanged (3.5–3.9σ) | 27f54e6ab |
| CFG260 | BUDHIES z ≈ 0.2 | not a calibrated point | d7eeb195b |
| CFG261 | KiDS absolute a₀ in z-thirds | class-dependent; M*-limited | 80fd3d666 |
| CFG262 | MUSE-DARK z-thirds by route | route-dependent | fb24a5922 |
| CFG263 | audit of the 32π no-gos | no door re-opens | 35058745f |
| CFG264 | untried routes to the rational 4 (+ owner route) | no derivation | 236771412 |
| CFG265 | hostile referee of PAPER39 | 1 CRITICAL, 3 MAJOR → v1.1 | e36c38b10 |
| CFG266 | gas for the Danhaive 41 | 38/41 beyond ALMA; not reachable | 8f0526f33 |
| CFG270 | KMOS3D 192 cube fits | stars-only upper bound; gas-bracketed | b2e86a913 |
| CFG271 | HZ9 | vacuous bounds | a18b17d72 |
| CFG272 | ALPAKA five discs | ill-conditioned | d993f02dc |
| CFG273 | Danhaive gold 41 | conditioned, gas missing; upper bound only | 208944196 (+ 42b45bfc0) |
| CFG274 | Amvrosiadis eight discs | 7/8 no root; near-Newtonian | 255f07244 |
| CFG277 | Roman-Oliveira four [CII] discs | gas vs dynamics; not a₀ | 0f6c4cd58 |

## Papers
- **PAPER38** v1.2 is deposited (DOI 10.5281/zenodo.23085582, concept 23073071). v1.3 (the DR4-paragraph correction) is prepared, not deposited (180e14149).
- **PAPER39** v1.1 (the closure map) is prepared after the CFG265 referee, not deposited (12de6965e, 80aa3a19a).

## Waiting on the owner
1. Deposit PAPER38 v1.3 (`--newversion 23085582`) and PAPER39 v1.1.
2. Before DR4: a registered Gaia archive account, and whether to file Amendment 19 (pre-registering the sync correlation fallback).
3. The calculation chat's open download question (in that chat).
4. Whether to scrub the owner's name and home path from the 401 held peer files so they can be committed.
