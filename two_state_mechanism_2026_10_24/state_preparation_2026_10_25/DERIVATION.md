# Formation, entropy, and interaction feedback

Base evidence: research branch commit fd502a8f56846535ea2126b2ef667b1f1e005fdf,
particularly nodal_medium_2026_10_25. Original objective remains a common
microscopic, charge/energy-conserving disk/dwarf/cluster mechanism. This work
attacks preparation, not an observational fit or completed formation theory.
All derivations below are self-reviewed, not independently reviewed.

## 1. Which state can a quadratic unitary protocol prepare?

Use the predecessor's low-energy band with u in [0,1] and occupied-mode
weight w(u)du=chi*u*du, chi=11.220184543019636. Energies are measured in Lambda,
time in hbar/Lambda. A two-level block has

    b=(u,m,-e), H_u=b.sigma, r_dot=2 b cross r.

m is a spatially uniform internal mass/order coordinate perpendicular to the
applied dipole field e. This is an additional physical degree of freedom, not a
renaming of temperature. It is not yet derived from a material's microscopic
interaction. The nodal band and cutoff are still assumed.

At half filling the grand-canonical Gaussian covariance has Bloch length

    L(u)=tanh(sqrt(u^2+m_i^2)/(2*t_i)),
    r_i=-L b_i/|b_i|.

Each block's covariance has trace one. This convention includes the empty and
doubly occupied sectors of the two single-particle orbitals; it is not the
canonical partition function of exactly one particle in a two-state atom.
Number-conserving quadratic evolution preserves the covariance eigenvalues
(1+/-L)/2 and therefore its entropy and Bloch length. It cannot cool a hot
initial nodal band into a pure filled band. This statement is blockwise; it does
not prohibit interacting redistribution, exporting entropy, or changing a
subsystem's state through correlations with other degrees of freedom.

For a final fixed H=(u,0,-e), after projection onto its eigenbasis,

    P_diag = integral w(u) [r.axis] axis_z du,
    P_diag <= P_best = integral w(u) L(u)*e/sqrt(u^2+e^2) du, e>0.

The inequality is Cauchy-Schwarz, r.axis >= -L. It bounds the stationary diagonal
response of this model, not all transient coherent polarization. The ground
response is P_0=chi*e*(sqrt(1+e^2)-e). The force-relevant small difference is
S_0=chi*e-P_0. Compare (P_0-P_diag)/S_0, not fractional errors in large P_0.

A gapped initial state suppresses low-u occupation defects exponentially in
m_i/t_i. It can therefore have a much higher *initial dimensionless temperature*
than a gapless final thermal state while producing nearly the cold response.
This is adiabatic state preparation, not a thermally equilibrated cold final gas.
Cooling the initially gapped state, forming the band, half filling and keeping
collisions from spoiling the resulting occupations remain physical obligations.

## 2. Two explicit gap-removal protocols and their work

Let s(t)=sin^2(pi*t/(2*T)), e=e_f*s, m_i=1. Compare

    linear-gap: m=m_i*(1-s),
    angular-gap: m=e_f*tan(arctan(m_i/e_f)*(1-s)).

The latter spends more time at small gap; it is deliberately designed using
knowledge of e_f. Neither is an autonomous astrophysical prediction. Both begin
at e=0, m=m_i and finish at e=e_f, m=0. No galaxy labels occur.

Advance each Bloch vector by an exact rotation about the midpoint b. Treat
changes in b before and after this rotation as quenches. Work *on* the medium is

    dW = integral w [dm_before*r_y(before)-de_before*r_z(before)
                    +dm_after*r_y(after)-de_after*r_z(after)] du.

At every step U(t)-U(0)-W(t)=0 algebraically for this discrete protocol,
U=integral w b.r. This ledger identity is verified numerically, but it alone
does not prove approximation of the smooth protocol; timestep and mode-count
refinement provide that separate check. In this example removing the gap costs
positive work. There is no unrecorded cooling or energy disposal. The final
'diagonal ensemble' is an eigenbasis projection diagnostic, not simulated
irreversible dephasing. Both instantaneous and projected P are recorded.

## 3. An explicit interacting channel changes the response

Consider an effective attractive contact channel

    H_int=-(g/2V) O^2, O=sum psi^dagger Gamma_mass psi,

with a thermodynamic mean-field treatment. The single channel is illustrative;
an isotropic vector interaction has extra orientational physics. This is a
specified interaction within an assumed band, not a derivation of that band.
At zero external field the mean-field energy density is

    F(m)=m^2/(2g)-C/3*((Lambda^2+m^2)^(3/2)-Lambda^3-|m|^3).

Here m has energy units and C counts each occupied degeneracy once. Set
Lambda=C=1 to express the result in lambda=g*C*Lambda. For lambda<=1, m=0
minimizes F. For lambda>1,

    |m|=(lambda^2-1)/(2lambda).

Differentiation gives 1/lambda=sqrt(1+m^2)-|m|. Thus a coupling can select a
mass and its condensation energy without adding an independent binding-energy
parameter. But it selects a GAPPED phase; it does not generate the desired
nodal spectrum. An m_i=1 ordered state requires lambda=1+sqrt(2) in these units.
The mean-field approximation does not establish the exact many-body phase.

