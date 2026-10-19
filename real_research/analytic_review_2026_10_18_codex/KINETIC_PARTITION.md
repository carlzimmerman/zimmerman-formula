# A spherical kinetic model of tethered and free cold mass

18 October 2026. Candidate ZAR-K1, derived at checkpoint ZAR-2026-10-18-01. This is a separately dated effective candidate. It does not amend the frozen canonical theory.

## Target and inputs

The target is narrower than a complete theory: determine whether a warm stationary carrier can share the framework's deep total halo profile between tethered and free populations without counting the halo twice.

Use G > 0, a0 > 0, fixed point baryonic mass M_b > 0, and spherical cold densities rho_t and rho_f with enclosed masses M_t and M_f. All masses have ordinary inertia and source ordinary Newtonian gravity. Only the tethered population carries the critical repulsion and deep cubic residual. The baseline radial force is the dimensional form of [CFG747](../../campaign_fresh_gravity/CFG747_collisionless_relaxation/README.md). Extending it to two populations is a declared model choice.

This construction uses the deep cubic approximation and zero stiffness. It does not implement the full simple interpolating function, the stiffness required by Solar-System tests, relativistic lensing, or a covariant material-frame action. It is intended for the deep outer region, not near its formal point-mass center.

The distinction between response source and gravitating mass is essential. The existing [multi-current dictionary](../../sol61_push/vacuum_core_round3_2026_10_15/action_join/inputs/MULTICURRENT_DICTIONARY.md) already warns that adding neutral mass destroys the old identity between total mass source and response charge. Here the response source is M_t, not M_t + M_f.

The two-population postulate itself already appears in [the October 14 condensed-rule analysis, part c](../../campaign_fresh_gravity/THEORY_PUSH_2026-10-14/B_condensed_rule.md). The addition here is an explicit kinetic compatibility family, with its total amplitude counted once, a radial reciprocal functional, and positive stationary distributions. It is not a new discovery of tethered/free populations.

## A reciprocal spherical energy

First take smooth compact radial profiles with a regular inner cutoff, so all integrals converge and boundary variations vanish. Let dM_i = 4 pi r^2 rho_i dr. Define

\[
\begin{aligned}
E={}&K_t+K_f+\int\Phi_b\,d(M_t+M_f)\\
&-\frac G2\int_0^\infty\frac{(M_t+M_f)^2-M_t^2}{r^2}\,dr
+\frac{G^2}{3a_0}\int_0^\infty\frac{M_t^3}{r^4}\,dr,
\qquad \Phi_b=-GM_b/r.
\end{aligned}
\]

The negative term is ordinary cold gravitational energy with tethered self-gravity canceled by its critical positive interaction. The cross energy is -G integral M_t M_f/r^2 dr, and is symmetric: the free population attracts the tethered population and receives the reciprocal force. The last positive functional is the existing deep cubic push generalized to the tethered mass alone. L = K_t + K_f - (E - K_t - K_f) defines an effective nonlocal spherical mechanical action with separately conserved populations. The point baryon is an external conservative source; its reaction would require dynamical baryons.

For an energy integral int F(M_t,M_f,r) dr, moving a small tethered mass outward at radius r gives radial acceleration partial F/partial M_t. This follows because the relocation changes enclosed mass by minus the moved mass throughout the short traversed interval. Accordingly, the interaction terms give

\[
a_t=-\frac{G(M_b+M_f)}{r^2}
+\frac{G^2 M_t^2}{a_0 r^4},\qquad
a_f=-\frac{G(M_b+M_t+M_f)}{r^2}.
\]

The free acceleration follows from varying the same energy. It is not an assigned one-way reaction. The energy has no dependence on M_b in its repulsive terms and therefore does not secretly insert a baryon-temperature coupling.

This is a phenomenological nonlocal action in spherical symmetry, not new microphysics. Positivity of its cubic term does not prove positivity of the full gravitational energy or dynamical stability. Separate mass conservation does not permit automatic conversion t to f. A literal gauge-charge realization needs a charge-carrying receiver for such conversion.

## The finite-stock virial obstruction

For a stationary collisionless tethered distribution F_t(x,v), define Pi_t = int vv F_t d^3v, kinetic energy K_t, and boundary term

\[
B=\oint_{\partial V}x\cdot\Pi_t n\,dS.
\]

The stationary momentum equation div Pi_t = rho_t a_t, multiplied by x and integrated, gives

\[
2K_t=B+\int r\left[g_b+g_f-\frac{G^2M_t^2}{a_0r^4}\right]dM_t.
\]

It includes ordered rotation in Pi_t and does not assume isotropy. If the tethered profile is its exact single-population deep law, M_t = sqrt(a0 M_b/G) r, the push cancels g_b, leaving

\[
2K_t=B+\int r g_f\,dM_t.
\]

For an isolated, stationary, finite-moment, one-population system with B = 0 and no additional gravity, K_t = 0. Warm motion requires a profile departure, external/free gravity, a boundary stress, or nonstationarity. Reflecting-wall shell simulations have a boundary term and cannot be cited as satisfying the isolated hypotheses.

More generally, in the same one-population limit put q(r) = M_t/[sqrt(a0 M_b/G) r]. Then

\[
\langle v^2\rangle_t=GM_b\left\langle\frac{1-q^2}{r}\right\rangle_t.
\]

This is a weighted deficit identity. If, additionally, q >= 1-epsilon throughout the support with 0 <= epsilon <= 1, then

\[
\langle v^2\rangle_t\leq (2\epsilon-\epsilon^2)GM_b\langle1/r\rangle_t.
\]

