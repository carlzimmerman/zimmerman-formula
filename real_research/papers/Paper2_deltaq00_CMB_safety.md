# Paper II — Why a running MOND scale does not break the CMB: the δq⁰⁰ = 0 identity

**Carl Zimmerman** · June 2026 · *full pedagogical write-up · companion to Paper I (the construction)*

---

## Abstract

In the evolving-MOND realization of Paper I, the acceleration scale a₀ grows toward the past as
a₀(z) = a₀(0)E(z). At the surface of last scattering (redshift z ≈ 1090, where the cosmic
microwave background was emitted) this makes a₀ roughly **twenty thousand times** its present
value. A scale that large could, in principle, wreck the exquisitely measured acoustic peaks of
the CMB. We prove it does not — exactly, at linear order in cosmological perturbations. The proof
has two parts. First, a₀ enters the action only through a term that is *third order* in the small
scalar perturbation δφ, and so cannot contribute to the *linear* equations of motion. Second — the
subtle part, which a naive counting drops — a single dangerous term survives that simple argument,
proportional to a perturbation δq⁰⁰ of the spatial projector. We show this term **vanishes
identically**, because the aether's unit-timelike constraint forces the perturbation of its time
component to be exactly δA⁰ = −Ψ, which cancels the metric perturbation δg⁰⁰ = +2Ψ. Hence
δq⁰⁰ = 0, the a₀-term is genuinely O(δφ³), and the running of a₀ leaves the linear CMB and matter
power spectrum *exactly* invariant. We confirm this numerically and state clearly the one thing
the theorem does not cover: the second-order effect, which is estimated to be small but is left
open.

---

## 1. Introduction — the worry, stated plainly

### 1.1 What the CMB is and why it is precise
The cosmic microwave background is the oldest light in the universe — a snapshot of the hot plasma
at z ≈ 1090, about 380,000 years after the Big Bang. Before that moment, photons and baryons
oscillated together as a single fluid; the **acoustic peaks** in the CMB's temperature spectrum
are a photograph of those sound waves frozen at last scattering. Their *positions* fix the sound
horizon and the geometry; their *relative heights* fix the baryon and dark-matter densities. Planck
measured them to fractions of a percent. Any new physics that distorts them at the percent level is
dead on arrival.

### 1.2 The specific danger
MOND modifies gravity below the acceleration a₀. In the evolving model, a₀(z_rec) ≈ 2.4×10⁻⁶
m s⁻² — about 2×10⁴ times today's value. Naively, a far larger MOND scale at recombination means a
far wider regime in which gravity is modified, which could badly distort the acoustic physics. **Is
the model already ruled out by the CMB?** This paper answers: no, and shows exactly why.

### 1.3 The result in one sentence
The acceleration constant a₀ couples only to a term that is *cubic* in the small scalar
perturbation, so it drops out of the *linear* perturbation equations — and the one loophole in
that statement is closed by an exact cancellation enforced by the aether's defining constraint.

---

## 2. Setup — where a₀ enters, and the language of perturbations

### 2.1 Recap of the host theory
From Paper I: the relativistic-MOND theory (AeST) has a metric g_μν, a scalar φ, and a
unit-timelike aether A_μ (A^μA_μ = −1). The acceleration constant a₀ appears **only** as the
coefficient of the spatial term

$$\mathcal F \supset \frac{2\lambda_s}{(1+\lambda_s)\,a_0}\,\mathcal Y^{3/2},\qquad
\mathcal Y = q^{\mu\nu}\nabla_\mu\phi\,\nabla_\nu\phi,\quad q_{\mu\nu}=g_{\mu\nu}+A_\mu A_\nu.$$

Here q_{μν} = g_{μν} + A_μA_ν is the **spatial projector**: it removes the part of any gradient
that lies along the aether's time direction, keeping only the spatial part. The cosmological
"dark-matter-mimicking" sector lives in a *different* function 𝒦(𝒬) that contains *no* a₀. (Paper I,
§2.3.) The running-a₀ modification of Paper I, a₀ → cθ/3Z, only multiplies the 𝒴^{3/2} term by
1/θ; since on the background θ̄ = 3H̄ ≠ 0, this does not change any of the counting below.

### 2.2 Cosmological perturbation theory — the bookkeeping
We split every field into a smooth background plus a small perturbation. On the cosmological
background (FRW), the scalar is homogeneous, φ̄ = φ̄(t); a galaxy or a CMB ripple is a small
perturbation δφ on top. We work in the standard "longitudinal gauge," where the metric is

