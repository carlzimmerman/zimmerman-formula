# The de Sitter–Unruh Modified-Inertia Theory: A One-Parameter Account of the MOND Acceleration Scale

**Carl P. Zimmerman**
Briar Creek Tech
2026-06-27

---

## Abstract

I present the de Sitter–Unruh modified-inertia (MI) theory as a self-contained, **one-parameter** physical account of the MOND acceleration scale a₀ — explicitly **not** a theory of everything. The theory rests on two physical inputs. First, an accelerated body immersed in a de Sitter universe sees a thermal bath at the Deser–Levin temperature T(a) = (ℏ/2πk_Bc)√(a² + (cH_Λ)²), which never falls below a universal floor T₀ = ℏcH_Λ/(2πk_Bc) = 2.20 × 10⁻³⁰ K set by the dark-energy horizon alone. Second, a relational/Machian principle: a body's force-responsive (dynamical) inertia is the **excess** of its bath response above that universal floor — a body unaccelerated relative to the cosmic vacuum carries no dynamical inertia. From these two inputs, four structures follow as consequences rather than fits: (i) the **scale** a₀ = cH_Λ/Z ∼ √Λ; (ii) the **interpolation form** μ_fw(x) = (√(1+4x²)−1)/2x, with the strikingly clean inverse μ/(1−μ²) = a/a₀, realized as the minimum of a convex, ghost-free potential; (iii) the **memory kernel** θ(0) = √2 (amplitude-branch selection) with a Lorentzian shape forced by the de Sitter Wightman function; and (iv) the **MOND sign** itself — the relational principle selects inertia-weakening (MOND) and rejects the passive-bath, inertia-raising (anti-MOND) reading. What remains is a single free number Z, provably free (κ-closure), entering exactly as Newton's G enters general relativity. I keep the honesty explicit and two-sided throughout: the sign is **conditional on the Machian premise** (the honest crux); Z and hence a₀'s numerical value are **not derived**; and the Standard-Model mass sector stays **walled** — this is a one-parameter theory of one infrared scale, **not a TOE**. The theory is consistent with, and assembles, the previously published effective-field-theory results (DOIs 10.5281/zenodo.20935948, 20938891, 20947913, 20963226) and with the author's 2026 retraction of all earlier TOE/Standard-Model overclaims. Predictions: an s^TX Lorentz-violation dipole, an a₀(z) "hostage" tied to the dark-energy equation of state, a modified-gravity-impossible dwarf orbital-history dispersion signature, and a definite floor temperature T₀ = 2.20 × 10⁻³⁰ K.

---

## 1. The two physical inputs

This paper takes one physical proposal as its subject and reasons forward from that proposal's own premises. It is not a variant of Milgrom's MOND and is not to be read through MOND's lens; where the standard MOND apparatus appears, it appears as a *consequence*, downstream of the two inputs stated here, never as a baseline against which the theory is judged.

### 1.1 Input A — the de Sitter–Unruh bath and its universal floor

An observer with proper acceleration a in a de Sitter universe sees a thermal bath. Combining the Unruh effect with the Gibbons–Hawking temperature of the cosmic horizon, Deser & Levin (1997) give the temperature such an observer measures as

> **T(a) = (ℏ / 2πk_Bc) · √( a² + (cH_Λ)² ),**

where H_Λ is the de Sitter rate fixed by the dark-energy density alone — the pure-Λ horizon clock, **not** the instantaneous Hubble rate H(z). Numerically cH_Λ = 5.42 × 10⁻¹⁰ m/s² and H_Λ = 1.81 × 10⁻¹⁸ s⁻¹ (a horizon time 1/H_Λ ≈ 17.5 Gyr).

The structure that does the work is the additive (cH_Λ)² under the root. Even a body at perfect rest (a = 0) does not see zero temperature; it sees a universal floor

> **T₀ ≡ T(0) = ℏcH_Λ / (2πk_Bc) = 2.20 × 10⁻³⁰ K.**

This floor is the Gibbons–Hawking temperature of the cosmic horizon. It is shared identically by every body and by the geodesic vacuum itself: nothing is colder, or more at rest, than the cosmic vacuum. The floor is universal in the precise sense that dT₀/da = 0 — it is the same constant for all bodies and carries no information about any particular body's state of motion.

