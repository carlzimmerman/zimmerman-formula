# Separating a Growing Neutrino Mass from Dynamical Dark Energy: the Scale-Dependent Growth Signature of an Evolving MOND Scale

**Carl P. Zimmerman** · Briar Creek Tech · 2026-06-28
**A companion/forecast note to "A Growing Neutrino Mass from an Evolving MOND Scale" (DOI [10.5281/zenodo.20977421](https://doi.org/10.5281/zenodo.20977421)).**

## Abstract

The de Sitter–Unruh modified-inertia proposal sets the MOND acceleration scale by the dark-energy density, **a₀ = cH_Λ/Z = (c/2)√(Gρ_DE) ≈ 9.36×10⁻¹¹ m s⁻²**, so a₀ evolves as **a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0))** on the DESI-preferred evolving-dark-energy branch. The companion note showed that *if* the lightest neutrino is a swampland-tower state, its mass is then **locked to a₀(z) with no free amplitude**, freezing by recombination so that the CMB imprints a ~25–45% lighter neutrino than today's — a right-signed, right-magnitude reading of the DESI "negative effective neutrino mass" anomaly. The honest objection that note left open is **degeneracy**: a constant neutrino mass with *generic* dynamical dark energy also pushes the inferred Σm_ν below the oscillation floor. Here we identify and quantify the one observable that breaks the degeneracy. A *growing* neutrino mass changes the free-streaming fraction f_ν(z), suppressing structure growth **only below the neutrino free-streaming scale k_fs(z)** — a **scale-dependent** step in the matter power spectrum. Dynamical dark energy changes the expansion H(z) and is **scale-independent**. The scale-dependence is therefore a separator no equation-of-state mirage can reproduce. A real CAMB calculation confirms the step (≈0.65% at the normal-ordering floor, ≈1.4% at Σ=0.10 eV), and a focused Euclid Fisher gives a detectability of **≈1.4σ at the floor rising to ≈3.9σ at Σ=0.10 eV** — i.e. the test's power is **hostage to the absolute neutrino mass**, which JUNO and KATRIN pin independently this decade. The prediction is **robust to the DESI DR1→DR2 update** (the locked mass ratio moves by <0.05). It remains **conditional** (on α≈λ and ν=tower), **founded-not-derived** (the absolute mass is free), and **dies if w→−1**. It is **not** a theory of everything.

## 1. The claim, and the degeneracy it must beat

The companion note's content reduces to one falsifiable statement: the same evolving a₀(z)=√ρ_DE that the framework already predicts forces, *if the neutrino is a tower state*, a neutrino mass that grows from past to present, **locked** to ρ_DE^(1/2) with no free amplitude. Propagating the public DESI DR1 w₀wₐ posterior gives m_ν(CMB)/m_ν(today) ≈ 0.54–0.72; the mass freezes through recombination, so a constant-mass CMB+BAO fit under-counts the late-time mass and infers Σm_ν^eff ≈ 0.032–0.042 eV — in the DESI low/negative band.

The objection: the mainstream reading of the same anomaly is *generic dynamical dark energy* mimicking a low Σm_ν. Both shift the **amplitude** of the inferred mass below the floor. On amplitude alone they are degenerate. A real test must find an observable where the two part ways.

## 2. The degeneracy-break: scale-dependence

They part ways in the **shape**, not the amplitude.

- A **growing neutrino mass** raises f_ν(z) = Ω_ν(z)/Ω_m(z) toward the present. Massive neutrinos free-stream out of potential wells below the free-streaming scale, so they suppress the growth of structure **only for k > k_fs(z)** (k_fs ≈ 0.007–0.016 h Mpc⁻¹ for the masses of interest). The signature is a **scale-dependent step** in P(k): suppressed small-scale power, intact large-scale power.
- **Dynamical dark energy** alters the background expansion H(z), which rescales the growth factor **uniformly in k**. It is **scale-independent**.

Therefore the scale-dependence of the late-time growth deficit is a separator that no w(z) can fake. This is a *qualitative*, physical fork (free-streaming vs background), not a numerical coincidence.

