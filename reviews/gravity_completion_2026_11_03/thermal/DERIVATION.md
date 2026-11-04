# TH07 thermal-vacuum discriminator

The cold zero-temperature vacuum cannot simply be inherited by a populated
hidden messenger bath. This statement is a static force calculation; it does
not establish loss of the vacuum in a nonequilibrium cosmological history.
The chosen initial temperature ratio xi=T_D/T_SM=.02 is an independent input.

The executed gas free energy is

    F_th(X,T_D) = T_D^4/(2 pi^2)
       [sum_physical_bosons n_b J_B(m_b^2/T_D^2)
        -sum_Weyls 2 n_f J_F(m_f^2/T_D^2)].

J_B(y)=integral_0^infty dx x^2 ln(1-exp(-sqrt(x^2+y))) and
J_F(y)=integral_0^infty dx x^2 ln(1+exp(-sqrt(x^2+y))).
[SOURCES.md](SOURCES.md) authenticates the integral, signs and dof factors.
The fermion contribution is negative because J_F is positive.
The code computes its derivative directly from occupation integrals and the
Hellmann–Feynman mass derivative; pressure constants are removed only for
X-dependent potential comparisons. Energy is rho_th=F_th-T dF_th/dT and
entropy is -dF_th/dT, including the X-independent pressure.

The SU3,SU2 and broken representation blocks have multiplicities 8,3,12.
Every broken block has four real tree scalars, of which exactly one is the
removed gauge Goldstone; it also has three Weyls and one massive vector.
SU3/SU2 each have four real scalars and two Weyls. Singlets contribute six
real scalars and three Weyls. The unbroken gauge sector has twelve Weyls and
twelve two-polarization vectors. Total counts: 86 physical real scalars,
73 Weyls (146 spin degrees), 60 vector polarizations; total boson/fermion
counts are both 146. At X=0 the broken 3x3 fermion block has one additional
zero mode per representation component, hence twelve additional massless
Weyls. They are retained. The constant light collective and Goldstino/gaugino
pressures do not generate an X force. At these temperatures their finite
sub-GeV masses have negligible effect on the messenger force; exact physical
super-Higgs pole matching remains an earlier independent obligation.

The vacuum comparison uses the actual preferred canonical/protected finite
packets. Exact microscopic neutral tree SUGRA plus full rigid one-loop CW is
evaluated globally on the rigid valley. Finite linear-normal/two-loop action
terms are evaluated only within their recorded coefficient domain; the local
radial masses reconstruct as .00645258803570 and .443208797969 GeV, respectively,
versus preferred .00645258820631 and .443208777437 GeV. Protected tau is held
fixed in that local check; its heavy response is negligible at the tested
accuracy. The global leading minimum differs from the finite point by .0344%
canonical and .00917% protected. This is explicitly a leading global thermal
profile; it is not a new all-field two-loop thermal phase diagram.

Executed static results, e=h=lambda=.003, g=sqrt(29/200)e:

| Quantity | Canonical | Protected |
|---|---:|---:|
| mu GeV |544638.2664|18170662.1115|
| cold outer minimum disappears, T_D GeV |376.4902|19328.7314|
| field there, X/X_vac |1.08946|1.27367|
| small-field thermal minimum disappears, T_D GeV |2538.0557|84625.4652|
| field there, X/X_vac |.0095971|.00743734|
| zero-T excess at small-field loss, GeV^4 |8.61190e13|1.06934e20|
| excess/rho_SM at xi=.02 |9.45514e-9|9.49920e-9|

These are unresummed numerical spinodal estimates, not precise transition
predictions. The CW origin curvature with respect to X/mu is
-2.06517244e-10 mu^4 for both points; the much smaller outer-vacuum radial
mass does not set the origin restoring scale. W0 supplies an explicit negative
small-X force, so the origin thermal minimum is displaced and vanishes by
merger with a nearby maximum. It is not fixed exactly at X=0.

The first scan covers 100 temperatures T_D/mu in [2e-6,.3], with nonnegative
physical tree spectra on X in [0,2.1X_old]. A second scan checks 60 logarithmic
fields from 1.5X_vac to 1e5X_old at six temperatures. At T_D/mu=.0015,.004,.005,
.008 all 60 force samples point outward for both gravity points. At .03 an
initial inward force changes to outward, providing a barrier. The far-field
SU3/SU2 seesaw masses become lighter; high-temperature entropy therefore does
not guarantee a unique globally favored near-origin state. The widest field
remains X/Mp<2e-5. This is finite sampled force evidence, not a universal
runaway theorem. Version 2 uses determinant-preserving two-by-two eigenvalues
and derivatives to avoid cancellation in the far seesaw limit.

There is an equilibrium window between small-field release and recovery of
the cold local vacuum with no local minimum in the tested range. A real bath
need not remain in chemical equilibrium during this roll. Frozen charged
fermion occupations can supply an inward mass force rather than the decaying
Boltzmann force of equilibrium. The separate thermal_kinetic sibling owns
that dynamical control. No excluded thermal-reheating history is inferred
from the static equilibrium profile alone.

The energy excess at the small-field spinodal is only about 1e-8 of the hotter
visible radiation for the chosen xi. A false-vacuum energy catastrophe is
therefore not a valid obstruction here. The independent thermal_review sibling
computes the comoving-energy gate and uses the same energy/free-energy
separation. No chosen xi, portal, entropy ratio or final photino FD population
has been derived.

