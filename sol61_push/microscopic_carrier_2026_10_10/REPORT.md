# A declared microscopic carrier, and its missing selector

2026-10-10. Started from `8459ceedd`; subsequent repository changes are unrelated concurrent work. This folder is the only write scope. This is a candidate model and analytic audit, not identification of the dark substance.

**Decision:** test a massive bosonic field in a state with many occupied modes, evolving its kinetic stress and energy current. The new work connects the candidate's support and collisions to one Hamiltonian. It also tests, and rejects in its simple form, the tempting idea that uniform dark-energy pressure confines the halo. It does not establish this field as nature's choice.

## Substance and motion

Let psi describe a nonrelativistic massive complex field, rho=m|psi|², with repulsive contact coupling g=4 pi hbar² a_s/m. Declare

\[
H=\int d^3x\left[\frac{\hbar^2}{2m}|\nabla\psi|^2+
\frac g2|\psi|^4+\rho\Phi_b+\frac12\rho\Phi_c\right],
\qquad\nabla^2\Phi_c=4\pi G\rho.
\]
Hamiltonian evolution gives
\[
i\hbar\dot\psi=\left[-\frac{\hbar^2\nabla^2}{2m}
+m(\Phi_b+\Phi_c)+g|\psi|^2\right]\psi.
\]

The field carries mass, supports multiple streams, and has a mass current j=hbar Im(psi* grad psi). Its occupied modes provide velocity dispersion; contact interactions redistribute momenta. “Cold” is a cosmological low-pressure condition, not zero motion in a halo. The equivalent quantum description has bosonic quanta; calling it a field does not establish a different observable species.

The classical equation describes a full occupied wave field, not just a ground-state ansatz. A statistical kinetic description needs a justified coarse-graining and collision operator. For weak contact interactions, Zaremba–Nikuni–Griffin's [v2 microscopic treatment](https://arxiv.org/pdf/cond-mat/9903029), equations 23, 29–33, supplies collisions among excited modes and exchange with a condensate. Replacing their external trap by self-consistent gravity is the proposed application, not their theorem. Their condensate/normal chemical-potential imbalance is an additional physical state variable; it cannot be identified with the project's settled/unsettled labels without a derivation.

