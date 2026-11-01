# DR4_orbit_count_memory: ARGUMENT FAILS [FILAMENT PAIR ONLY]. box⁻¹R is a potential plus a cosmic calendar, not an orbit count. N_dyn does split filaments from discs, but clusters aren't N ≤ 1 at a single graded radius

Criteria: `FROZEN_CRITERIA.md` (f3e1877327), committed alone first. `dr4.py`, `dr4.out`, `dr4_results.json`, MUTATE `dr4_MUTATE.*`. κ = ½ FITTED, unused. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind:** hand estimates were made first and disclosed. No gating rule was frozen or graded, since none earned it.

**Record.** The operator was already tested: CFG123 and CFG153, scoped no-go for the static DW/RR response; CFG70, memory timescale doesn't change the static reaction. The N_dyn gate wasn't. Matching Theorem: Zenodo 22261001, `opus_48_extended_research/papers/THE_MATCHING_THEOREM.md`.

## 1. What box⁻¹R actually is
Retarded, the kernel lies on the light cone, not a worldline. Total X = X̄(t) + 2Φ/c². Light crosses 1 Mpc in 3.3 Myr, so memory inside a well is suppressed by about (r/ct)², 6e-8.

| Site | X̄ | 2Φ/c² | total X |
|---|---|---|---|
| z = 3 filament, δ 1–100, L 0.1–1 Mpc | −12.7207 | −1.5e-8 to −1.5e-4 | −12.7208 to −12.7207 |
| SPARC disc, all points, p5–p95 | −16.0730 | −9.4e-6 to −1.6e-7, median −1.7e-6 | −16.07303 to −16.07302 |
| X-COP, x 0.1–0.7 R₅₀₀, p5–p95 | −16.0730 | −1.6e-4 to −5.7e-5, median −1.1e-4 | −16.07319 to −16.07309 |

- **L1 FAILS. Discs lie strictly between filament and cluster,** so no monotonic f(X) isolates them.
- The z = 0 disc-cluster gap is 1.1e-4, which is 6.8e-6 of |X̄|. It's clean, but it's a potential-depth cut, needs a fitted f with a feature at that place, and a disc in a cluster reads as the cluster.
- z = 3 versus z = 0 is a calendar: 3.35, or 1.9e6 disc depths. A z = 3 galaxy and a z = 3 filament share X̄.
- **L2 FAILS.** X̄ gained since z_f: disc −1.65, cluster −0.96, ratio 1.72. N ratio 9.8. A fixed circular orbit adds nothing from the well. X̄'s drift per orbit is −0.048 at the Sun and −1.13 at 1 Mpc in a cluster, so it counts cosmic time. The text's "tracked as N_dyn" has no derivation behind it.

## 2. N_dyn from real profiles
T = 2πr/v_c; native z_f (X73); ceiling uses full age. Native t₀ 13.77 Gyr.

| X-COP, 12 clusters, M_FORW | r kpc | N, z_f (range) | N, ceiling |
|---|---|---|---|
| 30 kpc | 30 | 14.4 (5.5–18.3) | 43.8 |
| 100 kpc | 100 | 5.8 (3.5–6.7) | 18.5 |
| x 0.1 | 124 | 4.9 (3.2–6.0) | 15.7 |
| x 0.3 | 373 | 2.4 (1.9–2.9) | 7.3 |
| x 0.5 | 621 | 1.6 (1.3–2.0) | 5.0 |
| x 0.7 | 870 | 1.15 (1.01–1.27) | 3.6 |
| R₅₀₀ | 1242 | 0.80 | 2.5 |
| R₂₀₀ | 1977 | 0.52 | 1.7 |

M_NFW agrees from 100 kpc out (N 5.61 there), and gives 11.1 at 30 kpc.

SPARC, 175 galaxies, 3391 points, z_f: N p5 6.4, median 22.9, p95 138. Last measured point: p5 4.2, median 10.5, minimum 2.45. Only 17 % of points and 17 % of galaxies' medians lie in 30–50. Reference disc (8.2 kpc, 230 km/s): 32.4, ceiling 62.9, so the claim's number is the solar radius. The same halo reads 2.3 at 100 kpc and 0.79 at R₂₀₀. Any well reads (t₀ − t_f) 10H₀/2π at R₂₀₀.

