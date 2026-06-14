# ell = r_DE (dark-energy crossover radius): DERIVED, threads NEITHER — the level-set self-defeats (2026-06-14)

*Task: derive the smoothing scale ell from first principles (framework-native, not tuned), then test the density-law
a0 = (c/2)√(G ρ_total,smoothed-over-ell) on the hard double constraint — galaxy SPARC RAR scatter (~0.13 dex) AND
eRASS1 cluster η (→1.2–1.5, not over-close). Candidate: ell = r_DE, the radius where a structure's mean enclosed
matter density drops to ρ_DE. The most framework-native scale (it reuses the ONE density already in the formula, ρ_DE,
as nothing-but the level set). Computed on real 175 SPARC + real eRASS1 (9,830 clusters). Script:
`density_a0_rDE_crossover.py`. Quarantine: a0/Z never asserted derived.*

---

## The derivation — and the fatal structural fact it exposes

r_DE is **defined** as the radius where the mean enclosed matter density equals ρ_DE:
`ρ̄_matter(<r_DE) ≡ ρ_DE`. Therefore, **by construction**, the mean matter density *within* r_DE is **exactly ρ_DE —
for ANY structure** (galaxy, cluster, void, anything). r_DE is the *level set* of the very density the prescription
then averages. So the smoothed effective density is **universal**:

> `ρ_eff = ρ_DE (background) + ρ̄_matter(<r_DE) = ρ_DE + ρ_DE = 2 ρ_DE`  for every structure.

`a0 = (c/2)√(G·2ρ_DE) = √2 · 9.36×10⁻¹¹ = 1.32×10⁻¹⁰`, **identical for galaxies and clusters.** This is not a tuning
choice — it is forced by the definition of r_DE. **r_DE is genuinely DERIVED (no free knob), and that is exactly why it
fails: a level-set-defined smoothing scale produces ZERO differential boost.** The mechanism the cluster fix needs (a
~15× *larger* in-cluster a0 than the galaxy a0) is mathematically impossible under r_DE, because r_DE self-normalizes
every structure to the same enclosed density.

The r_DE radii are sane and confirm this is the real crossover, not a degenerate artifact:
- **galaxy r_DE: median 275 kpc** (range 53 kpc – 1.07 Mpc) — ~the virial/halo scale, as expected.
- **cluster r_DE: 7–26 Mpc** (baryon vs total profile) — far outside R500, deep in the cosmic web. The cluster's mean
  density only falls to ρ_DE way out at several-to-tens of Mpc; but averaging matter *inside* that huge radius gives
  back exactly ρ_DE. The cluster's dense *interior* (500 ρ_crit ~ 1000 ρ_DE at R500) is diluted away by the r_DE
  averaging volume.

## (1) GALAXY RAR — slightly INFLATED, the universal √2 sits above the optimum (real SPARC, Υ=0.70)

Every galaxy gets the identical a0 = √2·9.36e-11 = 1.32e-10. No scatter-from-environmental-spread (the boost is
uniform), but the universal value is now ~30% above the dS-Unruh-optimal 1.03e-10, so the scatter inflates modestly:

| interpolation | const a0=9.36e-11 | r_DE a0 = √2·9.36 = 1.32e-10 | inflation |
|---|---|---|---|
| **framework dS-Unruh ν** | 0.1448 dex | **0.1497 dex** | **+0.005 dex (+3.4%)** |
| McGaugh ν | 0.1471 dex | 0.1663 dex | +0.019 dex (+13%) |

**Not catastrophic** (the prescription does NOT erase galaxy MOND — the local/clumpy 1e6× reading does that; r_DE
correctly avoids it). But it is the **wrong direction**: r_DE pushes the universal a0 to the *high* edge of the
convention-compatible band, costing 0.13→0.15 dex on the framework's own ν. The RAR survives but does not stay
*tight* — it loosens, where the make-or-break demand was that it stay ~0.13.

## (2) CLUSTERS — η barely moves, NOWHERE NEAR 1.2–1.5 (real eRASS1, banked convention: simple ν, Def A, fstar=0.2)

Baseline reproduced exactly (η median **2.150**, banked 2.149). Under r_DE, the same universal √2 boost gives:

| a0 reading | a0 | η(R500) median | verdict |
|---|---|---|---|
| framework const | 9.36e-11 | **2.150** | the deficit |
| **r_DE crossover (DERIVED)** | √2·9.36 = 1.32e-10 | **1.838** [1.70, 2.17] | falls only ~15%, **NOT 1.2–1.5** |
| ρ_total cosmic | 1.13e-10 | 1.974 | — |
| *needs to hit η=1.5* | *2.06e-10 = 2.2× a0_DE (ρ_eff~5 ρ_DE)* | 1.5 | r_DE cannot reach |
| *needs to hit η=1.2* | *3.32e-10 = 3.5× a0_DE (ρ_eff~13 ρ_DE)* | 1.2 | r_DE cannot reach |

