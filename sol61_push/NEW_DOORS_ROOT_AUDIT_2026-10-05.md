# Root mathematical review

## Reciprocal cold action

Independently reconstructed p'(b)>0, p(b_t)=d and b_t'=2d(a0-d)/(a0-2d)^2. Differentiating the moving-boundary integral cancels its boundary term and yields g_b=b+p and g_c=kappa d+b_t on the active branch. Cross derivatives both vanish there and both equal one in the inactive branch. This is actual source reciprocity, not a force-level multiplier alone.

Peer review found a genuine source-stress error in the initial cold report. For nonlinear H the correct trace is the Legendre density: T_ij=[B_j g_bi+D_j g_ci-delta_ij(B·g_b+D·g_c-H)]/(4piG). Curl-free potential gradients then give div T=rho_b g_b+rho_c g_c. Subtracting H instead works only in the quadratic case and leaves the extra gradient of B·g_b+D·g_c-2H. The action and reciprocal forces remain correct; the corrected report and fresh main_c/control_c runs verify the repaired trace with an exact nonlinear three-dimensional quartic identity and reject the old trace.

For a norm-vector completion the radial Hessian is [[1,1],[1,kappa]] in the inactive branch and diagonal (1+p',kappa+b_t') in the active branch. Transverse eigenvalues g_b/b and g_c/d are nonnegative. At kappa>1 the lower scalar eigenvalue mu=(1+kappa-sqrt((kappa-1)^2+4))/2 is positive; subtracting mu(|B|^2+|D|^2)/2 leaves a convex, coordinatewise nondecreasing norm function, establishing the advertised global strong-convexity bound, including nondifferentiable zero-flux points in the convex sense.

This statement concerns a static constrained flux functional. The attractive potential action has the usual negative gradient energy after flux elimination. It supplies no gravitational Hamiltonian positivity or covariant-health proof.

For compact enclosed masses d'=-2d/r, circular orbit differentiation gives kappa_r^2=(3g_c-2d g_c')/r. Substitution yields the reported numerator. Requiring positivity through the whole active constant-ratio branch, whose endpoint is d/a0=1/(eta+2), gives kappa-(eta+4)/eta^2>=0. Positive background density adds a term to fixed-profile tracer stiffness, but that term is absent from a Lagrangian shell's enclosed self-mass derivative. Distinguishing these controls is essential.

The independent orbit potential at kappa=1 is -d0/(2r)+d0/(4 sqrt(2d0)) ln[(r-sqrt(2d0))/(r+sqrt(2d0))]. Direct differentiation matches the active force. The proposed finite positive profiles are selected radial supports, not a result about collisionless formation.

The global Newton-vector obstruction also admits a direct proof: opposite changes (B,D)->(B+V,D-V) preserve B+D and can place both endpoints in the full Newtonian OFF region. Convexity caps the midpoint energy by the common Newton energy plus its fixed constant. Along aligned fixed d<a0/2, exact baryon max response forces the excess integral to grow without bound with b. Any finite pure-cold boundary energy is eventually insufficient. This excludes globally convex energies satisfying those unrestricted constitutive assumptions; it does not exclude restricted-domain actions or theories with auxiliary fields/constraints whose reduced flux energy is not convex.

## Constrained transition

Independently varied U(g,q)=[g^2+f(q)(2g^3/(3a0)-g^2)]/(8pi G). U_gg and U_g/g are positive in the stated g>0, 0<=f<=1 domain. U_qg gives the scalar/field mixing. Eliminating deltaPhi in a longitudinal Fourier mode produces the Hermitian decrement C C^dagger/(U_gg k^2), where C=(m,ik U_qg). It is positive semidefinite before subtraction. Density inertia m/(n k^2) follows from a mass-conserving displacement, and scalar inertia nI is positive.

The resulting diagonal frequency entries are a=n e_nn k^2/m-nm/U_gg and b=(e_qq-U_qg^2/U_gg)/(nI); squared off-diagonal magnitude is e_nq^2 k^2/(mI)+m U_qg^2/(U_gg^2 I). These reconstruct the script's two roots. For e_nn>0 the finite ultraviolet low root is [e_qq-U_qg^2/U_gg-e_nq^2/e_nn]/(nI). Negative values imply growth, not negative inertia. A finite-k scan cannot prove a universal bound by itself. The report additionally gives P(-s)=k^2[alpha(b+s)-L]+(s-J)(b+s)-M. For s above both the ultraviolet limit and the positive k=0 root, each term is nonnegative, bounding every growth root; the two endpoint limits attain the supremum. This establishes the uniform bound under the stated alpha>0,b>0 premises.

Adding kappa k^2 to the scalar stiffness gives positive leading k^2 coefficients when e_nn,kappa,I,n,m are positive. Expanding the zero-frequency determinant gives

kappa e_nn y^2+[e_nn(e_qq-U_qg^2/U_gg)-e_nq^2-m^2 kappa/U_gg]y-m^2 e_qq/U_gg=0, y=k^2.

This independently confirms the corrected cutoff polynomial. All physical-scale, transition-width, conservation/stress, formation-history, and covariant completion claims remain open. The calculation is a local background analysis; uniform density with a constant acceleration is not a global Poisson equilibrium.

## Transfer source accounting

Checked the CLASS script's conventions: k(h/Mpc) is multiplied by h, Hubble is in inverse Mpc, theta is conformal divergence in inverse Mpc, and U=-a(theta_b-theta_c). In Newtonian gauge, metric terms cancel exactly in the relative continuity equation. The common gravitational potential cancels in the relative Euler equation. Gas source -c_b^2 k^2 delta_b and photon-drag source -opacity*(4rho_gamma/(3rho_b))*(theta_gamma-theta_b) therefore have the reported signs and factors. Cosmic integration uses dt/da=1/(aH).

The wave coefficient ell^2/4, ell=hbar*c/(m_eV*Mpc_metres), has consistent units. Its Born source ell^2 k^4 delta_c/(4a^2) and stiffness ratio ell^2 k^4/(4a^4 H^2) are correct. Integrating this source on unmodified cold transfers is a first-order pressure forecast, not a full wave Boltzmann solution. EdS growing/decaying coefficients reconstructed at an epoch do not imply exact EdS evolution of the CLASS state. Numerical source closure and template rank do not supply observational detectability or microscopic identity.

## Analytic control and review correction

The root kernel independently uses quadrature against both analytic primitives. Sibling review correctly required the common baryon/cold growing amplitude to be explicit for the constant gas template. The report now states delta_b=delta_c=Aa and gives the Ab/Ac alternative. Run `main_b_explicit_common_mode` pins the clarification; `main_a` is historical and has a stale report hash. Its computational script and numerical formulas were unchanged. No stale run is used as current evidence.
