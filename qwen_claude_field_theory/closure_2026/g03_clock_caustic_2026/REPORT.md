# An exact clock caustic in the C-H action

2026-09-05. **Full theory OPEN; exact nonlinear clock-caustic branch established.**
This is a result for the same action in
[ACTION.md](../g03_covariant_action_2026/ACTION.md), using its full variations
in [FULL_VARIATION.md](../g03_covariant_action_2026/FULL_VARIATION.md).
It is neither a new empirical law nor a proof that every primordial-clock
theory fails. No extra action term or matter source has been inserted.

## 1. A full-action solution, not a frozen-metric approximation

Use length coordinates, signature (-+++), and c=1 until units are restored.
The action is Einstein-Hilbert with Lambda, its specified GHY terms and
minimally coupled matter, plus the auxiliary density

\[
\mathcal L_{\rm aux}=2|DU-a|^2+2\alpha^2q(|DW_b|^2/\alpha^2)
+\int_0^b L(W_z-\Delta_hW)\,dz+\lambda_0(W_0-U),
\quad b=\xi^2/2,\quad\alpha=a_0/c^2>0.
\]

Here n_mu=-partial_mu tau/sqrt(X), X=-(partial tau)^2>0,
a_mu=n^nu nabla_nu n_mu, and Delta_h is the intrinsic Laplacian of the
compact clock leaf. The exact kernel is parametrized by

\[
s=y(1-e^{-y}),\qquad
q(s^2)=2-2(1+y)e^{-y}-y^2e^{-2y}.
\]

Consider the branch

\[
U=W=C_U\ \text{(spacetime and heat-coordinate constant)},\qquad
L=\lambda_0=0,\qquad X=1,
\]

with ordinary matter absent. Since n_mu=-partial_mu tau is a unit gradient,
symmetry of its covariant derivative gives
a_mu=n^nu nabla_mu n_nu=(1/2)nabla_mu(n^2)=0.
Thus V=DU-a=0 and w=DW_b=0.

Do not substitute a finite q'(0). Direct differentiation gives
q(0)=0, d[q(s^2)]/ds -> 0 but q'(s^2) -> +infinity as s -> 0+.
The composite q(|w|^2/alpha^2) is C1 at w=0, and its first variation is
zero there. In particular f_mu=q' w_mu extends continuously to zero,
and q' w_mu w_nu also tends to zero. Its second variation is not regular.

Every auxiliary Euler-Lagrange equation and both heat endpoints now vanish:

\[
W_z=\Delta_hW=0,\quad W_0-U=0,\quad
L_z=-N^{-1}\Delta_h(NL)=0,\quad
L_b=4N^{-1}D_i(Nf^i)=0,
\]
\[
\lambda_0=L_0=0,\qquad -4N^{-1}D_i(NV^i)-\lambda_0=0.
\]

This works on a tilted or curved smooth closed leaf: its heat operator
preserves constants exactly. It does not rely on a flat Fourier kernel.
In FULL_VARIATION.md the full lapse derivative mathcal H, spatial stress
P_ij, and clock covectors mathcal A_mu and mathcal J_mu all vanish.
For the potentially singular clock-current term, partial_mu W_b is
identically zero; the continuous first variation of the composite is used.
Equivalently, the original auxiliary density has zero first variation
with respect to every field on this branch. Metric dependence of the heat
operator cannot contribute: delta(Delta_h) applied to a constant is zero,
and every multiplier is zero.

Consequently epsilon=P_ij=0, the clock equation and its conservation
identity are 0=0, and the remaining metric equations are exactly

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}=0.
\]

Take the expanding flat-slicing de Sitter metric with a spatial T3 quotient,

\[
ds^2=-dt^2+A(t)^2(dx^2+dy^2+dz^2),\quad A=e^{Ht},\quad
H=\sqrt{\Lambda/3}>0.
\]