- **L3 (claim, N_c = 1) FAILS.** Share of the X-COP grid with N ≤ 1: **0 of 60**, on z_f and on ceiling, and SPARC is 100 % above 1. The one threshold with no new number calls every graded cluster radius "disc".
- **L4 FAILS as frozen, one variant passes.** Best balanced misclassification: z_f **0.021 at N_c 6.0** (M_NFW 0.023), ceiling **0.078 at N_c 18**. Line 0.05 on both. Using last points only on z_f: 0.086. So on z_f a threshold near 6 does nearly split the X-COP grid from SPARC. It's FITTED, it triples with the age convention, and z_f favours it, since a cluster's inner region is older than its half-mass time. N_c 6 also turns clusters on inside about 100 kpc and turns an L★ disc off beyond about 45 kpc. Not graded: the frozen criteria don't allow a fitted threshold to count as surviving.
- **L5 PASSES.** z = 3 filament ceiling N: 0.105, 0.247, 0.748 at δ 1, 10, 100, below SPARC's p5 6.4. Background N is 0.06–0.07. This pair is really split, but a collapsed/uncollapsed test does that, and a compact z = 3 disc is already N about 35.

N is √(mean enclosed density) × age: N = 1, 5, 30 at 8 Gyr are 843, 21 080, 759 000 × ρ_m(0). It's a density gate with a slow age factor.

## 3. What N_dyn would add (L6)
N_dyn isn't a local covariant field. The form that produces it is u^μ∇_μ N = √(4πGρ̄(<r)/3) / 2π, and that adds:
1. **A clock scalar N**, a new first-order transported field, and it isn't X. 
2. **A unit timelike flow u^μ,** which route E doesn't carry as a gravitational field. Baryons or cold fluid would have to be chosen.
3. **√ρ̄,** non-analytic in R, and using mean enclosed density is a further spatial non-locality. Local R gives a different number.
4. **A start surface for t_coll.** Started from the beginning, the unbound background itself accumulates dN/dlna = 0.1125 in every era, reaching N = 1 after 8.9 e-folds; z = 1100 to 3 gives 0.63, z = 1e9 to 3 gives 2.2. So it needs a condition such as θ = 0 at turnaround.
5. **N_c,** unless N_c = 1, which L3 kills.

It's also not single-valued. Streams at one point in a halo have different histories. And N only rises along a flow, so material accreted in old groups brings its clock into a cluster unless a reset rule is added. That last point is an argument, not computed here.

**Matching Theorem.** Its proof uses c_s as a function of u alone. A c_s(u, N) would step outside that, so a clock can formally evade it, and L5 says the forest-versus-disc pair can be told apart. But that escape is due to the added clock, not to box⁻¹R, and the fluid would still have to be removed from discs after it has fallen in (the ER1 question). The Bullet-cluster part of that paper wasn't examined.

## Checks
K1 X′ −1.99994 (−2). K2 X̄(0) −16.087 vs CFG123's 16.035, +0.32 %. K3 kernel vs 2Φ NFW 1e-15. K4 age 1e-6 line passed. K5 2e-16. K6 z_f exact; X-COP M_FORW(R₅₀₀)/M₅₀₀ 0.977. K7 175, 12. MUTATE (X-COP v_c ÷ 30, depth shallower than filament): L3 flips to pass, discs stop being between; bites.

**Limits.** Background is flat with constant ρ_DE at native Ωm, h, not the framework's evolving ρ_DE; no line sits that close. X̄'s absolute value depends on the start, its differences don't. Filament is a uniform sphere; δ and L are a bracket. SPARC M₂₀₀ is V³/(10GH₀), z_f held flat below 10¹¹. Only 2π r/v_c used; r/v_c scales all sites alike and doesn't change overlap.

My expectation held, except that L4 on z_f came out passing its line, closer than I expected.

κ = ½ FITTED. Not theory closed.
