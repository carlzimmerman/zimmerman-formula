# FC-FINAL CLOSURE — AUDIT LOG

Candidate: **FC-FINAL** = constant-a₀ AeST with a fixed `J₁₀` constitutive law, frozen in
`FROZEN_CANDIDATE.md` (supersedes FC-8R; the σ + dynamical-a₀ machinery is retired — see change log).
Rules: `REQUIREMENTS.md`. Only **PASS / FAIL / OPEN**. No inheritance. No goalpost-moving.

## Status board (2026-08-28)

| Gate | Script | Status | Produced by the equations vs. missing |
|---|---|---|---|
| **0** symbolic audit | `fc8_symbolic_audit.py` | **PASS (5/5)** | `μ₁₀=y+O(y¹¹)`; `J₁₀=x³/3`; `𝓕_M=a₀²J₁₀=Y^{3/2}/(3a₀)=O(δ³)` ⇒ `δ²S_MOND=0`; aether projector removes φ̇ from Y ⇒ MOND adds no velocity-Hessian entry; MOND law + `1−μ₁₀=O((a₀/g)¹⁰)` + BTFR `v⁴=Ga₀M_b`. |
| **A** Hamiltonian rank | `dirac_fc8.py` | **PARTIAL** | *PASS:* modification is a function of Y only (a₀ const), Y has no φ̇ ⇒ zero velocity-Hessian contribution, **no new field ⇒ target N_phys=6** (not 7). *OPEN:* full nonlinear Poisson rank — the Y-dependent `F_Y` enters the constraint/gradient sector; must prove the 4-first/4-second-class degeneracy survives on branches (a)–(d). |
| **B** Tensor | `ppn_fc8.py` (+ TT) | **OPEN** | `Q_T>0, c_T²=1` must be re-derived for the modified `𝓕`, not inherited from AeST. |
| **C** PPN | `ppn_fc8.py` | **OPEN** | Derive FC-FINAL 1PN + FC-FINAL→EA map; extract γ,β,α₁,α₂,α₃; require `|α₁|<10⁻⁴, |α₂|<10⁻⁷`. No import. |
| **D** spherical (+m_×) | `spherical_fc8.py` | **PARTIAL** | *OPEN:* full nonlinear BVP `{Φ,Λ,A_t,A_r,φ}` **without** assuming the vector vanishes (the `m_×` scale); whether `g_N=g²/(g¹⁰+a₀¹⁰)^{1/10}` and Φ=Ψ come from the *solution*. |
| **E** lensing Φ−Ψ | `weak_field_fc8.py` | **OPEN** | Compute Φ−Ψ from the traceless FC-FINAL equation. Inheritance forbidden. |
| **F** infrared | `spherical_fc8.py` | **PARTIAL** | *Verified (MNRAS 531,272):* `r_C=⅓[18 r_M μ⁻²]^{1/3}`, `r_M=8.35 kpc`. **Fiducial μ⁻¹=3 Mpc ⇒ r_C≈370 kpc** (past the disk, not past 1 Mpc); `r_C≥1 Mpc` needs `μ⁻¹≈13.4 Mpc` (corrected a "2.1 Mpc" units-error). *OPEN:* r_C from the full solution. |
| **G** cosmology | `flrw_fc8.py` | **OPEN** | Linear cosmology reduces to AeST-with-K(Q) (MOND term sequestered O(δ³)); dark sector carried by `𝓕_Q^★`, NOT a₀. *OPEN:* full quadratic FLRW stability + the AeST nondynamical `k_*` mode + CMB/matter-power reproduction. |

## Overall

**FC-FINAL is a fully specified local candidate: AeST + one frozen MOND constitutive function, a₀ a
fundamental constant.** Its *ground-state / kinetic-sector* structure is clean (Gate 0 PASS; Gate A
kinetic PASS). It is **not** a validated theory: the full nonlinear rank (A), tensor (B), PPN (C),
spherical incl. `m_×` (D), lensing (E), and cosmology (G) are **OPEN** and require the *modified* FC-FINAL
field equations — not inheritance from AeST. No FAIL produced; no PASS faked.

**a₀²=κ²Gρ_DE is NOT in the action** — a cross-sector empirical hypothesis, no longer able to kill the
gravitational theory via a Hamiltonian pathology. The complementary empirical decider for the whole
program remains Gaia DR4's γ_v (`../closure_2026/FC_AEST/FROZEN_HIERARCHY.md`).

## The closure is one finite existence problem

Does a single AeST parameter point `{K_B, 𝓕_Q^★=K(Q), μ, a₀}` simultaneously give:

```
N_phys = 6 (Gate A)          c_T^2 = 1, Q_T>0 (Gate B)
no ghosts / grad instabilities + healthy nondynamical mode (Gate G)
|alpha_1|<1e-4, |alpha_2|<1e-7 (Gate C)     Phi=Psi in the full spherical solution (Gates D,E)
r_C beyond the tested galactic domain (Gate F)     viable AeST cosmology via K(Q) (Gate G)
```

No single constraint doing six jobs. Either a healthy corner exists → the bird is cooked, or a gate
FAILs at every corner → we learn exactly which ingredient is incompatible.

### Change log
- 2026-08-28 — Lane created as FC-8R (AeST + σ + potential lock `a₀²=κ²GV(σ)`, target 7 DOF). Gate 0 PASS.
- 2026-08-28 — **Retired FC-8R → FC-FINAL.** Removed σ; a₀ is now a fundamental constant; DOF target 7→6;
  `a₀²∝ρ_DE` demoted to a cross-sector hypothesis (out of the action). Rationale: every dynamical-a₀
  mechanism spawns its own closure problem (σ stability + PPN + cosmology); the constant-a₀ theory removes
  the recursion and is the stronger target. Gates remapped to 0/A–G. Gate 0 = 5/5 PASS; Gate A/D/F PARTIAL;
  B/C/E/G OPEN. σ verification preserved in `../closure_2026/FC_AEST/scripts/fc8_clean_lock_2026.py` (the
  σ-lock was clean; it is retired for parsimony, not because it failed).
- 2026-08-28 — **IR fiducial frozen: μ⁻¹=3 Mpc** (exploratory, not derived). `spherical_fc8.py` verifies
  `r_M=8.35 kpc` and `r_C(μ⁻¹=3 Mpc)≈370 kpc`. Corrected a scaling slip in the proposal: `r_C≥1 Mpc` needs
  `μ⁻¹≈13.4 Mpc`, not 2.1 Mpc (the intermediate formula was dimensionally length², not length). 3 Mpc pushes
  the oscillatory onset past the rotation-curve domain but not past 1 Mpc — recorded honestly, not upgraded.
