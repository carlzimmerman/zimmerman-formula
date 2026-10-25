# IC1_inner_column_cores — FROZEN CRITERIA (committed alone, before any script or number of this lane)

Lane id: IC1. X43 is left free for the session that runs X42; this lane does not edit X38–X42 or any of their files.

**Question.** X38 (route E, Burkert cold dark energy cores at ρ₀r₀ = Σ_a₀ ≡ a₀/(2πG)) passes SPARC and the cluster OUTER
bands but under-predicts the heaviest cluster cores (MID T3 Z +4). X40b found no native rule that raises them. X41
(`X41_collapse_floor_sigma`, 0ea05957ee) found that the collapse column Σ_coll = Δρ_m(z_f)·r_f of the half-mass object
has about the right mass slope (M^0.23) but sits 0.22–0.26 × Σ_a₀, so a "core-concentration factor" of about 11–23 is
missing. **Is that factor the ordinary inner concentration of a collapsed halo?** Test it with a rule that has no free
amplitude: the core inherits the densest column that inside-out spherical collapse builds, floored at Σ_a₀.

Standing rules: κ = ½ FITTED. Footings (canonical a₀ 9.3603e-11, alt 1.1312e-10 m s⁻²) are never pooled. Route E: gravity
is Newtonian on baryons + cold dark energy, and the law is emergent. Cold dark energy is a gravitating field component, not
matter and not a particle. Not "theory closed". Nothing here may say the data favour the framework.

**Post-hoc disclosure.** This lane's motivation was found after reading X41's committed numbers and X42's printed output
(uncommitted when this was frozen). For an NFW halo, (column at the scale radius) / (mean virial column) = c²/[3 m(c)],
m(c) = ln(1+c) − c/(1+c). That ratio is 11.0, 13.6 and 22.4 at c = 6, 7 and 10, which brackets the missing 11–23 and X42's
H1-EPS 13.6. IC1 has no amplitude, so these numbers cannot tune it. But the choice to test an inner-column rule was made
with them in view.

## 0. Step 0 (stop rules)

- **S0a.** X40b's committed `x40b_sd_scaling.py` is executed read-only, with only its output paths redirected. With s ≡ 1 it
  must reproduce X40b's committed X38-baseline numbers in `x40b_sd_scaling_results.json` to 1e-6. These are, per footing:
  the SPARC rms and median Υ on both backgrounds, every cluster key's pred in both h cells, and the groups mean and Z.
- **S0b.** X41's committed EPS block is executed read-only. It must reproduce X41's committed `sigma_coll_table` (Σ_coll
  and z_f at 10¹¹–10¹⁵ M☉) to 1e-8 relative.
- If either fails, **the lane stops** and reports the mismatch. No graded number is produced.

## 1. The halo (common, as X38 / X40b)

- Burkert, Σ ≡ ρ₀r₀ = s · Σ_a₀, s ≥ 1. X38's solver with its A1 compact root; SATURATED and RUNAWAY halos are counted.
- Galaxies: M200 from EM1's committed relation (background A 11.18 / 0.90, B 11.20 / 0.90), R200 at 200 ρ_c(0).
- Clusters: X30's machinery read-only, M_h(<r_ta) = M_fair = 5.364 M_b. Baryons are X30's β-gas × 1.2 + CFG922's BCG,
  exactly as X40b.
- Groups: P4 T3's estimator with X40b's halo (EM1 relation on background A, extrapolated, truncated at R200).
- Only the rule that sets s is replaced. It is IC1 below.

## 2. Rule IC1 — inside-out inner column, floored at Σ_a₀ (no free amplitude)

    Σ_core(M) = max(Σ_a₀, Σ_IC(M))   ⇔   s = max(1, Σ_IC(M) / Σ_a₀)

**Linear inputs.** σ²(M), D(z) and ρ_m0 come from X41's EPS block on backgrounds A (C2 refit) and B (CFG886), executed
read-only. That block uses EM1's CLASS run, a σ table on log M ∈ [7.0, 16.5] and D on z ∈ [0, 30].

**Collapse epoch of the inner mass fraction f.** This is the NFW (1997) median definition: the epoch by which half of the
halo's mass sits in progenitors more massive than fM. Analytic EPS:

    δ_c / D(z_c) = δ_c + w · √(σ²(fM) − σ²(M)),   w = √2 · erfc⁻¹(½) = 0.674490,   δ_c = 1.686

