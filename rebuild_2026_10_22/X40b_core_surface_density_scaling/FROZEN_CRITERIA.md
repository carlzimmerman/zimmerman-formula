# X40b_core_surface_density_scaling — FROZEN CRITERIA (committed alone, before any script or number of this lane)

Lane id: X40b (X40 is taken by the peer lane `X40_fixed_core_radius`, b37983a0f7; this lane is independent of it).

**Question.** X38 (9cc80516df / f72216ad98) gave route-E cold dark energy halos, Burkert-cored at ρ₀r₀ = Σ_a₀ ≡ a₀/(2πG)
(107 / 129 M☉ pc⁻²). They pass SPARC and the cluster OUTER band and under-predict the heaviest cluster cores (MID T3 Z +4.3 /
+3.8, MID KT slope +3.1 / +3.0, MGAS T3 OUTER +5.4 / +4.9). X39 (b75acfc767 / 54684fb62f) showed baryonic contraction
cannot supply the mass without rebuilding galaxy cusps. **Can a framework-native rule with no new constant raise the core
surface density at cluster masses by the needed ~2× while leaving galaxies at a₀/(2πG)?**

Standing rules: κ = ½ FITTED. Footings (canonical a₀ 9.3603e-11, alt 1.1312e-10 m s⁻²) never pooled. Route E: gravity
Newtonian on baryons + cold dark energy, the law emergent. Cold dark energy is a gravitating field component, not matter
and not a particle. No new fitted constant. Not "theory closed". Nothing here may say the data favour the framework.

## 0. Step 0 (stop rule)

X38's committed script is copied to a scratch directory (only its output directory redirected; inputs read from the record)
and rerun. Its graded numbers must equal the committed `x38_sd_halos_results.json` (SPARC rms and median Υ per footing and
background; every cluster key's pred in both h cells) to 1e-6. **If not, the lane stops** and reports the mismatch.

## 1. The halo (common to every rule)

Burkert, ρ = ρ₀r₀³/[(r + r₀)(r² + r₀²)], surface density Σ ≡ ρ₀r₀ = s · Σ_a₀ with s ≥ 0 set by the rule. Mass
normalisation, branch and saturation exactly as X38 + A1: M_h(<R) = π Σ r₀² B(R/r₀) = M_target, compact root, SATURATED
counted. Galaxies: M200 from EM1's committed relation (A 11.18 / 0.90, B 11.20 / 0.90), R = R200 at 200 ρ_c(0). Clusters:
X30's machinery read-only, M_h(<r_ta) = 5.364 M_b, mass constant beyond r_ta. Gravity Newtonian on M_b + M_h.

## 2. The rules (each fully specified; no fitted constant)

- **(A) Acceleration-set core (primary).** Σ = max(a₀, g_b(r₀))/(2πG), i.e. s = max(1, g_b(r₀)/a₀), with r₀ = r₀(Σ) the
  compact root of §1. g_b(r) = G M_b(<r)/r² from the baryons only.
  - **Self-consistency:** s* = the smallest s ≥ 1 with max(1, g_b(r₀(s))/a₀) ≤ s, i.e. the first fixed point reached from
    X38's floor. Found by a scan of s on a log grid 1 → 10³ (400 points), then brentq inside the first bracket to 1e-10. If
    no crossing to 10³: s = 10³ and the halo is flagged RUNAWAY (count reported). If g_b(r₀(1)) ≤ a₀, s* = 1 (X38 exactly).
- **(A′) Total-acceleration core.** As (A) with g_b replaced by g_N,tot(r₀) = G[M_b(<r₀) + M_h(<r₀)]/r₀², the halo's own
  mass included, with the same a₀ floor: s = max(1, g_N,tot(r₀(s))/a₀). Same fixed-point rule.
- **(B) a₀ at formation epoch.** s = a₀(z_f)/a₀(0), with a₀(z)/a₀(0) the record's DESI curve "M-DEC" (CFG223
  `cfg223_results.json`, as drawn by `chart_a0z_one.py`), interpolated linearly in z. Formation epochs (PROVISIONAL, round
  declared values): SPARC galaxies z_f = 1.5, groups z_f = 1.0, clusters z_f = 0.5. Footing-independent ratio.
  - **Reported bound (epoch-free):** the largest cluster/galaxy ratio the curve can give at any z_f ∈ [0, 3]:
    max(M-DEC)/min(M-DEC) on [0, 3]; and the **sign check**: d(a₀(z)/a₀(0))/dz on z ∈ [0, 1] — does later cluster formation
    raise or lower Σ relative to galaxies formed earlier?
- **(C) Reported only, NOT graded as framework-native.** Empirical S ∝ M^α with galaxies pinned: s = 1 for M_target ≤ M_piv,
  s = (M_target/M_piv)^α above, with M_piv = the largest SPARC M200 from EM1's relation on background A (so SPARC equals X38
  exactly). Clusters use M_target = M_fair; groups their M200. α on the grid 0, 0.05, …, 1.00. Reported: α_best
  (minimum Σ Z² over the 15 cluster keys, h 0.672, per footing) and the α interval where every cluster key passes in both h
  cells. Empirical context (PROVISIONAL, not transcribed in the record): Donato+2009 galaxy cores ~140 M☉ pc⁻²; Boyarsky+2009
  S ∝ M^~0.2.

