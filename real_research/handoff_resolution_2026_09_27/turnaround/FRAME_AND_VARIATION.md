# HR01-T constructive continuation and self-audit

Base: `48905ae11213afcb9ff1b7726530bb5dd1933fe3`, working-tree sources pinned in `mirror_sources.json`. This is a fixed-region Newtonian construction and an analytic local-symbol audit, not a covariant theory or a derivation of kappa. Both a0 footings are retained; kappa=1/2 remains fitted, Z=5.7888.

## Exact uniform-field subtraction from a specified action

Use potential-gradient convention g=grad Phi_N (physical acceleration is -g). For a fixed bounded region Omega, a nonnegative prescribed mask W, and q'(Y)=sqrt(1+Y^(-1/2))-1, define

S = integral dt dx {-[2 grad Phi.grad Phi_N-|grad Phi_N|^2-a0^2 W q(|g-A_Omega|^2/a0^2)]/(8 pi G)-rho Phi}.

A_Omega(t) is constant over each region and is varied, not externally chosen. Holding the region and W fixed, the field equations are

Delta Phi_N=4 pi G rho,
Delta Phi=4 pi G rho+div[W (nu(|g-A|/a0)-1)(g-A)],
0=integral_Omega W (nu(|g-A|/a0)-1)(g-A) dx.

Thus A is an implicit weighted mean. Under g -> g+b(t), A -> A+b(t) exactly; the nonlinear flux is invariant. This proves uniform-field cancellation within this explicitly modified action. It does not follow merely by a coordinate transformation of the original MOND action. The material center-of-mass acceleration is mass-weighted, whereas this stationary condition is weighted by W(nu-1); these coincide only under additional symmetry or assumptions. The three-cell counterexample in `frame_tide_audit.py` gives a difference of 0.0617899 in dimensionless field units.

There is also a useful existence/uniqueness result. For positive-volume support of W with integrable bounded g, the radial energy q(|g-A|^2/a0^2) is strictly convex in A: its tangential derivative has coefficient nu-1>0 and its radial derivative has coefficient

nu-1+y nu' = (nu-1)^2/(2 nu)>0, y=|g-A|/a0.

At g=A the energy behaves as |g-A|^(3/2), preserving strict convexity although its second derivative is singular. At large |A| the energy grows linearly, so the integral is coercive. Hence it has one stationary minimizer. The sign of the gravitational action does not change that stationary equation; this is an auxiliary elliptic construction, not a claim of a globally positive gravitational Hamiltonian. If W vanishes everywhere, A is undetermined and the flux vanishes, so no uniqueness is needed. Smooth dependence requires a nonsingular finite Hessian or a separate singular analysis.

The construction has no new numerical fit, but it has a new nonlocal structure and a region-selection rule. Those must be counted. Specifying Omega as a connected component of theta<=0 is insufficient for a full variational theory: varying theta moves its boundary, and components can merge/split. Shape derivatives, interface junction conditions, baryon-flow backreaction, and evolution of the component labels remain obligations. Varying only the two potentials while freezing a dynamically defined mask omits those terms.

## Uniform subtraction leaves a first-order density tide

Let the residual external field near the region center be T x+O(|x|^2); T is symmetric for a potential field. On a sphere around an isolated point mass write g_internal=g0 n and p(g)=(nu-1)g. Its radial linear response is

