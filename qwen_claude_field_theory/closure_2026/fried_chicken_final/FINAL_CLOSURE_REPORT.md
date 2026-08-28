# FINAL_CLOSURE_REPORT — Four-Architecture Filter + Winner Closure

**Date:** 2026-08-28. **Frozen kernel (shared by all four):** μ_10(y)=y/(1+y^10)^(1/10);
as AeST free function F_M = a0² J_10(√Y/a0), deep-MOND F_M ~ (2/3a0)Y^{3/2}, δ²F_M = 0.
**Basis-class labels:** THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED.
**On any FAIL:** cause classified HOST | KERNEL | COUPLING | CONSTRAINT-ARCHITECTURE.

**Re-run THIS session (exit 0):** fc_no_go_Hperp_unsources_Phi.py (12/12); fc_flrw_ir_sign_certificate.py
(20/20); fc_ctensor_map_2026.py (ALL PASS); fc_nonspherical_lensing_slip_2026.py (14/14); fc_A_certificate.py
(CERT1/CERT2); fc_C_laplacian_orthogonality_certificate.py; gate_lensing_weakfield_derivation.py (γ_PPN=0,
43,479σ); ppn_mmg_gate_2026.py (α_1=+4, α_3=−1, γ=0, β=1, kernel-indep <1e-19).

---

## 1. Verdict at a glance

| Arch | Overall | Died / blocked at | Failure class |
|------|---------|-------------------|---------------|
| **A** AeST + J_10 | **CONDITIONALLY-VIABLE (winner)** | blocked from closure at Gate 14 FLRW IR-sign (finite-k), α_2, c_s² | HOST (all three), none KERNEL |
| **B** constraint-first MMG + μ_10 | STRUCTURALLY-DEAD | Tier 1 / Tier 6 | CONSTRAINT-ARCHITECTURE |
| **C** Laplacian-auxiliary MMG + μ_10 | STRUCTURALLY-DEAD | Tier 1 / Tier 6 | CONSTRAINT-ARCHITECTURE |
| **D** BIMOND + DBI/khronon | STRUCTURALLY-DEAD | Tier 1 (cosmology sum-rule) | HOST |

Ranking: **A > B > C > D.** B > C because C = B + a Laplacian completion that the no-go proves is
Fourier-orthogonal to the Φ-sourcing sector (cannot help). D last: dead by a separate parameter-free
sum-rule theorem with DOF/c_T/PPN largely OPEN-adverse.

---

## 2. Architecture A = AeST + J_10 (WINNER, CONDITIONALLY-VIABLE)

| # | Gate | Status | Basis | Class | Evidence |
|---|------|--------|-------|-------|----------|
| 1 | Action well-posed | PASS | DERIVATION | — | AeST + additive a0²J_10(√Y/a0), single frozen fn, a0 const |
| 2 | DOF = 6 | PASS | EXTERNAL-INPUT | — | PRD 110.044015 / 2307.15126; FC Y>0 byte-in-class (F_QQ=2K2≠0, F_YQ=0, F_YY>0). NOT re-derived |
| 3 | Legendre regularity | PARTIAL | COMPUTATION | (Y=0 chart) | Y>0: detC ∝ K2/(2a0√Y)≠0. Y=0: aux-chart singularity, H_phys(Y=0)=2(2−K_B)I>0. OPEN: all-branch covariant Dirac theorem |
| 4 | Ghosts | PASS | COMPUTATION | — | δ²S_MOND=0 (CERT2); −(2−K_B)Y seed keeps Y=0 gradient sector positive |
| 5 | Hyperbolicity | PARTIAL | COMPUTATION | HOST | c_T=c_V=1; **quasi-static scalar c_s²∝1/K_B → ~3c** at α_1 ceiling, kernel-indep. Needs derived preferred-frame causal argument. LIABILITY |
| 6 | c_T (GW170817) | PASS | DERIVATION | — | c_T²=1 exact, K_B-/kernel-indep (c1+c3=0; TT=Einstein–Hilbert). ppn_fc8.py, fc_ctensor_map_2026.py |
| 7 | k=0 homogeneous | PASS | DERIVATION | — | Y=0 on FLRW ⇒ J_10 absent; H²=ρ/3+(QK_Q−K)/3, K_Q=I0/a³ dust-like. flrw_fc8.py |
| 8 | Matter consistency | PASS | DERIVATION | — | Minimal/metric coupling; no constraint-architecture deletion (contrast B) |
| 9 | PPN α_1 | OPEN (adverse-lean) | DERIVATION | HOST | α_1 = −4K_B ⇒ K_B < 2.5e-5 (LLR). Bound, not fail. Kernel-indep. fc_ctensor_map_2026.py |
| 10 | PPN α_2 | **OPEN** | OPEN | HOST | Finite (scalar regularises singular pure-vector α_2~1/c123, c123=0 THEOREM); COEFFICIENT uncomputed; O(w²) machine fails own D1/D2 under isotropic ansatz. Adverse-leaning |
| 11 | PPN α_3/γ/β | PARTIAL | DERIVATION | — | γ_PPN=1 derived kernel-indep; α_3, β not adverse; β (2PN) OPEN-benign |
| 12 | Lensing (Φ,Ψ,slip) | PASS | DERIVATION+COMP | — | Φ=Ψ exact non-spherical (14/14); M24 KiDS χ²/dof=0.640 @ canonical a0. No dark-lensing lever/Bullet kill. η(R500)~2 INHERITED not new |
| 13 | FLRW background | PASS | DERIVATION | — | F_MOND=O(δ³) sequestered; const a0 no δ-a0 source; χ clock c_χ=1. Λ=32πa0²/c⁴ MODEL-ASSUMPTION |
| 14 | **FLRW pert / IR (DECISIVE)** | **OPEN** | OPEN | **HOST** | δ²J_10=0 ⇒ IR spectrum J-independent ⇒ HOST. k→0 RESCUED on dS (bounded, χ̇~a⁻³, E~a⁻³→0; 20/20). **Finite-k band H≪k<k_* UNCOMPUTED** — decides PASS vs Mpc-runaway |