- w is the analytic median of the EPS step, not a fit.
- If D(z_c) ≥ 1, then z_c = 0.

**Shell density (the inside-out assumption).** The mass fM inside the halo keeps the mean density it had at its collapse,
Δ ρ_m(z_c(f)), with Δ = 18π² (the EdS value, as in X41). Its radius is r_f = [3fM / (4π Δ ρ_m(z_c))]^{1/3}. Its mean
enclosed column is

    C(f) = Δ ρ_m(z_c(f)) · r_f

**The densest column.** Ĉ(M) = max over f of C(f), for f ∈ [f_min, ½] with f_min = max(10⁻⁶, 10^7.0 / M), the lower edge
of the σ table.
- Search: a log f grid with 0.02-dex steps, then bounded Brent on log f inside the best grid bracket, to 1e-6 dex.
- If the argmax lies within one grid step of f_min, the halo is flagged **BOUNDARY**. Ĉ at f_min is still used, as a lower
  bound on the maximum, and the halo is counted.
- If the argmax is at f = ½, the halo is reported as such.

**Burkert matching (peak self-acceleration).** The inside-out halo's peak self-acceleration is

    g_IC = max over f of G fM / r_f² = (4π/3) G Ĉ

The Burkert core is given the Σ whose own peak self-acceleration, on the untruncated profile, equals g_IC:

    Σ_IC = (4π/3) Ĉ / k_B,   k_B ≡ π · sup_x h(x)/x²,   h(x) = ln(1+x²) + 2 ln(1+x) − 2 arctan x

k_B is computed numerically. It must equal 2π × CD1's committed `ceiling_over_a0` to 1e-6 (check K3).

**Halo mass M used by IC1.** As X41:
- SPARC and groups: M = M200;
- clusters: M = 6.364 M_b (the total, baryons + fair-share cold, inside r_ta).

**Background.** Σ_IC depends only on the background. SPARC rows use their own background (A or B). Clusters and groups use
background A, as X41 and X40b do. Σ_a₀, and hence s, depend on the footing.

## 3. Graded constraints (per footing)

- **SPARC (verdict-bearing):** EM1's line, rms ≤ 0.110 AND median Υ ∈ [0.50, 0.80], on both backgrounds A and B.
- **Clusters (verdict-bearing):** X38's 15 keys with X38's grading code, |Z| ≤ 2 in both h cells (0.672, 0.686). The keys
  are G-MID-T1..T3, G-MID-b, G-OUT-all, G-OUT-T1..T3, G-OUT-b, G-IN-all (KT 106), G-OUT-Mall, G-OUT-M1..M3, and G-IN-Mall
  (all 326).
- **Inner sub-grade (reported, not a class pass):** the core-sensitive keys G-MID-T1..T3, G-MID-b, G-IN-all and G-IN-Mall,
  each with |Z| ≤ 2 in both h cells. X38's own sub-grade (s ≡ 1) is printed beside it. This shows whether IC1 moves the
  cores. It cannot rescue a class that fails other keys.
- **Groups (graded line, reported beside the class, never folded into it, as X40b):** P4 T3's statistic, PASS iff
  CONSISTENT (|Z| < 2 and σ_tot ≤ 0.045). X38's baseline is printed beside it.
- **Known rule-invariant cells.** Under X38, X40b, H1, H2 and H1-EPS, G-OUT-M3 (UNDER, Z ≈ +2.2 to +2.5) and the groups
  line (ABOVE, Z ≈ +2.0 to +2.5) failed whatever the core rule did. They are graded here like every other cell. If they
  fail, the class fails. They are not excused.

## 4. Verdict classes (per footing; a class needs both footings to agree, else UNDECIDED)

- **IC1 PASSES** — the SPARC line passes on both backgrounds AND every cluster key passes in both h cells.
- **IC1 PASSES SPARC ONLY** / **IC1 PASSES CLUSTERS ONLY** / **IC1 FAILS** — otherwise, as X38. The failing keys are listed
  with their direction (UNDER / OVER).
- **IC1 INACTIVE** — Σ_IC < Σ_a₀ for every SPARC galaxy and every cluster, so the rule reduces to X38 exactly. It is
  reported with X38's grades. This is the expected outcome if inside-out collapse does not supply the concentration.
