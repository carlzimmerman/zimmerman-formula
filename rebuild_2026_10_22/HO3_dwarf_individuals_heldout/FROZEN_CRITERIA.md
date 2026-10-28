# HO3_dwarf_individuals_heldout — FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-27. One held-out test of the frozen combined picture ("CL2 picture") on the Local Group dwarfs **as
individuals**. Standing rules: κ = ½ FITTED. Footings never pooled; canonical (a₀ = 9.3603e-11 m/s²) is primary, alt
(1.1312e-10 m/s²) is reported with its own verdict. Cold dark energy is not matter and not a particle; ΛCDM appears only
as the rival. Not "theory closed". Nothing here may say the data favour the framework. No downloads.

## 0. Why this is held out, and what is not

- The calibrating lanes (X51 cooling-floor halos, X62 environment switch, CL2 which keeps X62's dwarfs unchanged)
  graded only the **five dwarf class medians** (|Z| < 2 on a bootstrap of the class median).
- **Held out here:** the per-object residuals, i.e. whether each dwarf sits where the picture puts it within its own
  measurement error; and the isolated LG field dwarfs one by one.
- **Not blind (disclosed):** the per-object field numbers are already in the record. X1's iso column, X24's README and
  X62's README print Leo T +0.41 ± 0.14 and Phoenix +0.40 ± 0.07 (canonical) above the law, and X51/X62 print seven
  satellite individuals (Crater II −0.97, NGC 147 −0.43, Sagittarius −0.25, ...). The rules below were chosen from the
  record's conventions, not tuned on these numbers, but the writer knew them. A reader should weight the verdict
  accordingly.
- **Partly calibrated (disclosed):** the satellites' halos (X51) were set so that their class medians pass; their
  per-object scatter was not graded. The LG field dwarfs carry no fitted constant at all in this picture (the law on
  baryons, a₀ per footing).

## 1. Sample (exactly X1's committed per-system table, per footing)

`rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv`: **89 dwarfs per footing** (the "OS1/CD1 89 dwarfs").
- **Satellites (host MW or M31): 76** = MW ultra-faint 31, bright M31 25, M31 others 5, MW classical 8, M31 dE 3, and
  X1's four MW individuals (Antlia II, Canes Venatici I, Crater II, Sagittarius).
- **Isolated (host "field"): 13** = X1's LG field class (Antlia B, Aquarius, Cetus, IC 1613, Leo A, Leo T, NGC 6822,
  Pegasus dIrr, Phoenix, Sagittarius dIrr, Tucana, UGC 4879, WLM).
- X20 (61 hosted, τ subsets) and X24 (13 field + matched-mass hosted) use subsets of this same table; no other dwarf
  individual set is graded in the record. Nothing is added or removed.

## 2. The frozen CL2 picture (implemented exactly)

