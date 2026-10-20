# CFG889 FROZEN CRITERIA: is the deficit gate dynamically sound once orbits mix?

Date: 2026-10-20. Written and committed ALONE, before any CFG889 script exists in the lane and before any drift, OU or gate run.
Nothing below may be edited after this commit; later changes go in dated disclosures in the README.

κ = ½ is FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) are judged separately and never pooled. Law
g = g_N ν_e(g_N/a0), ν_e(y) = 1/(1 − e^(−√y)). Cold energy is real gravitating mass; no particle species. Framework-native inputs
only. Not "theory closed". Nothing here says the data favour the framework. No constant is added; no knob is scanned. α stays free
(two values, 0.5 and 1, as in CFG882).

## 0. Question and what has been seen

**Question.** With collisionless orbits included (Vlasov in the total potential) plus the record's drift and FIX-2 OU relaxation,
gated by CFG639 HG (both act only where d = ρ_ph − ρ_c > 0), does the system (a) keep a dwarf's CFG877 clump, (b) heal or amplify
CFG882's empty-shell knife edge, (c) stay well behaved (no runaway voids, mass conserved, bounded energy)? Compare the ungated
two-sided drift.

**Seen before freezing.** CFG638 (kinetic form, fluid moments), CFG639 (HG; Part A NOT DIAGNOSTIC, IC-C not steady; Part B VG-1
UNDETERMINED), CFG641, CFG544 (spherical shell toy, FIX-1/FIX-2, drift keeps (v_r, v_t), OU to the Jeans dispersion of the current
density, rate α/τ), CFG554, CFG877 (V_x 10.655 / 10.587 km/s, M_cl 5.25e6 / 4.24e6 M_⊙, r_c 104 pc, r_t 199 / 163 pc, coded cap
237 / 205 pc), CFG882 (V1 two-sided drain s_50 = 10.37 / 8.58 Myr for H2 at α = 1; V2 gated retention exact; D1 knife edge 39–45%
of cells r_t–2 kpc emptied with 1–10% noise vs 0–5% without the clump; M_ex(<1 kpc)/M_cl 0.91–0.94 after 12 Gyr; no orbits).

**Scratch prototype before freezing (disclosed).** The equilibrium builder (Eddington inversion) and the shell Vlasov integrator
(below) were written and run in a scratch directory, with **no drift, no OU and no gate**, to check feasibility only: the DF is
positive everywhere on the grid (min f > 0) for H2 with and without the clump, both footings; pure Vlasov over 1.5 Gyr at N ≈ 1e5 keeps
the coarse profile (30 pc–3 kpc) within ≤ 0.03 dex except the innermost bin (~2σ), R(<r_t) moves by ≤ +0.03, and the energy drifts by
−3.5e-3 (scaling as 1/N, i.e. discreteness, not step size); 25–60 s per 1.5-Gyr run. The K-V tolerances in §4 were set after seeing
these pure-Vlasov numbers. No gated, ungated or OU run was made before this commit.

**Pre-freeze hand values (disclosed, not verdict inputs).** H2 canonical, smooth-capped clump: at r_t, τ ≈ 16 Myr, v_s ≈ 6.8 α km/s,
t_cross = r/V_c ≈ 18 Myr; at 1 kpc τ ≈ 124 Myr, v_s ≈ 2.9 α km/s, 1/Γ ≈ 124 Myr/α; at 2 kpc v_s ≈ 1.4 α km/s, t_cross ≈ 230 Myr.
T = 1500 Myr ≈ 6.5 t_cross(2 kpc) ≈ 80 t_cross(r_t). **Hand expectation:** outside the clump M_ex(<r) ≈ M_cl > 0, so every
noise-underfilled bin is pushed outward and no bin is ever pushed inward (overfilled bins are frozen). Orbits re-randomise which bins
are underfilled every few Myr, so the one-way push should act on the whole zone at roughly half duty: a smooth deficit (not empty
cells) building toward compensation of the clump, at a rate ~Γ/2. The ungated run should drain the clump on CFG882's time scale to
O(1). These are expectations, not criteria.

## 1. Equations (the record's, unchanged)

