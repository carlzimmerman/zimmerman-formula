# An explicit AeST realization of an evolving MOND scale, and its linear CMB-safety

**Carl Zimmerman** · June 2026 · *draft technical note · all results reproducible from the
cited scripts in this repository*

---

## Abstract

Milgrom (2014) suggested that the MOND acceleration scale a₀ may decrease with cosmic time,
tracking cH(z). We give an explicit covariant realization within the Aether-Scalar-Tensor theory
(AeST; Skordis & Złošnik 2021) by promoting the constant a₀ in the spatial sector to a function of
the aether expansion,

> **a₀ → a₀(θ) = cθ/(3Z),  θ ≡ ∇_μ A^μ,  Z = 2√(8π/3).**

On a Friedmann–Robertson–Walker background θ = 3H exactly, so a₀(z) = cH(z)/Z follows as a field
equation rather than an imposed relation. Our **main result** is that this running is invisible to
*linear* cosmology: a₀ enters the action only at O(δφ³), and the relevant metric/aether projection
δq⁰⁰ vanishes identically once the unit-timelike constraint is imposed — so the linear CMB and
matter power spectrum are **unchanged** from constant-a₀ AeST. We confirm the sound horizon and
acoustic scale numerically. We do **not** derive the coefficient Z; the second-order CMB effect is
left open; and we stress that the observable apparent-a₀ evolution is **degenerate with ΛCDM** halo
evolution out to z ≈ 2.3 (Magneticum simulations). The single regime in which the proposal is
distinguishable — high-z, *extended* (deep-MOND) galaxies — has not yet been observed.

## 1. What is, and is not, new

The relation a₀ ≈ cH₀ is a long-standing numerical coincidence (Milgrom 1983), and the idea that
a₀ might **evolve** as cH(z) is Milgrom's own (2014, Phys. Rev. D). The relativistic host theory,
and its property of fitting the CMB with c_GW = c, are Skordis & Złošnik's (2021). **This note
contributes only:** (i) an explicit, minimal covariant *implementation* of the evolving scale
inside AeST — coupling a₀ to the aether expansion θ rather than introducing a new field; and (ii)
the proof that this implementation leaves the linear CMB exactly invariant, including a term the
standard order-counting omits. It is an implementation-and-consistency result, not a new physical
principle, and the coefficient Z = 2√(8π/3) is a chosen O(1) number (it is not unique; e.g. 29/5
fits the present value marginally better), distinct from Milgrom's 2π only at the ~9% level.

## 2. The coupling and its two limits

The AeST action (Skordis–Złošnik Eq. 5) carries a metric, a unit-timelike aether A_μ (A^μA_μ = −1),
and a scalar φ, with a₀ appearing as the coefficient of the spatial 𝒴^{3/2} term of the free
function, 𝒴 = q^{μν}∇_μφ∇_νφ, q_{μν} = g_{μν} + A_μA_ν. We replace the constant a₀ by a₀(θ) = cθ/(3Z).

- **Background (FRW).** With A^μ aligned to cosmic time, θ = (1/√−g)∂_t(√−g A⁰) = 3ȧ/a = 3H
  exactly. Hence a₀(z) = cH(z)/Z = a₀(0)E(z), E(z) = √(Ω_m(1+z)³ + Ω_Λ).
- **Quasi-static galaxy.** To first order in the weak field, θ = 3H − 3HΨ − 3Φ̇ + ∇·B, with the
  3H carried by the *background* expansion. The corrections are negligible in a virialized system
  (Ψ ~ 10⁻⁶, Φ̇ ≈ 0, ∇·B ≈ 0), so a galaxy at epoch z sees a₀ ≈ cH(z)/Z to ~1 part in 10⁶,
  recovering Bekenstein–Milgrom dynamics with the epoch-appropriate scale. *(Verified in
  `reviews/theta_3H_coupling.py`.)*

## 3. Linear CMB-safety (main result)

On FRW the scalar gradient is purely temporal, so the spatial projector annihilates it: q̄⁰⁰ =
g⁰⁰ + A⁰A⁰ = −1 + 1 = 0, giving 𝒴̄ = 0 and δ𝒴 = 0 at linear order. The a₀-bearing term 𝒴^{3/2} is
therefore O(δφ³): absent from the linear equations of motion. The θ-dressing multiplies it by
1/θ with θ̄ = 3H̄ ≠ 0, which does not lower the order.

