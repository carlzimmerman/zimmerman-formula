# AS080 — Hydrostatic slope-temperature relation: derivation and audit

**Run:** `run_20260928T131319Z_as080_e004c2aa` · **Task:** `deepseek_push/astra_spawn_ideas/AS080_hydrostatic_slope_temperature_relation.md` (sha256 `1e353368ad08a4b9738a345bd17858170185ae7c48e505c77400fb19fdb627fd`) · **Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes subagent · **Outcome:** `supports_scoped_claim`

**Branch (declared):** Conditional deep-equilibrium sector — fixed logarithmic baryon well Φ = C ln r, isothermal EOS; Q / RAR / MU2 / EXP / MONO are *not* identified (deep-limit comparisons in §8 are explicitly branch-labeled; MONO is touched only where it equals RAR). All conclusions are conditional theorems with every premise listed.

Sources inspected (hashes match the pins in the seed and SOURCE_MANIFEST.json): `G084_maxentropy_law.py` (752999fd…), `G091_virial_triad.py` (8164360f…), `G233_eos_noscalar.py` (ad89298d…).

---

## 1. The precise claim, symbol dictionary, assumptions, boundary conditions

**Claim under audit (task §"Mathematics and principal test"):**

> dP/dr = −ρ·C/r **and** P = σ²·ρ **imply** γ = C/σ² — i.e. the density profile is the power law ρ(r) = A·(r/r_ref)^{−γ} with slope γ = C/σ², and **slope two requires σ² = C/2**.

**Symbol dictionary** (SI throughout):

| symbol | meaning | units | status |
|---|---|---|---|
| r | radius | m | independent variable, r > 0 |
| Φ | well potential Φ(r) = C·ln(r/r_ref) | m² s⁻² | assumed well (deep-regime potential; see §8 for its domain of validity) |
| C | well coefficient C = √(G_N·M_b·a0) = v_flat² | m² s⁻² | derived from inputs (dimension: √[(m³ kg⁻¹ s⁻²)(kg)(m s⁻²)] = m² s⁻² ✓) |
| G_N | Newtonian coupling 6.67430e-11 | m³ kg⁻¹ s⁻² | measured input; kept separate from G_bare / G_cosmo (never identified; the vacuum-density identities in §9 use G_cosmo conditionally) |
| M_b | baryonic mass (fiducial 6.5e10 M_sun, G031 MW proxy) | kg | observed input |
| a0 | framework scale (9.3619e-11 canonical / 1.1279e-10 alternative) | m s⁻² | framework input, κ = 1/2 adopted |
| r_M | = √(G_N M_b/a0), equipartition radius | m | derived |
| ρ(r) | mass density | kg m⁻³ | sought profile |
| P(r) | pressure | Pa = kg m⁻¹ s⁻² | P = σ² ρ |
| σ² | squared 1-D velocity dispersion (isothermal EOS coefficient) | m² s⁻² | **independently specified input** throughout §2–§7 (its value is *not* derived by the hydrostatic ODE; the conditional derivation of σ² = C/2 appears in §5 from an additional premise) |
| γ (gamma) | logarithmic slope γ = −d ln ρ/d ln r | dimensionless | derived γ = C/σ² |
| A | density normalization, A = ρ(r_ref)·r_ref^γ | kg m^(−3+γ) | single integration constant of the first-order ODE |
| r_ref | fixed reference radius (diagnostics: r_ref = r_M) | m | chosen fixed radius |
| r_in, R | shell boundaries, 0 < r_in ≤ r ≤ R | m | boundary conditions |

**Assumptions (every premise, explicit):**
1. **Hydrostatic balance** in the well: dP/dr = −ρ dΦ/dr = −ρ·C/r (signed radial form; Φ increases outward, force inward). ✓ sign: P decreases outward; d ln ρ/dr = −γ/r < 0.
2. **Isothermal (barotropic) EOS**: P = σ² ρ with σ² > 0 constant in r.
3. **Well**: Φ(r) = C ln(r/r_ref), C > 0, on a positive finite shell r_in ≤ r ≤ R, r_in > 0.
4. **Domain**: finite shell, no boundary conditions on ρ beyond normalization (first-order ODE ⇒ one integration constant A; A is the single density normalization, fixed by mass normalization — in the equilibrium sector by equipartition M_ph(<r_M) = M_b, i.e. A = C/(4πG_N), a framework input *not* derived here).
5. **Poisson consistency** (only in §5): ΔΦ = 4πG_N ρ — the well is sourced by the density itself.
6. No particle ontology, no dynamics, no attainment claim: the ODE is static; time-dependent formation/relaxation is outside this task (see §11).

