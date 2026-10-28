# Independent proof audit of CSM1 feasibility implications

Normalized claim: the corrected one-level fixed scorer uses a positive S9 mass shape q(M), a fixed positive
collapse column S(M), and U(M;L)=A[Lq(M)]^(5/4)S(M). The same U must determine the candidate-halo flag and the
corresponding core floor. The claim concerns this fixed finite scorer, including its basin and dwarf conventions.

Primary verdict: **conditional on a named input**. The algebraic reductions below are valid under the specified
positive inputs and fixed-profile semantics. Their numerical endpoints and the UFD obstruction use authenticated
finite data and cached or reconstructed scorer statistics. They do not establish the physical model.

## Dependency graph and obligations

| Implication | Leaf / status | Evidence and restriction |
|---|---|---|
| U>floor iff L>Lcrit(M) | internal algebra, passed | Lcrit=(floor/[A S])^(4/5)/q; positivity essential |
| U increases with L at fixed M | internal calculus, passed | dU/dL=(5/4)U/L>0 for L>0 |
| Target mass equality determines sole L | internal algebra plus finite S, passed conditionally | challenge fixed once at old canonical-A logM12.3 |
| Core collapse ratio scales as (Lnew/Lold)^(5/4) | internal algebra, passed | actual max-floored core ratio can be closer to1 |
| One global threshold replaces every pipeline | failed | backgrounds, interpolants and floor units differ; use direct local inequality |
| Full likelihood is continuous/monotone in L | not established | branch jump and profile redistribution must be handled |
| Existing old grid pass window is necessary for corrected model | failed as an inference | changed branch decisions alter scores at unchanged L |
| All-positive-support halo implies ENV=pureHalo | source semantics, passed | both use identical profiles/tail and same two-halo fit at all contributing nodes |
| L above max support Lcrit necessarily fails strict lens comparison | algebra + authenticated support, passed conditionally | needs no likelihood monotonicity; numerical cap is floating approximation |
| LG-off MW/UFD predictions independent of L | source semantics, passed | fixed law branch omits all halo/core/L inputs |
| LG-off MW/UFD score fails | finite cached evidence / reconstructed UFD, passed conditionally | MW cached175-cell box fails; UFD both states independently reconstructed |
| Alt UFD fails at every positive L | exhaustive two-state reduction, passed conditionally | all31 members share one LG flag; each branch's residual array independent of L; both |Z|>=2 |
| Canonical fails at every positive L | not established | its halo UFD state passes and necessary interval is nonempty |

For the lens bound, nonnegative interpolation weights were reconstructed from actual catalogue/source weights,
not inferred from the reported `frac_w_above_crossover`. The latter interpolates binary flags then thresholds
at0.5; it cannot certify absence of a small law contribution. Sparse interpolation agrees with direct np.interp
weighted sums on three test vectors to8.43e-16, and weight conservation to8.89e-16. An independent extraction
from actual F2 loaded inventory agrees exactly on counts, ranges and support nodes. If all support nodes are
halo, equality of model tables gives equality of the projected stacked predictions; identical deterministic
fits then give equal chi squared. The strict frozen `delta_halo<0` condition fails. This is a genuine necessary
tail bound for the implemented scorer; it is neither the old empirical lens window nor a sufficient pass test.

For the alt UFD theorem, the quantified domain is every L>0 in this unchanged scorer. Each of the31 members is
MW-hosted, so all use the same fixed LG mass, background and floor. Every L therefore lies in exactly one of
two states: all class members law, or all halo. The unchanged atomic8 cooled halo profile, law formula, measured
pulls, errors, row ordering and bootstrap seed have no other L argument. Both state statistics are reconstructed
from saved gN/gh/gobs rows and exactly match old/current references: alt halo Z=-2.7749963904920762, alt law
Z=+4.874405424798004. Since neither meets |Z|<2, no L can repair this fixed alt class. This is a proof by exhausting
two model states, rather than a numerical search over L. It does not apply after changing the dwarf profile,
membership, uncertainty model, basin rule or fitted parameter count.

## Boundary and regularity caveats

At exact U=floor the specified strict predicate chooses law. IEEE evaluation of an algebraically constructed
equality can land a few ulps on either side; tests use fixed relative1e-6 witnesses and report equality residuals.
Printed critical values are floating results, not interval-certified real enclosures. Outward-rounded bounds
or a direct numeric column comparison should be used for any near-boundary operational decision.

The max core column is continuous in L, but the force branch need not be. At the equality, the law prediction
is nu(gb/a0)gb while route E predicts gb+gh from a halo profile. No equation here forces gh=[nu(gb/a0)-1]gb at
every sampled radius. One cannot propagate U monotonicity into continuous or monotone observational chi squared.
Within a fixed branch, changing the column redistributes mass at fixed halo mass; outer and inner effects
need not have the same sign. Group error denominators also depend on model slopes. These are missing obligations
for any stronger continuous-L group/core exclusion.

## Strongest safe statement and next discriminator

The correction is materially different from constant-eta(L) switching. It ties an old acceptable switch target
to a much lower shared core level. The fixed alt UFD class is impossible at any L under its present two-state
construction. Canonical candidates must lie inside a nonempty necessary interval, approximately
2.4807124<L<=5.0068312, conditional on the inherited MW law failure and fixed lens scorer. Existing discrete
failures or a failed fourth challenge do not alone exclude that interval.

The predeclared discriminator was the actual same-L=2.5090648745652686 calibration/heldout grade. The initial
2.5090595510216196 implementation missed FP0's extra a0 digits and was corrected by2.12ppm using the same
algebraic target; old artifacts are retained. The actual target's column ratio is independently reproduced to
1.11e-16. Its lensing passes, while canonical groups fail at Z=+2.6219198092. This fourth result still does not
exclude every canonical L in the necessary interval. Any later all-L canonical argument must control branch
event thresholds and profile-dependent scores, rather than reuse old fixed-T grades or add another target scan.
This audit has not executed that new program.

The source P4 group rule supplies only the weak necessary inequality |mean residual|<0.09, because a pass needs
tot<=0.045 and |mean/tot|<2. A tight monotone L bound from group Z is not presently justified: both the residual
scatter term and finite-difference mass-slope term in tot change with the model, in addition to branch jumps.
The separate exact-arithmetic compact-Burkert monotonicity proof in heldout/ is valid within its fixed halo
branch; it does not make the full branch-switched likelihood monotone. No stronger group/lens exclusion is asserted.

Review provenance: independent subagent from calibration and heldout implementers, same declared inputs.
Reviewed base2c6b17d683c1a69a1c95754c255de1cc6f79800a dirty checkout; exact artifacts and source hashes are pinned
in scalar/support/review/LG/UFD manifests. Independent review does not by itself validate shared physical assumptions.
