# WT-04 FROZEN CRITERIA: clocks where the framework's extra gravity acts

Written 2026-10-21 before any WT-04 script or number. Committed alone. Later changes go in appended, dated amendments only.

**Settings.** κ = ½ FITTED. Footings a0 = 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt), run separately and never
pooled. Z = 5.7888. Cold energy is real gravitating mass; no particle species is added. Framework-native predictions only:
no NFW/halo-model fits, no ΛCDM mass functions or concentrations, and no standard-MOND yardstick inside a verdict. Any external
ingredient is reported separately and labelled. Not "theory closed". Nothing here says the data favour the framework.

## 1. Question

How do clocks tick where the framework's extra gravity acts, and is there any clock-rate observable (gravitational time
dilation, gravitational redshift, time delays) that differs from general relativity (GR) with the same total mass
(baryons + cold energy)?

- (a) Clock potential vs lensing potential in the CFG938 parent, including its slip.
- (b) Time-dilation depth of an isolated disc (NGC 3198) and a dwarf (DDO 154), centre to infinity, with the framework's own
  cut-off. Compared with Newtonian baryons only. Both footings.
- (c) Stacked gravitational redshift of cluster members relative to the centre (BCG), from the record's cluster model, with the
  kinematic terms. Compared with published stacks (PROVISIONAL data).
- (d) Strong-lens time delays: Fermat potential at fixed image positions and fixed Σ.
- (e) One line: any clock-rate observable that differs from GR with the same total mass?

## 2. Inputs (read only; commit hashes)

| input | commit | use |
|---|---|---|
| `campaign_fresh_gravity/THEORY_CANONICAL_2026-10-21_DRAFT.md` | 9470c0433 | the law g_N = g²/(g + a0); supply row; cluster rows §3.7, §4.3 |
| CFG938 `DERIVATION.md`, `cfg938.py`, `cfg938_results.json` | 92606e049 | action; tether stress p_r = −W_full(u), p_t = p_r + D(u)u/K; slip formula; K1a target |
| CFG847 `cfg847_results.json` | 15c0894c1 | the record's slip systems (reported alongside) |
| CFG804 `cfg804.py` | 67774ce37 | census f_ret(M_ta), fixed point M_ta = M_b/(f_ret f_b), supply 5.364 N M_b, edge rule; K1b target |
| CFG687 `cfg687_stack.py`, `cfg687_percluster.npz`, `cfg687_results.json` | a84425a1d | cluster gas model (β = 2/3, r_c = 0.15 R500, cut 3 Mpc, stars f* = 0.20 × gas), ν_mono primary kernel, 318 eRASS1 M_gas500 / R500 |
| CFG949 `README.md`, `cfg949_results.json` | 012eaa526 | H-UT reading (untethered cold energy, truncated NFW); primary-corner medians c, r_s, M_ta; K1c target 4.57 |
| CFG922 `cfg922.py` | e10ff47a2 | BCG convention: Hernquist, R_e = 15 kpc (a = 15/1.8153 kpc) |
| CFG925 `README.md` | 45e1c487a | EFE form E1 (the record's coded form; record's current choice is no EFE) |
| `CFG4_common.py` | 3409d12da | footings, ν_mono (imported read-only) |
| SPARC `NGC3198_rotmod.dat`, `DDO154_rotmod.dat` | 999f94dfe | baryonic rotation curves |
| L2 `l2_cluster_gravz_discriminator.py` | 6837cef2b | literature GRS values carried in the record (W11, S15, R23); PROVISIONAL |

No file downloads. Literature numbers not in the record come only from WebFetch/WebSearch of abstract or HTML pages
(no PDF), are labelled PROVISIONAL, and are recorded with source and how read (no suggested value in any prompt).

## 3. Definitions

