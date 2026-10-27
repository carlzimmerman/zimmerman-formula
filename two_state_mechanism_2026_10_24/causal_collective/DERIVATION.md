# Causal collective field: a Hamiltonian candidate and its limits

This is a conditional construction, not a claim that nature contains the chosen
medium. The adopted spherical acceleration relation and a0 remain inputs. A
critical excitation spectrum is inferred as a necessary scaling, not derived
from an independently established microscopic material.

## 1. Degrees of freedom, charge and action

Keep Maxwell variables A,D, B=curl A and explicit free carriers T(+q,m),
C(-q,epsilon*m). Add neutral bound pairs with an isotropic internal four-level
system: singlet |0>, excited vector |i>, i=1,2,3, of gap Delta. Its dipole
operator is d_i=d(|0><i|+|i><0|). A vector electric field couples the ground
state to its bright excited state; two perpendicular states remain dark. This
avoids assigning every fixed dipole a preferred spatial direction.

For normalized internal amplitudes c and number density n, let

    P_i = integral 2 n(Delta) d(Delta) Re(c0* ci) dDelta.

In rationalized units hbar=c_light=1, the local Hamiltonian is

    H = integral [ |D-P|²/2 + |B|²/2
                   + integral n(Delta) Delta sum_i |ci|² dDelta ] d³x
        + sum_free sqrt(m_a²+|p_a-q_a A|²).

Rest-mass subtraction is optional for an energy diagnostic, never a source of
reaction energy. The corresponding canonical action has -D.Adot, the usual
i n c_dagger cdot internal-state term (real symmetrized form is equivalent),
particle p.xdot, minus H, and a multiplier imposing div D=rho_free.
It gives E=D-P=-Adot-grad phi, Maxwell evolution and

    i cdot = [Delta sum_i |i><i| - d E_i(|0><i|+|i><0|)] c.

All displayed field and excitation energies are nonnegative. Coupling and
internal energy are derived together; there is no subtraction of polarization
work to make a state transition easy. Microscopic stabilization, the origin of
the level spectrum, and gravitational medium dynamics remain separate inputs.

The total coarse-grained gauge charge/current are

    rho_total=rho_free-div P, j_total=j_free+Pdot,
    div E=rho_total, partial_t rho_total+div j_total=0.

Each free T,C pair has equal opposite charge; internal excitation of a bound
neutral pair creates NO free monopole charge. This is not an ionization channel.
An eventual F<->T+C conversion must supply its own derived bound/continuum
states and energy/momentum-conserving matrix element. No conversion rate or
tethered-mass fraction is assigned by this model.

## 2. Causality and energy

Maxwell's equations contain the spatial derivatives; the local internal-state
and homogeneous carrier equations contain none. In the rest frame of a causal
local medium the principal electromagnetic characteristic speeds are +/-c_light,
with zero-speed local internal variables. For mobile carriers use relativistic
kinematics so |v|<c_light. This is a causal field-plus-local-response system;
it is not a full gravitational/cosmological UV completion. It replaces the old
instantaneous constitutive action and does not preserve its high-field cap.

The energy identities are

    partial_t[(E²+B²)/2]+div(E cross B)=-E.(j_free+Pdot),
    partial_t U_internal=E.Pdot,
    partial_t K_free=E.j_free,

with particle flux terms when matter transports. Their sum conserves energy.
The homogeneous nonlinear tests have B=0, explicit positive/negative momenta,
and no external drive, damping, energy projection or frozen countercharge.

At small amplitude, each internal mode gives

    Pj_ddot+Omega_j² Pj=f_j E, f_j>0.

For a transverse Fourier mode add a free plasma current Jdot=omega_p² E. In
energy-normalized variables (E,B,Omega_j Pj/sqrt(f_j),Pj_dot/sqrt(f_j),J/omega_p),
the generator is anti-Hermitian. Its eigenfrequencies are real. Only the E/B
block depends on k; the Hermitian derivative matrix has operator norm c_light.
Hellmann-Feynman therefore bounds every differentiable branch's group speed by
c_light. At crossings the one-sided eigenvalue slopes obey the same norm bound.
The finite linear test checks this and an exact single-oscillator polariton
formula. The causal argument is the principal-symbol/energy argument, not a
claim that testing finitely many wave numbers proves all propagation properties.

