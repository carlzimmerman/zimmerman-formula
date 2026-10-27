# Converging the Coulomb molecular parent

Base findings97b95ad15df9d49ca2f24da3c0c824277981be48. The goal remains physical,
charge/energy-conserving nonequilibrium assembly and unlabeled galaxy separation.
This stage uses the research-program/computation-audit workflow. No successful
galaxy model is assumed. Atomic units: mC=hbar=Q²/(4pi epsilon)=1.

Replace the minimal1s two-orbital approximation by a systematic Rayleigh-Ritz
basis for the clamped-nuclei one-electron Coulomb problem. In prolate coordinates
xi=(rA+rB)/R>=1, eta=(rA-rB)/R, and azimuthal m=0, use
f_nl=exp(-t/2) L_n(t) P_l(eta), t=R(xi-1),
with angular Legendre polynomials orthonormalized. Even l gives gerade, odd l
ungerade. This fixes the exponential at the separated hydrogenic scale but
increases both polynomial orders. No physical coupling is fitted.

Removing the common volume factor, the overlap and energy forms are
B=integral (xi²-eta²) f f,
H=2/R² integral[(xi²-1) f_xi f_xi+(1-eta²) f_eta f_eta]
  -4/R integral xi f f.
Generalized eigenvalues give electronic energy; add+1/R nuclear repulsion.
Gauss-Laguerre and Gauss-Legendre quadrature integrates the polynomial weighted
forms; orders exceed the degree required by the chosen bases. Dipole matrix
is (R/2) integral xi eta (xi²-eta²) f_g f_u in the same normalization.

Check nested orders (nr,na)=(6,8),(10,14),(14,22),(18,30) at nine separations;
compute full curves at the two middle orders. Report energies, dipoles and
eigen-equation residuals. Basis convergence, radial discretization, continuum
normalization, energy-domain coverage and time-integration accuracy are separate
obligations. Finite BO/mass/spin approximations of the earlier parent remain.

Primary context: Francisco M. Fernández and Javier Garcia, 'Highly accurate
potential energy curves for the hydrogen molecule ion', arXiv:2107.01228,
https://arxiv.org/abs/2107.01228 . It uses a different Riccati-Pade method. We
construct our own variational curves; an abstract is not numerical certification
of every table entry. No novelty claim or exact-spectrum claim.
