# X40b_core_surface_density_scaling: no framework-native rule raises the cluster core surface density

The criteria (`FROZEN_CRITERIA.md`) and the assumption ledger (`ASSUMPTION_LEDGER.md`) were committed alone in b09db13390,
before any script or number.

The lane id is X40b because X40 is the peer lane `X40_fixed_core_radius`. That lane is independent; it found that a fixed
core radius fails.

Standing caveats:
- κ = ½ is FITTED.
- The two footings are never pooled.
- Route E: gravity is Newtonian on baryons plus cold dark energy, and the law is emergent.
- Cold dark energy is a gravitating field component, not matter.
- This is not "theory closed". Nothing here says the data favour the framework.

**Question.** X38's halos are Burkert-cored at ρ₀r₀ = a₀/(2πG). They pass SPARC and the cluster outskirts, but the
heaviest cluster cores come out short. X39 showed that baryonic contraction breaks SPARC. Can a rule with no new constant
raise Σ_core at cluster masses while galaxies stay at a₀/(2πG)?

## Verdict: **NO FRAMEWORK-NATIVE RULE CLOSES IT** (both footings)

**Step 0 passes.** A scratch rerun of X38 matches the committed JSON exactly (max |Δ| = 0). This lane's code with s ≡ 1
reproduces X38 to 3.9e-7.

| canonical (alt) | X38 | rule A: max(a₀, g_b(r₀)) | rule A′: max(a₀, g_N,tot(r₀)) | rule B: a₀(z_f) |
|---|---|---|---|---|
| SPARC rms / median Υ, background A | 0.0795 / 0.77 (0.0729 / 0.60) | identical | identical (alt 0.0730) | 0.0827 / 0.79 (0.0751 / 0.66) |
| SPARC line | PASS | PASS | PASS | PASS |
| MID T3, pred (Z); measured 2.13 | 1.05 (+4.26) | identical | identical | 1.07 (+4.18) (alt 1.09, +3.73) |
| MID KT slope Z | +3.07 (+2.99) | identical | identical | +3.06 (+2.98) |
| OUTER all-KT Z | +0.14 (−0.06) | identical | identical | +0.11 (−0.09) |
| MGAS T3 OUTER Z | +5.36 (+4.94) | identical | identical | +5.29 (+4.88) |
| MGAS all OUTER Z | +2.36 (+2.08) | identical | identical | +2.32 (+2.03) |
| groups line (P4 T3), mean Δ (Z) | +0.097 (+2.48) ABOVE | identical | identical | +0.098 (+2.49) ABOVE |

### Rules A and A′: the rule never switches on in a cluster

At X38's cluster cores, the baryonic acceleration is far below a₀. Median g_b(r₀)/a₀ by KT tercile:

| tercile | canonical | alt |
|---|---|---|
| T1 | 0.048 | 0.041 |
| T2 | 0.055 | 0.048 |
| T3 | 0.073 | 0.064 |

- **Gas sets g_b(r₀).** The hot gas gives 98.3–99.5 % of g_b(r₀); the CFG922 BCG gives 0.5–1.7 %. This matches X39's
  finding that the BCG is negligible at 0.3–1 Mpc.
- **Adding the halo's own pull (A′) is not enough.** That term adds B(1)/2 = 0.254 a₀ at the core, so g_N,tot(r₀) still
  stays near 0.3 a₀.
- **So s* = 1 for every cluster.** All 326 clusters, both h cells and both footings. No halo ran away and none saturated.
- **Clusters reproduce X38 exactly.**

In SPARC, s* = 1 at every galaxy's chosen Υ on both footings and both backgrounds. A few halos have s* > 1, but only at
Υ values the fit does not choose. So galaxies stay at a₀/(2πG); this is verified, not assumed.

The effective scaling is α_eff = 0.000: the rules switch on in neither galaxies nor clusters. To set Σ ≈ 2–5 a₀/(2πG),
cluster cores would need a baryonic acceleration of 2–5 a₀. They have 0.04–0.07 a₀, which is 30–100× short.

### Rule B: the sign is right, but the effect is far too small

The DESI M-DEC curve for a₀(z)/a₀(0) is not monotone:

| z | 0 | 0.5 | 1.0 | 1.5 | 2.0 | 3.0 |
|---|---|---|---|---|---|---|
| a₀(z)/a₀(0) | 1.000 | 1.032 | 0.989 | 0.931 | 0.874 | 0.775 |

It peaks at z = 0.36.

- **The sign check comes out the opposite way to what was expected.** Clusters formed at z_f = 0.5 and galaxies at
  z_f = 1.5 give a cluster/galaxy Σ ratio of 1.108, which raises cluster Σ. This holds wherever cluster formation sits
  later than galaxy formation and above z ≈ 0.36. Below z ≈ 0.36, later formation lowers Σ: d(a₀/a₀,0)/dz runs from
  −0.11 to +0.23 on [0, 1].
