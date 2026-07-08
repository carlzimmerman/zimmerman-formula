# A Written de Sitter–Unruh Modified-Inertia Action (v3)

## The frame field is passive, the covariant theory is causal and ghost-free at two-point and Cassini-safe, the Einstein-aether strong-coupling wall is mis-applied, and gravitational lensing is viable but tuned

**Carl P. Zimmerman** · Briar Creek Tech · 2026-07-08 (v3)

---

### Abstract

The de Sitter–Unruh reading of the MOND acceleration scale, a₀ = cH_Λ/Z = c²√(Λ/32π) = 9.36×10⁻¹¹ m s⁻², posits that the scale is a modified-**inertia** effect of the cosmic (dark-energy) horizon rather than a modification of gravity. This paper writes the explicit nonlocal modified-inertia action and carries its covariant analysis to a definite boundary, reasoning throughout from the framework's own premises (a passive frame, with the MOND in the matter sector) rather than the standard aether/MOND lens. Results, each with reproducible verification (both a₀ footings): **(1)** the **worldline/matter sector is machine-verified** (ν(y)=√(1+1/y) to 3×10⁻¹³, Newton, deep-MOND, baryonic Tully–Fisher, the dS-Unruh-forced √2-DC-weight external-field kernel, exact ghost-freedom). **(2)** The modified-**inertia** realization **evades the Cassini quadrupole** by ~7 orders (deep-Newtonian ν−1≈7×10⁻⁷), where the modified-gravity realization fails at +6 to +14σ. **(3)** Promoting the frame field covariantly, **MOND does not force modified gravity** — the matter source is l=0 (soaked by the unit-timelike multiplier), evading the Bianchi shear lock. **(4)** The mixed matter–aether **two-point propagator is causal and ghost-free in closed form** (retarded construction; Källén–Lehmann spectral positivity across the whole cut; principal symbol = the GR light-cone). **(5, correcting v2)** The Einstein-aether **strong-coupling wall does *not* wall the framework**: that wall is a property of a *propagating* aether mode whose kinetic norm vanishes, but the framework's frame is **passive** (its own theory: an algebraic constitutive law, an SME background, the cosmic rest frame), with zero propagating aether modes — so the wall's object is undefined for it. The wall binds only the rejected AeST/khronon *modified-gravity* limb. **(6)** Gravitational **lensing is viable but fine-tuned**: light is massless, so lensing must come from the ghost-condensate dark sector, which reproduces the observed lensing=dynamics relation only if placed by hand to equal the MI dynamical excess (per-galaxy) — not excluded, not predicted. **Open:** an all-orders certifying well-posedness theorem for the non-entire branch-cut class, the interacting four-point vertex, and a first-principles condensate profile law. The MOND sign remains a **postulate** and a₀'s value is underived. An effective one-scale completion carried to a sharp, named boundary — **not a finished theory and not a theory of everything.**

### 1. Setting and scope

The framework reads a₀ as the acceleration at which a body's inertial response to the de Sitter vacuum departs from Newtonian, with the Deser–Levin temperature T(a) = (ℏ/2πk_Bc)√(a² + (cH_Λ)²) a horizon floor and the interpolation g_obs = √(g_bar² + g_bar a₀), ν(y)=√(1+1/y). The earlier theory-of-everything and Standard-Model claims were publicly retracted (2026-06-23) and are not reasserted; this is a one-scale effective-theory construction with named inputs, each labeled **derived**, **postulated**, or **open**. Crucially — and this is the correction to v2 — the framework is *modified inertia*: the MOND lives in the **matter** sector, and the frame field u^μ is a **passive**, horizon-anchored reference (the framework's own paper: an *algebraic constitutive law* g_bar=G(a) with no frame equation of motion; an SME gravity-sector *background*; the Cassini-constrained cosmic rest frame). It is **not** AeST/Einstein-aether, where a dynamical aether *carries* the MOND — the theory that fails Cassini.

### 2. The action

With signature (−+++), S[x,g,u] = S_EH[g] + S_u[g,u] + S_matter[x,g,u]: host GR unmodified; a unit-timelike frame constraint S_u = −∫√−g (λ/2)(u^μu_μ+1) (no aether kinetic term); and the modified-inertia content in the matter kinetic sector,
$$S_{\mathrm{matter}} = -\frac{1}{2}\int d^4x\,\sqrt{-g}\,\rho_m\,\big[\,s\,u^\mu\,K(\Box_u/a_0^2)\,u_\mu\,\big],\quad K(z)=\frac{\sqrt{1+4z}-1}{2\sqrt z},\quad \Box_u f = u^a\nabla_a(u^b\nabla_b f).$$
K is non-polynomial with a branch cut and a single healthy pole (residue +1). The equivalent Galley doubled-worldline form uses the conservative gradient G(a)^μ=a^μμ_fw(|a|/a₀), μ_fw the exact inverse of ν(y)=√(1+1/y); the external-field kernel θ(y)=θ₀/(1+(θ₀−1)y²), θ₀=√2, has its shape forced by the de Sitter Wightman function. Here **s=−1 is the MOND-sign postulate**, a₀=cH_Λ/Z=9.36×10⁻¹¹ (canonical), 1.13×10⁻¹⁰ (alternate footing).

