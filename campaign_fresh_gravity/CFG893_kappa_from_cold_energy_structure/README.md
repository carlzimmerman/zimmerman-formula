# CFG893: does the new cold-energy structure select κ? NOT SELECTED

**Bottom line.** No. Every balance the new structures impose either holds for every a₀, makes a₀ depend on galaxy mass, or
only bounds ακ jointly. κ stays free, and κ = ½ stays FITTED. Two structural reasons, both checked in sympy:

1. **κ needs c, and the cold-energy dynamics are Newtonian.** {a₀, G, ρ} have no dimensionless combination. With galaxy
   inputs the only groups are a₀/(Gρ̄^{2/3}M_b^{1/3}) and a₀/(GρL*), and only with c does a₀/(c√(Gρ)) exist (T1, K9). The c-free
   part of the system has a scaling symmetry, S_λ: x → λx, M → λ³M, a₀ → λa₀ at fixed density and time. That part is the drift,
   the gate, the deficit Poisson equation, the phantom, the supply, the catchment, the bath and the stiffened action, and all
   14 of its equations are invariant under S_λ (K7). So any c-free balance can only return a₀ ∝ Gρ̄^{2/3}M_b^{1/3} (mass exponent
   exactly 1/3) or hold for every a₀.
2. **c enters in only three places, and none of them gives an O(1) equality.** These are the dark-energy sink (through
   ε_DE = ρ_DE c²), drift causality |v_s| ≤ c, and the completion τ_ψ = c/a₀, which the record rejects. All three break S_λ (K7).
   - **Sink:** at most 5.8e-6 (can) or 6.5e-6 (alt) of ε_DE, and fixed by the end state, so independent of α.
   - **Causality:** an inequality only.
   - **τ_ψ = c/a₀:** rejected.

κ = ½ FITTED (κ_Λ 0.417 ± 0.095, CFG493). Footings 9.3603e-11 / 1.1312e-10 are κ-conditional and are never pooled; every
number below is given per footing. Cold energy is real gravitating mass, no particle species. Not "theory closed". No de
Sitter–Unruh argument is used. This lane does not touch the empirical provenance of κ or the 32π logic/Lean work (other chat).

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (fe9bd51fb).
- **Script:** `cfg893.py` (sympy + numpy, one process, about 2 s, < 130 MB).
  - Normal run: `OMP_NUM_THREADS=1 nice -n 10 python3 cfg893.py` → `cfg893.out`, `cfg893_results.json`. 13/13 K-tests pass, exit 0.
  - `CFG893_MUTATE=1` → `cfg893_MUTATE.out`, `cfg893_results_MUTATE.json`. All 4 teeth bite, exit 1 by design.
- **Inputs, read only:** CFG541's results JSON (C1 drift speeds, ΔW per unit mass) and cfg515_lib (census f_ret). Nothing was
  downloaded, and no other lane was edited.

## The relations and their classes