- **Suffix BOUNDARY-LIMITED** — appended if more than 10 % of the graded cluster halos are BOUNDARY (then Σ_IC is a lower
  bound).
- **Suffix FLOOR-BREAKING** — appended if more than 10 % of SPARC galaxies get s > 1. This is reported whether or not
  SPARC still passes.

## 5. Reported only (no verdict weight)

1. **The Σ_IC table** at 10¹¹–10¹⁵ M☉ on both backgrounds, giving Σ_IC, argmax f, z_c(argmax) and Ĉ. Also the log slope
   over 10¹³–10¹⁵ (X40b's requirement is 0.25–0.30) and the crossover mass where Σ_IC = Σ_a₀, per footing.
2. **The native concentration factor** η_IC(M) ≡ Σ_IC / Σ_coll(X41) at 10¹¹–10¹⁵ M☉. It is printed beside X42's post-hoc
   13.6 and X41's 11–23. The match is comparison only, never a grade.
3. **IC2, a BORROWED comparator.** An NFW halo with Dutton & Macciò (2014) c200(M) at z = 0 (PROVISIONAL: log c =
   0.905 − 0.101 log(M / 10¹² h⁻¹ M☉), quoted from the literature, not transcribed, no download).
   - Converted by the same peak-acceleration matching: NFW peak = 4πG ρ_s r_s · sup m(x)/x², so
     Σ_IC2 = 4π ρ_s r_s · sup[m(x)/x²] / k_B.
   - Graded with the same code, labelled BORROWED (ΛCDM-simulation calibration), with no verdict weight.
4. **Dwarf ordering.**
   - Inputs: CD1's committed rows for Draco, Sextans, Fornax and Leo I, per footing. M_b = 10^logMstar (gas-poor, disclosed)
     and M200 from EM1's relation on background A, extrapolated far below SPARC (disclosed).
   - Reported: s_IC for each dwarf and CD1's measured S beside it.
   - Label, pre-registered:
     - **DWARFS INACTIVE** — all four have s = 1;
     - **ORDER RIGHT** — Draco and Sextans both exceed Fornax and Leo I;
     - **ORDER WRONG** — Fornax and Leo I both exceed Draco and Sextans;
     - **MIXED** — otherwise.
   - Disclosed in advance: the EPS median gives one z_c per mass, with no per-object formation history, so the ordering is
     set by M200 alone. ORDER RIGHT would need lighter M200 for Draco/Sextans. This is a report, never a grade, and never
     a claim about the CCT dwarf campaign.
5. **Per footing:** s medians (SPARC; clusters by KT tercile; groups), r₀ medians, and SATURATED / RUNAWAY / BOUNDARY
   counts.

## 6. Checks (all must pass; `--mutate` must fail K2)

- **K0:** S0a holds (with s ≡ 1, X40b's committed X38-baseline numbers are reproduced to 1e-6).
- **K1:** S0b holds (X41's sigma_coll_table is reproduced to 1e-8 relative).
- **K2 (collapse epoch):** at three test masses (10¹², 10¹⁴, 10¹⁵ M☉, background A) and five f values each, z_c solves
  the frozen equation (D residual < 1e-8), D(z_c) ∈ (0, 1], and z_c is non-increasing in f on the grid (inner mass
  collapses first).
- **K3 (shape constants):** k_B equals 2π × CD1's `ceiling_over_a0` to 1e-6. sup_x m(x)/x² for NFW equals 0.216217 to 1e-5.
- **K4 (matching identity):** for a test Burkert halo with Σ = Σ_IC(10¹⁴ M☉), the numerically maximised G M(<r)/r² equals
  g_IC to 1e-6 relative.
- **K5:** peak RSS < 1 GB, one thread, PYTHONHASHSEED=0, `nice -n 15`. The run is not started while a 1024³ run is live.
- **MUTATE:** w is used with the opposite sign (inner mass collapsing later than today). K2's D(z_c) ≤ 1 check must FAIL
  (exit 1). Outputs go to `_MUTATE` files, and the MUTATE numbers are never graded.

## 7. Amendments

The rule, the f range, the matching and the verdict classes are fixed here. A post-result amendment may change check code
only, with the graded lines unchanged and disclosed. Any change to the rule after a graded number is printed is a new lane.