$$ds^2 = -(1+2\Psi)\,dt^2 + a^2(t)(1-2\Phi)\,\delta_{ij}\,dx^i dx^j,$$

with two small potentials Ψ and Φ. The **order** of a quantity counts powers of the perturbation:
δφ, Ψ, Φ are all "first order." The CMB acoustic physics is governed by the **linear** (first-order)
equations. Anything that only appears at second order or higher (∝ δφ², δφ³, …) is irrelevant to
the linear spectra. *The whole proof is a statement about what order a₀ appears at.*

---

## 3. The order-counting argument — a₀ is cubic

The acceleration constant sits in 𝒴^{3/2}. We track the order of 𝒴.

**Background.** On FRW the scalar is purely temporal, ∇_μφ̄ = (φ̄′, 0, 0, 0). The projector q̄^{μν}
removes the time direction. Concretely its time-time component is

$$\bar q^{00} = \bar g^{00} + (A^0)^2 = (-1) + (1) = 0,$$

because g^{00} = −1 and A^0 = 1 on the background. Therefore

$$\bar{\mathcal Y} = \bar q^{\mu\nu}\nabla_\mu\bar\phi\,\nabla_\nu\bar\phi = \bar q^{00}(\dot{\bar\phi})^2 = 0.$$

The spatial projection of a purely temporal gradient vanishes. So **𝒴 is zero on the background.**

**First order.** Expanding 𝒴 = q^{μν}∇_μφ∇_νφ to first order gives two pieces:

$$\delta\mathcal Y = \underbrace{\delta q^{\mu\nu}\,\nabla_\mu\bar\phi\,\nabla_\nu\bar\phi}_{\text{(A) projector perturbation}}
+ \underbrace{2\,\bar q^{\mu\nu}\,\nabla_\mu\bar\phi\,\nabla_\nu\delta\phi}_{\text{(B) gradient perturbation}}.$$

Piece **(B)** vanishes immediately: 2q̄^{μν}∇_μφ̄∇_νδφ = 2q̄^{0ν}φ̄′∇_νδφ, and the background
projector has q̄^{00} = 0 and q̄^{0i} = 0, so the whole thing is zero. *This is the part the
standard order-counting computes.* If that were the whole story, δ𝒴 = 0 and we would be done.

**But piece (A) is the loophole.** Because ∇_μφ̄ is purely temporal, only the time-time component of
δq^{μν} survives in (A):

$$\text{(A)} = \delta q^{00}\,(\dot{\bar\phi})^2.$$

This is *not* obviously zero — it depends on whether δq^{00} vanishes. **If δq^{00} ≠ 0, then
δ𝒴 ≠ 0, the a₀-term would appear at second order, and a₀ would leak into the linear CMB.** The
entire safety of the construction comes down to a single number: δq^{00}.

---

## 4. The theorem — δq⁰⁰ = 0, from the aether's constraint

We now show δq^{00} = 0 exactly, to first order. There are two contributions:

$$\delta q^{00} = \delta g^{00} + 2 A^0\,\delta A^0.$$

**The metric piece.** From g_{00} = −(1+2Ψ), the inverse is g^{00} = −1/(1+2Ψ) ≈ −1 + 2Ψ to first
order, so

$$\delta g^{00} = +2\Psi.$$

**The aether piece — here the unit constraint does the work.** The aether is *defined* to be
unit-timelike: g_{μν}A^μA^ν = −1, at every order. At first order, with the spatial components A^i
being themselves first-order (so A^iA^j is second-order and drops out), the constraint reads

$$g_{00}(A^0)^2 = -1 \;\Rightarrow\; -(1+2\Psi)(A^0)^2 = -1 \;\Rightarrow\; (A^0)^2 = \frac{1}{1+2\Psi} \approx 1-2\Psi,$$

hence A^0 = 1 − Ψ and

$$\delta A^0 = -\Psi.$$

The aether is **not free** to perturb its time component however it likes — the unit constraint
ties it rigidly to the metric potential Ψ. Putting the two pieces together,

$$\boxed{\;\delta q^{00} = \delta g^{00} + 2A^0\,\delta A^0 = (+2\Psi) + 2(1)(-\Psi) = 2\Psi - 2\Psi = 0.\;}$$

The metric perturbation and the constraint-forced aether perturbation **cancel exactly.** This is
the central identity. It is not an approximation or a tuning — it follows directly from the
definition A^μA_μ = −1. (We verified it symbolically; see `reviews/redteam_the_puzzle.py`.)

With δq^{00} = 0, piece (A) vanishes, so δ𝒴 = 0 **robustly** — including the term the simple
argument missed. Therefore

