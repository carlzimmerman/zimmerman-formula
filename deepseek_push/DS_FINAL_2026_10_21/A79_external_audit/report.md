# A79 — external proposal, audited. VERDICT: REFUTED (not committable as a passing lane)

**Provenance:** supplied by an external assistant ("google argon") on 2026-10-22 as a self-contained
`A79_final_synthesis/` package claiming **20/20 checks PASS** and a reproducible table of **8 mutations**.
Nothing here was written by the repo's own lanes. This directory records the audit; **the code is stored
verbatim as `a79_as_submitted.py` for the record, and is not adopted.**

**Headline: the claim is false on its own terms.** The clean run is **12/20, exit 1.** The claimed mutation
table (15/15/19/18/19/19/18/18 passes) is not reproducible either: the actual sweep is 11/11/12/10/11/11/10/10.

```
$ python3 a79_as_submitted.py
[FAIL] K1  a0_thermal_value          val=1.372526e-11  ref=8.61968e-11   err=8.41e-01
[FAIL] K2  kappa_DE_Z_over_4pi       val=0.07331614    ref=0.4606589     err=8.41e-01
[FAIL] K3  horizon_solid_angle_4pi   val=78.95684      ref=12.56637      err=5.28e+00
[FAIL] K4  thermal_vs_A71_sigma      val=2.62691  < bound=0.05
[FAIL] K9  Lstar_thermal_in_window   val=159.6241      ref=25.437        err=5.28e+00
[FAIL] K10 Rcore_both_within_1sigma  val=37.6607  < bound=0.5
[FAIL] K13 transverse_lambda_eta_kpc val=4115.469      ref=581.9         err=6.07e+00
[FAIL] K17 sersic_inner_lens         val=0.06965086    ref=0.0647        err=7.65e-02 > 5e-02
A79 SUMMARY: 12/20 checks PASS (MUTATE=NONE).   exit 1
```

---

## Defect 1 (fatal, 7 checks): the thermal wavelength carries an extra 2π

A72's derivation uses the **reduced** thermal wavelength, `λ = ħc/(k_B T_dS)`, which at
`T_dS = ħH_Λ/(2πk_B)` equals `2πR_Λ` and gives `a₀ = c²/λ = cH_Λ/(2π) = 8.62×10⁻¹¹`.

The submitted code writes `lambda_T_dS = (2π ħ c)/(k_B T_dS)` — the **full** `hc/kT` — which is `4π²R_Λ`,
so it returns `a₀ = cH_Λ/(4π²) = 1.3725×10⁻¹¹`, low by exactly **2π** (8.61968/1.372526 = 6.28016). Every
downstream thermal quantity then fails: κ = 0.0733 instead of 0.4607, the solid-angle ratio 78.96 instead of
4π, `L★` = 159.6 pc instead of 25.44, and the core pull 37.7σ instead of <0.5σ.

**This is the one genuinely useful by-product of the audit**: the two conventions are not interchangeable, and
the data pick one. The full-wavelength branch gives `a₀ = 1.3725×10⁻¹¹`, which is **2.63σ** from A71's
`8.544 ± 2.730×10⁻¹¹`. The reduced branch is `0.03σ` away. So the thermal-wavelength identification is not a
free convention — it is fixed by the fit. (Folded into `THEORY.md` §3.6.)

## Defect 2 (K5): the "H₀–κ degeneracy lock" is arithmetic, not physics

K5 asserts that `κ = 0.4607` at `H₀ = 73.0` "matches" `κ = ½` at `H₀ = 67.4` to 0.2%. It does — because
`0.460659 × 73/67.4 = 0.498933`, i.e. the "lock" is the coincidence `0.5/κ_DE = 1.08540` vs `73/67.4 =
1.08309`. κ is a fixed theory number and H₀ is a measurement; **nothing trades one for the other.** This is
precisely the class of construction A73 tested and killed with a 260,129-form look-elsewhere pool
(`P(≥1) = 1.000000`). It is not a check of anything.

## Defect 3 (K18): built on the exact artifact A78 corrected — and assigns a 12–20σ excluded footing

