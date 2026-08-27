# A Conditionally Closed Constraint-Defined MOND Theory with Two Tensor Degrees of Freedom: Hamiltonian Certification, Kernel-Agnostic Chassis, and Solar-System Viability

**Carl Zimmerman** (with AI-assisted derivation and verification; every load-bearing claim backed by
a committed runnable script in `github.com/carlzimmerman/zimmerman-formula`,
`openai_push/final_closure/` and `qwen_claude_field_theory/closure_2026/`)

**Date:** 2026-08-27 (v2 correction: same day)

## ⚠️ VERSION 2 STATUS CORRECTION (2026-08-27, same day)

**The "CONDITIONALLY CLOSED" label of v1 is WITHDRAWN.** A hostile referee-to-closure audit run the
same day (deliverables and scripts in `qwen_claude_field_theory/closure_2026/`, all committed and
reproducible via `RUN_ALL_GATES.py`) found three kernel-blind, footing-blind contradictions derived
from the frozen constraint set itself — the correct status is **FAILED as a relativistic completion**:

1. **γ_PPN = 0 exactly** (derived twice independently): the second-class constraint D²q = 0 leaves
   the spatial conformal potential unsourced — the deleted Hamiltonian constraint is precisely the
   GR equation that sourced it. Light sees half the (MOND and Newtonian) potential: ~43,000σ against
   the Cassini Shapiro measurement; solar deflection 0.875″, excluded at 1919 precision; galaxy–
   galaxy lensing RAR Δχ² ≈ +400–500.
2. **α₁ = +4 and α₃ = −1** — preferred-frame and momentum-non-conservation parameters sourced by
   the MOND constraint C_M itself; α₃ exceeds the pulsar bound by ~2.5×10¹⁹. The kernel swap of
   Gate 13 repairs only the EFE quadrupole and none of these.
3. **Matter non-conservation at Newtonian order** — v1's Gate-10 claim that violations enter at
   O(v²/c²) is falsified: evaluating the multiplier r₄ left symbolic in Gate 8 produces a
   matter-sourced force with unrescaled 1-AU anomaly ~10¹¹× the ephemeris bound.

Additionally, the "6 first-class" input to the 20−12−4 = 4 count is an unverified hypothesis pending
the {D²q, H_i} closure computation, and the FLRW linear scalar sector is empty (μ(0) = 0), so linear
growth/CMB cannot be confronted.

**What survives of v1, unaffected:** the nonrelativistic core — the generic-branch two-tensor-DOF
Hamiltonian skeleton (Pfaffian independently re-derived), the exact AQUAL reduction, the derived
anisotropic external-field-effect response tensor, the kernel-agnosticism lemma (Gate 13), the μ_n
Cassini analysis, and the closure of the k = 0 and y = 0 exceptional sectors. The structural lesson
is the paper's real content in retrospect: **deleting the Hamiltonian constraint is simultaneously
what produces the two-DOF count and what destroys lensing and matter conservation.** Two repair
forks are named in the audit (S₂′ = D²(q + ln N); C_M-as-secondary); each is a new certification
program, and neither, as formulated, repairs α₃. A new in-chassis result: Cassini-safety and a
non-Newtonian wide-binary signal are the same lever here, so Gaia DR4 becomes a sharp discriminator
(μ_n predicts γ_v ≈ 1.000–1.004).

The v1 text below is preserved unchanged for the record.

---

## Abstract

