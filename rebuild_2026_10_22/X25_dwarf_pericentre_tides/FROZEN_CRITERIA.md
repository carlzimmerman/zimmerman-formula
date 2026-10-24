# X25_dwarf_pericentre_tides — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** X20_hosted_dwarf_disequilibrium (frozen 87b6832e84, result bd736c128e) found the hosted-dwarf extra over the
isolated law (B_iso) is NOT tidal disequilibrium, with one disclosed qualifier: τ = g_tid/g_iso used the **current** host
distance, a lower bound on the stress at **pericentre**. Using orbit-based pericentres instead, does the extra correlate
with tidal stress, or vanish in the weakly stressed subset? This is the last data-side loophole for the dwarf requirement.

Standing rules: κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt a₀ = 1.1312e-10 m s⁻², never pooled. No
dark-matter particle. No knob scan: every threshold below is fixed here and never tuned. Not "theory closed". Nothing
here may say the data favour the framework. A fail is verified as hard as a win.

## 1. Data (read-only; nothing upstream recomputed)

- `rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv` (as X20): per footing `name`, `host`, `cls`, `logMstar`,
  `rh_pc`, `d_host_kpc`, `x_e_mid`, `Delta[Newton]`, `Delta[iso AQUAL L*0]` (= E, dex) and its `sdMC` (= s).
- **Pericentres:** `rebuild_2026_10_22/Z2_satellite_systematics/z2_per_system.csv`, per footing `r_peri_kpc`,
  `r_apo_kpc`, `r_peri_p16`, `r_peri_p84`. These are Z2's PM-based orbits (LVD Gaia PMs, distance, v_los; astropy
  Galactocentric frame) in S1's own MW field, the same field X1 used for x_e: μ = x/(1+x) law on a Hernquist baryon
  host, M_b = 6e10 M_sun, a_H = 3 kpc (E_mid). `r_apo_kpc ≥ 4999` is Z2's cap = unbound/first approach.
