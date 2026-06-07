# The Zimmerman Theory of Gravity

### The galaxy acceleration scale is set by the cosmological constant

$$a_0 \;=\; c^2\sqrt{\frac{\Lambda}{32\pi}} \;=\; \frac{c}{2}\sqrt{G\rho_\Lambda} \;=\; \frac{cH_\Lambda}{Z}, \qquad Z=\sqrt{\tfrac{32\pi}{3}}=5.789, \qquad a_0 = 9.36\times10^{-11}\ \mathrm{m\,s^{-2}}$$

[![Paper DOI](https://img.shields.io/badge/Paper-10.5281%2Fzenodo.20576485-blue)](https://doi.org/10.5281/zenodo.20576485)
[![Corpus DOI](https://img.shields.io/badge/Code%20%26%20Data-10.5281%2Fzenodo.20576494-blue)](https://doi.org/10.5281/zenodo.20576494)
[![Paper PDF](https://img.shields.io/badge/PDF-read%20the%20paper-success)](real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.pdf)
[![License](https://img.shields.io/badge/code-AGPL--3.0-lightgrey)](LICENSE)

**Author:** Carl P. Zimmerman (Briar Creek Tech) · **Paper:** [`real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.pdf`](real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.pdf)

---

## The idea

Galaxies rotate too fast for their visible mass below a characteristic acceleration **a₀ ≈ 1.2×10⁻¹⁰ m s⁻²**. That scale famously coincides with *c√Λ* and *cH₀* — a coincidence ΛCDM treats as accidental. This theory takes it literally: **the cosmological constant (the dark‑energy density of the vacuum) sets the acceleration scale of galaxies**, and because dark energy evolves, **a₀ evolves with it** — a declining `a₀(z) ∝ √ρ_DE(z)` that is the theory's one distinctive, falsifiable prediction.

It is an **emergent‑gravity theory of the dark sector** — a theory of gravity, dark matter, and dark energy as facets of one vacuum‑set scale. It is **not** a theory of everything, and it says so plainly.

## What the paper establishes

| | Result |
|---|---|
| 🟢 **The galaxy data** | At this a₀ and a single Υ≈0.70, the Radial Acceleration, Baryonic Tully–Fisher, and deep‑MOND mass‑discrepancy relations **agree to 8%** (RAR scatter 0.108 dex, better than regular MOND). |
| 🟢 **The shape is derived** | `g_obs = √(g_bar² + g_bar·a₀)` is **Milgrom's (1999) de Sitter–Unruh modified inertia**, over‑determined across three routes — not a fitted interpolation. |
| 🟢 **The galaxy sign is forced** | A computed DSSYK matter‑chord kernel puts galaxy‑scale probes at the spectral **center** → MOND enhancement; clusters at the **edge** → MOND fails — *the same kernel predicts the empirical cluster failure.* |
| 🟢 **The value of Λ is welded to a₀** | `a₀` and `ρ_Λ` are the two ends of one Cohen–Kaplan–Nelson UV–IR seesaw: `ρ_obs = (3/8π)M_P²H²` exactly (the meV vacuum scale is the Planck–Hubble geometric mean). |
| 🟢 **A real link to fundamental physics** | The *evolving* dark energy is **string‑swampland‑compatible** precisely where a static‑Λ ΛCDM is swampland‑forbidden. |
| 🎯 **The decisive prediction** | **a₀(z=3) = 0.74 a₀(0)** — a declining acceleration scale, with a +6% bump at z≈0.4. The rising `a₀ ∝ cH` rival is excluded (Δχ²≈49); the ΛCDM‑impossible External Field Effect leans the predicted way. |

## What it is *not* (the honest boundary)

- **Not a theory of everything.** The Standard Model is untouched — and every "geometric formula" for a particle‑physics constant in this repo's history is **retracted numerology** (see [`RETRACTIONS.md`](RETRACTIONS.md)).
- **The O(1) coefficient (32π) is a posit**, not a theorem (it cancels in the falsifiable `a₀(z)`).
- **The covariant, ghost‑free completion is unwritten** — the theory's principal theoretical gap.
- **The evolution is contested.** Current data (MUSE‑DARK III 2026) is in tension and leans unfavorable; the claim is decided by clean halo‑free deep‑MOND kinematics at **z≈3 (ELT‑class, this decade)**.

## 📄 The paper

**The Zimmerman Theory of Gravity** — comprehensive edition, ~9,500 words, 16 sections, 8 figures.
→ **[Read the PDF](real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.pdf)** · [Markdown source](real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.md) · [LaTeX](real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.tex)
→ Published: **[Zenodo 10.5281/zenodo.20576485](https://doi.org/10.5281/zenodo.20576485)** (CC‑BY‑4.0)

## Repository structure

```
real_research/                 # the genuine work
├── papers/                    # ★ the paper: PDF, Markdown, LaTeX, 8 figures, Zenodo metadata
│   ├── ZIMMERMAN_THEORY_OF_GRAVITY.pdf / .md / .tex
│   └── figures/               # RAR, a₀(z), BTFR, three-law, seesaw, ladders, galaxy/cluster split
├── reviews/                   # analysis + audit scripts (FDR, precision-physics review, foundations)
├── data/                      # public datasets: SPARC, 2MRS, eRASS1, high-z kinematics
├── predictions/               # the testable-prediction pipelines
├── figures/                   # additional generated figures
└── *.md                       # the foundation ledgers (derivation chain, cosmic seesaw,
                               #   deep-MOND sign kernel, swampland, predictions, MOND audit)
RETRACTIONS.md                 # scope & retractions — what is and isn't claimed (read this)
ai_slop/                       # deprecated AI-generated material — see the note at the bottom
```

## Reproduce

Every quantitative claim is a runnable script — clone, install, run:

```bash
pip install numpy scipy astropy matplotlib
python real_research/framework_a0_law_of_nature.py      # the three galaxy laws coincide at a₀ = 9.36e-11
python real_research/a0z_clean_ledger.py                # a₀(z): framework vs rivals (rising-cH excluded)
python real_research/forecast_a0z_elt.py                # the decisive z≈3 ELT forecast
python real_research/reviews/desitter_unruh_mond.py     # the derived deep-MOND shape (= Milgrom 1999)
python real_research/clusters_framework_a0.py           # the honest cluster residual
# rebuild the paper PDF (needs pandoc + tectonic):
bash real_research/papers/build_tex.sh
```

## Cite

> Zimmerman, C. P. (2026). *The Zimmerman Theory of Gravity: The Galaxy Acceleration Scale Is Set by the Cosmological Constant (a₀ = c²√(Λ/32π)).* Zenodo. https://doi.org/10.5281/zenodo.20576485

## License

Code: **AGPL‑3.0** ([`LICENSE`](LICENSE)). The paper text: **CC‑BY‑4.0**.

---

## ⚠️ A note on the [`ai_slop/`](ai_slop/) folder — AI‑generated material from an earlier model (Claude Opus 4.5)

This repository began as a single real observation (the MOND scale `a₀ ≈ cH₀`) and then, run largely **autonomously by an earlier model — Claude Opus 4.5 — sprawled into ~18,000 files** of AI‑generated material: a cascade of particle‑physics **numerology** (`m_p/m_e`, `α⁻¹ = 4Z²+3`, a `Z² → Standard Model` cascade), a 20.6 Gpc cosmic‑topology claim, galaxy‑chirality and quasar‑"ghost" detections, biotech/meteorology "Z‑resonances", an E₆ "theory of everything", and the autonomous agent swarms (HermesFlow / TruthFlow / OlympusFlow / …) that produced it all.

**None of it survived audit.** It was tested on real open data and against false‑discovery‑rate baselines, and **every headline retrodiction failed** — a *random* number reproduces the "constants" as well as `32π/3` does. It is **retracted in full** (see [`RETRACTIONS.md`](RETRACTIONS.md)) and is **not part of the Zimmerman Theory of Gravity's claims**. The genuine, peer‑facing result is the gravity‑and‑dark‑sector physics in [`real_research/`](real_research/) and the paper above.

It is **preserved, not deleted** — a labeled dead end is more useful (and more honest) than a quiet one. Browse it here if you're curious how the sausage *wasn't* made:

📁 **[`ai_slop/`](ai_slop/)** — *here be dragons.*
