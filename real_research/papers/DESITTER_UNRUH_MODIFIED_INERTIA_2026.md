# A Cosmological-Constant Acceleration Scale and its Modified-Inertia Completion

## The MOND scale as a de Sitter–Unruh inertial effect: $a_0 = c^2\sqrt{\Lambda/32\pi}$, its written covariant action, dark-matter-free lensing, and a falsifiable $a_0(z)$

**Carl P. Zimmerman** · Briar Creek Tech · 2026-07-09

---

### Abstract

The MOND acceleration scale famously coincides with the cosmic acceleration scales, $a_0 \sim cH_0 \sim c\sqrt{\Lambda}$ — a coincidence that $\Lambda$CDM treats as accidental. This paper takes it literally and develops it as a modified-**inertia** effect, not a modification of gravity: the acceleration at which a body's inertial response to the de Sitter (dark-energy) vacuum departs from Newtonian is set by the vacuum energy density, giving
$$a_0 \;=\; \frac{c}{2}\sqrt{G\rho_\Lambda}\;=\;c^2\sqrt{\frac{\Lambda}{32\pi}}\;=\;\frac{cH_\Lambda}{Z},\qquad Z=\sqrt{\tfrac{32\pi}{3}}\approx 5.79,\qquad a_0 \approx 9.4\times 10^{-11}\ \mathrm{m\,s^{-2}}.$$
Two claims are made and separated cleanly. **(i) An empirical reframing.** At this $a_0$ and a single stellar mass-to-light ratio, the SPARC radial-acceleration and baryonic Tully–Fisher relations are reproduced to $\sim 0.11$ dex, with the interpolation $\nu(y)=\sqrt{1+1/y}$ over-determined by the Deser–Levin de Sitter–Unruh temperature rather than fitted. **(ii) A covariant completion.** The explicit nonlocal modified-inertia action is written and carried to a definite boundary, reasoning throughout from the framework's own premises — a **passive** reference frame, with the MOND content in the **matter** sector. On those premises the theory has a machine-verified closed constraint algebra (zero propagating frame degrees of freedom), a rigorously defined causal nonlocal operator, a causal ghost-free two-point sector, and it **evades the Cassini quadrupole** by $\sim 7$ orders of magnitude where modified-*gravity* realizations of MOND fail at $+6$ to $+14\sigma$; because the frame is passive it carries no propagating tensor mode, so it satisfies the GW170817 graviton-speed bound trivially. **Gravitational lensing** is resolved without dark matter by a disformal photon metric built from the same passive frame: universal (one rule for all galaxies), Cassini-safe, ghost-free and causal. The one- and two-loop de Sitter **radiative structure is computed at the divergence level**: $a_0$ is not renormalized, and no transverse aether kinetic term is generated in either the matter or the graviton sector, so the passive frame survives two loops at that level. **The one distinctive, falsifiable prediction** is that $a_0$ evolves with the dark-energy density, $a_0(z)\propto\sqrt{\rho_{\mathrm{DE}}(z)}$, declining to $\approx 0.74\,a_0(0)$ by $z=3$; the framework's distinctive content dissolves back to ordinary MOND if dark energy proves to be a true cosmological constant. The MOND **sign**, the value of $a_0$, and the normalization $Z$ are **posited inputs, not derived**; the Standard Model is untouched. This is a one-scale effective theory carried to a sharp, named boundary — explicitly **not** a theory of everything.

### 1. Introduction

Rotation curves of galaxies flatten below a characteristic acceleration $a_0\approx 1.2\times 10^{-10}\ \mathrm{m\,s^{-2}}$ [Milgrom 1983; Lelli, McGaugh & Schombert 2016]. That scale sits within an order-one factor of both $cH_0$ and $c\sqrt{\Lambda}$. In $\Lambda$CDM this is a numerical accident; in the modified-dynamics program it is a clue. Two readings are possible. **Modified gravity** promotes a new field that sources the metric (AeST [Skordis & Złośnik 2021], the khronon [Blanchet & Skordis 2025], TeVeS); these bend light correctly but a dynamical vector/tensor sector generically fails solar-system tests. **Modified inertia** [Milgrom 1994, 1999] instead changes how bodies respond to a given gravitational field; it evades the solar-system problem but has historically lacked both a covariant action and a lensing account.

