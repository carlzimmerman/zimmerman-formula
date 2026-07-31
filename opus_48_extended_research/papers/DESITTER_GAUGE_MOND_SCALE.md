# The MOND Acceleration Scale as a de Sitter Curvature Scale: Gauged SO(4,1) Gravity Reduces a₀ = c²√(Λ/32π) to a Single Free Number

**Carl P. Zimmerman** · Briar Creek Tech
*Preprint — 2026-06-16*

---

## Abstract

The dynamics of galaxies require either unseen matter or a modification of dynamics below a characteristic acceleration a₀ ≈ 10⁻¹⁰ m s⁻², a scale that numerically coincides with c√Λ and with cH₀. This paper develops the hypothesis that the coincidence is structural: the acceleration scale is a **de Sitter curvature scale**, a₀ = c²√(Λ/32π) = (c/2)√(Gρ_DE) = cH_Λ/Z with Z = √(32π/3) = 5.789, evaluated on the dark-energy density alone, giving a₀ = 9.36×10⁻¹¹ m s⁻². I separate, sharply and with machine verification, what this proposal **derives** from what it **posits**. (i) Gauging the de Sitter group SO(4,1) à la MacDowell–Mansouri yields Einstein–Hilbert + Λ; an exhaustive symbolic enumeration certifies this is the **unique** two-derivative parity-even invariant in the class (exactly two quadratic-in-curvature SO(4,1) four-forms exist; exactly one is two-derivative). (ii) The deep-MOND **form** a₀ ∝ c²√Λ is over-determined: a false-discovery-controlled audit of candidate routes certifies **four** structurally independent mechanisms force it (correcting an earlier inflated count), with the de Sitter–Unruh modified-inertia route reproducing flat rotation curves and the v⁴ = GMa₀ scaling. **⚠️ Corrected 2026-07-30: those four mechanisms force the *scaling* a₀ ∝ c²√Λ, which is what is claimed here and what survives. The de Sitter–Unruh route additionally *produced* the interpolating kernel — (√(1+4x²)−1)/(2x), the α = 1 class — and that part is now given up, because that kernel implies a constant sunward anomaly 1279× over the Earth ephemeris bound. The kernel used from 2026-07-30 is μ(x) = x/√(1+x²) (α = 2, Milgrom 1983) and is *phenomenological*: the mechanism no longer derives it. See §2, Eq. (4).** (iii) The gravitational route fixes the kernel √(8π/3) **including the half-integer power of π** that no curvature-free thermal route produces, leaving the entire residual unforced content as **one O(1) number**, κ = ½: a₀ is exactly half the gravitational free-fall acceleration at the dark-energy density. I am equally explicit about the limits: the value of Λ is an input; the inertia mechanism's microscopic completion is unbuilt and a covariant home exists only as a sibling effective field theory degenerate with the relativistic MOND theory AeST on the static locus but not joined to it; and the Standard Model is not produced — the generation number N = 3 is shown to be a topological **parity obstruction** for the natural index over the de Sitter nucleation saddle, so it stays fitted, as it is in every theory. The proposal is therefore **an effective theory at a frontier with a certified gravity spine and a fitted Standard Model — not a theory of everything yet, as frustrating as it may be.** Two tests decide its distinctive content: Cassini (in hand) discriminates modified inertia, which it passes by a factor **2.2×10⁷** under the α = 2 kernel (it was ~30 under the retired α = 1 one), from an ungated modified-gravity completion, which it fails; and the declining prediction a₀(z=3) ≈ 0.74·a₀(0), cleanly separable (~6×) from both ΛCDM and a rival rising branch, is falsifiable with extremely-large-telescope spectroscopy this decade, hostage to whether DESI confirms evolving dark energy.

**Keywords:** modified gravity; MOND; modified inertia; acceleration scale a₀; cosmological constant; de Sitter horizon; gauge gravity; MacDowell–Mansouri; radial acceleration relation; external field effect; DESI; Cassini.

---

## 1. Introduction

