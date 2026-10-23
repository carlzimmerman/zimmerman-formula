# A conditional spherical stability bound for the finite kinetic family

The finite identified-medium equilibrium family has an exact nonnegative conserved-functional gap. Assuming a spherical kinetic evolution exists, preserves the stated invariants and remains in the admissible polarization domain, this gap bounds the squared phase-space distance from equilibrium. This is a substantive stability result within those hypotheses. It is not an unconditional global PDE theorem, nonspherical stability, attraction, or a formation/selection mechanism.

## Model and hypotheses

Use the identified-medium Newtonian dynamics of CFG939 with fixed spherical baryons, the finite distribution family of FINITE_KINETIC_RESULT.md, and negligible background density. Let f(x,v)>=0 be mass density in phase space, rho=integral f dv, and P the linear spherical density map divP=rho. Its potential-energy functional is

    U[rho]=integral rho Phi_b dx
           +integral V(P) dx + gamma/2 integral rho² dx,
    V(P)=a0²/K [-q-ln(1-q)-q²/2], q=K|P|/a0<1.

The critical quadratic's cancellation of cold Newtonian self-gravity is already part of this identified model. The formula is not the total energy of arbitrary independently gravitating cold matter plus an A33 field.

Include kinetic energy:

    H[f]=integral (v²/2) f dx dv+U[rho].

The effective particle energy is E_f=v²/2+delta U/delta rho. The kinetic equation is Hamiltonian transport by E_f. Assume sufficient regularity and decay to conserve H, mass, integral f² and the integrals below, with no boundary injection or escape omitted from the accounting. These assumptions must be checked for any actual numerical evolution or weak-solution framework.

For spherical evolution, L²=|x cross v|² is constant along characteristics, so integral L² f is also conserved. Noncentral forces do not share this property. The identification of P purely with the density map is likewise the spherical model; transverse-history degrees of freedom in three dimensions are not analyzed here.

## Conserved functional and equilibrium

Fix F>0, anisotropy radius ra>0 and cutoff Ecut. Define

    C[f]=H[f]+integral f²/(2F) dx dv
               +integral L² f/(2ra²) dx dv
               -Ecut integral f dx dv.

All its terms are conserved under the assumed spherical collisionless evolution. Let f0 be an exact self-consistent equilibrium of the form

    f0=F [Ecut-E_0-L²/(2ra²)]_+,
    E_0=v²/2+(delta U/delta rho)|rho0.

This is the same linear-cutoff distribution used in the preceding finite calculations. Those numerical profiles approximate such equilibria; a small ODE residual is not itself a validated continuum existence/error theorem.

Set A0=E_0+L²/(2ra²)-Ecut and delta f=f-f0. Expanding the quadratic Casimir, and the linear-plus-convex spatial energy, gives the exact identity

    C[f]-C[f0]
      = integral (delta f)²/(2F) dx dv
        + integral [A0]_+ f dx dv
        + integral [V(P)-V(P0)-V'(P0) dot(P-P0)] dx
        + gamma/2 integral (rho-rho0)² dx.

Inside the occupied region A0<0, f0=-F A0 and the linear variation cancels. Outside it f0=0 and the remaining linear term is A0 f>=0. This support term is essential; simply treating the cutoff as an unconstrained critical point would omit it.

V is convex on the cap ball. In dimensionless radial magnitude its derivatives are

    d[-q-ln(1-q)-q²/2]/dq=q²/(1-q),
    second derivative=q(2-q)/(1-q)²>=0.

The radial function is also nondecreasing, giving convexity as a function of the vector P. The field remainder is therefore nonnegative, as are every other term in the identity.

## What follows

For every admissible evolution satisfying the conservation hypotheses,

    ||f(t)-f0||_L2² <= 2F [C[f(0)]-C[f0]].

For gamma>0 the same gap also bounds gamma ||rho(t)-rho0||_L2²/2. Thus small initial functional gap prevents large growth in these controlled quantities for as long as the admissible evolution exists. This is an energy-distance stability statement; small initial L2 distance alone has not been shown to imply a small full functional gap, especially near the cap.

The identity also makes f0 a strict global minimizer of this functional within its admissible finite-energy class, conditional on its existence: equality forces f=f0. This does not select F, ra or Ecut physically. Changing them changes the functional and can select a different equilibrium.

The argument covers spherical disturbances, including changes to the radial distribution within that symmetry, not radial-orbit instability under nonspherical distortions. The field energy and cap may affect global well-posedness; this proof does not show that a solution remains uniformly away from q=1 or cannot develop singular structure. A finite integral energy is not automatically a pointwise cap margin.

## Why stability is not settling

The bound shows that an equilibrium can resist perturbations. It does not show that generic initial states converge to it. Collisionless evolution preserves mass, energy and many phase-space Casimirs. States with different conserved values cannot all strongly converge, in a topology preserving those quantities, to the same selected f0. Weak phase mixing or local relaxation remains possible without fine-grained convergence.

This clarifies the outstanding mechanism: a law-compatible stable equilibrium, its basin of coarse-grained relaxation, and the retained/free mass fraction are different questions. The current family still generally lies below the cold algebraic-law profile and has chosen distribution parameters. A stability bound does not cure that mismatch or derive kappa.

## Prior art and checks

SciSpace identified Rein, Vukadinovic and Braasch, *Nonlinear Stability of Stationary Plasmas—An Extension of the Energy-Casimir Method*, SIAM J. Appl. Math.59,831–844(1998), https://epubs.siam.org/doi/10.1137/S0036139997329069. The publisher abstract confirms extension of the method to distributions depending on additional particle invariants. Only the abstract was authenticated here; no theorem from that paper is transferred to the present nonstandard energy. The method and the use of particle invariants are established prior art, not a novelty claim.

energy_casimir_run/manifest.json validates;9 algebraic/numerical checks pass. They cover potential derivatives, quadratic expansion, occupied/unoccupied cancellation, anisotropic stationarity, central-force L² conservation, phase-space incompressibility and sampled convex field remainders. Removing the angular-momentum term breaks stationarity of the unchanged anisotropic distribution (8/9 pass). The checks support the displayed algebra; they do not certify global existence or independently validate all functional-analytic hypotheses. The argument is self-reviewed.
