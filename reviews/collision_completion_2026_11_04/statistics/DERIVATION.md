# Quantum conversion reaction measure, CC10

Base checkpoint: `fd417eea045a0b6259b8efff5e20ca62a2e14f7e`; actual
code/data versions are fixed by the fresh v2 manifests. This package owns
`statistics/` only. Couplings are e=h=lambda=.003,
g=sqrt(29/200)e; mu=2e6 GeV and xi=.02. The charged spectrum and vertices
are the full physical leading rigid projections in CT09 `photino/source.py`.
The finite one-loop unbroken-gaugino masses enter the two-body kinematics.
This does not add the missing SUGRA 1PI or medium matching.

## Continuous collision measure and physical degeneracies

Assume isotropic, unpolarized, component-equipartitioned, factorized one-body
occupations. Let eta=+1 for bosons and -1 for fermions. The physical F and C
degeneracies are 24 and 12. U1, SU2 and SU3 gauginos have spin degeneracies
2, 6 and 16 (one, three, eight generators). These factors normalize occupation
and density; they are **not** production branching fractions. Production uses
the actual projected group widths, including all summed daughter components.
At x>0 the lightest C block has twelve real physical degrees. The constructor
rejects any source row in which a heavier charged scalar is an open daughter;
such a species would need its own population rather than being folded into C.

For A -> B + lambda with rest width Gamma_A averaged over physical parent
states and summed over the specified daughter group, the isotropic forward
reaction measure after integrating parent directions is

    dR = g_A p_A^2 dp_A/(2 pi^2) * Gamma_A m_A/E_A * dz/2,
    E_B = (E_A E*_B + p_A p* z)/m_A, E_lambda=E_A-E_B,
    E*_B=(m_A^2+m_B^2-m_lambda^2)/(2m_A),
    p*=sqrt[(mA-mB-mL)(mA+mB+mL)(mA-mB+mL)(mA+mB-mL)]/(2mA).

The time-reversal inverse uses this **same** invariant matrix-element and
phase-space measure. Its occupation factor is exchanged, not assigned an
independent guessed inverse width. For F-heavy ordering the net factor is

    fF (1+fC)(1-fL) - (1-fF) fC fL.

For C-heavy ordering it is

    fC (1-fF)(1-fL) - (1+fC) fF fL.

Thus scalar Bose enhancement, both fermion Pauli factors, and inverse
conversions are simultaneous. At a fixed x only the kinematically allowed
emission direction exists for each group; its inverse always exists.

## Finite measure that conserves energy and has thermal detailed balance

Use fixed comoving q nodes and positive shell volumes W_i. With p=Tc q,

    nu_si = g_s W_i/(2 pi^2), n_si = Tc^3 nu_si f_si.

The first quadrature node is q=0 with positive shell weight; the upper node
is finite. This is an explicit nodal quadrature, not an exact cell integral.
Parent radial quadrature and angular Gauss quadrature give the nonnegative
event coefficient k=nu_Ai Gamma_A m_A/E_Ai w_z/2. Rates are df/dtau,
tau=mu tphysical; Gamma, m and E are expressed in mu units. The physical
event density is Tc^3 k d tau. For d/dN multiply by 1/(Hphysical/mu).

For each exact daughter energy, find its adjacent daughter energy nodes.
Choose nonnegative alpha and 1-alpha summing to one so that their weighted
energy is the exact daughter energy. Do this for both daughters. The event
stoichiometry is the five-entry column

    s=(-1, alpha, 1-alpha, beta, 1-beta).

Consequently E dot s=0 and each child count is exactly one. Events outside
the finite daughter support are omitted and their empty-state measure is
recorded; clamping energies is forbidden. This finite-support exclusion
preserves equilibrium and energy, but is a distinct cutoff approximation.

Linear interpolation of f is incompatible in general with exact quantum
detailed balance. Instead this implementation uses the entropic projection

    F = f_parent prod_children (1+eta_j f_j)^w_j,
    B = (1+eta_parent f_parent) prod_children f_j^w_j,
    j_event = k (F-B),    df_i/dtau=sum_event s_i j_event/nu_i.