The radial acceleration relation (RAR) and the baryonic Tully–Fisher relation establish, model-independently, that galaxy dynamics organize around a single acceleration scale a₀ ≈ 1.2×10⁻¹⁰ m s⁻² (McGaugh, Lelli & Schombert 2016; Lelli et al. 2017). That this scale satisfies a₀ ∼ c²√Λ ∼ cH₀ to order unity is, in ΛCDM, a numerical accident. The proposal examined here is that it is not an accident but an identity: **a₀ is the curvature scale of the asymptotic de Sitter geometry**, expressed on the dark-energy density,

  a₀ = c²√(Λ/32π) = (c/2)√(Gρ_DE) = cH_Λ/Z,  Z = √(32π/3) = 5.78881,  ρ_DE = Λc²/8πG, (1)

which evaluates to a₀ = 9.36×10⁻¹¹ m s⁻² on Planck/DESI Λ — within the spread the RAR permits at stellar mass-to-light Υ ≈ 0.70.

The contribution of this paper is not another empirical fit. It is a **disciplined separation of derived from posited**, carried to the point where the claims can be checked by a referee and, in three places, by a machine. I report which links of the chain from a single de Sitter axiom to Eq. (1) are forced, which are forced only within a stated class, and which are inputs; I correct two over-statements in the earlier literature on this proposal; and I state without softening the three places where the chain does not close. The result is a modest but, I argue, genuinely defensible claim: a de Sitter-gauged gravity theory whose modified-inertia sector ties the MOND scale to the cosmological constant down to a single O(1) number, with no dark-matter particle, and with two clean falsifiers.

Throughout I use the framework's own footing — a₀ = 9.36×10⁻¹¹ m s⁻² on ρ_DE, Υ ≈ 0.70, and the de Sitter–Unruh interpolation, Eq. (4) — rather than the conventional MOND values, because the question is whether *this* construction holds together, not whether it reproduces a different one.

## 2. The construction

**Gravity.** Gauge the de Sitter group SO(4,1) with a connection A = ½ω^{ab}M_{ab} + (1/ℓ)e^a P_a. The so(4,1) curvature F = dA + A∧A splits, under the symmetry breaking SO(4,1)→SO(3,1) defined by a unit-norm internal vector, into a Lorentz block F^{ab} = R^{ab}[ω] − (1/ℓ²)e^a∧e^b and a boost block equal to the torsion T^a (MacDowell & Mansouri 1977; Wise 2010). The action

  S ∼ ∫ ε_{abcd} F^{ab} ∧ F^{cd}        (2)

expands into Einstein–Hilbert + cosmological constant + Gauss–Bonnet, with Λ = 3/ℓ² and the Gauss–Bonnet term topological in four dimensions. This is the well-known gauge-theoretic route to dark-energy gravity; here it supplies the de Sitter foundation that Eq. (1) reads its scale from.

**Inertia.** A uniformly accelerated detector in de Sitter space registers the quadrature temperature (Deser & Levin 1997)

  2π k_B T_eff / ℏc = √(a² + (cH_Λ)²),  cH_Λ = c√(Λ/3),     (3)

a thermal floor T_dS = ℏH_Λ/2πk_B at zero acceleration. Taking inertia to track this effective temperature yields a modified-inertia law m·a·μ_fw(|a|/a₀) = F with the interpolation

  μ(x) = x/√(1+x²),    (4)

**⚠️ KERNEL CHANGED 2026-07-30 — and the change costs more than a symbol. Read this before using Eq. (4).**
Versions to 2026-06-16 carried μ_fw(x) = (√(1+4x²) − 1)/(2x), with g_obs = √(g_N² + g_N a₀), described here as "the exact algebraic inverse of the de Sitter–Unruh quadrature." That description was **correct**, and that is the problem. The quadrature above genuinely *produces* that kernel: taking ΔT = T(a) − T(0) and dividing by a gives μ = [√(a²+H²) − H]/a, which on writing a = x·a₀ forces H/a₀ = ½ and returns (√(1+4x²)−1)/(2x) identically (sympy difference 0). Its Newtonian approach is 1 − μ ~ 1/(2x) — the α = 1 class.

**That kernel is excluded by the inner planets.** Held to all accelerations it implies a *constant* sunward anomaly a₀/2 = 4.68×10⁻¹¹ m s⁻², which is **1279× the Earth 2σ ephemeris bound** derived from Sereno & Jetzer (2006) Table 1 through their Eq. (9). It also drives the companion disformal lensing construction's own B < 1 premise past 257× across Mercury→Saturn. Against that it buys **+0.0033 dex** on 175 SPARC galaxies — 0.10 σ_int, unresolvable.