We present a preferred-foliation Hamiltonian theory of minimally-modified-gravity (MMG) type in
which the MOND phenomenology is carried by the *constraint sector* rather than a propagating field:
the scalar (lapse) constraint of the ADM system is replaced by the exact MOND elliptic equation
C_M = D_i[c²μ(y)D^i ln N] − 4πGρ_m, y = (c²/a₀)|D ln N|. A twelve-gate Dirac–Bergmann certification
(all gates passing, scripts committed) establishes, on the generic branch (y>0, k≠0): exactly two
local propagating degrees of freedom (the TT pair; Dirac determinant (L_N K)² ≠ 0; count
20−12−4 = 4 phase-space dimensions), an exactly-GR tensor sector (c_T = c, Q_T > 0, no scalar
pole), the exact MOND weak-field law with no missing factor, and multiplier preservation with no
tertiary constraint. A thirteenth gate proves the chassis is *kernel-agnostic*: the constraint
algebra uses μ only through ellipticity (μ > 0, d(yμ)/dy > 0), so the interpolation is a modular
choice. This matters because the companion paper proves the external-field Cassini quadrupole
excludes exponentially-screened kernels (1−μ unscreened at y_ext ≈ 1.9): here we adopt
μ_n(y) = y/(1+yⁿ)^{1/n} with n = 5–10, which clears the 2026 Cassini ceiling on both a₀ footings
(committed 175-galaxy SPARC analysis) at a stated cost — RAR scatter 0.108 → 0.123–0.127 dex. The
cosmological k = 0 sector, left open by the closure, is prescribed by a CMC clock K = q(t) with
a₀(q) = cq/Z, giving the framework's distinctive testable scaling a₀(z) = a₀,₀H(z)/H₀ on FLRW. We
state plainly what the construction is not: it is not manifestly 4D generally covariant (the lapse
is removed by a second-class pair — a legitimate Hamiltonian MMG structure, not a covariant local
action); ∇_μT^{μν} = 0 is not a Bianchi identity (relativistic-order matter corrections arise); and
the k = 0 and y = 0 branches require separate treatment (the clock prescription is proposed, its
preservation not yet derived). κ = ½ and Z ≈ 21 in a₀ = κc√(Gρ_Λ) are fitted, not derived. Within
those stated conditions, this is — to our knowledge — the first single Hamiltonian object
simultaneously carrying a certified two-tensor-DOF count, the exact nonlinear MOND law, c_T = c,
and solar-system (Cassini) viability.

## 1. Motivation: why the constraint sector

Two structural results (companion paper) frame the construction. First, the single-invariant
carrier a₀²F(A²/a₀²) cannot remove its scalar while retaining MOND: the velocity-Hessian kernel
Z_ij = F′δ_ij + (2F″/a₀²)ā_iā_j has Z_⊥ = 2(1−μ) > 0 wherever MOND is active — nonlinearity in a
kinetic sector propagates a mode. Second, the auxiliary-Legendre pair carries the same nonlinearity
with *zero* propagating DOF: its Dirac Pfaffian N√h[2(ḡ·k)² − V″χk²] is strictly positive because
the Legendre relation forces V″ < 0 — nonlinearity in a constraint bracket removes a mode. The MMG
construction below is the completion of that observation: MOND enters only through an elliptic
constraint on the lapse, and the gravitational phase space is reduced to the TT pair by
second-class pairs, in the spirit of the MMG/auxiliary-constraint literature (arXiv:2011.00805,
2302.02090) and spatially-covariant two-DOF gravity (arXiv:1910.13995).

## 2. The theory

ADM variables (N, N^i, γ_ij; π_N, π_i, π^ij); q = (1/6)ln det γ, p = π/√γ. Constraint set for the
inhomogeneous modes: S₁ = C_M, S₂ = D²q, S₃ = D²p, S₄ = π_N, with

  C_M = D_i[c²μ(y)D^i ln N] − 4πGρ_m,  y = (c²/a₀)|D ln N|,

  H_T = H_GR + H_m + ∫d³x[λ_N S₄ + μ₁S₁ + μ₂S₂ + μ₃S₃ + N^iH_i + λ^iπ_i].

**Constitutive representation.** The static sector derives from a local spatial potential G(y) with
G′(y)/(2y) = μ(y). For the exponential kernel G = y² + 2(1+y)e^{−y} − 2; for the adopted μ_n the
primitive G_n(y) = 2∫₀^y sμ_n(s)ds exists and satisfies the same relation exactly (Gate 13).