**Framework inputs vs conclusions:** inputs — κ = 1/2, a0 (both footings), G_N, M_b, σ², the well ansatz; conclusions — the solution ρ = A(r/r_ref)^{−C/σ²} (exact), γ = C/σ² (exact), slope 2 ⟺ σ² = C/2 (exact), the Poisson-consistent selection of {γ = 2, A = C/(4πG_N), σ² = C/2} (§5, conditional), the deep-exterior kernel corrections with bounds (§8), the Newtonian-limit disjunction (§7).

---

## 2. Derivation of ρ(r) = A (r/r_ref)^{−C/σ²} and the slope-2 requirement

**Step 1 — eliminate P.** With P = σ²ρ (σ² constant):

σ² dρ/dr = −ρ C / r   ⇒   d ln ρ / d ln r = −C/σ².   (1)

**Step 2 — integrate** on (r_in, R), ρ(r_in) > 0:

ln ρ(r) − ln ρ(r_in) = −(C/σ²)·ln(r/r_in)
⇒ ρ(r) = ρ(r_in)·(r/r_in)^{−C/σ²} = **A·(r/r_ref)^{−γ}**,   γ := C/σ²,   A := ρ(r_in)·r_in^γ·r_ref^{−γ}.   (2)

A is the single density normalization; r_ref is any fixed reference radius (the two-parameter family (A, γ) reduces to one parameter once σ² is specified, since γ = C/σ²). Note γ is dimensionless: (m² s⁻²)/(m² s⁻²) = 1 ✓; ρ units: A·(dimensionless)^{−γ} ⇒ A carries kg m⁻³ ✓.

**Step 3 — slope two.** The logarithmic slope is γ by construction. Since C > 0 and σ² > 0:

γ = 2  ⟺  C/σ² = 2  ⟺  **σ² = C/2**.   (3)

So on the premises {hydrostatic balance, isothermal EOS, log well}, *slope two requires exactly σ² = C/2*; no other σ² produces slope 2. The map σ² ↦ γ is one-to-one (injective on σ² > 0), so the inference "measured slope s ⇒ σ² = C/s" is unique (verified, NC2).

**Units check of the ODE:** dP/dr ~ (kg m⁻¹ s⁻²)/m = kg m⁻² s⁻²; ρ·C/r ~ (kg m⁻³)(m² s⁻²)/m = kg m⁻² s⁻² ✓.

---

## 3. Scale factors, signs, leading neglected term

- **Signs:** dP/dr = −ρC/r < 0 (pressure decreases outward in the confining well); since σ² > 0, dρ/dr < 0; γ = C/σ² > 0, density falls as a positive power. Φ = C ln r rises outward; ΔΦ > 0 corresponds to the confining (logarithmic) potential of the flat-rotation well. All signs checked by substitution (P1a) and by the residual P2.
- **Scale factors:** the only scale in the ODE is the well coefficient C; r_ref is an *arbitrary* fixed radius (change of r_ref renormalizes A but not γ or any physical statement). The exponent is scale-free (dimensionless).
- **Domain of the power law as a *solution of the stated ODE*:** any shell with r_in > 0 (the solution is exact on every such shell — P2 measures residual 5.3e-51 at 50 digits). The *physical* domain of the well itself is the deep regime (below).
- **Leading neglected term when the log well is used as the deep approximation of a point-source kernel:** the actual kernels approach the well's gradient g = C/r only as r → ∞. On branch Q (algebraic): g_Q(r)·r/C = √(1 + (r_M/r)²) = 1 + ½(r_M/r)² − ⅛(r_M/r)⁴ + …; on RAR (= MONO in the deep regime, y = (r_M/r)² < y_star): g_RAR·r/C = t/(1−e^{−t}), t = r_M/r = 1 + ½t + (1/12)t² − (1/720)t⁴ + …; MU2: 1 + (3/8)t + O(t²); EXP: 1 + (1/4)t + O(t²). Quantified bounds in §8.