- **Switch:** a dwarf carries a route-E cold dark energy halo iff it is a satellite (X1 `host` ∈ {MW, M31}) OR its
  M200 > 10^12.3 M☉. The second clause is never true for a dwarf (X51's M200 ≤ ~3e8 M☉); it is evaluated anyway.
- **Satellites:** route E = Newtonian baryons + X51's halo, exactly as X62's `run_x51` does it (X51's cooling-floor
  M200 = max(EM1, M_cool = 1.13e8 M☉), a₀-floor Burkert core, binary correction, g_N from M★/2 at r₁₂ = 4/3 r_h).
  CL2's c_f(M) slope does not reach dwarfs: every dwarf sits on the a₀ floor (X51: Σ_coll ≪ Σ_a₀ below 1e11 M☉), and
  CL2's criteria (b57ed8751f: "The dwarfs are unchanged: their flag is satellite-only") keep X62's dwarfs. X51's
  halo prescription is unchanged.
- **Isolated:** the galaxy law on baryons only, g = g_N ν(g_N/a₀), ν(y) = ½ + √(¼ + 1/y), same g_N and g_obs as X51.
- **Residual:** E_i = log₁₀(g_obs / g_pred) (X51's E). **Per-object error** s_i = X1's `sdMC[Newton]` (the record's
  per-system Monte-Carlo error, the same s X51/X62 use in their class bootstrap). **Z_i = E_i / s_i.**
- Machinery: X51's committed script executed read-only as a text copy with exactly X62's one edit (the route-E total
  passes through LF_G with the satellite flag), as X62 and CL2 do. Per-object rows come from that copy's own `rows()`.

## 3. Held-out statistics and pass rules (per footing, per subsample: satellites N 76, isolated N 13)

Conventions: |Z| < 2 per graded unit (X49/X51/X62); "fraction beyond z ≥ 2 vs chance" (CD1 c99930b2af); permutation /
binomial p ≥ 0.01 as the significance floor (X20, X24).

- **S1 (tail fraction):** k = #{|Z_i| ≥ 2}. Binomial one-sided p = P(K ≥ k | N, p₀ = 0.0455). Pass iff p ≥ 0.01.
- **S2 (typical size):** median |Z_i| ≤ the 99th percentile of median |Z| for N independent N(0,1) draws (2×10⁵ draws,
  numpy default_rng seed 20261027). Pass iff so. (A median below the null is not a failure of the picture; reported.)
- **S3 (worst object):** P(max |Z| ≥ observed) = 1 − (1 − p₂(|Z|max))^N, p₂ the two-sided normal tail. Pass iff ≥ 0.01.
- **Subsample verdict:** CONSISTENT WITH ERRORS if S1, S2, S3 all pass; else EXCESS SCATTER: <rules>.
- **Footing verdict:** **HELD-OUT PASS** if both subsamples are CONSISTENT; else **HELD-OUT FAIL: <subsample (rules)>**.
  Canonical is primary; alt gets its own verdict. If they disagree the lane reports **SPLIT** with both.
- **Per-object flags (frozen, both footings):** Leo T and Phoenix: E, s, Z; flag ABOVE PICTURE if Z ≥ 2, BELOW if
  Z ≤ −2, else CONSISTENT. Every object with |Z| ≥ 2 is listed by name.
- **Reported, not graded:** sign balance (fraction E > 0) per subsample; Σ Z² vs χ²_N p-value; maximum-likelihood
  intrinsic scatter σ_int (E_i ~ N(μ, s_i² + σ_int²)); Spearman(E, log M★) per subsample (X24 found −0.73 in the
  field); the same S1–S3 with Crater II and Antlia II removed from satellites (tidal stripping is not modelled, X51/X24);
  per-object table as CSV.

## 4. Step-0 stop rule

Before any held-out number: the copy, run in X62's mode "on", must reproduce X62's committed
`x62_x51copy_on_results.json` (cfc8f2c3cf) class medians, Z and the seven individuals to 1e-9 on both footings; and in
mode "off" (route E everywhere) X51's committed `x51_dwarfs_results.json` class medians to 1e-9. If either fails, the lane
stops and reports the blocker (no held-out number is graded).

## 5. Checks (all must pass; MUTATE must fail K1)

- **K0:** Step 0 above (both footings).
- **K1:** switch property. For every object, g_pred equals the branch the frozen flag selects (host ∈ {MW, M31} OR
  M200 > 10^12.3 → g_N + g_h, else ν g_N) to 1e-12 relative, the flag recomputed independently from the CSV host
  column; counts 76 halo / 13 law per footing.
- **K2:** isolated E against X1's `Delta[iso AQUAL L*0]` (an independent computation of the same law): median |ΔE| < 0.03
  dex over the 13 (X51's K2 tolerance).
- **K3:** rule calibration. (a) 2000 pure-null samples (Z ~ N(0,1), N 76 and N 13): the subsample fail rate is ≤ 0.04.
  (b) Planted excess (Z ~ N(0, 2²)) for N 76: fail rate ≥ 0.90. Seeded (20261027).
- **K4:** peak RSS < 1 GB; one thread; PYTHONHASHSEED=0.
- **Rerun:** a second normal run gives a byte-identical results JSON (sha256 recorded in the README).
- **MUTATE twin** (env `HO3_MUTATE=1`, outputs `*_MUTATE.*`): the satellite flag is inverted inside the copy (field
  dwarfs get halos, satellites the law) while K1 still checks the frozen flag. **K1 must fail**; the run exits 1.

## 6. What a result means

- HELD-OUT PASS: the picture places LG dwarfs individually within their errors; evidence for the switch picture on dwarfs,
  not a derivation of it.
- FAIL on isolated: the isolated dwarfs carry extra beyond the law system by system (as X24 found); the environment key is
  not clean, which is information about the switch, not a refit opportunity. No new constant is introduced in this lane.
- FAIL on satellites: the cooling-floor halo gets class medians right but not individuals (e.g. stripped systems).
