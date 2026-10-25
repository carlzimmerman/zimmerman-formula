# X42_core_rise_above_galaxies: neither the collapse floor nor baryon retention closes it

The criteria (`FROZEN_CRITERIA.md`) and the assumption ledger (`ASSUMPTION_LEDGER.md`) were committed alone in 4a13086d02,
before any script or number. `AMENDMENT_A1.md` (9caa641111) added two reported-only items at the coordinator's request
before any graded number: the H1-EPS variant and the core-concentration factor. Only Step 0 (X40b's own numbers) had run.

The lane id is X42 because X41 is the peer lane `X41_collapse_floor_sigma`. That lane computes a first-principles
Lacey–Cole EPS collapse floor with no fitted amplitude. It found the floor inactive (0.22–0.26 Σ_a₀). This lane does not
edit it; it reads that lane's committed `sigma_coll_table`.

Standing caveats:
- κ = ½ is FITTED.
- The two footings are never pooled.
- Route E: gravity is Newtonian on baryons plus cold dark energy, and the law is emergent.
- Cold dark energy is a gravitating field component, not matter.
- This is not "theory closed". Nothing here says the data favour the framework.

**Question.** X38's cores sit at Σ_a₀ = a₀/(2πG). X40b showed that, with galaxies pinned, clusters need a core surface
density that rises with mass, S ∝ M^0.25–0.30. Can either of two physically motivated rules produce that rise without a
constant tuned to the graded data, while keeping SPARC and passing groups and clusters?

- **H1, self-similar collapse floor:** Σ = max(Σ_a₀, Σ_a₀ (M/M_x)^{1/3}). It has one amplitude, M_x, calibrated on the
  cluster MID terciles only. SPARC and groups are then predicted out of sample.
- **H2, baryon retention:** Σ = Σ_a₀ · max(1, f_b,sys / f_b,gal). Here f_b,gal is the SPARC median and there is no other
  constant.

## Verdict: **BOTH FAIL** (both footings)

Where each hypothesis fails:

| | canonical | alt |
|---|---|---|
| H1 | groups (ABOVE, Z +2.41); MGAS T3 OUTER (G-OUT-M3, UNDER, Z +2.54 / +2.19) | groups (ABOVE, Z +2.27); G-OUT-M3 (UNDER, Z +2.54 / +2.19) |
| H2 | groups (ABOVE, Z +2.03); G-OUT-M3 (UNDER, Z +2.68 / +2.33) | G-OUT-M3 (UNDER, Z +2.48 / +2.14) |

Both rules fix most of what X38 got wrong:
- the MID cores: X38 MID T3 Z +4.26 / +3.80 becomes +0.48 to +0.83;
- the MID KT slope;
- the MGAS all-band.

Both rules keep SPARC. Both fail the heaviest gas tercile in the outskirts (MGAS T3 OUTER). X40b's empirical power law
also failed that key on canonical. H2 misses the groups line by Z +0.03 on canonical, and passes it on alt.

**Step 0 passes.** A scratch rerun of X40b matches its committed JSON with 0 differences, including the groups failure
(Z +2.48 / +2.29) and α_best 0.30 / 0.25.

## H1: the self-similar collapse floor (calibrated on clusters only)

| | canonical | alt |
|---|---|---|
| log₁₀ M_x (calibrated, cluster MID terciles, h 0.672) | 12.988 | 13.235 |
| Σ_ss(10¹⁴ M☉) | 232.5 M☉ pc⁻² = 2.18 Σ_a₀ | 232.4 M☉ pc⁻² = 1.80 Σ_a₀ |
| χ²_cal (3 MID keys) / χ² of 15 keys, h 0.672 | 1.77 / 17.37 | 1.77 / 17.37 |
| cluster s by KT tercile T1 / T2 / T3 | 2.91 / 3.19 / 3.84 | 2.41 / 2.64 / 3.18 |
| **SPARC (out of sample)**, rms / median Υ, background A; background B | 0.0795 / 0.77; 0.0792 / 0.76: PASS | 0.0729 / 0.60; 0.0729 / 0.60: PASS |
| **groups (out of sample)**, mean Δ log σ (Z) | +0.096 (+2.41) FAIL | +0.090 (+2.27) FAIL |

- **M_x lies above every SPARC halo and the median group (group median s = 1.000).** The largest SPARC M200 is 2.93e12 M☉, so s = 1 for every
  galaxy and SPARC is exactly X38's. This is a pass by construction of the calibrated M_x, not a test.
- **Groups have median s = 1.000, so the rule leaves them unchanged.** Their Z moves only from +2.48 to +2.41
  (canonical). The out-of-sample prediction for groups is a FAIL.
- **α free, with (α, M_x) both fit on χ²_cal:**
  - α_best = 1.00, at the edge of the grid (χ²_cal 0.56 / 0.60).
  - Δχ² ≤ 4 holds for α ∈ [0.10, 1.00] (canonical) and [0.05, 1.00] (alt).
  - **α = 1/3 is ALLOWED** (Δχ² 1.21 / 1.17).
  - The three MID points barely constrain the slope. They pin the cluster core level, not the mass law.
- **H1-EPS** (reported only; slope α_EPS = 0.2316 from `X41_collapse_floor_sigma`):
  - log₁₀ M_x = 12.21 / 12.57, Σ_ss(10¹⁴) = 277.5 M☉ pc⁻².
  - SPARC passes (7 % of canonical galaxies get s up to 1.15).
  - Groups +0.087 (Z +2.12) / +0.086 (Z +2.11): FAIL.
  - G-OUT-M3 fails. Δχ²_cal for α_EPS is 1.50 / 1.46, so it is allowed.
- **Both groups predictions fail.** H1 gives Z +2.41 / +2.27 and H1-EPS gives Z +2.12 / +2.11. The shallower slope
  reaches the groups more, but not enough.
- **Implied core-concentration factor**, Σ_ss / Σ_coll(EPS of `X41_collapse_floor_sigma`):
  - H1: 9.0× at 10¹³, 11.4× at 10¹⁴ and 14.4× at 10¹⁵ M☉; 12.9× at the median cluster (3.41e14 M☉). Both footings agree
    to 0.1×.
  - H1-EPS: 13.6× at every mass, by construction.
  - The peer's own η_needed is 11.4–19.0 (canonical) and 13.8–23.0 (alt).
  - A collapse-set core would have to be about 10–15× denser than the EPS half-mass object at formation. Nothing here
    derives that factor.
- **H1-cM** (reported only, Dutton & Macciò 2014 shape, PROVISIONAL): log₁₀ M_x = 11.79 / 12.22.
  - Groups Z +2.01 / +2.01: FAIL.
  - G-OUT-M3 fails.
  - The local slope of ρ_s r_s is 0.19–0.21 over 10¹¹–10¹⁵ M☉.

## H2: baryon retention (no fitted constant beyond the galaxy median)

f_b,gal = 0.0577 (the SPARC median, background A). SPARC f_b runs from 0.037 to 0.084.

| | canonical | alt |
|---|---|---|
| cluster f_b(R200), KT T1 / T2 / T3 | 0.152 / 0.166 / 0.196 | 0.145 / 0.158 / 0.186 |
| cluster s, KT T1 / T2 / T3 | 2.63 / 2.88 / 3.41 | 2.51 / 2.74 / 3.22 |
| SPARC, background A; background B | 0.0705 / 0.72; 0.0717 / 0.72: PASS | 0.0665 / 0.56; 0.0676 / 0.57: PASS |
| groups (f_b median 0.090, s median 1.56) | +0.082 (Z +2.03) FAIL | +0.077 (Z +1.87) CONSISTENT |
| clusters: failing keys; χ² of 15 keys | G-OUT-M3 (+2.68 / +2.33); 17.92 | G-OUT-M3 (+2.48 / +2.14); 17.43 |
| T-fb (Spearman ρ, p) under H2 / under X38 | +0.10 (0.18) / +0.14 (0.065): not strong | +0.16 (0.034) / +0.21 (0.0048): not strong |

- **H2 lands at the needed level with no fitted amplitude.** The cluster/galaxy baryon-fraction ratio is 2.6–3.4, which
  is the ~3–5× X40b asked for at its low end.
- **Upper-half SPARC galaxies get s up to 1.46.** This improves the SPARC rms (0.0795 → 0.0705 canonical).
- **The within-SPARC f_b trend is weak and positive** (X38 ρ +0.14 / +0.21). H2 reduces it, so it does not contradict H2.
  Within SPARC, f_b is a monotone function of M_b through EM1's relation, so T-fb tests mass and f_b together.
- **It still misses G-OUT-M3 on both footings, and groups on canonical by Z 0.03.** H2 therefore FAILS on both footings.
- **Reported variant: cluster f_b at r_ta** (1/6.364, s = 2.72 for all). It fails MID T3 on canonical, plus MID-b and M3.
  The rise inside clusters comes from f_b(R200) increasing with mass.

## Reading

- **Both rules supply most of the needed rise.**
  - H1 needs one cluster-calibrated amplitude, equivalent to a 10–15× concentration over EPS collapse.
  - H2 needs none: the cluster/galaxy baryon-fraction ratio of ~2.6–3.4 is close to the needed factor.
- **Two residuals remain, and they point the same way (more central mass needed):**
  - The groups line: H1 does not reach the groups; H2 just misses on canonical.
  - The MGAS T3 OUTER band: the gas-richest clusters still under-predict, Z +2.1 to +2.7.
- **X40b's power law in mass leaves the same key failing**, so it is not specific to these two rules.
- H2 is the closer of the two: it fails 1 line on alt and 2 on canonical, with no tuned constant. It is not a pass.

**Choices fixed in the code before any graded number, inside the frozen text:**
- H1 uses the cluster halo mass M_fair, as X40b's (C) did.
- H2's cluster f_b uses X30's gas × 1.2 with no BCG, and R200 at 200 ρ_c(0) with background A's h. R200 was found inside
  X30's grid for all clusters (0 fallbacks).
- The α-free profile includes α_EPS and 1/3 on the grid.

**Checks 6/6:**
- K0: s ≡ 1 reproduces X38 to 3.9e-7, and X40b's groups exactly.
- K1: Step 0 passes.
- K2: H1 floor and rise; median cluster s T3 > T1.
- K3: H2 floor; galaxies at or below the median have s = 1, and the cluster median s is 2.96 / 2.81.
- K4: the groups integrator matches P4, and the R200 solver is accurate to 1.5e-14.
- K5: peak RSS 0.75 GB, runtime 4550 s.

**MUTATE:** `X42_MUTATE=1` sets H1's exponent to 0, so s ≡ 1 and H1 collapses to X38: groups Z +2.48 / +2.29, MID T3 and the MGAS bands fail. It also inverts H2's ratio, giving low-f_b galaxies s up to 1.54 and clusters s = 1. K2 and K3 FAIL as frozen, checks 4/6, exit 1. Those numbers are reported only.

## Files

- `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `AMENDMENT_A1.md`
- `x42_step0.py` → `x42_step0.out`, `x42_step0_results.json`
- `x42_core_rise.py` → `x42_core_rise.out`, `x42_core_rise_results.json`
- `_MUTATE` twins of the output and results files
- `x42_x30_machinery*.log` (local, gitignored)

Run:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x42_step0.py                    # exit 0 (Step 0)
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x42_core_rise.py                # exit 0, 6/6
    X42_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x42_core_rise.py   # exit 1, K2 + K3 fail

The groups use Tian+2026 from `_external_data/vizier2026/J_A_A_710_L39.tsv`, which is outside git, as in P4 and X40b.
