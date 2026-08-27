# Carrier No-Go Theorems for Two-Degree-of-Freedom MOND: the F(A²) Class, the Auxiliary-Legendre Escape, and a Hamiltonian Audit of Causal Nonlocal MOND

**Carl Zimmerman** (with AI-assisted derivation and verification; all load-bearing claims backed by
committed runnable scripts in `github.com/carlzimmerman/zimmerman-formula`)

**Date:** 2026-08-27

## Abstract

We prove three structural results on where a MOND-type modification can and cannot live inside a
gravitational theory with exactly two local propagating degrees of freedom (DOF). **(1)** For the
single-invariant khronon carrier L = a₀²F(A²/a₀²), A_μ the acceleration of a hypersurface-orthogonal
preferred foliation, the khronon velocity-Hessian kernel is Z_ij = F′δ_ij + (2F″/a₀²)ā_iā_j with
det Z = F′²(F′+2sF″). A genuine constant-rank scalar-removing degeneracy forces F′ = F″ = 0, hence
F = const: **no nontrivial MOND carrier of this class removes the scalar** — wherever MOND is active
(μ<1), Z_⊥ = 2(1−μ) > 0 and the khronon propagates. The result persists on expanding (FLRW) and
shearing (Bianchi-I) backgrounds, where θ and σ are invariants orthogonal to A²; isolated zeros of
Z_∥ are strong-coupling surfaces, not Dirac constraints. This explains structurally why published
relativistic khronon MOND carries a third mode. **(2)** The same nonlinearity is *curative* one door
over: the auxiliary-Legendre pair L = −χ|DΦ|² − V(χ), with V the Legendre dual of any monotone μ,
has Dirac Pfaffian N√h[2(ḡ·k)² − V″χk²] > 0 for all k (V″ = −2a₀ḡ/μ′ < 0), i.e. two genuine
second-class pairs and **zero propagating DOF** — MOND in a constraint bracket instead of a kinetic
Hessian. **(3)** We give the first canonical (ADM/Dirac–Bergmann) audit of the 2026 causal-nonlocal
MOND architecture (Deffayet–Woodard type): the full localized theory counts 2 tensor + 2 scalar
modes, one scalar being the localization ghost — the (U,ξ) kinetic block [[a,b],[b,0]] has
det = −b² < 0 on every background; the retarded/fixed-IC prescription removes the ghost's free
Cauchy data at linear order but is a boundary prescription, not a Dirac constraint. We further prove
the nonlocal invariant Z[g] localizes to the total field strength in a bound system embedded in an
external field (nonlocal remnants ≤8%), so the external-field quadrupole applies with 1−μ at
y_ext ≈ 1.9: the exact-exponential branch yields Q₂ ≈ 2×10⁻²⁶ s⁻², failing the 2026 Cassini ceiling
by 10–14σ — the decisive, structural kill of the branch, on a gate the published construction
defers. Its cosmological branch is w = 0 dust with a₀ provably free (a reverse-arrow theorem: any
de Sitter point fixes H*/a₀ from the shape of f, so ρ_DE follows from a₀, never conversely); on
FLRW the double-timelike projection R_{μν}u^μu^ν gives an α_T-type tensor operator with
c_T²−1 ≈ +4×10⁻² (a GW170817 conflict, modulo one unverified cancellation), while c_T = 1 holds
exactly on Minkowski. Favorably, the cosmology↔MOND crossing Z = 0 is regular in the physical field
including the transport sector. Every claim is
PROVED/DERIVED at the stated scope; none extends to multi-invariant carriers, extra-field
completions, or twisting congruences, which remain open.

## 1. Setup and conventions

Signature (−,+,+,+). Preferred foliation with unit normal u_μ = −∂_μφ/√(−(∂φ)²);
acceleration A_μ = u^ν∇_νu_μ; in unitary gauge A_i = D_i ln N, A² = |D ln N|². MOND interpolation
μ(x), x = g/a₀, with μ→x (deep MOND), μ→1 (Newtonian). a₀ = 9.36×10⁻¹¹ m/s². Throughout, κ = ½ and
Z ≈ 21 in a₀ = κc√(Gρ_Λ) = cH_Λ/Z are FITTED/postulated, never derived; nothing below depends on
that normalization.

