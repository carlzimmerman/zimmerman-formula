# One Free Number: An Exhaustive Closure on the Normalization of the de Sitter–MOND Acceleration Scale a₀ = c²√(Λ/32π)

**Carl P. Zimmerman** · Briar Creek Tech · 2026-06-26

---

## Abstract

The MOND acceleration scale a₀ ≈ 1.2×10⁻¹⁰ m s⁻² coincides numerically with the cosmological quantity c√Λ, and can be written exactly as a horizon surface gravity,

> **a₀ = c²√(Λ/32π) = (c/2)√(Gρ_DE) = cH_Λ / Z,  Z = √(32π/3) ≈ 5.789.**

The dimensionless content of this identity factorizes cleanly. The group **√(8π/3) is forced** — it is the Einstein coupling 8π (from ρ_DE = Λc²/8πG) times the Friedmann 3 (from H² = 8πGρ/3), a sympy-exact algebraic fact. The **only** undetermined number is the outside coefficient **κ = ½** (the "c/2"). Whether a₀'s *value* is derived or merely fitted therefore reduces to a single yes/no question: can κ = ½ be forced from first principles?

This note reports an exhaustive negative answer. Across **~24 structurally-distinct routes** — ghost-freedom, unitarity, holography, a microscopic degree-of-freedom count, the Atiyah–Patodi–Singer η-invariant on the de Sitter horizon, five "symmetry-breaking" mechanisms (Hopf-bundle flux, the Witten SU(2) anomaly, the gravitational-Chern–Simons framing anomaly, a cosmic-string conical defect, a ζ-regularized Casimir energy), eight further families (on-shell dS-Unruh, 4-form flux quantization, horizon-entropy quantization, and five further normalization, index, and limit-matching constructions), and a gated brute-force over six classes of modified-inertia action — **no construction forces κ = ½ non-circularly.** Every route fails for one structural reason, which we make precise: κ is the absolute classical normalization sitting *outside* the gravitational square-root, while every number-fixing probe in physics (signs, ratios, scales, quantized levels, spectral asymmetries, vacuum energies) lives *inside* it, or is a mod-ℤ / dimensionless object **type-mismatched** to a bare multiplicative coupling. The mismatch is formal: a₀(2κ) = 2·a₀(κ) exactly, so κ is strictly linear and classical, while every quantized invariant is periodic or rational. The one type-distinct avenue — asymptotic safety, which outputs real numbers rather than mod-ℤ invariants — is examined separately and also fails: a₀ depends on √Λ alone, so the renormalization-group fixed point's G–Λ invariant is orthogonal to it.

A genuine and instructive caveat closes the loop. The framework *does* contain a rigorously forced ½ — the binomial ½ in the de Sitter–Unruh effective acceleration √(a²+(cH)²) − cH = a²/(2cH) + … — but it is bonded to cH and therefore sets the **temperature root** a₀ = 2cH_Λ. The two roots differ by **exactly 2Z ≈ 11.58** (the long-noted "~12×"); forcing this ½ into κ's slot would demand κ_eff = Z ≈ 5.789, not ½. It is a real ½ of the framework's own making, and it is provably not κ.

The defensible conclusion is unchanged from, and strengthened relative to, the author's prior work: **a₀ ≈ c√Λ is a forced scale, while its precise normalization is one free posit. The framework is a provably one-parameter effective theory — not zero-parameter, and not a theory of everything.** What we add here is not a new mechanism but the demonstration that, within the established toolkit, there is a structural reason no such mechanism appears. The live content is now entirely empirical: a declining a₀(z) ∝ √ρ_DE(z) and a Lorentz-violating s^TX dipole, both falsifiable this decade. All symbolic checks are reproducible from the public repository.

---

## 1. What is forced, and what is one number

Write the de Sitter rate H_Λ = c√(Λ/3) and the dark-energy density ρ_DE = Λc²/8πG. The acceleration scale is

$$a_0 \;=\; \kappa\, c\sqrt{G\rho_{\text{DE}}} \;=\; c^2\sqrt{\frac{\Lambda}{32\pi}}\quad\text{at }\ \kappa=\tfrac12,\qquad \rho_{\text{DE}}=\frac{\Lambda c^2}{8\pi G}.$$

Equivalently a₀ = cH_Λ / Z with **Z = cH_Λ / a₀ = 2√(8π/3) ≈ 5.789**. Because H² = 8πGρ/3 holds for *any* density, the ratio Z = √(32π/3) is an algebraic identity, not a measurement: the H cancels. Its dimensionless value decomposes as

$$Z = 2\sqrt{\tfrac{8\pi}{3}},\qquad 8\pi\ (\text{Einstein: }\rho_{\text{DE}}=\Lambda c^2/8\pi G)\;\times\;\tfrac13\ (\text{Friedmann: }H^2=8\pi G\rho/3),$$