### 3. Verified: the worldline sector and the Cassini evasion

Machine-checked, both footings: the circular-orbit reduction reproduces ν(y)=√(1+1/y) to 3.35×10⁻¹³; Newton, deep-MOND, and baryonic Tully–Fisher v⁴=GM a₀ (exact); the form-factor↔RAR identity g_obs=√(g_bar²+g_bar a₀); the √2-DC-weight external-field kernel; and ghost-freedom (single pole +1 vs the Ostrogradsky ghost of the local truncation). **Cassini:** the anisotropic galactic external field (a_ext=2.29 a₀) enters only Saturn's inertial response, deep-Newton-suppressed by ν−1≈7×10⁻⁷; the l=2 quadrupole is ~7.4×10⁻³⁴ s⁻² — ~7 orders below the 5.2×10⁻²⁷ ceiling. The modified-gravity realization instead fails at +6 to +14σ. This is Milgrom's [2009] statement that the inner-solar-system quadrupole is an AQUAL/QUMOND effect absent in modified inertia, realized explicitly.

### 4. The covariant completion, on the framework's own terms

Because the frame is passive and the MOND is in the matter sector, the covariant question is *not* whether a dynamical aether is strongly coupled — it is whether the passive-frame + nonlocal-K matter system is well-posed. Four results:

**(a) MOND does not force modified gravity.** Varying S_matter, the source it adds to u^μ's field equation is J^μ=−ρ_m s k u^μ: l=0, parallel to u^μ, soaked by the multiplier λ. It never populates the l=2 traceless-shear channel whose divergence is the Bianchi lock that forces AeST's Cassini quadrupole. So the covariant lift does not collapse to modified gravity; a passive frame carries at most Q₂^u≲7×10⁻³⁵ s⁻² over an open, ghost-free region.

**(b) The mixed two-point propagator is causal and ghost-free in closed form.** The dynamical-u variation resums to Q(z)=K+2zK′=2√z/√(1+4z); the retarded memory kernel has strictly causal support (an advanced control correctly flips it), Titchmarsh UHP-analyticity holds, and Källén–Lehmann spectral positivity ρ(s)≥0 across the whole cut is verified in closed form (a control correctly flags a known Ostrogradsky ghost as ρ<0). The branch cut is a healthy radiation continuum, not a ghost.

**(c) The principal symbol is the GR light-cone**, D(w)/w = 1 + i a₀/2w − a₀²/8w² + …, the nonlocal correction O(a₀/w) UV-subdominant and IR-gapped — hyperbolic, no secular runaway. So the passive-frame theory is **principal-symbol-well-posed**.

**(d) The Einstein-aether strong-coupling wall is mis-applied (correcting v2).** That wall is, by construction, a property of a *propagating* aether/khronon mode whose canonical kinetic norm vanishes (M_sc∼√N M_Pl; the mode speeds carry the vanishing norm in the denominator) [Blas–Pujolàs–Sibiryakov 2009; Gong et al. 2018]. The framework's frame is passive — zero such modes — so the wall's central object is *undefined*, not violated. It binds only the rejected AeST/khronon modified-gravity limb (which fails Cassini at +6–14σ). v2's "the covariant route is walled by strong coupling" applied that dynamical-aether wall to the passive-frame realization and is hereby corrected.

**What is open.** There is no off-the-shelf *certifying* all-orders well-posedness theorem for the non-entire branch-cut (Källén–Lehmann/Herglotz) class — positivity + analyticity are passed checks, not a theorem (the proven literature covers only *entire* form factors). And the interacting four-point vertex plus nonlinear back-reaction (Box_u is built from u, so "linear on a fixed passive-u background" is the controlled slice) is not closed in one pass.

### 5. Gravitational lensing: viable but fine-tuned

In modified inertia the modification is to how massive bodies respond; **light is massless and has no inertia to modify**, so photons follow GR null geodesics of real mass — baryons plus the ghost-condensate dark sector. The observed weak-lensing RAR matches the dynamical RAR [Brouwer et al. 2021; Mistele & McGaugh 2024], which *requires* the condensate to supply exactly the MI dynamical excess, M_cond(r)=M_bar(ν(y)−1). Nothing in the framework forces this: the condensate amount is a free shift-charge integration constant (dI₀/da₀=0), and generic clustering profiles miss the required shape by 0.12–0.55 dex — only a hand-placed profile matches. Worse, a fixed cosmic I₀ gives a constant M_cond/M_bar while the MI excess runs as √M_bar across the galaxy population, so the tuning is *per-galaxy*. This is **not a tension** (M_cond=M_bar(ν−1) is positive-density, monotonic, and realizable — the framework is not excluded) and **not a prediction** (it is a fit). Verdict: viable but fine-tuned, the location of generic two-sector dark theories. The genuinely distinctive modified-inertia signature lives in the *dynamical* sector (the MG-impossible non-adiabatic velocity-dispersion hysteresis), not in lensing.