This input is established physics in its kinematic content: the Deser–Levin temperature is a real property of de Sitter space. The further *reading* — that this temperature is what a body's inertia responds to — is the theory's postulate, made explicit in Input B and again in §5.

### 1.2 Input B — relational/Machian inertia: dynamical inertia is the excess above the floor

The second input is a principle about what inertia *is*. In a relational (Machian) view, inertia is a body's resistance to acceleration **relative to the rest of the universe**, not relative to absolute space. The universal, body-independent contribution to the bath response is the shared floor T₀. The theory's principle is then sharp:

> **The force-responsive (dynamical) inertia of a body is the EXCESS of its bath response above the universal de Sitter floor T₀. A body unaccelerated relative to the cosmic vacuum has zero dynamical inertia.**

The kinematically meaningful, body-specific quantity is therefore not T(a) but the floor-subtracted excess. A short computation (sympy-verified) gives the clean fact that drives everything downstream:

> **√( T(a)² − T₀² ) = (ℏ / 2πk_Bc) · a,    exactly linear in a.**

The excess responds to force: d√(T²−T₀²)/da |₀ = ℏ/2πk_Bc, finite and nonzero. The full temperature does **not** respond at the floor: dT/da |₀ = 0. So the force-responsive piece of the inertia is *necessarily* the excess, and necessarily *linear* in the acceleration amplitude — a point that will matter for both the form (§3) and the kernel (§4).

These two inputs — the bath with its floor (A), and the relational excess principle (B) — are the entire physical foundation. Everything in §§2–5 is a consequence of them, together with one shape posit (the √-equation-of-state, stated where it is used) and one free number (§6).

---

## 2. The derived scale: a₀ = cH_Λ/Z ∼ √Λ

The acceleration at which the bath response becomes order-unity — where the excess √(T²−T₀²) becomes comparable to the floor T₀ itself — is set by the single rate in the problem, cH_Λ. The crossover is

> **a₀ = cH_Λ / Z = 9.36 × 10⁻¹¹ m/s²,**

with Z the theory's geometric normalization (the lone free number, §6). Because cH_Λ ∝ H_Λ ∝ √(ρ_Λ) ∝ √Λ, the scale is

> **a₀ = (c/2)·√(G ρ_DE) ∼ √Λ.**

This is the load-bearing structural success: the MOND scale is not a fitted input but a **horizon-derived** acceleration, locked to the dark-energy density. Three consequences follow immediately, all forced for a w = −1 (constant-Λ) cosmology:

- **a₀ is a cosmic constant at every epoch.** Because the bath clock is the dark-energy horizon and ρ_DE is flat, a₀ = 9.36 × 10⁻¹¹ is identical at big-bang nucleosynthesis, recombination, cosmic noon, today, and in the infinite future. The MOND scale does not evolve (for w = −1).
- **The CMB acoustic epoch is deep-Newtonian.** A recombination-era fluid element has RMS acceleration ∼ 5 × 10⁻⁸ m/s² ≫ a₀, i.e. x ∼ 500 ≫ 1, so the modification is sub-percent and the acoustic peaks are untouched. The theory does not distort the CMB under constant a₀.
- **The Machian limit is sharp.** As Λ → 0, cH_Λ → 0, a₀ → 0, so x → ∞ for every finite acceleration and μ_fw → 1 everywhere: pure Newton, no MOND. The horizon sources 100% of the low-acceleration inertia deficit, while the rest-mass coupling survives. The theory is, precisely and by its own statement, *half-Machian*.

What §2 does **not** do is fix Z, and therefore it does not fix a₀'s numerical value. The scale's *form* (∼ √Λ) is forced; its *normalization* is the one free parameter. This boundary is held throughout (§6, Quarantine).

---

## 3. The derived form: μ_fw and the convex ghost-free potential it minimizes

The relational excess of Input B is linear in a (§1.2). To turn that excess into the body's inertia ratio μ = m_inertial/m_rest one needs a constitutive shape — the theory's √-equation of state,