with **the lone free factor the outside 2 = 1/κ.** Everything physical about whether a₀'s number is *derived* lives in this single coefficient. The question of this note is therefore sharp and binary.

## 2. The exhaustive closure

We organize ~24 attempts to force κ = ½ into six structural failure-classes. Each was checked by direct symbolic computation; the per-route verdicts and scripts are in the repository.

| Class | Representative routes | Why it cannot reach κ |
|---|---|---|
| **A. Scale-fraction wall** | ghost-freedom; unitarity; holography; topological Dirac-η; the dS-Unruh Taylor-½ | sees only signs / ratios / scales / a mod-ℤ phase — never the outside multiplier |
| **B. Double-count** | de Sitter surface gravity c²/2R; Gibbons–Hawking T, S = A/4; ζ-Casimir; 4-form flux energy | the ½ is real but *already spent* building cH_Λ and the 8π in ρ_DE |
| **C. κ cancels from the ratio** | 4-form quantization integer n; CKN g\* dof-count; the deep-Newtonian g_obs/g_bar ratio | κ divides out of every observable ratio → unconstrained |
| **D. Inserted structure** | Hopf base-flux + parity anomaly; Witten SU(2); a posited cosmic string | the ½ needs a field/flux de Sitter does not force (MM curvature F = 0 on-shell) |
| **E. Tunable, not ½** | lens-space η; cosmic-string deficit angle; CKN root g\* | gives a continuum fixed by a free scale, ½ only at a hand-picked value |
| **F. Conventional / mod-ℤ phase** | round-S³ Dirac η = 0; Chern–Simons level ∈ ℤ; framing c/24; θ/2π; APS η/2 | a periodic or geometry-blind object, not a classical coupling |

Two computations deserve a sentence. **The de Sitter horizon is the Hopf bundle** S¹→S³→S²; one might hope a base-S² monopole flux (H²(S²)=ℤ, unlike H²(S³)=0) supplies a ½. But the de Sitter saddle is the *full* S³ (the round Dirac η is exactly 0 by the ± symmetric Camporesi–Higuchi spectrum), the MacDowell–Mansouri SO(4,1) curvature **vanishes on-shell** (de Sitter is the flat connection, so there is no dynamical flux to twist), and the only ½ available — a Chern–Simons parity-anomaly level — is mod-ℤ and requires an inserted charged fermion. The forced Hopf numbers are 0 and 1, never ½. Separately, **the Witten SU(2) anomaly** (often invoked via "3 generations is odd") in fact counts electroweak *doublets*: the Standard Model has (3 colors + 1 lepton)×3 = 12, an *even* number, so the anomaly never fires.

## 3. The structural reason

The failures are not independent accidents; they are one fact seen six ways. Any candidate dynamical operator splits into a **functional shape**, which lives *inside* the gravitational root and *can* fix a clean number — the conformal coupling ξ = 1/6, the a₄ heat-kernel anomaly, the binomial ½, and Z itself are all genuinely forced — and an **overall normalization**, which lives *outside* the root, and is where κ resides. The separation is exact:

$$\frac{a_0(2\kappa)}{a_0(\kappa)} = 2 .$$

κ is a strictly **linear, classical, ℏ-free multiplier.** Every number-fixing tool physics offers is, by contrast, a mod-ℤ level (Chern–Simons, framing, θ), a spectral asymmetry mod ℤ (η-invariants), a dimensionless ratio (unitarity, ghost-freedom), or a vacuum energy that renormalizes ρ_DE (Casimir, flux). None of these can equal a bare multiplicative coupling — a periodic or rational object cannot fix a linear one. Physically, the value a₀ = c²√(Λ/32π) depends on √Λ *alone*: the Newton constant cancels identically, since ρ_DE = Λc²/8πG makes √(Gρ_DE) = c√(Λ/8π). The Einstein factor 8π survives *inside* the root as part of the forced shape; κ is the bare prefactor *outside* it, carrying no coupling at all. This is why κ is doubly out of reach — no spectral, topological, or ratio probe can fix a linear classical multiplier (the type-mismatch above), and no ultraviolet-gravity completion acting *through* G can reach a quantity from which G has already cancelled. The brute-force over six independent action classes (k-essence, nonlocal kernels, modified dispersion, entropic, Horndeski, spectral) returns no survivor for the same reason: each leaves κ a free outside multiplier, selects the temperature root, or inserts the answer.

## 4. The forced ½ that exists — and is not κ

It would be dishonest to report only the negative. The framework contains a **genuinely forced ½**, and locating it sharpens the result. The de Sitter–Unruh modified-inertia mechanism (Milgrom 1999; Deser–Levin 1997) gives the effective low-acceleration response