## 3. Static response, and why a critical spectrum is needed

At imposed E the internal ground eigenvalue is
(Delta-sqrt(Delta²+4d²E²))/2. Differentiation yields the isotropic ground response

    P_Delta=n d E/sqrt(E²+s²), s=Delta/(2d).

For a single finite gap this has an analytic odd expansion P=chi E-O(E³).
Cold spherical positive-carrier balance g=(q/m)E, after cancellation of the
leading Newtonian term, then gives g_b proportional to g³. The desired deep
relation g_b~g²/a0 cannot arise from this gapped analytic branch.

Suppose the dipole-weight density over s behaves as n(s)d~s^p near zero. For
0<p<2, subtracting the linear susceptibility and substituting s=|E|t gives
chi E-P proportional to E|E|^p. Thus the desired exponent requires p=1.
This fixes an exponent condition; it does not explain a microscopic critical
state or why every disk would occupy it.

Choose the simplest finite-cutoff realization n(s)=A s for0<s<s_max, with a
common matrix element d. Define chi=A d s_max and u=E/s_max. Integration gives

    P/E=chi [sqrt(1+u²)-|u|],
    D=E+P,
    ell(E)=E²/2 + chi*s_max²/3 [(1+u²)^(3/2)-|u|³-1].

Here n(s) is number density per unit s; equivalently with dimensionless s/s_max,
the density coefficient is chi*s_max/d. The code sets s_max=d=1. The Legendre
energy is E.D-ell, equal to field+excitation energy on the ground branch.
Both D'(E)>=1 and D/E>=1: a passive Maxwell medium does not inherit the previous
maximum-D constraint. The old compulsory-core bound must NOT be reused here.

For a lower cutoff eta_s=s_min/s_max, keep the same zero-field chi by normalizing
the spectrum. Then

    P/E = chi*(1+eta_s)/[sqrt(1+u²)+sqrt(eta_s²+u²)].

Any nonzero lower gap ultimately restores the cubic low-field source relation.
The finite quadrature used in dynamic tests has a positive smallest gap. It
does not establish the gapless adiabatic limit used in the continuum static fit.

## 4. Matching gravity removes independent charge and cutoff scales

Write beta=q/m, epsilon_r=1+chi. At weak field the effective repulsion is
q²/(4pi epsilon_r r²). To cancel T's own Newtonian attraction at leading order,

    beta²=4pi G(1+chi).

This replaces the vacuum normalization from the previous action. It must not
be combined with that earlier q/m value. Define f=chi/(1+chi) and g_star=beta*s_max.
For cold spherical T, no enclosed free countercharge, and negligible additional
gravitational acceleration from the neutral medium, Gauss's law and force
balance give

    g_b = f*g [1-sqrt(1+(g/g_star)²)+g/g_star].

Matching the deep coefficient fixes g_star=f*a0. One dimensionless static
parameter chi remains. The high-field limit is g/g_b ->1+1/chi, so exact
Newtonian recovery is not obtained at finite chi on this branch. A finite
tolerance may permit approximate agreement; the scan reports calibration to
the target relation, not an observational likelihood or parameter derivation.

If the medium's gravity is appreciable, the left-hand side is instead the total
non-T gravitational source S=g_b+g_medium+g_other. The static curve must not then
be presented as a baryon-only acceleration relation. The mass-budget test below
does not prove the required negligible-medium-gravity condition; this is a
separate consistency obligation. A homogeneous cosmological background may
require a different treatment, but would supply a different density/locality
constraint rather than permission to discard a clustered medium's gravity.

