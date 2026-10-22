# Estimates examined and not used as the uniform proof

These are analytic attempts, not executed numerical failures and not
counterexamples to the existence statement.

1. **Reuse the old full-state same-point displacement gate.** The FGF047
   bound is of the form t(Lambda M+F0)<delta. With unscaled fluid invariants,
   speed O(N) and gradient O(N^4), a fixed chart-distance bound can cost
   O(N^-5). Its positive time for each N does not prove the required N^-4
   horizon. We instead allow the O(N) fluid amplitude and control density
   along fluid trajectories; the field chart alone uses a fixed same-point
   margin and has O(1) gradients.

2. **Bound q by a rectangle in r,s.** Separate invariant amplitude bounds
   |r|,|s|=O(N) give only |q|=O(N/c), hence density bounds exp(O(N/c)).
   Those bounds do not close uniform field-source coefficients. This does
   not mean the actual density grows exponentially. The exact identity
   D_v q=-v_x instead gives an N-independent q excursion on the proved
   interval because integral ||v_x|| dt<=a kappa.

3. **Set c/N to zero after the compression rescaling.** The q,u subsystem
   has characteristic-coordinate inverse constants proportional to N/c.
   A uniform diagonal estimate that suppresses them is unjustified. We keep
   the original fixed c>0, all pressure terms, and the exact (r,s) equations.
   No pressureless equation or limit is used.

4. **Apply a generic cubic higher-gradient estimate with all component
   gradients replaced by O(N^4).** The term ||D^2 lambda|| M^3 then appears
   O(N^12), yielding an O(N^8) contribution across N^-4 time. That bound
   does not establish the sharper Htot=O(N^7) used for our force-derivative
   estimate. It could still provide a finite fixed-N restart norm, so it is
   not an obstruction to uniform existence. The actual fluid speeds have
   zero Hessian, and field speed derivatives see only O(1) field gradients;
   the block inequality (5.1) supplies the stated O(N^7) result.

5. **Infer a finite-interval response from vanishing initial field jets.**
   p=w=p_t=w_t=0 initially on the hydrostatic patch does not provide uniform
   bounds on later derivatives. No Taylor remainder estimate has been proved
   from those jets alone. Instead (6.1) and (6.4) integrate derivatives that
   are controlled on the actual constructed interval.

No breakdown-transfer attempt is claimed. The bounded task ends after the
uniform pre-breakdown interval and feedback estimates; persistence of the
old frozen-field upper endpoint is a separate, open implication.
