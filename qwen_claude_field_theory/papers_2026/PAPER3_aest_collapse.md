# The Minimal Sacrifice Is Not Minimal: Why Two-Degree-of-Freedom MOND Collapses into AeST

**Carl Zimmerman** (with AI-assisted derivation and verification; every load-bearing claim is
backed by a committed runnable script in `github.com/carlzimmerman/zimmerman-formula`)

**Date:** 2026-08-27

## Abstract

Relativistic completions of MOND face a well-known tension between reproducing the modified
force law, preserving gravitational lensing, and keeping the degree-of-freedom (DOF) count
minimal. We report a systematic closure attempt across seven local architectures and extract two
structural results. **First**, a *cost table*: exact MOND requires deforming the GR Hamiltonian
constraint away from the point at which Hojman–Kučař–Teitelboim uniqueness applies, and each way
of relaxing that structure carries a distinct, *measured* cost — deforming the constraint algebra
gives γ_PPN = 0 and α₃ ≠ 0; introducing spatial nonlocality damages the tensor sector (c_T = 0) or
the solar-system quadrupole; altering the momentum dependence propagates a scalar; and altering
the matter metric misroutes the source. We do not claim a universal no-go: HKT identifies a
structural *obstruction class* for local metric Hamiltonians satisfying its hypotheses, and each
architecture must be matched to those hypotheses individually. **Second**, and our main result,
the natural escape — paying for one extra propagating DOF via a screened (k-mouflage/Vainshtein)
scalar — does *not* deliver a cheaper theory. Such a model passes five gates cleanly (3 DOF,
c_T = 1, γ_PPN = 1, the exact interpolation μ(y) = 1 − e^{−y}, and BTFR/RAR), but fails two, both
of which are **blind to the DOF count**: (i) a conformally coupled scalar cannot bend light,
because null geodesics are conformally invariant, so the model predicts galaxies that rotate like
MOND and lens like bare baryons — excluded by the observed agreement of the lensing and dynamical
radial-acceleration relations; and (ii) the Cassini external-field quadrupole and the wide-binary
signal are governed by the same interpolation-transition sharpness at the same external field
η ≈ 1.9, so any screening that clears the former flattens the latter. Repairing (i) requires a
disformal matter coupling, which requires a preferred timelike vector, which lands on the
AeST/TeVeS class with six DOF. We therefore state the **AeST-collapse theorem**: within local,
minimally-coupled completions, *lensing costs a vector, not a scalar*, so the 2+1 route does not
interpolate between two-DOF gravity and AeST — it collapses into AeST. A corollary of practical
importance: in the surviving class the acceleration scale a₀ is not structural, which relocates
the framework's falsifiable content to the measurement side, where a₀ = κc√(Gρ_Λ) with
a₀(z) ∝ H(z) remains untouched by every obstruction reported here and is directly testable with
Gaia DR4 wide binaries.

## 1. Setup and scope

We work throughout in ADM variables (N, N^i, h_ij; π_N, π_i, π^ij), with matter minimally coupled
to a physical metric. The MOND target is the exact interpolation

    μ(y) = 1 − e^{−y},   y = |∇Ψ|/a₀,   D_i[μ(|∇Ψ|/a₀)∇^iΨ] = 4πGρ_b,

with AQUAL primitive F(y) = y²/2 + (1+y)e^{−y} − 1, F′(y) = yμ(y). Throughout, κ = ½ and Z ≈ 21 in
a₀ = κc√(Gρ_Λ) are **fitted**, never derived; no result below depends on that normalization.

"Two DOF" means two propagating tensor polarizations and no propagating scalar or vector, verified
by a nonlinear Dirac–Bergmann count rather than by a linearized perturbation argument.

## 2. The cost table (a structural obstruction class, not a universal no-go)

Hojman, Kučař and Teitelboim (1976) showed that a Hamiltonian constraint which (a) closes the
Dirac algebra, (b) is ultralocal in h_ij, and (c) is at most quadratic in momenta, is uniquely the
GR constraint. Exact MOND requires a nonlinear μ in the static constraint, hence a deformation
away from that point, hence the failure of (a), (b) or (c) — or a change in how matter sources the
constraint. **Which structure is relaxed determines which observable fails.** Across seven
architectures analyzed in this program:

