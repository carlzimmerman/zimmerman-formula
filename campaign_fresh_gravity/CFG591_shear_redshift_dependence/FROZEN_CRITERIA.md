# CFG591 FROZEN CRITERIA: does CFG590's cosmic-shear exclusion survive a redshift-dependent framework/ΛCDM ratio R(k, z)?

Date frozen: 2026-10-10. Committed alone, before any number of this lane is computed.

Settings: κ = ½ FITTED; footings canonical a0 = 9.3603e-11 and alt a0 = 1.1312e-10 m/s², never pooled; flat a0 = κ c √(G ρ_DE), so for w = −1 a0 is the SAME at every z (the framework's own prediction, declared; no a0(z) ∝ H(z) variant is run); kernel ν_mono; candidate B; G9. The cold energy's MASS is still required; no particle species. Not "theory closed"; nothing here says the data favour the framework. Nothing is downloaded. Other lanes are read only (imported or exec'd, never edited).

## 0. The question

CFG590 found the framework PRIMARY (CFG559 kinetic profile with the CFG557 α-free finite-age supply ceiling) EXCLUDED by cosmic shear at equal HMcode-2020/BAHAMAS feedback (min Zmax 5.27 canonical, 8.24 alt), with ΛCDM-DMO + feedback CONSISTENT. Its main caveat: R(k) was computed at z = 0 only and held fixed in z. Its own scaled family R_s = 1 + s (R − 1) changes class below s = 0.64 (canonical) / 0.43 (alt); a crude post-hoc estimate gave s_eff ≈ 0.78. This lane replaces the fixed R with R(k, z) from the same halo-model machinery run at each epoch, and re-applies CFG590's frozen rule unchanged.

## 1. R(k, z): the halo model at each epoch (unchanged code paths, epoch inputs recomputed)

Epochs z = 0, 0.25, 0.5, 0.75, 1.0; both footings. The CFG556 halo-model source is exec'd read-only up to its run block; the CFG557 `frame_profile_sc` and CFG559 `frame_profile_kin` function sources are exec'd verbatim (extracted from `cfg559_tests.py`) in the same namespace. The only overrides are the epoch inputs below; all lengths stay comoving [Mpc/h], k comoving [h/Mpc], ρ̄_m comoving (z-independent).

- **Linear spectrum:** CFG556's Eisenstein–Hu no-wiggle P_lin(k, 0) × D(z)², D from `cfg557_lib.Dgrow` (flat ΛCDM, no radiation), normalised to D(0) = 1.
- **σ(M, z), mass function, bias:** σ(M, z) = σ(M, 0) D(z). Tinker et al. 2008 Δ = 200m with its redshift evolution A(z) = 0.186 (1+z)^−0.14, a(z) = 1.47 (1+z)^−0.06, b(z) = 2.57 (1+z)^−α, log10 α = −[0.75 / log10(200/75)]^1.2, c = 1.19 (recalled, PROVISIONAL). Tinker et al. 2010 bias in ν = δ_c/σ(M, z) (unchanged form, δ_c = 1.686). A_miss and the turnaround 2-halo normalisation ∫ n b M_ta/ρ̄_m recomputed at each z.
- **Concentration:** Duffy et al. 2008 full sample, Δ = 200m: c200m = 10.14 (M / 2e12)^−0.081 (1 + z)^−1.01 (recalled, PROVISIONAL).
- **Turnaround radius:** mean enclosed density of the extended NFW = Δ_ta(z) ρ̄_m(z). Δ_ta(z) = 11.81 × Δ_ODE(z)/Δ_ODE(0), Δ_ODE(z) = `cfg557_lib.Epoch(z).Delta_ta` (the shell that turns around exactly at t_obs(z) in the flat-ΛCDM spherical-collapse ODE; anchored to CFG556's 11.81 so the z = 0 node is CFG556's exactly).
- **r200c / M200c** (stellar-mass input and baryon shapes): mean density 200 ρ_crit(z), i.e. 200/Ω_m(z) in units of ρ̄_m(z).
- **Stars:** Moster et al. 2013 with its z evolution: log10 M1 = 11.590 + 1.195 z/(1+z), N = 0.0351 − 0.0247 z/(1+z), β = 1.376 − 0.826 z/(1+z), γ = 0.608 + 0.329 z/(1+z) (recalled, PROVISIONAL). Hernquist / β-model shapes as CFG556 (fractions of r200c).
- **Census retention:** CFG416 `fret_of(log10 M_ta)` unchanged at every z (as CFG557's KiDS lens epochs; declared).
- **The law at epoch z:** y = G M_b(<r) / (r_phys² a0) with r_phys = r/(1+z) and a0 flat. Implemented by setting the namespace's comoving-units a0 to a0/(1+z)² (so r_M, r_e and y are the physical ones expressed comovingly). Nothing else in the profile code changes.
- **Finite-age supply s_c*(M_ta, z):** CFG557's α-free free-fall ceiling recomputed at each epoch with `cfg557_lib.s_catch(Epoch(z), M_ta, M_b, footing, α = ∞)` on that epoch's halo grid (t_obs = age at z; δ_L(M) from the EPS main-progenitor ODE at z, q = 2.2). At z = 0 the stored CFG557 grid (`cfg557_derive_results.json`, "ff") is used; the recomputed z = 0 grid is reported as a check.
- **Kinetic redistribution Δm(x; M_ta, z):** CFG559's toy (`cfg559_toy.run_cell`, imported unchanged: CFG544 toy, FIX-2, IC-B, α = 1, N = 30000, seed 544, code step 5e-4, T = 10 Gyr bench end state, last-1-Gyr average) rerun at each z > 0 for the PRIMARY supply, nodes log M_ta 11.0–15.0 step 0.5, both footings (72 cells), because the cell's dimensionless numbers (r_M/r_*, M_set/M_b, r_ta/r_*, T/t_u) change with s_c*(z) and the physical r_ta(z) = r_ta,comoving/(1+z). Cell construction = `cfg559_toy.make_cell` with exactly those epoch inputs. At z = 0 the CFG559 toy tables are reused (identical setup). T = 10 Gyr is kept at every z (the bench's steady end state; the finite age enters through s_c*, as in CFG559); this is a declared assumption, and each cell's CFG544 gate (steadiness) is reported. A cell failing the gate is flagged, its Δm still used.
- **The full-supply kinetic variant (CFG559 VARIANT_full_kin) is NOT rerun at z > 0** (it would need 72 more toy cells); it is carried at its z = 0 R as in CFG590 and is reported only, not used for the VARIANT-SENSITIVE flag.

**Models built at each z (R on CFG556's 260-point k grid, 1e-3–10 h/Mpc):**
- **PRIMARY:** CFG559 `PRIMARY_kin` path (s_c*(z), kinetic Δm(z)); R = 1 + (P_F,ta − P_L,ta)/P_L,std at z.
- **Mainline variants (for the VARIANT-SENSITIVE flag):** CFG557 `TESTED` path (s_c*(z), sharp); CFG556 `census|cen` (sharp, full supply); CFG556 `census|emg` (emergent edge).
- **Survivors reported with their own class at each z and as R(k, z):** CFG556 `census|emg` and CFG556 `census|cen|r200scope` (R = P_F,200/P_L,std).

## 2. Projection: CFG590 unchanged except R(k) → R(k, z)

`cfg590_shear.py` is exec'd read-only up to its main block (CAMB 1.6.6, HMcode-2020 DMO base, HMcode-2020 BAHAMAS feedback S_fb(k, z; T), T grid, M1 Limber C_ℓ for the KiDS-like / DES-like n(z) and noise, A_eff fit, M2, mapping systematics, classify, judge, full_report, crossings, S8-equivalent). ONE function is replaced: `R_of`. For a 2-D R table (z nodes × k) it interpolates linearly in z between nodes (written r0 + w (r1 − r0)), evaluated at each lens-plane z of the Limber grid, then applies CFG590's own k rule (R(k < 1e-3) = 1, R(k > 10) = R(10), log-k interpolation). For a 1-D R it calls CFG590's original `R_of`. M2 (z = 0.5) uses R(k, 0.5).

- **z > 1 (beyond the last node), PRIMARY rule:** R(k, z > 1) = R(k, 1.0) (held). **Reported bracket:** R ≡ 1 for z > 1. If the class differs between the two, the verdict carries the flag HIGH-Z-TAIL-SENSITIVE (no class change by itself).
- Data (recalled, PROVISIONAL, as CFG590): KiDS-1000 A_mod 0.858 ± 0.052; DES Y3 0.82 ± 0.04.

## 3. Verdict per footing (CFG590's frozen rule, unchanged)

Mapping M1, full feedback range T ∈ [7.3, 8.3]; Zmax(T) = max_d |Z_d(T)|:
- **EXCLUDED:** Zmax(T) ≥ 3 for every T in [7.3, 8.3].
- **TENSION:** not EXCLUDED, and Zmax(T) ≥ 2 for every T.
- **CONSISTENT:** Zmax(T) < 2 for some T (state whether such a T lies inside the fiducial [7.6, 8.0]).
- **NOT DIAGNOSTIC:** the class changes under M2, ℓ_max 1000 or 3000, or n(z) mean ± 0.1.
- **VARIANT-SENSITIVE** (flag): a mainline variant of §1 (with its own R(k, z)) gives a different M1 class.
- Also reported (as CFG590): feedback off class; per dataset the T with Z = 0 and the |Z| < 2 range over [7.0, 9.0]; ΔA vs ΛCDM at the same T; S8-equivalent for the PRIMARY.
- **Effective redshift scaling (reported):** s(z) = (R(k = 1, z) − 1)/(R(k = 1, 0) − 1) per footing and node, and the A_eff-equivalent s_A = (A_F,z − A_ΛCDM)/(A_F,fixed − A_ΛCDM) at T = 7.8 and off, compared with CFG590's thresholds 0.64 / 0.43 and its post-hoc 0.78.
- **Survivors' status:** the M1 class (and final class with systematics) of `census|emg` and `r200scope` with R(k, z), plus per-z R(k = 1).

## 4. Controls (a failed control labels the lane NO LABEL)

- **HZ0:** the z-generalised halo model at z = 0 reproduces CFG559 `PRIMARY_kin` R, CFG557 `TESTED` R and CFG556 `census|cen`, `census|emg`, `census|cen|r200scope` R to max |ΔR| ≤ 1e-10 (both footings).
- **HZ1:** σ8 of P_lin(z) = 0.811 D(z) to 1e-3 relative; I(k = 1e-3) = 1 to 1e-3 for L-std, L-ta and the framework cases at every z; mass conservation |M_F(< r_ta) − M_ta|/M_ta ≤ 1e-6 for the PRIMARY at every z (every 4th halo).
- **HZ2 (reported):** Δ_ODE(z) per node; the z = 0 recomputed s_c* grid vs the stored one (max |Δ|); s_c* at log M_ta 12/13/14/15 per z; toy C6 (m_sharp(1) = 1 to 1e-9) and C7 (mass exact) in every new cell.
- CFG590's controls C1–C4 are re-executed by the exec'd code and re-reported.

## 5. MUTATE (`CFG591_MUTATE=1`; separate `_MUTATE` outputs; exit 1 = all teeth bite)

- **MZ1:** R(k, z) set to the z = 0 values at every node (PRIMARY and every variant) must reproduce CFG590's stored A_eff table (M1 KiDS, M1 DES, M2; feedback off and every T in [7.3, 8.3]) to ≤ 1e-12 absolute ("exactly"; the tolerance is declared so floating-point round-off cannot be confused with a change) and CFG590's M1 and final classes.
- **MZ2:** R ≡ 1 (as a 2-D table) must reproduce ΛCDM's A_eff exactly (|ΔA| ≤ 1e-12) and its class.

## 6. Outputs

`cfg591_lib.py` (epoch namespace + s_c*(z)); `cfg591_toy.py` → `cfg591_toy.out`, `cfg591_toy_results.json`; `cfg591_halo.py` → `cfg591_halo.out`, `cfg591_halo_results.json`; `cfg591_shear.py` → `cfg591_shear.out`, `cfg591_results.json`, and with `CFG591_MUTATE=1` → `cfg591_shear_MUTATE.out`, `cfg591_results_MUTATE.json`; `README.md`. Compute: `nice -n 10`, ≤ 4 threads/processes. All numbers quoted come from the JSON.

## 7. Pre-freeze disclosure (dated 2026-10-10)

Read before freezing: CFG590 criteria, script, README, post-hoc; CFG556 criteria, README, script; CFG557 criteria, README, lib, derive, tests (halo-model part); CFG559 criteria, README, lib, toy, tests (halo-model part); CFG544 cell/IC code. No number of this lane was computed. Expectation (hand, not a threshold): CFG590's post-hoc cluster-share scaling (s_eff ≈ 0.78) suggests the canonical class is near its 0.64 boundary; lower concentrations and a younger universe (smaller s_c*) at z > 0 could push the excess either way (a smaller supply pulls the edge in, CFG557), so the sign of the change in R − 1 is not assumed.
