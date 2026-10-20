# CFG893 FROZEN CRITERIA: does any new structure in the cold-energy equations select κ?

Written before any script of this lane exists. Committed alone. κ = ½ is FITTED (record estimate κ_Λ 0.417 ± 0.095, CFG493).
The footings 9.3603e-11 (canonical: κ_Λ = ½ with ρ_Λ = Ω_Λ ρ_crit) and 1.1312e-10 (alt: κ_crit = ½ with ρ_crit) are
κ-conditional and are never pooled. Cold energy is real gravitating mass, no particle species. Not "theory closed". No knob
scans. No de Sitter–Unruh argument is used or cited. The GF2 "κ derived" claim is the singular-isothermal-sphere ratio, not the
law's κ (record audit a755b66ca); this lane treats that ratio as a by-construction trap (R11). Scope: ONLY whether the new
dynamical structure (CFG541/542/544 sink and energy bookkeeping, CFG638 fluid equations, CFG639 deficit gate, CFG882 clump
retention, the catchment supply rule of THEORY_CANONICAL v2/CFG804, the stiffened action of S2, CFG878 fragment mass) fixes κ.
The empirical provenance of measured κ and any logic/Lean argument about 32π belong to another chat and are not touched.

## 0. Disclosure (what I read and estimated before freezing)

Read: CFG638 README; CFG541 README, EQUATIONS.md and results JSON (C1 drift speeds, S energy section, settings); CFG542 and
CFG544 READMEs; CFG639 and CFG882 READMEs; THEORY_CANONICAL 2026-10-14 / 10-16 / 10-18; STANDING_2026-10-09_law.md; CFG804 and
CFG807 READMEs; PARAMRED D_KAPPA criteria and output; puzzle_32pi_nonselection RESULT.txt and the first lines of the other
sol61 puzzle_32pi lanes; sonnet55_push/puzzle_32pi README; the GF2 audit commit message; cfg515_lib.py (census f_ret).

Estimated by hand before freezing (expectations, not results; the script decides):
- The c-free balances (b)-(d) solve to a0 ∝ G ρ̄^{2/3} M_b^{1/3} (mass exponent 1/3).
- The phantom field of the round rule obeys g_ph = a0·y(ν(y) − 1) ≤ c_ν a0, with c_ν ≈ 0.648 at y ≈ 2.5 for ν_mono
  (ν = 1/(1 − e^(−√y))) and sup = 1 (y → ∞) for the simple kernel. Hence a drift-speed bound
  |v_s|/c ≤ α c_ν a0/(c √(4πG ρ_m,loc)) = α c_ν κ √(ρ_DE/(4π ρ_m,loc)), free of c and of galaxy mass.
- At CFG541's point-mass cluster reservoir (ρ_m,loc = (1 − f_b) Δ_ta Ω_m ρ_crit, α = 1) that bound is ≈ 0.043 (can), close to
  CFG541's C1 value 4.27e-2, i.e. the cluster cell nearly saturates it. This is used only as a K-test of the bound.
- Sink budget: (Ω_c/Ω_Λ)·(ΔW/M)/c² for CFG541's cluster-like system is ≈ 6e-6 of the dark-energy energy density.
- α bounds from causality at fitted κ, ν_mono / simple, Δ_loc = f_b: ≈ 2.9 / 1.9 (can), 2.4 / 1.6 (alt); all above 1.186.

## 1. What counts as "κ selected" (frozen)

A relation R is **SELECTED** iff all hold:
1. R is an equation (not an inequality) implied by the committed equations listed above, with **no added hypothesis**;
2. solved for a0 it gives a0 = k · c √(G ρ_DE) with k a pure number built only from π, e and kernel constants;
3. k does not depend on galaxy mass (∂ ln a0/∂ ln M_b = 0 symbolically), on free constants (α, β, L*, ε_sw, σ_J or σ_floor,
   threshold θ), on empirical inputs (census f_ret, a mass function, measured a0 or κ, Ω_c/Ω_b chosen to match), or on
   cosmological density ratios Ω_m/Ω_Λ (which would make κ redshift-dependent, against a constant κ).

Other classes (one per relation, first that applies):
- **SELECTED UNDER HYPOTHESIS H**: conditions 2-3 hold but R needs an added hypothesis H. Reported as a lead; never "selected" or
  "derived"; does not change the overall label.
- **IDENTITY**: R holds for every a0 (a0 cancels, or a0 only labels a family of solutions).
- **MASS-DEPENDENT**: solved for a0, ∂ ln a0/∂ ln M_b ≠ 0 (no universal κ).
- **JOINT/BOUND**: R is an inequality, or fixes κ only jointly with a free constant, a state variable (local overdensity Δ_loc)
  or an Ω ratio.
