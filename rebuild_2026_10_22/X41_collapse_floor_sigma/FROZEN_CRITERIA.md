# X41_collapse_floor_sigma — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** X38 + X40b found that cold dark energy core surface density must be a₀/(2πG) across galaxies, then climb
as about M^0.25–0.30 through groups and clusters (to 3–5 × a₀/(2πG) in cluster cores). Can the climb come from each
halo's own collapse?

**Rule CF** (owner session 10-25):

    Σ_core(M) = max(Σ_a₀, Σ_coll(M)),   Σ_a₀ = a₀/(2πG) (X38)

Σ_coll is the surface density the halo had when it collapsed, taken from the record's own linear growth history. No
ΛCDM concentration relation is used.

Standing rules: κ = ½ FITTED. Footings never pooled. Route E: Newtonian, law emergent, cold dark energy not matter. No
new constant. Not "theory closed". Nothing here may say the data favour the framework.

## 1. Σ_coll (first principles; no simulation calibration)

- **Linear P(k) and D(z):** EM1's CLASS run on the record's backgrounds A (C2 refit) and B (CFG886), executed read-only.
  This is EM1's code up to its halo-profile block.
- **Formation redshift:** the Lacey & Cole (1993) extended-Press–Schechter median half-mass formation epoch, which is
  analytic:
  - δ_c / D(z_f) = δ_c + ω̃ √(σ²(M/2) − σ²(M)), with δ_c = 1.686 and ω̃ = 0.974 (the EPS median for f = ½);
  - δ_c = 1.686 and Δ = 18π² are spherical-collapse values (first principles);
  - ω̃ = 0.974 is the analytic EPS median, not a fit.
- **Collapsed object:** half the mass, M/2, at mean density Δ ρ_m(z_f) with Δ = 18π². Then
  r_f = [3(M/2) / (4π Δ ρ_m(z_f))]^{1/3}.
- **Σ_coll ≡ Δ ρ_m(z_f) · r_f** (the object's ρ r at formation; frozen convention).
- **Halo masses:**
  - galaxies: M = M200 from EM1's committed relation (as X38);
  - clusters: M = 6.364 M_b (the fair-share total inside r_ta; X30's `Mfair` + M_b).

## 2. Halos and grading (as X38)

- Burkert with ρ₀r₀ = Σ_core(M) (X38's solver and its A1 branch/saturation rule).
- SPARC uses EM1's line on both backgrounds; clusters use X30's keys and |Z| ≤ 2 in both h cells.
- Gravity is Newtonian. Groups are not graded here: X40b's groups line machinery is not reused (named, not done).

## 3. Verdict (per footing; the class needs both footings to agree)

- **CF PASSES** — the SPARC line passes AND every cluster key passes.
- **CF INACTIVE** — Σ_coll < Σ_a₀ for every SPARC galaxy and every cluster, so the rule reduces to X38 exactly. This is
  reported with X38's grades.
- **CF PASSES SPARC ONLY** / **CLUSTERS ONLY** / **FAILS** — otherwise, as X38.

Reported, no verdict weight:
- the Σ_coll(M) table at 10¹¹–10¹⁵ M☉ and its log slope;
- the ratio Σ_coll / Σ_a₀ at the galaxy and cluster medians;
- the single multiplier η on Σ_coll that would make the rule active and raise the cluster cores to X40b's required 3–5 ×
  Σ_a₀. That multiplier is a DIAGNOSTIC of what a collapse-to-core relation must supply, never adopted. Whether the slope
  matches X40b's M^0.25–0.30 is the physics content.

## 4. Checks (all must pass; `--mutate` must fail K1)

- **K0:** X38's SD numbers are reproduced with the rule forced to Σ_a₀ (SPARC rms 0.0795 bg A canonical; OUTER all pred
  0.697).
- **K1:** EPS formation. At a test mass with σ²(M/2) − σ²(M) known, z_f solves the frozen equation to 1e-8. D(z_f) lies in
  (0, 1].
- **K2:** σ(M) from the executed EM1 code equals EM1's printed σ₈ for both backgrounds (EM1's KC: own vs F3 to 1e-3).
- **K3:** peak RSS < 2 GB.
- **MUTATE:** ω̃ is used with the opposite sign (formation later than today); K1's D(z_f) ≤ 1 check must fail.
