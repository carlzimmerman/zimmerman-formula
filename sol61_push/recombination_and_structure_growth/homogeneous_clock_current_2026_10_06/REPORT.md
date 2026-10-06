# The homogeneous clock charge: a tuned cosmological connection, not a cold mass or MOND-scale selector

This calculation follows the retained logKGB action beyond its J=0 rolling vacuum. A nonzero conserved shift charge permits an early dust-dominated GR branch. Joining it smoothly to the selected late rolling vacuum requires a particular charge combination: it is a boundary tuning, not automatic attraction of arbitrary charge data. The entire homogeneous result is independent of the acceleration-response scale A. It also predicts a limited late background dust enhancement, rather than introducing an independently conserved cold mass.

## Conventions and actual homogeneous equations

Use d=n+1, n>=3, Einstein coefficient M/2, `A_n=n(n-1)/2`, H*>0, c>0 and `eta=c/(A_n M H*^2)`. Here c is the scalar-action coefficient, not the speed of light. Set c_light=1 and use `X=q^2/2>0`, q=phidot>0. The action functions are `K=-c ln(X/Xref)`, `G=-sqrt(2)c/(nH*) X^(-1/2)`, with L3=-G Box phi and constant vacuum density rho_v. The actual current and stress conventions are recorded in ../../puzzle_32pi/dynamical_sector_2026_10_06/kinetic_braiding/REPORT.md.

Direct substitution into `J=q K_X+nHq^2 G_X`, `rho_phi=qJ-K` gives

`J=2c(H/H*-1)/q`, `a_FRW^n J=J0`,

`rho_phi=c ln(q^2/(2Xref))+2c(H/H*-1)`.

The scalar pressure is `p_phi=-c ln(q^2/(2Xref))-[2c/(nH*)] qdot/q`. These are background stress equations of the same action, not a pressureless-fluid assumption. The Friedmann equation is `A_n M H^2=rho_d+rho_v+rho_phi`, with conserved ordinary dust `rho_d=rho_d0 a_FRW^(-n)`.

On every homogeneous isotropic clock, its normalized congruence is geodesic even when q varies: a_mu=0. The added response `M lambda_n[(1-epsilon)a_mu a^mu-2W(|a|;A)]` and its first variation vanish. Consequently the entire homogeneous equations above are unchanged for every positive A, not just on the final exact vacuum. Quadratic perturbations about a geodesic homogeneous clock also depend only on the quadratic coefficient, since W=O(|a|^3/A). This statement presumes a finite positive response scale on the visited history; a zero-scale singular limit is excluded.

## Normalize to the selected late vacuum

Let q* satisfy the J=0 vacuum constraint

`q*=sqrt(2Xref) exp[(A_n M H*^2-rho_v)/(2c)]`.

It is a field normalization, not a measured matter abundance. For the expanding H>H* branch require J0>0. Define dimensionless quantities

`h=H/H*>1`, `z=rho_d/(2c)=D a_FRW^(-n)`, `D=rho_d0/(2c)>0`, `j=J0 q*/(2c)>0`.

Current conservation then gives `q/q*=a_FRW^n(h-1)/j`. Subtract the selected vacuum Friedmann equation to obtain the exact algebraic history

`f(h)=g(z)+ln(D/j)`,

`f(h)=(h^2-1)/(2eta)-(h-1)-ln(h-1)`, `g(z)=z-ln z`.

No MOND scale appears. The scale-factor normalization cancels in j/D, as required: both J0 and rho_d0 transform with the same a_FRW^n normalization.

## Two folds and the unique smooth GR-to-vacuum charge

For h>1,

`f'(h)=h[1/eta-1/(h-1)]`.

Thus f has a unique minimum at `h_c=1+eta`, with `f_min=1-eta/2-ln eta`; f tends to infinity at both endpoints h->1+ and h->infinity. Similarly g has unique minimum1 at z=1 and tends to infinity as z->0 or infinity.

An early GR dust history needs the upper h>h_c root at z>>1. A late selected H* history needs the lower 1<h<h_c root at z<<1. Any continuous transition between them must pass through the f minimum. An all-positive-z history can make that passage without a missing-real-root interval only if the minima coincide:

`1+ln(D/j)=1-eta/2-ln eta`, hence

`j_crit=D eta exp(eta/2)`, equivalently `J0 q*=rho_d0 eta exp(eta/2)`.