---

## 4. Independent checks (different representations, actual residuals)

| check | representation | result (actual residual) |
|---|---|---|
| P1a | symbolic substitution of (2) into (1) (sympy) | residual ≡ 0 exactly |
| P1b | sympy `dsolve` of (1) — independent integration path | general solution satisfies (1) symbolically ≡ 0 |
| P1c | slope table: σ² = C/2, C/3, C, 0.7C ⇒ γ = 2, 3, 1, 10/7 exactly | all exact (sympy) |
| P1d | Poisson consistency Δ(C ln r) = C/r²; 4πG_N·(C/4πG_N)r⁻² = C/r⁻²; solve for γ ⇒ γ* = 2 | exact |
| P1e | Newtonian profile ρ_N = exp(G_N M_b/(σ² r)) solves σ²ρ′ = −ρG_N M_b/r² | exact |
| P2 | **50-digit mpmath substitution on 6 fixture shells × 2 footings × 1201 pts (14 412 points)**: |σ²ρ′ + Cρ/r|/|Cρ/r| | max = **5.32e-51** |
| CC1 | analytic substitution, 12 interior fixtures (r_in/R = 0.01/0.1/0.5 × R/r_M = 0.62/1) × 2 footings, float64 | max = **1.3e-16 class (exact identity)**; finite-difference diagnostic on log grid shown for transparency |

P2 is the mandated independent representation (direct differentiation + substitution at high precision); the residual is not a Boolean — it is the measured maximum relative residual.

---

## 5. The slope-two selection is *not* made by the ODE: Poisson self-consistency

The ODE alone admits every positive slope (NC1: σ² = C/3 is a perfectly valid slope-3 solution of the *same* ODE). Slope 2 is selected only when the well is required to be sourced by its own density:

ΔΦ = 4πG_N ρ,   Φ = C ln r   ⇒   C/r² = 4πG_N·A·r^{−γ}   ∀ r
⇒   γ = 2 **and** A = C/(4πG_N)   ⇒   σ² = 2πG_N A = **C/2**.   (4)

This is the hydrostatic twin of the equilibrium chain in G084 (max entropy at fixed M, E ⇒ γ = C/σ²; virial + fluid closure ⇒ σ² = C/2, G091 V2b) and G233 C1 (σ² = 2πG A): here the temperature is *derived* from {hydrostatics, isothermal EOS, log well, the well sourced by the profile} — no virial theorem, no entropy functional enters. All four premises are explicit and conditional: e.g. in the full MONO field theory the well is not sourced this simply away from the deep limit, so this derivation of σ² = C/2 is **conditional on the log well** (its deep-domain status is quantified in §8). The equipartition amplitude A = C/(4πG_N) is *forced* by (4), not assumed, and σ² = C/2 follows with no further input. ✓ (P1d; Lean T4).

---

## 6. Controls (each capable of failing)

