# Early precursor derivation

EP-20261023, base1205446ebcea9e5ddcbe0ebae3d665326fa75e63. Self-derived from the passive reduced action in ../reciprocal_field_2026_10_22/RESULT.md and units in ../fragment_radiation_2026_10_22/DERIVATION.md. No primordial power spectrum or covariant parent is supplied by those inputs.

## 1. Finite inertia does not unlock a faster local growing mode

Use dimensionless time t/t0, physical wavenumber q=k_phys ell0, eta=.005, chi0=1, and J=4piG rho t0². Subtract the homogeneous density in e as in the inherited cosmological diagnostic. For one cold fluid, let u=div P, delta be fractional density contrast, and h=J delta-u. Linearized continuity, Euler and polarization equations give

 delta_tt=J delta-q² h,
 eta u_tt+(1+q²)u=q² J delta.

For a real growing mode exp(st), set x=s²>0. Eliminating u gives

 h=J delta (1+eta x)/(1+q²+eta x),
 eta x²+[1+q²-eta J(1-q²)]x-J=0.

The constant term is negative, so exactly one root is positive and one negative. At x_Q=J/(1+q²), the polynomial equals eta J² q^4/(1+q²)² >=0. Since it is negative at zero and has one positive root,

 0<x<=J/(1+q²)<=J.

Equality for eta>0 occurs only at q=0. The implicit derivative with respect to Q=q² is

 dx/dQ= -x(1+eta J)/[2eta x+1+Q-eta J(1-Q)] <0,

because the denominator at the positive root is the positive quadratic discriminant square root. There is no finite-wavelength maximum of this growing branch. Delayed polarization gives less cancellation of the repulsive mismatch force; it does not release extra attraction.

For pressureless baryons and cold fraction fc, the growing-mode matrix after symmetrization is

 B(x)=J [[fb, sqrt(fb fc)], [sqrt(fb fc), fc S(x)]],
 S(x)=1-Q(1+eta x)/(1+Q+eta x).

Its largest eigenvalue lambda_+(x) is nonincreasing in x since dS/dx=-eta Q²/(1+Q+eta x)²<=0. The positive growing root solves x=lambda_+(x), hence x<=lambda_+(0)<=J. The same ordering in Q excludes a finite-Q maximum in this branch. The proof is for frozen homogeneous coefficients, positive kinetic terms and the scalar growing mode. It does not establish a finite-inertia FRW transfer function, bound arbitrary transient data, or exclude nonlinear collapse.

The phase and rotational mediator have no linear scalar source at e=P=X=0: their sources are quadratic or vortical. The inherited positive-coefficient transverse block has positive nonzero frequency squared. Thus no new scalar tachyonic precursor selector appears in this background.

## 2. Conditional cosmological onset requirements

Use the inherited quasistatic EdS system, N=ln a:

 delta_b''+.5delta_b'=1.5(fb delta_b+fc delta_c),
 delta_c''+.5delta_c'=1.5(fb delta_b+fc delta_c/[1+(k ell0/a)²]).

Starting at z_i=1100 with delta_b=delta_c=delta_b'=delta_c'=delta_i, linearity gives delta_c(z)=D_c(k,z) delta_i. The linear extrapolation reaches delta_c=1 at delta_i=1/D_c. This is NOT a spherical-collapse barrier; baryons can reach order-unity contrast earlier and invalidate the coupled linear evolution. Positive cooperative evolution gives the dust comparator D_dust=1101/(1+z) as a ceiling in this specified initial-value problem. This comparison uses the quasistatic equations, not the finite-inertia theorem as an expanding-background substitute.

Map characteristic comoving radius to mass by M=(4pi/3)rho_m0 R_L³, k=1/R_L. This convention has no pi factor and does not turn a Fourier mode into a bound halo. The canonical1.0952264e7Msun gives R_L=.0403793Mpc and k=24.7651/Mpc with the reference mean matter density. The initial amplitudes are freely varied; they are not CMB temperature fluctuations or a derived density spectrum.