Kinetic form (CFG638): ∂ₜf + ∇ₓ·[(v + v_s)f] − ∇Φ·∇ᵥf = γ χ ∇ᵥ·[(v − u)f + σ_J²∇ᵥf], spherical (χ = the gate below; CFG639 calls it G).
- ∇²Φ = 4πG(ρ_b + ρ_c): static Plummer baryons + the cold particles' own enclosed mass (Newtonian Poisson; cold energy is real mass).
- Drift v_s = −α χ τ ∇ψ = α χ τ G M_ex(<r)/r² r̂ (G = Newton's constant), M_ex(<r) = M_c(<r) − M_tgt(<r), τ = (4πGρ_m)^(−1/2),
  ρ_m = ρ_b + ρ_c (CFG544 FIX-1 two-sided ψ). The drift moves positions at fixed (v_r, v_t) (CFG544 convention = the kinetic form).
- OU (FIX-2): rate γ = α/τ, target σ_J² = P/ρ_c, P(r) = ∫_r^∞ ρ_c g dr' of the current binned cold density in the current total
  field (CFG544 `ou_step`): v_r → a v_r + bξ₁, v_t → |(a v_t + bξ₂, bξ₃)|, a = e^(−γΔt), b = √(σ_J²(1 − a²)).
- **Gate χ (CFG639 HG):** χ = 1[d > 0] per radial bin, d = m_tgt − m_c (target minus particle mass in the bin), multiplying both the
  drift and the OU. **Ungated:** χ ≡ 1. **MUTATE:** χ = 1[d < 0].
- 1_B 1_C = 1 for r < R2 (the settled catchment); beyond R2 no drift, no OU (pure Vlasov).
- **Target (ρ_tgt).** ρ_ph of the host's own baryons (round rule, ν_e), times a smooth catchment taper T(r) = 1 for r < R1 = 3 kpc,
  cos²[(π/2)(r − R1)/(R2 − R1)] to R2 = 5 kpc, 0 beyond; d uses ρ_tgt, so the settled state is exactly ρ_c = ρ_tgt (no artificial
  deficit in the taper). Disclosed model choice (CFG882 used a hard 20-kpc box).
- **Clump.** CFG877's cored shape with a **smooth cap**: M_x(<r) = M_cl u/(1 + u⁴)^(1/4), u = V_x² r³/(G(r² + r_c²) M_cl),
  r_c = 104 pc. Reason (disclosed): an isotropic equilibrium cannot carry CFG877's hard cap (a density jump makes the Eddington f
  negative). Same core, same total M_cl; r_50 = 150 / 133 pc, r_90 = 269 / 230 pc (canonical / alt).

## 2. Numerics (fixed now)

- **Units** pc, M_⊙, Myr. Hosts (illustrative Plummer, as CFG882): H2 (M_b 3e5, a 200 pc) primary; H1 (1e4, 30 pc) and H3 (2e7,
  700 pc) report-only.
- **Initial state** = an isotropic equilibrium of the total cold density ρ_tgt + ρ_x in the total potential (Eddington inversion,
  Φ(∞) = 0). Halo particles sampled from ρ_tgt (seed per run family), clump particles from ρ_x; velocities of both from the same total
  f, so the union samples f exactly; equal particle mass m_p. Paired no-clump runs use the identical halo radii and the same velocity
  uniforms with the no-clump f.
- **Particle number.** H2: m_p = (total cold mass, canonical, with clump)/1e5 (≈ 618 M_⊙), same m_p for alt; H1: N ≈ 1e5; H3:
  N ≈ 2e5 (m_p per host from its canonical clump run). Resolution check: m_p/4 (N ≈ 4e5).
- **Imposed noise ε** (as CFG882 D1): halo radii sampled from ρ_tgt(1 + εξ_k) per gate bin, ξ_k ~ N(0, 1) clipped at ±3, seed 889,
  renormalised to the same halo mass; velocities from the unperturbed f. ε ∈ {0.01, 0.1}. ε = 0.01 is below the per-bin shot noise
  (3–8% in the zone), so that level is "shot-noise dominated".
- **Gate bins.** Faces {0} ∪ geomspace(2 pc, 5 kpc, 160) (Δln r = 0.049). m_tgt per bin from the tapered target cumulative.
  M_ex at faces from the bin sums; per particle linearly interpolated within its bin. τ and σ_J² per bin.
