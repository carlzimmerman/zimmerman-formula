# A Written de Sitter–Unruh Modified-Inertia Action

## The worldline sector verified, the MOND sign postulated, and the covariant frame-field kinetic term as the sole remaining obstruction

**Carl P. Zimmerman** · Briar Creek Tech · 2026-07-08

---

### Abstract

The de Sitter–Unruh reading of the MOND acceleration scale, a₀ = cH_Λ/Z = c²√(Λ/32π) = 9.36×10⁻¹¹ m s⁻², posits that the scale is a modified-**inertia** effect of the cosmic (dark-energy) horizon rather than a modification of gravity. Prior work characterized the *obstructions* to a covariant completion — a strict trichotomy (local → Ostrogradsky ghost; field → modified gravity failing Cassini; nonlocal → the only ghost-free horn) and an all-orders sign wall (a passive, unitary de Sitter bath sources the *anti*-MOND sign). Here we write the **constructive** counterpart: an explicit nonlocal modified-inertia action, and we report precisely how far it is finished. The **worldline / matter sector is written and machine-verified** (28/28 assertions, both a₀ footings): its circular-orbit reduction reproduces the framework's interpolation ν(y)=√(1+1/y) to 3×10⁻¹³, together with the Newtonian and deep-MOND limits, the baryonic Tully–Fisher relation v⁴=GM a₀, the external-field kernel with a de Sitter–Unruh-forced √2 DC weight, exact ghost-freedom (a single healthy pole, against the Ostrogradsky ghost of the local truncation), conservativeness, and a deep-Newtonian solar-system quadrupole suppression that renders the inertia realization Cassini-safe. **One physics input is postulated, not derived:** the MOND sign s = −1, walled all-orders against the passive vacuum and licensed only by a named Machian posit. **One structural edge is open and load-bearing:** the generally-covariant field theory is asserted, not constructed — the frame field u^μ is written as a non-dynamical clock, and no admissible covariant kinetic term for u^μ is yet known that keeps it effectively non-propagating (Cassini-safe) rather than collapsing to the modified-gravity limb. This is an effective completion assembled to its current ceiling — **not a finished theory and not a theory of everything.**

---

### 1. Setting and scope

The framework reads a₀ as the acceleration at which a body's inertial response to the de Sitter vacuum departs from the Newtonian value, with the Deser–Levin temperature T(a) = (ℏ/2πk_Bc)√(a² + (cH_Λ)²) providing a horizon floor and the interpolation

$$g_{\mathrm{obs}} = \sqrt{g_{\mathrm{bar}}^2 + g_{\mathrm{bar}}\,a_0}, \qquad \nu(y)=\sqrt{1+1/y}, \quad y=g_{\mathrm{bar}}/a_0 .$$

Two facts sharpen the present task. First, a covariant **modified-gravity** realization of this scale (AeST / Blanchet–Skordis khronon) inherits a solar-system quadrupole tension with the improved Cassini bound Q₂ = (1.6 ± 1.8)×10⁻²⁷ s⁻² (Park et al. 2026) at the +6 to +14σ level for the framework's own slow interpolation. Second, a companion computation shows the **modified-inertia** realization evades that bound by ~7 orders of magnitude, because in modified inertia the Sun's field stays Newtonian (no phantom-density quadrupole) and the response is deep-Newtonian-suppressed by ν−1 = a₀/2a ≈ 7×10⁻⁷ at Saturn. The inertia realization is therefore the one worth writing down — provided it can be written at all. This paper writes it, and reports the exact boundary of what is thereby established.

We are explicit throughout about the classification of each claim as **derived**, **postulated**, or **open**. The framework's earlier theory-of-everything and Standard-Model claims were publicly retracted (2026-06-23) and are not reasserted; what follows is a one-scale effective-theory construction with named inputs.

### 2. The action

With signature (−+++) and c restored, the assembled action is

$$S[x,g,u] = S_{\mathrm{EH}}[g] + S_u[g,u] + S_{\mathrm{matter}}[x,g,u].$$

**(A) Host gravity, unmodified.**
$$S_{\mathrm{EH}} = \frac{1}{16\pi G}\int d^4x\,\sqrt{-g}\,(R - 2\Lambda).$$

**(B) Frame constraint only** — a unit-timelike clock u^μ with a Lagrange multiplier, and, decisively, **no Maxwell-type kinetic term**:
$$S_u = -\int d^4x\,\sqrt{-g}\,\frac{\lambda}{2}\left(u^\mu u_\mu + 1\right).$$
The omission of an F² = (∇_{[μ}u_{ν]})² kinetic term is exactly what keeps the lift Cassini-safe; restoring it is what collapses the theory to the modified-gravity limb (§5).

