# A Growing Neutrino Mass from an Evolving MOND Scale: A de Sitter–Unruh Reading of the DESI Σmν Anomaly

**Carl P. Zimmerman** · Briar Creek Tech · 2026-06-27

## Abstract

The de Sitter–Unruh modified-inertia proposal sets the MOND acceleration scale by the dark-energy density, **a₀ = cH_Λ/Z = (c/2)√(Gρ_DE) = c²√(Λ/32π) ≈ 9.36×10⁻¹¹ m s⁻²** (Z = √(32π/3) ≈ 5.789), so that a₀ *evolves* with redshift as **a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0))** on the DESI-preferred evolving-dark-energy branch. This note draws one consequence and confronts it with a live anomaly. Evolving dark energy implies a rolling quintessence field; the swampland Distance Conjecture then predicts a tower of states whose mass tracks that field. The framework's vacuum scale **E_dS = ρ_DE^(1/4) ≈ 2.24 meV** sits, uniquely among Standard-Model scales, *within one order of magnitude* of the neutrino mass scale (the electron is 10⁸, atomic-MOND accelerations 10³³, away) — so the neutrino is the one place the framework's de Sitter vacuum and a particle scale meet. **If the lightest neutrino is the lightest tower state, its mass grows from past to present, locked to a₀(z) with no free amplitude:** propagating the public DESI w₀wₐ posterior gives **m_ν(z=3)/m_ν(0) ≈ 0.59–0.75**, and a mass that *freezes by recombination*. The testable consequence is sharp: the CMB imprints a neutrino **28–46% lighter** than today's, so a constant-mass fit to CMB+BAO *under-counts* the late-time mass — yielding an inferred **Σm_ν^eff ≈ 0.032–0.042 eV** when the true present-day value sits at the normal-ordering oscillation floor (0.059 eV). This is the right sign and the right rough magnitude to be the **DESI "negative effective neutrino mass" anomaly**. We state the limits plainly: nothing here *derives* m_ν (the absolute scale is free; the meV match is generic to any ρ_cosmic^(1/4)); the signature is partly *degenerate* with the standard "dynamical dark energy mimics negative mass" reading; the framework-distinctive content is the **lock** of the mass evolution to ρ_DE^(1/2), testable only by a joint CMB-vs-late-time Σm_ν fit constrained by a₀(z). This is a prediction about the **neutrino/dark sector only — not a theory of everything.** It is decided by the same DESI w(z) gate as the a₀(z) prediction, sharpened by CMB-S4 + DESI-DR3/Euclid growth (≈2027–2030), and it *dies if* DESI converges to w = −1. All numbers are reproducible from the public repository.

This note supplements the author's published one-parameter de Sitter–Unruh papers and does not restate or strengthen any claim about deriving the Standard Model.

---

## 1. What is claimed, and what is not

| Statement | Status |
|---|---|
| a₀ = cH_Λ/Z, evolving as a₀(z) ∝ √ρ_DE(z) | **Prior result** (the framework; DESI-hostage, marginal) |
| E_dS = ρ_DE^(1/4) ≈ 2.24 meV is ~1 order from the neutrino scale | **Computed fact** (the scale gap closes *only* for ν) |
| The framework *derives* m_ν, or any mass | **No — disavowed.** Absolute scale free; meV match generic to ρ_cosmic^(1/4) |
| *If* the lightest ν is a tower state, m_ν(z) is *forced in the ratio* by a₀(z) | **Conditional** (on the Distance Conjecture α≈λ and ν = tower state) |
| m_ν grows from CMB to today by ~28–46%, an inferred Σ^eff below the floor | **Computed** from the real DESI posterior |
| This is *the* explanation of the DESI Σm_ν anomaly | **No — a candidate, right-signed, partly degenerate** |
| A theory of everything / the Standard Model | **Not claimed. Disavowed.** |

The contribution is item 5 read against item 6: a **physical, falsifiable, right-signed reading** of a live anomaly, honestly scoped.

## 2. The evolving acceleration scale and the rolling field

