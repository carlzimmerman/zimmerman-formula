# Stronger candidate: an increasing scale profile controls the coupling

Root derivation, 2026-09-30, from the reviewed FGF023 equilibrium and Hessian.
This is an exact proposed improvement to its sufficient short-slab condition,
not a claim of physical theory closure or historical novelty.

Keep C=4piG, lambda=b_g>0, q=g lambda-B>0, positive rho,J,cs² and kinetic
coefficients. On a regular compact hydrostatic patch with g>0 define
w=chi', R=rho q/lambda, and M=U''-T_chi-q²/lambda. Assume w>0 throughout
the closed interval. Compactness then gives a positive minimum of w. No
assumption is made that M itself is positive.

Differentiate J chi''=U'-T(g,chi) along the equilibrium. Because T_g=q,
J w''=(U''-T_chi)w-qg'. Since lambda g'=C rho+q w,

    J w''=M w-C R.                                      (1)

The eta/matter part of FGF023's factorized energy has the exact identity

 J eta'²+M eta²+C R(w xi²+2xi eta)
   =J w²[(eta/w)']²+(C R/w)(eta+w xi)²
     +[J(w'/w)eta²]'.                                  (2)

To verify, the first square plus the total derivative gives
J eta'²+(J w''/w)eta²; the second gives the remaining terms by (1).
This checks every sign without assuming a uniform scale equilibrium.

Consequently the full quadratic potential equals

 2V=integral {cs² rho xi'²
       +lambda/C[psi'+(C rho xi-q eta)/lambda]²
       +J w²/C[(eta/w)']²+R/w(eta+w xi)²} dx
       +[cs²rho'xi²-2rho xi psi+(J/C)(w'/w)eta²]_left^right. (3)

All three perturbations vanish at the fixed endpoints, so the boundary term
is zero. Every volume term is nonnegative. Zero energy forces xi'=0, hence
xi=0. Then the last square forces eta=0 (R/w>0), and the potential-gradient
square forces psi'=0, hence psi=0. Smooth compact positive coefficients also
supply coercivity through the derivative squares and Dirichlet inequalities.
With positive kinetic form, this is a sufficient longitudinal linear stability
criterion on every such regular monotone-increasing scale patch. There is no
explicit length restriction or old Poincare determinant assumption.

This is NOT existence of arbitrarily long increasing solutions. FGF023 local
IVP with w_i>0 gives a nonempty family; continued intervals must retain w>0,
regularity and positive density. We have not yet supplied a specific longer
family where the old sufficient bound fails. If w reaches zero the formula
is singular; if w<0 the last square has a negative coefficient. Neither case
alone proves instability. They are outside this positivity theorem.

The earlier positive Dirichlet rank-one term from static psi elimination is
unchanged and must not be discarded as an equality. Here the psi square is
kept in the full dynamical energy. No static elimination of eta is used.

Controls intrinsic to the algebra: (i) changing M to M+delta while keeping
(1) unchanged leaves residual delta eta²; thus equilibrium must be used;
(ii) neglecting endpoint terms is unjustified for non-Dirichlet eta;
(iii) sign-changing/zero w is not admitted by dividing through w; (iv) setting
eta=0 alone does not freeze the background scale; chi' coupling remains.
These are symbolic controls, not claimed numerical executions.

This uses Q or R MOND constitutive flux B'=C rho, not Newtonian missing mass.
Both a_ref=9.3619e-11 and 1.1279e-10 m/s² are separate positive inputs; frozen
a_ref=a0 E(z) and constant-vacuum references remain distinct. The local a varies,
so literal pointwise constant-vacuum scale compatibility is not repaired.
No registered M action, metric/photon theory, zero-field, free-boundary,
3D/nonlinear or observational conclusion follows. No imported mechanism.