**(C) The modified-inertia content** lives in the *matter kinetic* sector, ρ_m-weighted and gated by a nonlocal branch-cut form factor:
$$S_{\mathrm{matter}} = -\frac{1}{2}\int d^4x\,\sqrt{-g}\,\rho_m(x)\,\big[\,s\;u^\mu\,K\!\left(\Box_u/a_0^2\right)u_\mu\,\big],$$
with
$$K(z) = \frac{\sqrt{1+4z}-1}{2\sqrt{z}} = \mu_{\mathrm{fw}}(\sqrt z), \qquad z=\Box_u/a_0^2, \quad \Box_u f = u^a\nabla_a\!\left(u^b\nabla_b f\right),$$
where □_u is the proper-time wave operator along u (the field lift of d²/dτ²), reducing on constant-|a| / orbit-averaged worldlines to |g_N|²/a₀². The function K is non-polynomial with a branch cut and a **single healthy pole** (residue +1); this nonlocality is precisely the ghost-free horn of the trichotomy. In the deep-MOND regime 1/K → a₀/|a|.

**Equivalent worldline form.** The field action lifts a Galley doubled-worldline (in–in) action
$$S[x_+,x_-] = \int d\tau\left[\,m\,u_+\!\cdot u_- + F\!\cdot x_- - s\,m\,a_-^\mu\,G(\bar a_+)_\mu\,\right], \quad G(a)^\mu = a^\mu\,\mu_{\mathrm{fw}}(|a|/a_0) = \nabla_a\Phi_a,$$
with μ_fw(x) = (√(1+4x²)−1)/(2x) the exact inverse of ν(y)=√(1+1/y), G an exact gradient of a convex acceleration potential (conservative), and ā₊ the even-kernel-smoothed acceleration (lossless). The external-field / memory kernel is
$$\theta(y) = \frac{\theta_0}{1+(\theta_0-1)\,y^2}, \qquad \theta_0=\sqrt2,\;\; \theta(1)=1,$$
whose Lorentzian form-class and √2 DC weight are forced by the de Sitter worldline Wightman function W(u) ∝ −1/sinh²(κ(u−iε)/2), κ = 2πT_eff; the corner location ω_c is *not* bath-forced.

Here **s = ±1 is the MOND-sign postulate** (s = −1 is the MOND branch, equivalently K(0)=0), a₀ = cH_Λ/Z = 9.36×10⁻¹¹ m s⁻² (canonical, ρ_DE, Z=√(32π/3)=5.78881), with the alternate footing 1.13×10⁻¹⁰ (ρ_total) carried throughout.

### 3. What is verified (the worldline / matter sector)

Every item below is machine-checked in the reproducibility scripts (§7), both footings, 28/28 assertions, exit 0:

1. **RAR shape.** The circular-orbit equation of motion μ_fw(a/a₀)·a = g_N reproduces ν(y)=√(1+1/y) over y ∈ [10⁻⁴, 10⁴] to max relative error 3.35×10⁻¹³.
2. **Newtonian limit** μ_fw(x→∞) = 1 (exact); **deep-MOND** μ_fw(x→0) ~ x, a = √(a₀ g_N) (5×10⁻⁴).
3. **BTFR** v⁴ = GM a₀, r-independent (exact); v_flat(10¹⁰ M_⊙) = 105.6 / 110.7 km s⁻¹ on the two footings.
4. **Form-factor ↔ RAR identity.** Inverting Y = μ_fw(X)·X gives X = √(Y²+Y) exactly, i.e. g_obs = √(g_bar² + g_bar a₀).
5. **External-field kernel** θ(y) with the dS-Unruh-forced √2 DC weight, monotone-decreasing, θ(1)=1 (circular orbits drop the kernel).
6. **Ghost-freedom.** By residue computation, K(z) has a single pole at p²=0 with residue +1 and no other pole; the local truncation carries an Ostrogradsky ghost (residue −1 at p²=−M²). Nonlocality is what removes the ghost.
7. **Conservativeness / losslessness** — exact gradient force plus an even time-domain kernel.
8. **Cassini suppression** forced by the deep-Newton ν−1 = a₀/2a ≈ 7×10⁻⁷ at Saturn.

### 4. What is postulated

Three inputs are named and never used as results:

- **The MOND sign s = −1.** This is the one load-bearing physics postulate. The passive, unitary (Källén–Lehmann ρ ≥ 0, KMS) de Sitter bath gives δm = 2∫ρ(ω)/ω² dω ≥ 0, i.e. inertia *raised* = anti-MOND, at every order that can be computed (2-point spectral, all-orders Bisognano–Wichmann mean-force Gibbs, ground-state passivity, adiabatic dressing, and the de Sitter Euclidean-KMS corner). The MOND sign requires ρ < 0 (a negative-norm ghost) or an active/pumped medium that de Sitter does not supply; it is admitted only through a named Machian state-function posit, itself a posit and not a theorem.
- **The value of Z = √(32π/3).** Only the scale a₀ ∼ √Λ is forced; the 32π/3 is a gravitational normalization invisible to the kinematic kernel (κ-closure), so the numerical value of a₀ — and which footing — is not derived. Both are carried; the spread does not flip any verdict here.
- **The corner ω_c / memory order.** The bath fixes the Lorentzian form-class and the DC weight, not the corner location.