The code builds its connection, Riemann tensor, contractions and Einstein
equation from the metric. No expected curvature is inserted into that
calculation. The branch satisfies every varied equation throughout each
smooth pre-caustic slab. This is exact preservation along an explicit
solution, **not** a generic canonical/Dirac closure or uniqueness theorem.

## 2. Reconstructing the clock from exact characteristics

At the construction slice t=0 introduce a periodic label q and conserved
covariant spatial geodesic momentum

\[
P(q)=-p_0\sin(kq),\quad p_0>0,\quad k=2\pi m/L_x>0,\qquad
\tau_0(q)=-\frac{p_0}{k}\cos(kq)+C.
\]

P is not coordinate velocity. Write E=exp(-2Ht), gamma=sqrt(1+P^2 E),
gamma_0=sqrt(1+P^2). The exact map and its momentum derivative are

\[
x(t,q)=q+D(P(q),t),\qquad
D=\frac{P(1-E)}{H(\gamma_0+\gamma)},\qquad
D_P=\frac{1-E}{H\gamma_0\gamma(\gamma_0+\gamma)}
=\int_0^t\frac{e^{-2Hs}\,ds}{(1+P^2e^{-2Hs})^{3/2}}.
\]

The rationalized formulas are regular at P=0. The proper-clock increment is

\[
T(P,t)=\int_0^t\frac{ds}{\sqrt{1+P^2e^{-2Hs}}}
=t+\frac1H\log\frac{1+\gamma}{1+\gamma_0},\qquad T_P=-PD_P.
\]

Define tau(t,x(t,q))=tau_0(q)+T(P(q),t). With J=x_q=1+P'D_P,
the identities tau_q|t=-PJ and dx/dt=PE/gamma give, while J>0,

\[
\tau_x=-P,\qquad \tau_t|_x=\gamma,\qquad X=\gamma^2-EP^2=1,
\qquad n^\mu=(\gamma,EP,0,0).
\]

Thus this is an actual single-valued clock solving the eikonal equation,
not a freely assigned vector field. Its transport equation is
P_t+(PE/gamma)P_x=0. A direct connection calculation independently verifies
n.n=-1 and n^nu nabla_nu n^mu=0.

## 3. Global first caustic: a sharp threshold for this family

For all t>=0, D_P lies between zero and (1-E)/(2H), while P'>=-p0 k.
The two relevant bounds saturate simultaneously at q=0 modulo 2pi/k.
Hence the exact global minimum is

\[
J_{\min}(t)=1-\frac{p_0k}{2H}(1-e^{-2Ht}).
\]

Before its first zero the periodic map is a degree-one diffeomorphism.
A finite future caustic occurs if and only if p0 k>2H, and

\[
\boxed{t_*=-\frac{1}{2H}\log\left(1-\frac{2H}{p_0k}\right).}
\]

At p0 k<2H the Jacobian is bounded away from zero. At equality
J_min=exp(-2Ht)>0 for every finite time: equality is not a finite caustic.
For H=0, D=tP/gamma_0, D_P=t/gamma_0^3 and t*=1/(p0 k), also the
H->0 limit. In physical seconds H_phys=cH and T*=t*/c; the threshold
is c p0 k>2H_phys. No physical growth rate or a0-Lambda relation is fitted.

## 4. Invariant clock singularity, smooth spacetime

Direct covariant differentiation yields the clock expansion

\[
K=\nabla_\mu n^\mu
=H(2\gamma+1/\gamma)+\frac{EP'}{\gamma^2J}.
\]

At the focusing center q=0 the extrinsic principal curvatures are
H-p0 k E/J, H, H. Therefore

\[
K=3H-\frac{p_0kE}{J}
=-\frac{1}{t_*-t}+O(1),\qquad
K_{ij}K^{ij}=(H-p_0kE/J)^2+2H^2,
\]
\[
{}^{(3)}R=6H^2-K^2+K_{ij}K^{ij}
=\frac{4Hp_0kE}{J}\longrightarrow+\infty\quad(H>0).
\]

The sign of the Gauss relation agrees with the inherited ADM/GHY convention.
Raychaudhuri gives dot K=-K_ij K^ij+3H^2 along this center; the exact
symbolic residual vanishes and the computed pole residue is -1.
At the threshold p0 k=2H, the center instead has K=H for all finite t.
Spacetime invariants remain

\[
{}^{(4)}R=12H^2,\qquad R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}=24H^4.
\]

