# FGF050: preserved unsuccessful estimates

These are failures of proposed estimates. None refutes compression for the
actual fixed-coefficient, exact C1,1 initial family.

1. **Equal density sources imply cancellation.** The exact source contribution
   is -(C/(2 tau b))(I_+-I_-), with I_epsilon=integral j_epsilon n_x(s,X_epsilon).
   Both transported arguments and terminal-label Jacobians differ. Same-point
   cancellation deletes actual transport and cannot estimate this difference.

2. **Continuity removes density gradients for free.** On a nonresonant segment,
   I=-[jn/r]-integral jn D_v r/r^2. In the actual isothermal equations,
   D_v r=-g-c^2 n_x/n-D_v lambda. Pressure therefore leaves
   integral j c^2 n_x/r^2. Its fast-core gain is only O(V^-2)=O(N^-2).
   The proposed bound omitting it is algebraically false. Dividing by
   1-c^2/r^2 introduces fluid-acoustic/field coincidences and variable weights.

3. **Positive initial velocity supplies global speed separation.** Initially
   v=0 at both compact joins and v>b0 at the center for sufficiently large N.
   The lambda_-=+b family has v-b=0 on both packet halves already at t=0.
   The lambda_+=-b family has only an O(1) edge gap initially, with no supplied
   full-time sign or O(V) separation. A gate applying only to the fast core
   leaves the edges/exterior/possible later resonance regions uncontrolled.

4. **A cutoff deletes resonance.** The exact global identity (11) retains
   L=integral j(1-theta)n_x and a transition term
   integral jn D_lambda theta/r. Expanding D_lambda theta exposes pressure and
   compression again. No estimate for the number of transitions or their
   signed total follows from the partition. Segmentwise integration requires
   every boundary trace instead of this transition term.

5. **Mass controls endpoint density and its gradient.** Exact continuity gives
   swept mass integral n|v-lambda| along each fixed-sign segment. A fixed-mass
   smooth positive density bump has unbounded point value and gradient as its
   width tends to zero. This is a functional-inequality obstruction only:
   that bump is not claimed to solve the coupled system or match its initial
   data. Taking sup_x separately at each t further defeats conversion of a
   single-path mass estimate into the target time integral of spatial suprema.
   Repeated crossings require multiplicity control, which is not established.

6. **Opposite paths bound the derivative through a mass wedge.** Reynolds
   transport gives integral(r_+ n_+-r_- n_-)=initial wedge mass. The needed
   integral is the difference of j n_x, not the flux difference. A derivative
   in terminal x reintroduces endpoint/relative-speed derivatives. Positivity
   of mass supplies no bound for those derivatives.

7. **Large N offsets an unbounded remainder.** Under j<=jmax and b>=bmin,
   A_P<=[2 jmax c^2/(delta^2 V^2)] integral(T_N-s) sup|n_x(s)|ds.
   Thus one sufficient bound is that latter integral=o(omega V^2)=o(N^6).
   It is not supplied. Even a polynomially small factor cannot control an
   unspecified trace, or the exponential-in-N amplitude bound obtainable
   from crude fluid invariant rectangles. This does not assert exponential
   growth of the actual density. A compact state alone also fails to bound
   j=exp(-integral lambda_x), which is another full-time derivative gate.

8. **The fast endpoint has a helpful universal sign.** Combining endpoint
   pieces gives density contribution -C n/[tau(v^2-b^2)] when both paths are
   separated. It is adverse in |v|>b and favorable in |v|<b. Initial and
   transport terms prevent inference of the total gradient sign. There is no
   valid universal favorable-density-source shortcut.

9. **Short-time control or small energy closes the full-time budget.**
   FGF048's kappa/omega bound cannot be relabeled B_*/omega. The initial
   O(N^-1) energy coexists with O(N^4) velocity gradient and O(N^7) gradient
   Lipschitz seminorm. Both field fluxes and moving-cone energy terms remain.
   No energy estimate of the missing density/field trace follows.

Stop after this bounded derivation. The useful next check is a genuinely new
signed estimate of the low-speed/transition trace and pressure remainder,
with full-time chart and Jacobian gates. There were no mathematical executable
computations, numerical samples, imported mechanisms, or repeated sweeps.