- **Rule B fails on size, not sign.** No choice of epochs can do better than max/min of the curve on z ∈ [0, 3], which is
  1.336. That is far below the 3–5× that (C) needs.
- **Its SPARC galaxies sit at 0.93 Σ_a₀,** which moves median Υ to 0.79 (canonical) and 0.66 (alt). Both are still
  inside the line.
- **The formation epochs are PROVISIONAL.**

### (C), reported only and not framework-native: S ∝ M^α with galaxies pinned

The pivot is the largest SPARC M200, 2.93e12 M☉.

| | canonical | alt |
|---|---|---|
| α_best (minimum χ² over the 15 cluster keys, h 0.672) | 0.30 (χ² 18.5) | 0.25 (χ² 18.7) |
| failing keys at α_best | MGAS T3 OUTER, Z +2.22 | MGAS T3 OUTER, Z +2.36 |
| α where every key passes in both h cells | none | 0.30 only |

At α = 0.25–0.30 the cluster cores sit at s ≈ 3.0–3.8 (KT T1) and 3.7–4.8 (KT T3).

- **The missing factor is about 3–5, not about 2.** With galaxies pinned at a₀/(2πG), the cluster cores need roughly
  3–5 × a₀/(2πG).
- **The needed slope is in the range of the empirical scaling.** α ≈ 0.25–0.30 compares with Boyarsky+2009's S ∝ M^~0.2,
  which is PROVISIONAL and not transcribed in the record.
- **Rules A, A′ and B fall far short of it.** Their effective α is 0.000 for A and A′ and 0.011 for B.

### Groups: a new failure for X38 itself

The P4 T3 line was not graded in X38. Here X38's halos (s ≡ 1) under-predict group σ, so the line fails:

| model | mean Δ log σ (Z), canonical | alt |
|---|---|---|
| X38 halos, EM1 relation (extrapolated) | +0.097 dex (+2.48) | +0.091 (+2.29) |
| fair-share variant (M200 = 5.364 M_bar) | +0.197 (+4.47) | +0.192 (+4.32) |

- Every rule leaves this unchanged.
- It points the same way as the clusters: group-mass halos also want more central mass than Σ_a₀ gives.

## Reading

- **Acceleration-set and epoch-set cores are both ruled out as the missing scaling.** Σ_core = max(a₀, g)/(2πG) is the
  natural way to tie the core to a₀ with no new constant. It is inert: wherever there are cores, the baryons are
  sub-a₀. a₀(z_f) can supply at most 1.34×.
- **The requirement is now sharper than X39's ~2×.** With galaxies held at a₀/(2πG), cluster cores need Σ of about
  3–5 a₀/(2πG). That is a mass scaling with α ≈ 0.25–0.30, and groups lean the same way.
- **Nothing in the record yet supplies it.**
  - A pure power law still fails MGAS T3 on canonical.
  - The peer X40_fixed_core_radius showed that a fixed core radius fails.
  - So surface density remains the right variable, but its mass scaling would be a new constant. In (C) that constant is
    α; nothing here derives it.

**Choices fixed in the code before any graded number, inside the frozen text:**
- The BCG enters only g_b, used by rules A and A′. The lensing mass stays X38's M_b + M_h, which keeps K0 exact. X39
  showed that the BCG's lensing mass is negligible at these radii.
- The groups' halo uses EM1's G and background-A h. The groups' integral uses P4's constants.

**Checks 6/6:**
- K0: reproduces X38, and Step 0 passes.
- K1: the fast compact root matches X38's solve_r0 to 6.2e-9, including 10 saturated cases.
- K2: the a₀ floor holds (test halo, and min s* = 1).
- K3: the fixed-point residual is 4.1e-15.
- K4: the groups integrator matches P4 to 8.9e-16 dex on all 63 rows.
- K5: peak RSS 0.60 GB, run time 157 s.

**MUTATE** (`X40B_MUTATE=1`, max → min) fails K2 and exits 1. Its test halo gives s* = 0.001; under it, SPARC rms is
0.25 at Υ 1.20 and the clusters fall to s ≈ 0.002.

## Files

- `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`
- `x40b_sd_scaling.py`
- `x40b_sd_scaling.out`, `x40b_sd_scaling_results.json`
- `_MUTATE` twins of the output and results files
- `x40b_x30_machinery*.log`

Run:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x40b_sd_scaling.py                 # exit 0, 6/6
    X40B_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x40b_sd_scaling.py    # exit 1, K2 fails

The groups use Tian+2026 from `_external_data/vizier2026/J_A_A_710_L39.tsv`, which is outside git, as in P4.
