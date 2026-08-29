# CRISPY FRIED CHICKEN RECIPE 

**Permanent architectural specification for the relativistic-MOND program.** Every theory is just a
different batter; the ingredients, mandatory gates, and forbidden substitutions stay fixed. A candidate is
not "good" because it resembles a survivor — only if it uses the required ingredients and survives the
gates. Purpose: never resurrect a killed mechanism under new notation; never confuse phenomenology with
field-theory viability; never change μ to dodge a relativistic failure; never spend big compute on a
candidate that fails a cheap structural test; never promote "no computed kill" to "viable."
**Every future Claude/Qwen prompt on this program begins from this file. Last updated 2026-08-29.**
Rule: a gate flip = edit the ledger here in the SAME commit as the script. Never delete a graveyard entry.

---

## 1. FROZEN INGREDIENTS
- **I1 — MOND kernel:** μ(y)=1−e^{−y}, y=g/a₀. Limits μ=y+O(y²) (y≪1), μ→1 (y≫1). Changing μ = a
  DIFFERENT recipe, branched explicitly, never silently substituted.
- **I2 — Single physical metric:** S_m=S_m[g,ψ]. No hidden second metric / disformal matter metric /
  sector-dependent G without explicit reclassification.
- **I3 — GR tensor sector:** c_T=1, Q_T>0. No hiding a tensor-speed correction behind a low-frequency
  approximation.
- **I4 — Local screening anchor:** the Solar System is high-acceleration INSIDE the galactic MOND
  environment ⇒ screening must be controlled by a LOCAL dynamical quantity (acceleration/derivative), not
  environment labels, halo phases, potential-only or velocity-dispersion screening.
- **I5 — Newtonian recovery:** y≫1 → GR with exponentially small corrections; regular limit. No singular
  1/y factors to repair perturbative order unless the full nonlinear theory proves them removable.
- **Numbers (locked):** a₀=κc√(Gρ_Λ)=9.3619e-11 (κ=½ FITTED, Z~21 FITTED — the a₀ reframing is the
  claim, not a derivation). a₀(z)∝√ρ_DE(z) = TARGET/prediction, NOT action-derived.
- **μ realizations (verified):** (A) auxiliary-Legendre χ: V′(χ)=−[ln(1−χ)]², χ=μ(y); primitive
  G(y)=y²+2(1+y)e^{−y}−2 with G′/(2y)=1−e^{−y}. (B) nonlocal F₊(Z)=4[1−(1+√Z/2)e^{−√Z/2}], Z=4y²,
  2F₊′=e^{−y} (`mond_compiler_2026/FROZEN_PRIMITIVE.md`). Constitutive ingredients, not new fields.

## 2. PROHIBITED INGREDIENTS (CLOSED unless a new derivation overturns the no-go)
- **P1 — Quadratic MOND carrier stress:** a carrier lensing only through (DΦDΦ)^TF-type quadratic flux
  vs a linear obstruction. [T3 + order-counting kill a9261161: Σ_P is unique O(ε²,Φ²).]
- **P2 — Unscreened constant preferred-frame coupling:** killed by α₁,α₂. The viable pattern is
  **α_PF ∝ 1−μ = e^{−y}** (or a proven equivalent). [AeST α₂∝1/K_B; disformal α₂∝φ̇_c².]
- **P3 — Lapse-weighted MOND destroying the constraint algebra** (H_perp demoted → unwanted scalar).
  [φ=lnN and sf42 both leaked → 3 DOF + strong coupling.]
- **P4 — Hidden propagating scalar:** "auxiliary"/"nonlocal" by NAME doesn't count — must demonstrate no
  independent canonical initial data. A localization trick does not remove a physical scalar.
- **P5 — Ghost by negative spectral residue:** negative kinetic eigenvalue/residue = kill unless a full
  constrained analysis proves the variable nonphysical.
- **P6 — Temporal nonlocality as a free escape:** spatial elliptic nonlocality is admissible research;
  □⁻¹_ret needs an explicit causal construction + phase-space analysis. [Banked: ω²=½c²k² warning.]
