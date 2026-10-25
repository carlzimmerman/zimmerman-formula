# Three distinct energy questions

1. Canonical energy in a fixed ball includes gravitational surface energy. Its increase during mass outflow does not alone decide the fate of a moving material remnant.
2. For a real smooth cutoff w and v=w psi, isolated nonlinear self-energy is E_self[v]=K[v]+W[v], with W[v]=(1/2) integral |v|² Phi[v]. The cutoff kinetic cost is part of K[v]. The full snapshot potential includes an additional envelope, so negative energy under that potential is not independent self-binding.
3. The FROZEN one-wave Hamiltonian H_self=K_operator+Phi[v] has expectation numerator K+2W, not K+W. Its negative-energy spectral weight is not a count of bound particles, a spatially retained mass or a long-term nonlinear capture fraction.

## Finite frozen-spectrum bounds

For a normalized wave and finite Hermitian H, let mu=<H>, sigma²=<H²>-mu², p the spectral probability of E<0. The weak kinetic form is positive semidefinite, so H>=a with a=min Phi<0. For mu<0, mu>=a p gives p>=mu/a.

A second bound follows from nonnegative conditional variances. Write q=1-p. If mu<0 and the nonnegative-energy conditional mean is y>=0, the negative-energy conditional mean is (mu-q y)/p. The variance is at least q(y-mu)²/p, minimized over y>=0 at y=0. Thus sigma²>=q mu²/p, so p>=mu²/(sigma²+mu²). For mu>0, reversing the signs gives p<=sigma²/(sigma²+mu²). Handle p=0 or1 by limits. These are exact finite spectral-measure inequalities; reported numbers use float64 with ordinary numerical error. Gaussian, boost and exact finite diagonal-measure controls test the implementation.

The calculation uses the FULL nonspherical frozen operator, not a monopole. Its lower kinetic bound is checked from the radial Hermitian matrix and nonnegative angular eigenvalues. A real density cutoff changes the trial wave and its self-potential; none of these diagnostics is applied as an extra force in evolution.

## Phase motion versus cutoff artifacts

Writing the physical wave psi=sqrt(rho) exp(i theta) gives

    K = (eta²/2) integral |grad sqrt(rho)|²
          + (eta²/2) integral rho |grad theta|².

The second term is K_phase. A real cutoff changes amplitude but preserves local phase where nonzero. Therefore its continuum K_phase is the original phase kinetic weighted by w². The finite SEM product rule is approximate; both versions are computed and their difference reported. The streaming implementation reproduces the previous weak partition on analytic and complex random fields.

For all declared windows/states, K_phase - Pz²/(2M) + W_self remains positive. Hence omitting ALL amplitude-gradient energy, not merely the cutoff cost, still does not make these entire measured windows self-bound at their present density. This does not exclude smaller bound components. It shows why removing net spin or translating the center is insufficient evidence of relaxation.

At fixed wave shape, scaling mass by c gives K→cK and W→c²W. Whole-window self-energy could become negative through mass alone only for c>K/abs(W). This is a diagnostic scaling, not an evolved assembly history or a permissible mass renormalization. Alternatively, at fixed density, achieving negative energy requires removing more than K-abs(W) kinetic energy while not increasing other costs. The fractions and implied masses in summary.json are conditional requirements, not demonstrated attainable changes.

## Common initial infall screen

The screened family is

    psi_lambda = psi_original exp[i(lambda-1) S(r)/eta].

It preserves density, mass supply, angular phase and Jz. Residual phase beyond the extracted radial carrier is retained. The weak kinetic form gives exactly on each fixed grid

    E_g(lambda)=A_g lambda²+B_g lambda+C_g+W_g,
    A_g=(1/2) integral rho [S'(r)]² >=0.

C contains the zero-carrier kinetic form; B is its cross term with the original radial phase. W is unchanged. Direct Gaussian and nonzero-cross-term controls verify the coefficient construction. This is a common fraction of the four original carriers, not a common physical infall speed and not a derived cosmological history.

All tested quadratics open upward, have E_g(0)<0 and one positive root lambda_g in[0,1.5]. Therefore requiring initial whole-wave negativity in Draco/Sextans but nonnegativity in both controls gives

    max(lambda_Fornax,lambda_LeoI) <= lambda
                                   < min(lambda_Draco,lambda_Sextans).

On ne256, this would require .687029874 <= lambda < .674276848, an empty interval. ne128 gives the same ordering; the gap changes by1.17e-7 between these grids. Strict negativity excludes the equality endpoint as well. This is complete sign coverage for the stated finite quadratic family, not a dynamic capture theorem. Positive-energy whole waves can contain negative-energy components; negative total energy does not supply the observed profile, retained core mass, star survival or the action bridge.