- Current Galactocentric distance for check K6 only: `distance_gc` from `real_research/data/dsph/lvd_dwarf_mw.csv`.
- **Set H** (X20's verdict set): `MW ultra-faint`, `bright M31`, `M31 others`, 61 systems per footing.
  **Set P = H ∩ {pericentre on disk}.** M31 satellites have no PM orbit on disk (Z2: "M31 satellites have no PMs on
  disk"); G2's M31 entries are assumed brackets (r_p = 0.3 d), not orbits, and are NOT used. No orbit is invented.
  Systems of H without a pericentre are listed as "no pericentre" and are not tested at pericentre.

## 2. Step 0 — stop rule

Re-implement X20's τ, T1 and T2 with its seed and RNG call order, and reproduce on both footings:
median τ (0.012147 / 0.012059), Spearman(E, log τ) (+0.002644 / +0.012322), permutation p (0.112694 / 0.103295),
T2 τ ≤ 0.1: N 54, median +0.480495 / +0.445101, sd 0.082765 / 0.082054, Z 5.8055 / 5.4245, EXTRA.
Tolerance: |Δ| ≤ 1e-6 on every number, N and label equal. **If Step 0 fails on either footing the lane STOPS**: no
pericentre number is computed, the README reports the failure, verdict "NOT RUN".

## 3. Pericentre stress (defined here, never fitted)

As X20: r₁₂ = (4/3) r_h, g_N = G(M★/2)/r₁₂² (Υ_V = 2), g_iso = g_N·10^(Delta[Newton] − Delta[iso]).
With g_e(r) = S1's host field at radius r (E_mid mass, the footing's a₀), r_p = Z2's central pericentre (this footing):

    τ_peri = 2 g_e(r_p) r₁₂ / r_p / g_iso          (X20's formula with d → r_p)

**Shock / heating proxy** (impulse approximation, Gnedin-Ostriker form, no fitted constant):

    V_p   = pericentre speed from E and L conservation between r_p and r_a in S1's potential Φ (Φ' = g_e);
    Δv    = (2 g_e(r_p) r₁₂ / r_p) · (r_p / V_p)       (tidal acceleration × passage time)
    σ_iso = sqrt(g_iso r₁₂ / 3)                         (the isolated law's own dispersion, never σ_obs)
    x     = (σ_iso / r₁₂) · (r_p / V_p)                 (adiabatic parameter)
    S₁    = (Δv / σ_iso)² · (1 + x²)^(−3/2)              (per passage)
    N_p   = max(1, 10 Gyr / T_r),  T_r = 2 ∫ dr / v_r from r_p to r_a;  N_p = 1 if r_a ≥ 4999 kpc (unbound)
    H     = S₁ · N_p                                     (cumulative heating proxy, PRIMARY shock proxy)

Reported only (no verdict weight): τ with factor 3; τ_grad = |dg_e/dr|(r_p) r₁₂ / g_iso (Z2's logT_peri form with
X1's g_iso); τ_max = max(τ_X20, τ_peri); S₁ alone; τ_peri at Z2's r_peri_p16 (closer orbits); and for every H system
without a pericentre, the r_p/d it would need to reach τ = 0.1.

## 4. Tests (per footing, on set P)

- **C1** Spearman ρ(E, log τ_peri) and Kendall τ_b. Bootstrap sd of ρ (10 000 resamples over systems, E_i drawn
  ~ N(E_i, s_i), seed 20261024). Null: same-host permutation — permute the orbit pairs (r_p, r_a) among systems of the
  same host (all of P is MW-hosted), keep each system's own r₁₂ and g_iso, recompute τ_peri; 20 000 permutations,
  seed 20261024; one-sided p = (#{ρ_perm ≥ ρ_obs} + 1)/(N + 1) (tides predict E rises with stress).
  Significance in σ: Z_p = Φ⁻¹(1 − p).
- **C2** the same for log H.
- **W, weak-stress subset**: τ_peri ≤ 0.1 (PRIMARY) and ≤ 0.03: median E, bootstrap sd (10 000, MC errors folded as
  X20), Z = median/sd, labels as X20/X19: EXTRA Z ≥ 2, NONE Z < 1, AMBIGUOUS between. Same per H-class in P.
- **PC, partial correlation**: does the M★ / r_half trend survive at fixed τ_peri? Rank-based partial Spearman:
  rank-transform E, log M★ (resp. log r_half) and log τ_peri, regress the ranks of each of the two on the rank of
  log τ_peri, correlate the residuals. Reported with raw ρ(E, log M★) and ρ(E, log r_half) on P. Bootstrap sd
  (10 000) and a two-sided permutation p (E permuted among P, 20 000). **SURVIVES** iff the partial ρ has the sign of
  the raw ρ and two-sided p < 0.05; **WEAKENED** iff same sign and p ≥ 0.05; **GONE** iff sign flips or |partial| < 0.1.
  Also reported: partial of E on log H at fixed log M★.
- **Fraction**: f_tid = 1 − Ẽ(τ_peri ≤ 0.1) / Ẽ(P), with a bootstrap 68 % interval (paired resampling).

## 5. Verdict (per footing; the class needs both footings to agree, else UNDECIDED)

- **UNDECIDED** — N(P) < 15, or N(τ_peri ≤ 0.1) < 8, or the footings disagree.
- **TIDES EXPLAIN IT** — W at τ_peri ≤ 0.1 labelled NONE (N ≥ 8), AND min(p_C1, p_C2) ≤ 6.75e-4 (≥ 3σ one-sided,
  Bonferroni for the two proxies), AND the τ_peri ≤ 0.03 subset is not EXTRA when its N ≥ 8.
- **TIDES RULED OUT AT PERICENTRE** — W at τ_peri ≤ 0.1 labelled EXTRA, AND p_C1 ≥ 0.05 AND p_C2 ≥ 0.05.
- **TIDES PARTIAL** — anything else; the fraction f_tid is stated with its interval.

**Scope (frozen):** the verdict covers set P only. H systems without a pericentre (expected: all M31 classes, which
have no PM orbits on disk) keep X20's current-distance result, a lower bound; the README must say so in the verdict line.

## 6. Checks (all must pass in the normal run)

- **K0** Step 0 reproduction (§2), both footings.
- **K1** S1's host field reproduces X1's `x_e_mid` = g_e(d_host)/a₀ for every P system: max relative error ≤ 1e-6.
- **K2** the V_p / T_r routine on a Newtonian point mass (M = 1e11 M_sun, r_p = 30, r_a = 150 kpc) returns vis-viva V_p
  and Kepler's period within 1e-3 relative.
- **K3** positive control: E_syn = 0.5 log τ_peri + N(0, s_i) on the real P: C1 permutation p < 0.01.
- **K4** negative control: E permuted among P (τ_peri kept), 200 shuffles × 2 000 permutations: fraction with
  p > 0.01 ≥ 0.90.
- **K5** peak RSS < 1 GB, one thread.
- **K6** orbit sanity: every P system's r_p ≤ 1.02 · distance_gc + 0.5 kpc and r_p ≤ r_a.

## 7. MUTATE twin (env `X25_MUTATE=1`)

Swaps Z2's r_peri and r_apo (the orbit read at apocentre). **K6 must FAIL** (named must-fail check); exit code 1.
Outputs are written to `_MUTATE` files. Its numbers carry no verdict weight.
