# FC-FINAL CLOSURE — AUDIT LOG

Candidate: **FC-FINAL** = constant-a₀ AeST with a fixed `J₁₀` constitutive law, frozen in
`FROZEN_CANDIDATE.md` (supersedes FC-8R; the σ + dynamical-a₀ machinery is retired — see change log).
Rules: `REQUIREMENTS.md`. Only **PASS / FAIL / OPEN**. No inheritance. No goalpost-moving.

## Status board (2026-08-28)

| Gate | Script | Status | Produced by the equations vs. missing |
|---|---|---|---|
| **0** symbolic audit | `fc8_symbolic_audit.py` | **PASS (7/7)** | `μ₁₀=y+O(y¹¹)`; `J₁₀=x³/3`; `𝓕_M=Y^{3/2}/(3a₀)=O(δ³)` ⇒ `δ²S_MOND=0`; aether projector removes φ̇ from Y ⇒ no velocity-Hessian entry; MOND law + `1−μ₁₀=O((a₀/g)¹⁰)` + BTFR. **A6:** both AeST asymptotic limits give `β₀=1` ⇒ **λ_s=1** (fixed by J₁₀, not fitted). **A7:** `F_YY=1/(4√Y a₀)→∞` at Y=0 (singular Hessian) but `δ²S_M=0` ⇒ degenerate branch, not a ghost. |
| **A** Hamiltonian rank | `detC_legendre_regularity.py`, `dirac_fc8.py`, `y0_degenerate_dirac.py` | **PARTIAL — Y>0 PASS (proven-in-class); Y=0 rank OPEN** | **Generic Y>0 = PASS (proven-in-class):** FC-FINAL's F satisfies every hypothesis of the published AeST general-F 6-DOF theorem (2307.15126 / PRD 110.044015) on Y>0 — Q-sector byte-identical to the paper's own example (F_QQ=2𝒦₂≠0), separable (F_YQ=0, also covered), F_YY finite>0 ⇒ `det C ∝ K₂/(2a₀√Y) ≠ 0` for all Y>0 (7-agent workflow all *proven-in-class*; `detC_legendre_regularity.py` 6/6; field-redefinition invariant via `F_YY·F*_qq≡1`). **Y=0 = rank defect, OPEN (corrected — earlier "6-DOF benign" was too strong):** on the aligned homogeneous surface `U_μμ=−1/F_YY→0`, C_μν=0 ⇒ **`det C|_{Y=0}=0` exactly** — the regular 4+4 classification stops applying; must restart the Dirac algorithm there. NOT a ghost/7-DOF (quadratic stability is favorable — eigenvalues→(2−K_B)>0, seed-rescued vs bare-AQUAL collapse), but benign-conversion-vs-tertiary-chain is undecided. **OPEN residual:** the full nonlinear constraint continuation through Y=0 + the independent covariant re-derivation. |
| **B** Tensor | `ppn_fc8.py` (+ TT) | **PASS (c_T=1)** | 7-agent PPN workflow: dictionary c₁=K_B, c₂=0, c₃=−K_B, c₄=0 (Maxwell locus, c₁₃=0) ⇒ **c_T=1 exact and free** (Δc_T/c_T~10⁻⁴³ on GW170817, no tuning). Q_T>0 on the healthy branch; the MOND term is O(δ³) on the vacuum ⇒ no new quadratic tensor operator. |
| **C** PPN | `ppn_fc8.py` | **OPEN (adverse-leaning) — α₂ is the live danger** | 7-agent workflow: **γ_PPN=1 DERIVED, exact, kernel-independent** (F depends on g only via Y,Q; unit-timelike aether strips the traceless part ⇒ ∂_i∂_j(Φ−Ψ)=0, no source; holds even deep-MOND — a clean PASS, sharper than the O((a₀/g)¹⁰) heuristic). **β OPEN-not-adverse** (2PN; MOND part ~10⁻⁸⁰ negligible; can't import EA β=1 — the (2−K_B)J·∂φ scalar mixing puts FC-FINAL *outside* the Einstein-aether family). **α₁=−4K_B** ⇒ needs K_B<2.5e-5. **α₂ = crux, contested:** EA import invalid (Maxwell locus on the c₁₂₃=0 Foster–Jacobson pole); scalar-retained reading gives α₂=(5/2)K_B ⇒ needs K_B<4e-8, but this value is *disputed in-corpus* (may collapse to GR on a consistent background) ⇒ α₂ genuinely NOT settled. No empty corner *proven* (not a kill), but not healthy either. |
| **D** spherical (+m_×) | `spherical_fc8.py` | **PARTIAL** | *OPEN:* full nonlinear BVP `{Φ,Λ,A_t,A_r,φ}` **without** assuming the vector vanishes (the `m_×` scale); whether `g_N=g²/(g¹⁰+a₀¹⁰)^{1/10}` and Φ=Ψ come from the *solution*. |
| **E** lensing Φ−Ψ | `weak_field_fc8.py` | **OPEN** | Compute Φ−Ψ from the traceless FC-FINAL equation. Inheritance forbidden. |
| **F** infrared | `spherical_fc8.py` | **PARTIAL** | *Verified (MNRAS 531,272):* `r_C=⅓[18 r_M μ⁻²]^{1/3}`, `r_M=8.35 kpc`. Requirement `μ⁻¹≳1 Mpc` (**fitted, not a theoretical constant**): `μ⁻¹=1 Mpc⇒r_C≈177 kpc` (past the disk); `r_C≥1 Mpc` needs `μ⁻¹≈13.4 Mpc`. Earlier `μ⁻¹=3 Mpc` fiducial (r_C≈370 kpc) withdrawn as a frozen constant. *OPEN:* r_C from the full solution. |
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

## OVERALL STATUS (2026-08-28): CONDITIONALLY CLOSED — not globally proven

FC-FINAL is a fully specified local candidate whose generic branch, tensor sector, and lensing (γ=1) are
**derived PASSes**, with two live open fronts and no proven kill:

| | Result |
|---|---|
| Generic Y>0 nonlinear DOF class | **PASS** (proven-in-class, 6 DOF; det C≠0) |
| c_T=1 (GW) | **PASS** (exact, free) |
| γ_PPN=1 (lensing/slip) | **PASS** (derived, kernel-independent, even deep-MOND) |
| Y=0 quadratic stability | **PASS** (no ghost/strong-coupling) |
| Constitutive regularity of sharp J₁₀ | **PASS** (F_YY>0, longitudinal coeff>0 on Y>0) |
| **Y=0 exact nonlinear Dirac rank** | **OPEN** (det C=0 at Y=0; benign-conversion-vs-kill undecided) |
| **α₂ preferred-frame** | **OPEN, adverse-leaning** (α₂=(5/2)K_B⇒K_B<4e-8, or uncomputed; α₁=−4K_B⇒K_B<2.5e-5) |
| β (2PN) | OPEN, not adverse |
| Full nonlinear spherical + m_× (D) | OPEN |
| FLRW perturbations/growth (G) | OPEN |

**The two swings did NOT find the catastrophic extra scalar we hunted.** The surviving structural question
is narrow and specific: **the exact nonlinear constraint continuation through the Y=0 rank-deficient
surface.** The surviving observational danger is **α₂**. Neither is a proven kill; neither is closed.

### Change log
- 2026-08-28 — Lane created as FC-8R (AeST + σ + potential lock `a₀²=κ²GV(σ)`, target 7 DOF). Gate 0 PASS.
- 2026-08-28 — **Retired FC-8R → FC-FINAL.** Removed σ; a₀ is now a fundamental constant; DOF target 7→6;
  `a₀²∝ρ_DE` demoted to a cross-sector hypothesis (out of the action). Rationale: every dynamical-a₀
  mechanism spawns its own closure problem (σ stability + PPN + cosmology); the constant-a₀ theory removes
  the recursion and is the stronger target. Gates remapped to 0/A–G. Gate 0 = 5/5 PASS; Gate A/D/F PARTIAL;
  B/C/E/G OPEN. σ verification preserved in `../closure_2026/FC_AEST/scripts/fc8_clean_lock_2026.py` (the
  σ-lock was clean; it is retired for parsimony, not because it failed).
- 2026-08-28 — **IR fiducial μ⁻¹=3 Mpc proposed then WITHDRAWN as a frozen constant.** `spherical_fc8.py`:
  `r_M=8.35 kpc`, `r_C(3 Mpc)≈370 kpc`. Corrected a scaling slip (`r_C≥1 Mpc` needs `μ⁻¹≈13.4 Mpc`, not
  2.1 Mpc — the intermediate formula was dimensionally length²). Final position: **`μ⁻¹≳1 Mpc` is a fitted
  observational requirement, not hard-coded** into the fundamental theory.
- 2026-08-28 — Gate 0 → **7/7**: added **A6** (`β₀=λ_s=1`, fixed by J₁₀ via both AeST asymptotic limits —
  a genuine internal check) and **A7** (`F_YY→∞` at Y=0: constitutive Hessian singular on the homogeneous
  background; `δ²S_M=0` ⇒ not a ghost). The **Y=0 degenerate branch** is now Gate A's named key open item:
  the AeST general-F 6-DOF theorem applies on the generic Y>0 branch but not at Y=0, which needs its own
  degenerate Dirac analysis. This is the last fundamental field-theory gate.
- 2026-08-28 — **Y=0 degenerate branch ATTACKED → RESOLVED BENIGN** (7-agent adversarial workflow, 3 derive
  + 3 refute, ALL benign-6DOF; `y0_degenerate_dirac.py` 5/5 + `../../real_research/reviews/fc_final_Y0_dirac_route_a_2026.py`).
  The `F_YY→∞` degeneracy is a Legendre-chart/AQUAL-like non-analyticity on the ∇φ=0 locus, not a pathology:
  reciprocity `F_YY·F*_qq≡1` (regular in `x=√Y/a₀`); φ momentum via `F_QQ=2𝒦₂` (F_YY never enters the kinetic
  matrix); spatial eigenvalues `→(2−K_B)>0` (divergence tamed by ∇φ→0); `δ²S_M=0` ⇒ auxiliary declassifies
  only on the measure-zero locus carrying zero dynamics. No ghost/DOF-jump/strong-coupling. **Control check:**
  bare AQUAL strong-couples at ∇φ=0; AeST survives *specifically* via the `−(2−K_B)Y` kinetic seed — a
  non-trivial rescue. RESIDUAL: full covariant nonlinear multi-constraint AeST Dirac (completeness, not a
  hiding pathology). The "last fundamental field-theory gate" (per the 2026-08-28 A7 entry) is discharged
  favorably at the computed level.