Exact reproduction of the old relation at all fields is impossible for this
passive ground-state medium. It would require
D(E)=epsilon_r E/(1+beta E/a0), whose derivative drops below1 at
g/a0>sqrt(epsilon_r)-1, contrary to passive ground-state D'>=1. Over a finite
range this is a necessary susceptibility bound for EXACT matching, not the
same as a tolerance-based approximate fit.

## 5. Matter inventory and oscillator strength constrain response time

Assume the neutral modes are built from the same charge carriers, each pair of
mass (1+epsilon)m, with dipole matrix element d=q*l. For the critical spectrum,
total bound-pair number density is n_bound=chi*s_max/(2d). Hence

    rho_bound*l = (1+epsilon)*f²*a0/(8pi G).

This is a required polarization mass budget, not additional invisible matter
that can be added freely. Assigning all available dark mass to the medium gives
an optimistic minimum l. If l is comparable to the system size, the point-local
dipole approximation fails. Changing microscopic l by galaxy would defeat the
universal mechanism. With fixed l,chi and the matched cutoff, the required
medium density is fixed too; local density variations generally change chi.

For canonical charged constituents, the dipole oscillator-strength sum rule
follows from [x,[p²/(2mu)+V(x),x]]=hbar²/mu:

    sum_n (E_n-E_0)|<0|q*x|n>|² = q²*hbar²/(2mu).

For a medium this bounds total susceptibility oscillator strength by
sum_j f_j <= n_bound*q²/mu, with mu=epsilon*m/(1+epsilon) in rationalized units.
The critical spectrum has uniform dchi/d(s/s_max), giving
sum_j f_j=chi*Omega_max²/3, Omega_max=2d*s_max/hbar. Consequently

    Omega_max² <= 12pi G rho_bound/(epsilon*f).

The bound assumes the canonical constituent description and a complete positive
oscillator-strength inventory. Other low-energy models must derive their own
sum rule; they cannot claim this bound while arbitrarily exceeding its strength.

With rho_bound <=3 eta Mb/(4pi b³), eta=5.364,

    (Omega_max*t_dyn)² <= 9eta/[(1+eta)*epsilon*f].

The modes contributing the nonanalytic response at x=g/a0 have s/s_max~x/f;
their field-dressed mixing frequency is approximately sqrt(2)*Omega_max*x/f.
At sufficiently small x they cannot track an evolving field adiabatically even
under the all-mass upper bound. A static ground-state curve alone is therefore
not evidence that a finite-age galaxy reaches it. The calculation reports bounds
at x=1e-4, not actual relaxation rates; relaxation is absent from the conservative
Hamiltonian. Initial ground-state preparation would be another physical input.

## 6. Population discrimination and countercharge

Free +/- carriers in the low-frequency medium have screened coupling
q²/(1+chi)=4pi G m². Under the same virial proxy as the previous stage,

    lambda_D/b=(1+epsilon)/6 sqrt((1+eta)/eta),
    omega_p,screened*t_dyn=sqrt(3eta/[epsilon(1+eta)]).

Susceptibility cancels after matching gravity. This still gives no population
selector by mass/size alone. These low-frequency formulas require frequencies
below the relevant material response; they are not used as an instantaneous
replacement in the nonlinear dynamical tests.

A local common bulk velocity leaves the electrostatic internal and relative
carrier response unchanged. Density gradients, rotation-induced transport,
magnetic fields and different thermal histories can matter in a full evolution,
but this model has not derived them or converted them to free/tethered fractions.
Countercharge cold force balance remains problematic: e=g for stationary T
implies a_C=-(1+1/epsilon)g. The medium cannot make the negative carriers disappear.

## Sources and interpretation

Maxwell-Bloch dynamics is an established local field/material framework; see
the primary analysis https://www.aimsciences.org/article/doi/10.3934/dcds.2003.9.663 .
Our undamped Hamiltonian, critical spectrum, gravity matching and bounds above
are the explicitly stated candidate derivations, not claims from that paper.
Existing dipolar-dark-matter work is distinct: live-medium instabilities matter,
as illustrated by https://academic.oup.com/mnras/article/517/1/498/6713968 .
No stability or observational result from that different theory is imported here.