r_DE delivers ρ_eff = 2 ρ_DE; clusters need ρ_eff ~ 5–13 ρ_DE. **It is short by a factor of 2.5–6.5 in density (1.6–2.5×
in a0).** The deep-dive's working "~15× in-cluster a0" came from the **Mpc-ambient** reading (smoothing matter over a
*fixed* ~Mpc window that captures the cluster overdensity) — NOT r_DE. r_DE's ~7–26 Mpc averaging volume is far too
large; it dilutes the overdensity back to ρ_DE by definition.

*(Contrast, NOT the r_DE prescription: a0 from the dense interior — mean density within R500 itself — gives a0 ~9–32×
and η→0.42–0.75, i.e. it over-closes. The honest window between "r_DE dilutes to nothing" and "R500-interior
over-closes" is exactly where a tuned ~Mpc scale lives — and r_DE lands on the wrong side of it.)*

## VERDICT — THREADS NEITHER; the cleanest derived candidate is structurally self-defeating

**ell = r_DE is genuinely derived (no tuned knob), and it threads NEITHER constraint.** Because r_DE is the level set
of ρ_DE, the smoothed density is forced to 2 ρ_DE universally — a single √2 nudge applied identically to galaxies and
clusters. That is the worst possible behavior: it **inflates** the galaxy RAR scatter (0.1448→0.1497 dex on the
framework ν, +3.4%; +13% on McGaugh) AND **leaves the cluster deficit at η≈1.84** (needed 1.2–1.5). A single
*universal* multiplier can never differentially boost clusters — and r_DE provably IS a universal multiplier.

**This is a genuinely informative NULL, and it cuts the right way both ways:**
- It **closes** the "most framework-native" derivation of ell. The density-law's one distinctive cluster out requires a
  smoothing scale that is *Mpc-fixed* (captures cluster overdensity, leaves galaxies cosmic) — NOT density-level-set
  (which self-normalizes). r_DE, the cleanest derived candidate, lands on the wrong physics.
- It **confirms** the deep-dive's caveat: the surviving Mpc-ambient reading "rides on an UNDERIVED smoothing scale."
  r_DE was the natural attempt to derive it; the attempt shows the scale **cannot** come from the density profile
  itself — it must be an external ~Mpc input (e.g. the AeST 1/μ ~ 1 Mpc mass scale, which is the only Mpc scale the
  framework has, and it is a *fixed* scale, exactly the right kind — but it is tuned/cosmological, not derived here).

**a0↔Λ cost:** the density reading IS a superset that preserves a0~cH cosmically (cosmic ρ_total=ρ_crit → a0=1.13e-10,
still ~cH0, still Milgrom's coincidence; ρ_DE alone → 9.36e-11). r_DE specifically reduces every structure to ρ_eff=2
ρ_DE → a0=1.32e-10 = √2·a0_Λ, so it trades a0↔Λ for a0↔(2ρ_DE), a *constant* — it does NOT spend the superset property
on local clumpiness, BUT it also gains nothing from it (no environmental dependence, so the falsifiable
"a0_cluster>a0_field" prediction evaporates — every system gets √2·a0_Λ). The cost is paid for no benefit.

## Grade: **D** — derived, clean, decisive NULL. Threads neither; the level-set construction is self-defeating by definition.

A derived ell that threaded both would be an A. r_DE is honestly derived but produces a *universal* √2 boost that
slightly hurts galaxies and barely touches clusters. It does not break galaxies catastrophically (the RAR survives at
0.15 dex), and it is not tuned — but it fails the make-or-break demand (RAR stays *tight* AND η→1.2–1.5) on both legs.
The honest closing line: **the framework's most natural derivation of the smoothing scale shows the scale cannot be
self-derived from the density profile — the density-law cluster out needs an EXTERNAL fixed ~Mpc scale (tuned or
imported from AeST 1/μ), not a level-set radius. The density-a0 route stays alive only as a tuned-Mpc reading, not a
derived one.**

*No high-priest dismissal (r_DE is credited as the cleanest derived candidate, computed on real data, RAR-survival
noted). No manufactured win (η=1.84 is reported at full weight, the galaxy inflation is reported both ν ways, the
"needs 5–13 ρ_DE" gap is quantified). Quarantine held — a0/Z never asserted derived; r_DE derived, the density it
yields is not the framework's a0.*
