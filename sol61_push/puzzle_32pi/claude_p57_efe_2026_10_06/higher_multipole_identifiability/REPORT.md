# Finite external-field multipoles do not identify the vacuum moment

At fixed external Newtonian field, the next even inner multipole supplies independent information: the old two-bump quadrupole-null perturbation changes the hexadecapole. Nevertheless, three compact high-acceleration bumps preserve both exactly and change C. More generally, any finite collection of these inner even multipoles at finitely many external fields has a compact-support null direction with nonzero vacuum moment. This is a constitutive-kernel result, not a healthy covariant-action construction or a statement that the full p57 likelihood is preserved.

## Current Claude input and conventions

The inspected checkout HEAD was cfa06dbfae97280425bbb61f862eb61468c03dce. Current p57 explicitly uses the field-equation QUMOND multipoles through l=8, rather than its withdrawn algebraic force. Its amended 150-particle orbit-averaged calculation freezes particles at q<25 AU, omits Neptune scattering, and reports final detached fraction and time-averaged detached occupancy. No astronomical or orbit calculation was rerun here. The current README verdict is inconclusive for its registered final-fraction decision; our finite inner-multipole theorem does not preserve either nonlinear statistic.

Let r_M=sqrt(GM/a0), e=g_N,external/a0>0, and f(y)=nu(y)-1. The physical anomalous acceleration is grad psi, with psi=-Phi_p and Delta psi=div D. Use D=f(|G|/a0)G-f(e)a0 e zhat, G=-GM rhat/r^2+a0 e zhat. Write psi=sum psi_l(r)P_l(mu). For l>=2, define the inner harmonic coefficient

    A_l = -1/(2l+1) integral_0^infinity s_l(r) r^(1-l) dr,
    psi_l(r)=A_l r^l + local-source contributions,

where s_l=(2l+1)/2 integral_{-1}^1 div D P_l dmu. For compact high-y perturbations the anomalous source is separated from the origin and its contribution is exactly harmonic there. Thus delta A_l has no local-source ambiguity. The quadrupole convention is Phi_Q=-Q2 r^2 P2/3, hence Q2=3 A2. A4 here is the coefficient of r^4 P4 in psi, not a quadrupole-normalized number.

## Exact functional and the next multipole

For even l>=2, put t=(r_M/r)^2, xi=-mu, y=sqrt(e^2+t^2+2et xi), and

    H_l(t,xi)=(l+1)(t+e xi)P_l(xi)-e(1-xi^2)P_l'(xi).
    W_l,e(y)= integral_{|y-e|}^{y+e} [y/(2e)] t^((l-5)/2) H_l(t,xi(y,t)) dt.
    M_l=integral_0^infinity f(y)W_l,e(y)dy,
    A_l=a0 M_l/(2 r_M^(l-1)).