**Kernel.** μ_n(y) = y/(1+yⁿ)^{1/n}, n = 5–10 (see §4).

**Cosmological sector (proposed prescription).** The homogeneous (k=0) modes of (q,p) — excluded
from the closure — are prescribed by the CMC clock K = q(t) with a₀(q) = cq/Z; on FLRW q = 3H, so

  a₀(z) = a₀,₀ H(z)/H₀,

the framework's distinctive falsifiable scaling (Z-independent as an evolution law). The absolute
normalization a₀ = κc√(Gρ_Λ) (κ = ½, Z ≈ 21) is fitted, and — as the companion paper's
reverse-arrow theorem shows for the nonlocal chassis — should not be advertised as derived here
either.

## 3. Certification (the twelve gates + Gate 13)

All scripts in `openai_push/final_closure/scripts/`, `bash run_all.sh` → ALL GATES PASS (re-run
2026-08-27). On the generic branch y > 0, k ≠ 0:

1. **Constitutive:** G′(y)/(2y) = μ(y) exactly.
2. **Newtonian limit:** div[μ∇Ψ] = 4πGρ_b with all factors of c² cancelling; deep-MOND
   g = √(g_N a₀) (BTFR), Newtonian recovery.
3. **Dirac matrix:** the 4×4 second-class matrix on (S₄,S₁,S₂,S₃) has Pfaffian L_N·K and
   determinant (L_N K)², independent of the off-diagonal couplings {C_M, D²q}, {C_M, D²p}.
4. **Ellipticity:** the lapse operator's principal eigenvalues λ_⊥ = μ, λ_∥ = μ + yμ′ are positive
   for all y > 0.
5. **Laplacian pair:** {S₂(k), S₃(−k)} = ½k⁴ ≠ 0.
6. **Rank:** full rank on the generic branch; the k = 0 and y = 0 degeneracies are *excluded*, not
   resolved (§5).
7. **DOF count:** 20 − 12 (first-class + gauge) − 4 (second-class) = 4 phase-space dimensions = the
   two TT polarizations. No propagating scalar or vector.
8. **Preservation:** the four multipliers are fixed; no tertiary constraint.
9. **Tensor sector:** identical to GR — c_T = c, Q_T > 0, no scalar pole.
10. **Matter:** spatially covariant, Newtonian-order consistent (see §5 for the relativistic
    defect).
11. **Classification:** a Hamiltonian MMG theory with a local first-kind Lagrangian on a fixed
    foliation; *not* manifestly 4D covariant, and not advertised as such.
12. **Falsification sweep:** none of eight auto-rejection criteria triggered (no extra pole, no
    vanishing Dirac determinant on the branch, no hidden tertiary, no ghost/gradient instability,
    no Newtonian-limit failure, no matter inconsistency, no inert-multiplier pathology, no global
    overclaim).
13. **Kernel-agnosticism (new):** gates 3–9 use μ only through λ_⊥ > 0, λ_∥ = d(yμ)/dy > 0.
    For μ_n: d(yμ_n)/dy = y(2+yⁿ)/(1+yⁿ)^{1+1/n} > 0 exactly, with the correct deep-MOND and
    Newtonian limits. The two-DOF certificate therefore transfers verbatim to the μ_n kernel.
    (`13_kernel_swap_ellipticity.py`.)

## 4. Solar-system viability: the kernel choice and its price

The companion paper's localization result makes the Cassini test kernel-decisive: the EFE
quadrupole is sourced at the external Milky-Way field y_ext ≈ 1.9, where 1−μ is unscreened for
exponential kernels (e^{−1.9} ≈ 0.15 ⇒ Q₂ ≈ 2×10⁻²⁶ s⁻², a 10–14σ exclusion). The committed
175-galaxy SPARC analysis with per-kernel Υ refits (route1B, 25/25 checks) gives:

