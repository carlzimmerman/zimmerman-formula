# Independent coordinator derivations of the three physical lanes

2026-10-19. This is a focused mathematical review of the displayed derivations,
not an independent rerun, a proof of formation, or an audit of the full original
relativistic theory. The final input hashes are in the packet checkpoint.

## Occupied source continuum

I reconstructed the box vertex from canonical field factors. The coefficient
for each unordered nonzero pair is g/(omega_p sqrt(2MV)): two daughter
contractions cancel the factor two in the two daughter mode normalizations.
Then unordered phase space gives

    J_H = (g²/(4M)) integral d³p/[(2pi)³ omega_p²] delta(E-2omega_p)
        = g² beta(E)/(16pi² M).

The last radial integral is beta/(4pi²). Thus J_H has the fixed M in the
denominator, agrees with Gamma(M)/(2pi) on shell, and differs by E/M from
the running-width prescription away from it. This resolves an actual
off-shell ambiguity rather than changing an on-shell decay result.

The source resolvent Schur complement gives G_s=[z-epsilon_b-Sigma]^-1.
Solving the continuum inhomogeneous equation produces the outgoing
coefficient sqrt(J)G_s; its magnitude squared is J|G_s|²=rho_s. This needs
the stated scattering/absolutely continuous assumptions; persistent bound
weight is separately counted. Integrating the one-particle occupation gives
2n_X, confirming fPhi=16pi² n_X rho_s/(pE). A different envelope F(H) changes
rho_s by |F|². The occupation claim is therefore state specific.

For J=A sqrt(epsilon)/(1+epsilon/Lambda)², at z=-Lambda y² substitution
epsilon=Lambda t² gives

    Sigma=-2A sqrt(Lambda) integral_0^infinity
                   t²/[(1+t²)²(t²+y²)]dt
         = -pi A sqrt(Lambda)/[2(1+y)²].

