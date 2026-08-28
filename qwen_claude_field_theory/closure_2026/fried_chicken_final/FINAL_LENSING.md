# FC-FINAL (AeST + J₁₀) — NON-SPHERICAL LENSING CLOSURE

**Task:** confirm Φ = Ψ (γ_PPN = 1) for a **non-spherical** (axisymmetric / generic weak) source,
not just the committed spherical case; compute α_lens(b) = (2/c²)∫∇⊥(Φ+Ψ)dz vs GR(M_eff); reproduce
the committed KiDS M24 anchor χ²/dof = 0.64.

**Winner architecture:** A = AeST (Skordis–Złośnik, 6 DOF) + frozen sharp kernel μ₁₀(y)=y/(1+y¹⁰)^{1/10}.

**Certificate script (self-contained, re-runnable):**
`fried_chicken_final/fc_nonspherical_lensing_slip_2026.py` — **14/14 checks PASS this session.**

---

## What was OPEN before this run

- `fc8_closure_2026/weak_field_fc8.py` (Gate G3, gravitational slip Φ−Ψ): status **OPEN** — "AeST
  normally has Φ=Ψ, therefore PASS" was explicitly **forbidden** as an inheritance.
- `fc8_closure_2026/spherical_fc8.py` (Gate G4): Φ=Ψ "come out of the SOLUTION rather than assumed" —
  listed OPEN, and only for the **spherical** BVP.
