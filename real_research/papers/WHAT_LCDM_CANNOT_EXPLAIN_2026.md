# What ΛCDM Cannot Explain: The Radial-Acceleration Relation and the Mounting Empirical Tensions of the Concordance Model

**Carl P. Zimmerman** · Briar Creek Tech · 2026-06-28

## Abstract

ΛCDM is the standard model of cosmology, and on the largest scales it is a quantitative triumph: the cosmic-microwave-background acoustic peaks, big-bang nucleosynthesis, the growth of large-scale structure, and cluster lensing are all reproduced with a handful of parameters. This essay is not a denial of that record. It is an accounting of the bill the model has **not** paid — and of one law in particular, the radial-acceleration relation (RAR), that it cannot reproduce without a fine-tuned conspiracy. Galaxies obey a tight, one-parameter relation between their observed and baryonic accelerations, with intrinsic scatter consistent with zero, anchored at a fixed acceleration **a₀ ≈ 1.2×10⁻¹⁰ m s⁻²** that happens to equal *cH₀* to a factor of order unity and *c²√(Λ/32π)* on the nose. MOND **predicted** this law in 1983; ΛCDM must **assemble** it, after the fact, from stochastic halo formation and baryonic feedback that have no a-priori reason to be tight. Set alongside the four-decade null on the dark-matter particle and the precision-cosmology tensions — the ~5σ Hubble discrepancy, the DESI preference for *w ≠ −1*, and the ~5σ cosmic radio dipole — the galaxy-scale regularities are not loose ends. They are the fingerprint of physics the concordance model is missing. ΛCDM is not falsified. It is a framework carrying a large and growing empirical debt, and the debt is concentrated exactly where it is least able to pay: at a fixed acceleration scale that knows about the cosmos.

## 1. Where the model works — and where it stops being predictive

Every headline success of ΛCDM is a **large-scale, linear, statistical** success. The CMB power spectrum is linear perturbation theory on a smooth background. Nucleosynthesis is equilibrium nuclear physics in the first three minutes. The matter power spectrum and cluster abundances are statistical properties of a Gaussian random field. In all of these, dark matter is a smooth, pressureless fluid, and the theory is genuinely predictive.

Descend to the scale of an individual galaxy — nonlinear, baryon-dominated in the center, dark-matter-dominated in the outskirts — and the predictiveness evaporates. Halo concentration, formation history, angular-momentum content, and the strength and timing of baryonic feedback are all stochastic, and all are **tuned, galaxy by galaxy, to fit the rotation curve after it is measured.** This is the regime where the concordance model stops forecasting and starts curve-fitting, and it is exactly the regime where the data are the most regular.

## 2. The radial-acceleration relation: the law that requires a conspiracy

In 153 disk galaxies spanning five decades in mass and every morphology, with 2,700 independent resolved measurements, McGaugh, Lelli & Schombert (2016) and Lelli et al. (2017) found that the observed centripetal acceleration is a **single, tight function of the acceleration expected from the visible baryons alone:**

> g_obs = g_bar / [1 − exp(−√(g_bar/a₀))],  a₀ ≈ 1.2×10⁻¹⁰ m s⁻².