Zero-weight endpoint factors are omitted. The powers define geometric
interpolation of f and availability separately; they are equivalent to
linear interpolation of the odds variable

    phi=log[f/(1+eta f)].

They are not ordinary linear interpolation of occupations. Away from zero
or saturated occupations, interpolation error in each logarithm is bounded
by max|second energy derivative| times the energy-cell width squared /8.
This gives local consistency as the energy grid is refined. At a zero or
saturated boundary this smooth-error bound is unavailable. The initial
exactly empty bath is retained, and numerical grid refinement remains an
independent obligation for its generated boundary layers.

At a thermal node, phi_s=-(E_s-mu_s)/T. Thus

    log(F/B)=phi_parent-sum_children w_j phi_j
            =(mu_parent-mu_child1-mu_child2)/T,

because E dot s=0. FD/BE equilibrium is therefore exact to floating-point
error for every event when mu_A=mu_B+mu_lambda, without requiring vanishing
gaugino chemical potential. At F-heavy fixed x, carrier count NF+NC and
NF+sum Nlambda are invariants. At C-heavy x replace NF in the second
invariant by NC. On an orbit admitting both emission directions, only
NF+NC survives among these two combinations; repeated gaugino production
can draw energy from the changing background.

The physical entropy is Tc^3 sum_i nu_i h_eta(f_i), where

    h_eta=-f log f + (1+eta f) log(1+eta f)/eta.

Its collision derivative is sum_event k(F-B)log(F/B)>=0. The equality
condition is vanishing affinity on the connected represented reactions.
At f_boson=0, reverse losses involving that node vanish; at f_fermion=0
losses vanish, and at f_fermion=1 gains vanish. Hence the continuous
finite ODE leaves the quantum domain invariant. Each charge sector can be
lifted separately: the charged daughter copies its parent's signed U1
charge and all gauginos are U1 neutral. Every lifted event then has zero
signed-charge sum. The current aggregate equal-sector code tests the
equivalent carrier column identity; it does not introduce charge asymmetry.

## Numerical integration and varying backgrounds

`ReactionEvents` exposes coefficient, index, weights, stoichiometry, sparse
S, physical measure, energy, eta, flux, RHS and analytic sparse Jacobian.
`implicit_step` solves backward Euler with sparse Newton and a line search
restricted to f>=0 and ffermion<=1. It does not clip accepted populations or
correct their energy afterward. A failure requests a smaller step. The
finite constraints are linear in number coordinates, so a converged step
preserves them to the nonlinear/sparse-solve error.

Rebuild the event energies/coefficients on each actual x,Tc background.
No reaction changes the fixed comoving measure. The associated force and
redshifting work are obtained from the **same** discrete gas energy:

    rho=Tc^3 sum nu f E, P=Tc^3 sum nu f (Tc q)^2/(3E),
    d_x rho=Tc^3 sum nu f m dm/dx / E,
    partial_N rho|f,x=-3(rho+P).

All neutral gaugino rest energies and their derivatives can be retained.
When averaging an orbit the field-action equation must retain the
occupation-energy covariance already derived in CT09 ACTION_IDENTITY.md.
This operator supplies the per-phase C_i and E_i required there; the
construction itself is not a completed field-feedback history.

## Finite checkpoints and limits

`run_local001` tests three backgrounds x=2,5,25.4000254000381, with both
possible charged mass orderings. Each starts as an energy/invariant-preserving
perturbation of a specified FD/BE equilibrium and evolves 30 inverse maximal
partial widths. All declared checks pass: energy and number drifts <=3e-16,
thermal detailed balance <1e-12, positive occupations, fermions <=1,
nondecreasing entropy, and final relative L1 equilibrium error <=2.8e-6.
This is computational verification of the specified finite projected system,
not radial convergence or a full cosmology. The actual empty-bath experiment
is a separate checkpoint. Neutral cascades, pair correlations, nonlocal pole
response, finite heavy-pole matching and initialization remain separate
physical dependencies. No auxiliary radiation source replaces gaugino energy
in this operator.
