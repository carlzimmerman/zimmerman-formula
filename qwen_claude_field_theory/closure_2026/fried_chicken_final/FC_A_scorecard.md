# FC Architecture A = AeST (Skordis–Zlosnik) + J_10 — Scorecard

Adversarial score, 2026-08-28. Hard-gate order; eliminate on the earliest irreparable structural fail.
Basis-class per gate: THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED.
On any FAIL, cause is classified HOST | KERNEL | COUPLING | CONSTRAINT-ARCHITECTURE.

Frozen kernel: `mu_10(y)=y/(1+y^10)^(1/10)`; as AeST free function `F_M=a0^2 J_10(sqrt(Y)/a0)`,
deep-MOND `F_M ~ (2/(3 a0)) Y^{3/2} = O(Y^{3/2})`.

Reproduced THIS session (both exit 0):
- `closure_2026/FC_AEST/scripts/fc_lensing_rar_mu10_2026.py` → gamma_PPN=1, Phi=Psi, M24 KiDS chi2/dof=0.640 @ canonical a0=9.36e-11 (B21 set 2.843).
- `closure_2026/FC_AEST/scripts/fc_flrw_quadratic_gate.py` → F_MOND=O(delta^3); chi clock c_chi=1; c_T=1 inherited; AeST low-k liability inherited-open.
- `fried_chicken_final/fc_A_certificate.py` (this lane) → CERT1 kernel-regularity PASS; CERT2 delta^2 S_MOND=0 for arbitrary J (J-independence) PASS.

| # | Gate | Status | Basis | Failure-class | Evidence / note |
|---|------|--------|-------|---------------|-----------------|
| 1 | Action well-posed | PASS | DERIVATION | NONE | AeST action + additive `a0^2 J_10(sqrt(Y)/a0)` in the Y-sector; single frozen constitutive function, a0 a constant. |
| 2 | DOF count | PASS | EXTERNAL-INPUT | NONE | 6 physical DOF from the published AeST general-F theorem (PRD 110.044015 / 2307.15126). NOT re-derived here. FC's Y>0 branch is byte-in-class (F_QQ=2K2≠0, F_YQ=0, F_YY finite>0). |
| 3 | Legendre regularity | PARTIAL | COMPUTATION | (Y=0 chart only) | Generic Y>0: det C ∝ K2/(2 a0 sqrt(Y)) ≠ 0 (proven-in-class, `detC_legendre_regularity.py`). Y=0: `det C_aux→0` is a singularity of the auxiliary Legendre CHART, not the physics — physical gradient Hessian H_phys(Y=0)=2(2−K_B)I>0 (`y0_physical_hessian.py`). OPEN residual: formal all-branches covariant Dirac theorem on the singular boundary (referee-vulnerable, not a known pathology). |
| 4 | Ghosts | PASS | COMPUTATION | NONE | No new ghost from J_10: delta^2 S_MOND=0 (CERT2) ⇒ kernel adds nothing at quadratic order; the −(2−K_B)Y kinetic seed keeps the Y=0 gradient sector positive (bare AQUAL would strong-couple, AeST does not). |
| 5 | Hyperbolicity | PARTIAL | COMPUTATION | HOST (if it bites) | Tensor & vector luminal. **Quasi-static scalar `c_s^2 ∝ 1/K_B` → ~3c at the alpha_1/LLR K_B ceiling** — a real superluminal characteristic set by K2, kernel-independent (delta^2 J_10=0). Not auto-excluded (AeST has a preferred foliation; needs a DERIVED global-time causal-structure argument, not asserted). Cause is HOST (K2/aether sector), not the kernel. |
| 6 | c_T (GW170817) | PASS | DERIVATION | NONE | c_T^2=1 exactly, K_B- and kernel-independent (c_1+c_3=0; TT sector = Einstein–Hilbert since F_μν=J=Y=0 on background). `ppn_fc8.py`, `fc_flrw_quadratic_gate.py`. |
| 7 | k=0 / homogeneous consistency | PASS | DERIVATION | NONE | On FLRW Y=0 ⇒ J_10 does not enter the background; H^2=rho/3+(Q K_Q−K)/3, shift charge K_Q=I0/a^3 (dust-like). Clean 3-way sector separation. `flrw_fc8.py`. |
| 8 | Matter consistency | PASS | DERIVATION | NONE | AeST matter coupling is metric/minimal; unlike MMG-B there is no constraint-architecture deletion, so stress-energy conservation is intact (contrast: gate_matter_conservation in B fails at Newtonian order). |
| 9 | PPN alpha_1 | OPEN (adverse-leaning) | COMPUTATION | HOST | alpha_1=−4K_B ⇒ K_B<2.5e-5 (LLR). Kernel-independent (mu_10→1 decouples). Bound on K_B, not yet a fail. |
| 10 | PPN alpha_2 | OPEN (adverse-leaning) | OPEN | HOST | alpha_2 genuinely UNCOMPUTED on the consistent Y≠0 background. The (5/2)K_B empty-corner no-go was REFUTED as a background artifact (typeII 44/44 on the consistent background); but no positive computed pass exists. Needs full coupled A^μ–phi 1PN O(w^2). If it scales with K_B it is a HOST (aether) obstruction, kernel-blind. |
| 11 | PPN alpha_3, gamma, beta | PARTIAL | DERIVATION | NONE | gamma_PPN=1 derived (kernel-independent, even deep-MOND). alpha_3, beta not adverse; beta (2PN) uncomputed but OPEN-benign. |
| 12 | Lensing (Phi, Psi, slip) | PASS | DERIVATION + COMPUTATION | NONE | Weak-field Phi=Psi EXACT and kernel-independent ⇒ no dark-lensing lever, no phantom slip, no Bullet-type kill. Quantitative RAR: M24 KiDS chi2/dof=0.640 @ canonical a0 (reproduced). Do NOT claim canonical fits BETTER than fitted (fit a0=1.35e-10→0.24; anchoring is cheaper, not better). Inherited (not new): standard MOND cluster mass residual η(R500)~2.0 raw. |
| 13 | FLRW background | PASS (new content) | DERIVATION | NONE | Sequestration: F_MOND=O(delta^3) drops from the quadratic FLRW action; constant a0 ⇒ no delta-a0 sourcing; decoupled chi clock canonical (c_chi=1). `Λ=32π a0^2/c^4` is MODEL-ASSUMPTION/INPUT, not derived. |
| 14 | FLRW perturbations / IR | **OPEN — DECISIVE** | OPEN | **HOST** | AeST's known low-k unbounded-Hamiltonian scalar mode (2109.13287, EXTERNAL): Hamiltonian unbounded below for k<k_*, k_*^2=(1+lam_s)/lam_s · mu^2, mu^2=2 K2 Q0^2/(2−K_B). Committed FLRW characterization: SECULAR (linear-in-t), NOT exponential; k_*≤~Mpc^-1 ⇒ plausibly confined to cosmological scales; **FLRW-background sign UNCOMPUTED**. **Failure-class = HOST, PROVEN via J-independence:** delta^2 J_10=0 for arbitrary admissible prefactor (CERT2) ⇒ the quadratic IR spectrum is J-independent ⇒ no kernel choice fixes or worsens it. This is the single calculation that decides A. |

