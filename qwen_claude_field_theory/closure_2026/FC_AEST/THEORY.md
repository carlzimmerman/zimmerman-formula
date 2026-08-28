> ⚠️ **QUARANTINED / SUPERSEDED — NOT the current candidate.** This FC-AeST construction uses the
> **exponential observable kernel** μ_obs=1−e⁻ʸ (field function tanh(y/2)), which was **eliminated by the
> Cassini EFE quadrupole at 3.76× the ceiling** — see `scripts/fc_cassini_CORRECTED_2026.py` and
> `FROZEN_HIERARCHY.md` (both in this directory). The **frozen candidate is the SHARP-J₁₀ FC-FINAL** — AeST +
> `μ₁₀(y)=y/(1+y¹⁰)^{1/10}`, a₀ constant, 6-DOF-AeST — in `qwen_claude_field_theory/fc8_closure_2026/`
> (`FROZEN_CANDIDATE.md`, `THEOREM_PACKAGE.md`). **Do not mix the exponential branch into FC-FINAL.**
> Retained as historical record (append-only); the exponential-fails-Cassini result is itself a committed finding.

# FC-AeST: Cosmologically Anchored Aether-Scalar-Tensor MOND

**What it is (stated honestly).** The AeST chassis (Skordis–Złośnik, arXiv:2007.00082) — *not* a
new theory — with two additions: (i) the exact-exponential MOND kernel translated *correctly* into
the AeST field variable via the two-field inverse problem; (ii) Carl's cosmological promotion
a₀²(Q) = −κ²c²G·K(Q) (published, DOI 10.5281/zenodo.22015358), making a₀ a function of the
cosmological scalar. Matter is minimally coupled to g_μν, so photons and matter share one metric —
this is why AeST-type theories escape the conformal-lensing trap that killed our scalar routes.

## Action
    S_FC = (1/16πG̃) ∫ √−g [ R − 2Λ − (K_B/2)F² + (2−K_B)(2J·∇φ − Y) − F(Y,Q) − λ(A²+1) ] + S_m[g,ψ]
    Q = A^μ∇_μφ,  Y = (g^μν + A^μA^ν)∇_μφ∇_νφ,  A² = −1
    F(Y,Q) = K(Q) + (2−K_B) J_FC(Y; a₀(Q)),   a₀²(Q) = −κ²c²G·K(Q),  K(Q) = −½F(0,Q)

## The kernel bridge (verified exact — scripts/fc_aest_kernel_bridge.py)
AeST's quasistatic sector gives g = g_φ + f_G g_N with μ̃(g_φ/a₀)g_φ = f_G g_N — a **two-field**
structure, so the field function μ̃ is NOT the observable μ. Solving the inverse problem for the
observable μ_obs(y) = 1−e^{−y} (f_G = ½):

    x ≡ g_φ/a₀ = (y/2)(1 + e^{−y}),   μ̃(x) = (1−e^{−y})/(1+e^{−y}) = tanh(y/2)

with dx/dy = ½[1+(1−y)e^{−y}] > 0 (monotone, invertible). Limits survive exactly: Newtonian g→g_N;
deep-MOND g→√(a₀ g_N) ⇒ v⁴ = G a₀ M_b (BTFR). The AeST constitutive function is then
J′_FC(x²) = tanh(y(x)/2).

## The novelty: the cosmological lock
    a₀(z) = κc√(G ρ_DE(z)),   ρ_DE(z) := −K[Q̄(z)]   ⇒   a₀(z)/a₀,₀ = √(ρ_DE(z)/ρ_DE,₀)

For a cosmological constant (w=−1) this is a₀ = const (flat — consistent with STANDING). It is
distinctive **only if dark energy evolves**, which is what DESI DR2/DR3 probe. This supersedes the
naive a₀(z) ∝ H(z) reading (disfavoured ~2.3σ in STANDING).

## Honest status
See `results/kernel_bridge.out` for the full gate table. Established/inherited: kernel bridge and
limits (exact, new), c_T=1, γ_PPN=1, lensing, 6 DOF (AeST-baseline, committed/literature). **New:**
a₀(z) ∝ √ρ_DE. **Open risks specific to FC:** whether the Q-dependent a₀ (a) preserves the 6-DOF
Hamiltonian, (b) worsens or tames AeST's known low-k unbounded-Hamiltonian mode (arXiv:2109.13287),
(c) controls the oscillatory third quasistatic regime (arXiv:2304.05134). **Honest concessions:**
this is **6 DOF, not 2** — the 2-DOF program is closed; FC-AeST is a different, heavier chassis. κ²
and Z remain FITTED (a₀ is now a field, but its coefficient is not derived).

**One-line:** the first FC candidate that removes *both* MMG killers (no C_M lapse-constraint; no
conformal-lensing trap), at the cost of 6 DOF — with the genuine new hypothesis being the dark-
energy→a₀→galactic-MOND constitutive lock, testable now against DESI.
