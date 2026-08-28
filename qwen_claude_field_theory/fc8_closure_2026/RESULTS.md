# FC-8R CLOSURE — AUDIT LOG

Candidate: **FC-8R (Reduced Potential-Locked AeST)**, frozen in `FROZEN_CANDIDATE.md`.
Rules: `REQUIREMENTS.md`. Only **PASS / FAIL / OPEN**. No inheritance. No goalpost-moving. Corrections and
failed branches are kept, not hidden.

## Status board (2026-08-28)

| Gate | Script | Status | What is produced by the equations vs. what is missing |
|---|---|---|---|
| **G0** symbolic audit | `fc8_symbolic_audit.py` | **PASS (7/7)** | Exact elimination valid (V>0 global); `μ₁₀=y+O(y¹¹)`; `J₁₀=x³/3`; `𝒜(χ)=κ²GV` carries no χ̇/∇χ ⇒ MOND K_χχ=0, K_∇χ=0, all orders; `δ²S_MOND=0` on vacuum; `a₀,₀²=κ²GV₀`; SS suppression `1−μ₁₀=O((a₀/g)¹⁰)`; BTFR. **A6:** linear MOND–χ coupling vanishes at vacuum — `∂L_M/∂χ\|_{χ₀}=0`, mixed `δ²S_{MOND-χ}=0`, `δa₀^(1)=0` (all ∝ V'(χ₀)=0); honest: `δa₀^(2)=κ²Gm²δχ²≠0`. |
| **G1** Dirac rank | `dirac_fc8.py` | **PARTIAL** | *PASS:* velocity Hessian block-diagonal `diag(H_AeST,1)` — no auxiliary fields, χ ordinary canonical, perturbative `N_phys=6+1=7`. *OPEN:* full nonlinear Poisson rank on branches (a)–(e); 7 is a TARGET, not a theorem, until the matrix rank is printed. |
| **G2** PPN | `ppn_fc8.py` | **OPEN** | MOND term is SS-negligible, but AeST preferred-frame `α₁,α₂` must be **derived for FC-8R** and the FC-8R→EA map made explicit — not imported. Nothing derived yet. |
| **G3** slip Φ−Ψ | `weak_field_fc8.py` | **OPEN** | On the branch χ=χ₀ ⇒ ∇χ=0 (no new anisotropic stress) makes Φ=Ψ *plausible by inheritance* — forbidden as PASS. Φ−Ψ not yet computed from the traceless FC-8R equation. |
| **G4** spherical + IR | `spherical_fc8.py` | **PARTIAL** | *Derivable:* `r_C~(r_M μ⁻²)^{1/3}` ⇒ IR onset beyond galactic scales requires `μ⁻¹≳Mpc` (falsifiable constraint). *OPEN:* full nonlinear BVP; whether `g_N=g²/(g¹⁰+a₀¹⁰)^{1/10}` and Φ=Ψ come from the *solution*. |
| **G5** FLRW growth | `flrw_fc8.py` | **PARTIAL** | *PASS:* vacuum χ sector healthy (`K_χ=+1, c_χ²=1`, `δ²S_MOND=0`). *OPEN:* full quadratic system (metric+aether+φ+χ), the AeST nondynamical `k_*` mode, and whether the FLRW solution stays potential-dominated (`χ̇²≪V`) so `a₀(z)` is acceptable. |

## Overall

**FC-8R is a fully specified local candidate action with a clean kinetic/DOF structure at the vacuum
(G0 PASS; G1/G5 perturbative PASS).** It is **not** a validated theory: the four decisive gates —
**full nonlinear Dirac rank (G1), PPN (G2), nonlinear Φ−Ψ (G3), FLRW perturbation stability (G5)** — plus
the nonlinear spherical solution (G4) are **OPEN**, and require the actual FC-8R field equations, not
inheritance from AeST. No FAIL has been produced; no PASS has been faked.

**a₀²=κ²GV(χ) remains an imposed lock with a chosen V — a clean phenomenological realization, not a
symmetry consequence.** The surviving-branch empirical decider (6-DOF AeST + sharp μ_n) is Gaia DR4 (see
`../closure_2026/FC_AEST/FROZEN_HIERARCHY.md`).

## The closure is now one finite existence problem

Architecture is frozen. The remaining task is to find whether a **single AeST parameter point**
`{K_B, K(Q)=−2Λ+𝒦₂(Q−Q₀)², μ, m_χ, V₀}` simultaneously satisfies:

```
N_phys = 7 (full nonlinear Dirac rank, G1)      c_T^2 = 1 (G2/GW)
no ghosts, no gradient instabilities (G5)        |alpha_1| < 1e-4, |alpha_2| < 1e-7 (G2)
Phi = Psi in the full spherical solution (G3/G4)  r_IR beyond the tested galactic domain (G4)
acceptable FLRW growth (G5)
```

No single constraint is being asked to do six jobs (the C_M trap). Either a healthy corner exists → the
bird is cooked, or a gate FAILs at every corner → we learn exactly which ingredient is incompatible.

### Change log
- 2026-08-28 — Lane created. FC-8 → **FC-8R** (auxiliary α,ζ eliminated exactly, V>0 global). G0 PASS (6/6);
  G1/G4/G5 PARTIAL; G2/G3 OPEN. Sources: `../closure_2026/FC_AEST/scripts/{fc8_clean_lock,fc7_groundstate_closure,fc7_reduced_action_rank}_2026.py`.
- 2026-08-28 — G0 → **7/7** (added A6: linear MOND–χ coupling vanishes at the vacuum, δa₀^(1)=0, mixed
  δ²S_{MOND-χ}=0, all ∝ V'(χ₀)=0; honest δa₀^(2)=κ²Gm²δχ²≠0). Closure restated as a finite existence problem.