So Eq. (4) is now the α = 2 kernel μ(x) = x/√(1+x²) (Milgrom 1983), and **two things must be said plainly:**

1. **The scale survives, and that is this paper's actual thesis.** a₀ = c²√(Λ/32π) = (c/2)√(Gρ_DE) = cH_Λ/Z is unaffected: every premise its derivation uses — Herglotz–Nevanlinna positivity, passivity sup K = 1, the unit sum rule ∫dμ/|t| = K(∞) − K(0) = 1, the horizon floor — holds for the α = 2 kernel, whose spectral measure ρ(s) = (1/π)√(s/(1−s)) on 0 < s < 1 is in fact *simpler* than the α = 1 one (one region instead of two, compact support, finite mass ½, no additive constant). §3.1's SO(4,1) uniqueness, §3.2's certified count of four independent mechanisms forcing the *form*, and §3.3's reduction to the single number κ = ½ are all **untouched** — none of them uses the tail.

2. **The kernel's derivation does not survive.** The α = 2 tail cannot be obtained from this quadrature, and the obstruction is structural rather than a failure of ingenuity: for *any* T = f(√(a²+H²)), the floor subtraction followed by the division by a leaves a term linear in H/a, so α = 1 is rigid under the whole family (checked for f = √, quarter-power, and log). **The kernel is therefore now phenomenological — adopted because it passes the ephemerides, not derived from the mechanism.** The de Sitter–Unruh route previously supplied the scale *and* the kernel as one object; it now supplies only the scale. Note that it was already not supplying the coefficient: Milgrom's identical derivation fixes a₀ = 2cH_Λ, i.e. 2Z = 11.58× the value used here, which this paper already re-normalises to κ = ½. What remains forced is the **scaling** a₀ ∝ c√(Gρ_Λ), which §3.2's own false-discovery-controlled audit finds four independent mechanisms deliver.

The trade is not derived-versus-fitted. It is derived-and-excluded versus fitted-and-viable, and no option keeps a derived kernel.

Eq. (4)'s limits are μ → 1 (Newtonian, x ≫ 1) and μ → x (deep-MOND, x ≪ 1) — **shared with the retired kernel**, so flat rotation curves and v⁴ = GMa₀ are unaffected.

## 3. What is derived — and certified

The chain from the de Sitter axiom to Eq. (1) was graded link by link, each re-verified by direct symbolic computation rather than taken from prior text. Three load-bearing links were additionally certified by exhaustive machine enumeration; those scripts and their output are archived with the source repository.

**3.1 The gravity action is unique in its class (certified).** An exhaustive kernel-certified enumeration of gauge-invariant quadratic-in-F four-forms on SO(4,1) returns **exactly two**: the parity-even ε-trace (which gives Einstein–Hilbert + Λ + topological Gauss–Bonnet, with no torsion) and the metric δ-trace (which gives a four-derivative Yang–Mills/Weyl²-type theory with a torsion sector). Of these, **exactly one** is a two-derivative parity-even metric theory, and its two-derivative content is exactly Einstein–Hilbert + Λ. The selection of the two-derivative parity-even branch over the gauge-allowed four-derivative branch is a physics input — the demand for second-order metric dynamics — not a theorem; with that input made explicit, "Einstein–Hilbert + Λ uniquely" is rigorous. (Certificate: `gap1_so41_invariant_uniqueness.py`, PASS, 15 s.)

**3.2 The form a₀ ∝ c²√Λ is forced by four independent mechanisms (certified count, corrected).** Earlier presentations of this proposal claimed "≥ 7" independent derivations of the form. A false-discovery-controlled germ-fingerprint audit (1.5×10⁶ Monte-Carlo decoys, exact symbolic membership tests) shows that count is **inflated**: three of the routes are the *single* de Sitter–Unruh quadrature germ re-read under a rescaling x → λx, and collapse to one equivalence class. The certified count of structurally independent generators of the form is **four** — the de Sitter–Unruh quadrature, a conformal-SO(4,1) route, a gauge-Yang–Mills route, and a precanonical route. Four still over-determines the form (two would suffice), and I report four rather than seven. (Certificate: `gap2_germ_fingerprint_FDR.py --full`, K = 4, FDR q = 10⁻⁶ with no spurious collapses, 68 min.) I emphasize this correction because the honesty of the count is part of the claim.