## 3. Baryons g_b

- **SPARC:** X39's spherical construction, copied: M_b(<R_k) = max(0, g_bar R_k²/G) at the measured radii at each Υ of the
  grid, made monotone; ∝ r² inside the first radius; beyond R_last a log-linear rise to M_b,tot(Υ) = (Υ L₃.₆ + 1.33 M_HI)
  × 10⁹ M☉ (or M_b(<R_last) if larger) at 3 R_last, constant after. g_b(r) = G M_b(<r)/r². The halo is solved per Υ, and
  EM1's fit_one picks Υ as before. Disclosed: spherical approximation of the disc.
- **Clusters:** X30's M_b (β-model gas × 1.2) + CFG922 BCG Hernquist (a = 10 kpc), matched and filled exactly as X39.
  Disclosed: X30's ×1.2 may already include part of the BCG (double count favours rules A, A′). Variant with no BCG reported.
- **Groups:** Hernquist with the catalogue M_bar and a = R_e/1.8153 (P4 T3).

## 4. Graded constraints (each rule, each footing)

- **SPARC (verdict-bearing):** EM1's line, rms ≤ 0.110 AND median Υ ∈ [0.50, 0.80], on both backgrounds A and B.
- **Clusters (verdict-bearing):** X38's 15 keys with X38's grading code: G-MID-T1..T3, G-MID-b, G-OUT-all, G-OUT-T1..T3,
  G-OUT-b, G-IN-all (KT 106), G-OUT-Mall, G-OUT-M1..M3, G-IN-Mall (all 326); |Z| ≤ 2 in both h cells (0.672, 0.686).
- **Groups (graded line, reported beside the class):** Tian+2026 BFJR, the 63 "Galaxy group" rows, P4 T3's statistic and
  line (CFG540): Δᵢ = log σ_obs − log σ_pred, σ² = ⟨r·g⟩/3 whole-system (isotropic, Hernquist tracer) in the Newtonian
  field of baryons + halo; halo M200 from EM1's relation on background A, extrapolated (disclosed), truncated at R200; class
  mean, SE, σ_sys = s̄ × 0.10 dex; PASS iff CONSISTENT (|Z| < 2 and σ_tot ≤ 0.045). Reported variant: fair-share M200 =
  5.364 M_bar. X38's own groups grade (s ≡ 1) is computed as the baseline.

## 5. Verdict classes (a class needs both footings to agree, else UNDECIDED)

- **RULE A CLOSES THE CLUSTER CORES (and keeps SPARC)** — rule A passes the SPARC line on both backgrounds AND every cluster
  key in both h cells.
- **RULE A′ CLOSES THE CLUSTER CORES (and keeps SPARC)** — rule A fails, rule A′ passes as above.
- **RULE B CLOSES THE CLUSTER CORES (and keeps SPARC)** — A and A′ fail, B passes as above (not expected).
- **NO FRAMEWORK-NATIVE RULE CLOSES IT** — none of A, A′, B passes. Each rule's failing keys and legs are listed, with
  the direction (UNDER / OVER).
- **UNDECIDED** — the footings disagree on the class.
- The groups line is reported beside the class for every rule (PASS / FAIL and Z), never folded into it.

Reported: per rule, s* medians (SPARC at the chosen Υ; clusters by KT tercile; groups), RUNAWAY and SATURATED counts,
cluster r₀ by KT tercile, and the **effective scaling** α_eff = OLS slope of log s* on log M_target over SPARC + clusters
(all 326, h 0.672), compared with (C)'s needed α. Also the no-BCG variant for A and A′.

## 6. Checks (all must pass)

- **K0:** with s ≡ 1 this lane's code reproduces X38's committed graded numbers (SPARC rms / median Υ, every cluster pred,
  h 0.672 and 0.686) to 1e-6; and Step 0 passed.
- **K1:** the fast compact-root inversion used here returns X38's `solve_r0` r₀ to 1e-8 on 200 random (M, R, Σ) cases,
  saturated cases included; the solved r₀ returns M_target to 1e-8.
- **K2 (floor):** a test halo with g_b ≡ 0 returns s* = 1 and X38's r₀ exactly under rules A and A′; every graded halo has
  s* ≥ 1 under A and A′.
- **K3 (fixed point):** every halo with 1 < s* < 10³ satisfies |max(1, g(r₀(s*))/a₀) − s*| < 1e-8 s*.
- **K4:** the groups integrator with no halo equals P4's `group_logsig` with ν ≡ 1 (Newtonian) to 1e-4 dex; the 63 group
  rows are read.
- **K5:** peak RSS < 1 GB, one thread, PYTHONHASHSEED=0, `nice -n 15`.

## 7. MUTATE

`X40B_MUTATE=1`: max() → min() in rules A and A′ (s = min(1, g/a₀): the a₀ floor becomes a ceiling, Σ drops below a₀/(2πG)
where the baryons are weak); the fixed point is then the largest s ≤ 1 with min(1, g(r₀(s))/a₀) ≥ s, scanned on a log grid
10⁻³ → 1 (s = 10⁻³ if none). Outputs go to `_MUTATE` files. **K2 must FAIL** (exit 1). The MUTATE graded numbers are
reported, never used.
