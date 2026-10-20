# CFG913 FROZEN CRITERIA: is there ONE mobility law α(local variables) for the cold-energy drift that satisfies the merger, galaxy and dwarf-clump constraints at once?

Date 2026-10-20. Block 910–919 (LEDGER.md:662 reserves CFG913 for this question). Committed alone, before any script exists.

**Kind of lane.** Feasibility (constraint satisfaction) over pre-declared function classes. Nothing is fitted to data. No knob
scan: every threshold that is tested is fixed below by a rule (an edge of another constraint's region, or a natural value),
never searched. A clean "infeasible" is a valid result.

**Settings.** κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.1312e-10 (alt) m/s², never pooled; every verdict is per
footing and FEASIBLE needs both. Cold energy is real gravitating mass (class A: ∇²Φ = 4πG(ρ_b + ρ_c)); no particle species.
Every new constant is flagged. Not "theory closed". Nothing here says the data favour the framework. No downloads. One core,
`OMP_NUM_THREADS=1 nice -n 10`, each process < 1 GB. Inputs read only; no other lane edited.

## 1. The record's drift (context)

CFG638 README:23–24: v_s = −α 1_B 1_C τ∇ψ, τ = (4πGρ_m)^(−1/2), ∇²ψ = 4πG(ρ_ph − ρ_c), OU relaxation rate γ = α/τ.
CFG638 README:57–58: "A constant α cannot do both" (collisionless in mergers, fluid in galaxies). This lane asks whether a
LOCAL α(x) can. α becomes α_hi · F(x), where α_hi is the record's existing free O(1) coefficient (not new) and F ∈ [0, 1].

## 2. The three constraints (numbers as quoted in the source lanes)

**M, mergers (Bullet + Harvey through the CFG623 pipeline).**
- CFG623 README:64, :72: α = 0 ALLOWED on both footings (Z_B +1.09 / +1.06). README:65, :73: α = 0.03 UNSCORABLE, Z_B +3.12 /
  +2.65 (fails |Z_B| < 2 on value). README:66–67, :71, :74–75, :79: α = 0.1, 0.3, ∞ EXCLUDED. Rule: CFG623 FROZEN_CRITERIA.md:44–46
  (Z_B = (f − 0.045)/0.125, ALLOWED iff scorable and |Z_B| < 2 and |Z_H| < 2).
- CFG639 README:75–82 (deficit gate HG): α = 0.1 has Z_B +1.71 / +1.44, Z_H +1.83 / +1.88 (passes on value, unscorable by the
  stability rule); α = 0.3 has Z_B +2.87 / +2.37 (fails on value); frozen allowed set {0} can / {0, 0.03} alt. B-M1: 71.4% of
  cold settle steps gated off in the pericentre window, so 28.6% of merger cold steps have d > 0.
- CFG641 README:52–60: under the stars-only source and the RN reservoir the gate is off 99.96% and α plays no role (reservoir-
  dependent). Reported, not used as a bound.
- **Bounds used.** α_M,ungated: value bracket [0, 0.03) (lenient bound α < 0.03); α_M,gated (laws that contain the gate):
  value bracket [0.1, 0.3) (lenient bound α < 0.3). Strict reading: the frozen allowed sets.
- Window (CFG623 FROZEN_CRITERIA.md:60–61): t − t_peri ∈ [0.1, 0.6] Gyr AND d_SG ≥ 200 kpc.

**G, galaxies (settling to the law within the age).**
- CFG598 README:79: MW inside 30 kpc SETTLED for α ≥ 0.5 on both footings (min q 0.993 / 0.993); α = 0.25 just misses (q 0.984 /
  0.985). Rule: CFG598 FROZEN_CRITERIA.md:80, SETTLED iff q ≥ 0.99 in every cell with r ≤ 30 kpc; (i) holds iff SETTLED and not
  OVERFILLED (M_c/M_ph(<30 kpc) − 1 ≤ 0.01). README:82: groups P0 pass for α ≥ 0.5 (not re-run here; disclosed).
- Causality (CFG542 README:48): stable iff αβq < 1, so α_max = 1 (β = 1, q → 1) and 1.186 (q = 1 − f_b). CFG541 README:29:
  t₉₀ ∝ 1/α.
- **Bound used:** G-allowed constant α in (0.25, 1.0] (0.25 fails; 0.5 and 1 pass; 1.0 is the causal maximum where q → 1).
  For non-constant laws G is decided by the G-test (section 5), not by this bracket.

**D, dense dwarf clumps (retain the overfill for 12 Gyr).**
- CFG882 README:38–46: exact cumulative law ∂ₜM_ex(<r) = −Γ(r)M_ex(<r), Γ = α q/τ at r (drift-only, ungated two-sided drift);
  README:53–62: α_50 = 6.2e-4 to 1.02e-3, α_c ≤ 1.37e-3.
- CFG889 README:5–7, :16–18: with orbits and the gate, t_50 = 105–148 Myr/α, so half the clump for 12 Gyr needs α ≲ 0.9–1.2e-2
  (extrapolated; README:134, α = 0.05 keeps R = 0.70 at 1.5 Gyr).
- Clump (CFG877 README:10–12): σ = 7.53 km/s, M_cl 5.3e6 / 4.2e6 M_⊙, cored shape r_c = 104 pc, capped at M_cl; cap radius 237 /
  205 pc (README:48–49). Host H2 (3e5 M_⊙, Plummer 200 pc) as CFG882/889. Self-gravity Newtonian (CFG888 README:3–7).
- **Bounds used.** Ungated laws: α(x) ≤ α_D,loc(x) ≡ ln 2 · τ/(q · T_D) at every D-operative state, T_D = 12 Gyr (CFG882's exact
  law applied radius by radius; reduces to CFG882's α_50 for uniform α, K-D3). Gated laws: α ≤ min(α·t_50)/T_D from CFG889's
  primary cells (K-D2).

Context: THEORY_CANONICAL_2026-10-18.md:103–118 (CFG888/889 caveats: no law-boosted self-gravity; the gate erodes the clump).

## 3. Declared local variables (dimensionless; reference scales from the framework only)

The framework has no c-free reference density built from a0 and G alone (a0^a G^b cannot be a density). It provides:
(i) ρ_Λ ≡ a0²/(κ²Gc²) from the a0–Λ tie a0 = κc√(Gρ_Λ) (CFG0_own_findings_inventory.md:62; CFG172_FROZEN_CRITERIA.md:84), per
footing, κ = ½ fitted; (ii) a0 with a LOCAL velocity, ρ_ref = a0²/(4πGσ_J²) (c-free).

| x | definition | natural value (no new constant) |
|---|---|---|
| x_ρ | ρ_m/ρ_Λ (ρ_m = ρ_b + ρ_c). The ratio τ√(Gρ_Λ) = (4π x_ρ)^(−1/2) "dynamical time vs the Hubble/de Sitter time" is the same variable | x_ρ = 1 |
| x_g | g/a0, g = \|∇Φ\| of real mass (ρ_b + ρ_c) | 1 |
| x_J | y_J = σ_J/(τ a0) = σ_J√(4πGρ_m)/a0 (c-free density variable; y_J² = ρ_m/ρ_ref) | 1 |
| x_q | q = ρ_c/ρ_m | none |
| x_δ | δ = (ρ_ph − ρ_c)/ρ_ph (> 0 deficit, < 0 overfill); the gate is 1[δ > 0] | 0 |
| x_M | 𝓜 = \|u_c − u_b\|/σ_J: bulk cold velocity relative to the local baryon bulk velocity, drift excluded, over the local Jeans dispersion. Frame B (primary): u_b = mass-weighted over all local baryons (the phantom's source). Frame A (variant): gas only | 1 (sonic) |

σ_J is the record's FIX-2 target: the isotropic Jeans dispersion of the local cold density in the class-A field,
σ_J²(r) = (1/ρ_c)∫_r^∞ ρ_c g dr.

## 4. The constraint regions (operative local states), computed by the script

**M (merger).** CFG623's cached α = 0 runs (`runs/a0_{can,alt}_v2666.7_eta1.132.json`; at α ≈ 0 the states are the collisionless
ones a law must leave immobile), window epochs as above. At each epoch: points around the sub's cold peak at s ∈ {0, 10, 25, 50,
75, 100, 150, 200} kpc (M-core; primary) and also {250, 300} (M-wide; variant), 8 directions in the orbital plane. Local state by
superposing CFG599's spherical progenitor profiles (`Progenitor599`, read-only import; main 1.5e15, sub 1.5e14 with the cool core)
centred on the diag peaks (sub cold, sub galaxies, sub gas, cloud com, main cold/galaxies/gas). Velocities: centred finite
differences (±2 epochs) of the peak positions; galaxy velocities from `vgal`. u_c = ρ_c-weighted cold velocity. σ_J: ρ_c-weighted
Jeans dispersion of each progenitor's settled cold energy. δ is not computed from the fields: it is taken from the logic of the
gate and CFG639 B-M1 (gate-open merger states, δ ∈ (0, 1], exist: 28.6%).

**G (galaxy).** The CFG598 P0 drift PDE for the MW (`cfg598_lib`, read-only import; N = 300; both footings), which is where the
α ≳ 0.5 bound comes from. Report: the flux-weighted (mass moved across faces) distribution of donor-cell states at constant
α = 0.5 (1–99% quantiles). 𝓜 = 0 for P0 (cold energy at rest relative to static baryons; only the drift moves it). Variant
G-inf (report only): 𝓜_ff = v_ff/σ_J for free fall from r_ta in the settled MW at t0, the kinematics of real infall.

**D (dwarf clump).** CFG877's capped clump (CFG882's profile, cap at M_cl) on H2 plus H2's law-settled halo (ν = 1/(1 − e^{−√y})),
at r ∈ [1 pc, R_D]. D-lenient: R_D = r_50 of the clump excess (CFG882's exact law keeps M_ex(<r) wherever Γ(r) = 0, so α = 0 out to
r_50 keeps half, drift only). D-conservative (primary): R_D = 450 pc (CFG889: the overfill reaches the noise at ~350–450 pc and
orbits reach the skin). 𝓜 = 0 (equilibrium, no bulk flow); δ < 0 inside the cap, δ = 0 (± fluctuations) outside it.

