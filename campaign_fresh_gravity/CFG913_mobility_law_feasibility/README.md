# CFG913: is there one mobility law α(local variables) for mergers, galaxies and dwarf clumps?

**Class as frozen: INFEASIBLE IN THE DECLARED CLASSES.** All 42 declared class members are infeasible on the record's own
numbers. All ten K-tests pass. The frozen MUTATE tooth DOES NOT BITE. A post-hoc positive control returns FEASIBLE WITH ONE
NEW CONSTANT once both obstructions are removed together, so the decision logic can return a feasible answer.

**What it says.** No law α = α_hi·F(x) in the record's local variables can be ≈ 0 for a merging cluster's cold energy,
≳ 0.5 for a settling galaxy and ≲ 1e-3 to 1e-2 for a dwarf's clump all at once. Two pairs of constraints block it, each on its own:

- **Mergers against galaxies (M–G).** Density, g/a0, y_J, q and δ do not separate them. The merging sub's cold energy
  (ρ_m 1.5e-4 to 5e-2 M_⊙/pc³, g/a0 0.003–1.4) shares states with galaxy regions that must stay mobile. The Mach-like variable
  separates them only because the P0 galaxy test holds the galaxy's cold energy at rest (𝓜 = 0). Even then the threshold must
  sit below 0.02 (all-baryon frame) or 0.085 (gas frame), which is a new constant. At the natural sonic value 𝓜 = 1 the
  separation fails:
  - In the all-baryon frame, 54–56% of the merger core states (69–71% weighted by cold mass) are subsonic. The sub's stars move
    with its cold energy (star share 0.83–0.85 there).
  - In the gas frame, 27–37 of 2223 states are subsonic. They sit 100–200 kpc from the cold peak, where the sub's own cool-core
    cloud or retained gas dominates the local gas.
  - Real infall gives galaxies 𝓜_ff = 1.6–4.1, which reverses the ordering. A Mach factor that waits for collapse gives CFG598's
    P2 outcome instead: the MW is overfilled at every α.
- **Clumps against galaxies (D–G).** No declared variable separates them on both footings. The clump and the galaxy are both at
  𝓜 = 0, both cold-dominated (q 0.95–0.99 against 0.90–0.995), and in the same g/a0 range (0.01–0.26 against 0.004–0.42).
  Density comes closest:
  - At the conservative clump edge (ρ_* = 6.1e-3 / 6.8e-3 M_⊙/pc³), the MW is frozen inside 9.1 kpc. The inner cells starve
    (min q 0.36 / 0.32 at about 4 kpc) and the inflow jams at the threshold (q up to 113 / 153 at 8.8 kpc). M_c/M_ph(<30 kpc) is
    4.8 / 5.4.
  - At the lenient edge (r ≤ r_50, ρ_* = 0.154 / 0.192), the frozen region shrinks to ≤ 2.1 / 1.9 kpc. The canonical footing
    passes (min q 0.9963). The alt footing misses by one baryon-dominated cell: q 0.973 at 1.2 kpc, where ρ_ph/ρ_b = 0.18.
- **Common cause.** To finish settling inside 30 kpc, the galaxy must keep its dense inner region mobile. Its transport-weighted
  states are outer-halo states (ρ_m ≤ 1.4e-3 M_⊙/pc³, y_J ≤ 0.28 at the 99% quantile). Those alone would be separable from the
  clump in density and from the merger in y_J. But freezing the inner region either starves it or jams the one-way inflow
  (PH2, PH2b).
- **Minimal variable set:** none among the six declared variables. A feasible law needs a variable outside this list for D–G.
  Outside the P0 idealisation it also needs one for M–G, or it needs two new constants plus a lenient clump reading that the alt
  footing does not support.

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are kept apart and never pooled; FEASIBLE would have needed both. Cold energy
is real gravitating mass; there is no particle species. No new constant is adopted. Not "theory closed". Nothing here says the
data favour the framework. The lane compares the record with itself; the only data enter through the source lanes' frozen
verdicts.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (957aaab55), block 910–919 (LEDGER.md:662).
- **Script:** `cfg913.py`.
  - `OMP_NUM_THREADS=1 nice -n 10 python3 cfg913.py` writes `cfg913.out`, `cfg913_results.json` and `cfg913_gtests_cache.json`
    and exits 0.
  - `CFG913_MUTATE=1 …` writes `cfg913_MUTATE.out` and `cfg913_results_MUTATE.json`. It exits 0 because the tooth did not bite;
    it would exit 1 if it bit.
  - One process, under 200 MB. 147 G-test PDE runs of 1–11 s each (332 s in total), no step cap hit, mass error ≤ 6.4e-15. With
    the cache present, a re-run takes under a minute.
