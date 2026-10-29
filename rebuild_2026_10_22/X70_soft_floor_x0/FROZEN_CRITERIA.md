# X70_soft_floor_x0: FROZEN CRITERIA (committed alone, before any script or graded number)

**Source.** The external model's final-mile spec, Task 3 (relayed by the owner, 10-29). It weakens the floor as a function
of the peak baryonic acceleration:

Σ_core = max(Σ_M F(X₀), η Σ_coll), with F(X₀) = 4X₀/√(1 + (4X₀)²) and X₀ = max_r g_bar(r)/a₀.

**Standing:**
- κ = ½ FITTED. Footings never pooled. Not "theory closed". Nothing here may say the data favour the framework.
- Route E, Newtonian. η = 14.83 (c_f = 4) EXTERNAL, not refit.
- **The "4".** The spec calls 4 the exact ratio 2πGΣ/g_pk,Burkert. Pre-flight arithmetic (not a graded number):
  max B(x)/x² = 0.50897, so the ratio is 2/0.50897 = **3.93**, not exactly 4. The spec's 4 is used as written; 3.93 is a
  reported variant. F is a chosen interpolating form. It is not derived, and the label says so.

## Inputs

- **SPARC:** all 175 `_rotmod.dat` files, through EM1's loader.
  - X₀ is evaluated at the fiducial Υ_disk = 0.50, Υ_bul = 0.70 (EM1's U = 0.50 column):
    g_bar = (sgn(V_gas) V_gas² + Υ_d V_disk² + Υ_b V_bul²)/R, maximised over the tabulated radii.
  - One X₀ is computed per galaxy and footing (a₀ is per footing).
- **Fit:** X43's SPARC harness (via X68's read-only namespace). The rule is changed only for floor galaxies:
  s = max(Σ_M F(X₀), η Σ_coll(M200)). EM1's Υ marginalisation is unchanged.

## Gates (per footing; the class needs both footings to agree)

- **G1:** fewer than 15 % of the 175 galaxies have F(X₀) < 0.794 (a shift of more than 0.1 dex in Σ_core's floor).
- **G2:** SPARC rms ≤ 0.08 dex on both EM1 backgrounds.
- **Verdicts:** **SOFT FLOOR PASSES** = G1 ∧ G2. **FAILS** = the list of failed gates.

## IC 1613 (graded separately; "rescued" or "not rescued")

- **Data:** IN1's single-point HI estimator at R_max = 2.71 kpc. M★ = 2.88e7 and M_gas = 5.93e7 M☉ (Oh+15, RT1 parse).
  V_rot is rescaled from 48° to i = 32° and 36° (IN2's independent MUSE values).
- **Model:** route E, g_pred = g_N + G M_h(R_max)/R_max².
  - M_h is X43's Burkert at Σ_core (hard floor, then soft floor).
  - M200 comes from EM1's background A relation at lM_b = log(M★ + M_gas), normalised at R200, as in X43's SPARC.
- **X₀ is not measured by a profile here.** It is bracketed:
  - (lo) g_N(R_max)/a₀ of the point mass, a lower bound on the peak;
  - (hi) the peak of an exponential thin disc of mass M★ + M_gas with R_d = R_h/1.678 (R_h = 1.44 kpc, IN1's X1 row).
- **Rescued** iff |E_HI| ≤ 2 × 0.075 (RT1's s) at both i = 32° and 36°, for both X₀ brackets, on both footings.
  The hard-floor E_HI is reported alongside.
- **Reported:** the residual change for every SPARC galaxy with F < 0.794, and the 3.93 variant.

## Checks (all must pass, else UNDECIDED, exit 1)

- **K0:** with F ≡ 1, the harness reproduces X43's committed SPARC rms on both footings and backgrounds to 1e-6.
- **K1:** F(X₀) → 1 for X₀ ≫ 1 and F(0.33) ≈ 0.80 (algebra). The exponential-disc peak is checked against quadrature.
- **K2:** peak RSS < 2 GB, single thread (X48 A4 is live).

MUTATE: the factor 4 → 8, with separate outputs. It must change the SPARC rms by more than 1e-4, otherwise the harness
is insensitive.
