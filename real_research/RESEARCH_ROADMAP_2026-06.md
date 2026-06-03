# Research roadmap — ten legitimate next steps, piece by piece

**Carl Zimmerman · June 2026.** Concrete, bounded, honest next steps to push the framework forward —
ordered by leverage and tractability. Each is a single piece with a clear deliverable; none involves
numerology or a manufactured derivation. The honest context that shapes the order: the *theory* engine
is at its boundary (every route walked; the deep-MOND sign is unsolved by everyone), and the *existing*
data are weak and confounded (the 3 direct a₀(z) points favour the framework at ~2σ; the high-z TFR is
gas-confounded — `reviews/btfr_evolution_confound.py`). So the highest-value moves harden the data and
the foundation, not the (boundary-reached) engine.

---

## Tier I — Harden the existing-data case (most immediate, most tractable)

**1. Gas-clean the direct a₀(z) points.** Re-derive the existing high-z a₀ measurements (Várásteanu z=0.05,
MUSE-DARK III z=0.9, + SPARC z=0) using *per-galaxy* gas masses (HI/CO where available) so a₀ is read from
the deep-MOND tail free of the gas-fraction confound that wrecks the TFR. *Deliverable:* a cleaner 3–5
point a₀(z) with a controlled baryon census. *Why legitimate:* removes a known systematic, doesn't add a
parameter. *Tractable.*

**2. Build a homogeneous direct-a₀(z) compilation.** Reanalyse existing high-z IFU surveys (KMOS³ᴰ, KROSS,
KGES, the A&A 2024 0.6<z<2.5 TFR sample) with **one** pipeline + controlled baryon census, extracting a₀
from each galaxy's deep-MOND tail. *Deliverable:* tens of a₀(z) points replacing the 3-point dependence;
directly resolves the direct-vs-TFR tension. *Tractable–moderate* (the data are public; the work is the
homogeneous reduction).

**3. Joint forward-model fit.** Model {direct a₀, BTFR zero-point} jointly from {a₀(z), gas fraction,
pressure support} and fit the data, *marginalizing* the confounds. *Deliverable:* the honest current
significance of a₀∝E(z) vs SIV (decrease) vs constant vs ΛCDM, with systematics in the error bar.
*Tractable.* This is the rigorous replacement for the χ²=3 toy.

## Tier II — The foundation (§0: is MOND real?) — highest leverage on everything

**4. Wide-binary reanalysis.** Compute the framework's EFE-suppressed wide-binary acceleration and confront
the **Chae vs Banik** Gaia DR3 datasets head-to-head. *Deliverable:* where the framework's prediction sits
in the 16–19σ-Newtonian (Banik) vs MOND-consistent (Chae) split. *Why it matters most:* if MOND is dead at
z=0, the whole framework dies (§0). *Tractable–moderate* (data public; the dispute is methodological).

**5. z=0 EFE consistency.** Test whether the framework's a₀ reproduces the SPARC **EFE detection** (Chae
2020/2021): does the predicted external-field suppression match the measured ~0.1 dex RAR downturn in
high-field galaxies? *Deliverable:* a clean existing-data consistency check of the EFE that Tier-2 (the
distinctive test) relies on. *Tractable.*

## Tier III — Theory (the engine / covariant completion) — hard, high value

**6. Derive the AeST 𝒦(𝒬) cosmological function** from the horizon/de Sitter foundation — the remaining
~20% of the covariant completion not yet forced (`clean_slate_field_theory.py` derived the rest). *This is
the one genuinely open theory piece that is neither numerology nor closed.* *Deliverable:* either a forced
form of 𝒦(𝒬) (a real result) or a precise proof of what extra input it needs. *Hard; honest about it.*

**7. Modified-inertia vs modified-gravity observable test.** Compute where the de Sitter–Unruh (inertia)
and Debye/AeST (gravity) interpolations **differ observably** — the closed-orbit/non-locality issue made
concrete (e.g. eccentric-orbit dwarfs, the EFE in detail). *Deliverable:* a data-testable discriminator
between the two engines, turning "which engine" from philosophy into measurement. *Moderate.*

## Tier IV — Sharpen the distinctive test

**8. Combined-probe joint forecast.** A single likelihood combining direct a₀(z) + EFE + confound-
marginalized TFR. *Deliverable:* the sample size to distinguish framework / SIV / ΛCDM / constant at 5σ —
the rigorous successor to the per-test forecasts. *Tractable.*

**9. Concrete observing request.** Turn the z~3 proposal into a **named-program target list**: specific
extended, rotation-supported, deep-MOND candidates from existing catalogues (COSMOS, CEERS, the ALMA
[CII] disc samples), with per-target JWST/ALMA exposure and expected significance. *Deliverable:* an
actionable Cycle proposal skeleton. *Tractable.*

## Tier V — Dissemination

**10. Revise & circulate the paper.** Fold the **SIV discriminator** (framework vs SIV opposite directions,
the χ² evidence), the **honest TFR confound**, and the **combined-probe significance** into the published
scaling-MOND paper; post a revised version and circulate to a high-z-dynamics observer for the z~3
collaboration. *Deliverable:* a stronger, better-situated paper and a path to the actual measurement.
*Tractable; needs Carl in the loop (authorship/contact).*

---

## Suggested order (piece by piece)

Do **1 → 2 → 3** first (harden the a₀(z) data; cheap, public data, directly answers "does the posit
survive the confounds?"). In parallel, **4** (the foundation — highest stakes) and **5** (a quick
consistency check). Then **8 → 9 → 10** to sharpen and disseminate. Hold **6 → 7** (theory) as the
longer-horizon track — real, hard, and honestly not where the near-term evidence moves.

**The honest through-line:** none of these *proves* the posit (nothing can). They (i) harden or kill the
existing-data case under controlled systematics, (ii) stress the foundation (is MOND real at all?), and
(iii) make the one decisive test — a clean direct a₀ at z~3 — actually happen. That is how this moves
forward legitimately: not by deriving more, but by *measuring* the one thing that distinguishes the
framework from its rivals.
