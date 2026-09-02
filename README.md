# The Zimmerman Programme

**One claim: the galactic acceleration scale is set by the dark-energy density.**

$$a_0 \;=\; \kappa\,c\sqrt{G\rho_\Lambda}\;=\;c^2\sqrt{\frac{\Lambda}{32\pi}}\;=\;9.3619\times10^{-11}\ \mathrm{m\,s^{-2}}$$

Plain text, for the record: `a0 = kappa * c * sqrt(G * rho_Lambda) = c^2 * sqrt(Lambda / (32 pi)) = 9.36e-11 m/s^2`, with κ = ½ **adopted** — measured **0.551 ± 0.043** by a distance-free method (fitted, **not derived**; four candidate coefficients sit inside 2σ). Alternative footing (ρ_total, cH₀): a₀ = 1.1279×10⁻¹⁰ — every dimensional result in this repository is quoted on both footings.

The exact algebraic law (the **a₀-line**) and the operative interpolation kernel:

$$g_{\rm obs}^2-g_{\rm bar}^2=a_0\,g_{\rm bar}
\qquad\Longleftrightarrow\qquad
g_{\rm obs}=\sqrt{g_{\rm bar}^2+a_0\,g_{\rm bar}}\,,
\qquad
\nu(y)=\frac{1}{1-e^{-\sqrt{y}}}$$

