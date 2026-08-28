# FC_NO_GO — The H_perp-deletion structural no-go

**Certificate:** `fc_no_go_Hperp_unsources_Phi.py` → `ALL LEGS PASS (12/12)`, exit 0 (this session).
**Cross-checks (re-run this session, all exit 0):**
`openai_push/final_closure/gate_lensing_weakfield_derivation.py` (DERIVED–FAIL, γ_PPN=0),
`openai_push/final_closure/scripts/ppn_mmg_gate_2026.py` (34/34, α_3=−1 kernel-blind),
`qwen_claude_field_theory/closure_2026/fried_chicken_final/FC_B_kernel_blindness_cert.py` (ALL CERTIFICATES PASSED).

---

## Statement (source-free class → THEOREM)

> **Theorem (H_perp-deletion unsources Φ).**
> Let a spatially-covariant, constraint-first gravity theory reach `N_grav = 2` gravitational
> degrees of freedom by **removing the Hamiltonian constraint `H_perp` from the constraint set**
> and imposing in its place a **source-free elliptic constraint on the conformal spatial factor**
> `q = −(1/6) ln det γ`, of the schematic form
> `S_2 = D² q ≈ 0` (or `D²(q + f[N]) ≈ 0`, with **no matter density on the right-hand side**).
> Then in the static weak-field (PPN) limit, with decaying boundary conditions,
> `q ≡ 0 ⇒ Φ ≡ 0 ⇒ γ_PPN = Φ/Ψ = 0`, light sees exactly **half** the dynamical potential,
> and the result is **invariant under any admissible MOND kernel μ(y)** and **under promotion of
> the constraint to a Laplacian multiplier `D²λ`.**

This is proved (not asserted) as four independent sympy legs:

| Leg | Content | Certificate |
|-----|---------|-------------|
| **1** | GR baseline: `q = Φ` at linear order (the conformal factor **is** the curvature potential); `H_perp` carries ρ onto Φ: `Φ̂ = 4πGρ/k² ≠ 0`; trace-free ij → `Φ=Ψ ⇒ γ_PPN=1`. | LEG 1 PASS |
| **2** | Replacement: source-free `−k² q̂ = 0 ⇒ q̂(k≠0)=0 ⇒ Φ=0 ⇒ γ_PPN=0`. | LEG 2 PASS |
| **3** | Kernel-blindness: `S_2 = D²q` contains no μ; `∂S_2/∂μ ≡ 0`. μ lives only in the lapse/AQUAL constraint `C_M` (the Ψ sector). Swapping μ_exp→μ_10 changes Ψ, never Φ. | LEG 3 PASS |
| **4** | Laplacian-blindness: to fake a smooth k≠0 curvature source a multiplier needs `λ̂ = −S₀/k²`, a 1/k² pole singular at k=0; the `D²λ` multiplier (support {k=0}) is orthogonal to the k≠0 Φ-sourcing equation. | LEG 4 PASS |

**Physical one-liner (verbatim from the committed lensing gate):** *"the deleted `H_perp` is
precisely the equation that sourced Φ."* MMG has no ij Einstein equation to fall back on, so the
ij/curvature sector is not under-supplied — it is **unsourced**.

---

## Why it is kernel-blind and Laplacian-blind (the classification)

The MOND kernel μ(y) enters **only** the lapse constraint `C_M = D_i[c² μ(y) D^i ln N]`, which
fixes the Newtonian/AQUAL potential Ψ (dynamics, rotation curves — these are correct). The
curvature potential Φ is fixed by a **different** constraint, and in B/C that constraint is the
flat, matter-free Laplacian on q. Hence:

- **KERNEL** classification is **excluded**: `∂S_2/∂μ ≡ 0` (Leg 3). Numerically the repo cert
  confirms γ_PPN=0, α_3=−1, matter non-conservation are invariant μ_exp→μ_5→μ_10 to <1e-19.
- **LAPLACIAN-completion** (architecture C) is **excluded**: the `D²λ` multiplier cannot reach
  the k≠0 sector without a 1/k² pole (Leg 4; corroborated by
  `fc_C_laplacian_orthogonality_certificate.py`, disjoint Fourier support supp{m=0}={0}).
- The true class is **CONSTRAINT-ARCHITECTURE**: the failure is manufactured by the *choice* of a
  source-free q-constraint made **in order to** hit the 2-DOF count.

α_3=−1 and α_1=+4 share the same root: they come from the elliptic `C_M` lapse response in the
g_0i / Φ_1 sector, not from μ. This is why even the named within-family repair
`S_2 → D²(q+lnN)` (which can set γ_PPN=1) does **not** touch α_3 — it is repair-resistant inside
this chassis, and it demands a full Dirac re-certification (Gates 3,6,7,8) for the new bracket
`{π_N, S_2'} = −D²(·/N) ≠ 0` before it is even a candidate.

---

## Scope — where it is a THEOREM and where it is a sharp obstruction

**THEOREM (unconditional) for the source-free class.** Any architecture whose 2-DOF certificate
rests on a q-constraint with **no matter density on the RHS** has γ_PPN=0, kernel-blind and
Laplacian-blind. **B and C are instances** and are eliminated at **Tier 1 / Tier 6** — the
γ_PPN=0 → M24 KiDS lensing Δχ² = +403…+498 over 15 bins (~20–22σ), Cassini γ ~43,000σ. Neither
the frozen kernel μ_10 nor the D²-completion can move these numbers.

**SHARP OBSTRUCTION-with-named-escape for the general class.** The *only* escape is a q-constraint
that carries the matter density, `D² q ~ +4πG ρ`. But that constraint **is `H_perp`'s content**
(the Poisson-for-curvature equation) reintroduced under another name; it is second-class with π_N
in a *different* way, so the `20 − 12 − 4 = 4 ⇒ 2` count must be **re-certified** through the full
Dirac program. B and C bought their 2-DOF count *precisely by declining* that source term. Hence:

> You may have **{2 DOF via a source-free q-constraint}** or **{γ_PPN = 1}**, **not both**, until
> some architecture exhibits a ρ-sourced q-constraint that *still* certifies at exactly 2 DOF.
> No such architecture exists in the committed record.

**What the theorem does NOT claim** (honesty guardrails): it does not claim every conceivable
2-DOF gravity is dead (that would over-reach); it does not transfer to architecture **A**, which
is diffeomorphism-covariant and **retains `H_perp`** among its four first-class constraints, so its
Φ is sourced (`Φ=Ψ` derived, M24 χ²/dof=0.64 @ canonical a₀). A pays for keeping `H_perp` with
6(+1) DOF, not 2 — it never enters this no-go's hypothesis. The no-go is exactly the price of the
constraint-first 2-DOF *ambition*, not of MOND, not of μ_10, and not of the k=0 sector (where
B/C are healthy: Friedmann regenerates first-class, `sf54` exit 0).