- **Inputs, all read only:**
  - CFG598 `cfg598_lib` (P0 drift PDE, MW host) and CFG599 `cfg599_lib` / `cfg599_sim` (progenitors, `epoch()`), imported;
  - CFG623's cached α = 0 runs;
  - the result JSONs of CFG623, 639, 598, 542, 882, 889 (`parts/`) and 877.
  Nothing was downloaded and no other lane was edited.

## The three constraints, reproduced (K-tests, all PASS)

| K | source (committed numbers) | bound used here |
|---|---|---|
| K-M1 | CFG623: α = 0 ALLOWED on both footings (Z_B +1.09 / +1.06); 0.1, 0.3, ∞ EXCLUDED; α = 0.03 Z_B +3.12 / +2.65 | ungated value bracket [0, 0.03) |
| K-M2 | CFG639 (gate): allowed {0} / {0, 0.03}; α = 0.1 Z_B/Z_H +1.71/+1.83, +1.44/+1.88; α = 0.3 Z_B +2.87 / +2.37; gate off 71.4% | gated value bracket [0.1, 0.3) |
| K-M3 | Progenitor599 reproduces the cached runs' M_ph and M_b exactly; `epoch()` gives 2699.4 / 2686.5 km/s and d_SG 196.94 / 196.99 kpc, equal to CFG623 | merger reconstruction valid |
| K-G1 | CFG598 MW P0 min q: 0.9842 / 0.9849 at α = 0.25 (fails 0.99), 0.9928 / 0.9930 at 0.5 | α_G in (0.25, 0.5] |
| K-G2 | the G-test code with F ≡ 1 reproduces CFG598 at α = 0.25, 0.5, 1 on both footings (relative difference 0) | per-cell α code valid |
| K-C | CFG542: α_max = 1.000 (q = 1), 1.1864 (q = 1 − f_b) | α_hi = 1.0 |
| K-D1 | CFG882: α_c max 1.371e-3; α_50 6.18e-4 to 1.02e-3 | ungated clump bound |
| K-D2 | CFG889: α·t_50 = 105.5–147.5 Myr over the 8 primary gated cells | α_D,gated = 8.8e-3 to 1.23e-2 |
| K-D3 | local rate bound ln2·τ/(q·12 Gyr) at the cap radius on H2: 9.8e-4 / 8.4e-4, against CFG882's H2 α_50 8.6e-4 / 7.2e-4 (ratio 1.13 / 1.17) | α_D,loc applied radius by radius |
| K-D4 | clump profile reaches M_cl at 237.2 / 204.5 pc (CFG877 README:48–49) | D model valid |

## Local conditions in the three regimes (canonical values; alt within ~10% except where given; ρ_m/ρ_Λ differs by the footing's ρ_Λ)

| | M: merging sub, ≤ 200 kpc of its cold peak, 39 window epochs (0.21–0.59 Gyr after pericentre) | G: MW P0 at α = 0.5, flux-weighted donor states (1–99%) | D: clump on H2, r ≤ 450 pc (lenient r ≤ r_50 = 148 / 132 pc) |
|---|---|---|---|
| ρ_m (M_⊙/pc³) | 1.5e-4 – 5.1e-2 | 3.1e-8 – 1.4e-3 (2.6e-8 – 1.6e-3) | 6.1e-3 – 1.6 (lenient ≥ 0.15 / 0.19) |
| ρ_m/ρ_Λ (ρ_Λ = a0²/κ²Gc² = 8.63e-8 / 1.26e-7 M_⊙/pc³) | 1.7e3 – 5.8e5 | 0.36 – 1.6e4 | 7.1e4 – 1.8e7 |
| τ | 19 – 343 Myr | (follows ρ_m) | 3.3 – 54 Myr |
| σ_J | 115 – 634 km/s | — | 4.4 – 7.6 km/s |
| \|u_c − u_b\| | 6 – 1247 km/s (all baryons); 57 – 1856 km/s (gas) | 0 (P0) | 0 |
| 𝓜 | B 0.019 – 4.5; A 0.089 – 15.3 | 0 (P0); real infall 1.6 – 4.1 | 0 |
| g/a0 | 0.003 – 1.40 | 0.004 – 0.42 | 0.011 – 0.26 |
| y_J | 0.46 – 4.0 | 3e-4 – 0.28 | 0.04 – 0.50 |
| q | 0.035 – 0.997 | 0.90 – 0.995 | 0.955 – 0.994 |
| δ | gate-open states in (0, 1] exist (28.6% of settle steps, CFG639) | −0.11 – 0.90 | −3.3 – 0 (skin 0 ± fluctuations) |
| α bound | < 0.03 ungated, < 0.3 gated (lenient) | (0.25, 1.0] constant; else the G-test | α_D,loc 1.9e-4 – 3.2e-3; gated ≤ 8.8e-3 |