**CAMB confirmation.** Replacing the linear `ΔP/P ≈ −8 f_ν` rule of thumb with real CAMB transfer functions (`reviews/growing_nu_camb_fisher.py`), comparing the present-day power for the true (heavier, today's) mass against the CMB-anchored (lighter) constant-mass fit:

| Σmν today | small-scale (k>0.2) suppression | large-scale (k<0.01) | **scale-dependent step** |
|---|---|---|---|
| 0.059 eV (NO floor) | 1.09% | 0.44% | **0.65%** |
| 0.10 eV (above floor) | 2.00% | 0.61% | **1.39%** |

The step is real and lives at the free-streaming scale — exactly where dynamical dark energy leaves no feature.

## 3. Detectability: hostage to the absolute mass

A focused Euclid Fisher for the **scale-dependent** part of the signal (subtracting its k-mean to marginalize any scale-independent amplitude or dark-energy contribution) gives:

> **≈1.4σ at the normal-ordering floor (Σ=0.059 eV); ≈3.9σ at Σ=0.10 eV.**

The detectability scales with f_ν, i.e. with the **absolute** neutrino mass. This is the actionable result: at the oscillation floor the test is marginal, but even a modestly higher mass makes it a real detection — and the absolute mass is being pinned **independently** by JUNO (first data 2026) and KATRIN this decade. The growth-tomography test does not stand alone; its power is set by a number other experiments are already measuring.

## 4. Robustness to the DESI DR1→DR2 update

The companion note used DESI DR1 (2024). Recomputing the locked mass ratio across both the DR1 best-fits and the published DESI DR2 (2025) central w₀wₐ values (`reviews/growing_nu_dr2_sensitivity.py`):

> m_ν(CMB)/m_ν(today): **DR1 0.56–0.71 → DR2 0.57–0.74** — a shift of <0.05, well inside the supernova-sample spread.

The prediction is robust to the data update; DR2's main effect is to *tighten* the evidence for evolving dark energy (2.8–4.2σ), the condition on which the whole prediction is hostage. (The DR2 cobaya chains were not accessible from our environment; DR2 values are published centrals, to be verified against arXiv:2503.14738.)

## 5. Honest scope

- **Founded-not-derived.** The absolute m_ν is free; the framework forces the *ratio* m_ν(z)/m_ν(0) (via Δφ fixed by the measured w(z)) and the *scale* E_dS = ρ_DE^(1/4) = 2.24 meV — not the mass itself.
- **Conditional** on α≈λ (a swampland conjecture, not a theorem) and on the lightest neutrino being a tower state.
- **Approximate.** The CAMB step uses a two-constant-mass bracket for the true m(z) interpolation (it captures the endpoint signature); the Fisher uses rough single-tracer volume/number-density and does not marginalize galaxy bias or nonlinear scales. A publication-grade forecast needs the full Boltzmann m(z) evolution and a multi-tracer Fisher.
- **Dies if w→−1.** No roll → no field excursion → no mass evolution → no signal (not a falsification, just a null).
- **Neutrino/dark sector only — not a theory of everything.** The charged-lepton and quark masses are untouched and walled.

The contribution of this note is narrow and concrete: it converts the companion paper's qualitative "testable by a joint fit" into a **specific, physical, dark-energy-unfakeable observable** (the free-streaming step) with a **computed detectability** that sharpens with the absolute neutrino mass.

## References
- C. P. Zimmerman, *A Growing Neutrino Mass from an Evolving MOND Scale*, DOI 10.5281/zenodo.20977421 (2026).
- M. Milgrom, *The modified dynamics as a vacuum effect*, Phys. Lett. A 253 (1999) 273.
- J. Lesgourgues, S. Pastor, *Massive neutrinos and cosmology*, Phys. Rept. 429 (2006) 307.
- A. Lewis, A. Challinor, A. Lasenby, *Efficient computation of CMB anisotropies in closed FRW models* (CAMB), ApJ 538 (2000) 473.
- DESI Collaboration, *DESI DR2 Results II: BAO and Cosmological Constraints*, arXiv:2503.14738 (2025).
- R. Fardon, A. Nelson, N. Weiner, *Dark energy from mass varying neutrinos*, JCAP (2004) [astro-ph/0309800].
- E. Gonzalo, L. Ibáñez, I. Valenzuela, *Swampland constraints on neutrino masses*, JHEP (2022) [arXiv:2109.10961].

*Reproducible: `reviews/{growing_nu_fsigma8_forecast, growing_nu_camb_fisher, growing_nu_dr2_sensitivity}.py` (exit 0). Footing a₀ = 9.36×10⁻¹¹ m s⁻², Z = √(32π/3). Companion: DOI 10.5281/zenodo.20977421.*