(kernel form: **Milgrom & Sanders 2008**, ApJ 678, 131, Eq. 13 at α = ½ — adopted by McGaugh–Lelli–Schombert 2016; credited, not claimed). Operative arm since 2026-08-08: **modified gravity** — the modified-inertia arm is closed, excluded 21σ by lensing. Prior art on the arm verdict: Banik & Zhao ([arXiv:2110.06936](https://arxiv.org/abs/2110.06936), §2.5–2.6).

**The relativistic realisation** embeds the scale in Aether-Scalar-Tensor theory (Skordis & Złośnik 2021, PRL **127** 161302 — theirs, credited) with one structural promotion — **the MOND scale is the dark sector's pressure**:

$$\boxed{\;\mathcal{A}(\mathcal{Q})\equiv a_0^2(\mathcal{Q})=\kappa^2\,G\,\bigl(-\mathcal{K}(\mathcal{Q})\bigr)\;}
\qquad
\mathcal{K}(\mathcal{Q})=-M^4+\mu^2\Lambda_D^2\left[1-\sqrt{1-\frac{(\mathcal{Q}-\mathcal{Q}_0)^2}{\Lambda_D^2}}\right]$$

an offset-DBI with β ≡ μ²Λ_D²/M⁴ = 1 (selected, not derived). Since p = 𝒦 identically and −𝒦 = ρ_Λ today, the a₀ normalisation above is reproduced to the digit, **w = −1 stays exact**, and the redshift law is **derived, not imposed**:

$$\frac{a_0^2(z)}{a_0^2(0)}=\frac{\sqrt{1+\nu_0^2}}{\sqrt{1+\nu_0^2\,(1+z)^6}}\,,
\qquad z_t=\nu_0^{-1/3}-1\in[17,35]$$

— constant to <1% everywhere MOND is tested (z ≤ 5), **off at recombination as an output** (a₀ falls to 0.002–0.006 of today's value), so the CMB's dust-like clustering is a prediction, not an accommodation. Newest result (2026-08-14): AeST's free background rate is **pinned by galaxy-scale phenomenology alone**, in observables where a₀ cancels identically:

$$\mathcal{Q}_0=\frac{g_{\rm tot}-g_N}{c\,v}\;\approx\;2.4\times10^{-3}\,\text{–}\,1.5\times10^{-2}\ \mathrm{Mpc}^{-1}$$

interior to Skordis & Złośnik's own CMB fits, containing both their MOND-compatible parameter sets and excluding their MOND-incompatible one ([DOI 10.5281/zenodo.21937958](https://doi.org/10.5281/zenodo.21937958)).

**Standing 2026-09-02 (rev. 6) — what the September closure changed.** The condensate above is a **γ = 2 polytrope** in the static limit, $p_d=(2\pi G/\mu^2)\rho_d^2$, $c_s^2=4\pi G\rho_d/\mu^2=|\Psi|c^2$ (published, [DOI 10.5281/zenodo.22242701](https://doi.org/10.5281/zenodo.22242701), v2 [22254075](https://doi.org/10.5281/zenodo.22254075)). Read on the cosmic background the same relation gives $c_s^2(z)=4\pi G\rho_{\rm dm}(z)/\mu^2$, which **pins** the DBI amplitude at β = 1, $\Lambda_D/Q_0=\nu_0\Omega_\Lambda/\Omega_{\rm dm}$, 18–300× above the repository's own $P(k)$ ceiling: **the v9 single-field dark sector is excluded**, and the cluster cosmology built on it is withdrawn ([RETRACTIONS.md](RETRACTIONS.md), 2026-09-02). Underneath is a $K$-independent matching theorem: a galaxy well today is the background at $(1+z)^3=\delta_{\rm well}\le5000$ with identical sound speed, so a dust cold enough for the Lyman-α forest falls into galaxies — **pressure cannot keep Ω_dm out of galaxies**, for any $K$. The superfluid route, a rising $a_0\propto H(z)$, and a Hubble-scaled high-pass filter were each run and closed the same way; a quadratic-order theorem shows any elliptic auxiliary that enters the lapse equation frees one dust-like scalar, which is why TeVeS, AeST and the superfluid all carry a third field. The v9 embedding also fails the preferred-frame PPN bounds (α₁, α₂; 2026-08-31, [`closure_2026/fried_chicken_final/`](qwen_claude_field_theory/closure_2026/fried_chicken_final/)), and the nonlocal Deffayet–Woodard kernel class is unstable at linear order (published, [DOI 10.5281/zenodo.22253953](https://doi.org/10.5281/zenodo.22253953), v2 [22255522](https://doi.org/10.5281/zenodo.22255522)). **What survives:** $a_0=\tfrac c2\sqrt{G\rho_{\rm DE}(z)}$ with κ fitted, the $a_0(z)$ switch-off law (it needs only the trace khronon dust), MOND phenomenology, and a cold Ω_dm that double-counts with the boost in galaxies by 2.7–4.4× — the programme's blocking problem. Scripts: [`closure_2026/condensate_pincer_2026/`](qwen_claude_field_theory/closure_2026/condensate_pincer_2026/); explainer: [DUST_FALLS_INTO_GALAXIES.md](opus_48_extended_research/papers/DUST_FALLS_INTO_GALAXIES.md).

> ### ⚠️ Read this first
>
> **This is not a theory of everything.** All theory-of-everything and Standard-Model claims were
> **publicly retracted 2026-06-23** — see [RETRACTIONS.md](RETRACTIONS.md), which records every
> withdrawn claim, dated, including material from an earlier automated effort that is **not part of
> the audited programme**.
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
> ($\kappa=\tfrac12$ against Milgrom's derived 2), the **pressure promotion 𝒜(𝒬) and its derived
> a₀(z) law**, the **𝒬₀ pin**, the **frozen wide-binary pre-registration**, and the structural
> results below. Not a derivation of the law, and not a derivation of its scale.
>
> **→ [STANDING.md](STANDING.md) is the single source of truth.** If anything here conflicts with it,
> STANDING is newer.

---

## Start here

| document | what it is |
|---|---|
| **[STANDING.md](STANDING.md)** | **The entry point** (rev. 6 block, 2026-09-02, at the top). Claim · earned · postulated · live fronts · closed doors · open liabilities · retractions in force. |
| [RETRACTIONS.md](RETRACTIONS.md) | Every withdrawn claim, dated. |
| [INTEGRITY_AUDIT.md](INTEGRITY_AUDIT.md) | Audit trail on the corpus itself. |
| [CITATION.cff](CITATION.cff) · [LICENSE.md](LICENSE.md) | How to cite; code AGPL-3.0, content CC-BY-4.0. |

---

## What is novel, by topic

Ordered by how much survives scrutiny. Each entry links the working directory and the paper.

### 1 · The coefficient reduction and the a₀ line
$a_0=\kappa c\sqrt{G\rho_\Lambda}$ makes every $\pi$, the 32 and the 3 cancel, and
$g_{\rm obs}^2-g_{\rm bar}^2=a_0g_{\rm bar}$ is an exact identity.
**RAR fit: 0.108 dex on SPARC** at Υ = 0.70 — the anchored a₀ costs *nothing* against a fitted one
(anchoring is cost-free, not "better"; both are indistinguishable after Υ-refit). κ is **measured**:
0.551 ± 0.043 distance-free, 0.465 ± 0.076 from the BTFR.
[`prep_2026/a0_line/`](prep_2026/a0_line/) · paper [THE_COSMOLOGICAL_CONSTANT_SETS_A0.md](opus_48_extended_research/papers/THE_COSMOLOGICAL_CONSTANT_SETS_A0.md)

### 2 · The field theory — THE COMPLETION (v9)
The full action, the pressure promotion, the derived a₀(z), and the no-ghost/c_T = 1 health
results — with the non-claims led by "κ = ½ NOT DERIVED".
Verified (all script-backed): CLASS CMB pass (0.01σ vs cosmic variance) · lensing 21.2σ → 0.6σ with
γ_PPN = 1 · c_T = 1 exact · no-ghost theorem · RAR 0.108 dex · BTFR · solar system ·
**pure-framework weak-lensing RAR 40 kpc–2.2 Mpc, χ²/dof = 2.03 canonical / 0.94 alt, no dark
component** (real KiDS data, and the same fit *rejects* adding one).
Honest limits: **dark matter exists at full Ω_dm, and as of 2026-09-02 it is cold** — the condensate's
own equation of state, read on the cosmic background, excludes the single-field dark sector and closes
every kinetic mechanism for keeping it out of galaxies (see the rev. 6 block above). The action, the
promotion, the switch-off law and the health results stand; the "dust job" does not.
**Paper: [THE_COMPLETION.md](opus_48_extended_research/papers/THE_COMPLETION.md) · v9 DOI [10.5281/zenodo.21895046](https://doi.org/10.5281/zenodo.21895046)** (concept [21863521](https://doi.org/10.5281/zenodo.21863521)) · plain-language companion [10.5281/zenodo.21865866](https://doi.org/10.5281/zenodo.21865866) · evidence: [`nbody_2026/`](nbody_2026/), every stage green.

### 3 · Pinning AeST's free parameter — the 𝒬₀ pin
AeST's authors state the dark-sector density is "not (classically) predicted"; its published fits
span four orders of magnitude in 𝒬₀. Three framework commitments collapse that freedom to one
parameter, and galaxy-scale phenomenology fixes it: **𝒬₀ ≈ 2.4×10⁻³–1.5×10⁻² Mpc⁻¹** — with the
corroboration that both MOND-compatible published CMB fits land inside the band and the
MOND-incompatible one lands outside, though no CMB information entered the derivation. The pin is
**a₀-free in observables** (the local-a₀ challenge was raised by the author and adjudicated in the
open), and it survived its strongest internal test: a candidate transport mechanism that would have
drained the halo turns out to be inconsistent with the pin that calibrates it — a fixed-point
result that closed a door and defended the pin in the same move.
**Paper: [PINNING_Q0_IN_AEST.md](opus_48_extended_research/papers/PINNING_Q0_IN_AEST.md) · v4 DOI [10.5281/zenodo.21937958](https://doi.org/10.5281/zenodo.21937958)** (concept [21935942](https://doi.org/10.5281/zenodo.21935942)) · scripts: [`nbody_2026/`](nbody_2026/) stages 56–63.

### 4 · Wide binaries — the sharpest live front
[`prep_2026/gaia_dr4_prep/`](prep_2026/gaia_dr4_prep/) — **frozen, hash-stamped pre-registration**,
ten amendments, all filed *before* data. **In force (Amendment 10): γ_v = 1.1614–1.1814 canonical /
1.1917–1.2267 alt**, no-verdict edge 1.23, built on the full nonlinear AQUAL-EFE solve (the
registered point-response number was killed by its own solve — largest eigenvalue declared
isotropic — and replaced by a computed band, in the open, before data). **Clock: Gaia DR4,
~Dec 2026.** Newest (2026-08-14): the EFE-present *exact two-body* solve shows the band top is
conservative **and** a sub-band reading is more likely — both directions stated; and under the
framework's own local-a₀ structure DR4 doubles as a *conditional* charge meter.
**New note: [DR4_TARGET_UNDER_LOCAL_A0.md](opus_48_extended_research/papers/DR4_TARGET_UNDER_LOCAL_A0.md) · DOI [10.5281/zenodo.21937976](https://doi.org/10.5281/zenodo.21937976).**
⚠️ The literature disagrees violently on this quantity — Banik+24 reports 19σ Newtonian; Chae 2023
reports γ = 1.43 ± 0.06 — which is why the systematic budget is split one-sided.

### 5 · The BTFR discriminator and a₀(z) fronts
The derived a₀(z) law predicts **<2×10⁻⁴ dex** of BTFR zero-point evolution at z ≤ 5 (flat below
z_t) — so the observed 1 < z < 5 null is a *prediction*, while the naive a₀ ∝ cH(z) reading is
disfavoured ~2.3σ with two wrong-sign tests. Pre-stated falsification bars: **0.15 dex** (HI,
gas-dominated, z ≤ 1) / **0.33** ([CII], z ~ 2–5) / **0.44** (stellar); SKA-mid/ngVLA reach
decisive power. Any robust a₀ evolution below z ~ 5 falsifies the law — either sign.
[`nbody_2026/stage60_btfr_discriminator_2026.py`](nbody_2026/stage60_btfr_discriminator_2026.py) · cross-scale: [`prep_2026/a0z_crossscale/`](prep_2026/a0z_crossscale/)
**Framework vs ΛCDM (2026-09-01):** ΛCDM's RAR scale is emergent from halo structure and rises ×1.8 by z = 2; added as a fourth zero-parameter law to the joint likelihood over the 10 committed high-z constraints it is **undecided and prior-dominated** (the sign flips with the drift ceiling; Ciocan carries every face-value verdict). The decisive measurement is the **deep-MOND BTFR zero-point at z ≈ 2.5: framework 0.00 dex, ΛCDM-native +0.33 dex, one clean point at ±0.13 dex decides at 20:1** — a JWST/ALMA target, not a survey. To mimic a flat a₀, ΛCDM's haloes would have to be diluted to 0.61 (z = 2) / 0.40 (z = 3) of their N-body concentrations. [`a0z_lcdm_native_hypothesis_2026.py`](prep_2026/a0z_crossscale/a0z_lcdm_native_hypothesis_2026.py) · [`real_research/crispy_2026/`](real_research/crispy_2026/)

### 6 · Structural theorems (MI era, kept for the record)
Seven machine-verified results on the closed modified-inertia arm; five are prohibitions.
**Paper: [MI_STRUCTURAL_THEOREMS.md](opus_48_extended_research/papers/MI_STRUCTURAL_THEOREMS.md) · DOI [10.5281/zenodo.21708842](https://doi.org/10.5281/zenodo.21708842)** — the worldline
test-particle theory survives as mathematics; the arm is closed as physics.

### 7 · Nulls, published as nulls — **the part most worth reading**
- [`project_atomos/`](project_atomos/) — exhaustive Standard-Model parameter search, **null**, DOI [10.5281/zenodo.21654272](https://doi.org/10.5281/zenodo.21654272), published *after* an audit withdrew two of its own claims
- **Z carries no geometry:** at the real ±16% precision **9,912** expressions match a₀; $Z=\sqrt{8\pi/3}/\kappa$ carries exactly one bit beyond κ — [`reviews/z_numerology_density_2026.py`](reviews/z_numerology_density_2026.py)
- κ-forcing closed: [KAPPA_ONE_PARAMETER_GEOMETRY.md](opus_48_extended_research/papers/KAPPA_ONE_PARAMETER_GEOMETRY.md) · [THE_SEARCH_WAS_NEVER_WASTED.md](opus_48_extended_research/papers/THE_SEARCH_WAS_NEVER_WASTED.md)

---

## Working rules

Enforced by the scripts, not by trust.

1. **Test the framework on its own terms** — modified gravity (since 2026-08-08), horizon-derived a₀, its own interpolation. Never through the standard-MOND lens.
2. **Verify a deficit as rigorously as a win.** Manufacture neither.
3. **Both a₀ footings on every dimensional number** — canonical ρ_DE (9.36×10⁻¹¹), alternative ρ_total (1.13×10⁻¹⁰) — and show the spread.
4. **Every load-bearing claim gets a committed, runnable script** that exits non-zero on a failed internal check. No hard-coded verdicts.
5. **Never say "the theory is closed."**
6. **Amend frozen pre-registrations in the open, before data.**
7. **Adversarial refereeing before commit** — findings land only after an independent attempt to refute them, and refuted drafts are withdrawn with banners, not silent edits.
8. **Cite or flag** — any number not traced to a script or a cited paper is marked unverified.
9. **Nothing personal in this repository.**

---

## Publication record

[![Crispy Fried Chicken Matching Theorem](https://img.shields.io/badge/Crispy%20Fried%20Chicken%20Matching%20Theorem%20(Sep%202%202026)-10.5281%2Fzenodo.22261001-red)](https://doi.org/10.5281/zenodo.22261001)
[![Nonlocal MOND Kernel Instability v2](https://img.shields.io/badge/Nonlocal%20MOND%20Kernel%20Instability%20(v2%2C%20Sep%202026)-10.5281%2Fzenodo.22255522-red)](https://doi.org/10.5281/zenodo.22255522)
[![Cluster Phase Pinning v2](https://img.shields.io/badge/Cluster%20Phase%20Pinning%20Polytrope%20(v2%2C%20Sep%202026%20%E2%80%94%20cosmology%20withdrawn)-10.5281%2Fzenodo.22254075-orange)](https://doi.org/10.5281/zenodo.22254075)
[![THE COMPLETION v9](https://img.shields.io/badge/THE%20COMPLETION%20v9%20(dark%20sector%20excluded%20Sep%202026)-10.5281%2Fzenodo.21895046-red)](https://doi.org/10.5281/zenodo.21895046)
[![Q0 Pin v4](https://img.shields.io/badge/Pinning%20AeST's%20Q0%20(v4%2C%20Aug%2014%202026)-10.5281%2Fzenodo.21937958-red)](https://doi.org/10.5281/zenodo.21937958)
[![DR4 under local a0](https://img.shields.io/badge/DR4%20Target%20under%20Local%20a0%20(Aug%2014%202026)-10.5281%2Fzenodo.21937976-red)](https://doi.org/10.5281/zenodo.21937976)
[![DR4 Pre-registration](https://img.shields.io/badge/Gaia%20DR4%20Pre--registration-10.5281%2Fzenodo.21702746-black)](https://doi.org/10.5281/zenodo.21702746)
[![MI Structural Theorems](https://img.shields.io/badge/MI%20Structural%20Theorems%20(v2)-10.5281%2Fzenodo.21708842-blueviolet)](https://doi.org/10.5281/zenodo.21708842)
[![Atomos Null](https://img.shields.io/badge/Atomos%20SM%20Search%20%E2%80%94%20NULL%20(v2)-10.5281%2Fzenodo.21654272-lightgrey)](https://doi.org/10.5281/zenodo.21654272)
[![License](https://img.shields.io/badge/code-AGPL--3.0-lightgrey)](LICENSE)
[![Content License](https://img.shields.io/badge/content-CC--BY--4.0-lightgrey)](LICENSE.md)

<details><summary>Full chronological badge wall (2026 record)</summary>

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

</details>

---

## Citation and licence

Cite the repository via [CITATION.cff](CITATION.cff) (GitHub's "Cite this repository" button), or
cite individual papers by their Zenodo DOIs above.

**Code: [AGPL-3.0](LICENSE). Prose, papers, figures, and scientific content: CC-BY-4.0.**
Details: [LICENSE.md](LICENSE.md). Author: Carl P. Zimmerman (Briar Creek Tech),
ORCID [0009-0008-3508-7982](https://orcid.org/0009-0008-3508-7982).
