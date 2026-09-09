# Physical-response gate for the submitted action

Status: conditional obstruction in the previously declared planar static
weak-field reduction; not a universal no-go or a complete covariant audit.

Define a=1/(4 pi G)-2(c1+c4), b=2-K_B, j1=J'(s0^2), and
d=j1+2s0^2 J''(s0^2) on a regular constant-gradient scalar background.
After the independently varied spatial equation fixes zero slip with suitable
boundary conditions, the quadratic Fourier density is

L2=-a k^2 Phi^2/2+2b k^2 Phi phi
   -b(d k^2+j1 xi^2 k^4)phi^2-rho Phi.

Direct variation and elimination, away from poles and k=0, give

Phi(k)=-rho(k)/[k^2 A(k)],
A(k)=a-2b/(d+j1 xi^2 k^2),
dA/dk=4b j1 xi^2 k/(d+j1 xi^2 k^2)^2.

Exact local AQUAL linearized along a uniform nonzero physical background
has a k-independent longitudinal coefficient
[mu(y)+y mu'(y)]/(4 pi G_N). Thus this reduced action cannot reproduce that
equation at arbitrary wavelengths on regular backgrounds with b*j1*xi !=0.
A change in the measured constant G_N cannot remove dependence on k.
At k=0 the displayed Fourier Hessian vanishes, and this analysis supplies no
homogeneous constraint count or cosmological conclusion.

The long-wavelength inverse response is a-2b/d (when d !=0); the short-
wavelength limit is a (when j1*xi !=0). These describe an environmental,
scale-dependent effective coupling rather than a derived universal Newton
constant. The regular cases xi=0, b=0, or j1=0 remove the displayed dependence;
they are not certified viable repairs. Degenerate backgrounds and omitted
higher-order metric effects require their own analysis.

Construction implication: a completion retaining this reduction needs an
explicit cancellation of the scale-dependent physical response. Alternatively
the full covariant reduction must demonstrate why this truncation is invalid
in the proposed regime. Approximate long-wavelength agreement alone does not
meet the requested exact general-source MOND requirement. No inference about
the different IC50 action is made.

Reproduction from repo root:
`python3 qwen_claude_field_theory/closure_2026/user_action_response_gate.py`
Exit 0. The script differentiates the quadratic density, computes its Hessian
and determinant, solves both equations, checks substitution and the xi=0
control. Its numerical examples are dimensionless illustrations, not data.
The Hessian is static: it is not a kinetic Hessian or Poisson-bracket matrix.
This bounded interpretation follows the Mathbox computation-audit discipline.
