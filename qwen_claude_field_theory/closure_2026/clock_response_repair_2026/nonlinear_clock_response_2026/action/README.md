# Full plane ADM action through quartic order

This directory extends the same unrestricted plane scalar/shear action used
by `cosmological_bridge_2026/derive.py`. It supplies an executable local
generator for the cubic and quartic action, the nonlinear lapse/shift
constraints, and their generated Fourier sources. It does **not** supply a
constraint-reduced quartic action, nonlinear lapse preservation/evolution,
or an attractor. A second bounded calculation below constructs the generated
mean/second-harmonic **initial** constraint response through order two.

No coefficient functions or particles were added. The numerical coefficients
are derivatives of the existing logarithmic `P` and square-root `W` at the
**physical** sourced `Q`, with `gamma=1e-6`.

## Variables and exact density

Use unitary clock coordinates, `delta tau=0`, with background clock rate
`sbar=tau_dot`. The lapse is `N=1+n`, the coordinate shift is `N^x=b`, and

\[
h_{xx}=a^2e^{2z+4e},\qquad h_{yy}=h_{zz}=a^2e^{2z-2e},
\qquad v=\sqrt h=a^3e^{3z}.
\]

With `Ax=z_x+2e_x`, `Bx=z_x-e_x`,

\[
K_x={H+\dot z+2\dot e-bA_x-b_x\over N},\quad
K_y={H+\dot z-\dot e-bB_x\over N},\quad K=K_x+2K_y,
\]

\[
Q={q+\dot\sigma-b\sigma_x\over N},\quad
Y=h^{xx}\sigma_x^2,\quad X=Q^2-Y,
\quad D^2\chi=h^{xx}[\sigma_{xx}+(2B_x-A_x)\sigma_x].
\]

Here `q` denotes the physical homogeneous `Q`; it is not the constitutive
reference history `qbar`. The density is

\[
\begin{aligned}
\mathcal L={}&Nv\left\{\frac{M^2}{2}[-4K_xK_y-2K_y^2+{}^{(3)}R]
 +P(X,\tau)-V(\tau)-M^2\Lambda\right.\\
&\left.\quad+\gamma[-\tfrac23Q^3K+2QK_xY+2Q^2D^2\chi
       +\chi^x\partial_xY]+C_rX_r^2
       +\tfrac12(\rho+\delta\rho)(X_d-1)\right\}
       +v\bar s W(Y,\tau).
\end{aligned}
\]

The final braiding term starts at cubic order and therefore was properly
absent in the older quadratic-only generator. It is restored here. An exact
symbolic check compares the implemented braiding density with the covariant
divergence definition of `gamma X Box chi`, at arbitrary plane lapse and
shift. The boundary vectors are

\[
B^t=-\gamma v(Q^3/3-QY),\qquad
B^x=\gamma vb(Q^3/3-QY)-\gamma Nv h^{xx}\chi_x(Q^2+Y).
\]

The compatibility identity is `chi_t=NQ+b chi_x`; no zero-shift restriction
is made in that check.

## Generated coefficients and constraints

`Jet([f0,f1,...,f4])` stores ordinary epsilon coefficients, without factorials.
`action_pieces(f,bg)` accepts arbitrary spatial jets at every order. Thus the
generic API permits independent zero, first, second, and third harmonics and
induced responses. `harmonic_fields` is only a convenient first-harmonic
witness. `P` is Taylor-expanded through `PXXXX`; `W` through `WYY`, since
`Y` begins at order two. These are existing derivatives, not independent
coefficient reconstructions.

The density coefficients are exported as `action_harmonics.S2/S3/S4` in
`run_001/result.json`. The constant harmonic is the spatial period average.
The unaveraged coefficients are retained: in particular, the vanishing
average of the first-harmonic cubic density is **not** interpreted as an
absence of quadratic field-equation sources.

The lapse constraint is obtained from the raw action before projection:

\[
\begin{aligned}
\frac{C_N}{v}={}&\frac{M^2}{2}[{}^{(3)}R+4K_xK_y+2K_y^2]
  +P-V-M^2\Lambda-2Q^2P_X\\
&+\gamma[2Q^3K-2QK_xY-2Q^2D^2\chi+\chi^x\partial_xY]\\
&+C_r[X_r^2-4R_Q^2X_r]
 +(\rho+\delta\rho)[(X_d-1)/2-T_Q^2].
\end{aligned}
\]

Define

\[
p_x=-2M^2K_y+\gamma(-2Q^3/3+2QY),\quad
p_y=-2M^2(K_x+K_y)-4\gamma Q^3/3,
\]

\[
p_Q=2QP_X+\gamma(-2Q^2K+2K_xY+4QD^2\chi).
\]

Then the coordinate shift equation, with spatial integration by parts
performed after variation, is

\[
C_b=\partial_x(vp_x)-v[p_xA_x+p_yB_x+p_Q\sigma_x
    +4C_rR_QX_r r_x+(\rho+\delta\rho)T_Q\theta_x].
\]

`constraints(f,bg)` implements these formulas for arbitrary spatial jets.
`constraint_source_harmonics` exports the exact first-, second-, and
third-order harmonic coefficients. The second-order scalar/even source has
zero and `2k` harmonics; the odd shift source has `2k`. Third-order sources
have `k` and `3k`. These are varied local equations, so no single-mode
averaging suppresses the response channels.

## A linear-constraint-compatible source

The stronger source witness uses the unchanged `Background(.01)` and
`mode_system(v,k=3)` at `t=0`. Its physical background is