- **NC1 (negative control, mandatory):** σ² = C/3 inserted into the *same* ODE gives the *valid* slope-3 solution ρ = A(r/r_ref)⁻³ — the log-log fit on [0.1, 1] r_M returns fitted slope **3.000000000000**, not 2; likewise σ² = 0.7C ⇒ slope 10/7. A solver that forced γ = 2 would FAIL this control. (Both footings; fits are exact to 1e-12.)
- **NC2 (identifiability):** slope s ⇒ σ²_inferred = C/s recovers the input σ² for s = 2 (⇒ C/2) and s = 3 (⇒ C/3) to 1e-12. The hydrostatic map σ² → slope is injective on σ² > 0.
- **NC3 (deep-limit leading terms):** at t = r_M/r = 1e-3, 50-digit mpmath: Q δ/(t²/2) = 0.99999975 = 1 − t²/4 + O(t⁴); RAR δ/(t/2) = 1.00016667 = 1 + t/6 − t³/360 + O(t⁵) — the numerically measured deviations reproduce the closed Bernoulli-series coefficients to 1e-9 (no fit).
- **NC4 (Newtonian regime):** at r/r_M = 0.1 and 0.5 the power law's residual against the *Newtonian* hydrostatic ODE (σ²ρ′ = −ρG_N M_b/r²) is |(r/r_M)² − 1| = 0.99 and 0.75 — O(1), i.e. the power law is NOT a Newtonian solution; the exponential ρ ∝ exp(G_N M_b/(σ² r)) solves the Newtonian ODE exactly (sympy P1e; Lean T5). **The slope-temperature power law is a deep-regime statement; the Newtonian-limit profile is exponential.**
- **CC1 (interior fixtures):** r_in/R = 0.01/0.1/0.5 × R/r_M = 0.62/1 — exact substitution residual (≈1e-16, machine precision; 50-digit 5.3e-51 in P2). These fixtures are **controls of the imposed-log-well ansatz**, not point-source deep-MOND statements (§8).

The negative control (NC1) failed to fail in the honest sense — it genuinely produced the slope-3 solution; the controls that *did* expose structure are NC4 (the power law is not Newtonian) and the ansatz-fixture caveat of §8.

---

## 7. Domain catalogue

| domain | what holds exactly | what is only approximate / ansatz |
|---|---|---|
| r > 0, imposed well Φ = C ln r | the power law (2), γ = C/σ², slope-2 ⟺ σ² = C/2 | the well itself is an *ansatz* (the imposed-log-well fixture R ≤ r_M is not a controlled point-source deep-MOND domain) |
| deep exterior r ≫ r_M (point source) | the well gradient C/r is the asymptotic limit of Q, RAR, MU2, EXP, MONO(=RAR deep); corrections bounded in §8 | finite-r kernel corrections (branch-specific) |
| Newtonian regime r ≪ r_M | — | the log well is NOT the Newtonian potential; power law invalid (NC4) |
| full MONO with heat filter S | — | transfer needs the registered filter scale ξ for the point-source exterior (open dependency, §11) |

---

## 8. Deep exterior: full-kernel slope deviations (the seed's mandated check)

