# Collisionless support and nonradial stability

Use the same dimensionless action parameters alpha=.005, d=b=.125, eta=.005 and logarithmic W(p)=-p-ln(1-p). ell=.44042213kpc, M0=1.30257985e8Msun, t0=12.07427Myr. This phase studies isolated stationary matter without baryons or expansion; it does not replace the preceding cosmological gas calculation with a demonstrated formation history.

## Kinetic support allowed by the action
The particle action has specific Hamiltonian E=v^2/2+psi, psi=phi+h. Its continuum kinetic lift is

    df/dt = partial_t f + v.grad_x f - grad(psi).grad_v f = 0.

In a static field any isotropic f(E) is stationary. Choose a waterbag, f=f0 for E<mu and zero otherwise. Then rho=4pi f0 [2(mu-psi)]^(3/2)/3, and isotropic stress p=rho v_max^2/5=K rho^(5/3). The minimum kinetic energy density at fixed rho and occupancy ceiling f0 is (3/2)K rho^(5/3), where K=(1/5)[3/(4pi f0)]^(2/3). Filling a centered velocity ball minimizes kinetic energy under that ceiling. Thus no new cold-fluid force or action parameter was inserted; K specifies a phase-space distribution. A supplied K is not a value predicted by the action.

Stationarity at fixed mass gives

    (5/2) K rho^(2/3)+phi+h=mu,
    rho=[(mu-phi-h)/((5/2)K)]_+^(3/2).

The spherical equations are

    phi'=g, g'+2g/r=rho,
    h'=-P/(1-|P|), P'+2P/r=rho-chi*h,
    chi'=z, z'+2z/r=[alpha(chi-1)-h^2/2]/d.

At the origin g=P=z=0. At radius R impose phi+R g=0, R^2 g=M, and decaying asymptotic Robin conditions on h and chi-1. The radial mass convention is M=int rho r^2 dr; the physical density unit contains4pi. The BVP uses scipy's explicit singular S matrix, not division by zero. Its P denominator is protected in unsuccessful Newton iterates; every accepted solution is independently required to lie well below that protection threshold. All reported solutions satisfy it.

A negative mu is a stationary energy cutoff: all particles in the continuum distribution have E<mu<0 relative to the isolated zero potential at infinity. This supports a bound equilibrium interpretation. It does not establish that a cosmological seed reaches this state or that perturbations cannot eject a small fraction.

## Nonradial second variation
Let a_r=(1-|P|)^2, a_t=1-|P|. For a scalar spherical-harmonic density perturbation delta_rho_l, static field relaxation gives

    B_l=alpha-d Laplacian_l,
    delta_chi=B_l^-1(h delta_h),
    L_l delta_h=delta_rho_l,
    L_l=chi-r^-2 d_r(r^2 a_r d_r)+a_t l(l+1)/r^2+h B_l^-1 h.

With G_l=-Laplacian_l, the reduced density-energy Hessian is

    H_l=(5/3)K rho^(-1/3)+L_l^-1-G_l^-1.

This includes phase relaxation. The field block of the unreduced energy is positive: e^2/(2chi) is jointly convex for chi>0, W is convex, and phase potential/gradient terms are positive. Field inertia also adds positive kinetic energy. Thus minimizing the field block is the relevant energetic discriminator, not freezing an inconvenient field response.

The computation discretizes the radial Sturm-Liouville operators with spherical finite volumes and whitens by sqrt(cell volume), keeping the inverse gravity and field response on the entire exterior domain. Density perturbations are supported where the equilibrium rho is nonzero. The l0 subspace has fixed mass. Exact translation symmetry creates a neutral l1 perturbation delta_rho proportional rho'; its overlap, unprojected curvature, and projected complement are all reported rather than silently deleting a negative eigenvalue.

For l>=1, a useful independent bound follows from the variational form of G_l^-1 and pointwise Cauchy-Schwarz:

    <q,G_l^-1 q> <= int [r^2/(l(l+1))] q^2 r^2 dr.

If support radius is rs and Dmin=min[(5/3)K rho^(-1/3)], then l(l+1)>rs^2/Dmin makes the kinetic-minus-gravity Hessian positive without needing field repulsion. For the fiducial solution the bound is about36.77, hence all l>=6 are covered; l0–5 are checked numerically. Finite-grid positivity with an identified translation error is evidence for local energetic stability, not a rigorous all-perturbation nonlinear Vlasov theorem. We do not import Newtonian Vlasov-Poisson stability theorems into this modified, dynamical-field theory.