| kernel | RAR rms (dex) | Q₂/ceiling (canonical / alt) | 1-AU monopole vs Mars budget |
|---|---|---|---|
| exponential (MS08-type) | 0.100 | 7.8 / 8.5 (≈22σ / 24σ) | 0 |
| a₀-line | 0.108 | 5.6 / 6.4 | 3.3×10⁴ / 4.0×10⁴ × |
| μ₅ | 0.123 | **0.39 / 0.82** | 2.7×10⁻⁸ × |
| μ₁₀ | 0.127 | **0.08 / 0.21** | ~10⁻²⁸ × |

μ₅ clears everywhere on the canonical footing (and everywhere but −2σ alt); μ₁₀ clears the full
±2σ measured g_ext range on both footings. **The price, stated plainly:** the RAR fit degrades from
0.108 to 0.123–0.127 dex. The deep-MOND limit — hence a₀, the BTFR, and the amplitude law — is
identical across all μ_n to 5×10⁻⁷; the solar system constrains the *transition*, not a₀. This
trade is the physical content of the kernel choice and must not be hidden.

## 5. What "conditionally" means (the three defects)

1. **Preferred foliation.** The lapse is removed by the second-class pair (π_N, C_M), not a
   first-class refoliation constraint. The theory is a Hamiltonian MMG model on a fixed foliation —
   a recognized consistent class — but not a manifestly 4D generally covariant local action.
2. **Relativistic matter defect.** Because the lapse equation is the MOND constraint rather than
   the Hamiltonian constraint, ∇_μT^{μν} = 0 does not hold as a Bianchi identity; matter equations
   acquire MOND-induced corrections at v ~ c. Newtonian-order consistency is verified (Gate 10);
   the relativistic completion of the matter sector is open.
3. **Excluded branches.** k = 0: the homogeneous (q,p) modes survive the second-class reduction and
   are here assigned to the CMC clock of §2 — a proposal whose preservation under H_T is not yet
   derived. y = 0: both principal eigenvalues vanish (the exact Newtonian point); the degenerate-
   elliptic limit needs separate treatment, as in the committed York-line analyses.

Lensing and cosmological perturbations are likewise open at the relativistic level; nothing in this
paper should be read as a completed relativistic phenomenology.

## 6. Relation to prior work and claim of novelty

Constraint-sector MOND realizes, in Hamiltonian form, the moral of the carrier no-go: MOND
nonlinearity must sit in constraint brackets, not kinetic Hessians. The chassis belongs to the
MMG/auxiliary-constraint class of Aoki et al. and the two-tensor-DOF spatially-covariant program of
Gao et al.; its novelty is (i) the *exact nonlinear* MOND elliptic law as the lapse constraint with
a full twelve-gate Dirac certification on the generic branch, (ii) the kernel-agnosticism theorem
making solar-system viability a modular kernel property rather than a rebuild, and (iii) the CMC
clock coupling a₀(z) ∝ H(z) to the otherwise-undetermined k = 0 sector. We do not claim: 4D
covariance, a derivation of κ or Z, global closure, or observational confirmation.

## Reproducibility

`bash openai_push/final_closure/run_all.sh` (Gates 1–12, exit 0);
`python3 openai_push/final_closure/scripts/13_kernel_swap_ellipticity.py` (Gate 13);
`route1B_monotone_escape_2026.py` (kernel/Cassini table);
consolidation record: `qwen_claude_field_theory/FINAL_THEORY_MMG_CONSOLIDATED_2026-08-27.md`.

## References

Milgrom (1983); Bekenstein & Milgrom (1984), AQUAL; Milgrom & Sanders 2008 ApJ 678, 131;
Aoki, De Felice, Mukohyama et al., MMG with auxiliary constraints: arXiv:2011.00805, 2302.02090;
Gao et al., spatially covariant gravity with two tensorial DOF: arXiv:1910.13995, 2104.07615,
2403.15355, 2604.14490; Desmond, Hees & Famaey (2024), Cassini EFE quadrupole; companion paper:
*Carrier No-Go Theorems for Two-Degree-of-Freedom MOND* (this repository, 2026-08-27).
