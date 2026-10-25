# X34_recombination_release — FROZEN CRITERIA (committed with ASSUMPTION_LEDGER.md, alone, before any script or number)

**The owner's idea.** "Think of a black hole as the singularity. What if recombination is the opposite of that?"

**Working reading, hypothesis RRB (recombination release boundary).** Recombination (z ≈ 1100, T ≈ 3000 K) is a release
boundary. The missing cold sector ("cold energy": gravitating field mass, never a particle; Ω_c/Ω_b ≈ 5.36) is released,
frozen out or decoupled at, or on the approach to, recombination, and clumps like dust afterwards.

Settings. κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt a₀ = 1.1312e-10 m/s², reported separately, never
pooled. a₀ is absent at linear order on FRW (Q6 D0, X4, X22), so Q1 and the forest half of Q2 are footing-independent
and are computed once; the dwarf half of Q2 and all of Q3 are computed per footing. No knob is fitted: every family
index (z_on, z_d, σ₀) is scanned on a frozen grid or bounded by a line, never adopted. Any "mass per quantum" is a
field-energy parametrisation, not a particle claim. Not "theory closed". Nothing here says the data favour the framework.

## 0. Step 0 — stop rule (all must PASS, else the lane stops with UNDECIDED and no Q1–Q3 number is graded)

| id | reproduction | line |
|---|---|---|
| S0-1 | C7's ΛCDM refit (`covariant_push_2026_10_22/C7_aest_class/c7_native_results.json`, `fits.LCDM`) re-evaluated with the pristine vanilla CLASS binary and C2's likelihood (plik-lite TTTEEE + low-ℓ TT + low-ℓ EE, executed read-only from `C2_aest_cosmology/c2b_native_cmb.py` as Q6 does) at Q6's precision (C7 A2 + start ×0.25): χ²_total equals C7's 1003.475 | \|Δ\| ≤ 2 |
| S0-2 | the same run's σ₈ equals C7's 0.827958 | \|ratio − 1\| ≤ 2e-3 |
| S0-3 | the X34 patched binary with the turn-on disabled (no `X34_ZON` set) equals the vanilla binary: TT, EE, φφ and σ₈ | max \|ΔC_ℓ/C_ℓ\| ≤ 1e-4 (ℓ 2–2508), σ₈ ≤ 1e-5 |
| S0-4 | X22's forest gate: the L319 cut family at X22's α_NF and α_PASS reproduces k_hm = 15.0788 / 59.894 h/Mpc and λ_hm = 0.41669 / 0.10491 Mpc/h (X22 JSON `step1`); X4's L346 bins and T²_5.3keV(k5) = 0.99519 read from `x4_dbi_door_results.json` | ≤ 1e-6 relative |
| S0-5 | X24's c₀ per footing read from `x24_dwarf_velocity_floor_results.json` and X24's field-dwarf rows rebuilt from X1's per-system CSV with X24's `load()` rule (13 LG field dwarfs per footing) | c₀ equal to 1e-9; N = 13 |

## 1. Q1 — timing (footing-independent)

**Two readings, both run in CLASS v3.3.4 (no semi-analytic proxy unless a run fails; any fallback is disclosed).**

- **R1 density turn-on (graded).** A patched vanilla CLASS (`x34_turnon.patch`, applied to the pristine v3.3.4 source
  on disk; built outside the repository) replaces ρ_cdm = ρ_c0 a⁻³ by ρ_c0 a⁻³ S(a), with
  S = ½[1 + tanh((ln a − ln a_on)/w)], a_on = 1/(1 + z_on), w = 0.05 (step). Energy is conserved by a homogeneous
  vacuum-like reservoir (w_res = −1) that holds the not-yet-released energy:
  ρ_res(a) = ρ_c0 ∫_{ln a}^{∞} e^{−3x} S′(x) dx (equal to ρ_c0 a_on⁻³ before release, 0 after). Total
  ρ_c + ρ_res obeys d(ρ_c + ρ_res)/d ln a = −3ρ_c. Perturbations (synchronous gauge only; the patch refuses Newtonian
  gauge): the released matter is created at rest in the cold frame and homogeneous on synchronous slices (δQ = 0), so
  δ_c′ = −h′/2 − (a′/a)(d ln S/d ln a) δ_c, and δρ_res = 0. ω_c denotes today's abundance (FITTED, as in Q6).