| | relation | source | class |
|---|---|---|---|
| R1 | exact Λ: ∂ₜε_DE + 3H(1+w)ε_DE = Q̄, w = −1 ⇒ Q̄ = 0 | CFG541 S(ii) | IDENTITY (a₀-free). Incompatible with E_sink > 0 for every κ, so dark energy must be dynamical (record) |
| R2 | dynamical DE absorbs Q, a₀ = κ√(Gε_DE) ⇒ d ln a₀/dt = Q̄/(2ε_DE) | CFG541/542 + S1 | IDENTITY: a₀(t) = C₁exp(∫…), so the constant (κ) is free. Drift ≤ 2.9e-6 / 3.3e-6 in ln a₀ (1.25e-6 / 1.42e-6 dex) |
| R3 | [H3: DE is the accumulated settling energy] ε_DE = ∫Q̄ dt | added | MASS-DEPENDENT (a₀ = ε²/(ρ_c²ξ²GM_b), exponent −1). Needs κ ≈ 1.5e10 (can) / 1.2e10 (alt): EXCLUDED |
| R4 | [H4: the sink drives a DE evolution of size 0.01] | added | MASS-DEPENDENT. Needs κ ≈ 1.5e6 / 1.2e6: EXCLUDED |
| R5a–c | [H5: gate edge d = 0 at the catchment edge r_ta] ρ_ph(r_ta) = (1−f_b)Δ_ta ρ̄_m, the same /3, or ρ_DE | added | MASS-DEPENDENT: d ln a₀/d ln M_b = 1/3 exactly (deep regime). Numerically 1/3 below the census f_ret turn-up, −0.29 above it |
| R6 | supply M_ph(<r_*) = 5.364 N M_b, N = 1/f_ret | S3 / CFG804 | IDENTITY in a₀: it fixes x_* = r_*/r_M = 54.14 at f_ret = 0.1 (77.1 / 30.3 at 0.07 / 0.18), the same for both kernels. MW-like (6e10) r_* = 512 / 466 kpc |
| R7 | [H7: supply runs out exactly at turnaround] r_* = r_ta | added | MASS-DEPENDENT (exponent 1/3). Implied a₀ = 1.9e-12 … 1.4e-11 |
| R8 | stationarity of the gated drift v_s = −ατ1[d > 0]∇ψ | CFG639 | IDENTITY: the residual at ρ_c = ρ_ph(a₀) is 0 for every a₀ |
| R9 | linear rate Γ = α(ρ_c/ρ_m)√(4πGρ_m) | CFG638 K6 | IDENTITY (∂Γ/∂a₀ = 0) |
| R10 | damped-ψ stability Γτ_ψ < 1 with τ_ψ = βτ, i.e. αβq < 1 | CFG541 §6 | IDENTITY (the record's α bound) |
| R11 | bath stationarity: for the deep 1/r² halo σ²/V² = ½ | CFG638; GF2 audit | IDENTITY. This ½ is the SIS ratio for every a₀, not κ (record audit a755b66ca) |
| R12 | drift causality \|v_s\| ≤ c | CFG541 C1, CFG542 K9 | JOINT/BOUND (see below) |
| R13 | M_cl = f·81σ⁴/(4Ga₀) | CFG878 | IDENTITY by construction (CFG877 computes M_cl from σ and the footing a₀). As an independent relation it would be JOINT (σ external, M_cl dwarf-dependent, CFG880) |
| R14 | stiffened action: W_rem → W_rem + W₀ leaves the EL equations unchanged | S2 (CFG807 V0) | IDENTITY. The rest state is the law for every a₀ |

**Frozen overall label: NOT SELECTED.**
- No relation is SELECTED or SELECTED UNDER HYPOTHESIS.
- No record-implied relation fixes, or bounds more tightly than the record does, any of α, β, L*, f_ret, 5.364 or σ.

## The one new quantitative result: the drift's causality ratio does not depend on c or on galaxy mass

- **The phantom field is bounded.** For the round rule, g_ph = a₀·y(ν(y) − 1) ≤ c_ν a₀.
  - ν_mono: c_ν = 0.64761, reached at y = g_N/a₀ = 2.540.
  - Simple kernel: the supremum is 1, approached as y → ∞ (K6).
- **So the drift speed is bounded.** With the one-sided deficit and spherical symmetry, |∇ψ| ≤ g_ph. Therefore

  |v_s|/c ≤ α c_ν κ √(ρ_DE / (4π ρ_m,loc)).

  c cancels because a₀/c = κ√(Gρ_DE) is a cosmic rate. Galaxy mass cancels because g_ph ≤ c_ν a₀ holds in every system.
- **This is the one place where κ enters the cold-energy dynamics at O(1).** The bound reproduces CFG541's C1 speeds (K12):
  - every cell sits below it;
  - the point-mass cluster cells saturate it: measured/bound = 0.9989 (can) and 0.9991 (alt).

| footing, kernel | Δ_loc = 9.96 (CFG541 reservoir): v/c (α = 1), α_max, κ_H12 | Δ_loc = 1 | Δ_loc = f_b | drift superluminal below |
|---|---|---|---|---|
| can, ν_mono | 0.043, 23.4, 11.7 | 0.135, 7.4, 3.70 | 0.341, 2.94, 1.47 | 0.018 ρ̄_m |
| can, simple | 0.066, 15.1, 7.6 | 0.209, 4.8, 2.40 | 0.526, 1.90, 0.95 | 0.044 ρ̄_m |
| alt, ν_mono | 0.052, 19.3, 9.7 | 0.163, 6.1, 3.06 | 0.412, 2.43, 1.21 | 0.027 ρ̄_m |
| alt, simple | 0.080, 12.5, 6.3 | 0.252, 4.0, 1.98 | 0.636, 1.57, 0.79 | 0.064 ρ̄_m |

- **α bounds (column entries 2).** They are taken at the fitted κ. All are looser than the record's α ≤ 1.186, so there is no new
  constraint.
- **The C1 margin.** At α = 1 the drift is causal wherever the local matter density exceeds 2–6% of the cosmic mean.
  CFG541's 1e-2 margin fails in its reservoir because v/c = 0.043–0.080 there, which restates CFG541 open item 3.
- **The equality H12 (κ_H12, column entries 3).** "Marginal causality at a declared density" would give κ = 1–12 at α = 1. It is
  an added hypothesis with no basis in the equations. It is joint in α and the local density, and it carries Ω_m/Ω_Λ, so it would
  run with redshift. Class JOINT/BOUND, not a selection.

## Report-only numbers, and a near-coincidence that is not a selection

- **H5(a) gives an a₀ of the observed order, but it moves with galaxy mass.** H5(a) puts the gate edge at turnaround with CFG541's
  reservoir density.
  - Implied a₀: 1.6e-11, 3.5e-11, 7.6e-11, 1.3e-10 and 6.4e-11 at M_b = 1e8 … 1e12 M_⊙. That is κ_Λ 0.09–0.68 and κ_crit 0.07–0.56.
  - At M_b = 10^10.5 it gives a₀ = 1.12e-10.
  - It returns the fitted a₀ at M_b ≈ 1.8e10 (can) or 3.3e10 (alt).
- **Why it is not a selection.** It varies by a factor of 8 over four decades in mass, which is the exponent-⅓ law of T1, bent by
  the census f_ret above ~1e11. It also needs H5 and the empirical f_ret.
- **What it is.** This is the familiar order-of-magnitude coincidence between a₀ and cosmic densities for Milky-Way-mass systems:
  a₀ ≈ Φ Gρ̄^{2/3}M_b^{1/3} with a large prefactor (Φ ≈ 2 × 10⁴ for H5(a)). It is not a derivation. Variants (b) and (c) sit 9× and 21× lower.
- **The rejected R10 variant.** With τ_ψ = c/a₀, stability would need κ > 379 at Δ_loc = 1e5 (α = 1, q = 0.5). That is why CFG541
  chose τ_ψ = βτ.

## What a selection would need (the door left open)

An equality in which a₀/c, or ε_DE, enters at O(1) strength and does not depend on galaxy mass.
- The cold-energy equations contain none. Their only O(1), mass-free κ-carrier is the drift causality ratio, and that is an
  inequality.
- One candidate would be a dynamical reason for marginal causality at a density the framework itself fixes. Nothing in the record
  supplies one, and the result would still run with Ω_m/Ω_Λ.
- The other would be a relativistic completion in which a₀/c appears as a rate in the field equations. The record has no such
  completion (open item "relativistic lensing").
- Inside the present equations, more sink accounting, gate thresholds or supply bookkeeping cannot change this verdict.
  - The sink is 1e-5 of ε_DE whatever α is.
  - Gate and supply balances are S_λ-invariant.

## Prior κ routes (not repeated here)

- **32π puzzle (sonnet55_push/puzzle_32pi).** AΛ = 32π² reduces to ρ_Λ r_s² = 1. Gauss–Bonnet cannot fix a scale.
- **~30 sol61 lanes (2026-10-14/15).** These cover the coefficient verdict, coupled and coupled-medium models, dilaton, flux
  sectors, joint and local selectors, Weyl cancellation, WZ kinetic, response cone, spatial regulator, density micro and micro,
  critical, curvature tracking, tracking force, nonlinear tracking, backreaction, environment, broken potential, flat
  reconstruction, kinetic threshold, relaxing auxiliary and medium cone. The non-selection theorem shows that the additive vacuum
  energy E₀ leaves Λ/a₀² arbitrary under the response tests.
- **PARAMRED D_KAPPA.** The footing is a relabelling by √Ω_Λ, the combination does not shrink, and no sealed test pins κ.
- **CFG807.** The stiffened action's vacuum energy is ill-defined (−∞ / +∞). C = 16π needs a hand-set turn-off.
- **GF2 audit (a755b66ca).** The "κ = ½ derived" claim is the SIS ratio σ²/V² = ½, not the law's κ. It reappears here as R11.
- **CFG541/542.** Q is derived, and α is FREE (only causality-bounded). Neither touches κ.
- **Record rule.** Never cite de Sitter–Unruh for κ = ½.

## Checks and MUTATE

- **K-tests: 13/13 PASS.**
  - K1 deep limit, V⁴ = GM_b a₀; K2 Newtonian limit; both kernels.
  - K3 M_cat/M_b = (1−f_b)/(f_bf_ret), a₀-free by construction.
  - K4 census edge, both kernels: ν_mono equals cfg515 to 1e-12; simple gives 54.141.
  - K5 SIS ½. K6 c_ν. K6b the closed-form phantom densities equal the sympy derivative to 1.5e-14.
  - K7 S_λ: 14/14 c-free equations homogeneous; the three c-bearing relations break it.
  - K8 footings: +2.1e-4 / −4e-6. K9 null spaces. K10 dimensions 16/16. K11 classifier controls. K12 R12 vs CFG541 C1.
- **MUTATE (exit 1): all teeth bite.**
  - M1, sink sign flipped: R2's drift changes sign, and R3 has no positive κ.
  - M2, gate threshold d > ρ̄_m: R5(a)'s a₀ moves 1.120e-10 → 1.356e-10, and the MW-like edge moves 511.8 → 515.4 kpc.
  - The overall label stays NOT SELECTED, because nothing was selected. The would-be relations shift or vanish, which shows they
    depend on knobs.

## Assumptions (flagged)

- **Geometry.** R5–R7 use a point mass and the round rule. The symbolic exponents use the deep-regime phantom; the numbers use the
  exact kernels.
- **R12 bound.** It uses the one-sided deficit and spherical symmetry. With the two-sided ψ, the cold mass's own field is added,
  and that field is not bounded by c_ν a₀.
- **Sink budget.**
  - B puts all cold energy in CFG541's cluster-like system, a generous upper bound.
  - The κ scaling ΔW/M ∝ V_f² ∝ κ^{1/2} holds ξ = ΔW/(MV_f²) fixed.
- **Background inputs.** Δ_ta = 11.8157 comes from CFG541's ΛCDM-background shell ODE (Ω_m, h only). Ω_Λ = 0.685 with the engine
  Ω_m = 0.3134. Both are used only for report-only numbers and K12.
- **Census f_ret.** It is empirical and enters report-only numbers only.

## Disclosures (2026-10-20)

- **Hand estimates before the freeze.** The exponent ⅓, c_ν ≈ 0.648, the cluster bound ≈ 0.043, B ≈ 6e-6 and the α bounds were all
  estimated by hand and stated in the criteria. The script confirmed them.
- **Two numerical fixes, made before the overall label was read.**
  - The lambdified ν_mono density (a sinh form) overflowed. It was replaced by a stable closed form; K6b was added post-freeze to
    check that form against the sympy derivative.
  - The R5 root-finding was moved to log space to avoid underflow deep in the Newtonian regime.
  - The R5 symbolic classes had already printed when the first run stopped. No numbers changed class.
- **One report line corrected.** The R5 "κ range" print was changed from first..last row to min..max.

κ fitted; not theory closed.
