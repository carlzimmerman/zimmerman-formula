# Closed S3_R x S1_L ensemble: CDQ-001 raw derivation

This derives the leading center-stabilized SU2 monopole EFT, including the neutral compact ensemble and its one-loop metric response. L is fixed and small; R tends to infinity at fixed positive matched parameters. No boundary, isolated-monopole tail truncation, electromagnetic coupling, quark or proton observable enters.

## 1. Parameters, source translation and global field domain

Start with the deformed action S_YM + integral_S3 sqrt(g) L^-3 P(Omega), where P=a1 |tr Omega|² stabilizes SU2 center symmetry, together with a real theta phase. Its flat-space weak-coupling input is authenticated in Unsal–Yaffe 0803.0344v2, PDF equations (2.1)-(2.5), (3.5)-(3.30), appendix A. In their root convention alpha1=(1,-1), alpha2=-alpha1. Remove the auxiliary decoupled U1 scalar. Set sigma_vector=(phi/2,-phi/2); then |d sigma_vector|²=(d phi)²/2. The physical scalar kinetic term is

    (kappa/2) (d phi)²,       kappa=g²/(8pi²L).

Let f be the weight per signed event per spatial volume, parametrically

    f=A mW³ (2g²)^-2 exp(-Delta S) exp[-4pi²/g²(mW)],  mW=pi/L.

A is the entire flat nonzero-mode prefactor in a common scheme, not a zero-mode norm; neither A nor Delta S is numerically fitted or evaluated here. At a Wilsonian scale m<<Lambda_UV<<mW, f and kappa mean matched renormalized coefficients. Higher operators and hard metric coefficients must use the same scheme. The source's printed gas equation (3.22) and cosine equation (3.25) differ by a factor two when both symbols zeta denote the per-sign weight. We resolve this algebraically: signed weight f gives cosine amplitude 2f per species. If zeta denotes the coefficient in the printed cosine action, zeta=2f. No physical coefficient below depends on silently choosing between them.

In a root-lattice SU2 cell one may take phi in [0,4pi), with two identical potential cells. A one-cell description uses [0,2pi). Denote the finite cell multiplicity by p (p=2 for the former choice). A constant overall p is retained explicitly. Choices of line-operator/global quotient convention can change this finite multiplicity; all local/neutral normalized formulas and all metric derivatives here are independent of p. We do not add an extra continuous free U1 mode. S3 has H1=H2=0; there are no smooth scalar winding sectors or Abelian harmonic magnetic flux sectors on this spatial manifold. Singular electric-line sectors and heavy W worldlines are outside the retained smooth EFT.

## 2. Exact closed-ensemble identity with a UV prescription

An event e has magnetic q_e and topological t_e. The four vertices are

    f exp[i(phi+theta/2)],    f exp[i(-phi+theta/2)],
    f exp[-i(phi+theta/2)],   f exp[-i(-phi+theta/2)].

Sum the event counts before approximating:

    S_EFT = integral sqrt(g) [kappa/2 (d phi)²
                              -4f cos(theta/2) cos(phi)] + S_hard[g,L].       (D1)

The theta argument is real, as follows from the phase weights. The source's printed i theta in (3.29) is not inherited. A compact zero-mode integral imposes sum q_e=0 exactly. If n_a-bar n_a=Q_a for the two monopole species, neutrality is Q1=Q2=Q, so total topological charge (Q1+Q2)/2=Q is an integer. Thus the full ensemble on the closed manifold is 2pi periodic in theta even though a selected saddle branch need not be.

For precision, regulate the nonconstant field at a fixed physical cutoff Lambda_UV and use one local covariant subtraction for core self energies and fugacity. Write phi=phi0+eta, integral eta=0. Its Gaussian covariance is G_R/kappa, where

    -Delta G_R(x,y)=delta_g(x,y)-1/V,   integral_x G_R(x,y)=0,
    V=2pi²R³.

