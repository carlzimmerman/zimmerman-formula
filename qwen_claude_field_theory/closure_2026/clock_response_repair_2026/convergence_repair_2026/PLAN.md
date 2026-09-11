# Ordered fixed-action gates

Base aafe58d20. User explicitly requires, in order:

1. Repair the 129->257 evolution constraint-refinement failure. No downstream
   late-time physics is trusted while this fails. Preserve the unchanged test;
   use manufactured controls, time refinement and projection consistency too.
2. Only after gate 1: derive how FLRW background expansion enters the actual
   action's constitutive argument. Do not choose a Hubble/peculiar prescription
   phenomenologically and do not equate a scalar invariant with a MOND kernel
   unless its weak-field reduction establishes that identification.
3. Only afterward: compute the same action's dust transport into galaxies and
   clusters. Compare with the user's stated retention targets without retuning.

No reconstruction or adjustment of P, W, V, background functions, gamma, a0,
or initial source parameters is authorized here. No substitute memory study.

The memory-transfer process was interrupted at the user's change of priority
(exit 130, during a symbolic factorization). Its uncommitted draft is not a
result and is outside this gate-repair change set.

Debugging record: original failure reproduced; changing projection tolerance
alone did not remove it; r-squared parity fixed a manufactured center cusp but
did not pass evolution; sharing center jets reduced the mismatch but did not
pass; using matching fourth-order lapse derivatives passed momentum refinement
but exposed a Hamiltonian error floor. The latest test uses affine radial
perturbation variables so adaptive errors are not scaled by the order-one
background. All thresholds and action coefficients remain unchanged.
