# Finite halo closure, thermalization, and vacuum heating

## Outcome

The finite, stationary, impermeable pressure boundary does not close the current
annihilating-fluid/heating-only model. Its boundary energy equation requires
net cooling, whereas the assumed radiation deposits positive heat. This rules
out that specific completion before a stability claim can be made. Capture
and thermalization also require independent optical depths and reaction-rate
hierarchies that have not been selected.

Constant vacuum energy cannot continuously supply the required local heating
power. A converting or decaying vacuum phase can supply energy, but its rate,
phase difference and depletion history remain additional inputs. Consequently
no finite stable halo or coefficient1/2 has been derived. The previous outer
flat-tail calculation remains a conditional asymptotic balance only.

Base8231467796; fixed contract001d6c981d. This result narrows the model's status;
it is not a no-go theorem for every open, conducting, cooling, or time-dependent
halo. No adopted action is changed.

## 1. A finite-boundary obstruction independent of the density ansatz

Use the same steady spherical equations as TRANSPORT_CAPTURE_RESULT.md:

    (r^2 n u)'/r^2 = J-K n^2,
    n c_v u T' + P div(u) = H_net,  P=n kB T.

The energy equation includes the removal of annihilating particles with their
mean kinetic energy; treating their disappearance as extra cooling of the
remaining particles would double-count that sink at constant s-wave rate.
Assume a fixed outer wall R beyond local production, smooth one-sided fluid
fields, J(R)=0, u(R)=0, n(R)>0, T(R)>0, K>0. At that wall continuity gives

    u'(R)=-K n(R),  div(u)|R=-K n(R).

The advected temperature term vanishes for finite T'. Therefore

    H_net(R)=-K n(R)^2 kB T(R) < 0.

The gas slows toward the impermeable wall while annihilating; the resulting
compression requires cooling. A model with only nonnegative radiative heating,
no conduction and no additional cooling cannot meet this boundary condition.
This conclusion uses neither an imposed1/r^2 density nor a particular gravity
law. It is an incompatibility of the assumed smooth stationary boundary and
the number/energy equations.

A singular boundary layer, a permeable boundary, nonzero local particle source,
conduction, viscosity, or an additional cooling process changes the problem.
So does a zero-density/zero-temperature surface. None is supplied by the
previous positive-temperature isothermal tail and fixed phase pressure. They
must be modeled, not inserted after solving the outer balance. A constant
vacuum on both sides does not provide a positive confining pressure either.

### Explicit check using the preceding outer profile

For n=A/r^2 and u(R)=0, continuity gives exactly

    u=K A(1/r-1/R).

With halo gravity v_h^2/r, v_h^2=4 pi G m A, momentum requires

    T(r)=m v_h^2/(2 kB)
         -m K^2 A^2/(4 kB r^2)
         +m K^2 A^2/(3 kB R r)+C r^2.

C would be fixed by thermal boundary data. Direct substitution into the energy
equation reproduces the negative required boundary heating for every choice
with T(R)>0. Adjusting C or the pressure cannot evade this sign. The profile
also neglects its core and central baryon gravity; the general boundary
argument above does not require those approximations.

A stability spectrum about this inconsistent stationary completion would be
meaningless. No finite stable halo is claimed on the strength of the earlier
local two-variable attractor or the outer asymptotic tail.

## 2. Capture and thermalization must meet simultaneous conditions

The prior result derives the portal capture cross section and energy-loss
criterion. Successful capture requires a sufficiently large baryonic column,
appropriate mass ratio and scattering energy transfer, or particles born bound.
Those inputs are not fixed by dark-energy density. Gravitational focusing alone
does not convert positive orbital energy into negative orbital energy.

For material relaxation, add the already-allowed quartic
-lambda_self chi^4/4!. Its nonrelativistic identical-particle elastic cross
section is lambda_self^2/(128 pi m^2) in natural units. Compare with the
annihilation coefficient K=lambda^2/(64 pi m^2). For relative particle speed v,

    Gamma_el/Gamma_ann
      = [lambda_self^2/(2 lambda^2)] (v/c).

Cold particles have v/c much less than1. Equal-order couplings do not imply
rapid thermalization before annihilation. Many elastic collisions before
particle loss require a correspondingly larger lambda_self/lambda, as well
as enough time and density. The independent stabilizing quartic is not selected
by the heating/annihilation coupling cancellation.

For a1/r^2 tail, material-fluid closure requires a short mean free path,
roughly n sigma_self r much greater than1, while optically thin central heating
requires a small integrated radiation optical depth. From the microscopic
radiation cross section,

    sigma_self/sigma_rad
       = [lambda_self^2/(8 lambda^2)] [1+2E/(mc^2)].

