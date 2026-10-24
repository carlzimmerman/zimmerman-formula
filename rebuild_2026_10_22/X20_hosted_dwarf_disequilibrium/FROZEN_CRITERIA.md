# X20_hosted_dwarf_disequilibrium — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** X19 (8960ea2285) found no low-dimensional selector, and the classes that block one are almost always the hosted
dwarfs: MW ultra-faints, bright M31 dSphs, M31 others. Is their "extra" over the isolated law (B_iso) a measurement artefact,
namely (T) tidal disequilibrium or (B) binary-star inflation of σ, rather than missing mass?

Standing rules: κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt a₀ = 1.1312e-10 m s⁻², never pooled. No
dark-matter particle. No knob scan: the thresholds below are fixed here and never tuned. Not "theory closed". Nothing here
may say the data favour the framework. Verify a fail as hard as a win: a pass here removes a red tile's support, so it gets
the same controls as a fail.

## 1. Data (read-only; nothing recomputed upstream)

- Per system: `rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv` (X1, committed). Per footing: `cls`, `name`, `host`,
  `logMstar`, `rh_pc`, `sigma`, `d_host_kpc`, `x_e_mid` (host law field g_e/a₀ at d_host, E_mid host), `Delta[Newton]`,
  `Delta[iso AQUAL L*0]` and its `sdMC`.
- **E_i = `Delta[iso AQUAL L*0]`** (dex in g, B_iso, X19's primary baseline), s_i its sdMC. X1's primary already carries the
  Arroyo-Polonio free-f binary ratio (UFDs; median ratio for unmatched M_V > −7.7) and Υ_V = 2.
- Binary ratios: `campaign_fresh_gravity/CFG257_ufd_kinematics_scoping/arroyo_polonio2026_tableA1.csv`
  (`sig_f0`, `sig_free`, `sig_f07`).
- Verdict set H: the three X19 EXTRA hosted classes, `MW ultra-faint` (31), `bright M31` (25), `M31 others` (5): 61 systems
  per footing. MW classical (AMBIGUOUS in X19) and Crater II / Antlia II / CVn I / Sagittarius are reported, no verdict weight.

## 2. The tidal susceptibility τ (defined here, never fitted)

    r₁₂ = (4/3) rh,   g_N = G (M★/2) / r₁₂²  (M★ = 10^logMstar, Υ_V = 2 as X1),
    g_iso = g_N · 10^(Delta[Newton] − Delta[iso])        (the isolated law's internal acceleration at r₁₂, X1's own)
    g_tid = 2 g_e r₁₂ / d_host,   g_e = x_e_mid · a₀       (deep-MOND host, g_e ∝ 1/d: stretch + centrifugal, factor n+1 = 2)
    τ = g_tid / g_iso

- τ uses the **predicted** internal acceleration, never g_obs (g_obs defines E: BY-CONSTRUCTION RISK). τ and E still share
  g_iso; the permutation null (§3) and the control K3 handle that.
- Current d_host ≥ pericentre, so τ is a **lower bound** on the orbit's peak tidal stress (disclosed; no orbits on disk).
- Reported variants (no verdict weight): factor 3 (point-mass host); Newtonian tidal 2 G M_host r₁₂/d³ is not used.

## 3. Tests (per footing; set H unless stated)

- **T1, correlation.** Spearman ρ(E, log τ). Null: permute the (d_host, x_e_mid) pairs among systems **of the same host**
  (MW with MW, M31 with M31), recompute τ, 20 000 permutations, seed 20261024. p = fraction with ρ_perm ≥ ρ_obs (one-sided:
  disequilibrium predicts E rises with τ).
- **T2, the equilibrium subset.** Systems with τ ≤ τ* = 0.1 (frozen: tidal stress below a tenth of the internal pull).
  Statistic: median E, sd by bootstrap over systems (10 000, seed 20261024, MC errors folded by drawing E_i ~ N(E_i, s_i)).
  Z = median / sd. Label as X19: EXTRA Z ≥ 2, NONE Z < 1, AMBIGUOUS between. Reported: τ* = 0.03 and 0.3, and the same
  per class.
- **B, binary room.** Per class of H: the σ factor that erases the class median, q_req = 10^(−Ẽ/2). The record's remaining
  binary room beyond X1's primary is r = σ_f07/σ_free (Arroyo-Polonio rows): median and minimum. Labels:
  **BINARIES CAN ERASE** if q_req ≥ median r; **ONLY AT THE EXTREME** if min r ≤ q_req < median r; **CANNOT** if q_req < min r.
  Reported: the total binary range σ_f07/σ_f0 (median, min) as an upper bound that ignores X1's correction.
- **Reported only:** Spearman ρ(E, ellipticity) where LVD has it (a tidal-distortion proxy; joined by name from
  `real_research/data/dsph/lvd_dwarf_{mw,m31}.csv`); E vs log τ table per system; MW classical and the individual systems.

## 4. Verdict (primary, per footing; class needs both footings to agree)

- **DISEQUILIBRIUM SUPPORTED** — T1 p < 0.01 AND T2 label NONE with N(τ ≤ τ*) ≥ 8.
- **PARTIAL** — exactly one of: T1 p < 0.01; T2 NONE (N ≥ 8).
- **NOT SUPPORTED** — T1 p ≥ 0.05 AND T2 label EXTRA.
- **UNDECIDED** — N(τ ≤ τ*) < 8, footings disagree, or none of the above.

The binary leg B is reported as its own line per class, with no say in the tidal verdict.

**What a verdict means for X19 (reported, no new rank run):** DISEQUILIBRIUM SUPPORTED would make the hosted classes'
X19 labels unreliable, leaving clusters T2/T3 + background as the EXTRA set. It would NOT supply a selector, and the
Bullet / CMB / phase-space closures of the cluster door still stand.

## 5. Checks (all must pass; `--mutate` must fail K0)

- **K0** plain medians of E per H class equal X19's printed plain medians (canonical +0.596 / +0.220 / +0.777; alt
  +0.539 / +0.185 / +0.697) within 0.005.
- **K1** g_obs implied by the CSV, g_N·10^Delta[Newton], against 3(σ b)²/r₁₂ with b = X1's binary ratio for that system
  (free-f where matched, median otherwise for M_V > −7.7, 1 else): median |Δ| ≤ 0.05 dex (MC medians vs point values).
- **K2** positive control: synthetic E_i = 0.5 log τ_i + N(0, s_i) on the real τ: T1 p < 0.01 must hold.
- **K3** negative control: E_i permuted among systems of the same host (τ kept): T1 p is reported; K3 passes if the
  machinery returns p > 0.01 in at least 90 % of 200 shuffles (calibration).
- **K4** peak RSS < 1 GB, one thread.
- **MUTATE**: E taken from `Delta[AQUAL + EFE L*0 (exact MOND + EFE)]` instead of the iso column; K0 must fail.