This paper develops the modified-inertia reading with the acceleration scale fixed by the **cosmological constant**. Section 2 states the scale; Section 3 gives the empirical anchor; Section 4 writes the covariant action and its verified structure; Section 5 resolves lensing; Section 6 reports the radiative structure; Section 7 gives the falsifiable prediction; Section 8 states the honest boundary. Every load-bearing claim is backed by a committed, runnable verification script; both admissible normalizations of $a_0$ ("footings") are carried throughout.

> **Retraction honored.** Earlier versions of this program made theory-of-everything and Standard-Model claims that were publicly retracted (2026-06-23). They are not reasserted here. The claims of this paper are the $a_0$ reframing and its covariant completion — nothing more.

### 2. The acceleration scale

Read $a_0$ as the surface-gravity scale of the dark-energy horizon. With $\rho_\Lambda = \Lambda c^2/8\pi G$ the dark-energy density and $H_\Lambda = c\sqrt{\Lambda/3}$ its de Sitter rate,
$$a_0 = \frac{c}{2}\sqrt{G\rho_\Lambda} = c^2\sqrt{\frac{\Lambda}{32\pi}} = \frac{cH_\Lambda}{Z},\qquad Z = \sqrt{\tfrac{32\pi}{3}}\approx 5.79.$$
The scale is one order-one factor $Z$ below the bare horizon acceleration $cH_\Lambda$. Two footings are admissible and are reported side by side everywhere: the **canonical** dark-energy footing $\rho_{\mathrm{DE}}/cH_\Lambda \Rightarrow a_0 = 9.36\times10^{-11}\ \mathrm{m\,s^{-2}}$, and the **total-density** footing $\rho_{\mathrm{tot}}/cH_0 \Rightarrow a_0 = 1.13\times10^{-10}$. The interpolation between the Newtonian and deep-MOND regimes,
$$g_{\mathrm{obs}} = \sqrt{g_{\mathrm{bar}}^2 + g_{\mathrm{bar}}\,a_0},\qquad \nu(y)=\sqrt{1+1/y},\quad y = g_{\mathrm{bar}}/a_0,$$
is the de Sitter–Unruh modified-inertia law of Milgrom [1999], fixed by the Deser–Levin temperature $T(a) = (\hbar/2\pi k_B c)\sqrt{a^2 + (cH_\Lambda)^2}$ [Deser & Levin 1997] — the vacuum's temperature acquires a floor from the horizon, and the departure from Newtonian inertia sets in when a body's own acceleration drops to that floor. The $O(1)$ coefficient $32\pi$ (equivalently $Z$) is a **posit**, not a theorem; it cancels in the falsifiable ratio $a_0(z)/a_0(0)$ of Section 7.

### 3. The empirical anchor

On the SPARC sample [Lelli et al. 2016], at $a_0 = 9.36\times10^{-11}$ and a single mass-to-light ratio $\Upsilon_\star\approx 0.70$, the radial-acceleration relation is reproduced with $0.108$ dex scatter — marginally tighter than the standard MOND fit on the framework's own $\nu$ — and the baryonic Tully–Fisher relation $v^4 = G M_{\mathrm{bar}}\,a_0$ and the deep-MOND limit $a = \sqrt{a_0\,g_{\mathrm{bar}}}$ are exact consequences. The RAR at this scale is convention-compatible but *non-diagnostic* of the specific value $9.36\times10^{-11}$ versus $1.13\times10^{-10}$ (the difference is absorbed by the interpolation and $\Upsilon_\star$); the diagnostic content is the redshift evolution of Section 7, not the $z=0$ zero-point.

### 4. The covariant action and its verified structure