For the actual deep exterior we use separate shells r_in/r_M = 10 and 100 with R/r_in = 2 and 10 (both footings), integrating the *pointwise* logarithmic slope of the hydrostatic profile under the **actual kernels** (no imposed-well shortcut): d ln ρ/d ln r = −(1/σ²)·r·g_branch(r), where g_Q = (GM_b/r²)√(1+r²/r_M²), g_RAR = (GM_b/r²)ν((r_M/r)²), MU2/EXP solve their implicit equations (Newton iteration, residual < 5e-17). MONO = RAR identically in this regime (y = (r_M/r)² ≤ 0.01 < y_star ≈ 2.3374, where h_mono = h_RAR; the filter's residual scale dependence is the §11 dependency).

Deviations δ(r) = slope(r)/γ − 1 of the *true-kernel* slope from the log-well slope γ = C/σ²:

| shell (r_in/r_M, R/r_in) | Q (max\|δ\|) | RAR≡MONO (max\|δ\|) | MU2 (max\|δ\|) | EXP (max\|δ\|) |
|---|---|---|---|---|
| (10, 2) | 4.99e-3 | 5.08e-2 | 3.85e-2 | 2.58e-2 |
| (10, 10) | 4.99e-3 | 5.08e-2 | 3.85e-2 | 2.58e-2 |
| (100, 2) | 5.00e-5 | 5.01e-3 | 3.76e-3 | 2.51e-3 |
| (100, 10) | 5.00e-5 | 5.01e-3 | 3.76e-3 | 2.51e-3 |

(δ at the inner edge is the largest: e.g. RAR at 10 r_M: 5.083e-2; at 100 r_M: 5.008e-3; Q at 10 r_M: 4.988e-3, at 100 r_M: 5.000e-5. Both footings agree to printed precision — the ratios r/r_M and C/σ² are footing-independent at fixed M_b.)

**Statement:** the log-well slope γ = C/σ² holds at r ≥ 10 r_M to < 5.1% (RAR/MONO), < 3.9% (MU2), < 2.6% (EXP), < 0.5% (Q); at r ≥ 100 r_M to < 0.51% / 0.38% / 0.25% / 0.005%. The leading corrections are exactly (½)(r_M/r)² for Q and (½)(r_M/r) + (1/12)(r_M/r)² for RAR (verified to 1e-9 at 50 digits, NC3; Q's is quadratic, RAR's linear — the operative branch converges to the log slope only linearly in t = r_M/r).

---

## 9. Footings and registered numbers (canonical vs alternative, kept separate)

Fixed inputs: G_N = 6.67430e-11 m³ kg⁻¹ s⁻², c = 299792458 m/s, M_sun = 1.98847e30 kg, pc = 3.085677581491367e16 m; M_b = 6.5e10 M_sun (G031 MW proxy); κ = 1/2 adopted on both footings.

| quantity | canonical a0 = 9.3619e-11 m/s² | alternative a0 = 1.1279e-10 m/s² |
|---|---|---|
| C = √(G_N M_b a0) | 2.841849e10 m² s⁻² | 3.119280e10 m² s⁻² |
| σ = √(C/2) | 119.20 km/s (= registered 119.2, G031) | 124.89 km/s (= registered 124.9) |
| r_M | 9.8375 kpc | 8.9626 kpc |
| ρ_Lambda = 4a0²/(G_cosmo c²), κ = ½ fixed, G_cosmo = G_N assumed | 5.8444e-27 kg m⁻³ | 8.4831e-27 kg m⁻³ (×1.4515 at fixed κ) |
| κ_eff at fixed canonical ρ_Lambda | 0.5 | 0.60238840 |
| g(10 r_M) = C/(10 r_M) | 9.3619e-12 m s⁻² | 1.1279e-11 m s⁻² |
| g(100 r_M) | 9.3619e-13 m s⁻² | 1.1279e-12 m s⁻² |
| γ, σ²/C | 2, 1/2 (both footings) | 2, 1/2 |

The slope-temperature relation and slope-2 requirement are *footing-independent* (dimensionless); both footings carry the same γ = 2 at σ² = C/2. ρ_Lambda values cite G_cosmo separately from G_N: the hydrostatic sector contains only G_N; the vacuum-density identity is a conditional matching statement (G_cosmo = G_N assumed for the number).

---

## 10. Lean certificate

`as080_hydrostatic_slope.lean` compiles with `lake env lean` from `fable_independent_2026/lean_2026` (host 4.34.0-rc2): **exit 0, zero `sorry`, zero `sorryAx`**, all seven theorems' `#print axioms` ⊆ {propext, Classical.choice, Quot.sound}:

- **T1 `slope_two_iff`**: (C/σ² = 2 ⟺ σ² = C/2) — the slope-2 requirement, exactly as claimed.
- **T2 `powerlaw_deriv`**: d/dr[A(r/r_ref)^p] = p·A(r/r_ref)^p/r (real-power derivative via HasStrictDerivAt.rpow; the standard rpow-deriv lemma is missing from this build's oleans, so the strict chain-rule form is used).
- **T3 `hydrostatic_ode_solved`**: σ²·ρ′ = −C·ρ/r at p = −C/σ² — the substitution step, closed by T2.
- **T4 `log_well_deriv`, `poisson_amplitude`, `poisson_selects_temperature`**: d/dr(C ln r) = C/r; 4πG_N·(C/4πG_N)/r² = C/r² (the slope-2 amplitude sources the well); C/(C/2) = 2.
- **T5 `newtonian_exp_solves`**: σ²·d/dr[exp(G_N M_b/(σ²r))] = −G_N M_b·exp(G_N M_b/(σ²r))/r² — the Newtonian-limit exponential solves its ODE.

Named blockers (not certified in Lean; verified symbolically at 50 digits in the Python lane): the 3D radial Laplacian step Δ(C ln r) = C/r² (nested `deriv`-level extensionality — `deriv_congr` unavailable in this build's oleans; source-tree `hasStrictDerivAt_rpow_const_of_ne` also absent from the compiled cache), and the implicit-kernel transcendental deviations of §8.

---

## 11. Limitations, next unresolved implication, suggested followup

**Limitations (what this result does NOT establish):**
- The log well is the *deep-regime* potential; the interior fixtures (R ≤ r_M) test the historical imposed-log-well *ansatz* only and are not point-source deep-MOND statements (P3/§8 quantify the deep-exterior kernel corrections instead).
- σ² = C/2 is derived **conditionally** on {hydrostatic balance, isothermal EOS, log well, well sourced by its own density} (§5) — inside the full MONO field theory, away from the deep limit and with the heat filter, the source relation differs; the equilibrium temperature input of the equilibrium sector (G084/G091) remains the registered input there.
- No dynamics/attainment: the profile is a static equilibrium; relaxation to it is a separate obligation (G035's kill and G081's marginal-mode verdict stand).
- The filtered-MONO transfer is NOT established: the heat-filter scale ξ for the point-source deep exterior is not registered in the equilibrium sources; the §8 bounds are for the unfiltered kernels (MONO = RAR deep, unfiltered).
- No new empirical test, no fit; a0, κ, M_b, G_N remain inputs.

**Strongest surviving statement (scoped claim):** On the fixed logarithmic well Φ = C ln r with C = √(G_N M_b a0) > 0, for every positive finite shell r_in ≤ r ≤ R (r_in > 0), the premises {dP/dr = −ρC/r; P = σ²ρ, σ² > 0} are solved exactly and uniquely (given ρ(r_in)) by ρ(r) = A(r/r_ref)^{−γ} with γ = C/σ²; γ = 2 ⟺ σ² = C/2 (Lean T1–T3, substitution residual 5.3e-51 at 50 digits); adding Poisson self-consistency selects γ = 2, A = C/(4πG_N), σ² = C/2 (P1d, T4). In the point-source deep exterior (r ≥ 10 r_M) the log well is the exact asymptotic potential of Q/RAR/MU2/EXP/MONO with branch-specific slope deviations bounded by §8 (< 5.1% at 10 r_M, < 0.51% at 100 r_M, RAR/MONO; exact leading coefficients verified to 1e-9). In the Newtonian regime the equilibrium profile is exponential, not a power law (NC4, T5).

**Next unresolved implication:** the filtered-MONO deep-exterior hydrostatic profile — the slope-temperature relation's transfer to the operative target needs (a) the registered heat-filter scale ξ for the point-source static exterior, and (b) the bound on the filtered acceleration's deviation ⟨S*nu(Sφ)⟩ from C/r at r ≥ 10 r_M. Until then, the equilibrium sector's σ² = C/2 remains conditional on the imposed log well in the interior and exact only asymptotically (to the §8 errors) in the deep exterior.

**Suggested followup (child spec AS080.C01):** derive F_ξ(r) := |r·g_MONO_filtered(r)/C − 1| on the same deep shells for the registered ξ (once it is pinned from the field-theory sources), and close the transfer bound; a second spec (AS080.C02) targets the interior transition: match the power-law equilibrium to the actual kernel at r/r_M ≲ 1 and quantify the interior slope deviation from 2 — the correction to the equilibrium sector's density slope in the transition region.

---

**Files in this run dir:** `derivation.md`, `result.json`, `as080_hydrostatic_slope.py`, `as080_supervised.py`, `as080_hydrostatic_slope.lean`, `as080_residuals.json`, `as080_bounds.json`, `raw_output.txt`, `lean_check.out`, `err_and_time.txt`, `supervise_out.txt`, `lean_probes/`. All hashes in `result.json` §artifacts_sha256. Prototype bounds: wall 0.76–0.92 s (supervised hard cap 120 s), max RSS ≈ 87 MB (supervised 512 MB cap), 1 thread — see `as080_bounds.json` for the enforcement mechanism (macOS forbids lowering RLIMIT_AS; RSS polling + SIGKILL used instead, mechanism recorded).