- **P7 — Screening that kills the kinetic term:** if α→0 simultaneously sends the scalar kinetic
  normalization →0, treat as STRONGLY COUPLED unless an independent finite normalization is shown.
  [The khronometric survivor's exact open wound.]

## 3. ACCEPTABLE PROTEINS
- **A1 — Constraint-first dynamics:** MOND as a gravitational constraint (q=−⅙ ln det γ,
  C_M = D_i[μ(y)D^i q]−source ≈ 0); generic branch gives a second-class pair + 2 tensor DOF. Branch-
  restricted; never promote to a global theorem without the open checks (foliation, matter, cosmology).
- **A2 — Auxiliary-Legendre χ** (see I5/μ-realizations).
- **A3 — Preferred frame, IF screened:** allowed when observables are screened (α_PF ~ e^{−y}); **MANDATORY
  DESIGN PRINCIPLE: PPN-visible coupling ≠ kinetic normalization** — the same coefficient must not control
  both (else P7).
- **A4 — Spatial trace-free tensors:** allowed to solve a genuine constraint problem, NOT to manufacture
  lensing; check G0 weak-field order BEFORE building the action. [Q_ij second-class removal is proven.]
- **A5 — Spatially nonlocal elliptic operators:** (−D²)⁻¹, f(−D²/a₀²) — elliptic, no temporal mode,
  controlled GR limit. NOTE: changes momentum scaling, NEVER perturbative amplitude order.

## 4. THE CORE COOKING RULE
**MOND strength ≠ lensing carrier ≠ propagating-scalar normalization** — unless a derivation proves
identifying them creates no instability. (The central lesson of the whole program: AeST identified the
first two and died at α₂; khronometric identifies the last two and risks strong coupling.)

## 5. REQUIRED GATES (in order; STOP at the first kill, record the structural reason)
- **G0 Structural order:** Φ→εΦ; order every proposed source. Different-order terms cannot cancel for
  arbitrary weak fields without an independently justified singular mechanism.
- **G1 Exact MOND reduction:** ∇·[μ∇Φ]=4πGρ over the full MOND domain (no isolated-point fits).
- **G2 Newtonian/GR limit:** regular, G_eff/G_N=1 with NO rescaling repair.
- **G3 Tensor sector:** explicit quadratic action; Q_T>0, c_T²=1.
- **G4 DOF:** actual Hamiltonian/characteristic analysis. Never infer DOF from appearance.
- **G5 Ghost/gradient:** K_i>0, c_i²>0 for every propagating mode (or an explicitly justified limit).
- **G6 Lensing:** derive Φ,Ψ; MOND-enhanced dynamics AND lensing; clean target Φ=Ψ.
- **G7 PPN:** compute γ,β,α₁,α₂,α₃ explicitly. Never infer α₂=0 from "no explicit vector."
- **G8 Strong coupling:** canonically normalize; compute Λ_sc on the ACTUAL Solar-System background;
  require Λ_sc ≫ E_relevant. A vanishing kinetic coefficient is not rescued by a large sound speed.
- **G9 Matter consistency:** full relativistic conservation, not just the Newtonian-limit check.
- **G10 Cosmology:** FLRW, a₀ behavior, cosmological G, perturbations, growth, CMB/ISW, k=0 branch.
- **G11 Strong field:** compact objects, BHs, caustics, nonlinear continuation where demanded.
- **G12 Radiative/naturalness:** is the screening relation technically stable or fine-tuned?

## 6. VERDICT VOCABULARY (exactly one per result)
**PASS** (explicitly established) · **OPEN** (survives prior gates, not yet computed) · **CONDITIONAL**
(works on a stated branch/domain) · **KILL** (demonstrated failure) · **DEAD CLASS** (structural proof
eliminates a family). Never call a candidate "viable" while OPEN or CONDITIONAL.

## 7. DISCOVERY ALGORITHM
Ingredients → G0 → G1 → … → G12. First kill ⇒ stop spending, record the reason, then **alter the
architecture, not a coefficient** (unless the failure is provably coefficient-specific).

## 8. GLOBAL DESIGN TARGET
One metric; μ=1−e^{−y}; correct MOND dynamics + lensing; c_T=1; no ghost; no gradient instability;
acceptable PPN; Λ_sc≫E; healthy matter + cosmology. **The DOF count is NOT frozen in advance — 2, 3, or
more is a RESULT, not an input.** (Forcing N=2 repeatedly killed mechanisms with coherent routes to
lensing + screening.)

## 9. CURRENT PROGRAM STATUS (2026-08-29)
**Master no-go (DEAD CLASS, exhaustive):** {local, ≤2-deriv, single-metric, correct MOND lensing} ⇒
{unremovable preferred-frame carrier}. 108k-candidate search, zero survivors; unique lensing fix =
Bekenstein's disformal (M5/M1=4.000000, rediscovered by root-finding); cancellation ∝A_0², frame not
removable. `mond_compiler_2026/CAPSTONE_PINCER.md`. ⇒ the 2-DOF/no-frame dream is dead; escapes = screen
the frame (A3/P2 pattern) or leave locality (A5).

**⭐ Current best candidate — khronometric/Hořava + MOND (self-screened), CONDITIONAL:**
`L = N√γ[K_ijK^ij − λ_K K² + R³ + η a²] − N√γ V(χ) + S_m[g,ψ]`, η=2(1−χ)=2e^{−y}, β=0, λ_K≠1.
(`theory_discovery/KHRONOMETRIC_MOND_GAUNTLET.md`, 35/35, BPS-anchored.)
| Gate | Verdict |
|---|---|
| G3 c_T=1 | PASS (proven; β=0 forced) |
| G6 lensing Ψ=Φ boosted | PASS (γ_PPN=1; NOT the ×2 under-lens) |
| G7 α₁=−8e^{−y}, α₂≈−e^{−y} | PASS structural (MOND-off ⇒ α≡0; const λ_K adds nothing unscreened) |
| G5 khronon health | PASS on 1<λ_K≤1.10 (BBN-narrowed) |
| G4 DOF | =3 (2 tensor + 1 khronon; H_perp 2nd class, Hořava-class) |
| 🔴 G8 Λ_sc as η→0 | **OPEN — THE make-or-break** (c_s²→∞; P7 risk; same wall as AeST c_s²~1/K_B) |
| 🔴 kernel-dependence | screening NEEDS the exponential kernel (μ_n gives α₂~7e-6 @Neptune, 60× over) |
| 🔴 Cassini Q₂ / G9–G12 | UNTESTED |
**Next architecture must separate: screened PPN response ⟂ finite kinetic normalization (A3 principle).**

**Live alternative — nonlocal DEFW/F₊ (aether-free):** evades the master no-go via A5; PASS: MOND, BTFR,
spherical lensing, c_T=1 (TT quadratic); OPEN: localization→G4→G7→G10 (P4/P6 apply; ω²=½c²k² warning).
`mond_compiler_2026/FROZEN_PRIMITIVE.md`.

## 10. GRAVEYARD (DEAD — never re-cook; the reason is the lesson)
| Architecture | Killed by | Ref |
|---|---|---|
| FC-AeST + c₂★ (6-DOF aether) | α₂=1+2/K_B~8e4 (λ_s=1); α₁~−2.7 | 66cf94e5, FC_AEST_STATUS.md |
| 2-DOF MMG constraint-first (lapse) | γ_PPN=0, α₁=+4, α₃=−1, matter non-conservation | REFEREE_REPORT_FINAL.md |
| Disformal scalar (TeVeS-no-vector) | under-lenses; α₂∝φ̇_c² unprotected | 4ccc9f27 |
| ZMBC auxiliary-σ Legendre | μ+2sμ′=0 ⇒ μ∝s^{−1/2} only | (sympy) |
| Local aux-carrier Q+(∇Φ∇Φ)^TF+R^TF | G0: Σ_AR O(ε³) vs Σ_P O(ε²); Σ_RR spin-0 only | a9261161 |
| TTA-1 as-written (B from χΦ′) | under-lenses ×2 (Ψ tied to un-boosted g_N) | TTA1_AND_SELFSCREEN.md |
| UV-deformed AeST (λ_∞~10⁸) | needs β₀~1e-8 vs fold β₀_min=0.533; placement pincer | (documented) |
| CCG curvature-ratio | Ostrogradsky; ratio singularity; tidal≠acceleration | (documented) |
| Minimal AC-MOND (aux connection) | regular branch A_μ=0 ⇒ carrier off | (sympy) |
| Whole local no-frame class | the 108k master no-go | 9c52966f |

## 11. THE "EXTRA CRISPY" RULE
Never "we found the new theory" → **"we found the next architecture."** Never "no ghost" → **"no ghost in
the tested sector."** Never "viable" until every mandatory gate is PASS. The objective is not to protect a
candidate; it is to kill everything that cannot work until the first thing that survives is left standing.
**That survivor gets the name.**