K and the induced leaf curvature are invariant under spacetime coordinate
changes and smooth increasing clock relabelings, since those leave n
unchanged as a geometric field. This is not merely a bad coordinate
Jacobian. The smooth clock congruence and the smooth intrinsic geometry
used to define the heat operator cannot continue through this caustic.
No unproved extra branch gauge identification is assumed either way.

## 5. The original compact clock-cap domain is respected

The slice t=0 was only used to construct the solution; it is not generally
a clock leaf and is not passed off as an action boundary. Put d=p0/k.
For 0<t<t*, tau_q=-PJ shows that its global extrema at fixed t are
tau_min=t-d+C and tau_max=t+d+C. If t*>2d, any level

\[
d+C<s<t_*-d+C
\]

is a smooth compact T3 graph lying entirely within 0<t<t*. Indeed
tau_t|x=gamma>0 and its time coordinates lie in [s-C-d,s-C+d],
whose endpoints are strictly inside (0,t*).
Restrict the action between any two such levels, with the stipulated fixed
cap data. Caps can approach s*=t*-d+C, where the focusing center becomes
singular. A sufficient nonempty-cap condition is p0<1/sqrt(2), together
with p0 k>2H, since t*>1/(p0 k)>2p0/k. The numerical example
H=1, p0=0.1, k=30 satisfies these inequalities. No noncompact extension
or problematic externally prescribed stress is used.

## 6. Reproducible computations and limits of the evidence

[clock_caustic.py](clock_caustic.py) differentiates the exact kernel,
derives metric curvature and clock acceleration, checks six independent
characteristic identities, solves the center Jacobian for its zero, and
checks Raychaudhuri. Independent DOP853 evolution integrates the
coordinate-time geodesic equations and their variational/Jacobi equation,
not the proposed closed-form Jacobian. Its evolved variables are x, v,
tau, J and J_dot; v_dot=-2Hv+H A^2 v^3 and
J_ddot=(-2H+3H A^2 v^2)J_dot.

Eight trajectories have maximum absolute error 7.15e-14. Independent
Jacobi events agree with the exact caustic times to less than 5.0e-13:

| H, p0, k | Exact t* | Integrated event |
| --- | ---: | ---: |
| 1, 0.2, 20 | 0.346573590279973 | 0.346573590280467 |
| 0.3, 0.1, 30 | 0.371905918857016 | 0.371905918856820 |
| 1, 0.05, 100 | 0.255412811882995 | 0.255412811883458 |

For H=1,p0=0.1,k=30, t*=0.549306144334055. At gaps 0.1,0.01,0.001,
0.0001 below t*, K is approximately -8.03,-98.00,-998.00,-9998.00,
whereas spacetime R=12 and Riemann-squared=24 throughout. The finite
2049-node scan checks implementation; the global bound in section 3,
not that scan, proves the first-caustic statement. Seeds are unnecessary.
The manifest records exact inputs, hashes, software, tolerances and grids.

The tests include sign/normalization identities, equality and zero-Hubble
controls, independent event integration, genuine clock caps, invariant
focusing and refusal of a full-theory certificate. Default exit 0 only
means these diagnostics pass; --require-closed returns 2 (OPEN).

## 7. Interpretation and next unavoidable gate

This result holds for every alpha>0 and xi>0 in this C-H action: changing
the exponential interpolation or filter width cannot affect a branch
where every auxiliary gradient and its first variation are zero. Any
proposed regularization must actually act on this focusing branch or
define an admissible continuation beyond the current smooth domain.