**3.3 The kernel carries a half-integer power of π, leaving one free number.** Writing a₀ = c²√(Λ/32π) = (c/2)√(Gρ_DE), the coefficient decomposes as Z = 2·√(8π/3). The 8π is the Einstein coupling: only the Einstein normalization ρ_DE = Λc²/8πG lands the kernel, and the √(8πG) under the square root carries a factor π^(1/2) — an *odd* half-integer power of π, equal to Γ(½)/√π up to rationals. No curvature-free thermal/horizon route produces an odd power of π (those yield π^(integer): 2π, 4π, 1/2π); the half-integer is the fingerprint of the gravitational density normalization. The residual factor 2 = κ⁻¹ sits *outside* the square root, and every gravitational ½ in the construction (the surface-gravity ½, the Komar (ρ+3p) factor, equipartition) is already spent in building the cH_Λ and the 8π. **The entire unforced content of Eq. (1) is therefore one O(1) number, κ = ½:** a₀ is exactly half the gravitational free-fall acceleration √(Gρ_DE) at the dark-energy density. The framework is provably *not* the naive de Sitter–Unruh object cH/2π (Z/2π = 0.921, 8% off), so κ = ½ is a distinct, single, honest posit — not a derivation.

## 4. What is posited or unbuilt — stated plainly

I do not soften these. They are why this is not a theory of everything.

**4.1 The value of Λ is an input.** Equation (1) ties a₀ to Λ; it does not predict Λ. In the gauge construction Λ = 3/ℓ² enters with the choice of internal model-space curvature, present before any symmetry breaking. The proposal converts the cosmological-constant problem from "why this a₀" into "why this Λ," a real economy (one coincidence instead of two) but not a solution.

**4.2 The inertia mechanism is unbuilt, and its covariant home is a sibling, not a join.** Equation (4) is a constitutive law, not a derived microscopic dynamics: the map from the de Sitter–Unruh temperature, Eq. (3), to an effective inertial mass is posited, not computed, and a naive linear-response (passive-bath) realization gives the *wrong* sign (inertia rising at low acceleration). A conservative, time-nonlocal worldline action reproducing Eq. (4) **can** be constructed (three independent ways: a Galley even-kernel functional, an influence-functional, and a covariant branch-cut form factor), and it correctly obeys — rather than evades — the Milgrom (1994) no-go by being strongly time-nonlocal. But coarse-graining it does **not** reproduce the relativistic MOND theory AeST (Skordis & Złośnik 2021) as a unified action. The two share the deep-MOND limit |∇φ|³ = Y^{3/2} with the same a₀ and the same field content (a unit-timelike vector and a shift-symmetric scalar), but they agree only on the constant-acceleration (circular-orbit) locus and diverge off it; AeST's aether-kinetic sector is not produced. AeST is a **sibling effective field theory**, not the framework's covariant completion. The covariant modified-inertia theory remains open.

**4.3 The Standard Model is not produced; N = 3 is a parity obstruction.** Embedding gravity and a grand-unified group in one gauge structure (the graviGUT route) yields, from the non-compact Lorentzian signature, exactly *one* anomaly-free chiral family — a genuine, if singular, result. It does not yield the gauge group (an input), the masses (the mass sector is decoupled from a₀ by ~40 orders and shows no forced relation that survives a look-elsewhere correction), or the number of generations. I tested the most natural route to the last: the Dirac family-index of the relevant coset over the de Sitter nucleation four-sphere — the framework's own forced t = 0 saddle. It is well-defined but **cannot equal three**: the index reduces to the gauge instanton number scaled by the Dynkin index of the chiral family (the **16** of SO(10)), which is even, so the index is always even and N = 3 (odd) is **parity-forbidden** for any winding; and the de Sitter four-sphere is a simply-connected spacetime saddle, not the internal manifold that generation-counting requires. N = 3 therefore stays fitted — exactly as it is in every theory in physics; this is the universal status of the flavor puzzle, not a special failure of this proposal.

## 5. The empirical front