In the de Sitter–Unruh picture a body's inertia is its response to the cosmic-horizon bath, fixing a₀ = (c/2)√(Gρ_DE) (Milgrom 1999; Deser–Levin 1997 for the temperature). The only falsifiable content is the **ratio**

> **a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)),** (1)

in which the undetermined O(1) coefficient cancels. On the DESI w₀wₐCDM branch, ρ_DE(z) = ρ_DE(0)·(1+z)^{3(1+w₀+wₐ)} e^{−3wₐz/(1+z)}, so evolving dark energy ⇒ a rolling scalar φ(z) with field excursion (canonical normalization)

> **Δφ(z)/M_Pl = ∫₀^z √(3|1+w| Ω_DE) d ln(1+z′).** (2)

Propagating the public DESI DR1 posterior (`a0z_desi_chains_propagation.py`) gives Δφ(z=3)/M_Pl ≈ 0.40–0.51 and a slope λ(0) = √(3(1+w₀)) ≈ 0.72–1.04 that **saturates the de Sitter swampland bound** c ≈ √(2/3) ≈ 0.82 — the field sits at the swampland edge.

## 3. The neutrino is where the scale gap closes

The framework's vacuum scale is E_dS = ρ_DE^(1/4) = **2.243 meV** (verified; the standard dark-energy scale). Its ratio to Standard-Model scales (`nu_de_coincidence.py`):

| scale | ratio E_dS / m | gap |
|---|---|---|
| solar splitting √Δm²₂₁ = 8.66 meV | 0.26 | **same order** |
| atmospheric √Δm²₃₁ = 50 meV | 0.045 | ~1 order |
| electron 0.511 MeV | 4.4×10⁻⁹ | ~10⁸ |
| atomic-electron MOND a₀/g | 10⁻³³ | ~10³³ |

The 8-to-33-order gap that walls off every other Standard-Model particle **closes to ~1 order only for the neutrino.** E_dS lies inside the oscillation window [8.6, 50] meV and *on* the published swampland bound m_ν ≲ Λ^(1/4) (Gonzalo, Ibáñez & Valenzuela 2021; the dark-dimension tower, Montero–Vafa–Valenzuela 2022, whose authors note it "may connect to neutrinos"). **This is a coincidence/inequality, not a derivation** — any cosmic density to the ¼ power lands near 2 meV.

## 4. A growing neutrino mass, locked to a₀(z)

If the lightest neutrino is the lightest tower state, the Distance Conjecture gives m_ν(z)/m_ν(0) = exp(−α Δφ(z)/M_Pl), with α≈λ the tower-potential coefficient. The **amplitude is not free in the ratio** — Δφ is fixed by the measured w(z). On the real DESI posterior (`nu_de_tower.py`, `dm_varying_mass.py`):

> **m_ν(z=3)/m_ν(0) = 0.59 (Union3) / 0.66 (DESY5) / 0.75 (Pantheon+)** — a **25–41% rise** from z=3 to today.

The sign is *growing* (lighter past, heavier today, MaVaN-class; Fardon, Nelson & Weiner 2004). Because Ω_DE → 0 by z ≈ 10, **Δφ plateaus and the mass freezes** through recombination — a today-versus-early *offset*, not a fast late drift, so it evades the tight early-time interacting-dark-energy bounds.

## 5. The sharp consequence: a reading of the DESI Σmν anomaly

DESI's cosmological fits prefer Σm_ν *below* the normal-ordering oscillation floor (0.059 eV) — formally a "negative effective mass" in ΛCDM. The framework's frozen offset gives this a physical cause (`nu_mass_cmb_vs_today_offset.py`):

> The CMB (z ≈ 1100) imprints the *frozen-early* mass, **m_ν(CMB)/m_ν(today) ≈ 0.54–0.72** — a **28–46% lighter** neutrino. A constant-mass CMB+BAO fit therefore *under-counts* the late-time mass: with the true present value at the floor (0.059 eV), the inferred **Σm_ν^eff ≈ 0.032–0.042 eV**, squarely in the DESI low/negative band.

