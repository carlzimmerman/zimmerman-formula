# Failed estimates and deferred continuation, FGF049

These are failures or limits of estimates, not counterexamples to coupled
compression. All physical coefficients and the initial C1,1 joins are fixed.

1. **Replacing the short kappa by B_*.** FGF048 requires a*kappa<=1/2 and
   strict blockwise gradient improvements. Its fluid comparison has an A_f^2
   contribution: on A_f<=a N^4 the integrated contribution at t=B_* N^-4
   is a^2 B_* N^4. The small-kappa inequality does not imply the corresponding
   B_* inequality. The accepted Htot<=C_H N^7 and derivative-feedback bounds
   are themselves conditional on that shorter first-gradient bootstrap.
   Reusing them up to the proposed upper time would be circular.

2. **Rectangular Riemann bounds.** Under the new force-impulse hypothesis,
   |q|<=[(1+Gamma)v0 N+c Q0]/c, so n can be as large as
   nref exp(Q0+(1+Gamma)v0 N/c). Combining this with n_x=n q_x and the
   unclosed q_x equation produces exponential-in-N source constants in
   (5.2),(5.6). Small time O(N^-4) alone does not offset them. These are
   conservative bounds, not evidence that actual density grows exponentially.

3. **Static source sign.** B_x=Cn+tau p_t and
   B_g g_x=Cn+tau p_t-B_chi k. Positivity of Cn does not control tau p_t or
   the scale term. Setting p_t=0 deletes actual feedback. No g_x>=0 theorem
   follows from the initial hydrostatic source.

4. **Equal-source cancellation.** The -Cn_x/tau sources agree at the same
   spacetime point, but their characteristic integrals follow speeds -b and
   +b. Subtracting them without transporting their arguments is invalid.
   Formula (5.4) also retains -2Hcal_chi k. An estimate of the two-path source
   difference remains untried in a form capable of reaching B_*/omega;
   this is the explicit resumption condition, not an exhausted route.

5. **An average as a pointwise bound.** integral K_N<=eta omega does not
   imply K_N(t)<=eta omega/T_N. Peaks are allowed. The successful proof uses
   the future-tail correction (4.4), not this false implication. This check
   prevents an erroneous Riccati proof while retaining the weaker integral
   hypothesis.

6. **Small initial energy.** Its O(N^-1) kinetic excess coexists with
   ||v_x(0)||=d_f v0 N^4/L and Lip(v_x(0))=8v0 N^7/L^2.
   Finite/small local energy therefore cannot supply a uniform gradient norm.
   Moreover shrinking-cone energy has both flux and Reynolds terms; treating
   it as a conserved positive norm would omit actual exchanges/boundaries.

7. **Initial jets or extra derivatives.** Even though p=w=0 initially,
   the density derivative immediately has terms -rho v_xx of order N^7.
   Time jets do not bound its integrated feedback over a full compression
   interval. Differentiating g_tt=(B_xx-Cn_x)/tau again to estimate g_x
   introduces B_xxx and n_xx as distributions and an unproved extra derivative
   gate. No C2 initial velocity was silently substituted.

8. **Inherited endpoint classification.** The fixed-force FGF046 theorem
   controls amplitude by a prescribed g0. The coupled chart may instead lose
   g/B_g margin or scale-state control. Section 6 derives a sufficient coupled
   restart gate but does not prove its hypotheses up to the actual maximal
   endpoint. A budget violation is neither a gradient singularity nor a
   stable-solution counterexample.

All eight checks were analytic. There are zero numerical samples and zero
mathematical executable computations. The next discriminating work is the
signed/two-characteristic density feedback estimate, with domain and chart
bounds tracked on the same interval. No extension of this bounded run is
claimed; the original unconditional research route remains open.
