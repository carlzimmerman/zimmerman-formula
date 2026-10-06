# Independent homogeneous-current review

Accepted within the stated flat-FRW, conserved-dust, positive-q and positive-charge class. I reconstructed the action current, pressure, Friedmann normalization and fold connection rather than adopting the report verdict. No mathematical correction is required in the inspected revision. This accepts a tuned homogeneous history, not its inhomogeneous stability, a cold-matter transfer model, an attractor, or a response-scale selector.

## Inspected evidence

Observed repository HEAD: `6988a2ecbab63393c26a160f81ee15a4391d6a0a`. Actual SHA-256 pins:

- `REPORT.md`: `c0e0ed1b377bc1470c193a9c54796676e47e2be5403821c64a38e306c6a527e8`.
- `checks.py`: `ee220cd941d4d5e14fe7dd6bd33f539d3ded667ca08bc90735563ff00c44be2e`.
- Earlier raw action/current dictionary, `../../puzzle_32pi/dynamical_sector_2026_10_06/kinetic_braiding/REPORT.md`: `f60cc5a4940fbd311e4cab34f1be7e60db186b51e3344cb92048c394e8596a1b`.

This is a mathematical peer review. I read the script without executing it or modifying execution inputs; runner validation is separately owned by the author. Finite sample counts do not supply the global branch proof.

## Raw action and stress reconstruction

For `K=-c ln(X/Xref)`, `G=-sqrt(2)c/(nH*) X^(-1/2)` and `-G Box(phi)`, differentiation gives `K_X=-c/X` and `G_X=sqrt(2)c/(2nH*) X^(-3/2)`. With `X=q^2/2`, these imply

`J=qK_X+nHq^2G_X=2c(h-1)/q`,

`rho_phi=qJ-K=2c(h-1)+c ln(q^2/(2Xref))`,

`p_phi=K-2XG_X qdot=-c ln(q^2/(2Xref))-2c qdot/(nH*q)`.

The pressure contains the braiding derivative term and must not be replaced by dust pressure. For `A_n=n(n-1)/2`, subtraction of the actual vacuum equation from `A_n M H^2=rho_d+rho_v+rho_phi` gives

`(h^2-1)/(2eta)=z+(h-1)+ln(q/q*)`.

Using the conserved current yields `q/q*=D(h-1)/(jz)`, hence precisely the reported `f(h)=z-ln(z)+ln(D/j)`. Both the `n` in the current and the `A_n` in Friedmann are required. The dimensions stated in the report agree: `J0 q*`, `c` and `rho_d0` all have density dimension `n+1`; `eta,D,j,h,z` are dimensionless.

## Necessity, uniqueness and smoothness of the connection

Let `y=h-1>0`. Direct differentiation gives `f'(h)=h(1/eta-1/y)`. There is only one minimum, at `y=eta`, and `f''(1+eta)=(1+eta)/eta^2>0`. The source function `g(z)=z-ln(z)` has its unique minimum at `z=1`, with `g''(1)=1`. Thus a continuous switch from the early upper root to the late lower root must touch `y=eta`. If the source minimum lies above the field minimum the roots never touch; if below, a missing-real-root interval prevents an all-positive-z history. Equality gives exactly `j=D eta exp(eta/2)`.

At this equality, writing `x=y/eta` gives `L(x)+(eta/2)(x-1)^2=L(z)` with `L(t)=t-ln(t)-1`. The left side decreases strictly on `(0,1)` and increases strictly on `(1,infinity)`; the same is true for the right side. Selecting `x<1` for `z<1` and `x>1` for `z>1` therefore defines a unique globally monotone connection. Locally both sides factor into their squared distance from 1 times a positive analytic function. The signed square root is analytic with nonzero derivative, so the implicit-function theorem gives the smooth crossing and positive slope `dh/dz=eta/sqrt(1+eta)`. The opposite local slope connects the opposite asymptotic assignments; staying on one algebraic root across the fold gives a cusp and does not satisfy the requested smooth GR-to-vacuum connection.

This fold is a degeneracy of the implicit background equation. Smooth passage at tuned data does not certify regular perturbative kinetic coefficients there. The report correctly retains the finite-gradient and inhomogeneous-health obligation.

## On-shell completion, limits and vacuum map

Current conservation gives `qdot/q=nH+Hdot/(H-H*)`. Substitution into the independently reconstructed stress yields exactly `rhodot_phi+nH(rho_phi+p_phi)=0`. Together with conserved dust and Friedmann, this yields the general-n spatial equation

`(n-1) M Hdot=-(rho_d+rho_phi+p_phi)`.

At the fold `H-H*=eta H*` is nonzero, so the current equation introduces no singular division there. The derived smooth history, positive q and `d ln(a)/dt=H` satisfy both homogeneous Einstein equations and the scalar equation at every finite positive scale factor. This is a background existence result; neither the Big Bang endpoint nor convergence of a perturbed spacetime solution follows.

The upper root obeys `h^2~2eta z` at large z. The lower root obeys `y~eta exp(eta/2) z` at small z, fixing `q/q*->1` and the late enhancement `exp(eta/2)`. The reported derivative at the fold follows from `dz/d ln(a)=-nz`. The range `1<exp(eta/2)<sqrt(e)` invokes the inherited four-dimensional vacuum health interval, not a health result for all n or for the whole dust history.

Under a constant vacuum shift `Delta rho_v`, `q` and `q*` rescale by `exp[-Delta rho_v/(2c)]`, while `J` and `J0` rescale inversely. Thus `J0 q*` and the critical condition are invariant. Conservation forbids relaxation of arbitrary charge into that condition. This is genuinely a tuned boundary-charge connection, not merely a freely assigned extra dust density.

Finally, the normalized homogeneous clock has vanishing acceleration even for variable q. For finite positive A, the retained acceleration operator and its first variation vanish there, while `W=O(|a_mu|^3/A)` contributes no quadratic term. Consequently changing A preserves these entire homogeneous histories and their quadratic equations. The calculation does not select A/H*, 32pi, an operational laboratory Newton constant, or a pre-recombination cold abundance. Radiation, negative-charge histories and nonminimal matter exchange remain outside the reviewed theorem.