## 2. Theorem 1: the F(A²) no-go

**Statement.** Let S = (M_Pl²/2)∫N√h[K_ijK^ij − λK² + ξ³R] + ∫N√h a₀²F(A²/a₀²) + S_m, with F local,
C², and the foliation hypersurface-orthogonal. If F yields a nontrivial MOND interpolation
(μ = 1 − F′/2 with μ<1 on an open set), the theory propagates 2 tensor + 1 scalar. No F yields a
genuine, background-persistent (constant-rank) Hessian degeneracy that removes the scalar while
retaining MOND.

**Proof sketch (scripts sf40, sf41, sf42_flrw).** Restoring the khronon (φ = t+χ) on a background
with ā_i ≠ 0, the χ̇-sector Hessian kernel is

  Z_ij = F′(s)δ_ij + (2F″(s)/a₀²)ā_iā_j,  s = A²/a₀²,

eigenvalues Z_⊥ = F′ (×2), Z_∥ = F′+2sF″; det Z = F′²(F′+2sF″). The bare χ̇² (k→0) coefficient is
identically zero and χ̈² cancels (no Ostrogradski). A constant-rank degeneracy on an open region
requires Z_⊥ = Z_∥ = 0 identically ⇒ F′ ≡ F″ ≡ 0 ⇒ F const. With the AQUAL identification
F′ = 2(1−μ): Z_⊥ = 2(1−μ) > 0 wherever μ<1 — the scalar propagates across the entire MOND regime.
The weakest (parallel-only) degeneracy ODE F′+2sF″ = 0 has only F = C₁+C₂√s, whose F′(0) = ∞
violates the deep-MOND boundary condition. Isolated zeros of Z_∥ at field values s* are
strong-coupling loci (rank non-constant, kinetic Hamiltonian diverges, Λ_sc ~ Z_∥^{3/4}→0), not
constraints. Kernel-dependent corollary: μ = x/√(1+x²) and μ = 1−e^{−√y}-type kernels have Z_∥ < 0
windows (longitudinal gradient ghost) at g ~ a₀; the a₀-line and simple kernels stay Z_∥ > 0.

**Adversarial robustness (workflow-verified, 4 independent attacks).** (i) No hidden constraint:
the removal requires the k²-entry {p_N,Φ_N} ∝ F′ to vanish, matching the linear-carrier anchor
A = 2ηk² (η=0 ⇔ GR). (ii) Boundary terms: the dropped cross term is a k⁰ mass shift, not a
principal-symbol shift. (iii) FLRW: ȧ cancels from a_μ identically; θ is orthogonal to A². (iv)
Bianchi-I shear: K_ij-blind; only openable by leaving the single-invariant class. **Scope:** local,
regular, hypersurface-orthogonal, single-invariant. Explicitly NOT covered: F(A²,K,σ²,D_ia^i),
extra fields, twisting congruences (ω≠0).

**Context.** This is why the relativistic khronon construction of Blanchet–Skordis carries three
dynamical modes: the nonlinear MOND terms are exactly the F″≠0 structure that forbids the
degeneracy. Independently, the spatially-covariant-gravity literature (arXiv:2604.14490 §III.2)
finds the admissible two-DOF cubic branches are acceleration-free; Theorem 1 is the quadratic-order
mechanism behind that statement.

## 3. Theorem 2: the auxiliary-Legendre escape (0-DOF MOND carrier)

**Statement.** L_M = −(1/8πG)N√h[χD_iΦD^iΦ + V(χ)] with χ,Φ auxiliary and V the Legendre dual of a
monotone interpolation (δχ: V′ = −|DΦ|²; δΦ: D_i(χD^iΦ) = 4πGρ ⇒ χ = μ(g/a₀), the AQUAL law) has
exactly zero propagating DOF: its four constraints (p_χ, p_Φ, and their secondaries) form two
second-class pairs with Dirac Pfaffian

  Pf = N√h[2(ḡ·k)² − V″(χ̄)χ̄k²] > 0 for all k ≠ 0,

since the Legendre relation forces V″ = −2a₀ḡ/μ′ < 0 for any μ′ > 0. (Script sf42.)