If J(x)=sum_e q_e delta_g(x,x_e), Gaussian integration gives

    Z_gas = sum_counts [f^K / product n_e!]
             integral product dvol(x_e) delta_(sum q_e,0)
             exp[i theta sum t_e]
             exp[-(1/(2kappa)) sum_(e,e') q_e q_e' G_R^reg(x_e,x_e')].       (D2)

The notation includes the consistently regulated self terms. Equivalently, subtract a common flat local singular self part and absorb only that part into f. Smooth, geometry-dependent regular self terms cannot also be removed from G without the compensating redefinition of f. The gas with point charges has an attractive short-distance collapse if the cutoff/core prescription is discarded; (D2) is an EFT identity with its core regulator, not an unregulated convergent point-plasma theorem. Charge-neutral backgrounds ensure the inverse Laplacian exists. Adding a constant c to all G entries changes the last exponent by -c(sum q_e)²/(2kappa)=0, including self terms. Hence a regular self-energy constant alone is not a physical fugacity response.

Let Z_0,can be the canonical compact free-scalar partition, with all nonconstant modes regulated identically. Then the normalized gas identity is

    Z_gas=Z_EFT,can/Z_0,can,        Z_total=N_hard[g,L] Z_EFT,can.           (D3)

The normalized gas alone has divided out the perturbative photon determinant. Its metric variation is not the total gauge-sector metric variation. The hard matching factor is left explicit, not set to one.

## 3. Exact compact uniform sector and theta branches

Freezing eta gives a well-defined exact integral for this uniform sector. Put lambda=fV, z=4lambda cos(theta/2). With normalized compact Haar measure,

    Z_tilde0 = integral_0^(2pi) dphi/(2pi) exp[z cos(phi)]
             = I0(z)
             = sum_(Q in Z) I_Q(2lambda)² exp(i Q theta).                  (D4)

The last equality follows by expanding each species' signed counts and applying Q1=Q2. All fixed-topology weights are nonnegative. For example, at small lambda, Z_tilde0=1+2lambda²(1+cos theta)+O(lambda^4); Q=+/-1 first occurs with weight lambda². At fixed finite V there is no term linear in f, since a single event violates exact neutrality. Taking V large at fixed f resums arbitrarily many events and produces extensive leading action -4f V |cos(theta/2)|. This is an order-of-limits issue, not a conflict.

The finite-volume function is smooth and 2pi periodic. The large-volume minimum switches from phi=0 modulo 2pi when cos(theta/2)>0 to phi=pi modulo 2pi when cos(theta/2)<0. Its energy is the lower envelope of the two theta branches -4f cos[(theta+2pi k)/2], k=0,1. Extra identical compact cells supply p only. At theta=pi the order-f potential vanishes; correlated pairs/higher operators are then leading and this massive saddle calculation does not apply.

(D4) is not the full interacting gas. It is exact after uniform-mode truncation and is useful for auditing neutrality, topology and compact normalization. In a small-box epsilon-type regime mR<<1 and kappa R>>1, nonconstant corrections can be organized perturbatively; in the desired fixed-m large-R regime we instead use the full saddle and determinant below. No exact-product ansatz I0(z) times an arbitrarily chosen determinant is claimed for the interacting theory.

## 4. Canonical zero-mode measure and the apparent finite-volume term

At a chosen stable saddle shift phi so the potential is -u cos(phi), with

    u=4f|cos(theta/2)|,        m²=u/kappa>0.

The canonical field is varphi=sqrt(kappa) phi and its orthonormal constant coefficient is a0=sqrt(kappa V) phi0. Each real mode is integrated with (mu/sqrt(2pi)) da, with fixed reference mass mu. Therefore the normalized compact integral (D4) has canonical factor

    J0=p mu sqrt(2pi kappa V),       Z_0,uniform=J0 I0(uV).                (D5)

This factor is forced by the coordinate change; it is not N_hard. Near each stable saddle,

    I0(z)= exp(z)/sqrt(2pi z) [1+1/(8z)+O(z^-2)],
    J0 I0(z)=p (mu/m) exp(uV) [1+1/(8uV)+O((uV)^-2)].                   (D6)

The leading Gaussian constant eigenvalue is m², independent of R. With Haar measure alone, d_V[-log I0(uV)]=-u+1/(2V)+O(V^-2). The derivative of -log J0 is -1/(2V), cancelling that term. The exact isolated uniform-sector derivative is

    epsilon_0=-u I1(uV)/I0(uV)-1/(2V)
             =-u+1/(8uV²)+O(V^-3).                                  (D7)

Its leftover V^-2 term is a uniform-sector interaction contribution, not a complete two-loop finite-volume result. In a full diagrammatic expansion the nonconstant-mode interactions must be included in the same counting. In particular, do not add (D7)'s isolated remainder to the one-loop determinant and advertise a controlled complete two-loop answer.

## 5. Complete leading saddle and Gaussian field determinant

For mR>>1, m<<mW and m/kappa<<1, the loop expansion of (D1) about a stable branch is controlled. The weak-coupling small-circle theory has this hierarchy parametrically. The complete Gaussian partition of the retained physical scalar, including its constant mode, is

    Z_EFT,can = p exp(uV) det[(-Delta_S3+m²)/mu²]^-1/2
                 times [interaction corrections].                    (D8)

Consequently W_EFT=-uV+W_m-log p, with W_m=(1/2)log det(P/mu²). The zero mode in (D8) already includes mu/m from (D6). Counting it twice, dropping it, or using a volume-independent normalized Haar measure changes finite-volume terms incorrectly. All hard local terms, their L-dependence, and any remaining gauge-to-dual global normalization reside in W_hard=-log N_hard.

Derive the S3 scalar spectrum by restricting degree-l harmonic polynomials of R4: radial separation gives -Delta eigenvalue l(l+2)/R² and dimension binomial(l+3,3)-binomial(l+1,3)=(l+1)². Thus

    P_n=(n²+a²)/R², d_n=n², n=1,2,..., a²=(mR)²-1.                     (D9)

Use a common zeta/finite-part local scheme. A positive massive scalar on a closed odd-dimensional manifold has no t^0 heat coefficient, so its full spectral zeta at zero is zero; there is no mu-dependent logarithmic scale term for this complete determinant. This also follows by Poisson summation of (D9) below. To compute the determinant, differentiate first and then retain the finite part:

    sum_(n>=1)^FP n²/(n²+a²)=-pi a coth(pi a)/2,
    d_a W_m=-pi a² coth(pi a)/2.                                     (D10)

Indeed sum 1 is zeta_R(0)=-1/2 and sum 1/(n²+a²)=[pi a coth(pi a)-1]/(2a²). Fix the integration constant by the proper-time scheme which retains the flat local term and has exponentially vanishing winding part for a->infinity. For a>0,

    W_m=-pi a³/6 + W_wrap(a),
    W_wrap(a)=pi integral_a^infinity t²/(exp(2pi t)-1) dt
      =a² Li1(exp(-2pi a))/2 + a Li2(exp(-2pi a))/(2pi)
                                +Li3(exp(-2pi a))/(4pi²).             (D11)

No mass-independent integration constant that varies with R is introduced. An additive fixed constant has no stress. Check (D11) at a=0: W_m=zeta_R(3)/(4pi²), also following directly from eigenvalues n²/R². Arbitrary local cosmological and curvature counterterms are part of matched W_hard; this convention evaluates the retained determinant rather than predicting those counterterms.

An independent heat-kernel derivation uses Poisson summation:

    K_P(t)=exp[-(m²-R^-2)t] sqrt(pi) R³/(4t^(3/2))
       times sum_(k in Z) [1-2pi²k²R²/t] exp[-pi²k²R²/t].              (D12)

The k=0 term integrates to -V(m²-R^-2)^(3/2)/(12pi), precisely the first term of (D11). The k!=0 terms are finite under proper-time integration, give W_wrap, and are exponentially suppressed at a large. This calculation, rather than a mass-gap assertion, determines the absence of an R² term in W_EFT.

## 6. Bulk subtraction and actual metric derivatives

At fixed matched f,kappa,L, subtract the flat extensive action in the same scheme:

    W_flat=V[-u-m³/(12pi)],
    Delta W= -(pi/6)[((mR)²-1)^(3/2)-(mR)³]+W_wrap(a)-log p.           (D13)

The flat p convention can remove log p; either way it has zero stress. At large fixed mR,

    Delta W = pi mR/4 -pi/(16mR)-pi/(96m³R³)+...
                 +O(poly(mR) exp[-2pi sqrt((mR)²-1)]).                (D14)

There is no R² term. In particular Delta W/(LV)=m/(8pi L R²)-1/(32pi L m R^4)+...; this quotient is a free-energy density, not a spatial metric derivative.

Define the isotropic spatial Euclidean response by varying R at fixed L and microscopic/matched coefficients:

    tau_s = (1/L) d_V W = (1/(3LV)) R d_R W,
    Delta tau_s = m³/(12pi L)
             [1-sqrt(1-(mR)^-2) coth(pi sqrt((mR)²-1))]
       = m/(24pi L R²)+1/(96pi L m R^4)+1/(192pi L m³R^6)+...
             +exponentially small terms.                            (D15)

Hence lim_(R->infinity) R Delta tau_s=0 for the complete leading tree plus Gaussian compact-ensemble contribution at fixed matched local parameters. The O(f) contact/vacuum potential -uV is included, not discarded as a propagating-mode contribution; its bulk-subtracted response is exactly zero for radius-independent u. Ordinary local hard curvature terms c1(L) integral sqrt(g) R3 contribute O(R^-2); higher analytic curvature terms contribute even powers R^-2j. Their coefficients are not determined here.

S3 x S1 is anisotropic. A temporal Euclidean response is instead tau_L=(1/V) partial_L W with the microscopic/deformation parameters held fixed, allowing f(L), kappa(L) and m(L) to vary. For the retained determinant at fixed R,

    Delta tau_L = (partial_L m²) m/(8pi)
             [1-sqrt(1-(mR)^-2) coth(pi sqrt((mR)²-1))]
       = (partial_L m²)/(16pi m R²)+O(R^-4).                          (D16)

The tree term -partial_L u cancels its flat subtraction if u is R independent. Equation (D16) states a response in terms of the matching functions; it does not pretend their L derivative was numerically computed. A Lorentzian vacuum energy requires the state and analytic-continuation dictionary. The absence of 1/R in both retained Euclidean responses does not supply that dictionary.

For completeness, the normalized monopole gas (D3) divides by a compact massless scalar. In the same canonical convention

    W_0= -log[p mu sqrt(2pi kappa V)]
                       +(1/2)log det'(-Delta/mu²).

Here the prime excludes its genuine zero mode, zeta'_operator(0) has zeta_operator(0)=-1, and radius scaling yields W_0=-(1/2)log(kappa R)+constant. Its spatial derivative is -1/(6LV), of order R^-3. Thus W_gas=-uV+W_m-W_0-log p has an additional +1/(6LV) in its spatial response. Multiplying back the perturbative scalar/photon partition removes that term. Neither convention gives 1/R, and confusing their observables would still be an error.

## 7. What remains unknown and how a linear term would enter

The computed statement concerns D1 with fixed local f,kappa and the canonical compact measure. The full gauge theory also requires W_hard[g,L] and common curved monopole-core matching. If the true matched fugacity had

    f_R=f_infinity [1+b(L)/(mW R)+o(R^-1)],

then already the tree functional would shift by

    Delta W_tree= -4 f_infinity |cos(theta/2)| b V/(mW R),
    Delta tau_s,tree= -8 f_infinity |cos(theta/2)| b/(3 L mW R).        (D17)

No value or nonzero existence of b is inferred. Local hard matching analytic in the curvature of a closed sphere does not generate b/R; showing that all core/long-distance/gauge-global pieces combine into that local matching requires the common-regulator gauge-to-dual calculation. A residual metric-dependent matching factor with W_hard proportional to R² would likewise give a linear inverse-radius stress. It is not fixed by normalized theta derivatives or by the canonical constant-mode Jacobian. We have neither assigned such a factor nor proved its absence in full deformed Yang–Mills. This is the first unresolved matching arrow.

The response to a hypothetical matching shift can also include the known one-loop ring contribution. Write f_R=f0+f1/R+..., kappa_R=kappa0+kappa1/R+..., u_i=4|cos(theta/2)| f_i, and m0²=u0/kappa0. The local tree-plus-ring density is F(u,kappa)=-u-(u/kappa)^(3/2)/(12pi). Its coefficient of 1/R is

    C1= -[1+m0/(8pi kappa0)] u1 + m0³ kappa1/(8pi kappa0).            (D18)

Thus the corresponding leading matching responses are

    Delta[W/(LV)] = C1/(LR)+...,
    Delta tau_s = 2 C1/(3LR)+...,
    Delta tau_L = (partial_L C1)/R+... .                              (D19)

The source parameters on this hypothetical path must obey the same common matching convention, and the formulas retain only the computed tree plus Gaussian order. With kappa1=0, the spatial coefficient is -8|cos(theta/2)| f1[1+m0/(8pi kappa0)]/(3L). Hard normalization contributes its own C1_hard if present. Equations (D18)-(D19) expose a missing matching input, not a prediction that it is nonzero. Variations of the R^-2 determinant curvature term induced by f1 begin at R^-3 and do not alter these 1/R formulas.

The explicit conditional result is therefore a controlled zero from the complete leading retained ensemble, rather than a zero for every omitted gauge-theory sector. It neither proves a no-go for physical QCD nor evaluates A_rho, electromagnetic-alpha dependence, or R(alpha). The small L stays fixed throughout.
