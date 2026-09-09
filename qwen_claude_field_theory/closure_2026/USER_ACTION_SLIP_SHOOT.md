# No-slip initial-data compatibility probe

For the illustrative curved-branch parameters, set P=B=0 and
P'=0.02, B'=-0.02, v=0.5 at the initial point. The proper radial metric has
A=0; the isotropic spatial coordinate obeys dz=exp(-B)dx. To leading weak-
field order Phi=P and Psi=-B, so these initial values match their gradients.
No PPN gamma is inferred from this planar local construction.

The script varies v' over 201 points in [-5,5], re-solving the exact spatial
constraint for scalar flux each time. It computes P''+B'' using the coupled
action-derived equations. The sampled range is [-0.334585,-0.0300052].
No sign-changing root is found, so no subsequent matched-curvature trajectory
is claimed. This does not exclude unsampled tangencies, other intervals,
other initial data, other parameters or a differently calibrated J.

The result demonstrates that matching initial potentials is insufficient;
the illustrative branch does not automatically preserve no-slip. Next solve
the compatibility equations jointly with the desired physical MOND
calibration, rather than assigning Psi from Phi.

Commands, repository root:

`python3 qwen_claude_field_theory/closure_2026/user_action_slip_shoot.py`

Exit 0: bounded diagnostic completed, zero roots; not a theory PASS.

`python3 qwen_claude_field_theory/closure_2026/user_action_curved_branch.py`

Exit 0. Its output was compared as parsed JSON to the previously committed
result and was unchanged after adding a main guard for safe reuse.
Mathbox computation-audit scope remains bounded; full theory OPEN.