**A verdict:** No structural kill. Only architecture clearing Tier 1. Three surviving liabilities (14, 10, 5)
ALL HOST, none KERNEL, and the decisive one (14) is J-independent ⇒ A cannot be killed or rescued by any
kernel move. Structurally alive, un-closed.

### 2b. Winner closure lane (this session's new computations)

| Closure calc | Verdict | Basis | Key result | Certificate |
|--------------|---------|-------|------------|-------------|
| Gate 14 FLRW IR-sign | **PARTIAL** | DERIVATION | k→0 mode RESCUED on dS (bounded, energy redshifts a⁻³). Finite-k band H≪k<k_* OPEN | fc_flrw_ir_sign_certificate.py 20/20 exit 0 |
| PPN α_1 / α_2 | **PARTIAL** | DERIVATION | α_1=−4K_B DERIVED (c-tensor map certified); c_T²=1, γ=1; α_2 finite but coefficient OPEN (D1/D2 fail) | fc_ctensor_map_2026.py ALL PASS; fc_alpha2_preferred_frame_2026.py D1/D2 FAIL (documented) |
| Non-spherical lensing / slip | **PASS** | DERIVATION | Φ=Ψ for generic non-spherical weak source, |γ−1|=O((v/c)²)~1e-6, kernel-indep; KiDS χ²/dof=0.64 reproduced | fc_nonspherical_lensing_slip_2026.py 14/14 exit 0 |

The closure lane **improved** Gate 14 (OPEN→PARTIAL: k→0 rescued) but did **not** close it (finite-k OPEN),
and **derived** α_1 while leaving α_2's coefficient OPEN. Net: A stays CONDITIONALLY-VIABLE.

---

## 3. Architecture B = constraint-first MMG + μ_10 (STRUCTURALLY-DEAD)

