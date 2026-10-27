# X56_law_floor_structure — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** Route E (Newtonian gravity on baryons + cold dark energy halos cored at max(a₀/(2πG), η Σ_coll)) passes
SPARC, the groups, the cluster cores and outskirts, and four or five dwarf classes. X53 found it loses outer galaxy lensing
to the law by Δχ² +430 / +456: its halos are too light and they end at R200. X50 found the law's phantom pulls harder than
the floor halo and is never thinner than it in galaxies. Its own pull is bounded, |g_ph| < a₀ = 2πG Σ_a₀ (X50 A1, exact).
**Is the structure one statement: gravity is never weaker than the law?**

Standing rules: κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter and not a particle. No ΛCDM number
enters a rule. Not "theory closed". Nothing here may say the data favour the framework.

## 1. Hypothesis LF (the law is a floor on gravity)

    g(r) = max( ν(g_b/a₀) g_b ,  g_N[ρ_b + ρ_E] )          equivalently  M_eff(<r) = max( M_b ν(G M_b/(r² a₀)),  M_b + M_E )

- **First branch:** the law, evaluated on the baryons alone. It is spherical/isolated, with the record's
  ν(y) = ½ + √(¼ + 1/y) (μ = x/(1+x)), and is identical to EM1's LAW, F2's L4 and X1's iso column.
- **Second branch:** route E exactly as committed, with no change to any halo.
  - M_E is the halo from X43's rule, with M200 from EM1 R1 (bg A) and truncated as each lane truncates it.
  - The dwarfs use X51's cooling floor M200 = max(EM1, M_cool).
- **Applied pointwise in radius** at the level of the enclosed mass (equivalently the spherical pull). The max of two
  non-decreasing profiles is non-decreasing, so the density is never negative.
- **Reading:** X43's rule takes the max over surface densities. LF takes the max over the pull, and the a₀/(2πG) floor
  becomes the law's own bounded phantom. **No new constant.** The posit is the max itself. It is disclosed as a posit; no
  action is written here.
- **Disclosed:**
  - the law branch ignores the external field (isolated);
  - the law branch acts on baryons only, never on the halo;
  - in SPARC the law's disc pull uses the record's GB, the disc's own Newtonian field.

## 2. Primary inputs (fixed now)

- **c_f:** X48's committed ng 48 table (`x48_analyze_results_ng48.json`, as in `x48_regrade_ng48`), the theory statement's
  native value. **Reported:** c_f = 4 (X43 / X53 primary).
- **Everything else is each source lane's committed machinery, executed read-only:**
  - SPARC, groups and the 15 cluster keys from X43 (via X48's regrade);
  - lensing from X53 (B21 KiDS-1000 isolated lenses, full covariance, CFG805 two-halo term);
  - dwarfs from X51.

## 3. Grade (per footing; both footings must agree)

| line | pass if |
|---|---|
| SPARC | X43's `line` on bg A and bg B (rms ≤ 0.110, 0.50 ≤ median Υ ≤ 0.80) |
| groups (63, P4 estimator) | CONSISTENT |
| clusters (X30's 15 keys) | \|Z\| ≤ 2 in both h cells, every key |
| LG dwarfs (X51's five classes) | \|Z\| < 2 for every class |
| outer lensing (X53, all radii, with 2h) | Δχ²(LF2H − L2H) ≤ +9 **and** Δχ²(LF2H − H2H) < 0 |

- **Verdict:** **LAW FLOOR UNIFIES** if every line passes on both footings. Otherwise **LF FAILS: <lines>**. If the
  footings disagree, the verdict is **UNDECIDED**.
- **Reported:**
  - for each line, where each branch wins (fraction of radii or systems where the law branch is active);
  - SPARC per-galaxy rms against the law and against X43;
  - the lensing primary range R ≤ 0.31 Mpc;
  - the c_f = 4 variant.

## 4. Checks (all must pass; `--mutate` must fail K1)

- **K0 (law branch off):** reproduces X48 regrade ng 48 (SPARC 0.0650 / 0.0657, groups Z +1.53), X53's H2H χ² at
  c_f = 4 (583.9 / 580.6), and X51's MW ultra-faint median, each to 1e-3 relative.
- **K1 (floor property):** in every system and at every radius, M_eff ≥ both branches, and it equals one of them to 1e-12
  relative.
- **K2 (halo branch off):** reproduces EM1's LAW rms (0.0541 / 0.0537) and X53's L χ² (160.7 / 127.6) to 1e-3.
- **K3:** peak RSS < 1 GB; one thread; minutes.
- **MUTATE:** max → the route-E branch alone wherever the law branch would win, inside a K1-tested system (the law floor
  broken). K1 must fail.