A regular inner core generally violates the near-law hypothesis there; the identity is more useful than applying that bound indiscriminately. [CFG749](../../campaign_fresh_gravity/CFG749_angular_momentum/README.md) already found the nearly-rest requirement and escape of the tested orbiting states. This argument quantifies that mechanism; it is not a claim to have discovered the broad obstruction.

## A mixture that preserves the total deep profile

Define

\[
A=\sqrt{a_0M_b/G},\quad V_f^2=GA=\sqrt{GM_ba_0},\quad
M_t=fAr,\quad M_f=(1-f)Ar,\quad 0<f<1.
\]

The total cold mass is exactly A r for every f; the visible radial acceleration is GM_b/r^2 + V_f^2/r. Its asymptotic speed obeys V_f^4 = G M_b a0. This target amplitude is imposed in the ansatz, not selected by the action.

The population densities are b_i/r^2, with b_t = fA/(4 pi), b_f = (1-f)A/(4 pi). The forces become

\[
a_t=-\frac{C_t}{r^2}-\frac{D_t}{r},\qquad
a_f=-\frac{C_f}{r^2}-\frac{D_f}{r},
\]

where

\[
C_t=GM_b(1-f^2),\quad D_t=(1-f)V_f^2,\quad
C_f=GM_b,\quad D_f=V_f^2.
\]

Both C_i and D_i are positive. For isotropic stationary motion, the Jeans equation is

\[
\frac{d\sigma_i^2}{dr}-\frac{2\sigma_i^2}{r}
=-\frac{C_i}{r^2}-\frac{D_i}{r}.
\]

Direct integration gives

\[
\sigma_i^2=\frac{C_i}{3r}+\frac{D_i}{2}+H_i r^2.
\]

Requiring a bounded dispersion as r tends to infinity sets H_i = 0 and yields the formulas in the overview. A finite boundary generally chooses a nonzero H_i; these formulas cannot be inserted unchanged into a sharply truncated halo.

The outer relation sigma_t^2/sigma_f^2 tends to 1-f, so on this restricted branch the tethered fraction can be inferred from a **carrier** dispersion ratio rather than added as a second halo amplitude. The free and tethered populations must remain kinetically distinct:

\[
\sigma_f^2-\sigma_t^2
=\frac{f^2GM_b}{3r}+\frac{fV_f^2}{2}>0.
\]

For phases of identical carrier mass, ordinary equal-temperature equilibrium is therefore incompatible with a nonzero f on this bounded branch. This does not prohibit nonequilibrium coexistence or anisotropic finite halos. It also does not identify either dispersion with an observed stellar dispersion.

## Positive stationary phase-space distributions

Jeans moments alone need not have a positive underlying distribution. For this idealized family, positivity can be checked directly.

For either population let

\[
\Phi_i(r)=-C_i/r+D_i\ln(r/r_{\rm ref}),\qquad
\rho_i(r)=b_i/r^2,
\]

with positive C_i, D_i, b_i. Phi_i is strictly increasing from minus infinity to plus infinity. Regard rho_i as a function of Phi_i. Differentiating twice gives

\[
\rho_i''(\Phi_i)=\frac{2b_i(C_i+2D_i r)}{(C_i+D_i r)^3}>0.
\]

Define the mass distribution in phase space by

\[
\mathcal F_i(E)=\frac{1}{\sqrt8\,\pi^2}
\int_E^\infty\frac{\rho_i''(s)}{\sqrt{s-E}}\,ds.
\]

For any finite E the lower singularity is integrable and the upper tail decays exponentially. Thus F_i(E) is finite and positive. Since E = v^2/2 + Phi_i is conserved in the stationary field, this is stationary under its Vlasov equation. Its velocity integral is

\[
4\pi\sqrt2\int_{\Phi_i}^\infty
\mathcal F_i(E)\sqrt{E-\Phi_i}\,dE.
\]

Swapping the positive integrals uses

\[
\int_{\Phi_i}^{s}\frac{\sqrt{E-\Phi_i}}{\sqrt{s-E}}\,dE
=\frac\pi2(s-\Phi_i).
\]

The density integral consequently equals int_Phi^infinity (s-Phi)rho_i''(s) ds = rho_i(Phi), using the vanishing upper boundary values of rho_i and (s-Phi)rho_i'. This proves phase-space realizability in the prescribed effective forces, rather than only a formal Jeans solution.

The global family has a singular center and infinite mass. Its total energy and global virial integrals are not finite. Consequently its existence does not contradict the finite-stock virial obstruction. The compact-profile energy above supplies the force variation; its divergent value must not be evaluated on this infinite family and called a finite energy certificate.

## What remains before this is a physical theory

The exact result is a stationary **idealized kinetic family** for the stated spherical force dictionary. The following implications remain open:

1. A finite core, outer reservoir and matching conditions with positive distributions and counted stresses.
2. Stability under coupled density, relative-flow and nonspherical perturbations. Stationarity and a positive distribution do not establish stability.
3. A finite-stiffness, full-interpolation action and a relativistic stress/lensing completion.
4. A physical history selecting f and the amplitude A from independent initial conditions, plus a receiver for any lost energy or charge.
5. Candidate-matched data tests, including the known dwarf, early-type, cluster and absolute-shear failures.

The first inexpensive discriminator is analytic: try a finite matched member of this same energy model and check its distribution and boundary stresses. A failure rejects that matching construction, not the already proved compatibility identities. No simulation has been requested or launched as part of this note.