The total scatter is **0.13 dex**, and the per-point observational error budget (distance, inclination, mass-to-light) is **≈0.12 dex** — leaving **intrinsic scatter consistent with zero.** (Reproduced on the framework's own footing in `reviews/rar_framework_a0_mlfit.py`: 0.108 dex at a single Υ⋆ = 0.70, *tighter* than regular MOND.)

Here is the problem, stated without spin. In ΛCDM, dark matter **dominates** the dynamics — yet the relation is set **entirely by the baryons**, which do not. For the curve to be this tight, the dark halo's contribution at every radius must be a fixed, deterministic function of the *baryonic* acceleration there — across galaxies with wildly different formation histories, halo masses, and feedback. There is no dynamical reason in the theory for that conspiracy. Stochastic ingredients should produce stochastic scatter; the data show none. And the relation locks onto **one** acceleration, a₀, the same in a dwarf and a giant.

MOND wrote this law down in 1983, before the data existed. ΛCDM can be **tuned** to approximate it — Di Cintio & Lelli (2016), Keller & Wadsley (2017), and Navarro et al. (2017) reproduce its rough shape in simulations with carefully calibrated feedback — but the tightness, the zero intrinsic scatter, and the low-acceleration tail remain a struggle, and the result is a postdiction tuned to the answer. **The RAR is a prediction of modified dynamics and a retrofit of dark matter.** That asymmetry is the single most important fact in galaxy-scale cosmology, and it is routinely under-weighted.

## 3. An acceleration scale that knows about the cosmological constant

The scale a₀ is not arbitrary. Numerically,

> a₀ ≈ 1.2×10⁻¹⁰ m s⁻² ≈ cH₀/2π ≈ c²√(Λ/32π).

A scale that governs the internal dynamics of galaxies equals, to a factor of order unity, a scale built from the Hubble rate and the cosmological constant. ΛCDM has **no explanation** for this; Famaey & McGaugh (2012) concede as much in print. Why should the rotation of a galaxy "know" the dark-energy density of the universe? In the concordance model it is a coincidence to be noted and set aside. In any theory where inertia or gravity is referred to the cosmic horizon, it is **required** — which is the entire content of the reframing a₀ = cH_Λ/Z, offered here not as a finished theory but as the natural reading of a coincidence the standard model cannot absorb.

## 4. The baryonic Tully–Fisher relation

The same pattern repeats. The baryonic mass of a galaxy scales as the **fourth power** of its flat rotation velocity, M_bar ∝ V⁴, with a slope indistinguishable from exactly 4 and scatter smaller than halo abundance-matching naturally produces (McGaugh 2012; Lelli et al. 2019). Slope-4 is a MOND prediction. In ΛCDM the slope and normalization emerge from a balance of halo mass, baryon fraction, and feedback that, again, has no reason to land on the MOND value with so little scatter. A second predicted-then-retrofitted regularity.

## 5. The particle that was never there

Cold dark matter is, definitionally, a particle — and after four decades, it has never been detected. The best-motivated candidate, the weakly-interacting massive particle, has had its natural parameter space **excluded down toward the irreducible neutrino floor** by LZ and XENONnT. The QCD axion remains unseen. The sterile-neutrino "3.5 keV line" faded under scrutiny. None of this falsifies dark matter — a particle can always be made more weakly coupled — but it removes the load-bearing promissory note, *"we will find it soon,"* that justified treating the model's central entity as established. Twenty-seven percent of the universe remains an inference, not an observation.

## 6. The model is being pulled at several seams at once

Galaxy scales are not the only front.

- **The Hubble tension (~5σ):** the locally-measured expansion rate (SH0ES) and the CMB-inferred rate (Planck) disagree at a significance that a decade of work has sharpened, not dissolved.
- **DESI and w ≠ −1 (2.8–4.2σ):** the 2024–2025 baryon-acoustic-oscillation data, combined with supernovae, prefer evolving dark energy over a cosmological constant. The *Λ* in ΛCDM is the piece the newest precision data is actively cracking.
- **The cosmic dipole (~5σ):** the dipole in the distribution of distant radio sources and quasars (Secrest et al. 2021, 2022) is several times larger than the kinematic expectation from the CMB, straining the cosmological principle itself.

Each tension, alone, has a candidate systematic or an absorbing parameter. But a theory simultaneously in multi-sigma tension on H₀, on the equation of state of dark energy, and on the cosmological principle, *while* requiring a stochastic conspiracy to fit the tightest law in galaxy dynamics, *while* never having detected its central particle, is not a theory with loose ends. It is a theory under load.

## 7. What this is — and what it is not

It is not a falsification. ΛCDM has **zero clean, referee-proof kills**: every tension above admits a proposed systematic, a freed parameter, or a feedback prescription, and intellectual honesty requires saying so plainly. The bullet cluster, the third acoustic peak, and weak lensing remain real successes that a pure modified-dynamics theory must still answer for, and currently cannot fully. This essay does not claim that dark matter is dead, nor that any single alternative is established.

What it claims is narrower and harder to dismiss: that ΛCDM's empirical debt is **real, multi-front, and growing**, and that the galaxy-scale regularities — the RAR above all — are not noise to be averaged away but a **signal**, pointing at a fixed acceleration scale set by the cosmological constant. That is the one thing the concordance model cannot explain without conspiracy, and it is the one thing a vacuum-set a₀ explains for free. A model is in trouble not when it is refuted, but when its successes are increasingly *fits* and its competitor's are increasingly *predictions*. On galaxy scales, that is now the situation — and it has been, quietly, for thirty years.

## References (representative, real)
- S. McGaugh, F. Lelli, J. Schombert, *Radial Acceleration Relation in Rotationally Supported Galaxies*, Phys. Rev. Lett. 117 (2016) 201101.
- F. Lelli, S. McGaugh, J. Schombert, M. Pawlowski, *One Law to Rule Them All: The RAR in Disk Galaxies*, ApJ 836 (2017) 152.
- B. Famaey, S. McGaugh, *Modified Newtonian Dynamics (MOND): Observational Phenomenology and Relativistic Extensions*, Living Rev. Relativity 15 (2012) 10.
- S. McGaugh, *The Baryonic Tully–Fisher Relation of Gas-Rich Galaxies*, AJ 143 (2012) 40.
- A. Di Cintio, F. Lelli, *The mass discrepancy acceleration relation in a ΛCDM context*, MNRAS 456 (2016) L127; B. Keller, J. Wadsley, ApJL 835 (2017) L17; J. Navarro et al., MNRAS 471 (2017) 1841 (ΛCDM attempts at the RAR).
- A. Riess et al., *A Comprehensive Measurement of the Local Value of H₀* (SH0ES), ApJL 934 (2022) L7.
- DESI Collaboration, *DR1 (2024, arXiv:2404.03002)* and *DR2 (2025, arXiv:2503.14738)* cosmological constraints (w₀wₐ preference).
- N. Secrest et al., *A Test of the Cosmological Principle with Quasars*, ApJL 908 (2021) L51; MNRAS (2022).
- LZ Collaboration, *Dark Matter Search Results* (2024) and XENONnT (2023) — WIMP exclusion toward the neutrino floor.

*Honest scope: a critique of where ΛCDM is empirically strained, not a claim that it is falsified or that an alternative is established. RAR scatter reproduced in `reviews/rar_framework_a0_mlfit.py`; a₀ = c²√(Λ/32π) = cH_Λ/Z with Z = √(32π/3) ≈ 5.79. The author retracted all earlier "theory of everything" claims (2026-06-23); this essay makes none.*
