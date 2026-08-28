# FC-FINAL CLOSURE — AUDIT LOG

Candidate: **FC-FINAL** = constant-a₀ AeST with a fixed `J₁₀` constitutive law, frozen in
`FROZEN_CANDIDATE.md` (supersedes FC-8R; the σ + dynamical-a₀ machinery is retired — see change log).
Rules: `REQUIREMENTS.md`. Only **PASS / FAIL / OPEN**. No inheritance. No goalpost-moving.

## Status board (2026-08-28)

| Gate | Script | Status | Produced by the equations vs. missing |
|---|---|---|---|
| **0** symbolic audit | `fc8_symbolic_audit.py` | **PASS (7/7)** | `μ₁₀=y+O(y¹¹)`; `J₁₀=x³/3`; `𝓕_M=Y^{3/2}/(3a₀)=O(δ³)` ⇒ `δ²S_MOND=0`; aether projector removes φ̇ from Y ⇒ no velocity-Hessian entry; MOND law + `1−μ₁₀=O((a₀/g)¹⁰)` + BTFR. **A6:** both AeST asymptotic limits give `β₀=1` ⇒ **λ_s=1** (fixed by J₁₀, not fitted). **A7:** `F_YY=1/(4√Y a₀)→∞` at Y=0 (singular Hessian) but `δ²S_M=0` ⇒ degenerate branch, not a ghost. |
| **A** Hamiltonian rank | `detC_legendre_regularity.py`, `dirac_fc8.py`, `y0_degenerate_dirac.py` | **PARTIAL — Y>0 PASS (proven-in-class); Y=0 rank OPEN** | **Generic Y>0 = PASS (proven-in-class):** FC-FINAL's F satisfies every hypothesis of the published AeST general-F 6-DOF theorem (2307.15126 / PRD 110.044015) on Y>0 — Q-sector byte-identical to the paper's own example (F_QQ=2𝒦₂≠0), separable (F_YQ=0, also covered), F_YY finite>0 ⇒ `det C ∝ K₂/(2a₀√Y) ≠ 0` for all Y>0 (7-agent workflow all *proven-in-class*; `detC_legendre_regularity.py` 6/6; field-redefinition invariant via `F_YY·F*_qq≡1`). **Y=0 = CHART degeneracy, physically benign (`y0_physical_hessian.py` 5/5):** the `det C|_{Y=0}=0` (from `U_μμ=−1/F_YY→0`) is a singularity of the **auxiliary Legendre chart**, NOT of the physics. In the *physical* gradient `v_i=D_iφ` (not the invariant Y=v²), `∂²J₁₀/∂v_i∂v_j=(2/a₀)(rδ_ij+v_iv_j/r)` has eigenvalues `2r/a₀, 4r/a₀ → 0` — the MOND Hessian **vanishes** (finite C², not divergent), and the analytic seed gives `H_phys(Y=0)=2(2−K_B)I > 0` for K_B<2. So **`det C_auxiliary→0 ⇏ det H_physical→0`** — no ghost, no strong-coupling, no physical DOF jump (bare AQUAL *does* collapse to 0; the `−(2−K_B)Y` seed rescues it). Principle: define FC-FINAL fundamentally in the **primal `J₁₀(Y)` variables**; use the auxiliary Legendre chart only for Y>0. **OPEN residual (narrowed):** a formal all-branches covariant Dirac theorem on the singular boundary is still absent (would be referee-vulnerable) — but the *feared physical Y=0 pathology is resolved*. |
| **B** Tensor | `ppn_fc8.py` (+ TT) | **PASS (derived, c_T=c, Q_T>0, N_T=2)** | Derived directly from background symmetry: on FLRW/Minkowski `F_μν=J^μ=Y=0`, so `δ²_T[F²]=δ²_T[J·∂φ]=δ²_T[Y]=0` and `δ²_T𝓕` carries no TT derivative structure ⇒ the TT quadratic action = Einstein–Hilbert ⇒ **c_T=c, Q_T>0 (positive EH coeff), exactly 2 polarizations.** (Independently cross-checked by the EA dictionary c₁=K_B, c₃=−K_B ⇒ c₁₃=0.) The tensor sector is **not** where FC-FINAL dies. |
| **B2** Vector/scalar linear stability | `fc8_symbolic_audit.py` (A3) + inherited AeST | **CONDITIONAL (propagating) + OPEN (low-k)** | **J₁₀ is invisible at quadratic order** (`δ²J₁₀\|_{Y=0}=0`, since `J₁₀=O(Y^{3/2})=O(ε³)`, committed A3) ⇒ the linear scalar/vector spectrum is **AeST-inherited**, NOT modified by the sharp kernel. Propagating vector `ω_V²=k²+M_V²` and scalar `ω_S²=c_S²k²+M_S²` are healthy **conditional on `0<K_B<2, 𝒦₂>0`** (+ mass/kinetic conditions). **⚠️ The known AeST low-k nonpropagating mode (`ω=0`, Hamiltonian unbounded below for `k<μ`, 2109.13287) is NOT fixed by J₁₀ at quadratic order** (it's O(ε³)). Honest negative result: **J₁₀ alone does not cure the AeST linear instability.** The legitimate rescue (Minkowski `k<μ` is not the right criterion for the late-time FLRW background) is **Gate G — pending** (running workflow). |
| **C** PPN | `ppn_fc8.py` | **γ=1, c_T=1 PASS; α₂ = OPEN (specific kill REFUTED, not a proven pass)** | **γ_PPN=1** and **c_T=1** are clean derived PASSes. **α₂ = OPEN — not PASS, not FAIL.** Defensible results (7-agent workflow): (a) the `α₂=(5/2)K_B` empty-corner **no-go is REFUTED** — a *background artifact* (lives only on the inconsistent `λ_bg=0` background that violates the aether EOM by `2A_Y Q₀²`; on the consistent `λ_bg=(2−K_B)(1+J_Y)Q₀²≠0` background, `typeII` 44/44, the preferred-frame channel collapses, `S_par=2` for w≠0, so α₂≠(5/2)K_B); (b) the MOND `J₁₀` sector does **not** generate the PPN obstruction (`μ₁₀→1, μ₁₀'→0` decouples). **BUT α₂ itself is genuinely UNCOMPUTED** on the proper `Y≠0`/FRW background — `α₂=α₂(K_B,K''(Q₀),Q₀,…)` needs the full coupled `A^μ`–`φ` 1PN, `O(w²)` expansion. The "corner nonempty" (every candidate `O(K_B)→0`) is a **plausibility bound, not a computed pass.** So: OPEN. The next well-defined calc: `FC-FINAL —1PN,w²→ (γ,β,α₁,α₂)` with frozen K(Q) params, acceptance `\|α₁\|<1e-4, \|α₂\|<1e-7`. α₁=−4K_B ⇒ K_B<2.5e-5. (Disputed c_s² subluminality tension noted, not a stated corner condition.) |
| **D** spherical (+m_×) | `spherical_fc8.py` | **PARTIAL** | *OPEN:* full nonlinear BVP `{Φ,Λ,A_t,A_r,φ}` **without** assuming the vector vanishes (the `m_×` scale); whether `g_N=g²/(g¹⁰+a₀¹⁰)^{1/10}` and Φ=Ψ come from the *solution*. |
| **E** lensing Φ−Ψ | `weak_field_fc8.py` | **weak-field Φ=Ψ PASS; nonlinear OPEN** | **Weak-field Φ=Ψ (lensing mass = dynamical mass) — derived, kernel-independent** (γ=1, no dark anisotropic stress; the quasistatic AeST reduction `∇²Φ̃=∇·[J_Y∇χ]` with the required small-Y `J₁₀~(2/3a₀)Y^{3/2}` branch survives the sharp-kernel substitution). **OPEN:** full *nonlinear/non-spherical* relativistic lensing (complete coupled equations); and the outer-galaxy AeST μ-regime (3rd oscillatory regime) must terminate beyond the observable galactic domain ⇒ `μ⁻¹≳Mpc` (inherited constraint, already logged, Gate F). |
| **F** infrared | `spherical_fc8.py` | **PARTIAL** | *Verified (MNRAS 531,272):* `r_C=⅓[18 r_M μ⁻²]^{1/3}`, `r_M=8.35 kpc`. Requirement `μ⁻¹≳1 Mpc` (**fitted, not a theoretical constant**): `μ⁻¹=1 Mpc⇒r_C≈177 kpc` (past the disk); `r_C≥1 Mpc` needs `μ⁻¹≈13.4 Mpc`. Earlier `μ⁻¹=3 Mpc` fiducial (r_C≈370 kpc) withdrawn as a frozen constant. *OPEN:* r_C from the full solution. |
| **G** cosmology | `flrw_fc8.py` | **background DERIVED; IR-mode stability OPEN (main suspect)** | **FLRW background derived** (shift charge `K_Q=I₀/a³`; `H²=ρ/3+(QK_Q−K)/3`; dust-like `ρ_Q=QK_Q−K`, `p_Q=K`). **Clean 3-way separation** (a *good* structural feature): cosmology↔K(Q),Λ,I₀ • galaxy MOND↔J₁₀(Y) • propagation/PPN↔AeST kinetic — because `Y=0` ⇒ J₁₀ does NOT enter the homogeneous background. **`Λ=32πa₀²/c⁴` = ASSUMED/INPUT, not derived** (matches the committed inverse-K(Q) no-go: a₀²∝ρ_DE is a target; K(Q) reconstruction needed for ΛCDM; for pure dust it collapses to Q=0=GR). **⚠️ OPEN — the main suspect:** the AeST low-k IR scalar mode; since `δ²J₁₀=0` the cure (if any) can only come from `H(t),Q(t),K_QQ,K_B` on the time-dependent FLRW background — needs the full coupled FLRW quadratic action `det K_cosm(H,Q,K_QQ,K_B,k)>0, ω_i²(k,a)≥0`. **Caveat:** the quasistatic vector cannot be set to zero blindly (the `m_×` scale, PRD 110.024062). |

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
| Y=0 physical gradient sector | **PASS** (H_phys→2(2−K_B)I>0; no ghost/strong-coupling) |
| Constitutive regularity of sharp J₁₀ | **PASS** (F_YY>0, longitudinal coeff>0 on Y>0) |
| Y=0 auxiliary Legendre chart | **CHART degeneracy** (det C=0), *not* a physical DOF jump |
| **Formal all-branches covariant Dirac theorem** | **OPEN** (referee-vulnerable; the one unfinished theorem) |
| **α₂ preferred-frame** | **OPEN, adverse-leaning** (α₂=(5/2)K_B⇒K_B<4e-8, or uncomputed; α₁=−4K_B⇒K_B<2.5e-5) |
| β (2PN) | OPEN, not adverse |
| Full nonlinear spherical + m_× (D) | OPEN |
| FLRW perturbations/growth (G) | OPEN |

**The swings did NOT find the catastrophic extra scalar we hunted — and the Y=0 physical pathology we feared
is RESOLVED (it was a chart artifact).** 🍗 **Crispiness verdict: FC-FINAL is a fully specified, sharp-kernel
AeST candidate with NO known structural kill — crispy as a *candidate*, not yet crispy as a *watertight
published theorem*.** The two surviving fronts: (1) the formal all-branches nonlinear Dirac theorem on the
singular boundary (structural, referee-vulnerable, but no longer "maybe pathological"); (2) **α₂**
(observational, adverse-leaning). Neither is a proven kill; neither is closed.

**Housekeeping TODO (before any final paper):** quarantine the older exponential-kernel material
(`μ=1−e⁻ʸ`, the exponential FC manuscript) from the frozen sharp-`J₁₀` FC-FINAL candidate — do not mix.

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