| Gate | Status | Basis | Class | Evidence |
|------|--------|-------|-------|----------|
| Action / constitutive C_M | PASS | DERIVATION | — | 01_constitutive.py exit 0 |
| DOF = 2 | PARTIAL | THEOREM | — | 05_dof_count.py 20−12−4=4⇒2 (TT). CONDITIONAL: {D²q,H_i} first-class UNVERIFIED (uncomputed (1/3)D²(D·ξ)) |
| Legendre / rank | PASS | COMPUTATION | — | 09_legendre_check.py, 04_rank_and_ellipticity.py |
| Ghosts (L_N eigenvalues) | PASS | THEOREM | — | 13_kernel_swap_ellipticity.py: μ_10 positive-sweep, exact |
| Hyperbolicity / ellipticity μ_10 | PASS | THEOREM | — | 13: μ_n (n=5,10) satisfies every ellipticity condition |
| c_T | PASS | DERIVATION | — | 05 part E: TT untouched, overlap EMPTY |
| k=0 background | PASS | DERIVATION | — | sf54: Friedmann first-class, CMC clock a0(z)=a0,0 H(z)/H0 |
| **Matter conservation** | **FAIL** | DERIVATION | **CONSTRAINT-ARCH** | gate_matter_conservation_derivation.py: ∇_μT^{μi}=−ρD^iX at NEWTONIAN order; 1 AU anomaly 1.62e11× Sereno-Jetzer. Kernel-blind (μ(∞)=1) |
| **PPN α_1,α_2,α_3,β** | **FAIL** | DERIVATION | **CONSTRAINT-ARCH** | ppn_mmg_gate_2026.py 34/34: α_1=+4 (4e4× bound), **α_3=−1 (2.5e19× pulsar)**, α_2=0, β=1; kernel-indep <1e-19 (μ_5, μ_10 explicit) |
| **γ / lensing (Φ,Ψ,slip)** | **FAIL** | DERIVATION | **CONSTRAINT-ARCH** | gate_lensing_weakfield_derivation.py: D²q=0⇒Φ=0⇒γ_PPN=0; deflection ratio 0.5000 all 6 kernel×footing; Cassini 43,479σ; M24 Δχ²+403…+498 |
| FLRW background | PARTIAL | DERIVATION | HOST | sf54: a0-blind (a0=cH_Λ/Z not realized dynamically), sign-indefinite dust-like E |
| FLRW pert / IR | OPEN | MODEL-ASSUMPTION | HOST | 14_flrw_perturbations.py: μ(0)=0 empties linear scalar sector; nonlinear solver needed |
| Kernel-blindness cert | PASS | THEOREM | — | FC_B_kernel_blindness_cert.py: all 3 FAILs invariant μ_exp→μ_10, all CONSTRAINT-ARCH |

**B verdict:** THREE kernel-blind observational FAILs (γ_PPN=0 ~20σ, α_3=−1, Newtonian-order matter
non-conservation), all traced to the H_perp-deletion that buys the 2-DOF count. NOT μ_10 problems.

---

## 4. Architecture C = Laplacian-auxiliary MMG + μ_10 (STRUCTURALLY-DEAD)

| Gate | Status | Basis | Class | Evidence |
|------|--------|-------|-------|----------|
| k=0 / cosmology | PASS | DERIVATION | — | sf54: D² annihilates k=0, only π_N survives, first-class Friedmann |
| Laplacian multiplier orthogonality | PASS | THEOREM | — | fc_C_laplacian_orthogonality_certificate.py: supp{m=0}={k=0} disjoint from {k≠0}; λ~−S0/k² singular |
| **k≠0 lensing / γ_PPN** | **FAIL** | DERIVATION | **CONSTRAINT-ARCH** | gate_lensing_weakfield_derivation.py: −k²q=0⇒Φ=0⇒γ=0; M24 Δχ²+403…+498; Cassini 43,479σ; μ_10-blind (0.5000 all cells) |
| **α_3** | **FAIL** | DERIVATION | **CONSTRAINT-ARCH** | ppn_mmg_gate_2026.py: α_3=−1 (2.5e19× pulsar); d(α_3)/d(Laplacian mult)=0 ⇒ D²-completion cannot touch it |
| c_T = 1 | OPEN | EXTERNAL-INPUT | — | 2026 Laplacian-MMG viable subclass reported c_T>1; not reproduced in-repo. Does not change verdict (already dead) |
| 2-DOF certificate | PARTIAL | OPEN | — | REFEREE_REPORT_FINAL.md: {D²q,H_i} first-class UNVERIFIED |

**C verdict:** C = B + a Laplacian completion proven Fourier-orthogonal to the Φ-sourcing sector ⇒ inherits
B's kills, repairs none. The named within-family repair S_2′=D²(q+lnN) restores γ_PPN=1 but does NOT fix
α_3 (sourced by the elliptic C_M lapse response, which S_2′ never touches) and demands a full new Dirac
re-certification for {π_N, S_2′}=−D²(·/N)≠0 — a new program, not C.

---

## 5. Architecture D = BIMOND + DBI/khronon (STRUCTURALLY-DEAD)

