# Zero-flux curved branch construction

Using the same calibrated J and parameters as USER_ACTION_CALIBRATED_BRANCH,
set the conserved scalar flux to zero and solve the spatial constraint for
v' instead. Keep the initially matched logarithmic metric gradients and
v=s(0.02). Both signs of v' are allowed by this initial constraint:

| xi | initial v' | maximum constraint residual | maximum absolute P+B |
|---|---|---|---|
| 0.2 | -0.3596115804 | 4.46e-13 | 5.50399e-6 |
| 0.2 | +0.3596115804 | 6.66e-13 | 5.53267e-6 |
| 0.1 | -0.7192233933 | 4.47e-13 | 5.50722e-6 |
| 0.1 | +0.7192233933 | 1.44e-12 | 5.53216e-6 |

All runs reach x=0.02 at rtol=1e-10, atol=1e-12. This constructs compatible
zero-flux initial data rather than assigning the flux after solving. The
metric potentials are still independently evolved and no-slip is not
maintained for these illustrative vacuum data. Zero flux is therefore not
the sole missing condition. No galactic source boundary problem, PPN gamma,
global no-go, or exact general-source MOND result follows from these runs.

Next: solve the initial no-slip curvature condition jointly with the spatial
constraint and physical source/boundary conditions, rather than just the
flux condition. The xi*v' scale remains comparable between the two tested
xi values; these data are not a fixed-data xi-to-zero convergence sequence.

Commands from repo root:
`python3 qwen_claude_field_theory/closure_2026/user_action_zero_flux.py`
Exit 0; output preserved as user_action_zero_flux.json.
`python3 qwen_claude_field_theory/closure_2026/user_action_calibrated_branch.py`
Exit 0 after adding an import guard; output compared against the committed
JSON to check that the earlier experiment is unchanged.

Latest Fable commit 0680e1c89 adds a nonlocal-functional study. Only its file
inventory was inspected here; its headline has not been imported as evidence
for this different action. Mathbox computation-audit scope: full theory OPEN.
