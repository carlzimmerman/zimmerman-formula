# FC_SELECTION — Winner under the strict lexicographic filter

**Frozen kernel (shared by all four):** `μ_10(y) = y/(1+y^10)^{1/10}`; as an AeST free function
`δ²J_10 = 0` (kernel invisible at quadratic order). The kernel is therefore **not** the
discriminator — every verdict below is kernel-blind and traces to the **host / constraint
architecture**.

**Scripts re-run this session (all exit 0):** lensing gate (DERIVED–FAIL γ_PPN=0),
`ppn_mmg_gate_2026.py` (34/34), `FC_B_kernel_blindness_cert.py` (all pass),
`fc_flrw_quadratic_gate.py`, `fc_lensing_rar_mu10_2026.py`, and the new
`fc_no_go_Hperp_unsources_Phi.py` (12/12).

---

## The filter, tier by tier

| Tier | Test | A (AeST+J_10) | B (constraint-first MMG) | C (Laplacian-MMG) | D (BIMOND+DBI) |
|------|------|:---:|:---:|:---:|:---:|
| **1** | no-go-free / structural survival | **PASS** (no structural no-go; retains H_perp) | **FAIL** (H_perp-deletion no-go) | **FAIL** (H_perp-deletion no-go) | **FAIL** (Ω_dm sum-rule THEOREM, 30/30) |
| **2** | N_grav healthy & counted | PASS (6, PRD 110.044015) | (2, but conditional) | (2, conditional) | OPEN (BD ghost unchecked) |
| **3** | c_T = 1 | **PASS** (exact, kernel-indep) | PASS | OPEN (subclass c_T>1) | OPEN-ADVERSE (+3.9e-2 on DW chassis) |
| **4** | γ, α_1, α_2, α_3 | γ=1 ✔, α_1 bounded ✔, α_2 OPEN-adverse, α_3 benign | **γ=0, α_3=−1** | **γ=0, α_3=−1** | not computed |
| **5** | FLRW perts / IR | **OPEN (decisive)** | OPEN (μ(0)=0 empties linear sector) | OPEN | FAIL |
| **6** | lensing | **PASS** (Φ=Ψ, M24 χ²/dof=0.64) | **FAIL ~20σ** | **FAIL ~20σ** | OPEN |
| 7–8 | structure / strong field | inherited-open | dead | dead | dead |

### Eliminations
- **B** — dead at **Tier 1** (structural no-go) and independently at **Tier 4** (α_3=−1, 2.5e19×
  pulsar bound) and **Tier 6** (γ_PPN=0, ~20σ). Three kernel-blind, constraint-architecture FAILs.
  The one healthy structural result (N_grav=2) is itself **conditional** — the `{D²q, H_i}`
  first-class hypothesis carries an uncomputed `(1/3)D²(D·ξ)` that could collapse the certificate.
- **C** — dead at **Tier 1 / Tier 6** by the *same* no-go, now proven **Laplacian-blind**
  (Leg 4 + orthogonality cert): the `D²`-multiplier lives at k=0 and cannot source Φ at k≠0.
  Its only genuinely earned cell is the k=0 cosmology sector (`sf54` exit 0) — which the no-go
  never touched. α_3=−1 is repair-resistant (S₅: `d(α_3)/d(multiplier)=0`).
- **D** — dead at **Tier 1**: `route6_bimond_twin_2026.py` (30/30) proves the two-metric twin
  sector obeys `F_b + F_TM = 1 ≠ 2`, so it cannot carry Ω_dm to the CMB — kernel-independent,
  parameter-free THEOREM. DOF (BD ghost) OPEN, c_T OPEN-ADVERSE, most PPN/lensing/Boltzmann
  never computed. Mostly a construction (DOI 22015358), not a certification.

---

## WINNER: **A = AeST (6 DOF) + frozen J_10**, status **CONDITIONALLY-VIABLE**

A is the **only** architecture that clears **Tier 1** (it keeps `H_perp`, so Φ is sourced — it is
structurally exempt from the no-go that kills B and C), and it then survives **Tier 3** (c_T=1
exact) and the *derived* parts of **Tier 4** (γ_PPN=1) and **Tier 6** (Φ=Ψ, M24 KiDS χ²/dof=0.64
@ canonical a₀). It is the winner **with the fewest unsupported assumptions**: its remaining
blockers are honestly booked OPEN, not cooked into PASS.

A wins by *architecture*, not by kernel: it pays for a sourced Φ with 6(+1 χ-clock) DOF instead of
2. The 2-DOF constraint-first ambition (B, C) is exactly what the no-go forbids alongside γ_PPN=1.

### Decisive open calculations for A (what moves it VIABLE ↔ dead)

1. **[DECISIVE] Sign of the low-k scalar Hamiltonian on the FLRW background (not Minkowski).**
   `S_FC → S^(2)_FLRW → K,G,M²(k,a) → ω²(k,a)` in the three limits k≫aH, k~aH, k≪aH for a
   DESI-compatible K(Q)/ρ(z) trajectory. Minkowski gives unbounded for k<k_*,
   `k_*² = (1+λ_s)/λ_s · μ²`, `μ² = 2K₂Q₀²/(2−K_B)`. **Proven kernel-blind** (`δ²J_10=0`) ⇒ a
   property of the AeST host alone. Committed status: mode is **secular (linear-in-t), not
   exponential**, k_*≲Mpc⁻¹; the expanding-background sign is **UNCOMPUTED**. This single number
   decides A.
2. **α_2 on a consistent Y≠0 background** (Tier 4, adverse-leaning, kernel-blind). The `(5/2)K_B`
   empty-corner no-go was refuted as a background artifact (typeII 44/44); the genuine positive
   value needs the coupled A^μ–φ 1PN O(w²) solve. Currently OPEN.
3. **Quasi-static scalar `c_s² ∝ 1/K_B` → ~3c** at the α_1/LLR K_B ceiling (Tier 3/hyperbolicity,
   HOST). Kernel-independent. Needs a derived preferred-frame causal-structure argument, or it is
   a genuine superluminality liability.
4. **Legendre/Dirac all-branches covariant theorem** (regularity residual at the Y=0 auxiliary
   chart; physical Hessian `H_phys(Y=0)=2(2−K_B)I>0` already shown, formal all-branch proof open).

### Standing honesty flags (do not upgrade without a committed script)
- `Λ = 32π a₀²/c⁴` and `a₀² = κ²c²Gρ_Λ` are **MODEL-ASSUMPTION / TARGET**, never derived; κ=½,
  Z~21 **FITTED**.
- A's DOF are **6(+1)** (external PRD 110.044015, not re-derived) — the 2-DOF program stays closed;
  A does not claim it.
- The cluster residual η(R500)~2 is **inherited**, not new, and not resolved here.

**Bottom line:** the mathematics selects **A**, and it selects it *structurally* — because A alone
keeps the Hamiltonian constraint that sources the lensing potential. B and C are eliminated by a
theorem, D by a sum-rule theorem. A is CONDITIONALLY-VIABLE pending the FLRW low-k IR sign
(item 1), which is the one calculation that promotes it to VIABLE or kills it.