| Relaxed structure | Architecture | Failure mode |
|---|---|---|
| (a) algebra closure | MMG: H_⊥ → C_M, the MOND elliptic constraint | γ_PPN = 0 exactly; α₁ = +4, α₃ = −1 |
| (a) algebra closure | MMG with S₂′ = D²(q + ln N) | γ_PPN = 1 restored, but α₃ = −3 and the deep-MOND source sign flips (BTFR lost) |
| (b) ultralocality | Canonical displacement E_i = D_i Δ⁻¹ ³R | ³R^{(1)}\|_TT = 0 ⇒ no tensor gradient ⇒ c_T = 0 |
| (b) ultralocality | Causal nonlocal (Deffayet–Woodard class) | localization ghost (2T+2S); external-field Cassini quadrupole excluded at 10–14σ |
| (c) momentum structure | Single-invariant carrier a₀²F(A²/a₀²) | khronon scalar propagates (2+1); Z_⊥ = 2(1−μ) > 0 throughout the MOND regime |
| source routing | MOND on the conformal factor q | sourced by the spatial stress trace T^i_i ~ ρv²/c² ≈ 5×10⁻⁷ρ ⇒ effectively unsourced |
| source routing | Composite metric g̃ = e^{2αq}g | conformal ⇒ no lensing; disformal ⇒ photon/graviton cone split (GW170817) |

We emphasize the scope. HKT's hypotheses must be matched to each construction individually, and
the table is an empirical catalogue of costs, not a proof that no MOND completion exists. The
defensible statement is: **local two-DOF MOND cannot retain all of the GR Hamiltonian structure**,
and every relaxation tested carries a measured cost.

## 3. The 2+1 screened-scalar route

The natural response is to pay the cost openly: accept one extra propagating DOF and screen it.
Consider S = S_GR[g] + S_φ[φ] + S_m[g̃, ψ] with a k-essence scalar whose kinetic function K(X)
reproduces the desired μ by the AQUAL Legendre duality, and a conformal matter metric
g̃ = A²(φ)g. Screening is automatic in the MOND context: μ → 1 at high acceleration *is* the
screening, in the k-mouflage sense.

Five gates pass cleanly:

- **3 DOF exactly** — two tensor + one scalar, by construction;
- **c_T = 1** — a conformally coupled scalar does not enter the transverse-traceless sector;
- **γ_PPN = 1** — conformal coupling shifts both potentials equally, Φ̃ = Φ + ln A and
  Ψ̃ = Ψ + ln A, so the slip Φ̃ − Ψ̃ = Φ − Ψ is unchanged;
- **exact μ(y) = 1 − e^{−y}** — a free choice of K(X);
- **BTFR and the radial acceleration relation** — standard AQUAL phenomenology.

This is further than any two-DOF architecture reached. Two gates then fail.

### 3.1 Conformal couplings cannot lens

Null geodesics are conformally invariant: if g̃_μν = A²g_μν, the null condition and the null
geodesic equation are preserved up to reparametrization. Photons therefore propagate on the null
cone of the gravitational metric g and are **blind to φ**, while massive particles feel φ and
acquire the MOND acceleration. The prediction is unambiguous: galaxies rotate like MOND and lens
like their baryons alone. In deep MOND the dynamical enhancement is √(a₀/g_N) — a factor ≈ 3 at
g_N = a₀/10 — while the predicted lensing enhancement is zero.

This is excluded. Weak-lensing measurements find that the lensing radial-acceleration relation
agrees with the dynamical one out to ~Mpc scales; light sees the same excess acceleration that
rotation curves do. We stress that this failure is **independent of the DOF count**: it is the
same conformal-invariance argument that eliminates the composite-metric two-DOF construction in
the table above, and adding the third DOF does not touch it.

### 3.2 Repairing lensing costs a vector

To make photons see φ one must abandon pure conformal coupling for a disformal physical metric,
g̃_μν = A²(φ)g_μν + B(φ)∂_μφ ∂_νφ. Two consequences follow. First, a lensing-sized disformal
term splits the photon and graviton cones; with |c_γ/c_GW − 1| ≲ 2×10⁻¹⁵ from GW170817, the
required O(1) disformal contribution is excluded by many orders — an obstruction we verified
independently in the two-DOF setting. Second, and more structurally, the disformal term requires a
distinguished timelike direction. Building it from ∂_μφ alone forces φ's gradient to be timelike
everywhere relevant, which is a preferred-frame structure in disguise; making it covariant
requires an independent unit-timelike vector field. That is precisely the ingredient that TeVeS
and AeST carry, and it is why the Hamiltonian analysis of AeST yields **six** physical degrees of
freedom.

### 3.3 The Cassini–wide-binary lock is DOF-blind