**Metric.** Static weak field, Newtonian gauge: ds² = −(1 + 2Φ/c²)c²dt² + (1 − 2Ψ/c²)dx². Clock rate dτ/dt = 1 + Φ/c².
Lensing potential Φ_L = (Φ + Ψ)/2. Slow baryons fall with a = −∇Φ. Baryons and photons couple minimally to g (CFG938's S_b).

**(a) Derivation (sympy).** From the static spherically symmetric Einstein equations for an anisotropic source
(ρ, p_r, p_t): mass function m′ = 4πr²ρ; α′ from G^r_r; transform to isotropic coordinates at linear order. Expected form (to be
derived, not assumed): Ψ′ = Gm/r², Φ′ = Ψ′ + 4πG r p_r/c². Framework: p_r = −W_full(u), u = G M_c(<r)/r² (inside the cold
medium u = g − g_N on the law; outside, the field of the enclosed cold mass).

**Comparators.** G0 = GR with the same T⁰⁰ (baryons + cold-energy rest mass + W energy) and a pressureless cold component.
G1 (report only) = the same T⁰⁰ with the cold component supported by isotropic dispersion from the spherical Jeans equation.
δΦ ≡ Φ_framework − Φ_G0 = −∫_r^∞ 4πG r′ p_r/c² dr′.

**(b) Depth.** D = [Φ(∞) − Φ(0)]/c² = (1/c²)∫_0^∞ g dr. Baryons: g_N = V_bar²/r, V_bar² = V_gas|V_gas| + Υ V_disk²
(+ Υ V_bul²), Υ = 0.61 (as CFG938); inside the first radius g_N ∝ r; beyond the last radius a point mass
M_b = V_bar²(R_last) R_last/G. Spherical, midplane approximation (declared).
- **Primary (framework):** the S2 law g_N = g²/(g + a0) out to the catchment edge R_e, where the law's enclosed phantom mass
  (g − g_N)r²/G equals the supply 5.364 N M_b, N = 1/f_ret from the CFG804 census fixed point; beyond R_e, g = G(M_b + M_c)/r².
- **Newton:** g_N only.
- **No edge:** the law to r_max = 1, 10, 100 Mpc (shows whether D is finite without the supply).
- **Report-only variants:** ν_mono kernel; edge at 3 Mpc (the KiDS √-boost bound, external to the supply rule); E1 EFE
  g = g_N ν((g_N + g_N,e)/a0) with g_N,e = 0.01 and 0.03 a0 (assumed values, labelled; the record's current choice is no EFE).
- **FINITE** iff R_e < ∞ and D changes by < 1e-6 (relative) when the outer integration limit moves from 10 R_e to 1000 R_e.

**(c) Cluster redshift.** Δ(R) = c⟨z_gal − z_BCG⟩, negative = blueshift.
- Δ_grav(R) = −⟨Φ(r) − Φ(0)⟩/c, a line-of-sight average weighted by the member tracer n(r).
- Kinematic terms (derived here from special relativity and the light-cone weighting, then checked by Monte Carlo):
  transverse Doppler Δ_TD = ⟨v²⟩/(2c) = (3/2)⟨σ²⟩/c (isotropic); light-cone Δ_LC = +⟨v_z²⟩/c (weight 1 + v_z/c, to be
  derived); flux-limit (surface-brightness/beaming) term Δ_SB = −δ_SB⟨σ²⟩/c, δ_SB = x(3 + α) with x the cumulative luminosity
  function slope at the flux limit and α the spectral index. δ_SB is survey-dependent and EXTERNAL: bracket {0, 2, 4},
  midpoint 2. σ²(r) from the isotropic spherical Jeans equation in each reading's own g(r).
- Total P = Δ_grav + Δ_TD + Δ_LC + Δ_SB. Aperture value = count-weighted mean of Δ(R) over R < R_ap, weight 2πR Σ_tr(R).
- **Cluster:** the eRASS1 median of the 318 CFG687 clusters (by M_gas500; R500 from the same cluster set's median), plus the
  16% and 84% M_gas500 clusters (each with its own median-matched R500 by rank).
- **Readings.**
  - **R-LAW (primary; canonical cluster rule):** CFG687 gas + stars verbatim; kernel ν_mono (CFG687 primary; S2 variant);
    cold energy fills the law out to the catchment edge (census f_ret at the cluster's M_ta, M_b = 1.2 M_gas(<3 Mpc));
    Newtonian total beyond. Both footings.
  - **R-HUT (record variant, post hoc and FRAGILE per CFG949):** the same baryons, Newtonian, plus cold mass
    (1 − f_b) M_ta m(min(r, r_b)/r_s)/m(c) with the CFG949 primary-corner medians (c, r_s, M_ta; r_b = c r_s). Footing
    independent. Median cluster only (its per-cluster native profile is not rebuilt here).
- **Variant grid (the band):** kernel {ν_mono, S2} × edge {on, off (law to 10 Mpc)} × tracer {ρ_tot of the reading, ρ_gas}
  × BCG {off, on: 1e12 M_⊙ Hernquist a = 15/1.8153 kpc, law applied to it in R-LAW} × δ_SB {0, 2, 4} × cluster {16, 50, 84%}
  × R_ap {3, 6 Mpc}. Primary = ν_mono, edge on, ρ_tot tracer, BCG off, δ_SB = 2, median cluster, R_ap = 6 Mpc. Tracer
  truncated where the reading's density ends (gas cut 3 Mpc; edge; r_b; 10 Mpc for edge-off).
- Profile reported at R = 0.6, 1.6, 3.3, 5.2 Mpc (the bin centres carried in the record's L2 script).

**(d) Fermat potential.** τ(θ) = (D_Δt/c)[(θ − β)²/2 − ψ(θ)], ψ the projected Φ_L. Fixed image positions and fixed Σ_lens
(∇²ψ = 2Σ_lens/Σ_cr) fix ψ in both theories. The framework-specific piece at fixed T⁰⁰ is δψ from δΦ/2. Evaluated for a
Hernquist lens galaxy (M_b = 2e11 M_⊙, a = 5/1.8153 kpc) with the S2 law and its edge: fractional change of the Fermat
potential difference between R = 2 and 8 kpc.

## 4. Verdict rules (frozen)

**Theory (e).** For each observable k ∈ {a: Φ_framework vs Φ_G0 at the centre and along each system, b: depth D of both
galaxies, c: Δ_grav of R-LAW (primary and every band member), d: Fermat potential difference}, compute
F_k = max |X_framework − X_G0| / |X_G0| over systems and radii.
- **SAME AS GR WITH SAME MASS** iff max_k F_k < 1e-3 on both footings.
- **DISTINCT SIGNATURE** otherwise; name the observable, give its size on both footings.
- Identity flags (no verdict weight): clock rate = the potential that moves slow baryons (minimal coupling, both theories);
  Fermat potential at fixed lensing Σ is identical by construction. The only non-identity is the stress term δΦ.
- G1 (dispersion-supported comparator) is reported, not graded.

**Data (c), per footing and per reading (R-LAW primary; R-HUT graded the same way, labelled).** For each measurement j
(value m_j, error σ_j; for asymmetric errors the side toward the prediction):
- z_mid = (P_primary − m_j)/σ_j; z_near = distance from m_j to the nearest edge of the band [P_lo, P_hi], in σ_j (0 if inside).
- **CONSISTENT:** |z_mid| < 2 for every j.
- **TENSION:** z_near ≥ 3 for at least one j (no declared variant comes within 3σ).
- **NOT DIAGNOSTIC:** neither.
- Every data class carries **PROVISIONAL** (values from literature, carried in the record or looked up).
- Framework-internal result (no data): ratio Δ_grav(R-LAW)/Δ_grav(R-HUT) at the primary settings.

**(b) answer:** FINITE / NOT FINITE per the rule in §3, the size of D(law)/D(Newton), and what sets D (the supply edge,
reported as ∂D/∂ln R_e).

## 5. Controls (all must pass; a failed control withholds the classes until a dated amendment fixes it)

- **K1a:** CFG938 S4 cluster row: s_grad(W) = 5.0780e-6 (canonical) and 5.7916e-6 (alt) from `cfg938_results.json`, to 1e-6
  relative, with CFG938's constants and system (1.5e14 M_⊙ point mass, 1 Mpc).
- **K1b:** CFG804 K1: log M_b 10.5 → N = 10.000 (±1e-6), log M_ta 12.30 (±0.01); edge for N = 10 is 54.1 r_M (CFG804 bin 1
  "54 r_M").
- **K1c:** CFG949 A1/PH1: median M_gas(<3 Mpc)/M_gas500 over the 318 eRASS1 clusters = 4.57 (±0.01).
- **K2a:** Newtonian point mass: the Sun's surface redshift GM_⊙/(R_⊙c) = 0.636 km/s from the depth integrator (outside R_⊙),
  to 1e-4 relative.
- **K2b:** Plummer sphere: numerical Φ(0) = −GM/b to 1e-4.
- **K2c:** sympy: p = 0 exterior gives Φ = Ψ = −GM/r at linear order.
- **K3:** NFW analytic potential vs the numerical integral to 1e-4.
- **K4:** Monte Carlo (2e5 isotropic Gaussian velocities, σ = 1000 km/s): light-cone mean shift = σ²/c within 3 MC errors;
  transverse Doppler = (3/2)σ²/c to 1%.

## 6. MUTATE (`WT04_MUTATE=1`; all three teeth must bite)

- **T1 slip injection:** add an anisotropic term making Φ − Ψ = 0.1 Φ_L (s = 0.1). The theory class must flip to DISTINCT
  SIGNATURE.
- **T2 a0 → 0:** D(law) must equal D(Newton) to 1e-6, and R-LAW Δ_grav must equal the baryons-only value to 1e-6.
- **T3 N → ∞ (no supply edge):** the FINITE test of §3 must fail.

## 7. Compute rules

One process, `OMP_NUM_THREADS=1 nice -n 10`, peak RSS < 1 GB (`/usr/bin/time -l`), minutes; sympy/numpy/scipy. No other lane's
file is edited, run or staged. Outputs: `wt04.py`, `wt04.out`, `wt04_results.json` (+ `_MUTATE`), `README.md`, left uncommitted
for the orchestrator.

## 8. Blindness disclosure

Not blind. Read before freezing: the canonical v4 draft; CFG938 (slip ≤ 1.5e-5, its S4 table); CFG847; CFG804 (edge 320–450 kpc,
54 r_M); CFG687 (A_INNER 2.51 / 2.31, A_MID 1.91 / 1.75, A_OUTER 1.01 / 0.93); CFG949 (H-UT EXPLAINS at the primary corner,
FRAGILE; medians c 23.2, r_s 233 kpc, M_ta 4.53e14); CFG925 (EFE choice); the record's L2 lane (July 2026: GR+DM −8.1 to −12.4
km/s; MOND-from-baryons ~2× short; W11 −7.7 ± 3.0, S15 −11 +7/−5, R23 −11.4 ± 3.3 km/s carried as literature values).
Hand estimates made before freezing: D ≈ (v_f²/c²)[ln(R_e/r_in) + 1] ~ 1e-6 for NGC 3198; slip-level clock differences
~1e-5 of the signal or less; R-LAW cluster |Δ_grav| below the lensing-matched value because of the core deficit.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