With signature $(-+++)$ the action is
$$S[x,g,u] = S_{\mathrm{EH}}[g] + S_u[g,u] + S_{\mathrm{matter}}[x,g,u],$$
with host general relativity unmodified, a unit-timelike frame constraint $S_u = -\tfrac12\int\!\sqrt{-g}\,\lambda\,(u^\mu u_\mu + 1)$ carrying **no aether kinetic term**, and the modified-inertia content in the matter kinetic sector,
$$S_{\mathrm{matter}} = -\tfrac12\int d^4x\,\sqrt{-g}\;\rho_m\,\big[\,s\,u^\mu\,K(\Box_u/a_0^2)\,u_\mu\,\big],\quad K(z)=\frac{\sqrt{1+4z}-1}{2\sqrt z},\quad \Box_u f = u^a\nabla_a(u^b\nabla_b f).$$
Here $u^\mu$ is a **passive**, horizon-anchored reference frame — an algebraic constitutive law, a Lorentz-violating gravitational-sector background, the cosmic rest frame — **not** a dynamical aether. $K$ is non-entire with a branch cut and a single healthy pole; $s=-1$ is the **MOND-sign posit** (see §8). Reasoning from these premises rather than the standard aether/MOND lens, the following are established, each machine-verified on both footings:

- **Worldline sector.** The circular-orbit reduction reproduces $\nu(y)=\sqrt{1+1/y}$ to $3\times10^{-13}$; Newton, deep-MOND, BTFR, the de Sitter-forced $\sqrt2$-weighted external-field kernel, and ghost-freedom (single healthy pole vs. the Ostrogradsky ghost of the local truncation) all follow.
- **Constraint structure.** The full curved-spacetime Dirac analysis closes at the secondary level; the unit-norm sector is genuinely second-class (its $2\times2$ Dirac block has determinant $4(u\cdot u)^2\to 4$ on-shell), leaving **zero propagating frame degrees of freedom** — total propagating content is the two GR graviton polarizations. The concern that $u$ sits *inside* $\Box_u$ resolves negatively: the exact quadratic symbol at every order is $S_n=(-1)^n k_\perp^2 k_0^{2n}$, whose only root is $k_0=0$ independent of spatial momentum — a transport-along-$u$ structure with no wave-cone and zero group velocity. The operator ordering of $\Box_u$ is immaterial to this conclusion: the directional and covariantly-symmetrized orderings differ by a term $\propto a^b\,\partial_b(u\cdot u)$ that vanishes by the unit-timelike constraint.
- **Operator.** $K(\Box_u)$ is rigorously defined by the Borel functional calculus of the (essentially self-adjoint) directional operator, with a canonical Herglotz–Nevanlinna spectral representation carrying a unique positive Borel measure; $\|K\|\le 1$, causal-retarded, defined on all of $L^2$. Its branch cut is the physical de Sitter–Unruh emission continuum, not a ghost.
- **Two-point sector.** The mixed matter–frame propagator is causal and ghost-free in closed form (retarded construction; Källén–Lehmann spectral positivity across the whole cut; principal symbol equal to the GR light-cone), and nonlinear classical stability holds.
- **Cassini and GW170817.** The modified-inertia realization evades the solar-system quadrupole: the anisotropic galactic external field enters only Saturn's inertial response, deep-Newton-suppressed by $\nu-1\approx 7\times10^{-7}$, giving an $\ell=2$ quadrupole $\sim 7$ orders below the Cassini ceiling, where the modified-gravity realization fails at $+6$ to $+14\sigma$. Because the frame is passive it introduces no propagating tensor mode, so the graviton travels at $c$ and the GW170817 bound is satisfied automatically — the constraint that eliminates a broad class of modified-gravity theories does not apply.

The Einstein-aether strong-coupling "wall" often invoked against covariant MOND is **mis-applied** here: it is a property of a *propagating* aether mode whose kinetic norm vanishes, and the framework's frame has no such mode.

### 5. Gravitational lensing without dark matter

In modified inertia the dynamics come from the inertial response, not the metric, so a single-metric theory makes light — which has no inertia — track the *baryonic* metric and under-lens by the MOND factor $\nu$; enhancing the one metric to compensate **double-counts** the dynamics (it would over-predict rotation curves), forcing pure modified gravity and reinstating the Cassini problem. The resolution is a **disformal photon metric** built from the passive frame,
$$\tilde g_{\mu\nu} = g_{\mu\nu} + B\,u_\mu u_\nu,$$
on which **light** propagates while matter keeps modified inertia in $g$. Only the disformal $u_\mu u_\nu$ term bends light (a conformal factor is null-inert); fixing $B$ by the same $\nu$ the RAR uses makes lensing **universal** — one rule for every galaxy, not a per-galaxy fit — and **double-count-free by construction**, since the matter dynamics are untouched. It is **Cassini-safe**: $B\sim(\nu-1)\to a_0/2a\to 0$ at high acceleration, giving a PPN shift $|\Delta\gamma|\sim 10^{-13}$ at the Sun, far below the $2.3\times10^{-5}$ bound; and it is **ghost-free and causal** — $\tilde g$ is Lorentzian ($B\sim 3\times10^{-7}\ll 1$), photons are subluminal with respect to $g$, and the coupling is first-order in every dynamical field, hence Ostrogradsky-free. The disformal strength $B$ is fixed non-locally by the framework's **own** operator $K(\Box_u)$ (an AQUAL/Poisson lensing potential, momentum-conserving for any geometry; a local $B(a/a_0)$ is its exact spherical limit) — so it is not a new ingredient. This recovers the "lensing tracks dynamics" property [Brouwer et al. 2021; Mistele & McGaugh 2024] from modified inertia, without the dynamical aether that fails Cassini.