Its derivative below threshold is negative. A bound-pole normalization is
Z=[1-Sigma']^-1, in agreement with the note. The generic and tuned
threshold exponents follow from comparing a nonzero real constant with
the imaginary term pi A sqrt(epsilon); they are respectively +1/2 and -1/2.
For the flat-space finite-regulator NR contact extension, complete unordered pair
states have contact U|F><F| and source coupling gamma F, with U=4kc and
gamma=2c3 (the zero-momentum normalized pair has F0=1/sqrt(2V)). The
resolvent identity gives Sigma=gamma²L/(1-UL). For the continuum with a
finite UV cutoff L(0)<0 is finite, so Sigma(0)>-gamma²/U. A finite periodic
box retains its zero-relative-momentum pair and L(0-) diverges negatively;
the limiting Sigma is then exactly -gamma²/U. The original coefficients obey

    U delta > gamma²,
    lambda_tot > g²/[2M(M-2m)],

because lambda_tot=lambda_rep+g²/[(M-2m)(M+2m)] and M>2m.
Consequently nu=delta+Sigma(0)>=delta-gamma²/U>0. This excludes a zero-
threshold source pole for this positive specified finite-regulator NR
Hamiltonian. Equivalently its source/contact potential matrix is positive
definite, while relative kinetic energy is nonnegative. It does not promote
this coefficient delta to the dressed resonance detuning or cover arbitrary
mass counterterms/full relativistic loop matching. Newtonian gravitational
pair binding is absent from that displayed positive block; attractive gravity
can create subthreshold bound states and is not excluded by this argument.
The generic square-root
threshold survives the finite nonzero contact denominator.

The energy obstruction is conditional but exact: if each *occupied emitted
object* costs Omega=2d Delta, its energy density is 2 integral Delta w.
For the target this is logarithmically divergent even with variable d.
It does not apply to an unexcited object just because it has a high gap.
The formal UV tails leave the controlled leading source-pair projection;
they cannot serve as a measured or renormalized finite-energy population.

## Live relative mode and source

Transforming q_d,q_b to C,s diagonalizes the kinetic energy with reduced
mass mu=M_d M_b/(M_d+M_b). Uniform gravity couples only to total C.
Translation of the complete profiles gives the relative density
-i mu(k.s)(F_d-F_b), so the finite-k response must contain two factors of
F_d-F_b, one from drive and one from observed mass. Omitting the baryonic
term would falsely retain a uniform-field dipole.

For spherical profiles the Hessian is rotationally invariant and its trace
is integral rho_d laplacian U_b=4piG integral rho_d rho_b. Hence its one-axis
spring and frequency are exactly the stated kappa and kappa/mu on the
rigid-profile manifold. They are not automatically exact live normal modes.
The harmonic-core GP substitution independently gives qddot+omega_b²q=g.
A freely falling heavy core still has acceleration g, removing this drive.

For spherical compact profiles and a harmonic external U, every radial
shell averages grad U to grad U(0), so both mean accelerations are equal.
This is stronger than a small-k power count. For Gaussian unequal sizes,
F_d-F_b really does approach one between the two inverse radii. The
intermediate response is a genuine single-object possibility; its ensemble
homogenization is separately tested in PACKING_AND_SHARED_RESERVOIR.md.

Expanding erf(s/(sqrt(2)S))/s gives an energy quartic-to-quadratic ratio
-3s²/(20S²) and force correction -3s²/(10S²), confirming softening rather
than the rational model's hardening. Ordinary binding permits escape under
an indefinitely maintained relative force. The noted gravitational seagull
also follows from the second-order density expansion: the spring is already
contained in the Poisson energy and must not be added a second time.

## TF equilibrium, stability and tides

For p=K rho², hydrostatics gives rho=rho_c j0(pi r/R) and
R²=pi K/(2G). Direct mass integration gives rho_c=pi Mcal/(4R³).
The mass amplitude is free, so the radius relation supplies no selected
surface acceleration or population. The TF profile's sharp surface makes
the literal GP kinetic integral logarithmically divergent; it is an exact
fluid limit, with a quantum boundary layer needed at finite GP parameters.

I independently checked the density-Hessian argument. An eigenfunction
of the Newton integral operator has interior potential j_l(xr/R) and
matching condition x j_l'+(l+1)j_l=x j_(l-1)=0. Its quadratic coefficient is
K[1-pi²/x²]. The first l=1 eigenvalue is the translation zero and all l>=2
first roots exceed pi. For mass-preserving radial modes u=delta M(r), the
weighted Sturm operator -u''+2u'/r has regular eigenfunction r² j1(qr).
Dirichlet u(R)=0 gives qR=4.4934...>pi. This supports precisely local TF
density-mode stability, not full nonlinear or finite-GP stability.

For the axisymmetric STF tide U_ext=(e/2)r²P2, interior hydrostatics gives
H=A j2(pi r/R)P2. Matching the exterior B/r³P2 yields A=5eR²/2 and
B=eR⁵(15-pi²)/(2pi²). Since U_Q=-3G Qzz P2/(2r³),

    Qzz=-(15-pi²)R⁵ e/(3pi²G).

This derives the inverse-G response with the note's physical source and
normalization. The ensemble source is (1/2)partial_i partial_j(n Qij).
Using partial_j Eij=(2/3)partial_i laplacian U gives
P_i=n lambda_T partial_i laplacian U/3. Thus
4piG chi_eff=C f(kR)² with C=(15-pi²)/(3pi²), as stated. The trace/monopole
channel is separate and not proved absent. A uniform vacuum tide can deform
each object while its uniform-ensemble leading bulk P vanishes.

## Scope verdict

These three lanes establish actual conditional source-specific mechanisms
and spectra within their stated reductions. None establishes a populated
medium of local saturating acceleration dipoles or its universal normalization.
The remaining state, source and joint d-gap maps are mathematical obligations,
not numerical uncertainties repaired by the finite checks.
