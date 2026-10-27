# X51_dwarf_cooling_floor — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** X49 found that route-E a₀-floor halos fit four of five LG dwarf classes. The MW ultra-faints fall short (Z
+3.8), and their halo masses come from EM1's SPARC relation extrapolated to M200 ≈ 5×10⁵ M☉. A galaxy can only form in a
halo whose gas can cool. **Does the first-principles cooling threshold, used as a floor on the halo mass, close the
ultra-faints without breaking the other classes?**

Standing rules: κ = ½ FITTED. Footings never pooled. Route E, Newtonian, a₀-floor Burkert halos exactly as X49. Cold dark
energy is not matter. No ΛCDM stellar-to-halo relation. Not "theory closed". Nothing here may say the data favour the
framework.

## 1. The rule

    M200 = max( M_EM1(M_b),  M_cool )

- **M_cool (PRIMARY):** the halo mass whose virial temperature is T_vir = 10⁴ K (atomic hydrogen cooling) at
  z_form = 8 (UFDs are reionization-era fossils).
  - T_vir = μ m_p V_c² / (2 k_B), with μ = 0.59 (ionized, primordial), V_c² = G M / r_vir, and
    r_vir = [3M / (4π · 18π² ρ_m(z))]^{1/3}.
  - ρ_m(z) uses the record's background A (h, Ω_m from F3's refit).
  - Every dwarf class gets the same floor. It is a formation threshold, not a fit.
- **Reported variants:** H₂ cooling, T_vir = 2×10³ K with μ = 1.22 (neutral), at z = 8; and atomic cooling at z = 6
  and z = 10.
- Everything else is X49's code: data, binary correction, Burkert floor solver, g_pred, and the per-class bootstrap. The
  only change is M200.

## 2. Verdict (per footing; both must agree)

- **COOLING FLOOR FITS THE DWARFS** if all five classes are REPRODUCED (|Z| < 2), as X49's rule.
- Otherwise **FAIL: <classes with sign>**.
- Reported: M_cool, how many systems the floor lifts (M_cool > M_EM1), Spearman(E, log M★), and the individual systems.

## 3. Checks (all must pass; `--mutate` must fail K1)

- **K0:** with the floor switched off, X49's class medians are reproduced to 1e-9.
- **K1:** T_vir(M_cool, z = 8) = 10⁴ K to 1e-8, by root solve and re-evaluation.
- **K2:** M_cool(z) falls with z as (1 + z)^{−3/2} to 1e-6 (the analytic scaling), checked between z = 6 and 10.
- **K3:** peak RSS < 1 GB; seconds.
- **MUTATE:** μ = 0.059 (a factor 10 low); K1 must fail.
