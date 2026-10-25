# DF1_dwarf_floor_origin — FROZEN CRITERIA (committed alone, before any script; POST-HOC on disclosed numbers, see §7)

**Question.** Faint, gas-poor, pressure-supported dwarfs carry +0.2 to +0.6 dex more pull than the isolated law. The record
describes this extra as a velocity floor, σ² = σ_iso² + c₀² (X24: c₀ 4.59 / 4.05 km/s from the field dwarfs). Its
cross-system form is g_floor ∝ r₁₂^(−n) with n = 0.78 [0.73, 0.83] / 0.80 [0.75, 0.85] (X28). It is mass-driven, not
host-driven (X24), not in the action (X25), and not a₀-scaled (X28). **Is there a physical origin whose shape (the exponent
n and/or the stellar-mass dependence) follows from named physics, with no fitted shape constant?** Each candidate is graded
on the record's dwarf tables, and each gets a verdict. "None survive" is an allowed outcome.

Standing rules: κ = ½ FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², scored separately, never pooled. No
dark-matter particle (a candidate that needs a new particle species is dropped at screening). No knob scans: each candidate
has its shape fixed in advance and at most one normalization, calibrated on the 13 LG field dwarfs only (the class X24 and
X28 calibrate on). Not "theory closed". Nothing here may say the data favour the framework or ΛCDM. MUTATE writes separate
outputs. Light compute only (one thread, < 1 GB).

## 1. Screening (done before freezing; record checks cited)

