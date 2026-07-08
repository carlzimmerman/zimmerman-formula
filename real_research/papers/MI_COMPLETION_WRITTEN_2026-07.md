# A Written de Sitter–Unruh Modified-Inertia Action (v2)

## The worldline sector verified, the Cassini quadrupole evaded, MOND shown not to force modified gravity — and the natural covariant (Einstein-aether) completion walled by strong coupling at the GW170817 corner

**Carl P. Zimmerman** · Briar Creek Tech · 2026-07-08 (v2)

---

### Abstract

The de Sitter–Unruh reading of the MOND acceleration scale, a₀ = cH_Λ/Z = c²√(Λ/32π) = 9.36×10⁻¹¹ m s⁻², posits that the scale is a modified-**inertia** effect of the cosmic (dark-energy) horizon rather than a modification of gravity. Prior work characterized the *obstructions* to a covariant completion — a trichotomy (local → Ostrogradsky ghost; field → modified gravity failing Cassini; nonlocal → the only ghost-free horn) and an all-orders sign wall (a passive, unitary de Sitter bath sources the *anti*-MOND sign). This paper writes the **constructive** counterpart — an explicit nonlocal modified-inertia action — and carries its covariant analysis to a definite boundary. Four results are established, each with reproducible verification (both a₀ footings): **(1)** the **worldline / matter sector is written and machine-verified** (ν(y)=√(1+1/y) to 3×10⁻¹³, Newton, deep-MOND, baryonic Tully–Fisher, the external-field kernel with a dS-Unruh-forced √2 DC weight, exact ghost-freedom, conservativeness); **(2)** the modified-**inertia** realization **evades the Cassini quadrupole bound** by ~7 orders of magnitude (deep-Newtonian ν−1 ≈ 7×10⁻⁷ suppression), where the modified-gravity realization fails it at +6 to +14σ; **(3)** promoting the frame field to a covariant Einstein-aether field, **MOND does not force modified gravity** — the matter source is l=0 (parallel to the frame field, soaked by the unit-timelike multiplier), evading the Bianchi l=2 shear lock that kills the modified-gravity limb, and the Cassini-inert corner is a genuinely *open* region; **(4)** the mixed matter–aether **two-point propagator is ghost-free in closed form** (an all-orders resummation, single healthy pole), with no resonant un-suppression of the Cassini residual. The completion is nonetheless **not** a finished field theory along this route: the observationally-required corner — GW170817 (c₁₃ ≲ 10⁻¹⁵) intersected with the preferred-frame safety the inertia-evasion needs (α₁=α₂=0) — is the c₁₃=c₁₄=0 double-null where the Einstein-aether kinetic norms vanish, a **strong-coupling / ill-posed point**; the linear analysis loses control there and the nonlinear strong-coupling window (M_sc ~ 10¹¹ GeV, *not excluded* but undemonstrated) is the open question. The MOND sign remains a **postulate** (walled all-orders) and a₀'s value is underived. This is an effective completion carried to a sharp boundary — **not a finished theory and not a theory of everything.**

---

### 1. Setting and scope

The framework reads a₀ as the acceleration at which a body's inertial response to the de Sitter vacuum departs from the Newtonian value, with the Deser–Levin temperature T(a) = (ℏ/2πk_Bc)√(a² + (cH_Λ)²) a horizon floor and the interpolation g_obs = √(g_bar² + g_bar a₀), ν(y)=√(1+1/y), y=g_bar/a₀.

Two facts set the task. A covariant **modified-gravity** realization of this scale (AeST [Skordis–Złośnik 2021], the Blanchet–Skordis khronon [2025]) inherits a solar-system quadrupole tension with the improved Cassini bound Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻² [Park et al. 2026] at +6 to +14σ for the framework's own slow interpolation. A modified-**inertia** realization instead evades that bound (§3), because in modified inertia the Sun's field stays Newtonian — no phantom-density quadrupole. The inertia realization is therefore the one to write down; this paper writes its worldline sector and then tests whether it lifts to a well-posed covariant field theory. The framework's earlier theory-of-everything and Standard-Model claims were publicly retracted (2026-06-23) and are not reasserted; what follows is a one-scale effective-theory construction with named inputs, each labeled **derived**, **postulated**, or **open**.

