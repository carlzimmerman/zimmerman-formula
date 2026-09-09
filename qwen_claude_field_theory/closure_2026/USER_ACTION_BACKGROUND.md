# Static planar quadratic action and background consistency

The script `user_action_planar_quadratic.py` retains independent lapse,
longitudinal and transverse metric fields:
ds^2=-exp(2P)dt^2+exp(2A)dx^2+exp(2B)(dy^2+dz^2), tau=t.
It expands the submitted static action about phi=s0*x and a flat metric.
It includes the measure, nonlinear J through J'', mixing, acceleration term,
cosmological/K(0) constant, and the complete projected spatial derivative
contraction in this ansatz. EH is integrated by parts. Static extrinsic
curvature vanishes. Time/clock/shift variations are outside this calculation.

With C=Lambda/(8 pi G)+K(0), b=2-K_B, J0=J(s0^2), J1=J'(s0^2),
direct variation of the first-order density gives the background equations

E_P=-C-b J0,
E_A=-C-b J0+2b J1 s0^2,
E_B=-2C-2b J0,
E_phi=0.

Hence E_A-E_B/2=2b J1 s0^2. A cosmological constant cannot cancel this
anisotropic stress: for regular nonzero b,J1,s0 the assumed flat background
requires supporting matter or must be replaced by a curved solution.
This is not a general obstruction to the submitted theory or a claim that
a local short-wavelength analysis is impossible. It prevents interpreting
the previous off-shell flat-background response as a complete physical
solution without specifying the supporting system and its perturbations.

The output also contains the full quadratic density and four linearized
static Euler-Lagrange equations in this ansatz. The exact connection-term
result is recovered as an independent conformal-metric control. No metric
potential is assigned equal to another. No mode count is assigned.

Next: solve the background equations on a declared curved branch, or specify
a matter action supplying the background stress and perturb that action too.
Then eliminate all metric/scalar perturbations consistently. No new exotic
supporting matter has been introduced by this audit.

Command (repo root):
`python3 qwen_claude_field_theory/closure_2026/user_action_planar_quadratic.py`

Exit 0, including the corrected isotropic connection control. Output saved
as `user_action_planar_quadratic.json`. This bounded static derivation follows
Mathbox computation-audit scope; the full relativistic theory remains OPEN.
