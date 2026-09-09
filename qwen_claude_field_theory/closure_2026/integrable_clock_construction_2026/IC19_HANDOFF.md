# Current handoff: normalized cosmology works; design the scalar energy next

Base: `9b7d7b3db109f14a3f17d1e71efa384bd16f0690`.
**Full theory OPEN. IC19 fails the required healthy-scalar condition.**
This is progress: a distinct explicit action, spatial variation, constraint
preservation and a constructive compatibility condition were added and run.

[The action and derivation](IC19_NORMALIZED_SPATIAL.md) make three linked
changes: impose Carl's a0–Lambda normalization, use a lapse-independent
momentum switch, and remove old momentum-curvature/gradient operators that
were tuned for an obsolete witness. The pin still removes the mixed matter
response without adding an auxiliary propagating field. No other model's
MOND, PPN or matter PASS is imported.

## What is genuinely stronger

1. A uniform analytic bound `r²>=Lambda/(3h0²)>1` keeps the normalized,
   expanding homogeneous pole-clock/radiation/dust branch on eta=1 throughout
   its regular evolution. This is stronger than finding no transition roots
   on a grid. It is not a CMB fit or proof of past completeness.
2. The full pinned spatial Hamiltonian is explicit. The lapse secondary and
   its actual operator M(k), including its gradient coefficient, are varied.
   A positively curved, expanding homogeneous witness solves the constraints,
   and preservation determines a finite multiplier. Its k=0 and all k!=0
   auxiliary modes are regular by the sign criterion M0<0,B>0.
3. The physical scalar energy is then reduced separately. At S=.1,r=.82 its
   UV momentum coefficient is approximately -13.4036. Constraint regularity
   did not imply positive energy. The note proves why a ghost persists near
   the smooth switch's upper boundary in this restricted fixed-Einstein-TT,
   pure-pressure interpolation class. This does not refute the exponential
   kernel, the vacuum relation, or every clock theory.

## Next construction, not another switch scan

Do not repeat the aligned matter calculation or adjust the same switch shape
as though rank regularity could cure the negative scalar energy. Retain the
normalized clock and static exponential primitive. Replace the trace-momentum
interpolation with a joint kinetic/curvature construction.

For a proposed local Hamiltonian H(S,q,R), trace-free kinetic coefficient T,
and positive lapse-gradient coefficient B, the derived necessary UV
compatibility is

    (H_qq+T/3) H_RR-H_qR²=0.

It prevents a leading k^4 scalar dispersion term after enforcing energy
positivity in the stated principal reduction. The exact local Hessian family
in the note solves this equation, but NOT the other requirements. First
construct a global action that also has the correct tensor cone, positive
scalar k² coefficient, static zero jets and a regular lapse constraint. Then
test the existing expanding curved witness before spending effort on galaxy
fits. A momentum-dependent curvature coefficient without the corresponding
completion has its own negative high-frequency determinant; that shortcut
was explicitly checked and must not be called a solution.

Still required from the same successful revision: independent Phi/Psi and
matched MOND galaxy, all PPN coefficients, endpoint and interaction-scale
control, full spatial evolution, and empirical galaxy/cluster/cosmology tests.
The scale relation is imposed, not derived. No new empirical prediction or
complete theory is announced.

See [the run index](ic19_run_001/run_index.json) for exact commands, owned
files, actual test exits and provenance. Mathbox's audit distinguishes the
exact structural identities, finite witnesses and uncomputed obligations.
Review was a scoped self-review, not independent full-theory certification.