> **g_obs = √( g_bar² + g_bar·a₀ )    (the framework's own interpolation).**

Solving this for the inertia ratio μ = g_bar/a as a function of x = a/a₀ gives, with no further input (sympy-verified),

> **μ_fw(x) = (√(1 + 4x²) − 1) / (2x),**

with the correct limits μ → x deep (a ≪ a₀, inertia strongly lowered) and μ → 1 Newtonian (a ≫ a₀), approaching 1 strictly from below as 1 − μ_fw → a₀/2a with **no high-acceleration ceiling**. Written in the relational excess variable u = 2Z√(T²−T₀²)/T₀ — which collapses *exactly* to u = 2x because T²−T₀² = (ℏa/2πk_Bc)² and T₀ = (ℏ/2πk_Bc)·Z a₀ — the same function is

> **m_I/m_rest = (√(1+u²) − 1)/u = tanh( ½·asinh(u) ),    u = 2x,**

reproducing μ_fw to machine precision (residual 0.0 over seven decades in x; the tanh–asinh identity verified to ∼10⁻³⁸ in mpmath). The cleanest statement of the law is its inverse:

> **μ / (1 − μ²) = a / a₀ = x    (sympy-exact).**

Two structural facts make this a *constitutive theory*, not merely a suggestive curve:

- **It minimizes a convex, ghost-free potential.** μ_fw is the unique stable minimum of the Landau/Legendre potential Φ(μ; x) = μ²/2 − x·μ + x·μ³/3, since dΦ/dμ = 0 ⇔ μ/(1−μ²) = x (the inverse identity above) and Φ″ = 1 + 2xμ > 0 everywhere. The equation of state is the extremum of a convex potential bounded below — the response is single-valued and stable.
- **It is causal and free of the Ostrogradsky ghost.** As an *algebraic* state law g_bar = G(a) — a constitutive closure like p = p(ρ) — the equation of motion is the ordinary second-order ẍ = √(g_bar² + g_bar·a₀) with g_bar = GM/r². There is no acceleration inside the law, hence no higher-derivative ghost; this is precisely how the theory evades the local-gating trap (gating inertia by |a| in the action would put ẍ in the Lagrangian and produce a ghost; an equation of state does not). The force↔acceleration map is monotone and invertible (dg_bar/dx = 2x/√(4x²+1) > 0), and the associated response energy is convex.

A useful exact fact at the scale itself: μ_fw(1) = (√5 − 1)/2 = 1/φ = 0.61803…, the inverse golden ratio. A body at a = a₀ retains exactly φ⁻¹ of its rest inertia.

**Honesty marker.** The clean form lives in the *kinematic* excess variable √(T²−T₀²) ∼ a, not in the plain excess heat ΔT = T(a) − T₀. The literal "g_bar ∝ ΔT" heat law matches deep-MOND (ΔT ∝ a² there, matching deep-MOND g_bar ∝ a²) but then **overshoots to ∼11×** at high acceleration. So "inertia is a natural function of the heat" is true only in the deep limit; the full law is natural as a function of the kinematic excess (which is a in disguise). The √-shape is a posit (Input A's equation-of-state reading), not forced by the Machian principle, which fixes only the *argument* (excess-over-floor) and the boundaries g(0) = 0, g(∞) = 1.

---

## 4. The derived kernel: θ(0) = √2 and the Lorentzian shape

Because the theory is modified **inertia** and the bath is nonlocal in time, a body's inertia depends on its recent acceleration *history*, not only the instantaneous value. In an external field this is encoded by a history kernel θ(y) entering the effective acceleration argument A = a_internal + θ(y)·a_external, where y = ω_external/ω_internal is the ratio of the external (orbital) frequency to the body's internal frequency. Two features of θ are fixed by the bath itself.

**The DC weight θ(0) = √2.** Two independent framework-internal routes converge. First, the excess-heat engine: the inertia tracks the excess √(T²−T₀²), which is degree-1 (linear) in the acceleration amplitude, so θ multiplies an amplitude, not an energy; the −3 dB corner of an amplitude transfer sits at 1/√2, giving θ(0) = √2. (The alternative θ(0) = 2 would require re-admitting the rejected T²/energy reading, or a second independent memory clock — and the theory has a single Λ, a single dS clock.) Second, the additive-acceleration construction (Luo 2026): by the equivalence principle a static external field enters the first moment of the bath response at unit weight, while the variance-subtraction channel is owned by Λ alone — again the amplitude branch, again √2.

**The Lorentzian shape.** The de Sitter worldline correlator (Wightman function) is W(u) = −(κ²/16π²)/sinh²(κ(u−iε)/2), κ = 2πT_eff. Its large-separation envelope is exponential, e^(−κ|u|), which is precisely a Lorentzian transfer 1/(1 + (ω/ω_c)²) in the frequency domain (with a y⁻² tail). The kernel's *form* is therefore correlator-forced, no longer a bare ansatz.

So the kernel reads θ(y) = θ₀/(1 + (θ₀−1)y²) with θ₀ = √2 and θ(1) = 1, decreasing monotonically with an exact zero-crossing of the *relational effect* at y = 1.

**Honesty marker.** What the de Sitter correlator does **not** hand over is the *location* of the corner. Taken literally the bath scale κ ∼ H_Λ is far below every orbital frequency, so the corner at y = 1 (external frequency = internal frequency) rides on the "internal orbit = the averaging bandwidth" postulate, licensed by Milgrom (1994) only in the quasi-static limit; the general multi-frequency case is obstructed, not closed. A memory-order residual also survives: a single-pole memory gives (θ(0) = √2, tail y⁻¹) and a two-pole gives (θ(0) = 2, tail y⁻²); KMS alone does not fix the pole count. The honest classification is **plausible-with-forced-core**: existence of the corner, the DC value √2, and the Lorentzian form-class are bath-derived; the corner *location* and the memory order are modeling choices.

---

## 5. The sign — the relational principle selects MOND (conditional on Mach)

This is the deepest result and the honest crux of the theory, so it is stated carefully and two-sided.

There are two readings of the bath response, mirror images across μ = 1:

- the **absolute** reading R_abs = T/T₀, which gives R_abs(0) = 1 — full inertial reaction assigned to an *unaccelerated* body. This is absolute-space inertia, and it is **identically** the passive-bath, dissipative-drag result one obtains from the Feynman–Vernon/Hu–Verdaguer influence functional built on the de Sitter KMS bath: that bath is passive (it satisfies detailed balance, sympy-verified), so its back-reaction kernel has Källén–Lehmann-positive spectral density and yields δm ≥ 0 — inertia *raised* at low a, the **anti-MOND** sign.
- the **relational/excess** reading R(u) = (√(1+u²)−1)/u = μ_fw, which gives R(0) = 0 — zero dynamical inertia for an unaccelerated body. This is the **MOND** sign (inertia lowered at low a).

The relational/Machian principle of Input B does genuine selective work here, beyond mere naming. At a = 0 a body is geodesic — locally indistinguishable from rest in the cosmic frame — so by the equivalence principle / Mach it feels **no inertial reaction**. The absolute reading R_abs(0) = 1 assigns full inertial reaction to that unaccelerated body, the very thing Mach and the equivalence principle deny. The Machian principle therefore supplies an **independent criterion** — not a redescription of "subtract the floor" — that rejects the absolute/anti-MOND reading and selects the excess/MOND reading. And the reading it kills is *exactly* the passive-bath influence-functional result that has otherwise been forcing anti-MOND. The relational excess response reproduces μ_fw to literally zero (sympy), in closed form tanh(½ asinh(2x)).

This is why the passivity→anti-MOND theorem does not bind the theory: the relational reading is a *state function* (an equation of state), not a dissipative kernel; the no-go theorem applies to the kernel category, which is the absolute reading, and Mach is the principled reason to discard that category. So the MOND sign is upgraded from a bare definitional posit ("define inertia to vanish at the floor") to a **consequence of a named physical premise**.

**The cost, paid to the millimeter (honesty marker).** The selection is **conditional on the Machian premise**. Three independent checks confirm that nothing weaker forces the sign:

1. **No thermodynamic extremum forces it.** Every bath state variable — T(a), entropy S(a), excess heat Q(a) — is even in a (T ∼ √(a² + (cH_Λ)²)). So any free-energy or entropy extremum yields μ ∼ a² at low a, the *wrong* deep-MOND slope (μ_fw ∼ a is linear/odd). The linear drive that reproduces μ_fw is the floor-subtraction itself — the input, not the output. Stability *admits* the MOND sign (the anti-MOND potential is also locally convex) but does not *select* it.
2. **A two-bath non-equilibrium steady state breaks detailed balance but not passivity.** Adding a local field bath to the cosmic floor produces a nonzero steady heat current, yet the inertial shift remains a sum of two passive (positive) spectral densities ⇒ δm ≥ 0 = anti-MOND still. Breaking detailed balance redistributes energy; it never installs the negative spectral density (gain medium) the MOND sign would need.
3. **A temperature-independent sign theorem closes the active candidates.** For any KMS bath the detailed-balance factor (1 − e^(−ω/T)) is strictly positive for all ω, T > 0, so Im χ ≥ 0 independent of temperature — heating the bath cannot flip the dissipation sign. A growing de Sitter horizon is adiabatic versus any orbit by factors of 10²–10³ and, if it pumped at all, would have positive entropy production (dissipative = anti-MOND).

So the sign is derived **given Mach**, not by thermodynamics alone, and not by any passive mechanism. What was traded for the bare sign-posit is the Machian premise itself (that inertia is relational, and that the de Sitter vacuum frame is the cosmic rest frame). That is a genuine upgrade — a posit replaced by a deeper, more falsifiable premise carrying new content (a real universal floor temperature T₀ = 2.20 × 10⁻³⁰ K) — but it is **not a free lunch**, and the theory states the sign as conditional on Mach.

**The premise is not free-floating: it factors, and most of it grounds.** The Machian premise decomposes into the *existence* of a physical relational reference and the *definition* of inertia as the excess over its floor. The first clause is **not a new posit** — the reference is the same de Sitter-vacuum / cosmic rest frame the theory already carries and is *already constrained on* at Cassini through the s^TX dipole, and T₀ is the Gibbons–Hawking temperature of exactly that frame; the equivalence-principle boundary (geodesics unmodified) then falls out for free, since the bath is flat at the floor, dT/da|₀ = 0, for *any* version of the law. What does **not** reduce is a single clause — the floor-subtraction, i.e. common-mode rejection of T₀ — and it is not derivable from renormalization either, for a precise reason. Renormalization mandates subtracting the a = 0 reference only for **gauge** quantities (energy, work), which enter dynamics through *differences*, so the shared constant T₀ cancels and the subtraction is forced and content-free. Inertial mass is **non-gauge**: it enters as F = m a, so its absolute level at a = 0 is physical (the absolute and relational readings differ at every a > 0 by exactly 1). Tellingly, the theory subtracts T₀ for inertia *alone* while retaining it for s^TX, for velocity relative to the frame, and as a *reported* floor temperature — exactly what a universal vacuum-subtraction principle would forbid. The foundation, stated precisely, is therefore: **the equivalence principle + the de Sitter bath + the (Cassini-constrained) preferred frame + one irreducible, falsifiable Machian premise** — *inertia is the work-doing excess over the cosmic floor; a body at rest in the vacuum carries no dynamical inertia* — respectable in the way the equivalence principle itself was once a stated premise, and with a clear reason (the non-gauge character of inertia) why it does not reduce further.

---

## 6. The one free parameter: Z

The theory has exactly one free number, the geometric normalization

> **Z = 2√(8π/3) = √(32π/3) = 5.7888,    so that a₀ = cH_Λ/Z = 9.36 × 10⁻¹¹ m/s².**

Z is **provably free** by the κ-closure result (DOI 10.5281/zenodo.20963226): the normalization κ of the relevant action is the overall scaling of a φ₋-linear term, and no-ghost/stability/sound-speed conditions, unitarity (signs/causal structure/ratios only), and holography (the sole dimensionless group cancels classically) are all invariant under it. Nothing among those structural requirements fixes Z. An attempt to fix it microscopically (the CKN ultraviolet–infrared bound, matched to a Standard-Model degree-of-freedom count) returns *not-fixed*: the honest count gives an O(1) coefficient that is a function of the degree-of-freedom number, whereas the theory's normalization is pure geometry (Friedmann-3, Einstein-8π), the no-content (degree-of-freedom = 1) limit. Z is geometric, not microscopic, and it is the allowed single free number of a one-parameter theory.

The right analogy is Newton's constant in general relativity. GR derives the *structure* of gravity — the field equations, the geodesic law, light bending, the perihelion shift — with one dimensionful constant G that the theory does not predict and that must be measured. Here the theory derives the *structure* of the MOND scale — its ∼ √Λ form, the interpolation, the kernel, the sign — with one normalization Z that the theory does not predict. **a₀'s numerical value is not derived; its form and all its consequences are.** This is what makes the proposal a one-parameter theory rather than a zero-parameter one, and it is stated plainly rather than hidden.

---

## 7. Predictions

The theory's live content is empirical. Four predictions, ordered roughly by decisiveness:

1. **An s^TX Lorentz-violation dipole.** A preferred-frame modified-inertia theory is, in the Standard-Model-Extension language, a gravity-sector background s_μν. The same a₀/|a| that produces MOND induces a computable boost-dipole coefficient s^TX. The component-by-component value sits at roughly Saturn 8.68 × 10⁻¹⁰, about 1.5× the tightest current planetary-ephemeris (INPOP/Cassini) bound — the more decisive near-term gravity-side test, analysis-limited over ∼2028–2032. The companion CPT-even-only theorem (Lorentz-violating but CPT-preserving) is a structural prediction of the same construction.

2. **The a₀(z) hostage.** Because a₀ ∝ √(ρ_DE(z)), a₀ is exactly constant if w = −1 but evolves if the dark-energy equation of state does. Under the DESI/CPL fit (w₀ = −0.752, wₐ = −0.86) the scale shows a phantom-divide bump of ∼ +6% near z = 0.405 and a steep decline at high z (∼ −26% by z = 3), testable as a Baryonic-Tully-Fisher-zeropoint / rotation-curve normalization drift. This prediction **dissolves entirely if w → −1** — it is a hostage to the equation of state, stated as non-diagnostic until the data sharpen (DESI DR3 gate 2026–27; ELT tracking early-mid 2030s).

3. **A modified-gravity-impossible dwarf orbital-history dispersion.** Because inertia here is a functional of acceleration *history*, a diffuse dwarf galaxy on a radial-plunge orbit should run hotter (larger internal σ) than a circular-orbit dwarf of the same mass and same closest approach. At the selected θ(0) = √2 the boost is +12–14% in the realistic plunging band (a +12–30% envelope spanning the memory-order residual), with an exact zero-crossing at y = 1. This is **modified-gravity-impossible**: in any metric or field MOND (AQUAL/QUMOND/AeST) and in ΛCDM the external-field effect is instantaneous (internal dynamics depend only on the *momentary* external acceleration), so those theories predict exactly zero σ-vs-history correlation at fixed pericenter, for any a₀. The named carriers reaching the non-adiabatic band are Crater II (y = 3.28) and Antlia II (y = 2.55) against adiabatic controls Fornax and Sculptor. The decisive test is Gaia DR4 (December 2026) plus diffuse-carrier spectroscopy. A pre-registered pilot on 24 Milky-Way dwarfs is a statistically underpowered **null** (partial Spearman ρ = −0.196, p = 0.395) — existing data cannot yet test it (DOI 10.5281/zenodo.20947913).

4. **The floor temperature T₀ = 2.20 × 10⁻³⁰ K.** The theory predicts a real, universal de Sitter floor temperature shared by every body — the Gibbons–Hawking temperature of the cosmic horizon — as the athermal reference from which dynamical inertia is measured. It is the new falsifiable content the Machian upgrade carries.

---

## 8. Honest scope and open doors

The two-sided ledger, repeated and explicit, because the theory's credibility rests on it:

- **The sign rests on the equivalence principle, the bath, the Cassini-constrained preferred frame, and one irreducible Machian premise.** §5 shows the premise *factors*: its relational *reference* is the framework's own (already s^TX-constrained) preferred frame, and the equivalence-principle boundary is automatic from the bath's flat floor — neither is a new posit. The single clause that does not reduce is the *floor-subtraction* (common-mode rejection of T₀), and it is provably not forced by renormalization (which mandates subtracting the a = 0 reference only for **gauge** quantities; inertial mass is **non-gauge**) nor by any thermodynamic extremum or non-equilibrium steady state. This is the honest crux: a single, named, falsifiable premise — not a free lunch, and now with a clear reason (inertia's non-gauge character) why it is irreducible.

- **Z, and hence a₀'s value, is not derived.** Z is provably free (κ-closure). The theory is one-parameter, not zero-parameter; a₀'s *form* ∼ √Λ is forced, its *normalization* is the one measured number.

- **The Standard Model is walled — this is NOT a TOE.** The kernel fixes one infrared scale (a₀ ∼ cH_Λ). It does not count, quantize, or pattern Standard-Model masses; the flavor-disjoint-representation and forced-kernel walls stand. The author has publicly retracted (2026) all earlier TOE / Standard-Model-derivation overclaims; the honest position is the a₀ reframing only, and this paper makes no claim beyond it.

The named open doors, stated so that none is dressed as closed:

1. **Ground the floor-subtraction.** The relational *reference* and the equivalence-principle boundary now reduce to the framework's Cassini-constrained preferred frame and the bath; the one clause still standing is *why* inertia is the **work-doing excess** over the cosmic floor — i.e. why common-mode rejection of T₀ beats the absolute/passive-bath reading. This is shown *not* forced by renormalization (gauge vs non-gauge) or by thermodynamics, so a first-principles modified-inertia reason for it is the genuine remaining theory door.
2. **Establish the √-shape's necessity.** The interpolation form is the equation-of-state posit; Mach fixes only the argument and the boundary conditions, not the √-shape.
3. **The named active pump.** The lone un-theorem'd reopener on the kernel side is an in-band active galactic mechanism that would break de Sitter passivity in-band — which would also have to explain a₀'s observed universality. Not supplied by any passive source examined here.
4. **The kernel corner location and memory order** (§4) remain quasi-static modeling choices.

The theory is consistent with, and is the capstone of, the previously published effective-field-theory results: the de Sitter–Unruh a₀ no-go and one-free-number papers (DOIs 10.5281/zenodo.20935948, 20938891), the κ-closure / one-free-number result (DOI 10.5281/zenodo.20963226), and the dwarf orbital-history prediction (DOI 10.5281/zenodo.20947913). It claims to be exactly what those papers, and the retraction, support: a one-parameter modified-inertia account of a single infrared scale — **a theory, in the one-parameter sense, not a theory of everything.**

---

## Reproducibility note

All symbolic and numerical results above were verified with sympy, numpy, and mpmath: the linear excess identity √(T²−T₀²) = (ℏ/2πk_Bc)·a and the floor universality dT₀/da = 0 (Input B); the equation-of-state solve μ_fw = (√(1+4x²)−1)/2x with the inverse μ/(1−μ²) = x, the variable collapse u = 2x, and the identity (√(1+u²)−1)/u = tanh(½ asinh u) to ∼10⁻³⁸ (§3); the convex potential Φ = μ²/2 − x μ + x μ³/3 with unique stable minimum at μ_fw and Φ″ = 1 + 2xμ > 0, and the monotone-invertible, ghost-free force map (§3); the θ(0) = √2 amplitude-branch selection and the Lorentzian/exponential-memory envelope of the de Sitter 1/sinh² correlator (§4); the KMS detailed-balance relation S(−ω)/S(ω) = e^(−βω), the passive δm ≥ 0 result both spectrally and on the 1/sinh² kernel, the two-bath steady-current-but-still-passive result, and the temperature-independent (1 − e^(−ω/T)) > 0 sign theorem (§5); and the κ-closure invariance establishing Z as free (§6). Footing throughout: a₀ = cH_Λ/Z = 9.36 × 10⁻¹¹ m/s², Z = √(32π/3) = 5.7888, cH_Λ = 5.42 × 10⁻¹⁰ m/s², T₀ = 2.20 × 10⁻³⁰ K, and the framework's own interpolation μ_fw and Deser–Levin T(a) — never McGaugh's ν. Supporting scripts accompany the source memoranda (DERIVE_THE_SIGN, CONSTITUTIVE_LAW_SWING, INFLUENCE_FUNCTIONAL_DELTAT_INERTIA, THETA_KERNEL_TOWARD_FORCED, MAXIMAL_EXTRAPOLATION).

---

*Framework-internal throughout; no rival-theory comparison is used to judge the theory. Both-sided honesty (forced vs posited) is stated at every step. Not a theory of everything.*