Two tests decide whether the distinctive (modified-inertia, declining-a₀) content is right; both are computed on the framework's own footing.

**5.1 Cassini and the ephemerides — in hand, discriminating modified inertia from modified gravity.** Because the framework's distinctive content is modified *inertia*, the gate μ switches the modification off where a ≫ a₀. At Saturn (a/a₀ = 6.9×10⁵) the fractional deviation from Newtonian inertia is 1 − μ = **1.05×10⁻¹²** — a factor **2.2×10⁷ below** the Cassini bound |γ−1| < 2.3×10⁻⁵ (Bertotti, Iess & Tortora 2003). Under the retired α = 1 kernel this was 7.2×10⁻⁷, a factor ~32 below; the α = 2 switch improves the margin by six orders.

**⚠️ AND THIS SECTION PREVIOUSLY OMITTED A HARDER TEST THAN γ.** It tested only |γ−1|, which is a statement about the *fractional* deviation. The α = 1 kernel's more dangerous consequence is a **constant sunward acceleration a₀/2 = 4.68×10⁻¹¹ m s⁻² that does not decay with a/a₀ at all** — an absolute, not fractional, anomaly, invisible to the γ argument. Against the Earth 2σ limit of 3.66×10⁻¹⁴ m s⁻² (Sereno & Jetzer 2006, Table 1, inverted through their Eq. 9) that is **1279× too large**, and the framework's own external-field effect suppresses it only to 119–189×. This liability was present in earlier versions of this paper and unstated. Under the α = 2 kernel the same anomaly is 1.3×10⁻¹⁸ m s⁻², i.e. **3.6×10⁻⁵ of the bound** — it passes with five orders to spare. The framework's modified inertia therefore **passes both the γ test and the ephemeris test**, but only on the α = 2 kernel, and readers of earlier versions should treat the γ-only argument as incomplete. An *ungated* modified-gravity completion of the same a₀ (AeST-class) instead predicts a solar-system deviation of order √(a₀/g) ∼ 10⁻³, which **fails** the same bound. Cassini is thus, already, a ~3-order-of-magnitude discriminator that favors the modified-inertia reading and excludes an ungated modified-gravity host — consistent with §4.2's finding that AeST is a sibling, not the framework.

**5.2 DESI w(z) and the declining a₀(z) — the hostage and the clean discriminator.** The one beyond-standard-MOND prediction is a declining acceleration scale tracking the dark-energy density, a₀(z) ∝ √ρ_DE(z). On a DESI-favored evolving-dark-energy background this gives the cleanly separated predictions

| z | ΛCDM | this proposal (√ρ_DE) | rival rising (a₀ ∝ cH) |
|---|------|------------------------|------------------------|
| 1 | 1.00 | 1.01 | 1.79 |
| 2 | 1.00 | 0.87 | 3.03 |
| **3** | **1.00** | **0.74** | **4.56** |

(a₀(z)/a₀(0)). Two stages decide it. **DESI w(z) decides the premise:** if dark energy is exactly Λ (w = −1), a₀(z) is constant and the distinctive content vanishes — the proposal degenerates to standard MOND. DESI's current preference for evolving dark energy keeps the premise alive (necessary, not sufficient). **High-redshift deep-MOND kinematics decide the shape:** the predicted a₀(z=3) ≈ 0.74·a₀(0) is ~6× separated from the rival rising branch (4.56) and from ΛCDM (1.00), and is reachable with extremely-large-telescope spectroscopy of z ∼ 3 disks this decade. I state the present status honestly and both ways: the **declining direction is contested, not confirmed** — intermediate-redshift integral-field measurements have reported a *rising* a₀(z), and present data are ΛCDM-degenerate. This front is genuinely open.

## 6. Discussion

The proposal earns a specific, limited claim. It is **not numerology**: the de Sitter–Unruh engine is verified physics (Deser & Levin 1997), the gravity action is certified unique in its class, the form a₀ ∝ c²√Λ is over-determined by four independent mechanisms, and the residual freedom is honestly one number. It is **not a theory of everything**: the value of Λ is an input, the inertia mechanism's covariant completion is unbuilt, and no piece of Standard-Model content is produced (N = 3 is a parity obstruction along the one natural route). What it is, is an **effective theory at a frontier** in which the galactic acceleration scale is a de Sitter curvature scale, the dark sector needs no particle, and a₀ is reduced to half the gravitational free-fall scale at the dark-energy density. It is not a theory of everything yet — as frustrating as it may be — but it is a defensible theory of gravity and the dark sector, and it is honest about exactly where it stops.