**Right sign, right rough magnitude, no new free knob** — the offset is fixed by the measured w(z); only α≈λ is assumed. The framework's *growing neutrino mass* is a candidate physical reading of the DESI anomaly, from the same a₀(z)=√ρ_DE engine.

## 6. Limits, stated plainly

1. **No derivation.** The absolute m_ν is free; E_dS *restates* ρ_DE; the ~2 meV match is generic to ρ_cosmic^(1/4), not ρ_DE-specific.
2. **Partial degeneracy.** The signature overlaps the mainstream "dynamical DE mimics negative m_ν" reading, because Δφ is sourced by the same w(z). The **distinctive** content is the *lock* — the mass evolution tied to ρ_DE^(1/2) — visible only in a joint fit.
3. **Conditional** on α≈λ (a swampland conjecture, not a theorem) and on the lightest ν being a tower state.
4. **Neutrino/dark sector only — not a theory of everything.** The charged-lepton and quark masses remain untouched and walled.
5. **Falsifier:** it **dies if DESI converges to w = −1** (no roll → no tower → no mass evolution).

## 7. The decisive test

A **CMB-versus-late-time Σm_ν split that tracks ρ_DE^(1/2)** — i.e. a CMB-inferred mass below the growth/lensing-inferred mass, with the offset *locked* to the same a₀(z)/w(z) the framework fits elsewhere. Reachable by **CMB-S4 + DESI-DR3/Euclid** weak-lensing-growth tomography, ≈2027–2030. Direct kinematic (KATRIN/Project-8) and 0νββ probes are too insensitive this decade (predicted m_β ≈ 9 meV) and are not the falsifiers.

## 8. Conclusion

The same evolving a₀(z) that the framework already predicts forces, *if the neutrino is a tower state*, a **growing neutrino mass** that offers a right-signed, right-magnitude, physical reading of the live DESI Σm_ν anomaly — the one place the de Sitter vacuum and a Standard-Model particle meet without a 30-order scale gap. It is conditional, partly degenerate, and emphatically **not** a theory of everything; but it is falsifiable on a near-term clock by the same w(z) gate as a₀(z) itself.

## Acknowledgements and provenance
The de Sitter–Unruh modified-inertia route is Milgrom (1999); the temperature structure Deser–Levin (1997). The swampland Distance Conjecture is Ooguri–Vafa; the m_ν ≲ Λ^(1/4) bound and dark-dimension tower Gonzalo–Ibáñez–Valenzuela (2021) and Montero–Vafa–Valenzuela (2022); mass-varying neutrinos Fardon–Nelson–Weiner (2004). DESI Σm_ν results and the "negative effective mass" preference are from the DESI DR1/DR2 cosmology analyses. All magnitudes are reproducible: `reviews/{swampland_tower_from_a0z, nu_de_coincidence, nu_de_tower, dm_varying_mass, nu_mass_cmb_vs_today_offset}.py` and `reviews/a0z_desi_chains_propagation.py`, on the public DESI chains. This note claims a conditional, falsifiable reading of one anomaly — not a derivation and not a theory of everything.

## Selected references
- M. Milgrom, *The modified dynamics as a vacuum effect*, Phys. Lett. A 253 (1999) 273.
- S. Deser, O. Levin, *Accelerated detectors … (anti-)de Sitter spaces*, Class. Quantum Grav. 14 (1997) L163.
- H. Ooguri, C. Vafa, *On the geometry of the string landscape and the swampland*, Nucl. Phys. B 766 (2007) 21.
- E. Gonzalo, L. Ibáñez, I. Valenzuela, *Swampland constraints on neutrino masses*, JHEP (2022) [arXiv:2109.10961].
- M. Montero, C. Vafa, I. Valenzuela, *The dark dimension and the swampland*, JHEP (2023) [arXiv:2205.12293].
- R. Fardon, A. Nelson, N. Weiner, *Dark energy from mass varying neutrinos*, JCAP (2004) [astro-ph/0309800].
- DESI Collaboration, *DR1/DR2 cosmological constraints* (2024–2025), incl. the Σm_ν preference below the oscillation floor.