**Interpretation.** The identical nonlinearity that is fatal in a kinetic Hessian (Theorem 1) is
curative in a constraint bracket: V″ ≠ 0 makes {p_χ, ψ_χ} invertible and removes χ. This is the
structural door through which any two-DOF MOND completion must pass. The gravitational chassis it
must be attached to is treated in the companion paper.

## 4. Hamiltonian audit of causal nonlocal MOND (Deffayet–Woodard class)

The 2026 causal nonlocal construction (S = S_GR − (a₀²/16πG)∫√−g M[g]; clock (∂φ)² = −1 with fixed
initial data; U = □_ret⁻¹(R_{μν}u^μu^ν); Z ∝ (∂U)²; M by first-order transport sourced by f(Z)) is
the first equation-level architecture interpolating cosmology → MOND+lensing. We audited it
canonically; the published work contains no Hamiltonian analysis. Results (each with committed
scripts; exact-exponential branch f₊ with μ = 1−e^{−y} used where a branch choice is needed):

**4.1 Localization ghost (canonical count) and a proof the retarded prescription is not a Dirac
constraint.** Localizing □⁻¹ with multiplier ξ, the (U,ξ) kinetic block is [[a,b],[b,0]], b = √h ≠ 0,
det = −b² < 0 on every background and undegenerable by f(Z): the full Dirac–Bergmann count is
2 tensor + 2 scalar, one scalar a ghost. The clock pair (φ,λ) and transport pair (M,ν) are
second-class, 0 DOF. At linear order the retarded/fixed-IC prescription leaves the ghost
combination with zero independently-specifiable Cauchy data (Minkowski and FLRW). However, we prove
numerically that the retarded prescription is HISTORY-dependent — an identical local germ at t₀
yields O(1)-different retarded data (δU(0) = −1.39 vs δU̇(0) = −0.40 in the test configuration) — so
it is provably NOT a phase-space (Dirac) constraint: the ghost is demoted (no free retarded data)
but survives in phase space. The missing object that could upgrade this to a certificate is a
Schwinger–Keldysh/Galley doubled-phase-space construction; absent that, no canonical 2-DOF
certificate exists. (Scripts sf43, sf44; full-DOF gate.)

**4.2 External-field localization theorem ⇒ the Cassini kill (the decisive gate).** In a bound
system embedded in a long-wavelength external field, on the static slice □⁻¹ = −∇⁻² is self-adjoint
and Z[g] localizes (vary-first, under the causal IVP) to 4(g_total/a₀)²; the genuine nonlocal
remnants — the causal t=0 tail (~10⁻³⁰) and eikonal-u tilt (≤8%) — are far below the ~75–82%
destructive cancellation a Cassini pass would require, so the nonlocality supplies NO escape. The
EFE quadrupole is therefore governed by 1−μ at the EXTERNAL field y_ext = g_ext/a₀ ≈ 1.9 (Milky Way
at the Sun), not the planetary field: for μ = 1−e^{−y}, 1−μ(y_ext) ≈ 0.15 is unscreened, and the
exponential's strong-field suppression (e^{−7×10⁵} at Saturn internally) is irrelevant. Result:
Q₂ = 2.0×10⁻²⁶ s⁻² (canonical a₀) / 2.4–2.6×10⁻²⁶ (alt) versus the 2026 Cassini 2σ ceiling
5.2×10⁻²⁷ s⁻² — a FAIL by ×3.8–5.0, i.e. 10–14σ (two independent quadratures agreeing to 2–7%;
consistent with Desmond–Hees–Famaey 2024). The published construction defers exactly this gate.
The obstruction is STRUCTURAL: any interpolation kept MOND-active in galaxies (y ≲ 1) leaves an
O(0.1–0.6) unscreened response at y_ext ≈ 1.9. Kernels with sharp power-law approach μ_n, n ≳ 5,
clear the same bound at a stated RAR cost (companion paper).