## 5. Classes, the G-test, and the decision rules

**G-test.** The CFG598 P0 MW PDE run to t0 with α_cell = α_hi · F(x_cell) evaluated at the donor cell each step (subclass of
`cfg598_lib.Run`; flux and stability code copied verbatim, only α made per cell). Pass iff CFG598's (i) holds (min q ≥ 0.99 for
r ≤ 30 kpc and M_c/M_ph(<30) − 1 ≤ 0.01) on BOTH footings. α_hi = 1.0 (largest causal value at q → 1, most favourable to G)
unless stated; α_hi = 0.5 also for the candidate classes.

**Edges.** For a decreasing step F = 1[x < x_*]: M needs x_* ≤ min_M x, D needs x_* ≤ min_D x. For an increasing step
F = 1[x > x_*]: x_* ≥ max_M x, max_D x. Edges are per footing.

**Classes (declared now).**
- C0 constant α (no new constant).
- C1 gate α_hi·1[δ > 0] (CFG639 HG; no new constant).
- C2(x) single-variable monotone step, x ∈ {x_ρ, x_g, x_J, x_q, x_δ, x_M}, both orientations; threshold = one new constant
  unless the natural value works.
- C3 single-variable smooth monotone forms with one constant: rational 1/(1 + (x/x_*)ⁿ) for n = 1 and 2, and exp(−x/x_*) (n and
  the form fixed here, not tuned). For x_M, x_g, x_J the scale x_* = 1 is natural (no new constant).