This carrier is established Bose-field physics. [Levkov, Panin & Tkachev](https://arxiv.org/abs/1804.05857v2) also study gravitational kinetic condensation; their result is not a derivation of this project's halo law. No global novelty is claimed.

## How it can settle without an imposed temperature

Second moments of the mode distribution produce kinetic stress; third moments carry heat. A density-only equation omits both. For fixed baryons and a closed boundary the Hamiltonian conserves energy: inward settling must be balanced by hotter modes, outer expansion, escaping mass, or an explicitly coupled external reservoir.

The energy transfer is present in the equations themselves. With Phi=Phi_b+Phi_c, define
\[
e=\frac{\hbar^2|\nabla\psi|^2}{2m}+\frac g2|\psi|^4
+\rho\Phi+\frac{|\nabla\Phi_c|^2}{8\pi G},
\quad
\mathbf Q=-\frac{\hbar^2}{m}\mathrm{Re}(\dot\psi^*\nabla\psi)
-\frac{\dot\Phi_c\nabla\Phi_c}{4\pi G}.
\]
Direct differentiation of the field and Poisson equations gives
\[
\boxed{\partial_t e+\nabla\cdot\mathbf Q=\rho\dot\Phi_b}.
\]
Integrating gives H when the gravitational boundary term vanishes. This is a concrete energy current for the earlier [counter-transport proposal](../counter_transport_2026_10_10/REPORT.md). Outward current is possible, not guaranteed: its sign and magnitude must emerge from the state. A core exporting energy can contract while the recipient envelope expands. No such evolution has been simulated in this checkpoint, and it does not by itself select the required profile.

The local excited-mode collision operator conserves number, momentum and kinetic energy in each elastic encounter. A prescribed relaxation toward the desired Jeans dispersion is therefore not a derived substitute for it. The one-particle kinetic description, contact mean field, and condensate exchange must be kept mutually consistent, without double counting wave correlations.

## New linked test: one coupling sets pressure and scattering

For fixed local pair-correlation factor chi,
\[
P_{\rm int}=\frac{\chi g\rho^2}{2m^2},\quad
c_{\rm int}^2=\left.\frac{\partial P_{\rm int}}{\partial\rho}\right|_\chi
=\frac{\chi g\rho}{m^2},\quad
\sigma_{\rm scat}=8\pi a_s^2.
\]
The displayed deterministic field equation has its unaveraged quartic stress. Chi=1 describes the coherent closure; chi=2 requires a separate incoherent Gaussian ensemble closure with rho=m times the mean number density. It is not a substitution into the same single-wave equation. A general evolving state need not keep either value. Eliminating a_s proves
\[
\boxed{\frac{\sigma_{\rm scat}}m
=\frac{m^5(c_{\rm int}^2)^2}{2\pi\chi^2\hbar^4\rho^2}}.
\]
The cross section is the low-energy identical-boson contact result, not a Bose-enhanced transport rate. Thermalization, condensation and heat conduction require their respective occupation-weighted collision integrals; they are not interchangeable clocks.

At the previously audited mass 0.62 eV/c² and the **inherited illustrative** sigma/m=1 cm²/g, the generous chi=2 pressure gives:

| Benchmark | rho, kg/m³ | Comparison speed | Contact pressure speed |
| --- | --- | --- | --- |
| CFG428 density/velocity | 1.30665e-24 | 1000 km/s | 0.134 m/s |
| Declared galaxy example | 1e-21 | 200 km/s | 3.71 m/s |

These are not new empirical bounds or measured galaxy parameters. They show that this eV candidate, at that scattering strength, must obtain practically all halo support from orbital/kinetic stress, not contact pressure. The contact-speed-squared ratios are approximately 1.79e-14 and 3.43e-10 respectively. The dilute and low-energy contact conditions are comfortably satisfied at the adopted coupling. The arithmetic is checked independently in `check.py`; `run/manifest.json` pins the execution.

This is more restrictive than assigning a density profile and then choosing an unrelated pressure and settling rate. A change in the microscopic coupling changes both. It is an algebraic consequence of known interaction physics, not a new fundamental interaction.

## The vacuum-confinement route was checked too

For a thin spherical wall of tension T between vacuum energy densities epsilon_in and epsilon_out, normal stress balance is
\[
P_c(R)=\epsilon_{\rm in}-\epsilon_{\rm out}+2T/R.
\]
The vacuum pressure is negative. Equal vacuum inside and outside cancels; a positive gas confining pressure cannot simply be set to rho_DE c². A higher-energy interior or a wall could provide confinement, but their action and stability would be additional physics. This is local boundary stress balance, not a claim that cosmological vacuum energy has no gravitational effect.

An exact coefficient check is revealing. At the marginal point of a self-gravitating, pressure-confined regular isothermal sphere, the isothermal equations and mass turning condition give g_c(R)²=8 pi G P_s. Thus, if P_s=beta rho_DE c² and the cold edge circular speed is identified with the target speed, kappa=sqrt(8 pi)(M_c/M_b)sqrt(beta). Taking beta=1 and kappa=1/2 requires M_c/M_b=0.0997. The baryonic gravity then dominates, violating the cold-self-gravitating approximation used in that calculation. A joint baryon–fluid–wall calculation would be a new model, not a correction of that coefficient.

Derivation: use xi² psi'=m(xi), m'=xi² exp(-psi); at fixed sound speed and surface pressure the critical mass extremizes m exp(-psi/2), giving m²=2xi⁴ exp(-psi). With R=a xi and P_s=rho_center exp(-psi) sigma_v², elimination yields the stated 8 pi identity. The boundary problem is [Bonnor's pressure-confined sphere](https://articles.adsabs.harvard.edu/pdf/1956MNRAS.116..351B). This is a conditional identity, not a viable dark halo model.

## The remaining selector is explicit

The microscopic Hamiltonian above has **no vacuum-dependent coupling and no target density**. Adding a constant vacuum term does not change its local matter equation. It therefore cannot presently derive why a halo should select V_f^4=G M_b a0, why a0 tracks rho_DE, or why kappa=1/2. A uniform-vacuum term still affects spacetime on cosmological scales; claiming a derived local halo normalization requires showing that channel rather than ignoring it or assuming the answer.

Nor is the exact exponential kernel's inner isotropic-density obstruction removed: see the earlier [kinetic gate](../cold_field_identity_2026_10_10/KINETIC_GATE.md). Anisotropic or nonequilibrium states remain possible. A single stationary condensate is not an adequate substitute for the multimode calculation.

**The efficient research decision:** use this Hamiltonian as a declared carrier test, not as a finished theory. Before a large simulation, derive the heat-current closure in its valid regime and check its relaxation and merger scales with one common m and a_s. Then test the density across distinct initial energies and baryonic masses, without putting rho_ph or a Jeans target into the evolution. If agreement requires separately retuning the initial energy, boundary, or mode population for each galaxy, this mechanism has fitted rather than explained the law. A successful density result must then be connected to a specified vacuum coupling in the same theory.

Independent read-only reviewers verified the pressure/scattering elimination, dimensions, and energy-current signs. The field route and vacuum-boundary route were checked independently against the prior CFG288, CFG428, CFG461, CFG490 and Sol61 support/transport work. The final model remains conjectural; no microscopic mass/species, abundance, stable halo attractor, kappa, or 32pi-squared coefficient has been identified.