| Gate | Status | Basis | Class | Evidence |
|------|--------|-------|-------|----------|
| R1 (free fn eats local total field) | PASS | DERIVATION | — | DOI 22015358 construction-level |
| R3 (no G̃/G_N split) | PASS | DERIVATION | — | DOI 22015358 |
| Ephemeris / solar gap | PARTIAL | COMPUTATION | — | 1-AU anomaly 1e-3458.7; interpolation-dependent, robustness UNVERIFIED |
| DOF / Boulware-Deser | OPEN | OPEN | — | BD UNCHECKED; sf12 12/12: only lapse-degeneracy route replaces BIMOND with Hassan-Rosen; sf44 demoted DW "det=−b²" |
| c_T = 1 | OPEN-ADVERSE | COMPUTATION | COUPLING | c_T²−1=+3.9e-2 for DW-chassis khronon; NOT computed for BIMOND host; transfer UNPROVEN |
| **FLRW cosmology / Ω_dm** | **FAIL** | THEOREM | **HOST** | route6_bimond_twin_2026.py 30/30: F_TM=1−ν≤0, sum rule F_b+F_TM=1≠2 ⇒ twin sector cannot carry Ω_dm to CMB. Parameter-free |
| FLRW dS point | OPEN | OPEN | — | No BIMOND-native no-dS script; DW property not located for host |
| PPN | OPEN | OPEN | — | not computed |
| Combined-limit lensing Φ+Ψ | OPEN | OPEN | — | STANDING owed #2 |
| Boltzmann | OPEN | OPEN | — | STANDING owed #1 |
| F(A²) 2T+1S no-go (E01) | OPEN | OPEN | HOST | not evaluated for D's khronon |

**D verdict:** Dead at Tier 1 by the parameter-free sum-rule theorem (twin sector adds nothing; Ω_dm reverts
to DBI-khronon dust). DOF/c_T/PPN largely OPEN or adverse. Last place.

---

## 6. Host-vs-Kernel accounting (mission §5)

Every failure classified. **The frozen kernel μ_10 causes NONE of the kills.**

- **B/C γ_PPN=0, α_3=−1, matter non-conservation:** CONSTRAINT-ARCHITECTURE (H_perp deletion). Kernel-blind
  to <1e-19 (proven, μ_5 & μ_10 explicit). J_10 swap leaves all three invariant.
- **A Gate-14 IR mode:** HOST (AeST aether/K2). Proven J-INDEPENDENT (δ²J_10=0, CERT2).
- **A α_2, c_s²∝1/K_B:** HOST (K2/aether). Kernel-blind.
- **D Ω_dm sum-rule:** HOST (bimetric twin structure). Parameter-free, kernel-independent.

Conclusion: the MOND kernel is **not** the obstruction in any architecture. Each architecture lives or dies
on its **constraint architecture / host DOF structure**, exactly the level at which A (keep H_perp, pay 6 DOF)
differs from B/C (delete H_perp, buy 2 DOF).

---

## 7. Overall program verdict — INCONCLUSIVE

- **Not FRIED-CHICKEN-CLOSED:** the winner's decisive gate (Gate 14 finite-k FLRW IR sign) is OPEN and can
  still go either way; α_2 coefficient uncomputed; superluminal quasi-static scalar unresolved. Declaring
  these PASS would violate the honesty rules.
- **Not FRIED-CHICKEN-CONDITIONALLY-CLOSED:** that label is licensed ONLY when the sole remaining input is
  genuinely phenomenological (e.g. a0=½c√(Gρ_Λ)) hiding no unresolved consistency condition. Here there are
  THREE genuine unresolved consistency conditions (Gate 14 finite-k, α_2, c_s²) — not inputs. Disallowed.
- **Not BURNED-NO-VIABLE-THEORY:** A survives the entire Tier-1 filter that kills B/C/D, plus c_T=1, γ_PPN=1,
  Φ=Ψ, KiDS χ²/dof=0.64, FLRW background. A viable-conditional survivor exists.
- **Not (whole-program) NO-GO-THEOREM:** the proven H_perp-deletion no-go eliminates only the constraint-first
  2-DOF branch (B, C). A escapes it by construction (retains H_perp). The program does not terminate in a
  universal impossibility.

**Verdict: INCONCLUSIVE.** Winner A = AeST + J_10 is the unique conditionally-viable survivor; the
constraint-first branch is eliminated by a proven structural no-go; D is dead by a parameter-free cosmology
theorem. Closure of A hinges on ONE decisive number — the sign of the low-k scalar Hamiltonian on the FLRW
(not Minkowski) background in the finite-k band H ≪ k_phys < k_* — which no committed computation yet fixes.