- **κ-INDEPENDENT CONSTRAINT**: R constrains another quantity (dark-energy dynamics, a0 drift, edge r_*/r_M, α) for any κ.
- **EXCLUDED**: an equality (under an added hypothesis) whose κ solution is non-real, non-positive, outside [0.01, 100], or needs
  α > 1.186 (the record's causality maximum, CFG542 K9).

**Overall label (frozen):**
- **κ SELECTED** iff at least one relation is SELECTED.
- else **CONSTRAINS SOMETHING ELSE** iff at least one record-implied relation (no added hypothesis) fixes by an equality one of the
  record's free/input constants {α, β, L*, f_ret, Ω_c/Ω_b, σ_J/σ_floor}, or bounds one of them more tightly than the record
  already does (α ≤ 1.186; L* ∈ [24 pc, ≳ 1 kpc]). For R12 the α bound is evaluated at the fitted κ (κ_Λ = ½ can, κ_crit = ½ alt;
  a bound on α conditional on fitted κ, not a κ derivation), strict causality |v_s| ≤ c, at the three declared states
  Δ_loc ∈ {(1 − f_b)Δ_ta, 1, f_b}, for both kernels; tighter than 1.186 in any cell ⇒ CONSTRAINS (named, kernel-conditional).
- else **NOT SELECTED** (κ free).
Non-constant consequences (a0 drift, r_*/r_M, the need for dynamical dark energy) are reported in every case.

## 2. The relations (each written in sympy; added hypotheses flagged)

Task (a), the dark-energy sink (CFG541 S(ii), CFG542 Pb: Q = ρ_c α τ 1_B 1_C ∇ψ·∇Φ ≥ 0; ε_DE ≡ ρ_DE c²):
- R1 [record] exact Λ: ∂ₜε_DE + 3H(1 + w)ε_DE = Q̄ with w = −1 and ∂ₜε_DE = 0 ⇒ Q̄ = 0, against E_sink > 0 (CFG541).
- R2 [record + S1 a0 tracking] dynamical DE absorbing Q: a0 = κ √(G ε_DE) ⇒ d ln a0/dt = Q̄/(2 ε_DE); cumulative Δ ln a0 ≤ B/2.
- R3 [ADDED H3: dark energy is the accumulated settling energy] ε_DE = ∫ Q̄ dt.
- R4 [ADDED H4: the sink drives a dark-energy evolution of declared size X = 0.01] ∫ Q̄ dt = X ε_DE.
  The budget B = (Ω_c/Ω_Λ)·(ΔW/M)_max/c² uses CFG541's cluster-like ΔW per unit mass from its JSON (all cold energy settled in the
  most energetic system class: a generous upper bound). Settling energy is fixed by the end state, independent of α (CFG541 V4).
  At fixed M_b, ΔW/M ∝ V_f² ∝ κ^(1/2), so the κ an equality needs is κ_req = κ_fit (target/B)².
Task (b), gate threshold vs cosmic densities:
- R5 [ADDED H5: the gate edge d = 0 sits at the catchment edge r_ta] ρ_ph(r_ta) = ρ_edge with
  (a) ρ_edge = (1 − f_b)Δ_ta ρ̄_m (CFG541 reservoir), (b) (1 − f_b)Δ_ta ρ̄_m/3 (edge of a ρ ∝ r⁻² profile of mean Δ_ta),
  (c) ρ_edge = ρ_DE; r_ta³ = 3M_ta/(4πΔ_ta ρ̄_m), M_ta = M_b/(f_b f_ret).
Task (c), supply:
- R6 [record, S3/CFG804] M_ph(<r_*) = 5.364 N M_b, N = 1/f_ret, point mass, both kernels.
- R7 [ADDED H7: the supply is exhausted exactly at turnaround] R6 with r_* = r_ta.
Task (d), stationarity and stability of the gated drift, and the remaining structures:
- R8 [record, CFG639] stationarity of v_s = −α τ 1[d > 0] ∇ψ, ∇²ψ = 4πG(ρ_ph − ρ_c).
- R9 [record, CFG638 K6] linear relaxation rate Γ = α(ρ_c/ρ_m)√(4πGρ_m).
- R10 [record, CFG541 §6] damped-ψ stability Γ τ_ψ < 1 with τ_ψ = βτ; the variant τ_ψ = c/a0 (rejected by CFG541) reported.
- R11 [record, CFG638 energy equation, bath term] stationary tr Π = 3ρσ_J²; isotropic Jeans in the deep-regime 1/r² halo.
- R12 [record, causality] |v_s| ≤ c on B∩C; the bound of §0; the equality "marginal causality at a declared Δ_loc"
  [ADDED H12] reported as a would-be relation.
