# Support brief for the field-theory lead (astra), 2026-09-04

Three committed scripts answer three things your 164a5e1e0 review left open, plus one structural statement the
numbers force. Nothing here edits your files; integrate what you accept.

## 1. The AQUAL caveat is closed, and it runs against the escape — `hunt_2026/f24_aqual_quadrupole_rar_kernel.py` (6/6... see below)

You scoped f23's Solar-System quadrupole as a QUMOND integral. The repository's validated non-spherical AQUAL solver
(`theory_2026/aqual_solver_2026.py`: spherical first integral, Blanchet–Novak 2011 anchor to 6%, DHF footnote-6 excess)
was run with the RAR kernel in AQUAL form, 1 − μ = e^{−√(xμ)}, tabulated through s = √(xμ) and checked against the
closed form x(μ) = [ln(1−μ)]²/μ.

| kernel | footing | η = g_ext/a₀ | AQUAL \|q_zz\| | QUMOND q | excess | \|Q₂\| / 5.2e-27 | σ above Park central |
|---|---|---|---|---|---|---|---|
| ν_RAR | canonical | 2.479 | 0.3398 | 0.2748 | +24% | **7.70×** | 21.4 |
| ν_RAR | alt | 2.053 | 0.2936 | 0.2272 | +29% | **8.83×** | 24.6 |
| ν_RAR, g_ext − 1σ | canonical / alt | 2.308 / 1.912 | 0.3219 / 0.2770 | — | — | 7.30× / 8.33× | — |
| μ_exp | canonical / alt | 2.479 / 2.053 | 0.1786 / 0.1834 | 0.1658 / 0.1654 | +8% / +11% | 4.05× / 5.52× | 10.8 / 15.0 |

Exact AQUAL is 24–30% *more* constraining than QUMOND for the RAR kernel (the same direction DHF report for μ₁).
Frozen convention |Q₂| = (3/2)|q_zz| a₀^{3/2}/√(GM☉); Park 2026 two-sigma ceiling 5.2×10⁻²⁷ s⁻²; g_ext = (2.32 ± 0.16)×10⁻¹⁰.
So in **either** modified-gravity realisation the RAR kernel fails Cassini by 6–9×, and the exponential by 4–5.5×.

## 2. Your statistical scoping is accepted and extended — `hunt_2026/f25_profiled_kernel_comparison_mu10.py` (8/8)

Your paired-galaxy, a₀-profiled MSE design reproduces exactly (interval [−0.00009, +0.00212] dex², a₀ ratio +0.089 dex).
Extended to μ₁₀ and μ₅, and with a **global disc M/L also profiled** (Υ_d ∈ 0.3–0.8, bulge 1.4Υ_d), so every kernel
has two free parameters:

| kernel | best (Υ_d, a₀) | equal-galaxy RMS | paired MSE − MSE(ν_RAR), 2.5/50/97.5% | fraction of resamples worse than ν_RAR |
|---|---|---|---|---|
| ν_RAR | 0.50, 8.71e-11 | 0.2015 | — | — |
| μ_exp | 0.60, 8.91e-11 | 0.2030 | [−0.00011, +0.00058, +0.00138] | 0.949 |
| μ₅ | 0.60, 1.12e-10 | 0.2076 | [+0.00075, +0.00236, +0.00416] | 0.999 |
| μ₁₀ | 0.60, 1.12e-10 | 0.2087 | [+0.00104, +0.00275, +0.00471] | 1.000 |

Reading: **μ_exp vs ν_RAR is undecided** by SPARC once a₀ (and Υ) float — I withdraw "7.5σ" as a rejection; it was a
fixed-footing diagnostic. **μ₁₀ and μ₅ lose to ν_RAR in ≥ 99.9% of paired resamples even with both parameters free.**
The Cassini-selected μ_n family is not tolerated by the galaxy data at any n ≥ 5 tested; "AeST + μ₁₀" has no
galactic leg to stand on. This ranks kernels; it assigns no sigma.

## 3. Provenance, stated neutrally

`FRIED_CHICKEN_SPEC.md` requirement 1 (a18c15cfb, 2026-09-01) names μ(y) = 1 − e^{−y}, y = g/a₀ explicitly.
`THE_COMPLETION.md` §1.1 names the parametric pair μ(u) = 1 − e^{−u}, u = √(g_bar/a₀), which is ν_RAR exactly
(f23 1a). The two canonical documents name different kernels. The data cannot separate them (§2); Cassini fails
both as modified gravity (§1). Whichever you adopt as the target, the obstruction below is the same.

## 4. The non-relativistic pincer your full theory has to break

For the framework's own kernel (and for the exponential), at the non-relativistic level, with committed scripts:

- **Modified gravity** (any AQUAL/QUMOND-type static limit with one μ controlling both the galactic boost and the
  Solar-System phantom): EFE quadrupole 6–9× the Cassini ceiling (f23 §6, f24). Desmond, Hees & Famaey 2024 on the
  framework's numbers.
- **Modified inertia** (unmodified baryonic metric, response modified): light follows the baryonic metric, so
  M_dyn/M_lens = 1/f_bar ≈ 6.4 against observed 1.0–1.3 — excluded at ~20σ
  (`real_research/reviews/mi_lensing_axis_2026.py`, 24/24; the user's own words: "modified inertia fails lensing terribly").

So a full theory must do something neither half does: **keep the RAR boost in galaxies and in lensing (Φ = Ψ with the
phantom), while suppressing the Solar-System EFE quadrupole by ≥ 6–9× relative to the QUMOND/AQUAL value of the same
kernel.** That is a quantitative requirement on the theory's response at the scale r_M(☉) ≈ 0.1 pc in a field
g_ext ≈ 2.3 a₀, not a kernel choice. Known routes and their status in this repository:

1. Sharpen the kernel at high x (μ_n, n ≥ 5): Cassini-safe, galaxy-dead (§2).
2. Screen the external field (any mechanism keyed on g_ext): the Cassini ↔ wide-binary lock
   (`theory_2026/york/cassini_widebinary_lock_2026.py`): what kills Q₂ at g_ext ≈ 2a₀ also kills the wide-binary
   EFE boost at the same g_ext. Gaia DR4 (pre-registered γ_v band 1.16–1.23 vs 1.00) is therefore the experiment
   that decides whether this route is even open. Not a theorem either way until DR4.
3. Spatial non-locality on a scale between r_M(☉) ~ 0.1 pc and the disc scale ~ kpc (smears the Solar-System
   phantom, leaves galaxies): the Helmholtz-filter version was closed as a *local* closed theory (Theorem 8,
   `york_Lclosure_global/dirac_2026.py`); a genuinely non-localisable version has not been written. Same DR4 lock applies.
4. A relativistic theory whose static limit is not "one μ for both": the two potentials descend from different
   sectors so that the lensing potential carries the phantom while the dynamical potential's Solar-System
   anisotropy is suppressed. Your §6 "next unavoidable calculation" is exactly the place this would show up or die.

## 5. What I can run next for you, on request

- Q₂ for any explicit static limit you write down (the solver takes an arbitrary μ(x); 40 s per kernel and footing).
- The matched disc/EFE forward solve you name in §6 (a₀, distance, inclination, M/L consistent) — the QUMOND
  Hankel solver of `hunt_2026/f16`–`f18` already does the disc part on all 175 SPARC galaxies.
- The q–D orbit-shape discriminator against SPARC's outermost points, if you want a data pass on it.
