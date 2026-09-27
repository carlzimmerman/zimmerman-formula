# Independent read-only audit of CA5-GNC-R and its fixed-data barrier

Reviewed `../vacuum/ACTION.md` and `../vacuum/BARRIER_PROOF.md` after the
dual derivation. Accepted under the exact smooth compact fixed-data
hypotheses stated there. No change was made to either source.

The action replacement has the correct local lapse density
`t K+Wexc/t+V0 F(t)` and local Z source
`K+Wexc/t^2-V0 F'(t)`. The h-volume projector therefore acts on the latter;
the displayed mean stress and clock terms have the required sign. With
`F'(1)=F''(1)=0`, both the vacuum Z source and its linear susceptibility
vanish, while the physical homogeneous stress is still `-V0 g`.
Inversion symmetry applies to F, not to the full action or mean constraint.

The maximum-principle multiplier argument repairs a real gap that would
arise from assuming an energy bound automatically bounds a reciprocal
barrier derivative. At `tmax>=1`, the maximum has
`div_h(N Dt)<=0`, `F'(tmax)>=0` and `epsilon/tmax^2<=epsilon`, yielding
`lambda<=2mB+Nmax||epsilon||infinity`. At a minimum below d, both potential
derivatives are negative and `div_h(N Dt)>=0`. Dropping the nonpositive
excitation derivative gives
`Nmin V0[-F'(d)]<=lambda+2mB`, contradicted by sufficiently small d.
These signs are correct. The displayed explicit lower bound is weaker
than the resulting sharp inequality and remains valid when C=0.

For fixed d the quadratic extensions are convex C2 with globally
Lipschitz first derivatives: F'' is bounded on `[d,infinity)` and is
constant on the extension. H2 regularity in dimension three followed by
elliptic bootstrapping therefore permits the extrema argument. Below one,
`F'''=24(t-1)/t^5<0`; Taylor's integral remainder for t<d gives `F>=F_d`.
The same sign applies to `1/t`. Thus the regularized minimizer, once shown
to stay above d, is a minimizer of the original extended-energy functional.
Gradient strict convexity on mean-zero differences supplies uniqueness.

The action's general-vacuum infrared condition and its new all-mode sign
bound are consistent with the previously independently derived ADM scalar
block. They concern the actual empty de Sitter background, not arbitrary
occupied or inhomogeneous states. The constant-momentum limit, finite
compact-leaf spectrum, and lack of uniform zero-mode coercivity are
explicitly distinguished in the source.

Acceptance does not extend to continuum simultaneous U/Z existence,
an evolving uniform lower bound, full constraint rank or global nonlinear
gravity. The separate finite-spectral joint theorem in `DUAL_AUXILIARY.md`
must retain its finite-resolution scope. No unresolved algebraic or sign
defect was found in the reviewed fixed-data proof.