| # | idea | predicted shape | record check | kept? |
|---|---|---|---|---|
| S1 | **Polytropic cold medium, named equations of state** (P = Kρ^Γ, hydrostatic, extra component fills the stars' radius) | self-similar: c_s² ~ g r and ρ ~ g/(G r) give **g_x ∝ r^(−Γ/(2−Γ))**, so n = Γ/(2−Γ), m = 0 | Γ = 2 (contact-interaction BEC / tethered medium, n → ∞, fixed radius) is v3s γ_L: X25 wrong sign, not regraded. Γ = 1 is X24's floor in form. Γ = 0 is X28's F_g in form, but here its normalization is a medium constant, not η a₀ | **KEEP** Γ = 0 (Chaplygin / generalized-Chaplygin unified dark fluid at α → 0, logatrope; also Burgers turbulence), Γ = 1 (isothermal), Γ = 4/3, Γ = 5/3 (adiabatic ideal fluid) |
| S2 | **Kolmogorov cascade in a turbulent cold medium** (universal energy flux ε) | σ_x² ∝ (ε r)^(2/3): **n = 1/3**, m = 0 | not in the record | **KEEP** |
| S3 | **Self-similar secondary infall of cold energy onto each dwarf's baryonic seed** (Bertschinger / Fillmore–Goldreich, point seed) | ρ ∝ r^(−9/4), M_x(<r) ∝ M_seed^(3/4) r^(3/4): **n = 5/4, m = 3/4** | CFG872 excluded clump mass ∝ M★¹ (s = 1); infall is a different law (3/4, and r-dependent). CFG934/937 used virial cooling-floor halos, not infall profiles | **KEEP** |
| S4 | **Remnant-loaded stellar mass (IMF / Υ trend)**: unseen stellar remnants raise Υ in low-mass, metal-poor dwarfs | E = s·log₁₀ F, s = local slope d log g_law / d log g_bar; bound F ≤ 2 (the record's Υ_V range 1–4 around 2, X1 B4) | X31 closed gas loss, age and feedback, not the IMF | **KEEP** (bound-limited) |
| S5 | Two-body relaxation, mass segregation, expansion (stars as the only mass) | none in equilibrium | **Deep-law virial theorem**: for an isolated deep-regime system the mass-weighted σ² = (2/9)√(G M a₀) depends on M only. Internal redistribution at fixed M cannot change E | drop |
| S6 | Heating by passing perturbers (granular cold energy, substructure) | none in equilibrium | same theorem, and the system re-virializes; disequilibrium closed by X20/X25 | drop |
| S7 | Ambient-pressure confinement | — | stars are collisionless: pressure confines gas, not a stellar system | drop |
| S8 | Quantum (de Broglie) pressure of a light field (soliton cores) | M r = const: n = 3 | needs a particle mass (standing rule) | drop |
| S9 | Standard-model neutrinos (Σm ≈ 0.06 eV) | — | Tremaine–Gunn ceiling at σ = 5 km/s: ρ_max = g m⁴ (2πσ²)^(3/2) / h³ ≈ 3e-17 M☉ pc⁻³ for m = 0.06 eV, g = 2, against ~0.1 needed (16 orders of magnitude short) | drop |
| S10 | Unseen warm gas retained | — | X31 (gas); c_s(1e4 K) ≈ 10 km/s exceeds faint-dwarf binding (CFG937 filtering) | drop |
| S11 | Law-boosted isothermal clump (n = 1/2) | — | CFG888: no record formulation lets cold energy feed the law | drop |
| S12 | Any function of g_bar alone (for example a changed deep-regime slope) | — | X20: Σ and x order the extra at 2.8σ against M★ / r_half at 6.8σ; X28 acceleration form loses by Δχ² 110 / 195 | drop |
| — | tides, binaries, gas / age / feedback, γ_L, a₀-scaled floor, universal clump σ, cooling floor, √(a₀L★/3) | | closed by the brief | not redone |
| — | dark-energy heater | | sibling lane DH1 | not done here |

## 2. Data (read only)

X1 `x1_per_system.csv`, per footing, built exactly as X28 builds it (`load()`):
- E = `Delta[iso AQUAL L*0]`, s = its sdMC; σ_c = `sigma` × b (Arroyo-Polonio free-f ratio where matched; the median ratio
  for unmatched M_V > −7.7; else 1); σ_iso = σ_c 10^(−E/2); r₁₂ = (4/3) r_h; g_iso = 3σ_iso²/r₁₂.
- Classes: `LG field` (13, calibration only); graded H = `MW ultra-faint` (31), `bright M31` (25), `M31 others` (5);
  `MW classical` (8, graded, reported class). ALL = H ∪ MW classical ∪ field = 82 systems (X28's power-law set).
- M★ = 10^`logMstar` (M☉). Crater II and Antlia II reported individually.

## 3. Candidate forms

Power-law candidates: g_x = A a₀ (r₁₂ / 100 pc)^(−n) (M★ / 1e5 M☉)^m and **E_pred = log₁₀(1 + g_x / g_iso)** (X28's
convention). Shapes (n, m) are fixed: P0 (0, 0); P1 (1, 0); P4/3 (2, 0); P5/3 (5, 0); TK (1/3, 0); SI (5/4, 3/4).

IMF candidate: E_pred = s_i log₁₀ F, with s_i = 1 + d ln ν / d ln y of the simple ν = ½ + √(¼ + 1/y), evaluated at the
y where ν equals the system's own law boost ν_i = 10^(Delta[Newton] − Delta[iso]) (ν_i ≤ 1 → s_i = 1).

Normalization (A or F) is a bounded scalar search, log₁₀ A ∈ [−12, 6], F ∈ [1, 1000].

## 4. Tests

**T1 shape (verdict-bearing).** On ALL (82): the reference is the free power law, profiled over A on a grid
n ∈ [−1, 6] (step 0.02) × m ∈ [−1, 1.5] (step 0.02), then polished by Nelder–Mead. χ²_ref is its minimum. For each
candidate, χ²_c is its minimum over its single normalization on ALL. **Δχ²_shape = χ²_c − χ²_ref. T1 PASS if ≤ 5.99**
(95 %, two shape parameters). Reported: the m = 0 interval of n at Δχ² = 1 and 4, the 2-D best (n, m), and the
polytropic index the data imply, Γ_data = 2n/(1 + n).

**T2 out of sample (verdict-bearing).** The normalization is calibrated on the 13 field dwarfs. Graded on each H class
and MW classical: median residual E − E_pred, bootstrap sd (10 000 draws, seed 20261024, E_i ~ N(E_i, s_i), as X28), Z.
χ²_H against the law (A = 0) and against X24's floor (P1, the benchmark). **T2 PASS if |Z| < 2 for all three H classes and
χ²_H < χ²_H(law).**

**T3 physical normalization (verdict-bearing where defined).**
- P0 (Chaplygin-type, c_s² = C/ρ): from the field-calibrated g_x (constant), C = c_s² ρ_x = g_x²/(6πG), using
  c_s² = g_x r/3 and ρ_x = g_x(2 − n)/(4πG r). At forest densities this medium has c_s = √(C/ρ). **VIOLATED** if
  c_s > 13 km/s (X22's most lenient gate) at z = 3, overdensity 10, with ρ̄_c = Ω_c ρ_crit (1+z)³, Ω_c = 0.3085 × 5.364 /
  6.364, h = 0.6856 (CFG682 / CFG886 values).
- P1, P4/3, P5/3: c_s at forest densities is ≤ its dwarf value (Γ ≥ 1), so the gate cannot be violated by them: PASS by
  construction (the P1 value, c₀, is printed against 6–13 km/s).
- IMF: required F per system F_req = 10^(E_i/s_i). **VIOLATED** if, for any H class, median F_req − 2 > 2 × its bootstrap sd.
- TK, SI: no fixed-physics normalization; T3 not defined (NA). The implied ε (TK) and the implied mass inside 100 pc for a
  1e5 M☉ seed (SI) are printed only.

**T4 rotating discs (verdict-bearing).** ΔE = log₁₀(1 + g_x/g_obs) with the field-calibrated form at two SPARC-like points:
V = 30 km/s at R = 2 kpc and V = 100 km/s at R = 10 kpc, M = V⁴/(G a₀) for the M★ term (IMF: ΔE = s log₁₀ F at the y that
solves ν(y) y a₀ = V²/R). Tag [SPARC-COST] if ΔE > 0.05 dex at either point; **T4 FAIL if ΔE > 0.10 dex** at either point.

## 5. Verdicts

Per candidate and footing:
- **RULED OUT** if T1 fails or T3 is VIOLATED.
- **SURVIVES** if T1, T2 and T4 pass and T3 is PASS or NA.
- **PARTIAL** otherwise.

Per candidate: the class if both footings agree, else UNDECIDED (footings disagree). **Lane: SURVIVOR(S) = the candidates
that SURVIVE on both footings; "NONE SURVIVE" if there is none.** Crater II and Antlia II predictions are reported, no weight.

## 6. Checks (all must pass in the plain run; MUTATE must fail K0)

- **K0** X28 reproduced with X28's own m = 0 method (grid n ∈ [−0.5, 1.5], 201 points, A ∈ [0, 5]): n = 0.78 / 0.80, 68 %
  [0.73, 0.83] / [0.75, 0.85], to 0.011; and P1's field calibration as c₀ = √(A a₀ · 100 pc / 3) equals X24's c₀ to 0.01 km/s.
- **K1** P1's χ²_H equals X28's F_v χ²_H (217.0 / 194.8) to 0.1.
- **K2** positive control: E synthesised from TK at its ALL-calibrated A plus N(0, s_i) noise; T1 must PASS TK on it.
  (Whether T1 would then reject P1 is reported as power.)
- **K3** nesting: χ²_ref ≤ χ²_c for every power-law candidate (1e-6).
- **K4** peak RSS < 1 GB.
- **MUTATE** (`DF1_MUTATE=1`): r₁₂ is permuted across the 82 systems in the g_x term only (seed 20261025); E and g_iso
  untouched. K0 must fail. Outputs `*_MUTATE.*`.

## 7. Disclosure (post-hoc)

The X24 and X28 summary numbers (c₀, n and its interval, class residuals, χ²_H) were read in their READMEs before freezing.
No per-system number was printed or fitted in this lane before freezing. The polytrope mapping n = Γ/(2 − Γ), and the
observation that n ≈ 0.8 sits between Γ = 0 and Γ = 1, were worked out by hand from the published n. So the ladder is graded
with the target known. The candidates' shapes come from named physics, not from the data, and no Γ is fitted. A survivor
would be a lead, not a confirmation.