For the perturbations used here all integrations are ordinary convergent compact-support integrals. Derivation: insert the spherical divergence in A_l, integrate its radial derivative by parts, and integrate the angular divergence by parts. This gives -1/2 integral r^(-l)[(l+1)D_r P_l+D_theta sin(theta)P_l'] dr dmu. Substitution of G, even-l parity and dr=-(r_M/2)t^(-3/2)dt yields the displayed normalization. The removed uniform external field contributes only l=1. For l=2, H2 is -3/2 times the parent quadrupole integrand, so W2=-3 w_parent/2. Consequently Q2=-9a0/(4r_M) integral f w_parent, agreeing with the independent parent convention.

For y>e, q=e/y, W4=y^(3/2) F4(q), with the exact expression

    F4(q)=-5/(77q^5)[sqrt(1+q)(2q^5-q^4+20q^3-68q^2-56q+112)
                   +sqrt(1-q)(2q^5+q^4+20q^3+68q^2-56q-112)].

Its cancellations require sufficiently precise arithmetic at small q. Exact symbolic primitive and endpoint checks give

    W4=-5e^4/(112 y^(5/2))-65e^6/(1408 y^(9/2))+O(y^(-13/2)),
    W2=-3e^2/(20 y^(3/2))-33e^4/(224 y^(7/2))+O(y^(-11/2)).

Their ratio tends to (25/84)e^2/y. Thus the two weights are functionally independent, and neither can span the growing vacuum weight y.

## General finite-observable theorem

Fix finitely many pairs (e_j,l_j), with e_j>0 and even l_j>=2, and a finite tested y-window. In the unrestricted smooth-kernel class there exists f_delta in C_c^infinity((Y,infinity)), with Y larger than that window and every e_j, such that every integral W_lj,ej f_delta vanishes but integral y f_delta is nonzero.

The substantive asymptotic step is W_l,e=O(e^l y^(-(l+1)/2)), not a dimensional assumption. Scaling t=y tau gives W_l,e=y^((l-1)/2)F_l(e/y). With tau=1+qz, z in [-1,1],

    xi= -[z+q(1+z^2)/2]/(1+qz),
    F_l(q)=1/2 integral (1+qz)^((l-5)/2)
      [(l+1)(1+qz+qxi)P_l(xi)-q(1-xi^2)P_l'(xi)] dz.

This is analytic for |q|<1. Its coefficients below q^l vanish by rotational covariance, as follows. For any compact annular radial perturbation, its inner harmonic rank-l symmetric trace-free tensor is a smooth rotationally covariant function of the Cartesian external field E near zero. A Taylor term of degree n<l is built from an isotropic rank-(l+n) tensor contracted with n copies of E. At least two free symmetric indices must be paired by a Kronecker delta; its STF projection vanishes. Levi-Civita contributions vanish on symmetrization. Therefore the multipole starts at degree l. Applying this to every radial test perturbation and using test-function duality forces all coefficients of F_l below degree l to vanish pointwise. This proves the stated high-y bound (and even parity permits only subsequent even powers).

Now consider the linear map O from V=C_c^infinity((Y,infinity)) to the finite response vector. If ker O were contained in the kernel of C_delta(f)=integral y f, then C_delta would factor through the finite-dimensional image of O. Some constants a_j would satisfy C_delta=sum a_j O_j on V. Test-function duality would imply y=sum a_j W_lj,ej(y) throughout (Y,infinity), impossible because the right side is o(y). This proves the nonzero-C null direction, including redundant observables. It is not merely counting dimensions.

If the starting kernel satisfies f>0, nu'<0 and (y nu)'>0 strictly on the perturbation's compact support, multiplying the null direction by a sufficiently small nonzero amplitude preserves all three inequalities. The finite measured window and ambient nu(e_j) and all its derivatives are unchanged exactly. The theorem does not apply to real-analytic restrictions (compact support is then unavailable), infinitely many external fields, the full radial multipole functions, or arbitrary nonlinear observables. It does not establish arbitrary finite changes in C.

## Concrete controlled family

Use Claude's cutoff T=128.9153707043 without refitting it:

    f_T(y)=1/[y(sqrt(1+1/y)+1)(1+(y/T)^2)].

With a0=9.3603e-11 and observed external field 2.146e-10 SI, solve e[1+f_T(e)]=g_external/a0, giving e approximately 1.84663944. Let B(z)=z^3(1-z)^3 on [0,1] and zero elsewhere. For Y=1000,

    delta nu=1e-10 [B(y/Y-1)-17.50521049545364 B(y/Y-3)
                                    +27.39325028388057 B(y/Y-5)].

The coefficients are defined exactly by the two linear integral-null equations, not by their printed decimals. These C2 bumps are sufficient for these observables; the universal smooth theorem uses C-infinity test functions. Their supports are [1000,2000], [3000,4000], [5000,6000]. Since integral y B(y/Y-j)dy=Y^2(2j+1)/280, the exact defined family has

    delta M2=delta M4=0,
    delta C=0.00006492474273375385...

The earlier two-bump M2-null family has delta M4/amplitude=-2.62216699636e-8, so l4 supplies a genuine new discriminator before the additional freedom is included. Uniform bounds |B|<=1/64 and |B'|<=3/16 certify positive excess, decreasing nu and increasing y nu for the three-bump example. Their conservative remaining margins are respectively 3.8408152e-8, 8.0204346e-12 and 0.9974808285. These are constitutive monotonicity/source-inversion conditions; no full relativistic Hessian is tested here.

## Evidence and remaining arrow

The bounded script proves the l4 primitive and first series coefficients symbolically, checks direct weight integrals at q=.01,.1,.3, constructs the response-null family with 80-digit quadrature and repeats coefficient extraction at 100 digits (relative difference below 1e-53), and checks conservative uniform margins. It does not provide interval quadrature certificates. The exact existence and null definitions are mathematical statements above; the printed floating coefficients alone are not exact certificates. Negative controls remove the third bump, assert finite multipoles determine C, or reverse the Q2 normalization; each must fail its corresponding check.

The missing physical arrow is a justified restriction from the same covariant action that rules out these response-null kernels, or a full continuum of independent measurements. The numerical moment C is imported from the prior vacuum normalization; QUMOND's NR field equation alone does not identify Lambda or prove C=32pi. Neither the finite theorem nor the example preserves p57's nonlinear secular occupancy or final-fraction likelihood. Higher multipoles may constrain a specified finite-parameter family considerably; they do not select C over the unrestricted smooth response class.

Primary field-law source: Milgrom, *Quasi-linear formulation of MOND*, arXiv:0911.5464v2 (2 March 2010), equations (3)-(8), https://arxiv.org/html/0911.5464v2 . All l4 and finite-null derivations here are reconstructed directly; no novelty claim about the literature is made. Source copies and exact input hashes are indexed in sources.json and provenance.json. No new observational exclusion is claimed.
