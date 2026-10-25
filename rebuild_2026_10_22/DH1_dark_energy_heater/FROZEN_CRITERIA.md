# DH1_dark_energy_heater: frozen criteria (committed alone, before any script or number)

κ = ½ FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s², reported separately, never pooled. The cold component
is cold dark energy (gravitating field component, w ≈ 0; never matter, never a particle). No knob is fitted or scanned. Not
"theory closed". Nothing here says the data favour the framework or ΛCDM. Light compute only (sympy + closed forms, one
thread, < 1 GB).

## 0. Question

Is there an action term, keyed to dark energy and carrying no fitted coefficient, that turns the cold sector from a
collisionless single-stream dust (z ≳ 2) into a collisionless hot state with σ ≈ 550–770 km/s in KT clusters today
(COLD_SECTOR_SPEC R1–R7, §2)? Or is there a structural obstruction?

## 1. Record check (done before this file; see ASSUMPTION_LEDGER §3)

Closed and not redone: single-temperature universal heating (X23_late_heated_cold, X26 A3), vacuum heating
Q = ε H ρ_Λ c² (X24b), the isothermal sheet profile (X30), σ = c_s collisionless in the Bullet (X32). Related record items
that are not the same question: CFG958 (cold↔vacuum exchange that books energy; no heating law), CFG741 (P-wave heating,
Q ≤ 0.50), CFG742 (constant warm component), CFG643 (baryon→cold heat exchange), PH1 D5 (multi-stream never returns to
single-stream; the reverse direction of L1 below), sol61 kinetic_support (waterbag support, no heating). No record lane
states the Liouville/rescaling obstruction for a homogeneous driver, the wave-field adiabatic bound, or the f = ρ_DE/ρ_m
timing exponent.

## 2. Candidates (frozen list; each must say why it escapes X23, X24b, X30, X32)

| id | heater | structural difference from the closed forms |
|---|---|---|
| H1 | ratio-rate heater, per unit mass: dε_th/dt = ε c² d(ρ_DE/ρ_m)/dt with background ρ_m | universal in space (q = 0), unlike X24b (per mass ∝ 1/ρ, q = −1); rate tied to the DE/matter ratio, unlike X23 (no time law) |
| H1L | same, with local ρ_m | sign set by local collapse |
| H2 | coherent coupled-DE drive (inertia or anti-friction keyed to a DE background, v̇ = −(H − Γ_DE(t)) v − ∇Φ) | multiplicative on existing velocities, not additive heat |
| H3 | epoch trigger at a knob-free DE epoch (ä = 0; Ω_Λ = Ω_m; Milgrom crossing a₀ = cH/2π) releasing a latent specific energy homogeneously | step in time (any p), not a power law |
| H4 | a₀-triggered local phase change, keyed on g < a₀(z) | acceleration key, not a time or density key |
| H5 | wave-field (incoherent-mode) heating of a cold wave medium by a DE driver of rate Γ ≤ 3H | kinetic dispersion from mode excitation, not fluid heat |
| H6 | random kick field released at a DE epoch: σ² = σ_well² + v_k² | additive quadrature floor, outside X26's multiplicative family |

## 3. Gates (graded per candidate, per footing)

- **G1 KNOB.** The amplitude follows from the action with no fitted coefficient. FAIL if the candidate needs a
  dimensionless coefficient ε (or an exponent, threshold, length or velocity) that the action does not fix. Reported: the
  ε range the record's numbers require, and the natural (ε = O(1)) outcome.
- **G2 TIME.** With today's cosmic c_s set to the most forgiving value that passes R3 (X22 c_s,need 190.014 / 201.315 km/s),
  the candidate's derived time law must give c_s(z = 3) ≤ X22's p = 3 value (5.938 / 6.291 km/s) AND c_s(z = 2) ≤ X22's
  p = 3 value (12.189 / 12.914 km/s). These are the record's edge of "not FAIL" (X22 p = 3 is UNDECIDED-in-window; p = 2 is
  FAIL). Equal or below: PASS (edge). Above: FAIL.
- **G3 KINETIC (R6).** The candidate must produce a collisionless velocity dispersion in a medium that is single-stream at
  z ≳ 2, from the action's own dynamics, not a pressure. FAIL if the derived dispersion is zero, or is only a rescaling of
  gravitationally generated dispersion, or is bounded below the need (SPARC quadrature need √(c_s,need² − σ_SPARC²)).