## Verdict

**A = CONDITIONALLY-VIABLE.** No structural kill is produced. Every gate through lensing and the FLRW
background is PASS or PARTIAL-benign; the DOF=6 count is EXTERNAL (not re-derived, so marked EXTERNAL-INPUT,
not a claimed pass). The kernel J_10 is clean where it acts (deep-MOND, lensing) and provably INERT where the
theory is fragile (quadratic spectrum), so J_10 neither causes nor cures any of the three surviving liabilities.

Three surviving liabilities, ALL classified HOST (AeST), none KERNEL:
1. **Gate 14 IR-sign (decisive).** The low-k unbounded-Hamiltonian mode. HOST, proven J-independent.
2. **Gate 10 alpha_2.** Uncomputed, adverse-leaning; HOST (aether/K2 sector).
3. **Gate 5 superluminal quasi-static scalar** (c_s^2∝1/K_B). HOST (K2), needs a derived preferred-frame
   causal-structure argument.

Because all three are HOST and the decisive one is J-INDEPENDENT, A cannot be rescued OR killed by any
kernel move — its fate is set by AeST's own {K_B, K(Q), mu} sector. That makes A structurally alive but
un-closed: viable as a candidate, not a watertight theorem.

## Decisive open

Compute the sign of the low-k scalar Hamiltonian on the **FLRW background** (not Minkowski):
`S_FC → S^(2)_FLRW → K(k,a), G(k,a), M^2(k,a) → omega^2(k,a) → IR sign` in the three limits
k≫aH, k~aH, k≪aH, for a DESI-compatible K(Q)/rho(z) trajectory. Minkowski says "unbounded for k<k_*";
whether the expanding background lifts it to bounded/secular-but-harmless is the one number that decides A.
Kernel-blind by CERT2, so the answer is a property of the AeST host alone.
