# Independent review of the positive spectral route

**Primary verdict:** the ordinary-Stieltjes divergence, generalized-order threshold/moment, order-3 admissible family, finite-window freedom and fixed-linear-Yukawa source obstruction are correct under the report's explicit assumptions. No substantive mathematical correction is required. The report correctly stops before applying momentum-space positivity to an acceleration constitutive law. That missing physical map is essential, rather than a minor qualification.

Reviewed read-only: `../analytic_uv/REPORT.md`, `checks.py`, primary-source text copies and `runs/positive_spectral/manifest.json`. Actual hashes and independently evaluated controls are in `analytic_review_inputs.json`. The positive manifest validates against current files; that fact supplies provenance, not proof. No peer script was run or peer output overwritten.

## 1. Divergence and generalized moment reconstructed

Convergence of `integral rho(dt)/(y+t)^alpha` at any positive `y` makes the measure finite on every bounded interval. A nonzero positive measure has some bounded interval `[0,L]` of positive mass `w`, hence `e(y)>=w/(y+L)^alpha`. The tail of `integral y e(y)dy` diverges for `alpha<=2`, including logarithmically at two. This proof does not assume an absolutely continuous measure, a nonzero mass at zero, or finite total mass. A nonnegative constant term also diverges.

For `alpha>2`, Tonelli applies without requiring a priori finiteness. For each `t>0`, substituting `y=t u` gives

`integral_0^infinity y/(y+t)^alpha dy = t^(2-alpha) Beta(2,alpha-2) = t^(2-alpha)/[(alpha-1)(alpha-2)]`.

At `t=0` the inner integral is infinite. Consequently the stated negative moment is necessary and sufficient, interpreted in the extended positive sense. This agrees with the positive generalized Stieltjes class in the retained Karp–Prilepkina definitions (1)–(2); it does not identify the family's minimal Stieltjes order.

The consequence is **incompatibility with the chosen finite primitive**, not a theorem that all positive spectral quantum theories have divergent physical vacuum energy. A vacuum subtraction and its finite renormalization are different premises.

## 2. Order-3 family and full spatial action dictionary

For `rho_s(dt)=B t^(3/2) 1_[0,s]dt`, substituting `t=y u` produces `B y^-1/2 F(s/y)`. The beta integral gives `F(infinity)=3pi/8`, so `B=8A/(3pi)` fixes the deep coefficient. Expanding the denominator at large `y` gives the UV coefficient `(2B/5)s^(5/2)`. Independently integrating the order-3 moment yields `C_s=(B/2) integral_0^s t^(1/2)dt=(B/3)s^(3/2)`.

For all positive `y`, differentiation under this finite positive measure proves the complete-monotonicity formula. Positivity of the spectral measure alone does not prove the NR action convexity; the separate source derivative is needed. Directly,

`D=1+(B/sqrt(s))sqrt(v)F(v)-(2B/sqrt(s))v³/(1+v)³ >=1-2B/sqrt(s)`.

Thus the claimed bound is valid, though sufficient rather than necessary. Convex mixtures preserve it because `D` is affine in the response and its derivative.

I reconstructed source matching directly from `W=|p|²+|ph|²-a0² M(|p-ph|²/a0²)`, rather than assuming its reported dictionary. With `m=M'`, the two fluxes are `p-m(p-ph)` and `ph+m(p-ph)`. The unsourced auxiliary flux vanishes in spherical isolated matching, giving `ph=-m p/(1-m)`. The physical Newton flux becomes `b=p(1-2m)/(1-m)`. Setting the physical field `p=(1+e)b` therefore gives `m=e/(1+2e)` and `x*=y(1+2e)` as stated.

In orthonormal common/difference variables, the Hessian eigenvalues are three common values `2`, two transverse difference values `2-4m=2/(1+2e)`, and radial difference value `2-4(m+x* dm/dx*)=2/D`. Hence all six are positive away from zero difference field for this family. They degenerate in the deep endpoint; this is not uniform ellipticity there and says nothing about relativistic kinetic ghosts.

The primitive relation also follows directly: `dz=2y(1+2e)D dy`, so

`m dz-2ye dy=4ye(e+ye')dy=d(2y²e²)`.

The deep and UV powers make both endpoint terms zero. This establishes the same-static-action primitive coefficient under `M(infinity)=0`. Converting that coefficient to a cosmological vacuum retains the report's separately specified identical-metric and `f` assumptions from the BIMOND action; it is not deduced from spatial convexity alone. The retained Milgrom source contains the NR action/source equations (1)–(2) and its vacuum term (24). The additive normalization remains an independent premise.

## 3. Window freedom and independent numerical controls

For `0<y<=Y`, monotonicity of `F` gives `F(s0/y)>=F(s0/Y)>0` and `F(S/y)<=F(infinity)`. This proves the stated uniform relative-excess bound for every `S>=s0`. The shift in the moment is linear in mixture weight; solving for `S` realizes every positive desired shift while retaining all sufficient admissibility inequalities. The theorem requires a positive finite tolerance: exact equality on an open interval would contradict real analyticity and is not claimed.

Using a separate trigonometric **integral** `F(v)=integral_0^atan(sqrt(v)) 2sin(theta)^4 dtheta` at 70 decimal digits, I obtain `S=23202.7880515063`, `C_base=18.1082957473445`, relative bound `6.28108720873999e-6`, and global `D` floor `0.575586818421612`. These reproduce the reported values without using its incomplete-beta implementation. The retained extreme-UV cancellation failure is appropriately historical.

## 4. Physical pole dictionary: what is and is not established

For a canonical scalar with static positive operator `-Laplace+mu²` and universal linear source, eliminating the field gives a positive simple pole in **momentum squared**. The point-source potential is proportional to `-exp(-mu r)/r`; taking its radial derivative gives relative extra acceleration `alpha(1+mu r)exp(-mu r)`, with `alpha=g²/(4piG)` in the report's normalization. This is not a simple-pole function of the local acceleration variable.

The source-mass obstruction is exact. At fixed `r`, varying `M` changes `y=GM/(a0 r²)` through all positive values but leaves the Yukawa relative response unchanged. A universal function `e(y)` valid for all these sources must therefore be constant. For a fixed mass, each positive massive term has derivative `-mu² r exp(-mu r)` with respect to `r`, and hence increases with `y`; this also has the opposite monotonicity to MOND excess. A positive superposition preserves that inequality whenever it is finite. A finite massless contribution adds only a constant. The two-mass numerical control (`r=1,2` at the same dimensionless `y`) is consistent with this proof but not its substitute.

The remaining physical implication is substantial: a nonlinear microscopic action must derive how a background acceleration controls its fluctuation spectra, how that background-dependent data constrains the whole constitutive response, and how the same action fixes the vacuum moment and additive height. Fixed-background propagator positivity does not supply those functions. Generalized order-3 kernels in `y` are not automatically three healthy simple-pole particles. Pressure/source backreaction, nonlinear screening, field-dependent couplings, additional constraints and a relativistic completion can change the linear-Yukawa hypotheses; they require new derivations.

**Accepted scope:** a precise mathematical non-selector and a valid obstruction to the specified universal fixed-linear-positive-pole construction. Neither a healthy microscopic MOND model nor selection of 32pi has been proved.