$$\mathcal Y = O(\delta\phi^2),\qquad \mathcal Y^{3/2} = O(\delta\phi^3).$$

The a₀-bearing term is genuinely **third order** in the perturbations.

---

## 5. The consequence — the linear CMB is untouched

A term that is O(δφ³) in the action contributes to the equations of motion only at O(δφ²) and
higher — i.e. at *second* order and beyond. It makes **no contribution to the linear (first-order)
equations of motion.** Those are governed instead by the analytic kinetic term −(2−K_B)𝒴 (which is
O(δφ²), with an a₀-*free* coefficient) and by the cosmological function 𝒦(𝒬) (the dust mode and Λ,
also a₀-free). Therefore

> **a₀ → a₀(z) leaves the linear CMB spectrum C_ℓ and the linear matter power spectrum P(k)
> exactly invariant.**

The running of a₀ is invisible to linear cosmology. We confirmed this by directly integrating the
linear Einstein–Boltzmann system: toggling the running a₀ shifts the linear transfer function by
*zero*, and the background acoustic physics comes out right — sound horizon r_s = 144.3 Mpc
(Planck: 144.4) and acoustic scale ℓ_A = 301.7 (Planck: ≈ 301). (See `bridge1_linear_boltzmann.py`.)

Physically: the acoustic peaks are made by *linear* density waves (the perturbations at
recombination are ~1 part in 10⁵). a₀ — no matter how large its background value — only acts on
the *cubic* part of the dynamics, which is utterly negligible at that amplitude. The bigness of a₀
at recombination is irrelevant *because the relevant physics is linear and a₀ is not.*

---

## 6. Scope — what the theorem does and does not cover

The theorem is about *linear* order. It is exact there. Two honest caveats:

1. **Second order is open.** a₀ first acts at O(δφ³) in the action, i.e. second order in the
   equations of motion. At recombination a₀ is ~2×10⁴ larger, and CMB scales sit in the
   deep-MOND corner (g_bar/a₀ ~ 10⁻³), where the non-analytic 𝒴^{3/2} term makes a naive estimate
   soft. A scaling estimate puts the second-order fractional correction to C_ℓ at ~0.01–0.1% —
   likely below Planck's ~0.3–1% near the third peak, but *not provably so*. A full second-order
   Boltzmann calculation (a CLASS/hi_class patch) is required to settle it. (See
   `reviews/nonlinear_cmb_scoping.py`.)
2. **The result is inherited-and-protected, not predicted-from-scratch.** AeST fits the CMB only
   because its 𝒦(𝒬) sector was constructed to mimic cold dark matter. The δq⁰⁰ = 0 theorem proves
   the running a₀ *does not disturb* that fit at linear order — it protects an existing success
   rather than generating a new one. That is still a non-trivial and necessary result, but it
   should be stated honestly.

---

## 7. Conclusion

The central concern about an evolving MOND scale — that a₀ being ~20,000× larger at recombination
would distort the cosmic microwave background — is answered cleanly at linear order. The
acceleration constant couples only to the cubic 𝒴^{3/2} term, and the one term that could have
spoiled this argument vanishes because the aether's unit-timelike constraint forces δq⁰⁰ = +2Ψ −
2Ψ = 0 exactly. Consequently the running of a₀ leaves the linear CMB and matter power spectrum
untouched, as we confirm numerically. The identity δq⁰⁰ = 0 is the technical heart of the result:
a one-line cancellation, forced by the structure of the theory, that makes a cosmologically
evolving galaxy-dynamics scale compatible with the most precise data in cosmology — at linear
order. The second-order effect, estimated to be small, is the honest remaining frontier.

---

### References
- Skordis, C. & Złošnik, T. 2021, Phys. Rev. Lett. 127, 161302; arXiv:2007.00082 (AeST; CMB fit).
- Ma, C.-P. & Bertschinger, E. 1995, ApJ 455, 7 (linear Einstein–Boltzmann equations).
- Planck Collaboration 2018, A&A 641, A6 (CMB parameters; r_s, ℓ_A).
- Milgrom, M. 2014; Skordis & Złošnik 2021 (the evolving-a₀ idea and its host; see Paper I).

*Reproducibility:* `reviews/redteam_the_puzzle.py` (the δq⁰⁰ = 0 computation),
`bridge1_linear_boltzmann.py` (the linear spectra; running-a₀ effect = 0),
`reviews/nonlinear_cmb_scoping.py` (the open second-order estimate). Companion: **Paper I** (the
explicit θ-coupled construction).