## Pairwise separability (R1: can any function of ONE variable give the two regimes different α?)

| variable | M vs G | D vs G | how decided |
|---|---|---|---|
| ρ_m/ρ_Λ | no | no (lenient: canonical only) | G-test with a step at the other regime's edge |
| g/a0 | no | no | G-test |
| y_J | no | no | G-test |
| q | no | no | G-test |
| 𝓜 | yes, by R1, but only below 0.02 (B) / 0.085 (A); not at the natural 𝓜 = 1 | no (both at 0) | ranges |
| δ | no (gate-open merger states overlap settling δ) | no (G's 1% quantile −0.11; skin at 0; CFG889) | ranges and record |

G-test details (GT1, α_hi = 1; every run fails on both footings):
- Density below the merger edge (ρ_* = 1.5e-4) freezes the MW interior: min q 0.20 / 0.18.
- Density below the clump edge jams the inflow (see PH2).
- g/a0 and y_J steps either freeze everything (min q ≈ 0.2, as α = 0) or jam (y_J < 0.46: M_c/M_ph 2.8 / 2.9).
- q steps empty or jam the inner cells.

## Classes (42 members, all INFEASIBLE IN THE DECLARED CLASS)

| class | blocking pair and why |
|---|---|
| C0 constant α | M–G: α < 0.03 against (0.25, 1.0]. D–G: α ≤ 1.4e-3 against the same |
| C1 gate α·1[δ > 0] | D–G: gated kinetic α ≤ 8.8e-3 (CFG889). M–G NOT ESTABLISHED at node resolution: lenient gated M < 0.3 overlaps G > 0.25. G for gate laws is UNDETERMINED (CFG639 Part A NOT DIAGNOSTIC). In the P0 PDE the gate gives min q 0 (GT5, report only): the reservoir deposits are locally overfilled, so they never move |
| C2 steps in ρ_m/ρ_Λ, g/a0, y_J, q (both orientations) | the step at the stricter M∪D edge fails the G-test on both footings |
| C2 step in 𝓜 / in δ | D–G (both at 𝓜 = 0) / M–G overlap and the gate's kinetic erosion |
| C3 smooth density (1/(1+z), 1/(1+z²), e^{−z}); scale from the D bound | M: α = 0.11 / 0.84 / 0.87 at the lowest merger density (needs < 0.03), and the G-test fails (min q 0.01 / 0.0002 / 0; the last two jam to M_c/M_ph 3.5 and 13.7) |
| C3 natural-scale smooth forms in g/a0, y_J (x* = 1), both orientations | fail both the D bound and the M bound analytically (no G-test needed) |
| C3 smooth Mach (x* = 1) | D: 𝓜 = 0 gives α_hi in the clump |
| C4a gate × Mach step (no new constant) | D: the clump skin is at 𝓜 = 0 and δ > 0 (CFG889 erosion) |
| C4b Mach step at 1 × density step ρ_* (one constant) | M: 𝓜 ≤ 1 at some merger states in both frames. D–G: density G-test fails at both clump edges on alt and at the conservative edge on both footings |
| C4c gate × density step | M–G: gate-open merger states lie below any clump-edge ρ_* and get α_hi ≥ 0.5 > 0.3 |
| C4d Mach step × g/a0, y_J or q step | D–G not separable in those variables |
| C5 1/(1+𝓜ⁿ) × smooth density (n = 1, 2) | M: α_hi/(1 + 𝓜_min ⁿ) ≈ 1 (needs < 0.03). D–G: the smooth density G-test fails |

GT4 (natural-threshold G-tests) was never triggered: no step class was feasible, and every natural-scale smooth form failed its
analytic D or M check first.

## MUTATE (frozen: four runs, one constraint's local conditions × or ÷ 10 each)

| run | overall | minimal set | note |
|---|---|---|---|
| MUT-A merger 𝓜 ÷ 10 | INFEASIBLE | none | unchanged |
| MUT-B merger 𝓜 × 10 | INFEASIBLE | none | unchanged: the gas-frame minimum becomes 0.89 / 0.85, still below 1 |
| MUT-C clump density × 10 | INFEASIBLE | none | the lenient D–G density separation opens on both footings (min q 0.9963 / 0.9964). The conservative edge (0.061 M_⊙/pc³) still fails (min q 0.80 / 0.72), and the merger still blocks C4b |
| MUT-D clump density ÷ 10 | INFEASIBLE | none | unchanged (worse jams, M_c/M_ph up to 16) |

**Tooth (overall label or minimal set changes): DOES NOT BITE**, reported as frozen. The infeasibility is over-determined. Both
pairs block, so any single ×10 change to one constraint leaves the other pair blocking. That makes the verdict robust to
×10 changes, but the frozen tooth does not show that the logic can return feasible.

**Post-hoc positive control (no verdict weight):** merger 𝓜 × 100 and clump densities × 100 together. Result: FEASIBLE WITH ONE
NEW CONSTANT [CONDITIONAL-P0]. The feasible classes are C4b (ρ_* at the clump edge, 0.61 / 0.68 M_⊙/pc³, passes the MW on both
footings) and C5 1/(1+𝓜²) × e^{−z}. The minimal set becomes {𝓜, ρ_m}.

## Post-hoc diagnostics (report only; added after the first full run)

- **PH1 (where the merger is subsonic).** Frame B: 1190 / 1234 of 2223 core states. Local baryons there are 83–85% stars that
  co-move with the cold energy. Frame A: 37 / 27 states, all at s = 100–200 kpc; the local gas there is the sub's cool-core
  cloud (17 / 18) or its own gas (18 / 9). CFG623's mechanism test placed most of the early offset at that cloud
  (CFG623 README:35–37). A gas-frame sonic law would leave the drift on exactly there.
- **PH2 (density step, why the MW misses).**
  - Lenient edge: the frozen region holds 1.3% / 1.1% of M_ph(<30 kpc). Canonical min q 0.9963 at 28.9 kpc. Alt min q 0.9733 at
    1.21 kpc (ρ_ph/ρ_b 0.18). M_c/M_ph 1.006 / 1.007.
  - Conservative edge: frozen out to 9.1 kpc (20–21% of M_ph). Starved at about 4 kpc; jammed at 8.8 kpc.
- **PH2b (y_J step at the merger edge).** Frozen out to 21.6 kpc by t0, as the filling raises y_J; holds 70% of M_ph(<30).
  min q 0.40 / 0.37, M_c/M_ph 2.8 / 2.9.

## Corrections and disclosures (2026-10-20)

- **Correction 1 (implementation, before any class was read).** In the first full run the merger profiles were interpolated onto
  the progenitor grid's r = 0 node, whose stored density is singular. At s = 0 this gave ρ_m up to 6e3 M_⊙/pc³ and σ_J = 0.
  Distances are now floored at the first non-zero node (0.5 kpc). That run was stopped during GT1, its G-test cache deleted,
  and everything re-run.
- **Development crashes, no physics change.**
  - A JSON-parsing error on CFG882's per-footing summary keys (before any output).
  - A JSON serialisation error after a complete run (float dictionary keys). The verdict section of that run and of the
    committed run are identical (diff checked).
- **Post-hoc additions (no class weight), made after results had been seen:**
  - the "share of M-core states with Mach ≤ 1" lines (after the stopped first run);
  - PH1, PH2, PH2b;
  - the positive control.
- **Approximations.**
  - M states are static spherical CFG599 profiles centred on the simulation's peaks (not the simulated fields). Velocities come
    from ±2-epoch peak differences. δ in mergers is taken from CFG639's logic, not computed.
  - G uses CFG598's one-sided, drift-only P0 PDE, the source of α ≳ 0.5. D uses the record's two-sided drift (CFG882/889).
    The source lanes use different drift forms.
  - The MW only; the groups were not re-run. α_hi = 1.0, plus 0.5 for density, where nothing changes.
  - D-lenient uses CFG882's drift-only exact law; D-conservative uses CFG889's skin. In MUT-C/D only ρ and τ were scaled (g and
    σ_J fixed), as frozen.
- **R1 Mach "SEPARABLE"** comes from the P0 idealisation (galaxy cold energy at exactly 𝓜 = 0). It is a separation by a new
  constant below 0.02 / 0.085, and it reverses under real infall. It is not evidence for a Mach-gated mobility.
- **Not claimed:** any α_max or interpolation between merger nodes; that a feasible law exists outside the declared classes;
  κ derived; "theory closed".

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (957aaab55) |
| `cfg913.py` | script: K-tests, M/D/G regions, G-tests, decision rules, post-hoc diagnostics, MUTATE |
| `cfg913.out`, `cfg913_results.json` | main run |
| `cfg913_MUTATE.out`, `cfg913_results_MUTATE.json` | MUTATE run (and post-hoc positive control) |
| `cfg913_gtests_cache.json` | all 147 G-test PDE results, keyed by law and footing |