n.delta p = [nu-1+y nu'] r n.T.n.

The angle-averaged response is therefore

average(n.delta p) = [(nu-1)^2/(2 nu)] r tr(T)/3.

It vanishes to first order for a trace-free tide. It does not vanish for an environmental density perturbation, for which tr(T)=4 pi G delta rho in the potential-gradient convention. XR36 G9 estimates a density tide using (4 pi/3)G rho_bar delta_env r, and then says its monopole enters only at second order. Those two statements do not follow together. The second-order statement requires trace-free T, or a separately specified subtraction of the isotropic density tide. Subtracting one uniform vector cannot do that.

At z=.25, Mb=1e11 solar masses, r=.3 Mpc and delta_env=1, the source-like estimate gives e_tidal/a0=1.44410e-4 / 1.19494e-4. The leading phantom-flux changes are 4.18563% / 4.20163%. For an independently imposed e=1e-4, exact quadrature gives 2.85241% / 3.44957% for an isotropic tide and -0.0506486% / -0.0737220% for the tested trace-free shear. These are flux effects, not KiDS chi-square predictions.

A useful operational domain follows without adding a fitted length. Requiring the density tide to stay below fraction epsilon of the central Newtonian field gives

r <= [3 epsilon Mb/(4 pi |delta rho|)]^(1/3).

For the same density and mass, equality of tide and central field occurs at .676369 Mpc; the 10% radius is .313943 Mpc, independent of a0. This is a condition on the validity of an isolated-field approximation, not a derived physical edge. At 1 Mpc the small-tide expansion fails (tide/internal approximately 3.23); extending an isolated lensing profile there needs a genuine tidal solution.

## What the local action-symbol argument proves

For a frozen background, L=1/2 rho |u|^2+B W(theta), theta=div u, the displacement variation delta u=dot xi gives

delta S_gate = integral dt dx [partial_t grad(B W_theta)].xi,

up to boundary terms. Its principal longitudinal kinetic symbol is m(k)=rho+B W_theta_theta k^2. If W is C2, flat for theta<=0, and decreases somewhere for theta>0, the mean-value theorem forces W''<0 somewhere. The saturated positive-B local gate cannot have a positive kinetic symbol at every k. This is an actual analytic restriction on that gate family.

The static cancellation is a frozen-coefficient statement. B(x,t), W_theta(x,t), background gradients, moving interfaces and eliminating gravitational constraints all require their own terms. The vanishing of this one static contribution does not establish the entire static sector or a covariant model.

At m(k_g)=0, a generic nonzero potential symbol K(k_g) makes omega^2=K/m singular. For the continuum frozen-coefficient Cauchy problem one side has unbounded exponential growth as k approaches k_g, except a specially tuned simultaneous zero. This supports an ill-posedness diagnosis for that local continuum model. A negative kinetic sign by itself, or a finite box whose discrete spectrum misses k_g, is not the same proof. The source's sharp-gate limit is singular and is not a well-defined C2 substitution.

For a Gaussian filter with Fourier amplitude exp(-R^2 k^2/2), the frozen symbol is rho-C k^2 exp(-R^2 k^2), C=-B W_theta_theta>0. Since max k^2 exp(-R^2 k^2)=1/(e R^2), strict positivity requires R^2>C/(e rho). Equality leaves a zero at k=1/R; the source's 'healthy iff R>=R_min' needs strict inequality for a coercive symbol. Spatially variable coefficients do not inherit this Fourier iff without further bounds.

## A concrete kinetic completion and its price

A second route is a finite-region compensator, which avoids committing to one universal smoothing length. Let P theta=theta-average_Omega(theta), let the gate read P theta, and add

L_comp = (C_Omega/2)(P theta)^2,
C_Omega >= ess sup_Omega [-B W_theta_theta]_+.

For fixed Omega, fixed C_Omega and fixed B, the second variation in any velocity increment v obeys

integral B W''(P div v)^2 + C_Omega integral(P div v)^2 >= 0.

Adding rho|v|^2 with rho>0 gives a strictly positive kinetic form. On a static configuration theta=0, the compensator and its first variation vanish, preserving that prescribed static profile. The finite matrix check verifies this inequality independently. Choosing C as the curvature envelope uses the existing constitutive function rather than a fitted constant, but the envelope and subtraction are additional constitutive rules.

This is substantive partial construction, not the final remedy: P theta=0 on homogeneous expansion, so this gate alone no longer distinguishes Hubble flow from a static region. An independent background expansion offset or region membership criterion is needed. If C or Omega depends on the evolving fields, its variation must be included. If the original gate reads theta while the compensator reads P theta, the unpenalized mean mode needs a separate finite-domain coercivity bound and cannot be declared repaired by the above proof. The construction isolates precisely what a completion must supply; it does not pass the cosmology, bootstrap, or parameter-count gates.

## Check status and remaining implication

`frame_tide_audit.py` passes 9/9 bounded checks; MUTATE replaces the nonzero isotropic linear response by zero and fails exactly both footing isotropic checks (exit 1). Angular quadrature uses 96 Gauss-Legendre nodes and 192 azimuths; the finite kinetic test has 48 cells, seed 361. The analytic formulas give the universal statements under the explicitly fixed-domain hypotheses; the finite outputs only validate the implementation at these inputs. This is self-review, not an independent referee audit.

The smallest remaining implication is a differentiable, covariant region/frame-and-gate action whose full variation is coercive, whose region can turn around with the retained carrier without a forbidden extra fit, and whose tidal lensing and background cosmology jointly pass. The fixed-region auxiliary-vector and kinetic inequalities above supply pieces but not that implication.

## An analytic bootstrap condition for a retained carrier

For the sharp regional D2 gate, W=0 whenever a shell is expanding. Up to its first v=0 event the shell therefore follows precisely the ungated Newtonian baryon-plus-carrier equation, provided the initial data, carrier history, cosmological convention and regularity are the same. Uniqueness before the event proves that MOND switched on at that event cannot advance the first turnaround. This statement is specific to the D2 event; local D1 divergence and shell radial velocity have different signs in general.

With a time-independent seed mass and point-mass shell equation ddot r=-G Mseed/r^2+F(t)r, scaling r=Mseed^(1/3) s removes Mseed from the equation for s. For similarly scaled Hubble-flow initial data, R_turn is proportional to Mseed^(1/3). In convention B at z=.25 the baryon-only Mb=1e11 radius is approximately .378 Mpc, so reaching 1 Mpc before switching needs a seed mass approximately (1/.378)^3 Mb=18.5 Mb. A retained carrier of 5.36 Mb added to the baryons gives 6.36 Mb total, increasing that radius only by 6.36^(1/3), to approximately .700 Mpc. This estimate is conditional on a constant compact seed, this initial-time prescription and the source's smooth-background treatment; extended/time-dependent carrier halos require re-solving the trajectory. It is a constructive minimum-support criterion, not an exact inferred halo mass or a universal cosmological turnaround bound.

For the Local Group at z=0, calibrating to the source's Newtonian convention-B R0=.440 Mpc at Mb=1.145e11 gives total seed mass about 9.44 Mb for R0=.93 Mpc; the 2-sigma lower edge .69 Mpc requires about 3.86 Mb. The different radius requirements explain why adding the same constant carrier fraction is not automatically a joint lensing/timing remedy. Carrier evolution must be derived and jointly scored; it cannot be silently included after computing the baryon-only mask.

## Improved continuation: shear kinetic completion preserves the homogeneous gate

The mean-subtracted scalar completion above exposes a real defect: it erases the expansion signal. A distinct operator avoids that defect at frozen coefficients. Define the baryon velocity shear sigma_ij=(partial_i u_j+partial_j u_i)/2-delta_ij theta/3, and add L_shear=(C/2) sigma_ij sigma_ij. For periodic or spatially decaying perturbations, decompose each Fourier mode into longitudinal and transverse parts. Then

m_L(k)=rho+[B W_theta_theta+(2/3)C] k^2,
m_T(k)=rho+(C/2) k^2.

Choosing C=(3/2) c_*, c_*>=sup_theta[-B W_theta_theta]_+, makes both kinetic forms at least rho>0 for every k. For a fixed B and K=3H, the smallest envelope prescription is C=3 B ||(W_xx)_-||_infinity/(2 K^2); the gate shape fixes the norm. No additional fitted constant is required for this prescription, although adding this operator is a new constitutive choice. The identity follows also from integral |sigma|^2 >= (2/3) integral theta^2 under these boundary conditions. Pure Hubble expansion has sigma=0, as does a static galaxy, so the compensator and its first variation vanish on both backgrounds; the original W(theta/K) can still distinguish their theta values.

This is a genuine frozen-coefficient repair of the local kinetic obstruction, stronger than simply recommending smoothing. It does not prove full viability: variable coefficients need a weighted coercivity argument or a region-fixed upper bound; finite free boundaries admit dilation/conformal modes outside the periodic/decaying proof; baryon shear changes perturbations even when the original gate is off. The covariant candidate sigma_mu_nu=h_mu^alpha h_nu^beta nabla_(alpha u_beta)-(theta/3)h_mu_nu, h_mu_nu=g_mu_nu+u_mu u_nu, must be varied with the fluid and metric. Its metric-velocity terms can change the gravitational kinetic matrix. Therefore one must compute the full constraint-reduced principal symbol and observational response before claiming a well-posed action. This term repairs neither the pre-turnaround baryon deficit nor the tidal monopole by itself.

The updated independent script adds the Fourier eigenvalue and zero-Hubble-shear checks: 11/11 now pass. The original 9-check manifests remain historical records; the current source SHA and evidence are in the `*_shear` run directories.

### A coupled metric check of the shear repair

The shear operator has a calculable tensor-sector price. In local comoving coordinates with background u=n and sigma=0, a transverse-traceless metric perturbation has sigma_ij=(1/2) dot h_ij^TT to principal order. The ADM Einstein term gives M_Pl^2(dot h_TT^2-|grad h_TT|^2)/8; the compensator adds C dot h_TT^2/8. Therefore the frozen tensor speed is

c_T^2=M_Pl^2/(M_Pl^2+C)

in units c=1, with positive tensor kinetic coefficient. Thus curing the fluid sign by this covariant shear term changes gravitational-wave propagation wherever C>0. This is not an observational exclusion without a sourced propagation analysis, but it is a concrete new constraint; a scalar-only audit would miss it. On an exactly homogeneous FRW solution whose MOND-gradient energy B=0, this particular envelope C proportional to B vanishes and the correction is absent. On nonzero-gradient host backgrounds it need not be small.

In SI units the relative tensor kinetic correction is 8 pi G C/c^2 = (3/2) c_W q(y^2)[a0/(c K)]^2 for the proposed C, with c_W=||(W_xx)_-||_infinity. It remains finite only if the chosen background K is nonzero and the curvature envelope is finite. The source convention K=3H of the cosmological leaf has a positive de Sitter limit; substituting a local turnaround expansion K=theta would be singular and is not allowed by this derivation. A sharp step has no finite C2 curvature envelope and is outside this repair. An additional compensating gravity operator might restore tensor propagation but would be another constitutive choice requiring a new full-symbol audit. No such cancellation is claimed here.

### Scalar projection isolates a more economical nonlocal operator class

A final bounded continuation removes the tensor-speed shift at this same linearized level. On each specified spatial leaf define s=Delta^{-1} partial_i partial_j sigma_ij with its zero mode removed. For a nonzero longitudinal Fourier mode, s=(2/3)theta; for transverse vector modes and transverse-traceless metric modes it is zero. Add L_s=(C_s/2)s^2 while keeping the original gate's argument theta/K. Then

m_L=rho+[B W_theta_theta+(4/9)C_s]k^2,
m_T=rho,
Delta L_TT=0.

C_s=(9/4)sup[-B W_theta_theta]_+ repairs the frozen longitudinal kinetic coefficient, while the tensor quadratic action is unchanged by this operator. Homogeneous Hubble shear is zero, so its background expansion signal is preserved in W. This is closely related to the scalar mean-subtracted compensator, but here the original gate retains theta and the excluded zero mode is declared explicitly. The earlier variant that made W itself read P theta is unnecessary and is not carried forward.

This identifies a minimal candidate operator class, not a local covariant completion. Delta^{-1} is instantaneous on the chosen leaf and needs a zero-mode convention, boundary conditions, and a rule under region mergers. Projected covariant derivatives do not commute on general leaves; lapse, shift, scalar metric and fluid constraints must be varied together. Homogeneous dilation and free-boundary modes remain outside the nonzero Fourier proof. C_s must remain finite and its field dependence must be included. A claim of relativistic causality or nonlinear well-posedness is not established. The final independent script has 13 passing checks; MUTATE still fails exactly the two density-tide trace checks.
