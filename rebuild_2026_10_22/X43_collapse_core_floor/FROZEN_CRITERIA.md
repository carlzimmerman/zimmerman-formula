# X43_collapse_core_floor — FROZEN CRITERIA (committed alone, before any script or graded number of this lane)

**Hypothesis CC (derived on paper, 10-25, before any graded number):**

    Σ_core(M) = max( a₀/(2πG),  η Σ_coll(M) ),   η = (4 / (3 B(1))) c_f^{5/4}

Cold dark energy collapses like collisionless dust. The collapsed half-mass object at the Lacey–Cole EPS median formation
epoch has Bertschinger's self-similar infall profile, ρ ∝ r^(−9/4) (first principles). Its core is the inner 1/c_f of the
formation radius.
- Match a Burkert core to the infall profile by enclosed mass at r₀ = r_f/c_f. That gives
  ρ₀r₀ = (4/3) c_f^{5/4} Σ_coll / B(1), with B(1) = 3 ln 2 − π/2.
- Σ_coll is X41's Δ ρ_m(z_f) r_f, from the record's own CLASS P(k) and D(z). Its slope, M^0.23, was found in X41.
- The cold sector can never be cored more thinly than a₀/(2πG). That is the floor, and the framework's constant
  (a₀ = c²√(Λ/32π)).
- **c_f = 4** is the one external number: the concentration halos have at their formation epoch. It is EXTERNALLY
  CALIBRATED (Bullock et al. 2001, K = 4; Zhao et al. 2009), from ΛCDM simulations, and disclosed as such. It is not
  fitted here. It gives **η = 14.83**.
- Paper prediction (disclosed): η Σ_coll at 10¹² M☉ ≈ 101 M☉ pc⁻² ≈ the floor. Groups land above it, and 10¹⁴–10¹⁵ M☉
  lands at 2.8–4.9 × the floor, which is X40b's required 3–5×.

Standing rules:
- κ = ½ FITTED. Footings never pooled. Route E: Newtonian, law emergent. Cold dark energy is not matter.
- Not "theory closed". Nothing here may say the data favour the framework.
- Raw data, framework-native. c_f is the disclosed exception, and the label carries [c_f EXTERNAL].

## 1. Systems and grading (no number tuned)

- **SPARC:** X38's machinery (EM1 read-only, EM1's committed M200 relation) with Burkert at ρ₀r₀ = Σ_core(M200). EM1's
  line, both backgrounds.
- **Clusters:** X30's machinery and keys, read-only, as X38. M = 6.364 M_b, normalised to the fair share inside r_ta.
  |Z| ≤ 2 in both h cells.
- **Groups:** P4 T3's estimator and the 63 Tian+26 groups, executed read-only exactly as X40b does. M200 comes from EM1's
  relation on the groups' M_b, with Burkert at Σ_core(M200). The class uses P4's `class_stats`, and PASS = CONSISTENT.
- Σ_coll uses background A (X41's table) for every system; background B is reported for SPARC.

## 2. Verdict (per footing; the class needs both footings to agree)

- **CC PASSES** — SPARC line (both backgrounds) AND every cluster key AND groups CONSISTENT.
- Otherwise **CC FAILS: <systems / keys>**, listed with their sign.
- The label always carries **[c_f EXTERNAL]**.

Reported, no verdict weight:
- c_f = 3 and 5 (sensitivity only; a class change there is reported, never adopted);
- the crossover mass where η Σ_coll = Σ_a₀;
- the fraction of SPARC galaxies and groups above the floor;
- the comparison per key with X38.

## 3. Checks (all must pass; `--mutate` must fail K1)

- **K0:** X38 is reproduced with η = 0 (SPARC rms 0.0795 bg A canonical; cluster OUTER all-KT 0.697). X40b's group K4 is
  reproduced (63 groups, no-halo integrator vs P4 to 1e-4).
- **K1:** η = (4/(3B(1))) c_f^{5/4} equals 14.83 at c_f = 4 (to 1e-3). The infall-to-Burkert mass match at r₀ holds to
  1e-10 for one test halo.
- **K2:** X41's Σ_coll table is reproduced (10¹² M☉ → 6.8 M☉ pc⁻²).
- **K3:** peak RSS < 2 GB; one thread; minutes.
- **MUTATE:** the infall slope 9/4 is replaced by 3/2 inside η; K1 must fail.
