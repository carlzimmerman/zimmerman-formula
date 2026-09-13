# Door 1: constrained no-slip search, checkpoint 3e52670d0

The full target remains OPEN. This is a finite initial-data search in the
submitted action's previously derived static planar equations, not a new
theory, a sourced MOND solution or a universal incompatibility theorem.

The earlier two-variable least-squares exploration found no root. To avoid
interpreting optimizer failure as a mathematical obstruction, the recorded
calculation first solves the exact spatial constraint E_A=0 for w=xi*v' at
each v. Both signs are then tested for P''+B''=0 using the coupled equations.
P=B=0, P'=-B'=0.02 and scalar flux=0 are fixed. The kernel and other parameters
are inherited without refitting: g=.35, ca=.1, b=1, C=.01, a0=1, a=1.2, A=1.
These are illustrative dimensionless values, not measured couplings.

There are 121 logarithmic v samples in [1e-5,10], two xi values and two signs:
484 constraint-compatible states. The curvature ranges are:

| xi | minimum P''+B'' | maximum P''+B'' |
|---|---|---|
| .2 | -10106.2853 | -0.0273777126 |
| .1 | -9576.2691 | -0.0273897333 |

The largest absolute constraint residual is 1.60e-12; the largest relative
linear-system residual is 6.23e-16; the largest sampled spatial Hessian
condition number is 747. No sampled state preserves the initially matched
metric gradients even to second spatial order. Sampling does not exclude
tangential/unsampled roots, other parameters or other initial data. Some
large-gradient samples need not represent weak galactic fields. In particular,
the illustrative C is not a derived cosmological calibration.

This outcome argues against spending more integration time on this fixed
initial-data family. Door 2's structural degeneracy calculation and a
source-consistent boundary problem have higher priority. Any renewed search
should state the changed physical input before enlarging the grid.

## Reproduction and provenance

`contract.json` specifies the mathematical surrogate, software versions,
input list, limits and non-claims. `run_001/manifest.json` records the actual
argv, base Git state, pre/post input hashes, logs and exit status. The command
uses the installed Mathbox computation-audit bounded runner with timeout
60 seconds, output cap 1 MiB and cooperative library-thread cap 1.

Scientific command, from repository root:
`python3 qwen_claude_field_theory/closure_2026/door01_joint_2026/joint_constraint.py`

Runner and child exit 0. Manifest validation with `--root` exits 0. These
statuses certify execution/provenance, not a theory pass. The recorded output
is `run_001/stdout.txt`; the equations are in the explicitly hashed imported
module `user_action_calibrated_branch.py`.
