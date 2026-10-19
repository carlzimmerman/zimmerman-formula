# FSP-I: can atomic binding select the electromagnetic strength?

Parent: FSP-001; work package FSP-002. The user proposes a physical bridge between atomic size, baryonic mass and the gravitational/vacuum framework. This note tests a specific candidate principle: **the energy of ordinary bound matter selects alpha by minimization**. It is a new selector test, not an assumed term of the frozen framework.

Use alpha for the physical electromagnetic coupling, `a_B` for the infinite-nucleus Bohr radius, `a_H` for the reduced-mass hydrogen length, and `a_M` for the framework's acceleration scale. This avoids confusing the two unrelated quantities traditionally denoted a0.

## I1. What an atom's size actually supplies

In the leading nonrelativistic hydrogen approximation, with fixed positive electron and proton masses,

`mu = m_e m_p/(m_e+m_p)`,

`E_n = -mu c^2 alpha^2/(2 n^2)`,

`a_H = hbar/(mu c alpha)`.

The radius is not an extra field equation for alpha: minimizing the electron wavefunction energy fixes a_H **for every chosen alpha**. A measured length and a measured binding energy could extract alpha, through `2 |E_1| a_H/(hbar c)=alpha` in this approximation, but that is a measurement relation. The framework would need to predict one of those quantities independently to turn it into a mechanism.

The leading sensitivities are

`d log(a_H)/d log(alpha)=-1`,

`d log(a_H)/d log(m_e)=-m_p/(m_e+m_p)`,

`d log(a_H)/d log(m_p)=-m_e/(m_e+m_p)`.

Thus electron mass, nucleon mass and electromagnetic strength are distinct microscopic inputs. Fixing a proton's mass alone does not fix an atom's radius. This is a statement about the displayed Hamiltonian, not an exclusion of a theory relating those inputs.

## I2. A concavity obstruction for the proposed energy selector

Claim: Let I be an open interval of alpha values. Let H(alpha)=H0+alpha V on a common, alpha-independent variational domain of normalized states. Assume the energy infimum is finite throughout I. H0 can include any specified alpha-independent interactions, masses, nuclear core and framework potential. Define

`E0(alpha)=inf_{||psi||=1} [<H0>_psi + alpha <V>_psi]`.

Then E0 is concave on I. For 0<=t<=1, each state obeys

`t <H(alpha1)> +(1-t)<H(alpha2)> >= t E0(alpha1)+(1-t)E0(alpha2)`.

Taking the infimum of the left side proves

`E0(t alpha1+(1-t)alpha2) >= t E0(alpha1)+(1-t)E0(alpha2)`.

Consequently E0 has no strict local minimum at an interior alpha. At a twice-differentiable point E0''<=0. Adding alpha-independent rest masses/vacuum energy or summing the energies of fixed-composition matter with positive fixed populations preserves concavity. Adding a fixed linear electromagnetic nuclear self-energy also preserves it.

If a healthy scalar phi makes alpha dynamical and alpha'(phi*)!=0, an interior matter-only stationary point obeys E0'(alpha*)=0 and

`d^2[n E0(alpha(phi))]/dphi^2 at phi* = n E0''(alpha*) [alpha'(phi*)]^2 <= 0`.

It cannot supply a positive scalar restoring mass. More generally, a locally monotone alpha(phi) cannot turn the absence of a strict minimum into an isolated minimum. The claim does not exclude flat, unselected directions. If alpha'(phi*)=0, a function chosen to have an extremum can alter stability, but its selected alpha value has not been derived by this argument.

For fixed temperature and an alpha-independent density-matrix domain, the same conclusion applies to canonical free energy by the Gibbs variational expression `F=inf_rho[Tr(rho H)+k_B T Tr(rho log rho)]`, provided it exists. Each trial density matrix again gives an affine function of alpha. This statement does not treat the divergent unconstrained atomic partition function as finite; a finite volume/domain or other physical regularization is required.

## I3. A concrete stationary attempt

Hydrogen's optimized Coulomb binding energy is `-D alpha^2`, with `D=mu c^2/2>0`. Include an independently specified fixed-core electromagnetic energy `C alpha` and constant rest energy M0 c^2:

`E_matter(alpha)=M0 c^2+C alpha-D alpha^2`.

If C>0 the stationary value alpha*=C/(2D) is a maximum, with E_matter''=-2D<0. If C<=0 there is no positive stationary minimum. The exact value of C is not fitted or inferred here; no numerical match to alpha is attempted. The same curvature obstruction holds when ordinary Coulomb binding is computed beyond the one-orbital formula, within I2's affine-Hamiltonian hypotheses.

This attempt therefore supplies no stable selector for alpha from ordinary binding energy alone. This conclusion closes that specified principle; it does not close the shared-scalar or QCD routes.

## I4. The macroscopic baryonic-mass connection

For N neutral hydrogen atoms at fixed N and fixed constituent masses, ignoring hyperfine/QED/nuclear corrections,

`M_bar = N [m_p+m_e-mu alpha^2/2]`,

where mass units are used. If the framework's macroscopic source is matched to the physical total atomic rest mass, its asymptotic galaxy relation is `v_flat^4=G a_M M_bar`. This microscopic source matching is an explicit conditional application; S2 alone does not quantize the atom. Electronic binding then contributes

`d log(v_flat)/d log(alpha) = -mu alpha^2/[4 (m_p+m_e-mu alpha^2/2)]`.

This is a **response**, not an equation selecting alpha. Atomic population N is an additional physical datum; it is not predicted by a particle's mass. Real inferred galaxy masses also depend on gas/stellar calibration and nuclear composition. Holding m_p fixed deliberately excludes its QCD/EM sensitivity, which belongs to FSP-Q. Converting a measured galaxy mass to atom counts with atomic physics and then calling the result an independent alpha prediction would mix inference and dynamics.

## I5. Scope, escape and next discriminator

The affine Coulomb Hamiltonian is a controlled leading atomic approximation for the usual weak electromagnetic coupling. It is not a theorem about fully renormalized QED, relativistic pair creation, alpha-dependent electron/QCD masses, nonlinear scalar kinetic functions, changing temperature/composition, or a complete UV theory. These can change the premises. A nonlinear independent vacuum potential can overcome concavity, but its normalization and selected value must be calculated, not chosen from alpha.

The useful next step is the explicit FSP-B shared-scalar candidate: derive both the mass/coupling functions and vacuum term, retain every free coefficient, and check whether the stationary **value** of alpha is fixed. The atomic stationarity condition alone cannot substitute for that missing microscopic equation.

The standard definitions and numerical reference inputs are checked against [NIST CODATA 2022](https://physics.nist.gov/cuu/pdf/wall_2022.pdf); the framework relation is the frozen S1/S2 theory, not a new empirical validation. I2 and I3 are internal variational/algebraic proofs. No global novelty claim is made for concavity.