### 2. The action

With signature (−+++) and c restored, S[x,g,u] = S_EH[g] + S_u[g,u] + S_matter[x,g,u]:

- **Host gravity, unmodified:** S_EH = (1/16πG)∫d⁴x √−g (R − 2Λ).
- **Frame constraint** — a unit-timelike clock uᵘ with a Lagrange multiplier, and *(in the worldline sector)* no Maxwell-type kinetic term: S_u = −∫d⁴x √−g (λ/2)(uᵘu_μ + 1).
- **Modified-inertia content**, in the matter kinetic sector, ρ_m-weighted and gated by a nonlocal branch-cut form factor:
$$S_{\mathrm{matter}} = -\frac{1}{2}\int d^4x\,\sqrt{-g}\,\rho_m\,\big[\,s\,u^\mu\,K(\Box_u/a_0^2)\,u_\mu\,\big],\quad K(z)=\frac{\sqrt{1+4z}-1}{2\sqrt z},\quad \Box_u f = u^a\nabla_a(u^b\nabla_b f).$$

K is non-polynomial with a branch cut and a single healthy pole (residue +1); this nonlocality is the ghost-free horn of the trichotomy. The equivalent Galley doubled-worldline form uses the conservative gradient G(a)ᵘ = aᵘμ_fw(|a|/a₀), μ_fw the exact inverse of ν(y)=√(1+1/y). The external-field kernel θ(y)=θ₀/(1+(θ₀−1)y²), θ₀=√2, has its Lorentzian form-class and √2 DC weight forced by the de Sitter worldline Wightman function W(u) ∝ −1/sinh²(κ(u−iε)/2). Here **s = −1 is the MOND-sign postulate**, a₀ = cH_Λ/Z = 9.36×10⁻¹¹ m s⁻² (canonical, ρ_DE, Z=√(32π/3)), alternate footing 1.13×10⁻¹⁰ (ρ_total).

### 3. Verified: the worldline sector, and the Cassini evasion

Machine-checked, both footings (§8): (i) the circular-orbit reduction μ_fw(a/a₀)a=g_N reproduces ν(y)=√(1+1/y) to 3.35×10⁻¹³; (ii) Newton and deep-MOND limits; (iii) baryonic Tully–Fisher v⁴=GM a₀ (exact); (iv) the identity inverting Y=μ_fw(X)X → X=√(Y²+Y), i.e. g_obs=√(g_bar²+g_bar a₀); (v) the external-field kernel with the √2 DC weight; (vi) **ghost-freedom** — K(z) has a single pole (residue +1), the local truncation an Ostrogradsky ghost (residue −1); (vii) conservativeness.

**The Cassini evasion.** In modified inertia the Sun's field stays Newtonian; the anisotropic galactic external field (a_ext = 2.29 a₀) enters only Saturn's inertial response, deep-Newtonian-suppressed by ν−1 = a₀/2a ≈ 7×10⁻⁷ at Saturn (y = 7×10⁵). A Legendre decomposition gives an l=1 dipole ~1.5×10⁻²⁸ s⁻² (first order in a_ext) and the l=2 quadrupole ~7.4×10⁻³⁴ s⁻² (second order) — the latter, which Cassini constrains, ~7 orders below the 5.2×10⁻²⁷ ceiling. The modified-gravity realization, whose MOND is carried *by* the aether twist, instead fails at +6 to +14σ. This is the derived realization of Milgrom's [2009] statement that the inner-solar-system Q₂ anomaly is an AQUAL/QUMOND (modified-gravity) effect absent in modified inertia.

### 4. The covariant completion: two wins and a wall

We promote uᵘ to a covariant Einstein-aether field with the general two-derivative kinetic term L_kin = −M²[c₁(∇u)² + c₂(∇·u)² + c₃∇_μu_ν∇ᵛuᵘ + c₄a²] [Jacobson–Mattingly 2001], and test whether the completion is a well-posed field theory.

