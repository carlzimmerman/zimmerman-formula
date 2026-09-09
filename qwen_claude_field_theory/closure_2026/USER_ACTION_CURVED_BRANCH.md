# Constructive static branch from the same planar action

Introduce v=exp(-A)phi' and conserved scalar flux p_phi. Equivalently add
p_phi(phi'-exp(A)v) before varying. Variation of phi makes p_phi constant;
eliminating its cyclic coordinate gives the spatial Routh density

R=exp(P-A+2B)[g(2B'^2+4P'B')+ca P'^2+2b exp(A)P'v]
  -exp(P+A+2B)[C+b J(v^2+xi^2 exp(-2A)(v'^2+2B'^2 v^2))]
  -p_phi exp(A)v,

where g=1/(16 pi G). This is a change of variables and scalar-flux reduction
of the same static action, not a new matter sector. A is varied before
choosing A=0. Its equation equals minus the conserved spatial energy of R,
an identity checked symbolically. The remaining equations form a coupled
second-order system for P,B,v wherever its spatial derivative Hessian is
invertible. This Hessian is not a time-kinetic or Dirac matrix.

For a concrete numerical example choose dimensionless g=1, ca=0.1, b=1,
xi=0.2, C=0.01 and J(U)=G_exp(sqrt(U)) with a0=1. This preserves the supplied
exponential primitive as a constitutive input; it does not prove the physical
metric obeys exponential MOND. These parameters are illustrative, not fitted
or observationally viable values. Initial data are
(P,B,v,P',B',v')=(0,0,0.5,0.02,0,0).
The spatial constraint determines p_phi=-0.1592639582758006.

Two integrations to x=0.1 complete. Relative tolerances 1e-8 and 1e-10 give
maximum sampled energy-constraint residuals 1.372e-10 and 1.968e-12.
The minimum sampled singular value of the spatial Hessian is 0.0314775.
The endpoint metric fields at tighter tolerance are P=0.00247406,
B=-0.000629169. The solution is curved; no equality of potentials is imposed.

This constructs a local solution of the reduced static equations, with
improving numerical constraint accuracy. No global boundary matching,
independent clock/shift equations, tensor perturbations, empirical fit,
physical PPN value, or two-mode closure is certified. Positive singular
values here say invertibility, not absence of dynamical ghosts.

Next: restore and check the clock/shift equations on this branch, then derive
the coupled physical response using the intended MOND-calibrated J rather
than assuming the illustrative input is that calibration.

Command: `python3 qwen_claude_field_theory/closure_2026/user_action_curved_branch.py`
Exit 0; output saved as user_action_curved_branch.json. Mathbox bounded
computation-audit interpretation applies. Full theory remains OPEN.