### 6. Radiative structure on de Sitter

Using the framework's own Herglotz measure, which converts the nonlocal vertex into a positive superposition of local massive resolvents, the one-loop divergence structure on de Sitter is computed exactly (Seeley–DeWitt, under a stated $\rho_m = m^2\phi^2$ proxy for the quantum matter density):

- **$a_0$ is not renormalized**, additively or multiplicatively — there is no $z^0$ tadpole at the exact-measure level, enforced by a sum rule $\int d\mu(t)/|t| = K(\infty)-K(0) = 1$ (unit resolvent weight). The additive channel is protected to **all orders** by the exact shift symmetry $T\to T+\text{const}$ (the frame depends only on $\partial T$) together with the unit-timelike constraint, which collapses any surviving frequency-independent frame functional to a pure cosmological constant.
- **No transverse aether kinetic term is generated.** The dangerous graviton-frame mixing channel, real on de Sitter ($R_{\mu\alpha\nu\beta}u^\alpha u^\beta = -H^2 P_\perp$ exactly), closes because the curvature commutators are algebraic ($k_0^2\to H^2$, never $k_\perp^2$). Extending to two loops, the transverse channel is closed at the divergence level in **both** sectors: in the **matter** sector by the geodesy identity (the linear frame vertex vanishes at every order) together with $K(0)=0$; and in the **graviton** sector by a complete census of two-graviton-loop topologies, in which the graviton's transverse momentum is *rationed* (the frame's external-momentum power is zero for all $n$, while a cone requires two), the transverse-traceless graviton–frame vertex vanishes, and the constrained shift sector stays instantaneous. So the passive frame (zero degrees of freedom) survives two loops at the divergence level.
- **Finite parts (matter sector).** The one-loop effective potential is bounded below (the exact bound $\|K\|\le 1$ with $s=-1$ confines the effective mass-squared, precluding runaway), and the de Sitter infrared is regulated by the friction gap: $\Box_u$ is gapped at $-9H^2/4$, giving every loop field an effective mass $\ge 3H/2$ that removes the usual secular-growth pathology. Dressed Källén–Lehmann positivity and KMS detailed balance survive the real one-loop convolution.

**Open at this level.** This is a *divergence-level* radiative account, not a finished quantum field theory: the one- and two-loop **finite** parts, genuinely higher loops, the disformal-metric variant of the matter coupling, and constraint-survival under loops all remain to be computed.

### 7. The falsifiable prediction

Because $a_0$ is set by the dark-energy density, it is not constant: $a_0(z) = c^2\sqrt{\Lambda_{\mathrm{eff}}(z)/32\pi}\propto\sqrt{\rho_{\mathrm{DE}}(z)}$. For a cosmological constant this is flat; for evolving dark energy it declines. With the DESI DR2 CPL best fit ($w_0,w_a$) the density rises to a gentle peak $\sim 4.5$ Gyr ago and then falls, so the framework predicts
$$a_0(z{=}3) \approx 0.74\,a_0(0),\qquad \text{with a } \sim\!6\%\ \text{bump near } z\approx0.4,$$
a **declining** acceleration scale. This is the theory's one distinctive, pre-registered signature, and it is falsifiable in both directions:

- **Confirms** if deep-MOND kinematics at $z\approx2$–$3$ (ELT/HARMONI, JWST/NIRSpec, ALMA) show $a_0(z{=}3)\approx 0.74\,a_0(0)$ tracking $\sqrt{\rho_{\mathrm{DE}}}$, $>3\sigma$ from both constant and rising alternatives; equivalently, high-$z$ discs sitting $\approx -0.03$ dex below the $z=0$ baryonic Tully–Fisher zero-point.
- **Falsifies** if $a_0(z)$ is flat or rising, or — the standing hostage — if DESI DR3 drives $w\to-1$, in which case the distinctive content dissolves and the framework degenerates to ordinary MOND with no evolving scale.

The decisive near-term data are **DESI DR3** (the dark-energy equation of state), **Gaia DR4** (wide binaries and a Lorentz-violation dipole from the induced SME background), and **ELT-class high-$z$ rotation kinematics**.

### 8. The honest boundary

What is **derived / verified**: the interpolation shape (de Sitter–Unruh, over-determined); the worldline sector; the closed constraint algebra and zero frame degrees of freedom; the operator's rigorous definition; two-point causality and ghost-freedom; Cassini evasion and GW170817-safety; the disformal lensing construction (universal, Cassini-safe, ghost-free); and the divergence-level radiative structure in both sectors, on both footings.

What is **posited, not derived**: the **MOND sign** $s=-1$ (a passive de Sitter vacuum supplies the anti-MOND sign; the active response that would fix it is not sourced without a pump — so the sign is a Machian input); the **value of $a_0$** and the normalization $Z$ (a one-parameter effective theory, with $Z$ not forceable); and there is **no Standard-Model bridge** — the particle sector is untouched.

What is **open**: the finite-part and higher-loop radiative structure; a first-principles condensate/AQUAL closure of the non-spherical lensing potential; and, above all, the empirical verdict on $a_0(z)$.

This is an effective, one-scale, falsifiable modified-inertia framework carried to a sharp and named boundary. It answers the objections that eliminate modified gravity (Cassini, GW170817) and the objection that traditionally eliminates modified inertia (lensing), with explicit, reproducible computations; and it stakes its distinctiveness on a single near-term measurement. It is **not** a finished quantum field theory and **not** a theory of everything, and it says so plainly.

### Reproducibility

All load-bearing claims are backed by committed, runnable scripts (repository `real_research/reviews/`), including the worldline sector and Cassini evasion, the constraint/operator/two-point analysis (`mi_formal_completion_2026/`), the disformal lensing construction and its ghost-freedom/locality checks, the one- and two-loop de Sitter radiative computations (`oneloop_lane*.py`, `twoloop_*`), the operator-ordering invariance check, and the full two-graviton-loop transverse-aether census (`graviton_census_2loop/`). Iterative companion: written MI action, Zenodo concept DOI [10.5281/zenodo.21253644](https://doi.org/10.5281/zenodo.21253644).

### References

1. M. Milgrom, ApJ **270**, 365 (1983); Phys. Lett. A **253**, 273 (1999); Ann. Phys. **229**, 384 (1994).
2. S. Deser & O. Levin, Class. Quantum Grav. **14**, L163 (1997).
3. F. Lelli, S. McGaugh & J. Schombert, AJ **152**, 157 (2016); Phys. Rev. Lett. **117**, 201101 (2016).
4. C. Skordis & T. Złośnik, Phys. Rev. Lett. **127**, 161302 (2021); L. Blanchet & C. Skordis, arXiv:2507.00912 (2025).
5. T. Jacobson & D. Mattingly, Phys. Rev. D **64**, 024028 (2001); D. Blas, O. Pujolàs & S. Sibiryakov, JHEP **10**, 029 (2009).
6. M. Brouwer et al., A&A **650**, A113 (2021); T. Mistele & S. McGaugh, arXiv:2310.15248 (2024).
7. B. P. Abbott et al. (LIGO/Virgo), ApJL **848**, L13 (2017) (GW170817 graviton speed).
8. DESI Collaboration, arXiv:2503.14738 (2025).
9. C. R. Galley, Phys. Rev. Lett. **110**, 174301 (2013); D. V. Vassilevich, Phys. Rept. **388**, 279 (2003) (heat kernel).

*Both $a_0$ footings throughout. Each claim labeled derived / posited / open. The MOND sign, $a_0$, and $Z$ are inputs; the Standard Model is untouched. No completeness or theory-of-everything claim is made.*