- **R2 kinetic release (graded the same way; the reading that Q2 presupposes).** Stock CLASS idm–photon coupling
  (f_idm = 0.9999 with a 1e-4 CDM remnant to fix the synchronous gauge, n_index_idm_g = 0, m_idm default): the cold
  component is present as dust in the background at all times, but its momentum is locked to the photons until
  kinetic decoupling z_d, defined by S_idm_g·dmu_idm_g = a′/a with S_idm_g = (4/3)ρ_γ/ρ_idm (CLASS's own rate; u_idm_g
  solved from CLASS's formula, then verified on CLASS's thermodynamics table to 2 %).

**Grid.** z_on (R1) and z_d (R2) ∈ {1100, 1500, 2500, 4000, 7000, 12000, 20000, 50000, 100000}.

**Fit protocol per grid point.** Start = C7's ΛCDM refit parameters (ω_b, ω_c FITTED, 100θ_s, ln10¹⁰A_s, n_s, τ with
C2's τ prior, A_planck with its 0.0025 prior). (a) Evaluate at the start: if Δχ² < 4 there, the point is PASS on the χ²
leg without a refit (a refit can only lower χ²). (b) Otherwise Gauss–Newton (C7's steps): a full Jacobian at the start,
Broyden rank-1 updates, line search halving to 1/16, at most 8 iterations, stop when the fall < 0.05. Δχ² is taken
against C7's ΛCDM refit χ² as reproduced in S0-1. Precision: Q6's (C7 A2 + start ×0.25), lensed C_ℓ to ℓ 2508.

**Lines (record sources).**
- χ² lines from C2's frozen criteria (L148–149): "not distinguishable" iff Δχ² < 4; "disfavoured" iff Δχ² > 25.
- σ₈ line from F3/Q6: σ₈ within 5 % of the dust (ΛCDM) value, \|σ₈/σ₈,ΛCDM − 1\| ≤ 0.05, at the refit.
- Point class: PASS iff Δχ² < 4 and the σ₈ line holds; EXCLUDED iff (Δχ² > 25 and converged-enough) or the σ₈ line
  fails at the refit; UNDECIDED otherwise. Converged-enough: the GN run stopped on its fall rule, or 3 × (last
  iteration's fall) < Δχ² − 25. An EXCLUDED call that rests on σ₈ alone is flagged.
- Reported (not graded): the TT third-peak height (C_ℓ max in ℓ 750–870) and its ratio to the first peak (ℓ 180–260)
  vs ΛCDM at each refit; z_eq from the CLASS ΛCDM run.

**Outputs.** z_on,allowed = the smallest grid z (latest epoch) such that it and every grid point at larger z are PASS.
z_on,excl = the largest grid z that is EXCLUDED. The margin: log-interpolated z where Δχ² crosses 4 and 25 (reported),
and z_on,allowed / 1100.

**Q1 class (graded on R1).** PASS iff z_on,allowed ≤ 1500 (release at or near recombination allowed). EXCLUDED iff the
grid point z = 1500 is EXCLUDED (the latest allowed epoch is above ~1500). UNDECIDED otherwise. R2 gets the same class
by the same rule (reported beside R1; it is the reading Q2 depends on).

## 2. Q2 — relic speed

**Relic.** The component decouples kinetically from the photon bath at z_d with T_d = T_cmb(1 + z_d) (thermal contact
with photons at decoupling). Framework-native parameter: the energy per unit mass at decoupling,
e_d = (3/2) σ_d² (σ_d the 1D dispersion). A non-relativistic decoupled gas keeps σ ∝ 1/a, so today
σ₀ = σ_d/(1 + z_d). Field-energy parametrisation (not a particle): μc² ≡ kT_d c²/σ_d² (NR valid iff μc² ≫ 3kT_d;
checked and reported).

**Free streaming (derived).** Linear collisionless response of a Maxwellian component with comoving momentum
dispersion σ₀ (superconformal time ds = dt/a², ∇²Φ̃ = 4πGρ̄_m0 a δ_m), Gilbert's equation, solved as an explicit
Volterra sum from a_d = 1/(1 + z_d) to z = 0:
δ_c(k,s) = [δ_d + δ′_d Δs] e^{−k²σ₀²Δs²/2} + ∫_{s_d}^{s} ds′ (s − s′) (3/2) H₀² Ω_m a(s′) δ_m(k,s′) e^{−k²σ₀²(s−s′)²/2},
baryons the same with σ = 0 (pressureless after drag release; disclosed), δ_m = f_c δ_c + f_b δ_b. Background H(a)
from the S0-1 CLASS ΛCDM run. ICs at a_d: δ_c = δ_b = 1, growing mode f = y/(y + 2/3), y = a/a_eq (Mészáros).
T(k) = δ_m(k; σ₀)/δ_m(k; 0) at z = 3 and z = 2; T² is graded with **X22/X4's forest rule verbatim** (PASS iff T² ∈ [0.8,
1.2] at the six L346 bins at z = 3 and 2 and T²(k5) ≥ T²_5.3keV; FAIL iff T²(k5) < 0.9 or a bin < 0.5 or > 2.0;
UNDECIDED otherwise). Reported: λ_hm = 2π/k_hm (T = ½) at z = 3 vs X22's λ_forest = 0.417 Mpc/h and the strict 0.105.
- σ₀,PASS = largest σ₀ with forest PASS; σ₀,NF = largest σ₀ not FAIL (verdict-bearing, window-favourable as in X22);
  σ₀,loose = largest σ₀ with λ_hm(z = 3) ≤ X22's worst-bin edge λ (α_bin0.5 = 0.0914 Mpc/h mapped through the L319
  family, reported loosest line).

