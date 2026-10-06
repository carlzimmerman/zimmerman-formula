# Root check: exchanging the dust variable does not remove the kinetic zero

This is an algebraic audit of the supplied full quadratic action, not an invariant instability verdict or a computation of perturbation growth. Write `C=Sigma+kappa M p²`, `d=M/Theta`, `e=rho/(2Theta)` and `A=3M+C d²`, with positive `M,rho,p²` and nonzero `Theta`. Impose the finite-mode shift constraint `nu=d zetadot+e v` in the gravitational and exact dust action. Integrate `pi vdot` by parts with the actual `a_FRW³` volume factor. The coefficient of `v²` is

`B=C e²-rho p²/2`.

The coefficient of `v zetadot` is

`Lz=2e(Cd+3Theta)=rho A/M`.

Volume-factor derivatives, the `-d pi zetadot` term, matter tadpoles and all scalar potentials remain in the action; they do not change these two coefficients. Where `B!=0`, eliminating `v` therefore produces the two-velocity block

`A zetadot²-[(rho A/M) zetadot-pidot]²/(4B)`.

Its determinant is `-A/(4B)`. At an instantaneous clock zero `A=0`, one has `C=-3Theta²/M`, hence

`B=-3rho²/(4M)-rho p²/2<0`, `Lz=0`.

Thus dust elimination is regular at this zero, but the resulting second-order velocity matrix has rank one instead of two. In particular this dust momentum/coordinate exchange does not make the zero disappear. Any smooth invertible point transformation of these two variables preserves that rank by congruence. This conclusion is stronger than simply observing the negative sign in one representation, and weaker than proving that no regular canonical or gauge formulation exists.

The full null-direction equation still includes one-derivative clock–density mixing and time derivatives of the coefficients. It must be evaluated before claiming a physical evolution singularity, a ghost, or a Jeans growth rate. In particular a zero of the velocity coefficient cannot be crossed by dividing the evolution equations by `A`. This note supplies an exact local diagnostic for that next calculation.
