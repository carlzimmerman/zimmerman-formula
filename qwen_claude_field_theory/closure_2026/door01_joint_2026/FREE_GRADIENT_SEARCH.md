# Door 1 supplement: free-gradient compatibility search

The fixed P'=0.02, B'=-0.02 search was not the only possible initial family.
This supplement allows the common matched gradient to vary. For each of
v=(0.001, 0.01, 0.02, 0.05, 0.1) and xi=(0.2, 0.1), the unknowns are P' and
v', while B'=-P' enforces initial logarithmic no-slip and the conserved scalar
flux is fixed to zero. The two residuals are the exact spatial constraint and
the evolved curvature P''+B''.

The script runs 84 deterministic bounded least-squares starts per case:
|P'| logarithmically spaced from 1e-5 to 1, v' spaced from -10 to 10, and both
signs of P'. Bounds are [-10,10] x [-100,100]. The best residuals are:

| xi | v range | smallest best residual | largest best residual |
|---|---|---:|---:|
| 0.2 | 0.001-0.1 | 0.01428791 | 0.01748430 |
| 0.1 | 0.001-0.1 | 0.01428791 | 0.01777675 |

No tested start reaches the 1e-8 joint root criterion. The optimizer reports
convergence, but the residual floor means convergence to a nonzero
least-squares minimum, not a solution. This is consistent with the earlier
484-state constrained scan and makes a missed ordinary root in this bounded
family less likely. It still excludes neither roots outside the bounds,
tangencies, alternative source data, nor a different action branch.

Command from repository root:
`python3 qwen_claude_field_theory/closure_2026/door01_joint_2026/free_gradient_search.py > qwen_claude_field_theory/closure_2026/door01_joint_2026/free_gradient_results.json`

Exit 0. The script uses float64 SciPy least-squares on exact SymPy-generated
derivative functions; conditioning and interval errors are not certified.
The result is a bounded computational observation, not a no-go theorem.
The files are currently uncommitted because the host Git staging operation is
blocked by the account usage limit; the working-tree artifacts are preserved.
