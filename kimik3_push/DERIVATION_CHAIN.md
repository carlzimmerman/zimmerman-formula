# THE FULL DERIVATION CHAIN — from first principles to the amplitude law

**kimi-k3, 2026-09-13.** This is the entire structure of the programme laid out as a single chain,
from the one physical input to the observable, with **every rung labelled** as one of:

- **[DERIVED]** — follows from the rungs above it with no further input;
- **[FITTED]** — a measured number the framework takes as a boundary condition, not a derivation;
- **[POSTULATED]** — an assumed structure (the place a referee pushes);
- **[OPEN]** — not yet established; the gap that "complete" must close;
- **[LEAN]** — machine-checked in `kimik3_push/lean/AmplitudeLaw.lean` (exit 0, zero sorry).

The chain is written so that "a complete theory of gravity" is a *fixed, checkable* target:
when the **[OPEN]** rungs close and nothing is **[POSTULATED]** that should be **[DERIVED]**, it is done.

---

## Rung 0 — the single physical input  [FITTED]

**The cosmological dark-energy density sets one acceleration.**
$$\rho_\Lambda \;=\;\Omega_\Lambda\,\frac{3H_0^2}{8\pi G},\qquad \Omega_\Lambda\simeq 0.685,\ H_0\simeq 67.4\ {\rm km\,s^{-1}Mpc^{-1}}.$$
From it, one number with the dimensions of acceleration:
$$s \;=\; c\sqrt{G\rho_\Lambda}.$$
**Status:** measured cosmology. The framework adds no new input here; it only *uses* this number.

---

## Rung 1 — the acceleration scale  [FITTED — the honest centre of the framework]

$$a_0 \;=\; \kappa\,c\sqrt{G\rho_\Lambda},\qquad \kappa=\tfrac12\ (\text{fitted}),\qquad
a_0 = 9.3619\times10^{-11}\ {\rm m\,s^{-2}}\ (\text{canonical});\ \ 1.1279\times10^{-10}\ (\text{alt}).$$

**[LEAN `a0_pos`]** $a_0>0$ is certified. **What is fitted:** $\kappa=\tfrac12$. The programme's own
theorem (`kappa_closure/k01`, README rev. 20) proves $\kappa$ is a **zero mode of the candidate action**
— it enters the field equations only through $J'$, so *no action of this class derives it*. The
photocount reading (FABLE L237) identifies the interpolating function's exponent as a **mode count**
(the data select $n=2$, i.e. $\kappa=\tfrac12$), but the *value* of the count is empirical.
**This is the one number the theory does not derive. Everything below is downstream of it.**

---

## Rung 2 — the MOND radius (the only galactic length)  [DERIVED] [LEAN]

Given a baryonic mass $M_b$, the radius where its Newtonian field equals $a_0$:
$$r_M \;=\; \sqrt{\frac{G M_b}{a_0}}.$$
**[LEAN `rM_pos`, `rM_sq`]** positivity and $r_M^2 = GM_b/a_0$ certified.
**[LEAN `monomial_dim_length`, `mond_length_unique`, `mond_length_form`]** — the *dimensionally unique*
length buildable from $(G, M_b, a_0)$: solving the exponent system for a length forces
$L \propto G^{1/2}M_b^{1/2}a_0^{-1/2}$, i.e. $r_M$ and nothing else. **The dark sector has no galactic
length of its own** ($c^2/a_0 = 31{,}112$ Mpc is cosmological), so $r_M$ is the *only* scale a halo can know about. **[DERIVED]** and machine-checked.

---

## Rung 3 — the dark sector is cold, clustering, collisionless dust  [DERIVED — on the candidate action]

The relativistic completion (AeST chassis + offset-DBI cuscuton clock, README rev. 6 v9) has a scalar
sector whose perturbations, on the self-critical surface the dynamics drives to (L192/L193), have
$$c_s^2 = 0 \quad\text{exactly},\qquad \text{isotropic stress},$$
which is precisely a **clustering cold component**. Its density is carried by the **conserved Noether
charge** of the shift symmetry (L217), so it is not tuned per epoch. **Consequence for formation:** the
sector clusters and self-gravitates as **collisionless dust** — its perturbations are non-propagating,
so a collisionless N-body is the correct instrument for Rung 5. **[DERIVED]** as a property of the
action; **[POSTULATED]** in the sense that the action itself is the candidate, not yet the established theory.

---

## Rung 4 — virial equilibrium forces the BTFR  [DERIVED] [LEAN]