Ring/Debye corrections and gauge dependence matter when extracting an almost
vanishing curvature. The gas is a leading weak-coupling diagnostic, not a
screened model-specific thermal action. Vacuum SUSY cancellations do not
cancel bosonic versus fermionic thermal occupations. At the small-field loss
rho_th/F_hidden^2 is of order 5e-7, yet the thermal force can exceed the tiny CW
restoring force. Planck-suppressed modulus/gravitino equilibrium is not assumed
by specifying the rigid SU5 bath. Kinetic population and inverse reactions,
thermal normal response, and finite self-energies remain necessary for a
physical reheating/photino production history.

# TH07C low-reheat charged-parent decay tail

The surviving cold branch may instead be initialized with reheating below its
outer thermal spinodal. This is a distinct, executable producer test. The
U1 photino tree vertex couples only the broken charged sector; the much lighter
SU3/SU2 seesaw adjoints commute with U1 and are not tree U1-photino parents.
The actual preferred cold points have minimum participating parent masses
23504.70 GeV canonical and 698771.15 GeV protected. The minimum charged daughter
is a scalar 23205.86 GeV/687652.40 GeV, consistent with the coordinator's separate
charge-ordering calculation. A decay into chi retains a charged companion.

The physical real-scalar basis is formed by removing the twelve independent
gauge-orbit vectors from the 98-real Hessian. The 84 nonzero eigenstates plus
two physical flat directions give 86, and the measured projector residual is
below 1.1e-12. This matters: treating the twelve massless Goldstones as scalar
daughters would create unphysical heavy-fermion decay channels.

For L=-S y chi Psi+h.c. with distinct Majorana/Weyl species and massless chi,
the spin traces give

    Gamma(S -> Psi chi) = |y|^2 MS/(8pi) (1-MF^2/MS^2)^2,
    Gamma(Psi -> S chi) = |y|^2 MF/(16pi) (1-MS^2/MF^2)^2.

The second formula averages the initial fermion spin; the source later counts
its two spin degrees. No identical-chi factor is inserted for this distinct
pair. Projected actual couplings are obtained directly from the TP03 field
tensor, gauge Yukawa derivative and physical mass bases, without fitting a
decay width. The total squared U1 Yukawa norm is 1.9575e-5. Its all-real-scalar
basis-invariant bound 2g^2 Tr(R_U1^2)=2.61e-5 is checked; Tr(R_U1^2)=10 for the
two matter adjoints in these conventions.

Using equilibrium MB parents, zero initial chi, fixed cold spectrum and
constant xi=.02, g_sSM=g_rhoSM=106.75, the leading source is

    gamma_chi = sum gP MP^2 TD GammaP K1(MP/TD)/(2pi^2),
    Ychi = sum [45 gP Mp xi^5 GammaP /
          (4pi^4 gs sqrt(pi^2 grho/90) MP^2)]
             integral_(MP/TR)^infinity dx x^3 K1(x).

Here Mp is the reduced gravitational Planck mass; MP denotes each parent
mass. The xi^5 factor follows from visible entropy and the visible-dominated
Hubble rate. The Hall et al source is authenticated in SOURCES; the independent
integral_0^infinity x^3 K1(x)dx=3pi/2 is numerically checked in the fresh second
run. A final FD photino distribution is never imposed.

At the maximum cold-branch reheat temperature, the computed fixed-spectrum
source gives Ychi=7.80345e-31 canonical and 2.99966e-21 protected. These are
4.62958e-26 and 6.70354e-15 of the required density, respectively. The actual
chemical source diagnostic gamma/(n_chi,FD H) is 1.50554e-21 and 3.26105e-12.
The FD number in this denominator is a rate-comparison convention; it is not
an assigned final abundance. Source values at .25,.5,.75 of each reheat limit
are even smaller. Individual charged parent partial widths can exceed H;
that does not make the exceedingly rare population equilibrate chi.

A deliberately generous conditional envelope places all 292 physical
scalar/fermion/vector degrees at the lightest charged scalar and takes every
Gamma/M=.0009=100e^2, much larger than the computed scalar/fermion Yukawa norm
permits. It still gives only 1.10e-16 canonical /7.65e-6 protected of the target.
This envelope is stated as a width assumption, not an all-orders rate bound.
Real equilibrium outer-vacuum shifts increase the relevant broken-sector
masses, but a full source integrated along that branch is not asserted here.

Frozen parent populations need separate bookkeeping: their initial thermal
number can survive after equilibrium density decreases, so an equilibrium
source integral alone is not a rigorous bound on all such late decays. The
preferred second run records both initial decaying-parent yields and a much
looser all 292 initial-tail bound. This closes neither arbitrary reheating
above the static spinodal nor loop-induced neutral-adjoint cascades, which
were not included. Such cascades and their stable companion/entropy/velocity
budgets require actual rates and transport. The main reheated charged-parent
cold-vacuum hypothesis at xi=.02 cannot supply the target abundance within
this computed leading source, while the broader thermal route remains open.

For completeness, the maximum-reheat initial thermal numbers of the actual
decaying parents are 1.25552e-31 canonical /1.53086e-20 protected per visible
entropy. Even assigning all 292 degrees to the lightest charged mass gives only
2.69044e-30/2.50769e-19. Late decays of those frozen initial parents therefore
do not rescue this specified thermal-tail source. They do not bound an
arbitrarily externally prepared mother population.

The exact residual U1 companion obligation is recorded by the coordinator in
[CHARGED_RELIC.md](../CHARGED_RELIC.md), with full charge-squared classification
in [run_charged/result.json](../run_charged/result.json). A charged decay chain
cannot end entirely in neutral chi/gauge particles. For a source making all
chi, a 10% charged-mass allowance requires surviving N_C/N_chi<=1.115e-10
canonical /1.417e-10 protected. This is a required annihilation/depletion
calculation, not a theorem that it fails.