**Dwarf floor (derived, phase-space / Tremaine–Gunn type).** A Maxwellian relic's maximum fine-grained phase-space
density f_max = ρ̄_c0/(2πσ₀²)^{3/2} is conserved; a cored isothermal structure of relic density ρ and 1D dispersion σ
has f(0) = ρ/(2πσ²)^{3/2} ≤ f_max, so **σ ≥ σ_min(ρ) = σ₀ (ρ/ρ̄_c0)^{1/3}**. The floor this relic imprints at
saturation is σ_min. Dwarf density: Wolf mass inside r₁/₂ = (4/3) R_h, ρ₁/₂ = 3M₁/₂/(4π r₁/₂³) with M₁/₂ = 3σ²r₁/₂/G,
from X24's 13 field dwarfs (X24's σ rule); the total dynamical density bounds the relic density from above
(generous to the floor). ρ̄_c0 = ω_c ρ_crit/h² from C7's ΛCDM refit (abundance FITTED).
- Floor interval per footing: σ₀ ∈ [c₀,lo / Δ_max^{1/3}, c₀,hi / Δ_min^{1/3}], Δ = ρ₁/₂/ρ̄_c0 over the 13 field
  dwarfs, c₀ band = X24's 68 % interval (canonical 4.01–5.14, alt 3.41–4.66 km/s). Central: c₀ / Δ_median^{1/3}.

**Q2 class (per footing).** Evaluated at z_d = 1100 and 1500 (the recombination window); reported at z_d = z_eq and at
R2's z_on,allowed.
- PASS iff [floor interval] ∩ [0, σ₀,NF] is non-empty at z_d = 1100 or 1500;
- EXCLUDED iff it is empty at both, even with σ₀,loose and the floor interval widened by the full c₀ band of both
  footings' union (3.41–5.14 km/s);
- UNDECIDED otherwise.
- Reported: the strict-line intersection (σ₀,PASS); the intervals in σ₀, σ_d, e_d and μc²; the floor σ_min for the
  MW ultra-faints at the same σ₀.

## 3. Q3 — scale link (per footing)

Base recombination quantities, from the S0-1 CLASS ΛCDM run (z_* from CLASS): H_* = H(z_*); r_s,com (CLASS rs_star);
r_s,phys = r_s,com/(1 + z_*); c_s,* = c/√(3(1 + R_*)), R_* = 3ρ_b/(4ρ_γ) at z_*; v_p = √(kT_*/m_p); v_e = √(kT_*/m_e);
T_* = T_cmb(1 + z_*). Framework: a₀ (per footing), c.

