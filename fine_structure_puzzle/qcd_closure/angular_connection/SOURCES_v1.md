# Sources and input receipt

The new proof in RAW_DERIVATION_v1.md is internal. It invokes no external
spectral, index, heat-kernel, or determinant theorem. The DN variational
identity is derived by completing the form around the regular ODE solution;
the Riccati identity and contraction are proved directly. This avoids
transferring an external lemma with mismatched boundary or neutral domains.

Repository inputs read and used:

1. `qcd_closure/CONTRACT.md`: FSP-005 target, immutability and route scope.
2. `qcd_completion/higher_angular/REPORT.md`: current fixed-J statement and
   unresolved uniform connection obligation.
3. `qcd_completion/higher_angular/RAW_DERIVATION_v1.md`: exact far Pauli
   angular decomposition, channel counts and relative wall ranks.
4. `qcd_completion/higher_angular/UNIFORM_EXTERIOR_v1.md`: already-controlled
   exterior J~sqrt(R) band and its remaining complete-connection limit.
5. `qcd_completion/higher_angular/inputs_v1/j1_operator.json`: actual frozen
   Cartesian Hessian for the exact 120-component crosscheck.
6. `qcd_completion/angular_modes/REPORT.md`: background conventions, angular
   covariant derivative, and actual relative wall derivation.
7. `qcd_completion/angular_modes/transverse_followup/DERIVATION.md`: actual
   Cartesian tensor basis, sign convention and wall, not copied scalar data.
8. `qcd_completion/angular_modes/transverse_followup/REMAINDER_CONTROL.md`:
   earlier fixed-J charged-neutral tail warning and actual wall Schur setup.
9. `qcd_completion/reviews/kernel_rank/RAW_DERIVATION_v1.md`: earlier kernel
   theorem and its domain restrictions. Read for context, but its external
   index theorem is not a dependency of the new J>=6 bounds.

Input hashes are in INPUTS_v1.json. Exact-run code, contract and hand proof
hashes are additionally pinned before and after execution by the validated
v2 run manifest. No source novelty claim or physical alpha input was used.