### 5. The sole remaining obstruction

The generally-covariant field theory is, as written, **asserted rather than constructed.** In the action of §2, u^μ carries no kinetic term and hence no equation of motion — it is a background clock. The full covariant sense of the theory (metric variation, u^μ dynamics, well-posedness, dispersion) is not established: the scripts contain no metric variation, no u^μ field equation, and no perturbation analysis, and the solar-system quadrupole quoted in §3 is the companion computation's value imported for consistency, not computed by varying this action's stress tensor. The reduction identity □_u u^μ → |a|² u^μ that underwrites the derivations holds only on constant-|a| / orbit-averaged worldlines; off-circular jerk and congruence-gradient (shear/vorticity) terms are uncontrolled.

The obstruction is sharp and binary. Every *known* way to give u^μ covariant dynamics collapses the theory to modified gravity and re-inherits the Cassini quadrupole: an AeST-type −(K_B/2)F² kinetic term sources a phantom density everywhere (Q₂ ~ 3×10⁻²⁶ s⁻², above the 5.2×10⁻²⁷ ceiling), and a Deser–Woodard-type u = −∇χ/|∇χ| modifies the metric photons and orbits see (the mimetic modified-gravity limb). **No well-posed, generally-covariant, ghost-free kinetic completion for u^μ that keeps it effectively non-dynamical is presently known.** The decisive next computation is therefore explicit: write a candidate covariant kinetic term, vary the full action, linearize on a Newtonian-plus-galactic-external background, and *compute* (not import) the l=2 quadrupole and the mode spectrum. The outcome is one of exactly two: a kinetic completion exists that keeps u^μ effectively non-propagating in the solar system (Cassini-safe, modified inertia survives), or every admissible kinetic term forces u^μ to source the metric and the computed Q₂ exceeds the Cassini ceiling (collapse to modified gravity).

### 6. Honest standing

The inertia-based **worldline / matter sector is finished** to its stated inputs: an explicit, ghost-free, RAR-correct, BTFR-correct, EFE-carrying, Cassini-safe modified-inertia action, verified on both footings with the sign wall honored. **The MOND sign remains a postulate** — walled all-orders against the passive de Sitter vacuum — and the **covariant frame-field kinetic completion remains an open, load-bearing structural gap.** This is the constructive companion to the obstruction papers: it exhibits the action that survives the trichotomy and the sign wall, states its one physics postulate plainly, and reduces the entire remaining question to a single, well-posed, binary field-theory computation. It is not a complete theory and makes no theory-of-everything claim.

### 7. Reproducibility

All numerical claims are backed by committed scripts (repository `real_research/`): `reviews/mi_nonlocal_kernel.py` (kernel validation), `reviews/cassini_mi_evasion_2026/{mi_q2_compute,verify_order}.py` (the deep-Newton solar-system suppression), and the integrated worldline check assembling the above (28/28 assertions, both footings, exit 0). The sign-wall inputs are `ACTIVE_KERNEL_SIGNTHEOREM_2026-06.md` and `FOURTH_ORDER_SIGN_WALL_2026-07.md`; the trichotomy is `COVARIANT_MI_COMPLETION_2026-06.md`.

### References

- M. Milgrom, *The modified dynamics as a vacuum effect*, Phys. Lett. A **253**, 273 (1999).
- M. Milgrom, *MOND effects in the inner Solar system*, MNRAS **399**, 474 (2009).
- S. Deser & O. Levin, *Accelerated detectors and temperature in (anti–)de Sitter spaces*, Class. Quantum Grav. **14**, L163 (1997).
- C. Skordis & T. Złośnik, *New relativistic theory for MOND* (AeST), Phys. Rev. Lett. **127**, 161302 (2021).
- L. Blanchet & C. Skordis, *Khronon-tensor theory*, arXiv:2507.00912 (2025).
- C. Deffayet & R. P. Woodard, *A nonlocal realization of MOND …*, JCAP **04**, 081 (2026), arXiv:2512.10513.
- R. S. Park et al., *Cassini quadrupole bound*, arXiv:2602.17884 (2026).
- C. R. Galley, *Classical mechanics of nonconservative systems*, Phys. Rev. Lett. **110**, 174301 (2013).
- Companion (this program): *No Pump-Free Corner* (sign wall, all-orders), Zenodo 10.5281/zenodo.21184373; the covariant-MI quadrichotomy, Zenodo 10.5281/zenodo.21148494.

*Both a₀ footings carried throughout. Each claim is labeled derived / postulated / open; the MOND sign is a postulate, and the covariant kinetic completion is the one named open edge. No completeness or theory-of-everything claim is made.*