\[
Q=0.9078321505772312,\quad \bar s=1.0317810692809903,
\quad H=0.5191118192004086,\quad a=1.
\]

Set `u=(sigma,deltaQ,rad,deltaQr,theta,drho)` to
`(1,0.04804480860544282,0,0,0,0)`, which makes `sigma_dot=H sigma`.
The existing linear system reconstructs all lapse/shift/metric and matter
velocities. In particular,

\[
n_1=0.5188921876091798,\quad z_1=0.5415519992408945,
\quad b_1=3.050508956940767,\quad e_1=0.
\]

The first-order lapse/shift residual is below `3.9e-15`, the linear clock
residual is zero at floating precision, and the sourced background
constraint residual is below `1.4e-17`. Nevertheless,

\[
C_N^{(2)}=-0.5954917259948045-4.110835218861041\cos(2kx),
\quad C_b^{(2)}=-14.559416983248852\sin(2kx),
\]

\[
C_N^{(3)}=-31.923621341731067\cos(kx)+26.437895892894264\cos(3kx),
\]

\[
C_b^{(3)}=2.251082706146757\sin(kx)-11.398943739858181\sin(3kx).
\]

These are coefficients; the actual perturbations and residuals have their
respective powers of epsilon. They show that a valid linear seed requires
nonlinear response fields. They do not claim those fields have been solved.

## Checks and reproduction

Run all new scripts and tests with

```sh
python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_clock_response_2026/action/run_checks.py --result-file /private/tmp/adm_action_check.json
```

The reusable bounded run is described by `contract.json` and its validated
`run_001/manifest.json`. It records source/data hashes, the actual command,
versions, tests, runtime and resource bounds. `run_001/result.json` contains
the formulas and full numerical checks; the output directory is immutable
evidence and should not be overwritten for later runs.

Checks cover exact truncated-series arithmetic against independent
differentiation, all five original S2 sectors, the shifted covariant/ADM
boundary identity, raw complex-step lapse/shift variation with an independent
Fourier divergence, exact symbolic harmonic projection, and finite-amplitude
convergence against the frozen logarithm/square-root action. The off-shell
quartic coefficient is also extracted independently with Cauchy's formula
at two radii and 32/64 contour nodes, avoiding small-amplitude subtraction
loss. The latter is a floating-point analytic coefficient check, not an
interval certificate.

## Second-order initial response

`initial_response.py` now constructs a response that cancels the full local
Hamiltonian, momentum and unitary-clock equations through order two at this
same sourced initial slice. The full unitary-clock equation is

\[
E_\tau=P_\tau-V_\tau-WK+2W_YK_xY
       +2Q[W_YD^2\chi+W_{YY}\chi^x\partial_xY].
\]

For this initial-data construction, physical `Kx,Ky,Q` are expanded directly.
Dummy `N=1,b=0` assigns coordinate velocities representing these physical
jets; it is **not** a solution of the nonlinear lapse-preservation equation.
The free choices are `mean z2=0`, equal mean `Kx2,Ky2`, spatial `e2=0`,
`sigma2=0`, `Q2k=0`, and zero second-order matter perturbations. The mean
`Q2` is solved rather than being set to zero.

The resulting coefficients are

| Response | Coefficient of epsilon squared |
|---|---:|
| Common mean `Kx2=Ky2` | 2.094171295269856 |
| Mean `deltaQ2` | 2.3972469834708416 |
| `z2 cos(2kx)` | 0.2915963815334099 |
| `Kx2 cos(2kx)` | -10.016423763278171 |
| `Ky2 cos(2kx)` | -1.2521273561553874 |

The common mean curvature here is the correction in each diagonal component;
the trace correction is three times that value. All local quadratic
constraint coefficients fall from a maximum of `15.0255` to `2.81e-14`.
The five-dimensional response matrix has condition number `7924.98` and
determinant `-1.858986`. Exact frozen-function evaluations at
`epsilon=.002,.001,.0005` have residual orders `3.0108,3.0054`; their even
parts have orders `4.00021,4.000058`, as expected after a second-order solve.

These values differ from the earlier source witness because physical
initial jets, rather than first-order coordinate velocities with all
higher coefficients set to zero, are now held fixed. Their first-order
constraints agree; their second-order completions represent different
choices of the previously unspecified data.

The record is `run_002/result.json` with `run_002/manifest.json` and
`contract_initial.json`. Reproduce with

```sh
python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_clock_response_2026/action/run_initial_checks.py --result-file /private/tmp/adm_initial_response_check.json
```

No nonlinear lapse preservation, global charge-matching condition,
third-order response, or time evolution is asserted by this initial slice.

## Remaining reduction

For fields `f=epsilon f1+epsilon^2 f2+...`, the order-two equation is the
linear operator acting on `f2`, plus the exported `C2[f1]`. It is necessary
to solve the zero/`2k` metric, scalar, matter, and preserved clock evolution
together; the initial-constraint construction above covers one stage of
that process. The order-three equation also includes bilinear `f1,f2` sources
as well as the exported `C3[f1]`. The generic action API can generate these
terms by supplying the independent epsilon coefficients and their spatial
jets; averaging before this step would lose them. Homogeneous response
equations must be taken at genuine zero wavenumber, with their boundary and
constraint conditions, not obtained from division by finite `k`.

Only after substituting those response solutions can exchange terms be
included in a constraint-reduced quartic action. None of those remaining
steps is hidden behind the success of the generator's bounded checks.

Workflow used: `mathbox:computation-audit` and
`superpowers:test-driven-development`.