**4.3 Cosmological branch is dust; a₀ is provably free (reverse-arrow theorem).** On FLRW, Z ≤ 0
always and the transport gives M = −f(Z) + K/a³. The K/a³ term is a conserved charge redshifting as
matter: w = 0. The architecture's homogeneous component mimics dark MATTER, not dark energy; the
initial-data constant reproduces ρ₀ = 45a₀²/16πG as K = 6Ω_dm(cH₀/a₀)². Moreover a reverse-arrow
theorem holds: at any de Sitter fixed point the ratio H*/a₀ is a pure number set by the SHAPE of f —
the construction determines ρ_DE FROM a₀, never a₀ from ρ_DE. A relation a₀² = κ²c²Gρ_DE therefore
cannot derive on this chassis; "κ" would merely BE the fitted f-shape number (here κ_fit ≈ 0.64,
not ½). a₀ is a free parameter and a₀ ~ cH₀ remains an input coincidence.

**4.4 Favorable: crossing regularity.** The apparent f_ZZ ~ Z^{−1/2} divergence at the
cosmology↔MOND crossing Z = 0 is a Z-coordinate artifact: since δZ ∝ √Z̄∂δU, the physical quadratic
coefficient is C = −(κ/2)√Z̄e^{−√Z̄/2} → 0, and with the transport-M sector included the reduced
kinetic matrix is continuous (C¹ join, bounded 1/8 kink, no pole). The weak-field static sector of
the exact-exponential branch is elliptic everywhere: μ>0 and μ+yμ′ = 1−(1−y)e^{−y} > 0 for all
y > 0 — and we note the identity μ+yμ′ = 1−2(f′+2Zf″), so f′+2Zf″ < 0 (Z>4) is NOT an instability.
(Script verify_stability_and_crossing.py; scalar-sector gate.)

**4.5 Tensor sector: c_T = 1 on Minkowski only.** On Minkowski the a₀²M term is quartic in h_TT:
c_T = 1 exactly, Q_T > 0. On FLRW, however, the double-timelike projection R_uu = R_{μν}u^μu^ν
makes R_uu^{(2)}|_TT purely kinetic (an α_T-type operator, zero spatial-gradient monomials), giving
c_T² = 1/(1−8W̃) with c_T²−1 ≈ +3.9×10⁻² at the framework a₀ (Q_T > 0, so a speed failure, not a
ghost) — violating GW170817 by ~13 orders unless an exact cancellation of W̃ occurs under the
published vary-then-retard prescription (unverified; the single unplugged escape). By contrast the
full Ricci scalar R^{(2)}|_TT carries both kinetic and gradient sectors and protects c_T = 1 (as in
RR/RT nonlocal gravity); the u^μu^ν projection is precisely what destroys that protection.

**Verdict for the class: B (no-go for the exact-exponential branch).** The decisive kill is 4.2
(Cassini, structural); corroborated by 4.5 (FLRW tensor speed, one unverified escape) and bounded
by 4.1 (no canonical DOF certificate) and 4.3 (a₀ free; dust cosmology). The crossing/ellipticity
results (4.4) are the salvageable healthy core.

## 5. What these results do and do not establish

Established: Theorems 1–2 (adversarially verified symbolic results); the audit findings 4.1–4.5 at
their stated (mostly linear/branch-specific) scope. Not established: any statement about
multi-invariant or extra-field carriers (open); any derivation of κ or Z (fitted); any claim that
MOND phenomenology is confirmed — this paper is about internal mathematical structure only. The
companion paper presents the conditionally-closed constructive counterpart.

## Reproducibility

All results: `qwen_claude_field_theory/closure_2026/sf40–sf44*.py`,
`fried_chicken_exact_exponential_v2/scripts/`, committed with exit-0 check suites; adversarial
verification via multi-agent workflows with independent re-derivation, logged in the repository.

## References

Milgrom (1983); Bekenstein & Milgrom (1984); Milgrom & Sanders 2008 ApJ 678, 131 (kernel form
credit); Blanchet & Skordis relativistic khronon (JCAP); Deffayet & Woodard, arXiv:2512.10513
(2026); Deser & Woodard nonlocal cosmology, arXiv:1307.6639, 1711.08759; Gao et al.
spatially-covariant two-DOF: arXiv:1910.13995, 2403.15355, 2604.14490; Aoki–Mukohyama MMG:
arXiv:2011.00805, 2302.02090; khronometric theory: Blas–Pujolàs–Sibiryakov.