## Nonradial time evolution
The full inherited 3D TSC particle/logarithmic-P/live-chi solver is used, with eta=.005 and alpha=.005, b=d=.125. No matter damping and no field sponge are applied. Gravity is periodic in a finite box16ell, not the isolated BVP Green function. Particle positions are sampled from the equilibrium radial CDF and velocity directions/radii from its waterbag, with deterministic scrambled Sobol seed61423 and paired (x,v),(-x,-v). The actual particle density initializes the static field. Initial profile sampling, periodic images and grid forces therefore need refinement, even though the continuum BVP has converged.

An affine canonical perturbation x->A x, v->A^-T v with A=diag(exp(.05),exp(-.05),1) excites a genuinely nonspherical mode without changing phase-space occupancy. A further isotropic factor1.5 expands the cloud while reducing velocities; it then collapses/rebounds under the same live fields. This is a controlled formation-from-dilation test, not cosmological formation. All spatial particle coordinates and fields evolve freely, so the affine map restricts only initialization, not subsequent dynamics.

The reference dynamical time is sqrt(r50^3/M)~6.87t0. Forty t0 is~483Myr and~5.82 such times. Stability diagnostics include r10/r50/r90, shape, total energy and refinement. A finite survival interval is not indefinite stability, and half-mass convergence does not imply a fully resolved central density.

## Why support still does not choose a mass
The waterbag occupancy f0 and total material mass are kinetic invariants of an isolated evolution. At fixed K the BVP accepts a continuous family of input masses, not a unique eigenmass. Phase-space mixing can change the coarse-grained distribution, but Liouville transport does not create a unique f0. A self-consistent cosmological supply, mixing and escape calculation is needed to turn these equilibria into a mass distribution. Selecting a member by matching a dwarf is calibration.

## Conditional cosmological check
If the same waterbag occupancy is imposed homogeneously from z1100, sigma_1D(z)=sqrt(K)*rho_c(z)^(1/3) in velocity units. Under unforced EdS redshifting, its one-component comoving displacement is

    D=2 sigma_1D,0/[H0 sqrt(Omega_m)] [sqrt(1101)-1].

The free-streaming density kernel of a uniform velocity ball is 3 j1(k sqrt(5)D)/(k sqrt(5)D). It is a ballistic diagnostic, not a coupled gravitational growth function. At K=.05, D~.0883Mpc, over twice the earlier .04038Mpc seed scale. At k=1/Mpc the kernel is~.9961 but at the seed wave number it is~-0.0476 (phase reversal and small amplitude). Gravitational forces change this result; it cannot be read as a matter-power prediction. It demonstrates that importing the supported distribution primordially is not innocuous for dwarf-scale seeds. If dispersion is generated after collapse instead, this primordial estimate does not apply—but then its size and mass dependence must be derived from the nonradial assembly.

## Extension of the passive mass-selection obstruction
This is a conditional analytic result, not a universal obstruction to assembly or ejection. Assume an isolated differentiable branch of stationary equilibria at fixed waterbag occupancy K, fixed action parameters, positive chi, |P|<1 and decaying fields with vanishing boundary terms. Let T=(3/2)K int rho^(5/3), U=gravitational energy, V=int e^2/(2chi), Z=alpha/2 int(chi-1)^2, J=d/2 int|grad chi|^2, H=int h^2, B=int W, D=int p W'(p), all with the common1/(4pi) volume convention.

The dilation rho(x)->t^3 rho(tx), P(x)->t^2 P(tx), chi(x)->chi(tx) preserves mass and is an allowed canonical position/velocity compression for the waterbag. It gives

    2T+U+3V-3Z-J+2D-3B=0.

An amplitude variation at fixed K gives mu M=(5/3)T+2U+2V+D, using the stationary P equation to rewrite int rho h=2V+D. Phase stationarity gives V=2J+2Z+H/2. Subtracting E=T+U+V+Z+J+B and using the two identities yields

    mu M-E = -(4/3)T-4J-2Z-H+2B-D < 0,
    d(E/M)/dM = (mu M-E)/M^2 < 0.

For the logarithmic W, d[2W-pW']/dp=-p^2/(1-p)^2, and the expression vanishes at p0, so2B-D<=0. A nontrivial matter equilibrium has a strictly negative contribution. The result does not use spherical symmetry. It extends the prior passive fixed-mass obstruction to isotropic waterbag support: adding this physical support does not create an interior minimum of energy per mass along the stated branch. It does not imply that all masses admit equilibria, that mergers occur, or that dynamical fragmentation cannot select masses through supply, escape, anisotropy or additional constraints.

The sixteen numerical family members verify the Jeans virial and total virial identities to3.0e-6 and5.5e-6 relative, respectively; the mass-slope identity agrees within9.3e-5, including finite outer-boundary/tail errors. All computed mu M-E values are negative. The finite scan supports, but does not replace, the uniform conditional derivation.