The second failure concerns the external-field effect. The Solar System and the solar-neighbourhood
wide binaries sit in the *same* galactic external field, g_ext ≈ 1.8×10⁻¹⁰ m s⁻², i.e. η = g_ext/a₀
≈ 1.5–1.9 on the two a₀ footings. The Cassini quadrupole Q₂ is governed by the interpolation
evaluated at that external field, not at the (screened) planetary field. Consequently any
sharpening of the transition that suppresses Q₂ at η ≈ 1.9 also suppresses the wide-binary boost
1/μ(η) − 1 at the same η. A committed 175-galaxy scan over the family μ_n(y) = y/(1+yⁿ)^{1/n}
makes this quantitative: n = 5 and n = 10 clear the 2026 Cassini ceiling (0.39 and 0.08 of the
bound respectively) while predicting wide-binary velocity boosts γ_v = 1.0040 and 1.0001 —
Newtonian to the precision of the measurement. Screening strength here is a property of the
*kernel's transition sharpness*, not of the degree-of-freedom count; the third DOF buys nothing.

## 4. The AeST-collapse theorem

Collecting §3:

> **Theorem (AeST collapse).** Within local, minimally-coupled relativistic completions of MOND, a
> single additional propagating scalar cannot simultaneously deliver MOND dynamics and MOND
> lensing. A conformal matter coupling yields the dynamics but leaves photons blind to the scalar;
> restoring lensing requires a disformal coupling, which requires a preferred timelike vector and
> therefore additional propagating structure. The 2+1 route consequently does not interpolate
> between two-DOF gravity and the AeST/TeVeS class — it collapses into it.

The practical content is a correction to a natural intuition. One expects the DOF cost of
relativistic MOND to be payable incrementally, with a "minimal third degree of freedom" buying the
phenomenology. It is not: **lensing costs a vector, not a scalar.** The minimum viable structure
is the one the literature already occupies, and it is not cheap.

## 5. Corollary: where the falsifiable content lives

In the surviving (AeST-like) class the acceleration scale is an input: the interpolation
normalization and the cosmological constant enter as independent parameters, so a₀ is not
structural. This has a constructive consequence for the present framework. The relation

    a₀ = κ c √(Gρ_Λ),   a₀(z) = a₀,₀ H(z)/H₀

is untouched by every obstruction reported here — none of the seven architectures constrains it,
because each fails on the *relativistic completion*, not on the acceleration scale. Its
distinctive prediction, the cosmological evolution a₀(z) ∝ H(z), and its solar-neighbourhood
consequence for wide binaries are directly testable. Given §3.3, Gaia DR4 becomes a sharp
discriminator rather than a confirmation channel: a Cassini-safe kernel predicts γ_v ≈ 1.000–1.004,
whereas the framework's pre-registered band is 1.16–1.23. Those are distinguishable outcomes, and
the measurement decides between them without reference to any completion.

## 6. What is and is not claimed

Established: the cost table as an empirical catalogue with committed evidence per row; the
conformal no-lensing lemma; the DOF-blindness of the Cassini/wide-binary lock; and the collapse
theorem as stated in §4 under its explicit hypotheses (local, minimal coupling, single additional
scalar).

Not claimed: a universal no-go for relativistic MOND; that HKT alone implies all seven failures;
any derivation of κ or Z; any statement about nonlocal completions beyond the specific
architectures tested; and any claim that AeST itself is excluded — its own gates are a separate
matter, and the point here is that the 2+1 route offers no cheaper alternative to it.

## Reproducibility

Scripts, logs and per-gate outputs: `qwen_claude_field_theory/closure_2026/TWO_CHANNEL/` and
`CGD_GAUSSLAW/` (this paper), with the supporting two-DOF analyses in
`qwen_claude_field_theory/closure_2026/` and `openai_push/final_closure/`. Companion deposits:
*Carrier No-Go Theorems for Two-Degree-of-Freedom MOND* (DOI 10.5281/zenodo.22132648) and
*A Conditionally Closed Constraint-Defined MOND Theory* (v2, DOI 10.5281/zenodo.22133406).

## References

Milgrom (1983); Bekenstein & Milgrom (1984); Milgrom & Sanders (2008), ApJ 678, 131;
Hojman, Kučař & Teitelboim (1976), Ann. Phys. 96, 88; Bekenstein (2004), TeVeS;
Skordis & Złośnik (2021), AeST; Skordis & Złośnik (2024), PRD 110, 044015 (AeST Hamiltonian
analysis, six DOF); Babichev, Deffayet & Ziour (2009), k-mouflage; Vainshtein (1972);
Bekenstein & Sanders (1994), disformal couplings; Deffayet & Woodard (2026), causal nonlocal MOND;
Desmond, Hees & Famaey (2024), external-field Cassini quadrupole; Brouwer et al. (2021) and
Mistele et al. (2024), weak-lensing radial acceleration relation; Aoki & Mukohyama et al.,
minimally modified gravity with auxiliary constraints; Gao et al., spatially covariant gravity
with two tensorial degrees of freedom.