These conditions can be expressed as a parameter hierarchy; they have not been
shown to hold in one actual halo. Making a material collision rate large also
requires checking the mediator/particle EFT and transport effects. Hard recoil
from E comparable to mc^2 may eject a particle before its energy is shared;
soft radiation reduces recoil but changes the heating efficiency zeta. A bound
halo needs relaxation faster than loss and relevant dynamical times, with an
actual spectrum and capture supply. No numerical parameter window is claimed
from these inequalities alone.

## 3. Does the vacuum supply the luminosity?

For a vacuum stress tensor T_vac^{mu nu}=-V g^{mu nu}, metric compatibility gives

    nabla_mu T_vac^{mu nu}=-nabla^nu V.

With total stress-energy conservation, matter receives the opposite divergence.
A spacetime-constant V gives no local transfer source. In a local rest-frame
energy equation, vacuum decay supplies q=-dV/dt. Thus the cosmological vacuum
energy density is not, by itself, a continuously available heating luminosity.
Expansion and pressure-volume work do not justify inventing a local radiation
source in a fixed halo. Time-dependent scalar excitations or couplings would
be additional components beyond the constant-vacuum term.

This identity is the relevant distinction in interacting-vacuum theories;
see [Inhomogeneous vacuum energy](https://arxiv.org/abs/1203.6776) for context.
Its abstract was checked for the interacting-vacuum framework; the local
conservation identity used here is derived explicitly, not assumed from it.

### Phase conversion can release energy, but does not fix power

Let DeltaV be the higher-minus-lower vacuum energy density and let V_conv(t)
be the volume converted to the lower-energy phase. Available latent power is

    L_available=DeltaV dV_conv/dt.

For a spherical conversion front of radius R_f,
L_available=4 pi R_f^2 DeltaV R_f_dot. A static front has no continuing latent
power. For a finite available volume V_res, total latent energy is at most
DeltaV V_res; a sustained luminosity L depletes it on DeltaV V_res/L unless
there is a separately specified replenishment process. DeltaV need not equal
the external cosmological vacuum energy density rho_DE c^2.

One can make the rate dependence explicit in a thin-wall, weak-gravity,
zero-temperature tunneling illustration. A four-dimensional Euclidean bubble
has action difference

    B(R)=2 pi^2 Sigma R^3-(pi^2/2) DeltaV R^4,
    R_bounce=3 Sigma/DeltaV,
    B_bounce=27 pi^2 Sigma^4/(2 DeltaV^3).

The semiclassical exponential suppression depends on the barrier/wall tension
Sigma, not just the vacuum levels. The prefactor and cosmological/thermal
environment are further inputs. This analytic example is not a computed
nucleation history for our model, and its bounce is not a stable halo wall.
Changing the potential barrier while keeping its minima fixed changes the
conversion rate. No unique luminosity follows from the two vacuum densities.

## 4. Relation to the proposed normalization

The conditional outer-tail relation remains

    v_flat^4=2 G zeta L_a/c.

Producing the requested coefficient would require

    L_a/Mb = c^2 sqrt(G rho_DE)/(4 zeta).

This equation states the missing requirement; it is not used to choose a
luminosity or reaction rate. If a finite spherical phase reservoir supplied
that luminosity, its formal depletion time would be

    t_deplete = 16 pi zeta DeltaV R^3
                 /[3 Mb c^2 sqrt(G rho_DE)].

It is not universally a galaxy lifetime, nor does it select R, DeltaV or zeta.
For a decay prescription q=gamma DeltaV, the available luminosity is instead
gamma DeltaV V_res, retaining the independent rate gamma and reservoir volume.
Picking them to satisfy the required luminosity would insert the target.
Constant vacuum gives no such source at all.

The kinematic upper bound zeta<=1/2 from the previous scattering calculation
still is not the MOND normalization. Neither finite-wall matching nor vacuum
energy conservation turns that bound into the requested coefficient.

## Evidence and disposition

finite_halo.py passes12 exact checks of finite-wall continuity, momentum and
energy, cross-section/rate ratios, and reservoir accounting. The deliberate
omission of boundary compression fails the intended energy identity. Both
manifests are retained and validated. The covariant conservation argument and
thin-wall rate illustration are analytic, self-reviewed reasoning; no global
simulation, independent audit or full capture calculation is claimed.

The current positive-heating, impermeable finite-wall completion is ruled out
under the stated assumptions. Capture and thermalization remain requirements,
not completed results. A conducting/cooling boundary layer, an open reservoir
or time-dependent vacuum conversion could change the model, but each requires
additional interactions, rates and boundary conditions. Their numerical
solutions cannot be inferred from the analogy or chosen to enforce1/2.
The finite stable halo and vacuum-luminosity selector therefore remain open;
this checkpoint explicitly supersedes any interpretation that the outer
flat-tail balance already established a viable finite halo.