- R13 [record v3 addendum, CFG878] M_cl = f · 81σ⁴/(4G a0), f ∈ [0.75, 0.95], σ external.
- R14 [record S2] stiffened action: Euler–Lagrange equations unchanged by W_rem → W_rem + W0 (reproduces CFG807 V0); a0 is a
  parameter of W_rem′.
Theorem T1 (dimensional): {a0, G, ρ_i} admit no dimensionless group; with M_b or L* added the groups involve M_b or L*; only
with c added does the κ group a0/(c√(Gρ)) exist. So a relation can fix κ universally only where c meets the dynamics.

## 3. K-tests (exit 1 if any fails)

- K1 deep limit: g²/(g_N a0) → 1 as g_N → 0 for ν_mono and simple (sympy limit); V⁴ = G M_b a0 for a point mass.
- K2 Newtonian limit: g/g_N → 1 as g_N/a0 → ∞, both kernels.
- K3 by-construction identity: M_cat/M_b,now = (1 − f_b)/(f_b f_ret) exactly, a0-free.
- K4 census edge: ν_mono point mass r_*/r_M = 1/ln(1 + f_ret f_b/(1 − f_b)) (sympy), equal to cfg515_lib's formula to 1e-12;
  simple kernel x = √((5.364/f_ret + ½)² − ¼) (sympy), |x − 54| < 0.5 at f_ret = 0.1 (CFG804: "54 r_M").
- K5 SIS Jeans: σ²/V² = ½ exactly, ∂/∂a0 = 0.
- K6 c_ν: numeric max of y(ν − 1) for ν_mono on a log grid y ∈ [1e-6, 1e6] refined by bounded minimisation; simple-kernel limit 1
  exact; g_ph ≤ c_ν a0 on the grid.
- K7 scaling: every galaxy-scale equation is homogeneous under S_λ: x → λx, M → λ³M, t → t, v → λv, ψ, Φ → λ²·, a0 → λ a0
  (ρ fixed; dimensionless inputs fixed) (sympy).
- K8 footings: κ_Λ = ½ with H0 67.4, Ω_Λ 0.685 reproduces 9.3603e-11, κ_crit = ½ reproduces 1.1312e-10, each to rel 5e-4.
- K9 T1: the dimension matrix of {a0, G, ρ} has rank 3 and empty null space; with c the null space is one-dimensional and
  ∝ a0 c⁻¹ G^(−1/2) ρ^(−1/2).
- K10 dimensions: both sides of every relation R1-R14 carry the same (M, L, T) dimensions.
- K11 classifier positive controls: a0 = ½ c√(Gρ_DE) → SELECTED form; a0 = G ρ̄^(2/3) M_b^(1/3) → MASS-DEPENDENT; a relation
  holding for all a0 → IDENTITY.
- K12 R12 bound vs CFG541 C1 (read-only JSON): with ρ_m,loc = ρ_c0 = (1 − f_b)Δ_ta Ω_m ρ_crit (Δ_ta recomputed with CFG541's
  algorithm, |Δ_ta − 11.8157| < 1e-3) and α = 1, the bound ≥ the recorded max |v_s|/c in all six cells (MW, group, cluster ×
  can, alt); for the two point-mass cluster cells measured/bound ∈ [0.90, 1.00].

## 4. MUTATE (CFG893_MUTATE=1; writes _MUTATE outputs; exits 1 by design when every tooth bites)

- M1 sink sign flipped (Q → −Q): R2's Δ ln a0 must change sign; R3 must have no positive real κ solution.
- M2 gate threshold d > θ ρ̄_m, θ = 1: R5(a)'s implied a0 at M_b = 10^10.5 M_⊙ must move by |Δ ln a0| ≥ 0.01; R6/R8's settled
  profile becomes ρ_c = ρ_ph − θρ̄_m and the MW-like point-mass edge must move by |Δ ln r_*| ≥ 1e-3.
Any would-be selection that survives M1 and M2 unchanged would be flagged as insensitive to the structure it claims to use.

## 5. Report-only numbers (never verdict inputs)

Implied a0 and κ (each footing separately) from R5(a-c) and R7 at M_b ∈ {1e8, 1e9, 1e10, 1e11, 1e12} M_⊙ with the census f_ret
(cfg515_lib, read-only); B and κ_req for R3/R4; R12 bounds, the critical density ρ_caus = (α c_ν κ)² ρ_DE/(4π) below which the
drift is superluminal, the 1e-2-margin variant, and the H12 would-be κ; the R10 variant's κ lower bound at Δ_loc = 1e5.
Inputs: G, c, h = 0.674, Ω_m = 0.14237/h², Ω_Λ = 0.685 (CFG493 definition), f_b = 0.02237/0.14237, census f_ret, CFG541 JSON.
Nothing downloaded. Light compute only (one process, minutes, < 1 GB).
