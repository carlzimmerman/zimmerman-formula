# GATE 2 (reordered) — the u_μu_ν disformal completion: DOF-FIRST verdict

**Question (Carl's reorder):** the decisive gate is DOF-preservation, NOT lensing. Take the
η=0, D=0 York/CMC theory — CERTIFIED 2+0 (Gate 1, referee-sustained) — and test the
completion `g̃_μν = C g_μν + D u_μ u_ν`, `u_μ = −∂_μT/√(−∂T·∂T)` (CMC foliation normal, already
present, non-dynamical in CMC gauge) AS A NEW THEORY. E=0 kept OFF (dΦdΦ injects Φ̇² → 2+1).

Scripts (all green, committed): `gate2_dof_preservation_2026.py`, `gate2_lensing_2026.py`,
`gate2_cone_gw170817_2026.py`, `gate2_hostile_referee_2026.py`.

---

## (1) DOF FIRST — does a nonzero derived D preserve the exact 2+0 pair? → **YES, conditionally**

The crucial subtlety: `g̃_00 ∝ (D−C)N²`. If C or D depends on the COVARIANT
`X = ∂_μΦ ∂^μΦ = −Φ̇²/N² + |D_iΦ|²`, then Φ̇² re-enters the matter action *through the
coefficients* and revives a scalar kinetic term Z_Φ → **2+1** (real obstruction).

Computed `Z_Φ = 2 (∂S_m/∂g̃_00)(∂g̃_00/∂Φ̇²)` two independent ways (chain-rule + Taylor
coefficient):

- **Covariant** C(Φ,X)/D(Φ,X): `Z_Φ ∝ (C_X·tr + D_X·ρ) ≠ 0` → scalar revives → **2+1**. OBSTRUCTION.
- **Foliation-spatial** C(Φ,σ)/D(Φ,σ), `σ = |D_iΦ|²` only: `Z_Φ = 0` identically → P_Φ stays
  primary, `(P_Φ, C_Φ)` remains the exact second-class pair. Gate identity
  `∂g̃_00/∂Φ̇² = C_X − D_X` = 0 in the spatial class, verified by sympy.

**Admissible class (DERIVED by DOF-preservation, not fitted):** foliation-spatial disformal
`C(Φ, |D_iΦ|²)`, `D(Φ, |D_iΦ|²)`, non-covariant, `C > D` non-degenerate, coupled Φ-Hessian
elliptic. Non-empty: a nonzero D exists. AQUAL symbol `P(Y)=√y(y+2)/(1+y)^{3/2} > 0`, H_⊥
stays first-class (g̃-source ultralocal in h, c_T=1 intact), u/T carry 0 new fields in CMC gauge.
**Count = 2+0. Phase 1 PASSES.**

---

## (2) Does that SAME class close the ν² gap, keep γ_PPN=1, pass Cassini, give c_γ=c_GW? → **NO**

### Lensing — FAIL (the local class cannot close the phantom gap)
Only the disformal D moves the lensing potential; the conformal C cancels by null-geodesic
conformal invariance: `Σ = Φ_phys + Ψ_phys = Φ_g + Ψ_g − D/2`, with `∂Σ/∂γ_C = 0`,
`∂Σ/∂γ_D = −1`. The unique (C,D) that makes lensing = dynamics is `C = 1 − 2φ_ph`,
`D = −4φ_ph` with `φ_ph = φ_M − φ_N` (verified to reproduce `Φ_phys = φ_M` and `Σ = 2φ_M`).
But `φ_ph = Φ − ∇⁻²∇·[μ∇Φ]` is **NON-LOCAL** (inverse Laplacian) in the MOND field, whereas
the Phase-1 2+0 class admits ONLY *local* D(Φ,σ). Two counterexamples confirm no universal
local D exists: (shell) equal local (Φ,∂Φ) with shifted φ_ph; (equal-σ) `φ_N ∝ √M` differs
across masses at fixed |∇φ_M|. This is the disformal analog of the AQUAL lensing failure —
*the same locality that keeps the scalar non-propagating (2+0) forbids the non-local coupling
MOND lensing requires.*

### Cone / GW170817 — the disformal is DISQUALIFIED as the lensing source
Inverting `g̃ = Cg + Duu` (u·u = −1): `g̃^{μν} = (1/C)g^{μν} − D/(C(C−D)) u^μu^ν`, so the photon
null cone gives **`c_γ² = (C−D)/C = 1 − D/C`**, IDENTICALLY on FLRW and the static weak field
(sympy-verified; a drops from the ratio). Graviton TT sector is unmodified GR → `c_GW = c`.
Hence `c_γ/c_GW − 1 ≈ −D/(2C)`, and GW170817 (`|Δc/c| ≲ 1e-15`) forces `|D/C| ≲ 2e-15`. But a
disformal large enough to SOURCE the deep-MOND phantom deflection needs `D/C = O(1)` —
GW170817-excluded by **~15 orders**. Null geodesics are conformally invariant, so C cannot bend
light differently from g; D is the only photon handle, and it is pinned to ≲2e-15.

### γ_PPN / Cassini (secondary, honest scalings not sharp σ)
Newtonian D→0 ⇒ γ_PPN→1 (Cassini-γ safe); disformal Q₂ ~ 1e-17 ≪ (1.6±1.8)e-27. The inherited
μ-function EFE-Q₂ (memory: 3–15σ) is a SEPARATE, unresolved Φ-sector liability — neither
worsened nor cured here.

---

## (3) Decisive compatibility — is {2+0} ∩ {gap-closing} ∩ {luminal} non-empty? → **EMPTY**

`{2+0-preserving}` = local D(Φ,σ). `{gap-closing}` = `D = −4φ_ph` (non-local). `{luminal}` =
`|D/C| ≲ 2e-15`; disformal-sourced lensing needs `D/C = O(1)`. The two closure conditions
(dynamics = φ_M, lensing = 2φ_M) already EXACTLY determine both free functions C, D; adding the
2+0-locality condition and GW170817 **over-determines with no solution**. The intersection is
empty. **DERIVED no-go, not fitted** (over-determination, verified as rigorously as a pass; the
hostile-referee pass sustained it, including a fresh DOF attack that failed to break 2+0).

---

## (4) THE VERDICT — **NO_GO for the local-disformal route (theory NOT globally killed)**

A nonzero derived D preserves 2+0 (Phase 1 ✅), but the SAME D that would close MOND lensing is
non-local (breaks the 2+0-locality that defines the class) AND would need `D/C=O(1)` (breaks
GW170817 luminality). *Lensing repair necessarily breaks 2+0, GW, or derivability* — the
designated NO_GO condition. The u_μu_ν disformal is DISQUALIFIED as the MOND-lensing mechanism.

This is **not a global kill.** The 2+0 York/CMC spine (D=0) is untouched. The only surviving
escapes both LEAVE this class and MUST be re-gated for DOF:

- **(a)** the g-frame AQUAL scalar supplies `(ν−1)ρ` with γ_PPN=1 on its own — the classic
  single-metric "ν² gap," known-hard (historically why TeVeS/AeST ADD a vector), not closed
  here but not the disformal's job;
- **(b)** add a propagating vector (AeST / Skordis–Zlosnik arXiv:1905.09465, luminal class
  D/C→0) — changes the DOF count (E≠0 / new field), exactly what the 2+0 gate forbids as
  written. A DIFFERENT theory that must be re-gated.

---

## (5) What survives + the κ/Z EFT ceiling

**Survives untouched:**
- The **D=0, η=0 York/CMC 2+0 spine** — Gate-1 certified, referee-sustained.
- **a₀ = cq/Z** and the load-bearing prediction **a₀(z) = a₀,₀ H(z)/H₀** (derived, Z-independent).
- c_T = 1 exact; γ_PPN → 1 in the Newtonian limit; the disformal Cassini-γ and disformal-Q₂ are
  safe (the disformal is not the liability — the μ-function EFE-Q₂ is, separately).

**EFT ceiling (unchanged):** κ = ½ and Z ≈ 21 remain **fitted, not derived**; only a₀ ∝ H(z) is
predicted. This is a modified-gravity effective theory at a frontier, not a TOE. The Gate-2
result adds a specific structural fact: *within the single-physical-metric, no-new-DOF class, a
local disformal cannot be the relativistic MOND lensing mechanism* — the lensing burden is not
dischargeable without either the hard g-frame ν² closure or an added propagating field.

**Caveats (honest):** the O(1)-required-D for disformal-sourced lensing is an order-of-magnitude
scaling (`φ_ph ~ (v/c)²`), not a LOS-integrated exact σ; the GW170817 bound is applied at
emission z~0.01; whether the g-frame AQUAL scalar ALONE supplies (ν−1)ρ with γ_PPN=1 is NOT
proven negative here (known-hard, open). The toy-Lagrangian lapse-solve in the hostile-referee
pass is a structural demonstration that CMC lapse-fixing cannot manufacture an absent Φ̇, not a
full covariant Dirac re-run (that is the prior η=0 certification, taken as given).