The non-trivial step the usual order-counting omits is the contribution δq^{μν}∇_μφ̄∇_νφ̄ to δ𝒴.
The only surviving piece is δq⁰⁰(φ̄')². Imposing the unit-timelike constraint to first order gives
δA⁰ = −Ψ, hence

> **δq⁰⁰ = δg⁰⁰ + 2A⁰δA⁰ = (+2Ψ) + (−2Ψ) = 0** (exactly).

So δ𝒴 = 0 even with the aether perturbed: the running a₀ is invisible to the linear CMB and P(k)
for the *same* reason constant-a₀ AeST is. We confirm numerically that the sound horizon
(r_s = 144.3 Mpc vs Planck 144.4) and acoustic scale (ℓ_A = 301.7 vs ~301) are unchanged, and that
toggling the running shifts the linear transfer function by 0. *(Verified in
`reviews/redteam_the_puzzle.py` and `bridge1_linear_boltzmann.py`.)*

## 4. What this does not establish

- **The coefficient Z is not derived.** It is a free coupling; the present note fixes nothing about
  the factor of 2 beyond Milgrom's coincidence.
- **The second-order CMB is open.** a₀ first acts at O(δφ³); at recombination a₀ is ~2×10⁴ larger
  and the acoustic scales sit in the deep-MOND (𝒴→0) corner where the 𝒴^{3/2} non-analyticity makes
  the second-order estimate (~0.01–0.1%) soft. A full second-order Boltzmann treatment is required.
- **The galaxy result is leading-order** (test-field aether); the full back-reaction is unworked.
- **The dynamical predictions are deep-MOND** (g_bar < a₀). High-z galaxies are compact, with
  g/a₀ ∝ (1+z)^{1/2} rising toward the Newtonian regime, so the a₀(z) boosts are suppressed for
  compact, massive targets and apply to extended ones.

## 5. The one distinguishing test

The proposal's observable — an apparent a₀ rising with z — is **degenerate with ΛCDM**: hydro
simulations (Magneticum; Tian et al. 2022) reproduce a ×3 rise by z = 2.3 with no fundamental
evolution, matching E(2.3) = 3.46. The degeneracy is therefore not broken by current data. It may
break at **z ≳ 4 on extended (deep-MOND) galaxies**, a regime ΛCDM apparent-a₀ studies have not yet
mapped, where the evolving-a₀ prediction (M_dyn/M⋆ ∝ √E, v & σ ∝ E^{1/4}, BTFR zero-point ∝ −log E,
all keyed off one E(z)) can be compared channel-by-channel. The decisive measurement is whether
those channels move **coherently** with a single E(z) there. Until then the proposal is a
consistent, falsifiable hypothesis without distinguishing evidence.

---

## References

- Milgrom, M. 1983, ApJ 270, 365 (MOND; a₀ ≈ cH₀).
- Milgrom, M. 2014, Phys. Rev. D, arXiv:1412.4344 (cosmological variation of a₀ ∝ cH).
- Skordis, C. & Złošnik, T. 2021, Phys. Rev. Lett. 127, 161302, arXiv:2007.00082 (AeST).
- Tian, Y. et al. 2022, MNRAS, arXiv:2206.04333 (apparent a₀ evolution in ΛCDM; Magneticum).
- McGaugh, Lelli & Schombert 2016, PRL 117, 201101 (SPARC RAR).
- MUSE-DARK III 2026, A&A (intermediate-z RAR / a₀ at z ≈ 0.9).

*Reproducibility:* `reviews/theta_3H_coupling.py` (the coupling and its limits),
`reviews/redteam_the_puzzle.py` (δq⁰⁰ = 0), `bridge1_linear_boltzmann.py` (r_s, ℓ_A),
`reviews/nonlinear_cmb_scoping.py` (the open second-order check),
`reviews/NOVELTY_AND_DEGENERACY.md` (precedents and the ΛCDM degeneracy).
