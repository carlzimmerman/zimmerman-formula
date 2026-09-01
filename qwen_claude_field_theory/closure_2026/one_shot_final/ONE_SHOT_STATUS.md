# One-shot final status

## Target

One action must give exact exponential MOND, no slip, two gravitational tensor
degrees of freedom, bare-matter conservation, vanishing preferred-frame PPN
parameters, healthy perturbations, and expanding FLRW.

## Result

`FRIED` is not established. Candidate B improves on Candidate A by keeping
minimal-matter conservation and by reproducing the exact MOND,
spherical/BTFR, and high-acceleration limits in its scalar-isotropic reduction.
That reduction is not a solution of the complete metric equations.  The full
action fails two independent necessary gates:

1. Complete spatial metric variation leaves
   `Pi_TF=-2 a0^2 y^2 exp(-y)` on a nonzero constant-gradient MOND patch, so
   `Phi=Psi` is not a full field equation.
2. On the exactly tensor-luminal Minkowski branch, the action-derived finite-`k`
   Dirac chain leaves one scalar with
   `L_red=6 zeta_dot^2-2 k^2 zeta^2` and `c_s^2=1/3`.  Restoring the scalar
   spatial shear leaves the same count.

The separate homogeneous multiplier equation imposes `a_ddot=0`: coasting
expansion remains possible, while de Sitter and accelerating Lambda-FLRW are
excluded.  No generic nonlinear DOF count is asserted; only the closed
finite-`k` branch count is used as the theorem.

**Candidate B/action-class verdict: DEAD.  Global verdict: OPEN.**  The scoped
no-go is recorded in `CURVATURE_QUMOND_ADM_NO_GO.md`.  Exact exponential MOND
fixes `2 Q_Y=exp(-sqrt(Y))` in this scalar curvature-sourced architecture, so
an additive constant is its only unused freedom and cannot repair the scalar
or trace-free metric equations.  The remaining class is not an
action construction; it is a precisely named obligation: supply a nonlinear
tensorial, genuinely nonlocal action and its real constrained phase space.
Until then, it cannot be called a relativistic MOND completion.

## “High download/view” bimetric check

The likely record is the khronon-split bimetric host (DOI
`10.5281/zenodo.22033942`).  On 2026-09-01 its public counter was one unique
download and zero views, so the apparent ratio is a one-event denominator
artifact, consistent with a direct file/API/DOI hit that bypasses the landing
page.  The physics was nevertheless rerun from the live `sf13`-`sf23` files.
The crisp content is a derived bimetric MOND map and a candidate BD-ghost
constraint mechanism.  It is not the requested finish: the advertised healthy
count is `7=2+5`, continuum Dirac closure remains open, and lensing/PPN are not
closed.  Five massive spin-2 polarizations cannot be counted as
`N_grav=2`.

## Reproducible entry point

```bash
cd qwen_claude_field_theory/closure_2026/one_shot_final
python3 test_curvature_qumond_action_gate_2026.py
python3 curvature_qumond_action_gate_2026.py
python3 test_curvature_qumond_adm_dirac_gate_2026.py
python3 curvature_qumond_adm_dirac_gate_2026.py
```

All four commands must pass before using this ledger.  An exit status of zero
certifies that the calculations reproduced their stated results; it does not
turn the falsified candidate into a phenomenological pass.
