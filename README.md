# The Zimmerman Programme — a directory

**One claim: the galactic acceleration scale is set by the dark-energy density.**

$$a_0 \;=\; \kappa\,c\sqrt{G\rho_\Lambda}\;=\;\frac{cH_\Lambda}{Z},
\qquad \kappa=\tfrac12,\qquad Z=\sqrt{32\pi/3}=5.78881,
\qquad a_0 = 9.36\times10^{-11}\ \mathrm{m\,s^{-2}}$$

Realised as **modified inertia** with the interpolation $\nu(y)=\sqrt{1+1/y}$.

> ### ⚠️ Read this first
>
> **This is not a theory of everything.** All theory-of-everything and Standard-Model claims were
> **publicly retracted 2026-06-23** — see [RETRACTIONS.md](RETRACTIONS.md). Material from the earlier
> automated effort is kept for the record under [`ai_slop/`](ai_slop/), marked, and is **not part of the
> audited programme**.
>
> **Credit — and it is larger than this repository used to say.** The law
> $g_{\rm obs}^2=g_{\rm bar}^2+a_0g_{\rm bar}$ is **not merely the same interpolating kernel** as
> Milgrom's. **Milgrom (1999, *Phys. Lett. A* 253, 273, Eqs. 6–9) derives this exact law from the de
> Sitter–Unruh balance and fixes its coefficient at $a_0=2cH_\Lambda$** — verified symbolically here,
> difference exactly zero. Re-derived entropically by Pikhitsa (2010, arXiv:1010.0318) and
> Klinkhamer & Kopp (2011, arXiv:1104.2022), both also landing on $2cH_\Lambda$. The a₀–Λ *tie* has
> prior art three times over: Blanchet & Le Tiec (2009), Blanchet & Seraille (2025), and Singh (2026,
> arXiv:2601.04290 — the same formula, coefficient 8% away).
>
> **So what is this programme's?** A **re-normalisation of the coefficient to fit data**
> ($\kappa=\tfrac12$ against Milgrom's derived 2, which is $2Z=11.58\times$ larger), the
> **modified-inertia completion**, and the structural results in §2 below. Not a derivation of the law,
> and not a derivation of its scale.
>
> **→ [STANDING.md](STANDING.md) is the single source of truth.** If anything here conflicts with it,
> STANDING is newer.

---

## Start here

| document | what it is |
|---|---|
| **[STANDING.md](STANDING.md)** | **The entry point.** Claim · earned · postulated · 5 live fronts · 15 closed doors · open liabilities · retractions in force. |
| [RETRACTIONS.md](RETRACTIONS.md) | Every withdrawn claim, dated. |
| [INTEGRITY_AUDIT.md](INTEGRITY_AUDIT.md) | Audit trail on the corpus itself. |
| [ERRATA_GEMINI_TASKS_2026-07-16.md](ERRATA_GEMINI_TASKS_2026-07-16.md) | Errata from delegated-work audits. |

---

## What is novel, by topic

Ordered by how much survives scrutiny. Each entry links the working directory and the paper.

### 1 · The coefficient reduction and the a₀ line
The cleanest earned results. $a_0=\kappa c\sqrt{G\rho_\Lambda}$ makes every $\pi$, the 32 and the 3
cancel, and $g_{\rm obs}^2-g_{\rm bar}^2=a_0g_{\rm bar}$ is an exact identity.
**RAR fit: 0.108 dex on SPARC** at Υ=0.70 — beating regular MOND's 0.122–0.140 on the framework's own
footing. This number is untouched by everything below.
[`prep_2026/a0_line/`](prep_2026/a0_line/) · [`a0_line_mlpriors/`](prep_2026/a0_line_mlpriors/) · [`a0_line_trgb/`](prep_2026/a0_line_trgb/) · paper [THE_COSMOLOGICAL_CONSTANT_SETS_A0.md](opus_48_extended_research/papers/THE_COSMOLOGICAL_CONSTANT_SETS_A0.md)

### 2 · Structural theorems for the closure — **the most defensible novel content**
Seven machine-verified results; five are prohibitions that *remove* free content.
**Paper: [MI_STRUCTURAL_THEOREMS.md](opus_48_extended_research/papers/MI_STRUCTURAL_THEOREMS.md) · DOI [10.5281/zenodo.21708842](https://doi.org/10.5281/zenodo.21708842)** (v2)
- **Thm 1** first moment, worldline-general — [`mi_dcac_split_settled_2026.py`](real_research/reviews/mi_dcac_split_settled_2026.py)
- **Thm 2** $\mathrm{Im}\,K\equiv0$ ⇒ MOND amplitude and dissipation **mutually exclusive**; the sign postulate is **demoted** to unobservable
- **Thm 3** no *local* higher-derivative action reproduces the law ⇒ nonlocality is **required** — [`mi_closure_vs_action_gap_2026.py`](real_research/reviews/mi_closure_vs_action_gap_2026.py)
- **Thm 4** MI **cannot** modify the FRW background — [`mi_channelA_friedmann_2026.py`](real_research/reviews/mi_channelA_friedmann_2026.py)
- **Thm 5** the EFE is quadrature with a **vector** cross term ⇒ a **footing-free** rotation-curve dipole, 4.2–22.3%, attractor-faster — [`mi_efe_derived_general_2026.py`](real_research/reviews/mi_efe_derived_general_2026.py). *This is the one prediction that is both distinctive and MI-favourable.*

### 3 · The field theory — status and honest limits
[`prep_2026/mi_field_theory/`](prep_2026/mi_field_theory/) · [`mi_fingerprint/`](prep_2026/mi_fingerprint/) · [`mi_kernel_argument/`](prep_2026/mi_kernel_argument/) · [`kernel_fingerprint/`](prep_2026/kernel_fingerprint/)
**Status:** the law is *not* the Euler–Lagrange equation of the published action (Thm 8). It **is**
variational in a nonlocal **non-quadratic** class — Milgrom's own virial result (astro-ph/0510117) —
but only on the circular slice, and that class is not uniquely determined.
See [`mi_three_corrections_priorart_2026.py`](real_research/reviews/mi_three_corrections_priorart_2026.py).

### 4 · Wide binaries — the sharpest live front
[`prep_2026/gaia_dr4_prep/`](prep_2026/gaia_dr4_prep/) — **frozen, hash-stamped pre-registration** with amendments, all filed *before* data · paper DOI [10.5281/zenodo.21702746](https://doi.org/10.5281/zenodo.21702746)
**Clock: Gaia DR4, ~Dec 2026.** ⚠️ The literature disagrees violently on this exact quantity — Banik+24
reports **19σ for Newtonian**; Chae 2023 reports force γ = 1.43 ± 0.06. That disagreement is **13×** the
frozen systematic allowance, which is why Amendment 3 splits the budget one-sided.

### 5 · Clusters, a₀(z), and the closed fronts
[`prep_2026/a0z_crossscale/`](prep_2026/a0z_crossscale/) · [`a0z_from_sne/`](prep_2026/a0z_from_sne/) · [`cluster_efe_channel/`](prep_2026/cluster_efe_channel/) · [`cluster_kink_spec/`](prep_2026/cluster_kink_spec/)
Papers: [A0Z_DESI_DARK_ENERGY_SCALE.md](opus_48_extended_research/papers/A0Z_DESI_DARK_ENERGY_SCALE.md) · [CLUSTER_RESIDUAL_DENSITY_NOGO.md](opus_48_extended_research/papers/CLUSTER_RESIDUAL_DENSITY_NOGO.md) (DOI [10.5281/zenodo.20779562](https://doi.org/10.5281/zenodo.20779562))
The cluster residual is **real but shared** across the whole relativistic-MOND family — not
framework-specific, not a kill.

### 6 · Nulls, published as nulls — **the part most worth reading**
- [`project_atomos/`](project_atomos/) — exhaustive Standard-Model parameter search, **null**, DOI [10.5281/zenodo.21654272](https://doi.org/10.5281/zenodo.21654272), published *after* an audit withdrew two of its own claims
- κ-forcing closed: [KAPPA_ONE_PARAMETER_GEOMETRY.md](opus_48_extended_research/papers/KAPPA_ONE_PARAMETER_GEOMETRY.md)
- **Z carries no geometry:** [`reviews/z_numerology_density_2026.py`](reviews/z_numerology_density_2026.py) — closed forms in π at complexity ≤ 4 cover **100%** of targets in [3,12] to 1%; at the real ±16% precision **9,912** expressions match a₀, and `cH₀/7` fits to **0.056%**. $Z=\sqrt{8\pi/3}/\kappa$, so Z carries exactly one bit beyond κ.
- [THE_SEARCH_WAS_NEVER_WASTED.md](opus_48_extended_research/papers/THE_SEARCH_WAS_NEVER_WASTED.md)

### 7 · Kit and tooling
[`a0kit/`](a0kit/) · [`real_research/predictions/`](real_research/predictions/) · [`prep_2026/equation_book/`](prep_2026/equation_book/)

---

## Working rules

Enforced by the scripts, not by trust.

1. **Test the framework on its own terms** — modified *inertia*, horizon-derived a₀, its own interpolation. Never through the standard-MOND lens; never McGaugh's ν.
2. **Verify a deficit as rigorously as a win.** Manufacture neither.
3. **Both a₀ footings on every dimensional number** — canonical ρ_DE (9.36e-11), alternative ρ_total (1.13e-10) — and show the spread.
4. **Every load-bearing claim gets a committed, runnable script** that exits non-zero on a failed internal check. No hard-coded verdicts.
5. **Never say "the theory is closed."**
6. **Amend frozen pre-registrations in the open, before data.**
7. **Cite or flag** — any number not traced to a script or a cited paper is marked unverified.
8. **Nothing personal in this repository.**

---

## Publication record

[![Paper DOI](https://img.shields.io/badge/Paper-10.5281%2Fzenodo.20576485-blue)](https://doi.org/10.5281/zenodo.20576485)
[![Falsification Map DOI](https://img.shields.io/badge/Falsification%20Map%20(June%202026)-10.5281%2Fzenodo.20670670-blueviolet)](https://doi.org/10.5281/zenodo.20670670)
[![de Sitter Gauge DOI](https://img.shields.io/badge/de%20Sitter%20Gauge%20(June%2016%202026)-10.5281%2Fzenodo.20721540-blueviolet)](https://doi.org/10.5281/zenodo.20721540)
[![Skordis-Zlosnik DOI](https://img.shields.io/badge/Why%20Skordis%20%26%20Zlosnik%20Were%20Right%20(June%2020%202026)-10.5281%2Fzenodo.20773004-blueviolet)](https://doi.org/10.5281/zenodo.20773004)
[![Cluster Density No-Go DOI](https://img.shields.io/badge/Galaxy--Cluster%20Density%20No--Go%20(June%2020%202026)-10.5281%2Fzenodo.20779562-blueviolet)](https://doi.org/10.5281/zenodo.20779562)
[![s̄^TX Target DOI](https://img.shields.io/badge/s%CC%84%5ETX%20Ephemeris%20Target%20(June%2027%202026)-10.5281%2Fzenodo.20978308-blueviolet)](https://doi.org/10.5281/zenodo.20978308)
[![Growing-ν DOI](https://img.shields.io/badge/Growing%20Neutrino%20Mass%20(June%2027%202026)-10.5281%2Fzenodo.20977421-blueviolet)](https://doi.org/10.5281/zenodo.20977421)
[![Scale Without Law DOI](https://img.shields.io/badge/Scale%20Without%20Law%20(June%2028%202026)-10.5281%2Fzenodo.21016309-blueviolet)](https://doi.org/10.5281/zenodo.21016309)
[![Cluster Anisotropy DOI](https://img.shields.io/badge/Cluster%20Anisotropy%20MI%20Test%20(July%201%202026)-10.5281%2Fzenodo.21104820-blueviolet)](https://doi.org/10.5281/zenodo.21104820)
[![a0(z) Discriminant DOI](https://img.shields.io/badge/Non--Monotonic%20a0(z)%20(July%201%202026)-10.5281%2Fzenodo.21110936-blueviolet)](https://doi.org/10.5281/zenodo.21110936)
[![s̄^TX Fixed-Direction DOI](https://img.shields.io/badge/s%CC%84%5ETX%20Fixed--Direction%20Fit%20(July%202%202026)-10.5281%2Fzenodo.21137568-blueviolet)](https://doi.org/10.5281/zenodo.21137568)
[![Sign Premise DOI](https://img.shields.io/badge/Sign%20Premise%20%3D%20State%20Clause%20(July%202%202026)-10.5281%2Fzenodo.21139029-blueviolet)](https://doi.org/10.5281/zenodo.21139029)
[![Which-a₀ DOI](https://img.shields.io/badge/Which%20a0%3F%20Population%20Split%20(July%202%202026)-10.5281%2Fzenodo.21140507-blueviolet)](https://doi.org/10.5281/zenodo.21140507)
[![Fourth Horn DOI](https://img.shields.io/badge/Fourth%20Horn%20PT%2FPU%20Exclusion%20(July%202%202026)-10.5281%2Fzenodo.21148494-blueviolet)](https://doi.org/10.5281/zenodo.21148494)
[![Five Theorems DOI](https://img.shields.io/badge/Five%20Theorems%20Kernel%20Closure%20(July%203%202026)-10.5281%2Fzenodo.21152331-blueviolet)](https://doi.org/10.5281/zenodo.21152331)
[![Sixth Theorem DOI](https://img.shields.io/badge/Sixth%20Theorem%20Transient%20Closure%20(July%203%202026)-10.5281%2Fzenodo.21175723-blueviolet)](https://doi.org/10.5281/zenodo.21175723)
[![Residual Doors DOI](https://img.shields.io/badge/No%20Pump--Free%20Corner%20(v3%2C%20July%2017%202026%20%E2%80%94%20D3%20sign%20corrected)-10.5281%2Fzenodo.21179351-blueviolet)](https://doi.org/10.5281/zenodo.21179351)
[![Position Whitepaper DOI](https://img.shields.io/badge/POSITION%3A%20There%20Is%20No%20Dark%20Matter%20in%20Galaxies%20(July%2011%202026)-10.5281%2Fzenodo.21312985-black)](https://doi.org/10.5281/zenodo.21312985)
[![Flagship DOI](https://img.shields.io/badge/FLAGSHIP%20dS--Unruh%20MI%20%2B%20Lensing%20Trilemma%20(July%2011%202026)-10.5281%2Fzenodo.21312654-red)](https://doi.org/10.5281/zenodo.21312654)
[![Elastic-Medium Action DOI](https://img.shields.io/badge/Covariant%20Elastic--Medium%20Action%20(July%2010%202026)-10.5281%2Fzenodo.21301058-blueviolet)](https://doi.org/10.5281/zenodo.21301058)
[![y_c=Z/2 Cutoff DOI](https://img.shields.io/badge/Elastic--Medium%20Cutoff%20y_c%3DZ%2F2%20(July%2010%202026)-10.5281%2Fzenodo.21300855-blueviolet)](https://doi.org/10.5281/zenodo.21300855)
[![MI Completion DOI](https://img.shields.io/badge/Written%20MI%20Action%20%E2%80%94%20Covariant%20Completion%20(v13%2C%20July%209%202026)-10.5281%2Fzenodo.21253644-crimson)](https://doi.org/10.5281/zenodo.21253644)
[![MI Field Theory Results DOI](https://img.shields.io/badge/MI%20Field%20Theory%20Results%20(July%2016%202026)-10.5281%2Fzenodo.21403470-crimson)](https://doi.org/10.5281/zenodo.21403470)
[![a0-line / Lambda-inversion DOI](https://img.shields.io/badge/a0--line%20%2B%20%CE%9B--inversion%20from%20Rotation%20(July%2017%202026)-10.5281%2Fzenodo.21419735-red)](https://doi.org/10.5281/zenodo.21419735)
[![Lensing No-Go DOI](https://img.shields.io/badge/Passivity%20Obstruction%20%E2%80%94%20MI%20Lensing%20No--Go%20(July%2017%202026)-10.5281%2Fzenodo.21418816-red)](https://doi.org/10.5281/zenodo.21418816)
[![Sigma-Spread DOI](https://img.shields.io/badge/Relational%20%CF%83--Spread%20%E2%80%94%20MG--Impossible%20Signature%20(July%2017%202026)-10.5281%2Fzenodo.21421896-red)](https://doi.org/10.5281/zenodo.21421896)
[![Cross-Scale a0(z) DOI](https://img.shields.io/badge/Cross--Scale%20a0(z)%20%E2%80%94%20Galaxy%20vs%20Cosmic%20Dark%20Energy%20(v2%2C%20July%2019%202026)-10.5281%2Fzenodo.21440407-red)](https://doi.org/10.5281/zenodo.21440407)
[![SHLEM Null DOI](https://img.shields.io/badge/SHLEM%20Null%20%E2%80%94%20Which%20Acceleration%20Does%20Inertia%20Listen%20To%3F%20(July%2020%202026)-10.5281%2Fzenodo.21458605-red)](https://doi.org/10.5281/zenodo.21458605)
[![Triangle DOI](https://img.shields.io/badge/Three%20Roads%20to%20the%20%CE%9B%20Acceleration%20Scale%20(July%2020%202026)-10.5281%2Fzenodo.21460161-red)](https://doi.org/10.5281/zenodo.21460161)
[![TDG History DOI](https://img.shields.io/badge/Tidal%20Dwarfs%20%26%20History--Dependent%20Inertia%20(July%2020%202026)-10.5281%2Fzenodo.21461435-red)](https://doi.org/10.5281/zenodo.21461435)
[![Rubin Pre-Reg DOI](https://img.shields.io/badge/Pre--Registered%20a0(z)%20Gate%20vs%20Rubin%2FLSST%20SNe%20(July%2021%202026)-10.5281%2Fzenodo.21478568-black)](https://doi.org/10.5281/zenodo.21478568)
[![Corpus DOI](https://img.shields.io/badge/Code%20%26%20Data-10.5281%2Fzenodo.20576494-blue)](https://doi.org/10.5281/zenodo.20576494)
[![Paper PDF](https://img.shields.io/badge/PDF-read%20the%20paper-success)](real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.pdf)
[![License](https://img.shields.io/badge/code-AGPL--3.0-lightgrey)](LICENSE)
## Licence

Code [AGPL-3.0](LICENSE) · papers and text CC-BY-4.0 on Zenodo.