- C4 two-factor products with at most one new constant: one factor separating M from G, one separating D from G. Declared
  members: (a) gate × Mach step at 𝓜 = 1 (no new constant); (b) Mach step at 𝓜 = 1 × density step at ρ_* (one constant ρ_*);
  (c) gate × density step (one constant); (d) Mach step × the C2 step of any other variable that passes the D–G test.
- C5 smooth two-factor: 1/(1 + 𝓜ⁿ) (n = 1, 2; natural scale) × the C3 density forms.

**Rules.**
- R1 (pairwise, any function of one variable). A pair (G, K) is SEPARABLE in x only if a step at K's edge passes the G-test
  (PDE variables x_ρ, x_g, x_J, x_q), or, for x_M and x_δ, only if K's range lies strictly on one side of G's exact range
  (G-P0: 𝓜 = 0; G: δ runs from ≈ 1 down to ≤ 0.01). Overlapping ranges in x_M or x_δ = NOT SEPARABLE (no function of x alone can
  give one state two α values).
- R2 (C2). Feasible iff the G-test passes with x_* at the M∪D edge (the stricter of the two edges) on both footings. The
  admissible interval of x_* is reported as [lowest pre-declared tested value that passes, edge]; its lower end is NOT scanned.
  If feasible and the natural value lies on the admissible side of the edge, the G-test is also run at the natural value: pass
  = FEASIBLE WITH NO NEW CONSTANT.
