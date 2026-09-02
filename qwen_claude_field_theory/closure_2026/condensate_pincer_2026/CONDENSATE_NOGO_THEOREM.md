# The condensate no-go theorem, stated with its hypotheses, and the one hypothesis a viable theory must break

Status 2026-09-02. Every proof step is a committed check in `condensate_mu_pincer_2026.py` (20/20),
`mond_growth_framework_footing_2026.py` (7/7), `superfluid_route_gates_2026.py` (4/4) and
`rising_a0_baryon_only_gate_2026.py` (5/5).

## Theorem

Let the dark matter required by the CMB (an $\Omega_{\rm dm}$-worth of pressureless energy at recombination) be carried
by a field $\phi$ satisfying

- **H1 (charge dust).** Its energy density on any background is the shift charge times the clock rate,
  $\rho_{\rm dust}=Q_0\,n$ with $n=K'(u)$, for some function $K$ of the excitation $u=Q-Q_0$.
- **H2 (lapse relation).** In a static well of Newtonian potential $\Psi$ the excitation is fixed by the potential,
  $u=-Q_0\Psi$.
- **H3 (charge conservation).** On the cosmic background $n\propto a^{-3}$.
- **H4 (linear growth is Newtonian).** The linear growth of $\phi$'s perturbations is governed by the Newtonian
  potential with a pressure term $c_s^2k^2$, $c_s^2=K'/(QK'')$.

Then $\phi$ cannot both (a) be cold enough for the CMB and the Lyman-$\alpha$ forest and (b) be absent from galaxies
at the 30% level inside 30 kpc.

**Proof.** By H1 and H2 the well's dust overdensity is $\delta_{\rm well}=n_{\rm well}/n_0$, and by H3 the background
reaches that charge at $(1+z_{\rm match})^3=\delta_{\rm well}$; since $c_s^2$ is a function of $u$ alone, the background
at $z_{\rm match}$ has the well's sound speed. (b) bounds $\delta_{\rm well}\le5000$ by the mass budget, so
$z_{\rm match}\le16$, and pressure support of the well (H2 with $|\Psi|\sim v_c^2$) makes that sound speed
$75$–$283$ km s$^{-1}$ for every $K$ tried, analytic or not. By H4 a fluid that hot at $z\le16$ erases the power at
$k\gtrsim1\,h\,{\rm Mpc}^{-1}$ (Parts C, F, G) and, for the quadratic and DBI cases, is hot at recombination unless
$\mu^{-1}\le0.6$ kpc, which contradicts (b). $\square$

Corollaries. (i) For the v9 DBI khronon carrying $\Omega_{\rm dm}$ the amplitude is pinned, $R=\nu_0\Omega_\Lambda/\Omega_{\rm dm}$,
and (a) already fails at $k=0.2\,h\,{\rm Mpc}^{-1}$. (ii) A superfluid that thermalises in halos is condensed on the
background (thermalisation rate grows into the past) and falls under the theorem with $K\propto|u|^{3/2}$. (iii) H4 is
the framework's own footing: its derived cosmological kernel argument carries a Hubble floor that makes MOND irrelevant
to linear growth; without the floor, no dark field and no $a_0(z)$ law reproduces the measured shape either
(tilt $\times30$–$300$ between $k=0.05$ and $10\,h\,{\rm Mpc}^{-1}$).

## Which hypothesis a viable theory must break

- **H1** is the definition of a shift-symmetric dust; breaking it means the CMB's dark matter is not a charge, i.e. an
  ordinary cold component (particles, or a field without a conserved charge). Then (b) fails by ordinary clustering
  ($\xi=1$, overshoot 2.7–4.4$\times$). Not a way out.
- **H3** is charge conservation. Breaking it needs explicit shift-symmetry breaking, $V(\phi)$; the repo's route B
  found that class phantom-only and short by 4–12$\times$ against DESI.
- **H4** is Newtonian linear growth. Breaking it with a MOND boost has now been run both with and without the derived
  floor; neither reproduces the measured shape.
- **H2** is the lapse relation, $u=-Q_0\Psi$. It holds because $\phi$ is a clock: its time translation is what a static
  well perturbs. **This is the only hypothesis whose violation is not already excluded.** A dust whose excitation in a
  well is set by the acceleration $\nabla\Psi$ rather than by $\Psi$ would not be tied to the background at any
  $z_{\rm match}$, because the homogeneous background has no gradient. The MOND phantom itself is such an object,
  $\rho_{\rm ph}=\nabla\!\cdot[(\nu-1)\nabla\Phi_N]/4\pi G$, but it vanishes on the background and so cannot supply
  $\Omega_{\rm dm}$ at recombination. A gradient-carried dust that is nonzero on the background requires a spacelike
  background gradient, i.e. a solid or aether-like medium (three fields for isotropy), whose anisotropic stress is
  constrained by the CMB. Nothing in the repo has been built on that hypothesis. It is untried, it is narrow, and it is
  the only door the theorem leaves.

## What the theorem does not touch

$a_0=\tfrac c2\sqrt{G\rho_{\rm DE}(z)}$ and the MOND phenomenology it feeds. The theorem is about what carries
$\Omega_{\rm dm}$, not about $a_0$.