$$g_{\text{eff}} = \sqrt{a^2 + (cH)^2}\;-\;cH \;=\; \frac{a^2}{2cH} \;-\; \frac{a^4}{8c^3H^3}+\cdots,$$

whose leading coefficient is **exactly 1/(2cH)** — the universal √(1+x²)−1 ≈ x²/2 half, forced by the geometry, not inserted. But this ½ multiplies 1/cH: it is bonded to the de Sitter *rate* (the Friedmann/temperature root) and yields a₀ = 2cH_Λ. The coefficient κ we need multiplies the *density* root √(Gρ_DE), which carries the Einstein 8π. The two roots differ by exactly Z:

$$\frac{a_0^{\text{temp}}}{a_0^{\text{dens}}} = \frac{2cH_\Lambda}{cH_\Lambda/Z} = 2Z = \frac{8\sqrt{6}\,\sqrt{\pi}}{3} \approx 11.58 .$$

So the forced ½ is real and is the framework's own — but it is the *temperature-root* ½, separated from κ by exactly the factor Z = 5.789. Forcing it into κ's slot would require κ_eff = Z ≈ 5.789, not ½: a Z-error, sympy-exact. The intuition that "a forced ½ is in there" is correct; it simply belongs to the other root.

## 5. Scope and consequence

The result is a **strong negative**: no non-circular construction forces κ = ½ across ~24 structurally-distinct routes, and the reason is a precise type-mismatch rather than a failure of effort. It is *not* a formal no-go theorem against every conceivable exotic boundary condition or operator; an exhaustively-excluded statement of that strength is not claimed. What is claimed, and is doubly robust, is that within the established toolkit the ½ either is not present on the de Sitter geometry, or — even where a ½ appears — is not the outside classical coefficient κ.

One avenue deserves explicit mention, because it is *not* of the mod-ℤ kind addressed above. Asymptotic safety — the conjecture that gravity reaches an interacting ultraviolet fixed point — outputs genuine real numbers (the fixed-point couplings g\*, λ\* and the critical exponents), so the type-mismatch does not block it, and it was examined on its own footing. It too fails to force κ. Decisively, a₀ depends on √Λ alone — G cancels — whereas asymptotic safety's one scheme-robust invariant is the product g\*λ\* ∝ GΛ, *orthogonal* to a₀'s argument and numerically ≈ 0.10–0.14 across renormalization schemes (nearer 1/Z ≈ 0.17 than ½, and scheme-dependent where κ = ½ is exact); moreover its infrared limit is general relativity with a constant Λ, not a modified-inertia phase. We record asymptotic safety, explicitly, as the one theoretical avenue closed by *no non-circular construction found* rather than by a formal no-go.

The consequence is clean and was the author's published position, here proven rather than asserted: **the framework is a provably one-parameter effective theory.** Its forced content (the scale a₀ ≈ c√Λ, the ratio Z = 2√(8π/3), the de Sitter–Unruh square-root law, and with it the Radial Acceleration Relation and the Baryonic Tully–Fisher Relation) stands untouched. Its one free number, κ = ½, is now understood to be free *for a reason*. This is a stronger statement than "the mechanism was not found": there is a structural obstruction to there being one.

The live program is therefore entirely empirical. The single distinctive prediction — a declining acceleration scale, a₀(z) ∝ √ρ_DE(z), with a₀(z=3) ≈ 0.74 a₀(0) and a corresponding negative high-redshift Baryonic-Tully–Fisher offset — is falsifiable this decade with DESI w(z), JWST/ALMA high-z disc kinematics, and the ELT. A second, independent handle is the framework's forced Lorentz-violating signature: a gravitational s^TX boost-dipole at the few-×10⁻⁹ level, within reach of Gaia DR4-era solar-system and astrometric bounds. The math is mapped; the verdict now belongs to the data.

---

**Reproducibility.** All symbolic and numerical results are reproducible from the public repository, `real_research/` verdict documents `TOPOLOGICAL_KAPPA_ETA_VERDICT`, `KAPPA_FIVE_HAIL_MARY_VERDICT`, `KAPPA_ALL_DOORS_VERDICT`, and `KAPPA_GATED_ACTION_BRUTEFORCE_VERDICT`. This note documents a closure and corrects nothing in the author's prior honest description; it claims *less*, not more — a one-parameter effective theory with a now-understood reason for its single free coefficient.

**Key references.** Milgrom (1983, 1999, 2011); Deser & Levin (1997); Atiyah, Patodi & Singer (1975); Witten (1982, 1989); Camporesi & Higuchi (1996); Gibbons & Hawking (1977). Supersedes-toward-less and supplements arXiv/Zenodo 10.5281/zenodo.20935948.
