# Door 3: tensor-speed condition with the coherence operator

Status: conditional local obstruction, not a universal no-go.

`door01_joint_2026/tensor_principal.py` expands the submitted static action to
second order for a transverse tensor perturbation h on a frozen background with
clock normal to the slice, scalar gradient v, zero scalar Hessian at the point,
and wave direction along the gradient. Its quadratic principal density is

L2 = (F-c13) h_dot^2/2
     - (F+b J'(X) v^2 xi^2) h_x^2/2,

where F=1/(16 pi G), b=2-K_B and c13=c1+c3 in the submitted normalization.
Therefore

c_T^2 = [F+b J'(X)v^2 xi^2]/[F-c13].

The tensor kinetic sign requires F-c13>0. Exact luminality on this background
requires

c13 = -b J'(X)v^2 xi^2.

For a constant action coefficient c13 this condition cannot hold on an extended
galactic branch if b, xi and J'v^2 vary with the scalar gradient. The calibrated
exponential kernel makes that variation explicit. With

s(y)=a0*y*(a-A+A*exp(-y))/(2b),
J'(s(y)^2)=2b*exp(y)/(a-A+A*exp(-y)),

the required coefficient is

c13_req(y)=a0^2 xi^2 y^2 [A exp(y)-A-a exp(y)]/2.

For the illustrative calibration (a,A,b,a0,xi)=(1.2,1,1,1,0.2), its sampled
values over y in [1e-4,50] range from -2.40e-10 to -5.18e22. The derivative
is nonzero symbolically (for example at a=2A,y=1). If c13=0, as commonly used
to remove the bare aether tensor-speed shift, positive b J' produces c_T^2>1
whenever v xi is nonzero.

This does not rule out a covariant completion with a different tensor operator,
a restricted background where v=0, or a modified coherence term. It does show
that the submitted finite-xi action cannot claim universal c_T=c by setting a
single constant c13=0 while retaining the calibrated nonzero-gradient MOND
branch. A field-dependent coefficient would be a different action and would
need its own variation and constraint analysis. The result is local and does
not use the observational GW170817 uncertainty.

Commands (repository root):

```
python3 qwen_claude_field_theory/closure_2026/door01_joint_2026/tensor_principal.py
python3 qwen_claude_field_theory/closure_2026/door03_tensor_2026/tensor_luminal_calibration.py
```

Both exit 0 after the second script's explicit correction from J'v to J'v^2.
The latter correction is material and is reflected in `result.json`; the first
script supplies the independently derived principal symbol. No DOF count,
PPN result, empirical fit, or full-theory closure is claimed. Mathbox
computation-audit scope remains bounded.
