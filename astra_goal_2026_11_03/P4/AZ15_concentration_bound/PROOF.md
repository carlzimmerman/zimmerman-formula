# AZ15 — PASS conditional concentration bound

κ = ½ FITTED; not theory closed

## Claim and domain

For the SAME AZ14 constitutive term, write psi=rho^(1/4), M=integral psi^4>0, J=integral |grad psi|^4>0, and F=256lambda J. Assume smooth nonnegative psi on R³, finite M,J, sufficient decay, positive fixed lambda, isolated Newtonian self-gravity, and conserved total energy with nonnegative kinetic energy. The claim is a uniform upper bound on F and rho_max at fixed mass and energy. It is not existence or uniqueness of a solution, no-contraction, a CMB solution, or a relativistic theory. A finite-mass nonzero function with J=0 is impossible on R³; the zero-density case is trivial and excluded from divisions below.

## Direct bound without an imported embedding theorem

For any ball B_R centered at x, integrate the fundamental theorem of calculus along radial segments from x to y, then average y over the ball. Taking absolute values yields

|psi(x)| <= mean_B |psi| + integral_B [(1-(r/R)^3)/(4pi r²)] |grad psi| dV.

To see the kernel, interchange the radial integrations: the ball average has factor 3/(4pi R³), and integration of the outer radius from r to R gives (R³-r³)/3. The remaining line integral dr becomes dV/r². This identity explains both the normalization and the integrable origin singularity.

Holder bounds the mean by (3M/(4pi R³))^(1/4). Dropping 1-(r/R)^3 only increases the second term. The L^(4/3) norm of 1/(4pi r²) on B_R is

[ (4pi)^(-1/3) integral_0^R r^(-2/3) dr ]^(3/4)
=3^(3/4)(4pi)^(-1/4) R^(1/4).

Thus choose the algebraic scale R=(M/J)^(1/4) to obtain

sup |psi| <= C M^(1/16) J^(3/16),
C=(3^(1/4)+3^(3/4))/(4pi)^(1/4),
rho_max <= C^4 M^(1/4) J^(3/4).

This R is a proof device, not a fitted physical radius; the constant is non-sharp. The derivation holds uniformly at each center x, so taking the supremum is justified without assuming a maximum is attained.

## Self-gravity cannot defeat the positive high-gradient cost

For every x split integral rho(y)/|x-y| d³y at radius a. The near part is at most 2pi rho_max a²; the far part at most M/a. Choosing a³=M/(4pi rho_max) gives

sup_x integral rho(y)/|x-y| d³y <= (3/2)(4pi rho_max)^(1/3) M^(2/3).

The factor 1/2 in self-binding energy then gives

|W| <= (3G/4)(4pi)^(1/3) M^(5/3) rho_max^(1/3)
<= K G M^(7/4) (F/lambda)^(1/4),
K=(3/16)(3^(1/4)+3^(3/4))^(4/3).

In the last step J=F/(256lambda); 256^(1/4)=4 is essential. No shape assumption enters. For conserved E=T+F+W with T>=0,

E >= F-A F^(1/4), A=K G M^(7/4) lambda^(-1/4).

The right side tends to +infinity as F tends to +infinity. More explicitly, F>= (2A)^(4/3) implies A F^(1/4)<=F/2, hence F<=2E in that region. Therefore F cannot exceed max[(2A)^(4/3),2max(E,0)]. The preceding peak bound then bounds rho_max. This prevents unbounded density concentration for any smooth solution retaining these hypotheses. It does not bound every derivative, exclude velocity shocks, or prove continued smoothness. Boundary fluxes, varying total mass and external forcing need their own energy accounting.

## Independent affine check

For Gaussian axes Ri>0, the independent random coordinates give grad ln rho components -xi/Ri². Their fourth moments imply

F=lambda M[(sum Ri^-2)^2+2sum Ri^-4].

Using 1/r=(1/sqrt(pi)) integral_0^infinity t^(-1/2) exp(-tr²)dt and the Gaussian difference distribution gives

W=-GM²/(4sqrt(pi)) integral_0^infinity ds / sqrt[(s+R1²)(s+R2²)(s+R3²)].

At rmin=min Ri, F>=3lambda M/rmin^4, while the integral is <=2/rmin. Hence U>=3lambda M/rmin^4-GM²/(2sqrt(pi)rmin), diverging positively as any axis shrinks. The stronger global argument above is not inferred from this finite-family test.

## Controls and interpretation

All eleven frozen checks pass. The non-spherical axes (1,2,3) give F=4.002314814814815 by formula and independent product quadrature, and W=-.14348599776241652. Affine lower-gradient and upper-binding margins are +1.002314814814815 and +.13860879401146162. The spherical global density and binding margins are +1.5205055257230422 and +1.7504940347732456. These synthetic margins quantify loose inequalities, not measurement significance. Reversing lambda destroys the barrier; dropping the transformation factor produces an oracle error of 255. Known sphere binding and weighted Holder-kernel quadrature agree with exact answers.

Both footing labels apply to the same proof because a0 cancels. lambda remains FITTED and undetermined; no physical strength or radius was selected. Empirical rows are NOT EVALUABLE, with zero full-row credit. The bound strengthens AZ14's survival as a constitutive proposal but does not answer the live-disc contraction requirement.

Self-audit: checked powers, dimensions, kernel normalization, self-energy factor 1/2, positivity prerequisites, the J=0 case, and the distinction between density boundedness and global regularity. This is self-review, not independent proof certification.
