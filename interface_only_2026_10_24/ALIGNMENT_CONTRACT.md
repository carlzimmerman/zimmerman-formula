# IO-2: positive gradient alignment instead of loss of stiffness

IO-1 softening did not retain the local phase. Change the interaction, not its
scan range: Egrad=.5 ell² integral r² F(u)|grad x-eta h'(x) grad C|² dr.
It is positive and zero in pure uniform phases. Eta is an undetermined new
coupling; no microscopic derivation is asserted. This retains the original
stiffness while favoring alignment of a phase boundary and the kinematic
transition. Material support and vacuum tail remain as in IO-1.

Face discretization: d=Dx-eta h'(Avg x) DC. Derive its full Jacobian and
Hessian, including h''' and mixed u derivatives. All mass derivatives use d²,
not the old (Dx)². Derive actual T force from independent mass variation.

Both profiles, Rj/b=1,5,8, eta1,3,10, two initial states, n128:36 minima.
Eta0 controls already exist in IO-1 and are not rerun. Same fraction and
actual-force tests; all failures retained. Any apparent pass needs refinement
and recovery before interpretation. No live density or formation claim.