This branch has **zero auxiliary stress and zero clock charge**. It is
not itself a proof that the previously derived nonzero dust-density
perturbation becomes unstable, and no matter-observable curvature
catastrophe has been demonstrated. There is no claimed general ghost,
gradient-instability, acausality or local-ill-posedness theorem. Neither
generic Dirac rank/DOF nor uniqueness from complete canonical initial data
is settled. The exact zero-field first variation used here does not repair
the singular second variation found in the previous nonlinear-lift study.
C-H is still the screened extension identified in ACTION.md, not a
construction of the original exact AQUAL equation for general sources.

Next: establish the complete initial-data/constraint structure on this
zero-field branch and determine whether an admissible same-action
continuation exists. A weak or multivalued eikonal solution alone does not
suffice: the clock leaves, their heat operator, variational domain and
junction/selection rules must also be defined. If a new clock term is
needed, it is a new candidate whose DOF, MOND and lensing gates must be rerun.
An origin and abundance for a primordial clock remain separate obligations.

## 8. Prior-art scope and current repository boundary

The generic mechanism is not claimed novel. Barvinsky explicitly discusses
caustic formation in potential geodesic clock/dust flows, in section 3,
printed page 5 of [arXiv:1311.3111v1](https://arxiv.org/pdf/1311.3111v1),
*Dark matter as a ghost free conformal extension of Einstein theory*
(13 November 2013). That is a different action; its ghost and gauge results
are not imported here. Our derivation supplies this C-H branch, its exact
periodic de Sitter threshold, invariants and original compact-cap embedding.
No exhaustive priority search for that particular combination was made.

Bounded search on 2026-09-05: arXiv queries for geodesic aether caustics,
mimetic clock caustics, and “TeVeS gets caught on caustics”; the latter
identified arXiv:0802.1215 but its full text was not authenticated here.
Barvinsky's actual PDF header and section 3 argument were read, not just
search snippets. No external theorem is needed for sections 1–5.

Work began at HEAD 129311b8e. During this study HEAD advanced to 8e9d8c601,
adding Fable's f33b/f34 calculations for a different dynamical-scalar/clock
host. Those outputs supply no equation or health certificate for C-H.
The exact input hashes, rather than a clean-tree assumption, identify this
study's dependencies. Other contributors' tracked and untracked work is
untouched. No commit or push was performed for this study.

## 9. Files and verification commands

Only this directory was authored in this study: CONTRACT.md,
clock_caustic.py, test_clock_caustic.py, REPORT.md, results.json and
computation_manifest.json. The last two are generated. Run from repo root:

```sh
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_clock_caustic_2026 -v
python3 -B qwen_claude_field_theory/closure_2026/g03_clock_caustic_2026/clock_caustic.py
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_nonlinear_lift_2026 -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_flrw_scalar_2026 -v
git diff --check -- qwen_claude_field_theory/closure_2026/g03_clock_caustic_2026
```

The clock unit test invokes --require-closed with an isolated temporary
output directory and requires exit 2. Before implementation its eight
tests failed (exit 1), establishing a red baseline. Final verification
results: clock suite 8/8, nonlinear-lift suite 11/11, and FLRW suite 10/10
passed, each exit 0 (29 tests total). The producer's ten diagnostic groups
passed with exit 0; the strict-certificate run inside the clock test
returned the required exit 2. The scoped git whitespace check returned 0;
because these files are untracked, that check alone does not inspect them.

An independent read-only mathematical/code review found no important gap
at the stated branch scope. Its minor correction to the cap-time interval
from open to closed endpoints was applied in section 5. Mathbox self-review
covered this report only: this was the sole mathematical-token correction;
no remaining local notation or delimiter issue was identified. The stated
generic uniqueness and physical-health questions are not proofreading gaps.