- The committed anchor `FC_AEST/scripts/fc_lensing_rar_mu10_2026.py` **asserted** γ_PPN=1 ⇒ Φ=Ψ and
  used it; `route2_aest_embedding_2026.py` (PART E) **mechanised** it verbally ("the J·∂φ term enters
  the 00 sector, not the anisotropic-stress sector") but did not carry the **traceless ij equation for
  a non-spherical source** with a printed certificate.

This run supplies the missing general (geometry-free) derivation with runnable certificates.

---

## The derivation (labels: THEOREM / DERIVATION / COMPUTATION)

### PART 1 [DERIVATION, sympy] — the exact slip equation, no symmetry assumed
Linearized Einstein tensor for the **general** Newtonian-gauge metric
ds² = −(1+2εΦ)dt² + (1−2εΨ)δ_ij dxⁱdxʲ with **Φ(x,y,z), Ψ(x,y,z) arbitrary functions** (no spherical
symmetry). Certificates (`simplify(...) == 0`):

- `G_xy = ∂_x∂_y(Ψ−Φ)`, `G_xz = ∂_x∂_z(Ψ−Φ)`, `G_yz = ∂_y∂_z(Ψ−Φ)`  — **exact**.
- `G_00 = 2∇²Ψ`  — the Poisson/source equation (this is where the MOND kernel lives).

⇒ the slip obeys **∂_i∂_j(Ψ−Φ) = 8πG̃ (T_ij^field)_{i≠j}**, and matter is pressureless (no off-diagonal
matter stress). So **Φ=Ψ ⟺ the field off-diagonal stress vanishes at the same (linear) order as G_ij.**

### PART 2 [DERIVATION, sympy] — every AeST field off-diagonal stress is O(ε²)
Order-counting with a bookkeeping ε (=|Φ|~(v/c)²), keeping a **generic non-spherical** scalar profile
φ(x,y,z) **and a nonzero spatial aether aᵢ(x,y,z)** (we do **not** assume the vector vanishes — per
`REQUIREMENTS.md`). Certificates that the linear-in-ε part of each off-diagonal stress = 0:

| term | mechanism | certificate |
|---|---|---|
| **2A** k-essence Y-sector (carries the MOND kernel) | T_ij^Y = −2[(2−K_B)+F_Y](∂_iφ)(∂_jφ); the **entire kernel dependence** sits in the prefactor F_Y, multiplying a product of two first-order gradients | coeff(ε¹)=0, **any F_Y** |
| **2B** aether Maxwell −(K_B/2)F² | electric ~∂Φ, magnetic ~∂a, both O(ε) ⇒ stress O(ε²) | coeff(ε⁰)=coeff(ε¹)=0 |
| **2C** mixing 2(2−K_B)J^μ∂_μφ | **unit-norm identity** J^μA_μ = A^μA^ν∇_νA_μ = ½A^ν∇_ν(A²) = 0 kills the only would-be-linear (Q₀-background × aether-acceleration) piece; remainder O(ε²) | ε⁰=ε¹=0 |
| **2D** Q-sector K(Q) (dark-energy/condensate) | g_μν·𝓕 is isotropic (no off-diagonal); A_(μ∂_ν)φ piece is O(ε²) | structural |

**Why this is the real reason, not an inheritance:** AeST's scalar and aether couple to the metric
**only** minimally (through T_μν) and **derivatively** (shift symmetry: only ∂_μφ appears, never a φR
non-minimal term). A φR term is exactly what puts a **linear** φ into the ij equation in
Brans–Dicke/scalar–tensor and gives γ−1 = 1/(2+ω_BD) = O(1). Shift symmetry **forbids** that term ⇒ no
linear-order anisotropic stress ⇒ Φ=Ψ. **This is a HOST property, shared by every admissible kernel.**

### PART 3 [DERIVATION + COMPUTATION] — slip bound, non-spherical, with numbers
∂_i∂_j(Ψ−Φ) = 8πG̃·O(ε²) ⇒ **Ψ−Φ = O(ε²)** ⇒ **|γ_PPN−1| = O((v/c)²)**:
- L\* disk galaxy (v~200 km/s): ε ≈ 4.5×10⁻⁷ ⇒ |γ−1| ≲ 5×10⁻⁷ (margin ~2×10⁵× vs the ~10% lensing needs).
- Cluster (v~1000 km/s): ε ≈ 1.1×10⁻⁵ ⇒ |γ−1| ≲ 1×10⁻⁵ (margin ~9×10³×).

Same order at which **GR itself** has γ=1 for pressureless matter. Non-spherical, kernel-free.

### PART 4 [COMPUTATION] — α_lens(b) and the KiDS anchor
With Φ=Ψ, **α = (2/c²)∫∇⊥(Φ+Ψ)dz = (4/c²)∫∇⊥Φ dz**, and Φ is the **modified-Poisson** potential whose
gradient is g_obs (the RAR acceleration) — matter and light see the **same** Φ (γ=1).
- Genuine **non-spherical** source: razor-thin **exponential disk** (Freeman midplane g_bar via Bessel
  I₀K₀−I₁K₁, Md=6×10¹⁰ M⊙, Rd=3 kpc), mapped through μ₁₀ to g_obs. The lensing boost M_dyn/M_bar rises
  from 1.0 (inner, Newtonian) to ~4 (outer, deep-MOND) — the lensing "phantom" is the **same** missing
  mass dynamics infers; **no independent dark-lensing scale**.
- Committed **KiDS-1000 M24** weak-lensing RAR (Mistele+2024, arXiv:2310.15248), μ₁₀ @ canonical
  a₀=9.3619×10⁻¹¹: **χ²/dof = 0.640** — matches `fc_lensing_rar_mu10_2026.py` exactly.

---

## Verdict and honest scope

**DERIVATION (non-spherical):** for FC-FINAL (AeST + J₁₀) and a **generic** (axisymmetric disk, cluster,
or arbitrary) weak static source, **Φ = Ψ to leading PN order**, with |γ_PPN−1| = O((v/c)²) ~ 10⁻⁶,
**kernel-independent**. The MOND kernel appears **only** in the Poisson source (∇²Ψ) and in the prefactor
of an O(ε²) term — **provably absent** from the slip equation. Consequently the weak-lensing deflection
uses the same g_obs=μ₁₀ acceleration that sets dynamics ⇒ **lensing mass = dynamical mass**, and the
committed KiDS anchor χ²/dof=0.64 is reproduced. "The architecture lenses correctly" is now a **derived**
statement for non-spherical sources, no longer an assertion.

**Host-vs-kernel classification (his §5):** the leading-order no-slip is a **HOST** property — it follows
from AeST's minimal + derivative (shift-symmetric) coupling and holds for **any** admissible F_Y. The
kernel is a **KERNEL** input that sets the Poisson source only.

**What remains OPEN (stated plainly, not converted to PASS):**
1. This is the **leading PN order** (the lensing-relevant order). The full **O(ε²) slip** and its sign
   are not computed here — negligible for lensing (10⁻⁶) but a genuine completeness item.
2. The **Part-4 deflection magnitude** for the disk uses the spherical-equivalent projection
   α=4GM_dyn(<b)/(c²b); the load-bearing **non-spherical** result is Φ=Ψ (Parts 1–3). A full disk
   ray-trace (2-D ∫∇⊥Φ dz along real lines of sight) is not performed — it would only re-package the
   already-proven Φ=Ψ + modified-Poisson Φ.
3. The fully covariant **nonlinear** BVP with metric/aether backreaction (fc8 Gate G4) stays OPEN;
   this run settles the **linear (weak-field) non-spherical** slip, which is what lensing needs.

**Footings:** a₀ = 9.3619×10⁻¹¹ m/s² canonical (FITTED anchoring); κ=½ FITTED, never derived.
**Credit:** the AeST action, Q/Y projections, the J^μ∂_μφ vector coupling, and the Φ=Ψ mechanism are
Skordis & Złośnik 2021; the frozen J₁₀ kernel is the framework's. KiDS M24 data = Mistele+2024.