- **G4 SPLIT.** The derived dependence of today's c_s on the system must satisfy, at once:
  - KT clusters: c_s/σ_KT inside X26's sheet range at the KT median (556–736 / 595–761 km/s over σ = 517.1 km/s);
  - SPARC: c_s ≥ c_s,need at the SPARC median (σ = 70.5 km/s; X22);
  - cosmic medium: c_s,cos today ≤ the largest X29 survivor value (computed from X29's JSON: finite KiDS Δχ² < 9).
  FAIL if the derived dependence makes these an empty set. Where the dependence is r = 1 (c_s ∝ σ), X26's JSON verdict for
  the virial line (special_cases "virial r=1,q=0 (B)", any = false) is binding.
- **G5 DISTINCT.** If the derivation shows the candidate reduces to a closed form (same background time law, same spatial
  key), it inherits that form's class; say which.

Inherited, reported only (not regraded): any end state with KT-median c_s in X26's sheet range inherits X30's OUTER
exclusion (all 19 / 16 points fail) and X32's collisionless reading (EXCLUDED in all 4 combinations).

## 4. Derivations required (sympy where symbolic; `dh1_derive.py`)

- D1 (H1): background solution of dσ²/dN = −2σ² + S(N) for collisionless peculiar dispersion with S ∝ df/dN,
  f = ρ_DE/ρ_m; the exponent of c_s(a) and X22's p = (exponent) + ½. Also with the record's native DE drift (CFG689
  sqrtX at z* = 2.33, read from X35's JSON) as an effective exponent.
- D2 (H1, H1L, H3): general power key S ∝ f^n gives p = 3n/2 + ½; the n needed for p ≥ 3.
- D3 (L1, H2–H4, H6): for H = A(t)p²/2 + B(t) x·p + C(t)·x + Φ(x, t), the deformation-tensor (Riccati) equation; show
  the homogeneous terms do not enter ∂²H/∂x², so a single-stream sheet stays single-stream unless Φ'' folds it; fine-grained
  dispersion of a cold sheet stays zero.
- D4 (H2): the specific energy input of a homogeneous drive in a bound system is ∝ σ_well² (scale-free ⇒ r = 1); the
  required galaxy and cluster boost factors from the record's numbers.
- D5 (H5): for a wave medium ω = D k² driven at rate Γ, the excited velocity v = 2√(DΓ); R2 bounds D ≤ v_f/k_f; hence
  v ≤ 2√(v_f Γ/k_f), with k_f = X22's α_NF half-mode k (15.08 h/Mpc), Γ = 3H₀, taken generously (comoving k, no (1+z)).
- D6 (H1, H3, H6 amplitude): ε needed vs natural; the trigger epochs z(ä = 0), z(Ω_Λ = Ω_m), z(a₀ = cH/2π) with κ = ½.
- D7 (H6): the v_k window from G4's three lines in quadrature.

## 5. Classes (lane verdict, per footing)

- **CANDIDATE FOUND**: some candidate passes G1, G2, G3 and G4.
- **OBSTRUCTION**: every candidate fails at least one of G1–G4, and each failure is a derived reason (D1–D7), not a grid.
  The obstruction is then stated as the lemmas that cover each candidate.
- **UNDECIDED**: any step-0 or derivation check fails, or a candidate cannot be graded on G1–G3.

## 6. Step 0 and checks (exit 0 only if all pass)

- K0a: read X22 c_s,need (190.014 / 201.315) and p = 2, 3 rows (cs_z3, cs_z2, forest class) from X22's JSON; reproduce X22's
  p = 3 cs_z3/cs_z0 = 4^(−2.5) and p = 2 = 4^(−1.5) to 1e-9.
- K0b: X26 KT-median c_s ranges and σ medians (517.1, 70.5) read from X26's JSON / .out; virial r = 1 line any = false.
- K0c: X29 survivor count 23 / 15 reproduced from X29's JSON; max survivor C₀ reported.
- K0d: X35 S0-3 sqrtX 0.9094 / 0.9498 read back.
- K1: sympy identities D1–D5 hold symbolically.
- K2: D3 numerical: a 1-D cold sheet under a random homogeneous drive A, B, C (no Φ) keeps zero velocity spread at fixed x
  to ≤ 1e-12; with Φ'' ≠ 0 it folds (control).
- K3: peak RSS < 1 GB.

**MUTATE (`DH1_MUTATE=1`, separate outputs `*_MUTATE.*`):** (m1) collisionless cooling exponent −2 → −1 (fluid-like);
(m2) matter dilution a⁻³ → a⁻²; (m3) a homogeneous drive given a spatial gradient term (∂²H/∂x² ≠ 0 from the drive).
K0a's exponent reproduction, K1 and K2 must fail; exit 1.