- R3 (C3). The constant is set by the D bound at the D edge: α_hi F(x_D,edge) = α_D,loc(x_D,edge) (the most G-favourable
  admissible value); the D bound must also hold at every D state, the M bound α < α_M at every M state (lenient brackets); then
  the G-test.
- R4 (C4/C5). Feasible iff the first factor makes M satisfied (Mach step: 𝓜 > 1 at every M state; smooth Mach: α_hi/(1 + 𝓜ⁿ) <
  α_M at every M state with α_hi ≥ 0.5) AND the second makes D satisfied AND the G-test with both factors active passes (under P0
  the Mach factor is 1 for G). Gate laws use the gated M and D bounds.
- R5. G for gate laws: the record's test is CFG639 Part A, NOT DIAGNOSTIC, so G is UNDETERMINED for gate laws; a P0 G-test with
  the gate is run and reported only.
- R6 (qualifiers). Any feasible verdict that rests on 𝓜 is marked CONDITIONAL-P0 (galaxies' cold energy at rest relative to
  baryons while it settles). If it holds in frame A only, CONDITIONAL-FRAME. If it holds with D-lenient only,
  CONDITIONAL-D-LENIENT.

**Per-class labels:** FEASIBLE WITH NO NEW CONSTANT / FEASIBLE WITH ONE NEW CONSTANT (name it, give its admissible range) /
INFEASIBLE IN THE DECLARED CLASS (name the pair and variable that block) / UNDETERMINED (a source verdict is undetermined).

**Overall label** = the best class label over C0–C5 (with its qualifiers). If no class is feasible: INFEASIBLE IN THE DECLARED
CLASSES, with the obstruction named per pair (M–G, D–G). **Minimal variable set** = smallest set containing an M–G separator and
a D–G separator by R1.

## 6. Pre-declared G-test list (MW, P0, N = 300, both footings)

- GT0 controls: F ≡ 1 at α = 0.25, 0.5, 1.0 (K-G2).
- GT1: C2 steps for x ∈ {x_ρ, x_g, x_J, x_q} × {decreasing, increasing} × {M-core edge, D-conservative edge}, α_hi = 1.0.
- GT2: decreasing x_ρ step at the D-lenient edge (α_hi 1.0 and 0.5) and at the D-conservative edge with α_hi = 0.5.
- GT3: C3 density forms (rational n = 1, 2; exp) with ρ_* from R3 at the D-conservative and D-lenient edges, α_hi = 1.0.
- GT4: C2/C3 natural-threshold runs required by R2/R3.
- GT5 (report only, R5): gate × constant (α_hi 1.0) and gate × decreasing density step at the D-conservative edge.