A finite interaction cannot simply be omitted from the dipole susceptibility.
For the same interaction in the field-coupled channel, define p=P/(C*d*Lambda^2)
and e=dE/Lambda. On the stable unbroken branch 0<=lambda<1,

    h=e+lambda*p,
    p=h*(sqrt(1+h^2)-h)=h/(sqrt(1+h^2)+h), for e>=0.

The solution is unique: p'(h)=1/[sqrt(1+h^2)*(sqrt(1+h^2)+h)^2] <=1, so
(d/dh)(h-lambda*p)>=1-lambda>0. Put delta=1-lambda. Then

    p=e/delta-e^2/delta^3+O(e^3),
    chi_eff=chi_bare/delta,
    E_c=Lambda*delta^2/d.

The interaction renormalizes BOTH susceptibility and the field scale. It does
not fix lambda or remove the need for a physical formation law. The one-channel
autonomous test below acts in the perpendicular m channel, and its low-field
longitudinal response is not this same-channel formula. Keep those models distinct.

For diagnostic comparison with the existing spherical tether reduction, fix the
deep-acceleration normalization E/E_c=x/f, x=g/a0, f=chi_eff/(1+chi_eff). This
means e=delta^2*x/f. Define F_response=delta*p/e, and

    y_model=g_b/a0=f*x*(1-F_response),
    x_simple(y)=(y+sqrt(y^2+4y))/2.

Record log10(x/x_simple(y_model)) on the stated finite grid. The optimization
over chi_eff is a phenomenological diagnostic, NOT first-principles parameter
reduction, a data fit, or a population selector. At fixed effective chi, changing
lambda implicitly changes the bare chi. Near-critical enhancement also changes
the shape and cannot be treated as a free bandwidth increase at unchanged law.
Any optimizer hitting its upper chi bound is reported as boundary-limited.

## 4. Autonomous collective coordinate plus live homogeneous field

Remove the prescribed gap control. Take a real coordinate m and conjugate pi,
inertia I>0, stiffness kappa=chi/lambda. At fixed electric displacement D,

    P=sum w*r_z, E=D-P,
    H_total=E^2/2+sum w*(u*r_x+m*r_y)+kappa*m^2/2+pi^2/(2I),
    r_dot=2*(u,m,-E) cross r,
    m_dot=pi/I,
    pi_dot=-kappa*m-sum w*r_y.

These equations conserve H_total exactly: differentiation of E^2/2 supplies
-E*P_dot; the precession terms cancel as b.r_dot=0, and the coordinate force
cancels m_dot*(kappa*m+sum w*r_y). Every block also conserves |r| and trace.
There is no externally prescribed field history and no friction or heat sink.
This is a homogeneous live-field test, not a replacement for the project's 3D
field solver: there are no spatial waves, live gravity or countercharge transport.
Uniform D is a fixed-flux sector, not a dynamically assembled galaxy source.

Choose the unbroken channel lambda=.5. Initialize m=1, pi=0, a thermal band at
t_i=.1, and E_i solving E_i+P_thermal(m=1,E_i)=D. Take
D=e_f+P_ground(m=0,e_f), e_f=.01. The reference stationary nodal solution is
m=0,E=e_f with ground-state Bloch vectors. The energy excess of the initial
configuration is computed explicitly. A closed system with nonzero excess
cannot end in that sole reference ground state: energy must remain in another
coordinate, field, excitation, or exported degree of freedom. This does not
exclude a spatial medium radiating or transporting energy away.

Finite tests vary I and integrate for 20*sqrt(I). The last fifth of each record
measures mean E and RMS m, not an asserted equilibrium. Refinement changes
solver tolerance and mode count. Oscillations, energy excess and a mismatch
with the reference response are evidence against this simple autonomous
preparation protocol only, not a universal no-go theorem.

## Routes and remaining obligations

A: hot nodal quadratic preparation -- restricted by the exact length/entropy
invariant; interacting entropy transfer remains open.
B: cool gapped state then remove gap -- numerical reachability test; controller,
initial cooling, common microscopic scales and formation remain open.
C: contact interaction -- derives an ordered mass and modifies dipole response;
strong order gaps the band; it does not derive the nodal material itself.
D: autonomous gap plus live homogeneous D -- bounded conservation/relaxation test;
spatial energy transport and radiation are absent and remain open.

No disk, dwarf or cluster label is supplied anywhere. That absence is not itself
population separation. Positive monopole tether charge, countercharge inventory,
medium mass, causality and common-mass gravity tests remain unresolved.

Primary literature context: Naya, Bertolini and Carlstrom, Phys. Rev. Research 5,
013069 (2023), https://doi.org/10.1103/PhysRevResearch.5.013069, studies a finite
interaction threshold and a symmetry-broken insulating phase in a nodal-line
material model. Our equations above are derived here for the specified cutoff
and normalization; that paper does not establish our dark-medium mechanism.