- **Vlasov.** Kick-drift-kick in the enclosed-mass profile frozen at the start of each global step (tabulated on 24 000 log cells,
  0.01 pc–200 kpc), individual power-of-two substeps with Δt_i ≤ 0.05 min(√(r³/GM), r/v) (CFG544 scheme), reflection at 0.01 pc.
  Global Δt = 0.5 Myr.
- **Order per step:** Vlasov(Δt) → drift(Δt) → OU(Δt). The drift is sub-cycled (n_d = min(16, ⌈max |v_s|Δt/(0.4 Δr_bin)⌉),
  gate, M_ex, τ recomputed each sub-cycle); any remaining |Δr| > 0.5 Δr_bin is clipped and counted.
- **RNG:** OU normals are drawn for every particle in every step whatever the gate, so gated (with χ forced to 1) and ungated paths use
  identical streams.
- **Energy:** E = K + W, W exact for shells (−G m_p² Σ rank_i/r_i + Σ m_p Φ_b(r_i)); drift work from the tabulated potential
  before/after each sub-cycle; OU work = ΔK exactly; integration error ε_E = [E(t) − E(0) − W_drift − W_OU]/|E(0)|.
- T = 1500 Myr for every verdict run. R(t) recorded every step for the first 200 Myr, snapshots every 10 Myr.

## 3. Metrics

- **Retention** R(t) = M_ex(<r_t, t)/M_ex(<r_t, 0) (r_t = 199 / 163 pc, CFG882's radius; M_ex from particle counts minus the target
  cumulative). Also reported at r_90. t_50 = first time R ≤ 0.5.
- **Zone** = gate bins wholly inside (r_t, 2 kpc). Per snapshot: emptied fraction H_e (bins with zero particles; = CFG882's
  "< 1e-6 m_ph"), deep-hole fraction H_d (m_c < 0.5 m_tgt), zone ratio M_c,zone/M_tgt,zone, gate duty (fraction of zone bins with d > 0).
- **Compensation** C(r) = M_ex(<r)/M_cl at 0.5, 1, 2, 3 kpc.
- **Clump-induced** (clump run minus its paired no-clump run, same seed and ε): ΔH_e, ΔH_d (final values averaged over the snapshots
  in [T − 100, T] Myr; "mid" over [T/2 − 50, T/2 + 50]), and ΔM_zone = {[M_c,zone(T) − M_c,zone(0)]_clump − [same]_no-clump}/M_cl.
- **Energy** injected E_inj(t) = W_drift + W_OU; integration error ε_E; escape fraction f_esc = cold mass at r > R2 / total.

## 4. K-tests (each PASS/FAIL; any FAIL → class INCONCLUSIVE unless stated)

- **K-V** pure Vlasov (α = 0), H2, clump, ε = 0, both footings, 1500 Myr: coarse profile (10 log bins 50 pc–3 kpc) max
  |Δlog₁₀ ρ| ≤ 0.05 dex; |R(T) − R(0)| ≤ 0.05 (R relative to the sampled initial excess); |ΔE/E| ≤ 0.01; virial ratio
  2K/Σ m r g changes by ≤ 0.02.
- **K1** gated solver with χ forced to 1 = ungated solver, bit for bit (H2 canonical, clump, α = 1, 100 Myr): max |Δr| = 0 and
  max |Δv_r| = 0.
- **K1b** physical check that gated = ungated where d > 0 everywhere: no-clump halo with every other particle removed (ρ_c ≈ ½ρ_tgt),
  α = 1, 20 Myr; precondition: every occupied bin has d > 0 at every sub-cycle; then max |Δr| = 0. If the precondition fails, K1b is
  reported NOT APPLICABLE (not a FAIL).
- **K-OU** OU alone (drift off, χ ≡ 1, α = 1) on the no-clump equilibrium, H2 canonical, 500 Myr: the K-V profile tolerance holds
  and |ΔE/E| ≤ 0.01 (the Jeans target is neutral on an equilibrium).
- **K-M** mass: particle number conserved and all positions finite and > 0 in every run.
- **K-E** |ε_E| ≤ 0.01 in every verdict run (bookkeeping of drift and OU work closes).

## 5. Runs