## 7. K-tests (reproduce each constraint's quoted bound from its source lane's committed numbers)

- K-M1: `CFG623…/cfg623_results.json`: 0_can, 0_alt ALLOWED; 0.1, 0.3, ∞ EXCLUDED on both; Z_B(0.03) = 3.12 / 2.65 (±0.01).
- K-M2: `CFG639…/cfg639_merger_results.json`: allowed {0} / {0, 0.03}; Z_B, Z_H at 0.1 < 2 on both; Z_B(0.3, can) ≥ 2; gated-off
  fraction 0.714.
- K-M3: the merger reconstruction: `Progenitor599` gives the cached run's `Mph_tot` and `Mb` to ≤ 1e-6 (relative); the observed
  epoch's speed and d_SG equal cfg623_results (2699.4 km/s, 196.9 kpc) to ±0.1.
- K-G1: `CFG598…/cfg598_results.json` MW P0 min q: 0.25 → 0.9842 / 0.9849, 0.5 → 0.9928 / 0.9930 (±1e-4).
- K-G2: the G-test code with F ≡ 1 reproduces CFG598's MW P0 min q and M_c/M_ph(<30) at α = 0.25, 0.5, 1 to ≤ 1e-9 (relative).
- K-C: `CFG542…/cfg542_results.json` α_max = 1.0 (q = 1) and 1.1864 (q = 1 − f_b) (±1e-3).
- K-D1: `CFG882…/cfg882_results.json`: max α_c = 1.37e-3 (±0.01e-3); α_50 range 6.2e-4 to 1.02e-3.
- K-D2: `CFG889…/parts/part_G*.json`: α·t_50 over the 8 primary gated cells = 105–148 Myr (±1), so α_D,gated = 0.88–1.23e-2.
- K-D3: α_D,loc at CFG877's cap radius on H2 (uniform α) agrees with CFG882's H2 α_50 within a factor 1.5 on both footings.
- K-D4: the clump profile reaches M_cl at 237 / 205 pc (±2 pc), CFG877 README:48–49.
A failed K-test is reported as FAIL and not loosened; a verdict that depends on a failed K-test is marked so.

## 8. MUTATE (separate outputs `cfg913_MUTATE.out`, `cfg913_results_MUTATE.json`; exit 1 when the tooth bites)

Four runs, each perturbing ONE constraint's local conditions by an order of magnitude; the verdict logic and any G-tests the new
edges require are re-run:
- MUT-A: merger relative velocities ÷ 10 (𝓜_M × 0.1).
- MUT-B: merger relative velocities × 10 (𝓜_M × 10).
- MUT-C: clump densities × 10 (all D-operative ρ_c, ρ_m × 10; τ and α_D,loc follow).
- MUT-D: clump densities ÷ 10.
**Tooth:** bites iff the overall label or the minimal variable set changes in at least one of MUT-A..D. Class-table changes are
reported. If it does not bite, that is reported as frozen.

## 9. Pre-freeze hand values (disclosed; not verdict inputs)

From the source READMEs only (nothing computed): merger relative speed ~2700 km/s against a sub σ_J of several hundred km/s
(𝓜 ~ 3 in the gas frame; frame B unknown, possibly < 1 once the sub leaves the main's gas); merger densities ~1e-4 to 3e-3
M_⊙/pc³; MW densities 1e-4 (~70 kpc) to 2e-2 (~5 kpc); clump 6e-3 (450 pc) to 0.6 M_⊙/pc³; g/a0 ~0.1–0.3 for the clump, ~0.1–2
for the merger, ~0.01–5 for the MW. Expectation: density, g/a0 and y_J do not separate M from G; only 𝓜 might (P0); only density
might separate D from G, if the MW tolerates α = 0 in its densest inner cells.

## 10. Not claimed

No α_max or interpolation between merger nodes; no claim that any feasible law is physical or derived; no data comparison
beyond the source lanes' frozen verdicts; κ derived; "theory closed".