If the right-side minimum is lower, there is an interval with no real expanding H>H* root. If it is higher, the two roots remain disconnected; staying on the early upper root leads to growing H at late z->0, while staying on the late lower root has no early GR limit. A continuous branch cannot switch between distinct roots without violating the algebraic constraint. This proves necessity within the dust-only, positive-charge, globally continuous H>H* history class.

At the tuned equality there is a smooth crossing. Write `y=h-1` and `L(x)=x-ln x-1`. The equation becomes exactly

`L(y/eta)+(eta/2)(y/eta-1)^2=L(z)`.

Both sides have a nondegenerate quadratic zero at1. Factoring each side as `(x-1)^2` times a positive analytic function and taking the signed square root provides a local analytic monotone branch across the fold. Its slope is `dh/dz=eta/sqrt(1+eta)` at z=1. Upper roots for z>1 and lower roots for z<1 connect this branch for all z>0. This is a homogeneous background solution argument; finite-gradient health and inhomogeneous matter perturbations remain to be checked on that history.

Set q from its conserved-current relation along this smooth H(a_FRW), and integrate `dln a_FRW/dt=H`. For every finite positive scale factor, H and q are finite and positive, including the fold. Current conservation gives `qdot/q=nH+Hdot/(H-H*)` and directly implies `rhodot_phi+nH(rho_phi+p_phi)=0` with the actual pressure above. Conserved dust plus the differentiated Friedmann equation therefore gives the spatial Einstein/Raychaudhuri equation. This verifies a full homogeneous on-shell history, rather than only an algebraic Friedmann ansatz. The Big Bang limit a_FRW->0 and inhomogeneous equations are not made regular by this argument.

The current is conserved, so arbitrary J0 does not relax to j_crit. Calling the equality a regularity-selected trajectory specifies boundary data; it is not a dynamical mechanism that produces that charge. Vacuum rescaling changes q* and J0 inversely and leaves the physical combination J0 q* unchanged.

## Predictions and cold-sector limit

At z>>1 the upper branch has `h^2=2eta z[1+o(1)]`, giving `A_n M H^2=rho_d[1+o(1)]`. The clock's correction is subleading relative to that early dust density; its current is not a second independently conserved dust source in these equations.

At z<<1 the lower branch has `h-1=eta exp(eta/2) z[1+o(1)]`, and q/q* tends to1. Hence

`A_n M(H^2-H*^2)=exp(eta/2) rho_d[1+o(1)]`.

The late background dust coefficient is enhanced by exp(eta/2). On the inherited four-dimensional rolling-vacuum health interval0<eta<1 this lies between1 andsqrt(e), not an arbitrary dark-to-baryon abundance. This is an Einstein-background coefficient, not a universal laboratory G_N measurement or a CMB fit. The early matter perturbations, radiation era, atomic recombination and pressure/stress transfer have not been solved here. Relabeling this charge as the required pre-recombination cold mass would omit those obligations.

The fold occurs at `rho_d=2c`, `H=(1+eta)H*`, and has `dH/dln a_FRW=-n eta H*/sqrt(1+eta)`. Those are predictions of the tuned background route beyond an a0 relation. They depend on the action parameter eta, but not A. A separate response scale or nonlinear consistency principle is still required for A/H* or32pi.

## Scope, dimensions and evidence

This theorem treats spatially flat FRW, one conserved ordinary dust background, positive q and J0, and the retained shift-symmetric logKGB action. Radiation or nonconstant vacuum modifies the right-side fold location; another scalar potential or energy exchange changes the current. J0=0 gives the separate H=H* branch and does not supply an early GR dust expansion. Negative-charge H<H* histories are outside the theorem.

M has mass dimension n-1, c and all densities n+1, and H* dimension1. One can choose phi dimension(n-1)/2, so q has dimension(n+1)/2 and J dimension(n+1)/2; J0 q* has density dimension. The relation is classical and contains no hbar. Computation checks direct K/G substitution, fold algebra, charge normalization, late/early limits and bounded monotone background roots. Universal statements follow from the written calculus and signed-square-root proof, not finite samples.

The result sharpens the no-selection statement: even a smooth early-dust to late-vacuum homogeneous connection can tune a conserved clock charge while leaving every positive A untouched. It is neither a32pi derivation nor a complete cold-sector cosmology.