**Enumeration rule (exponents fixed by dimensional analysis).** Every product of exactly two distinct quantities from
{a₀, c, H_*, r_s,com, r_s,phys, c_s,*, v_p, v_e} whose exponents are uniquely fixed to give an acceleration, a speed or
a length, plus each single quantity that already has the target dimension. Dimensionless factors (1 + z_*, η_b) are
not used, except one comoving-conversion variant (×(1 + z_*)) for lengths compared with the comoving forest scale.

**Targets.** a₀ (per footing); c₀ (X24 central per footing); L★ (21.7 canonical / 22.9 alt pc, X27); λ_forest =
0.417 Mpc/h comoving (X22). Each candidate is compared with every target of its dimension.

**Match rule.** \|log₁₀(candidate/target)\| ≤ 0.1. The trials count N is the number of (candidate, target) comparisons
per footing. The chance rate is p = 0.2 / (log₁₀ span of all candidates of that dimension); expected chance matches
N·p are reported.

**Q3 class (per footing).** PASS (LINK DERIVED) only if a match follows from an action in the record — none is assumed;
UNDECIDED (NUMEROLOGY ONLY) if matches exist and none is derived; EXCLUDED (NO MATCH) if no comparison matches. Every
match is flagged as numerology. Q3 does not enter the overall class.

## 4. Overall class (frozen precedence)

1. Q1 (R1) EXCLUDED → if z_on,allowed(R1) ≥ z_eq and z_on,allowed(R2) ≥ z_eq: **RRB REDUCES TO ORDINARY CDM** (the
   only allowed window is cold and present long before recombination); else **RRB EXCLUDED BY TIMING**.
2. Q1 PASS and Q2 EXCLUDED on both footings → **RRB EXCLUDED BY RELIC SPEED**.
3. Q1 PASS and Q2 PASS on both footings → **RRB VIABLE (state the window)**.
4. Anything else → **UNDECIDED**.
Footings are reported separately; if they disagree on Q2, the class is UNDECIDED with both stated.

## 5. Checks (all PASS in the normal run) and MUTATE (`X34_MUTATE=1`, separate outputs `*_MUTATE.*`)

| check | normal | MUTATE change | MUTATE must |
|---|---|---|---|
| S0-1 … S0-5 | Step 0 above | none | PASS |
| K1_energy | on the R1 background table at z_on = 1100 (CLASS output, ρ_res = ρ_tot − Σ others): max \|d(ρ_c + ρ_res)/d ln a + 3ρ_c\| / max(3ρ_c) ≤ 2e-3 over the turn-on | ρ_res dropped from the identity | FAIL |
| K2_growth | Gilbert solver with σ₀ = 0 equals the direct growth ODE δ″ + (2 + d ln H/d ln a)δ′ = (3/2)Ω_m(a)δ at z = 0 and 3 | gravity sign flipped in the Gilbert source | FAIL |
| K3_jeans | Gilbert at σ₀ = 0.05 km/s, z_d = 1100: T(k) > 0.99 at k = 0.1 h/Mpc and T < 0.1 at k = 10 k_J,d (k_J,d = √(1.5Ω_m) H₀ a_d^{1/2}/σ₀) | none | PASS |
| K4_idm_rate | R2 at z_d = 2500: CLASS's own S_idm_g·dmu_idm_g / (a′/a) at z_d within 2 % of 1 | none | PASS |
| K5_turnon_bites | R1 at z_on = 1100 at C7's ΛCDM parameters changes TT at ℓ = 810 by > 1 % vs vanilla | the vanilla binary is run in place of the patched one | FAIL |
| K6_TG | σ_min(ρ̄_c0) = σ₀ (identity at the mean density) | none | PASS |
| K7_a0_lambda | a₀,canonical vs c²√(Λ/32π) with Λ = 3Ω_Λ H₀²/c² from the S0-1 run: ratio within 5 % (alt reported) | 32π → 16π | FAIL |

The MUTATE run skips the Q1 refits (only the checks run). Exit code 0 iff every check has its required outcome.

## 6. Run rules

PYTHONHASHSEED=0, `OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB RSS (CLASS runs ≈ 0.3 GB, ≈ 6 s each). No
download. Build of the patched CLASS outside the repository (temporary directory) from the pristine v3.3.4 source
already on disk; the patch and the build command are committed. `compute_queue/` is never touched.