**Win 1 — MOND does not force modified gravity.** Varying S_matter, the source it adds to uᵘ's field equation is Jᵘ = −ρ_m s k uᵘ: **l=0, parallel to uᵘ**, soaked entirely by the unit-timelike multiplier λ. It does not populate the l=2 traceless-shear channel whose nonzero divergence (∇·shear = (2/3)∇∇²f, sympy-exact) is the Bianchi lock that forces AeST's Φ-sourcing pressure and its Cassini quadrupole. The framework's MOND, living in S_matter, evades that lock. A plain inert aether carries at most Q₂ᵘ ≲ 7×10⁻³⁵ s⁻² (both footings), ~8 orders under the bound, over a genuinely **open, ghost-free, no-Cherenkov region** of (c₁,c₃) — not a measure-zero tuning. So the covariant lift does **not** collapse to modified gravity.

**Win 2 — the mixed propagator is ghost-free in closed form.** Varying the *fully nonlocal* K with uᵘ dynamical (uᵘ inside □_u) generates an infinite higher-derivative source tower that **resums**: Q(z) = K + 2zK′ = 2√z/√(1+4z). The mixed matter–aether two-point propagator has a single +1 (healthy) pole, Re Σ = 0 on-band, and the branch cut is a radiation continuum, not a pole. This is all-orders — verified against the closed-form resummation, not a truncation — and the dynamical-u coupling does **not** resonantly un-suppress the (ν−1)²-suppressed Cassini residual.

**The wall — strong coupling at the observationally-required corner.** Every ghost-free / hyperbolic / no-Cherenkov certification above was obtained at c₁₃ = c₁+c₃ = 0.787 — a point where the spin-2 graviton travels at 2.17c, **excluded by GW170817 by ~15 orders** (|c₁₃| ≲ 10⁻¹⁵ [Gong et al. 2018]). On the framework's own corner, c₁₄ ∝ c₁₃, and the preferred-frame safety the inertia-evasion needs (α₁=α₂=0) independently forces c₁₄=0 at c₁₃=0. The allowed corner is therefore the **c₁₃=c₁₄=0 double-null**, where the Einstein-aether kinetic norms vanish and the spin-1 speed diverges — the theory's known strong-coupling / ill-posed point. The nonlocal MI matter coupling is a₀-IR-gapped (dQ/dz→0 for ω≫a₀); it renormalizes the kinetic norm only in the galactic infrared and supplies nothing in the ultraviolet where the strong coupling lives. The linear two-point analysis loses control at this corner; the strong-coupling scale is high (M_sc ~ 10¹¹ GeV, so a controlled nonlinear/Stückelberg window is *not* excluded), but that window must be **demonstrated, not assumed.** Along the natural Einstein-aether route the completion is **walled at the linear level.**

### 5. What is postulated, and what remains open

**Postulated** (flagged, never used as results): the **MOND sign** s=−1 — the passive, unitary de Sitter bath gives δm = 2∫ρ(ω)/ω² dω ≥ 0 (anti-MOND) at every computable order (2-point spectral, all-orders Bisognano–Wichmann, ground-state passivity, the Euclidean-KMS corner, and the connected 4-point positivity), so the MOND sign requires an active/pumped medium de Sitter does not supply; it is admitted only through a named Machian posit. The **value** Z=√(32π/3) (only the scale a₀∼√Λ is forced) and the corner ω_c.

**Open:** (i) the nonlinear/Stückelberg strong-coupling analysis at the c₁₃=c₁₄=0 double-null — whether a controlled EFT window below M_sc survives (the c₁₃=0 plane is a live degeneracy in the aether literature; a window is not excluded); (ii) whether a *different* frame-field structure (beyond a two-derivative vector) evades the double-null without becoming the modified-gravity mimetic limb; (iii) the off-circular / congruence-shear terms in □_u beyond the constant-|a| slice; (iv) the separate four-point / de Sitter-positivity vertex.

### 6. Honest standing

The inertia-based worldline sector is written and verified; the modified-inertia realization evades Cassini; MOND does not force modified gravity; and the mixed two-point propagator is ghost-free in closed form. These are real, both-footing results. The completion is nonetheless **not** a finished field theory along the natural Einstein-aether route: the corner it is required to occupy — GW170817 ∩ preferred-frame safety — is the aether strong-coupling double-null, where the linear analysis breaks down and the nonlinear window is undemonstrated (though not excluded). The MOND sign stays postulated and a₀'s value underived. This paper therefore reports a sharp boundary: the covariant modified-inertia completion is neither the modified-gravity limb (Cassini-failing) nor a finished field theory — it is a well-posed worldline theory whose covariantization is walled at a specific, named, literature-live strong-coupling point. It makes no completeness or theory-of-everything claim.