- **Primary gated (verdict):** H2 × {canonical, alt} × α ∈ {0.5, 1} × ε ∈ {0.01, 0.1}, each with its paired no-clump run (16 runs).
- **Ungated comparison (V-U):** H2 × {canonical, alt} × α ∈ {0.5, 1}, ε = 0.01, clump and no-clump (8 runs).
- **Resolution (N ≈ 4e5):** H2 canonical, α = 1, ε = 0.01, gated, clump and no-clump.
- **Hosts (report-only):** H1 and H3, canonical, gated, α = 1, ε = 0.01, clump and no-clump.
- **D-noorbit (tooth T-H, and the CFG882 comparison):** particles with Vlasov and OU off (drift only, gated), H2 canonical,
  α = 1, ε ∈ {0.01, 0.1}, clump and no-clump.
- **D-mix (diagnostic):** no-clump H2 canonical equilibrium with every other zone bin emptied at t = 0 (particles removed), α = 0:
  how fast pure phase mixing refills a CFG882-like comb.
- **MUTATE** (env CFG889_MUTATE=1; separate outputs `cfg889_MUTATE.out`, `cfg889_results_MUTATE.json`): inverted gate in the primary
  gated runs at α = 1, ε = 0.01, both footings, clump and no-clump. The MUTATE summary exits 1 by design when M1 bites.
- Each run family is a separate process (`cfg889.py <part>`), one core, `OMP_NUM_THREADS=1 nice -n 10`, < 10 min, < 2 GB.

## 6. Verdicts

Per primary gated cell (footing × α × ε):
- **KEPT** iff R(T) ≥ 0.9 (mean over [T − 100, T]).
- **HEALED** iff ΔH_e ≤ 0.05 and ΔH_d ≤ 0.05 and ΔM_zone ≥ −0.10.
- **GROWING** iff at T, ΔH_d or −ΔM_zone exceeds its mid value by more than 0.05.
- **WELL BEHAVED** iff K-M holds, f_esc(T) ≤ 0.01, and energy is bounded: |E_inj(T)| ≤ 0.01|E(0)| or the |rate| of E_inj over
  the last third of the run is ≤ 0.5 × its |rate| over the first third.

**Teeth.**
- **T-H (hole metric):** in D-noorbit, ΔH_e ≥ 0.10 at both ε (orbits off must reproduce CFG882's knife-edge holes). If not, the hole
  part is NOT DIAGNOSTIC and the class is INCONCLUSIVE.
- **M1 (MUTATE):** inverted gate gives R(T) < 0.5 on both footings. If not, retention under the gate is NOT DIAGNOSTIC (class
  INCONCLUSIVE).

**Overall class (H2 primary cells only; hosts report-only):**
- **GATE SOUND** iff every primary cell is KEPT, HEALED and WELL BEHAVED, all K-tests pass, T-H and M1 bite, and the resolution run
  gives the same KEPT/HEALED status as its N ≈ 1e5 cell.
- **GATE UNSTABLE** iff K-tests pass, T-H and M1 bite, the resolution run agrees, and some primary cell is not HEALED or not WELL
  BEHAVED. Sub-labels, all stated: holes PERSIST (no cell GROWING) or GROW (some cell GROWING); energy BOUNDED or RUNAWAY; clump KEPT
  (all cells) or ERODED (cells listed).
- **CLUMP ERODED** is appended to either label if any primary cell is not KEPT.
- **INCONCLUSIVE** iff a K-test fails, T-H or M1 does not bite, or the resolution run changes the KEPT or HEALED status of its cell.

**Ungated comparison V-U (reported with a stated rule, no class weight):** DRAINS iff R(T) < 0.5 in every V-U clump run.
CFG882's O(1) claim (drift-only rate = the record's to O(1)) is **CONFIRMED** iff t_50(kinetic)/t_50(CFG882) ∈ [1/3, 3] in every
V-U clump run, with t_50(CFG882) = s_50/α (H2: 10.37 Myr canonical, 8.58 Myr alt); else **NOT CONFIRMED**.

## 7. Order and rules

This file is committed alone. Then `cfg889.py` and a runner, the parts in order (K, gated, ungated, resolution, hosts, D-runs),
MUTATE, the summary, README, one lane commit (own paths only). Footings never pooled. No downloads. No push. No edit of LEDGER.md,
THEORY_CANONICAL*.md or any other lane. Post-hoc changes go in dated README disclosures.