## 3. Second-order phase check and its failed validity gate

For a real cosine density mode, quasistatic h=h_amp cos(kx), where

 h_amp = J_c(N) delta_c(N)/(1+q²),
 J_c=1.5 fc (H t0)², q=k ell0/a.

Then h²/2 = h_amp²[1+cos(2kx)]/4. To test a possible second-order trigger, impose an explicit additional scalar FRW assumption:

 b(chi_tt+3H chi_t)-d a^-2 Laplacian chi + a_phase(chi-1)=h²/2,

with b=d=.125 and a_phase=.005. This scalar damping prescription is NOT derived for the full preferred-frame action. Use the same EdS clock H=H0 sqrt(Omega_m) a^-3/2, initial phase perturbations and their derivatives zero at z1100, and quasistatic P. For the homogeneous coefficient X and cos(2kx) coefficient Y, in dimensionless units and N time,

 X''+1.5X'+a_phase X/[b(Ht0)²]=h_amp²/[4b(Ht0)²],
 Y''+1.5Y'+[a_phase+4d q²]Y/[b(Ht0)²]=h_amp²/[4b(Ht0)²].

The zero phase initial data are a declared state choice, not an adiabatic preparation theorem. Both coefficients scale as delta_i². A prospective10% phase shift therefore needs delta_i=sqrt(.1/(|X_1|+|Y_1|)), where subscript1 denotes unit initial density normalization. These unit-amplitude trajectories are perturbation coefficients, not physical nonlinear solutions.

The validity audit also tracks the first-order polarization amplitude

 P_amp=q J_c delta_c/(1+q²).

At every prospective phase-onset time, require all earlier |P|<.1 and both density contrasts<1. The minimum over time of the larger normalized violation is >18 for every tested mass. Thus every apparent phase trigger lies outside at least one necessary approximation. Some exceed the exact logarithmic branch limit |P|<1 by a large factor. Those numbers indicate failure of the quadratic approximation, not physically admissible field amplitudes.

For the canonical mass, max |P|=.30449 for delta_i=.01, while max second-order phase shift is only .0001751. A conservative |P|<.1 condition requires delta_i<.003284 in this quasistatic history. The linear density extrapolation would require .03254 by z10 or .09253 by z30. These cannot be combined into a controlled linear-to-core formation solution. At delta_i=.001, the canonical field is within the P test but cold density at z10 is only .03073.

This is a meaningful new hierarchy: polarization nonlinearity can precede density nonlinearity, and precedes the claimed phase trigger in the tested histories. It is not evidence that this nonlinearity necessarily produces cores. Finite P response can matter at the early end, particularly for the larger scales, so the quantitative phase thresholds are conditional.

## 4. Why mass and population do not follow yet

A fixed linear response transfers an input density spectrum: P_delta(k,t)=|T(k,t)|² P_initial(k), with the appropriate multifluid transfer matrix in general. It does not determine P_initial, its higher moments, phases, field initial state, or the probability measure. The local growing rate has no finite-k optimum; the existing length controls suppression, not a universal remnant mass.

A homogeneous unperturbed classical solution stays homogeneous. Nonzero perturbations and a statistical state are inputs. A deterministic action plus fully specified initial data may predict evolution, but this reduced action alone has neither those data nor a covariant metric/clock evolution. A primordial-generation mechanism could provide them; none has been derived here.

Local flat-background equations also underdetermine cosmological completion. For example, a possible covariant curvature coupling proportional to R(chi-chi0)² vanishes in the flat-background reduction but changes the cosmological effective phase mass. This is an illustration of missing information, not a proposal to add a fitted coupling or a claim of unchanged real-galaxy solutions. A consistent parent must choose such terms and constraints before a cosmological simulation can be labeled action-derived.

A matter budget only fixes integral M n(M,t)dM. Neither a primordial spectrum nor a bound-fragment definition, formation kernel, central capture probability, survival law or cluster orbital distribution has been supplied. Assigning those quantities would fit the desired population rather than derive it.