### 7. Related work

The construction sits between the relativistic modified-gravity realizations of MOND — AeST [Skordis & Złośnik 2021], the Blanchet–Skordis khronon [2025], and the nonlocal (mimetic modified-gravity) model of Deffayet & Woodard [2026] — and the modified-inertia program of Milgrom [1999, 2009]. The covariant frame-field sector is Einstein-aether [Jacobson & Mattingly 2001; Jacobson 2008], whose PPN structure [Foster & Jacobson 2006] and GW170817 constraint [Gong et al. 2018] supply the wall. The nonlocal form factor's ghost-freedom is of the class analyzed by Barvinsky [2003]; the doubled-worldline nonconservative formalism is Galley [2013].

### 8. Reproducibility

All numerical and symbolic claims are backed by committed scripts (repository `real_research/`): the worldline sector and Cassini evasion in `reviews/cassini_mi_evasion_2026/` and the integrated check; the covariant kinetic wins in `reviews/mi_kinetic_completion_2026/` (l=0 source, open inert corner, both footings); the mixed-propagator ghost-freedom and the strong-coupling wall in `reviews/mi_propagator_2026/` (`propagator_compute.py`, `refute_strongcoupling.py`). The sign-wall inputs are `ACTIVE_KERNEL_SIGNTHEOREM_2026-06.md` and `FOURTH_ORDER_SIGN_WALL_2026-07.md`; the trichotomy is `COVARIANT_MI_COMPLETION_2026-06.md`.

### References

1. M. Milgrom, *The modified dynamics as a vacuum effect*, Phys. Lett. A **253**, 273 (1999).
2. M. Milgrom, *MOND effects in the inner Solar system*, MNRAS **399**, 474 (2009).
3. S. Deser & O. Levin, *Accelerated detectors and temperature in (anti–)de Sitter spaces*, Class. Quantum Grav. **14**, L163 (1997).
4. T. Jacobson & D. Mattingly, *Gravity with a dynamical preferred frame*, Phys. Rev. D **64**, 024028 (2001).
5. T. Jacobson, *Einstein-aether gravity: a status report*, PoS QG-Ph, 020 (2008), arXiv:0801.1547.
6. B. Z. Foster & T. Jacobson, *Post-Newtonian parameters and constraints on Einstein-aether theory*, Phys. Rev. D **73**, 064015 (2006), gr-qc/0509083.
7. C. Skordis & T. Złośnik, *New relativistic theory for modified Newtonian dynamics* (AeST), Phys. Rev. Lett. **127**, 161302 (2021).
8. L. Blanchet & C. Skordis, *Khronon-tensor theory of gravity*, arXiv:2507.00912 (2025).
9. C. Deffayet & R. P. Woodard, *A nonlocal realization of MOND that interpolates from cosmology to gravitationally bound systems*, JCAP **04**, 081 (2026), arXiv:2512.10513.
10. Y. Gong, S. Hou, D. Liang & E. Papantonopoulos, *Gravitational waves in Einstein-aether and generalized TeVeS after GW170817*, Phys. Rev. D **97**, 124023 (2018), arXiv:1802.04303.
11. R. S. Park et al., *Constraints on Lorentz violation and the MOND quadrupole from Cassini*, arXiv:2602.17884 (2026).
12. A. O. Barvinsky, *Nonlocal action for long-distance modifications of gravity*, Phys. Lett. B **572**, 109 (2003).
13. C. R. Galley, *Classical mechanics of nonconservative systems*, Phys. Rev. Lett. **110**, 174301 (2013).
14. Companion (this program): *No Pump-Free Corner* (sign wall, all-orders), Zenodo 10.5281/zenodo.21184373; the covariant-MI quadrichotomy, Zenodo 10.5281/zenodo.21148494; the written MI action v1, Zenodo 10.5281/zenodo.21253645.

*Both a₀ footings carried throughout. Each claim is labeled derived / postulated / open; the MOND sign is a postulate; the covariant completion is walled at a named strong-coupling corner with the nonlinear window open. No completeness or theory-of-everything claim is made.*