### 6. Honest standing

Reasoning from the framework's own passive-frame, MOND-in-matter premise: the worldline sector is written and verified; the modified-inertia realization evades Cassini; MOND does not force modified gravity; the mixed two-point propagator is causal, ghost-free (Källén–Lehmann), and principal-symbol-well-posed; and the Einstein-aether strong-coupling wall is a mis-application that does not bind the framework (it binds only the rejected modified-gravity limb). Gravitational lensing is viable but fine-tuned (per-galaxy), not solved and not a kill. The completion is therefore **not** the modified-gravity limb (Cassini-failing) and **not yet** a finished field theory — it is a well-posed worldline theory whose passive-frame covariantization is causal, ghost-free at two-point, and principal-symbol-well-posed, with three honest open edges: a certifying all-orders theorem for the non-entire branch-cut class, the interacting four-point vertex, and a first-principles ghost-condensate profile law. The MOND sign stays postulated and a₀'s value underived. No completeness or theory-of-everything claim is made.

### 7. Related work

The construction sits between the relativistic modified-gravity realizations of MOND — AeST [Skordis & Złośnik 2021], the Blanchet–Skordis khronon [2025], the nonlocal mimetic model of Deffayet & Woodard [2026] — and the modified-inertia program of Milgrom [1999, 2009]. The covariant frame sector is Einstein-aether [Jacobson & Mattingly 2001], its PPN structure [Foster & Jacobson 2006], its GW170817 constraint [Gong et al. 2018], and its strong-coupling corner [Blas, Pujolàs & Sibiryakov 2009]; the nonlocal well-posedness class is Källén–Lehmann/Herglotz–Nevanlinna (passive-causal), distinct from the entire-function class [Biswas et al.; Barnaby & Kamran]. The doubled-worldline formalism is Galley [2013]; the lensing constraint is Brouwer et al. [2021] and Mistele & McGaugh [2024].

### 8. Reproducibility

Committed scripts (repository `real_research/reviews/`): the worldline sector and Cassini evasion (`cassini_mi_evasion_2026/`); the covariant kinetic wins (`mi_kinetic_completion_2026/`); the mixed-propagator causality + Källén–Lehmann positivity (`mi_propagator_2026/`); the framework-first correction of the strong-coupling wall (`mi_strongcoupling_framework_2026/`); the all-orders Cauchy checks (`mi_cauchy_wellposed_2026/`); and the lensing fine-tuning analysis (`mi_lensing_2026/`). Sign-wall inputs: `ACTIVE_KERNEL_SIGNTHEOREM_2026-06.md`, `FOURTH_ORDER_SIGN_WALL_2026-07.md`; trichotomy: `COVARIANT_MI_COMPLETION_2026-06.md`.

### References

1. M. Milgrom, Phys. Lett. A **253**, 273 (1999); MNRAS **399**, 474 (2009).
2. S. Deser & O. Levin, Class. Quantum Grav. **14**, L163 (1997).
3. T. Jacobson & D. Mattingly, Phys. Rev. D **64**, 024028 (2001); B. Z. Foster & T. Jacobson, Phys. Rev. D **73**, 064015 (2006), gr-qc/0509083.
4. D. Blas, O. Pujolàs & S. Sibiryakov, JHEP **10**, 029 (2009), arXiv:0906.3046.
5. C. Skordis & T. Złośnik, Phys. Rev. Lett. **127**, 161302 (2021); L. Blanchet & C. Skordis, arXiv:2507.00912 (2025).
6. C. Deffayet & R. P. Woodard, JCAP **04**, 081 (2026), arXiv:2512.10513.
7. Y. Gong, S. Hou, D. Liang & E. Papantonopoulos, Phys. Rev. D **97**, 124023 (2018), arXiv:1802.04303.
8. R. S. Park et al., arXiv:2602.17884 (2026); DESI Collaboration, arXiv:2503.14738 (2025).
9. N. Barnaby & N. Kamran, JHEP **02**, 008 (2008); T. Biswas et al., JHEP **10**, 054 (2010).
10. M. Brouwer et al., A&A **650**, A113 (2021), arXiv:2106.11677; T. Mistele & S. McGaugh, arXiv:2310.15248 (2024).
11. C. R. Galley, Phys. Rev. Lett. **110**, 174301 (2013).
12. Companion (this program): sign wall, Zenodo 10.5281/zenodo.21184373; covariant-MI quadrichotomy, 10.5281/zenodo.21148494; written MI action v1/v2, 10.5281/zenodo.21253645 / 21260830.

*Both a₀ footings throughout. Each claim labeled derived / postulated / open; the MOND sign is a postulate; the Einstein-aether wall is corrected as a mis-application; lensing is viable-but-tuned. No completeness or theory-of-everything claim.*
