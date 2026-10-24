# X23_late_heating_graded — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** X22 (5c7114f508) found one gravitationally consistent window: universal late heating. The cold component is
cold through z = 2–3 and has c_s,need = 190.0 / 201.3 km/s today. X22's README states that "clusters, hosted dwarfs and
low-z lensing under late heating are not graded". Graded with X22's own profile at X22's own c_s,need, with nothing
chosen here, does late heating reproduce the required-extra pattern of X19's classes and of the hosted dwarfs one by one?

Standing rules: κ = ½ FITTED. Footings canonical / alt, never pooled. The cold component is field mass, never a particle.
No knob: c_s is read from X22's JSON (`step2.per_footing.<f>.cs_need_kms`), never tuned. Not "theory closed". Nothing here
may say the data favour the framework. Low-z lensing is not graded here (named, not done).

## 1. The model (X22's, copied verbatim)

- Hydrostatic isothermal content in a flat well: M_c(<r) = 5.364 M_b · (1/δ_ta) · 3/(3 − β) · (min(r/r_ta, 1))^{3−β},
  β = V²/c_s², β capped at 2.9 (X22's BCAP). δ_ta = 5.55. r_ta = [3 (Ω_m/Ω_b) M_b / (4π δ_ta ρ̄_m)]^{1/3}. X22's
  CFG946 constants.
- V for a class or system is √2 σ (X19's convention for rotators, σ = V/√2; isothermal V_c² = 2σ² for pressure-supported
  systems). For hosted dwarfs σ is the observed σ, which already contains the extra. This is favourable to retention.
- The cold mass enters as X22 does (X6 d2): g_pred = ν(g_N + g_c)·(g_N + g_c), with ν of μ = x/(1+x) at each footing's a₀.
  The baseline is g_iso = ν(g_N) g_N (B_iso). **E_pred = log₁₀(g_pred / g_iso).**
- Classes at the β cap are **CAPTURED** (the isothermal well cannot hold the component hydrostatically). They are graded
  at the cap (X22's convention), and the label carries the flag.

## 2. Inputs

- **Class table:** X19 JSON (`intervals["<f>|p16_84"][class]`, medians for M_b, σ, ρ_b and x; `E_table["<f>|iso"]` for E
  and s; `per_footing_class` labels). Measurement radius from the medians: g_N = x a₀, r = 3 g_N / (4π G ρ_b),
  M_b(<r) = g_N r² / G, r_ta from the class median M_b. Cosmic background: not graded by this formula (late heating is
  cold before z ≈ 2 by X22's construction).
- **Hosted dwarfs, per system:** X1 `x1_per_system.csv`, the 61 systems of X19's three hosted EXTRA classes. M_b = 10^logMstar
  (Υ_V = 2), r₁₂ = (4/3) rh, g_N = G (M_b/2)/r₁₂², E and s from `Delta[iso AQUAL L*0]` and its sdMC, σ from `sigma`.

## 3. Grading (per footing)

- Residual Z_res = (E_obs − E_pred)/s.
- A class is **REPRODUCED** iff |Z_res| < 2.
- Decisive classes are X19's L-S EXTRA and NONE classes on that footing (the background excluded). AMBIGUOUS classes are
  reported.
- Hosted dwarfs, per system (reported, plus one verdict line): the fraction of the 61 systems with E_pred ≥ E_obs − 2s.
  Also the median E_pred.

## 4. Verdict (both footings must agree)

- **LATE HEATING REPRODUCES THE PATTERN** — every decisive class is REPRODUCED.
- **LATE HEATING FAILS: <classes>** — at least one decisive class has |Z_res| ≥ 2. The failing classes are listed with
  their sign: UNDER means the extra is missing, OVER means too much.
- **UNDECIDED** — the footings disagree in class.

## 5. Checks (all must pass; `--mutate` must fail K0)

- **K0:** c_s,need read equals 190.014 / 201.315 km/s to 0.01. The class E and labels read equal X19's printed values
  (SPARC small −0.046, MW ultra-faint +0.625 canonical; the label sets as printed in X19's .out).
- **K1:** at c_s → ∞ (β → 0), E_pred → log₁₀ of the uniform-density content (the analytic limit), to 1e-10, for one
  class. At c_s → 0, every class is CAPTURED.
- **K2:** the closed-form M_c equals the quadrature of 4πr²ρ to 1e-8 (X22's C4, three β values).
- **K3:** peak RSS < 1 GB.
- **MUTATE:** c_s,need × 2 is read; K0 must fail.