Three corrections to the earlier presentation of this proposal are folded in here in the interest of a referee-resistant record: the independent-mechanism count is four, not seven (§3.2); the de Sitter axiom is not a single minimal postulate but bundles four co-inputs (dimension, signature, the sign of Λ, and the breaking); and the gravity action's uniqueness is rigorous only with the two-derivative parity-even class stated explicitly (§3.1). Earlier claims that a discrete-holography (DSSYK) kernel *forces* the galaxy-scale sign, and that the coefficient is fixed by a unique entropy calculation, are **withdrawn**: those routes were found, on direct recomputation, to depend on free inputs and are not part of the present claim.

## 7. Conclusion

If the galactic acceleration scale is the curvature scale of the asymptotic de Sitter geometry, then a single, machine-certified line connects gauging the de Sitter group to a₀ = c²√(Λ/32π), with the entire unforced content reduced to one number, κ = ½, and no dark-matter particle. The price, stated without discount, is that the value of Λ is an input, the modified-inertia mechanism lacks a covariant home (its honest status is a sibling of AeST, not a join), and the Standard Model — including the number of generations, here a parity obstruction — is fitted. The proposal therefore stands or falls not as a theory of everything but as a falsifiable theory of gravity and the dark sector: Cassini already discriminates its modified-inertia content from a modified-gravity host, and the declining prediction a₀(z=3) ≈ 0.74·a₀(0), hostage to DESI's verdict on evolving dark energy, is the clean test this decade.

---

## Reproducibility

All quantitative claims are reproducible from the public repository `https://github.com/carlzimmerman/zimmerman-formula`. The three certification scripts are in `opus_48_extended_research/reviews/derivation_chain/` (`gap1_so41_invariant_uniqueness.py`, `gap2_germ_fingerprint_FDR.py`, `gap3_conservative_kernel_dissolves_antimond.py`); the graded chain and the empirical-front computation are in `opus_48_extended_research/reviews/` (`DERIVATION_CHAIN_COMPLETE_2026-06-15.md`, `EMPIRICAL_FRONT_AND_DEFENSIBLE_RESULT_2026-06-16.md`). Run with `pip install numpy scipy sympy mpmath`.

## Selected references

- Bertotti, Iess & Tortora (2003), *Nature* **425**, 374 — Cassini test of |γ−1|.
- Deser & Levin (1997), *Class. Quantum Grav.* **14**, L163 [gr-qc/9706018] — de Sitter–Unruh quadrature temperature.
- Lelli, McGaugh, Schombert & Pawlowski (2017), *ApJ* **836**, 152 — RAR/BTFR and a₀.
- MacDowell & Mansouri (1977), *Phys. Rev. Lett.* **38**, 739 — gauge gravity from SO(4,1)/SO(3,2).
- McGaugh, Lelli & Schombert (2016), *Phys. Rev. Lett.* **117**, 201101 — the radial acceleration relation.
- Milgrom (1994), *Ann. Phys.* **229**, 384 [astro-ph/9303012] — modified-inertia no-go (nonlocality).
- Milgrom (2022), [arXiv:2208.07073] — modified-inertia formulation and energy conservation.
- Skordis & Złośnik (2021), *Phys. Rev. Lett.* **127**, 161302 [arXiv:2007.00082] — AeST relativistic MOND.
- Wise (2010), *Class. Quantum Grav.* **27**, 155010 [gr-qc/0611154] — MacDowell–Mansouri and Cartan geometry.

*Both-ways statement. Credited at full weight: the certified-unique gravity action, the four-mechanism over-determination of the form, the √π-carrying gravitational kernel reducing the freedom to κ = ½, and the in-hand Cassini discriminant. Conceded at full weight: Λ is an input, the inertia mechanism's covariant completion is unbuilt (sibling, not join), the Standard Model and N = 3 are fitted (the latter a parity obstruction), and the declining a₀(z) direction is contested. No quantity a₀, Z, or κ is asserted derived. This is an effective theory at a frontier, not a theory of everything.*