K18 computes `β = (2Ω_Λ·ratio − 2)/3`, which is **A33's vacuum-only relation** (`ρ_m` dropped). A78 showed
this is the artifact: with matter included, `β = 0` sits *exactly* at `Λ_bare = Λ_obs`, and the relation is
`2 + 3β = 2(Ω_Λ·ratio + Ω_m)`. Inverting both at the code's own `ratio = 2.189`:

| relation | β | ΔN_eff | vs BBN bound 0.30 |
|---|---|---|---|
| A33 vacuum-only (as coded) | +0.3325 | −3.716 | **12.4×** |
| A78 matter-inclusive (correct) | +0.5427 | −6.064 | **20.2×** |

So K18's "β > 0, healthy" state is a footing **excluded at 12–20× the BBN bound** — and its mutation
`beta_ghost` (ratio → 1.0) is built on the same wrong relation, since ratio = 1.0 is where β = 0 under the
correct one, not where β = −0.211.

Worse, the accompanying assertion `dg/dβ == 0` is **vacuous**: the expression differentiated is
`g²/(g + a₀)`, which contains no β at all, so sympy returns 0 by construction. The actual β-carrying object is
`Z = K(2+3β)/β + ηp²`, whose derivative is `−2/β²`, not 0.

## Defect 4 (K12, K14): re-asserts the γ/η closure A77 refuted

K12 grades `γ/η = (σ_c/c)² = 7.52×10⁻¹⁰ < 1.916×10⁻⁷` as PASS. That identification was tested and refuted by
A77 (40/40) two ways: (i) `c_T² = γ/η` is a stiffness/inertia ratio, not `dP/dρ` — they coincide only if
`ηρ_c = 1`, and the identification needs `ηρ_c = 7.5×10⁻⁹`, off by 1.34×10⁸; (ii) equipartition gives
`3k_BT_dS/m_P = 2.764σ_c²` → 13.84 km/s, not 8.33, predicting κ = 1.144 — 6.5σ excluded. Passing A69's
one-sided bound by 248× discriminates nothing.

## Defect 5 (K17): right physics, wrong check — the one salvageable idea

K17 computes the Sérsic-index boost to the inner-lens enclosed mass: n = 5.8 vs 4.0 at `R < 0.3 R_e` gives
**+0.06965 dex = +17.4 %**. A70's surviving shape residual is **+0.172 ± 0.060 (17.2 %, 2.9σ)**. The magnitudes
**match** — a steeper Sérsic index supplies almost exactly the inner mass A70 needed. But (i) the check fails
its own 5 % tolerance (7.65 % error), and (ii) `n = 5.8` is *assumed*: the catalogue has no Sérsic column, so
this is a consistency observation, not a resolution. It should be re-run with n measured or marginalized.

## Design flaw: the headline and the closure block don't talk

K19/K20 pass (`8π/κ² = 12π²`, `y_t = 77.85`) because they use the **closed-form** `κ_DE = Z/4π`, not the
`a₀` the lane computed. So the lane's headline number (the thermal `a₀`) and its closure verification are
decoupled — the closure passes while the `a₀` that is supposed to imply it fails by 2π.

## Minor

- Dead code: `record_check("K7", …) if False else None`.
- K11 checks the elastic sound speed at an explicit `L★ = 24.025 pc`, inconsistent with the lane's own
  `L★ = 159.6 pc`.
- K7's comment claims "~1.08e8" while its value is 1.33e9.
- `sp.Subs(...)` is a sympy class instantiation, not substitution.

---

## What survives

1. **The λ convention is fixed by the data** — the full-wavelength branch is 2.63σ out, the reduced branch
   0.03σ. Worth stating explicitly in THEORY (done, §3.6).
2. **The Sérsic n ≈ 5.8 route to A70's inner-lens residual** (+17.4 % vs +17.2 %) — a real, testable
   consistency, currently limited by the missing `n` column.

Everything else is either already in the record (A72/A73/A77/A78) or contradicted by it. **No part of A79 is
adopted as evidence.**