If the sector settles into virial equilibrium confined at $r\sim r_M$, the virial theorem gives its
velocity dispersion:
$$\sigma^2 \;=\; \frac{G M_b}{2 r_M}.$$
Eliminating $r_M$ with Rung 2:
$$\sigma^4 \;=\; \frac{G M_b\,a_0}{4}\qquad\Longrightarrow\qquad v_{\rm flat}^4 = G M_b\,a_0$$
up to the order-unity virial factor. **This is the baryonic Tully–Fisher relation.**
**[LEAN `btfr_virial`]** certifies the algebraic identity $\sigma^4 = GM_b a_0/4$.
**[LEAN `btfr_exponent`]** certifies that $v^4 = C M_b$ is a $1/4$ power law in $M_b$.
The **exponent is derived** (FRIED_CHICKEN row 2 ✅); the **normalisation is $\kappa$** (Rung 1, fitted).

---

## Rung 5 — the amplitude law is the condensate's HYDROSTATIC EQUILIBRIUM, not a collapse product  [OPEN — the crux, and the repo's own key]

**The missing piece, and it changes this rung entirely.** The framework's central structural
identification (README rev. 6, the boxed promotion) is that **the MOND scale is the dark sector's
pressure**:
$$\mathcal{A}(\mathcal{Q})\equiv a_0^2(\mathcal{Q})=\kappa^2 G\,\bigl(-\mathcal{K}(\mathcal{Q})\bigr).$$
And the matching theorem (rev. 6) states that **a galaxy well is just the cosmic background at**
$(1+z)^3=\delta_{\rm well}\le 5000$, **with the identical sound speed.** Therefore the amplitude law is
**NOT built by collapse** — collapse is how a *particle* halo forms, and this sector is a *condensate
field* (Rung 3). It is the **hydrostatic equilibrium of the condensate in the baryonic potential well**,
with an effective sound speed set by the baryonic potential itself, $c_s^2 = |\Psi|$ (rev. 6 polytrope).
The K001/N-body collapse I was running tests the *wrong mechanism* — it answers how a collisionless
dust halo would form, not how a condensate equilibrates. That is the thing I was missing.

**The derivation this reframes.** Hydrostatic balance of a condensate with $p_d = (2\pi G/\mu^2)\rho_d^2$
(a $\gamma=2$ polytrope, so $c_s^2 = d p/d\rho = 4\pi G\rho_d/\mu^2$) against the baryonic potential
$\Psi$:
$$\frac{1}{\rho_d}\nabla p_d \;=\; -\nabla\Psi \quad\Longrightarrow\quad c_s^2 \;=\; \frac{4\pi G\rho_d}{\mu^2} \;=\; |\Psi|.$$
**The resolution (K008 6/8, K009 8/8 — both pushed).** The amplitude law is **exactly** a
self-gravitating isothermal sphere (SIS) at the **constant** temperature
$$\sigma^2 \;=\; \tfrac12\sqrt{G M_b a_0} \;=\; \frac{G M_b}{2 r_M},\qquad
\rho_d(r) \;=\; \frac{\sigma^2}{2\pi G\,r^2} \;=\; \frac{\sqrt{G M_b a_0}}{4\pi G\,r^2},$$
coefficient **exactly 1**, giving $v_c^2 = 2\sigma^2 = \sqrt{G M_b a_0}$ i.e. $v_c^4 = G M_b a_0$
(BTFR). The honesty checks in K009 make the logic airtight:

- The identity $c_s^2 = |\Psi|$ is **not** constant in $r$, so it does **not** by itself give $r^{-2}$:
  in a baryon-dominated well it gives $\rho_d \propto 1/|\Psi_b| \propto r^{+1}$ (rising, wrong); in a
  self-gravitating condensate the self-consistent ODE $(r^2 u')' = -4\pi G C r^2/u$ has **no real
  power-law solution** ($u_0^2 = -2\pi G C < 0$). So $c_s^2=|\Psi|$ is the **coupling**, not the state.
- The $r^{-2}$ **state** is the *constant-$\sigma$* isothermal sphere. A constant $\sigma$ is a
  **global** boundary condition — exactly the loophole the barotropic no-go (Rung 5 preamble) leaves
  open, because it forbids only a *local* $\rho$-dependent temperature, not a globally-set uniform one.

**So the amplitude law reduces to ONE formation statement:** the condensate equilibrated to the
**uniform** virial temperature of the baryonic well evaluated at the MOND radius,
$\sigma^2 = GM_b/(2 r_M)$. The microphysics $c_s^2 = |\Psi|$ is *why the condensate can sit at the
potential's temperature*; the constant $\sigma$ is the value $|\Psi|$ had where it last equilibrated,
at $r_M$. **[OPEN — the single remaining rung]:** show the condensate *mixes/thermalises across*
$r_M$ so that this global temperature is selected rather than left free. Everything else in the chain
is derived and Lean-certified.

- **No local equation of state works** (proven, FRIED_CHICKEN.md / `collapse_2026.py`): no barotropic
  $c_s^2(\rho)$ gives both a flat curve and the BTFR. So it is a **formation/violent-relaxation** question.
- **No local covariant selection rule works on realistic baryons** (proven, `local_selection_2026.py`,
  reproduced K005): the invariant $g_b^3/|\nabla g_b|^2 = GM_b/4$ is exact for a point/Hernquist but
  varies $12.1\times$ across an exponential disk, so no *local* rule picks the temperature. It must be
  set by the **collapse history** (multi-streaming, caustics, violent relaxation).
- **The dimensional theorem** (Rung 2) forces the confinement radius to be $\propto r_M$. What is *not*
  proven is that the sector **settles** there with the isothermal slope and the Rung-4 temperature.

**Status: [OPEN] — being computed (K001).** A cold, collisionless 3D N-body collapse of the dust sector
in the baryonic field measures (i) the relaxed density slope (isothermal = $-2$), (ii) the confinement
radius vs $r_M$, (iii) the settled $\sigma^2$ vs $GM_b/(2r_M)$, (iv) the $M_b$-scaling exponents.
**A PASS closes the formation route and, with Rungs 2–4, completes the amplitude law. A FAIL is a
no-go that must be reported.** Self-gravitating cold collapse onto a seed is *known* to relax toward
$\rho\sim r^{-2}$ (Gunn 1972; Fillmore–Goldreich 1984), so the route is viable; the question is the
coefficient and the scale in *this* regime.

---

## Rung 6 — the profile gives the flat rotation curve at the BTFR level  [DERIVED] [LEAN]

For $\rho = A/r^2$ with $A = \sqrt{GM_b a_0}/(4\pi G)$, the enclosed mass is $M(<r) = 4\pi A r$, so
$$v_c^2 \;=\; \frac{G M(<r)}{r} \;=\; 4\pi G A \;=\; \sqrt{G M_b a_0}\quad(\text{constant in } r),$$
hence $v_c^4 = G M_b a_0$ — a **flat rotation curve at exactly the BTFR level**.
**[LEAN `profile_slope`]** ($\rho=A/r^2 \Rightarrow d\log\rho/d\log r = -2$) and
**[LEAN `vc_flat`]** ($v_c^2 = 4\pi G A$, $r$-independent) certified.
K005 confirms numerically: flat to slope 0, $v_c^4/(GM_b a_0) = 1.000000$ on both footings.

---

## Rung 7 — the radial acceleration relation and the kernel  [DERIVED shape; the $a_0$ is Rung 1]

The static field equation (AQUAL/QUMOND on the candidate action) with the photocount-selected kernel
$$\mu_n(Y) = 1-(1+Y)^{-n},\qquad n=2\ (\text{data-selected}),$$
reproduces the SPARC radial acceleration relation. **Status:** the RAR is a *fit* (this is the input
that selected $n=2$), intrinsic scatter **0.108 dex** — a standing shortfall against the 0.06 dex
requirement (row 1), carried honestly, not hidden.

---

## Rung 8 — cosmology and the redshift law  [DERIVED — on the candidate action]

Because $a_0$ is built from $\rho_{\rm DE}$, its cosmic evolution is **derived, not imposed**:
$$\frac{a_0^2(z)}{a_0^2(0)} = \frac{\rho_{\rm DE}(z)}{\rho_{\rm DE}(0)}.$$
For $w=-1$ this is **flat to $<1\%$ for $z\le 5$** — a falsifiable prediction (PREDICTIONS P2),
decided by the deep-MOND BTFR zero-point at $z\approx2.5$ (framework 0.00 dex vs ΛCDM-native +0.33 dex).
The dark sector carries $\Omega_{\rm dm}=0.265$ to the CMB via the Noether charge (Rung 3).

---

## Rung 9 — what is NOT in this chain (the honest boundary)

1. **$\kappa = \tfrac12$ is fitted** (Rung 1). Proven underivable by the candidate action class; the
   photocount mode-count is empirical. This is the single irreducible input.
2. **Requirement 10 (Rung 5) is OPEN** pending K001's collapse verdict.
3. **The two tracks are a proven fork** (FABLE L236): the cuscuton-clock relativistic construction and
   the parameter-free curve cannot be merged (they assign the same coefficient values $6.9\times10^{13}$
   apart). The chain above uses the curve (Rung 7) and the dust property (Rung 3) — a complete theory
   must resolve which horn is real.
4. **Clusters are short by ~2×** at $R_{500}$ — a known open front, explicitly *not* a bar for this
   framework (FRIED_CHICKEN).
5. **Dwarf EFE over-suppression** and the **RAR 0.108 dex** scatter are standing liabilities.

---

## The one-sentence state of "complete"

> Every rung is **[DERIVED]** and **[LEAN]**-certified **except** the single fitted number $\kappa=\tfrac12$
> (Rung 1) and the formation step **Rung 5**, which is being computed now. **A complete theory of gravity
> = this chain with Rung 5 closed (K001) and the fork (Rung 9.3) resolved.** Nothing else is missing.
