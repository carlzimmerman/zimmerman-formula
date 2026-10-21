# A13 — mutation record

**Flag.** `python3 a13_checks.py --mutate` (equivalently `A13_MUTATE=1`). Writes
`a13_MUTATE.out` and `a13_results_MUTATE.json`, and **must exit 1**.

**What is mutated.** The nonlinear solve of
$\nabla\!\cdot\!(\mu\nabla\Phi)=4\pi G\rho_b$ is replaced by the *linear superposition of the
two single-mass phantoms*, eq. (3) applied twice:
$$C_{\rm super}(x,\zeta)=\frac{1}{4\pi}\left[\frac{1}{x^2+(\zeta-\tfrac12)^2}+\frac{1}{x^2+(\zeta+\tfrac12)^2}\right],$$
which is what an "explicit spherical/point-mass calculation" gives if the nonlinearity is
ignored. This is the specific error the lane exists to rule out, so it is the right tooth.

**Why it must fail.** The superposition is positive everywhere, so there is no negative
pancake, no missing depth, and no lensing signal. At the saddle it gives $C=2/\pi=+0.6366$
against the law's $-0.2404$ at $R=0.2d$; the true solution is $-0.6450$ at $R=0.02d$.

**Observed (from `a13_MUTATE.out`).**

```
h=0.0040  N= 20736  C(0.2)=+0.54881  S_neg=+0.00000
h=0.0020  N= 32761  C(0.2)=+0.54880  S_neg=+0.00000
h=0.0010  N= 48400  C(0.2)=+0.54879  S_neg=+0.00000
h=0.0005  N= 67600  C(0.2)=+0.54880  S_neg=+0.00000
Richardson limit S_inf = +0.00000

K1  PASS grad_err=9.81e-04, rho_err=5.74e-03
K2  FAIL C(0.2)=+0.54879          (AG6C published -0.2401, within 3%)
K3  FAIL S(h=0.002)=+0.00000      (AG6C published -0.2064, within 6%)
K4  FAIL S_inf=+0.00000           (must lie in (-0.240,-0.218))
K5  PASS C_super=+0.6366          (analytic statement, unaffected by the mutation)
K6  FAIL mean MW-M31 depth=-0.000 (paper midpoint 2.0, ratio in [1.00,1.20])
K7  FAIL -89 check=+203.4, -33 check=+76.3
K8  FAIL S_strip=0.000            (AG7 published 0.87)
K9  FAIL eps_orient=1.000         (degenerate: no deficit map, acceptance undefined)
K10 PASS ratios=['1.00','0.75','0.34','0.02']   (EFE curve is a separate solve)
K11 PASS void=0.435, filament=0.002              (EFE curve is a separate solve)
K12 PASS void penalty=5.3, filament penalty=3.0e+05
A13 COMPLETE: 5/12 checks PASS.        exit code 1
```

**Reading.** The seven checks that depend on the phantom (K2, K3, K4, K6, K7, K8, K9) all break;
the four that are independent statements (K1 solver control, K5 analytic superposition value,
K10–K12 EFE curve, which is recomputed from scratch) survive, exactly as they should. The
mutation is caught by the sign and by the amplitude, not by a numerical accident: the mutated
$C(0.2)=+0.549$ differs from the true $-0.2404$ in sign *and* by a factor 2.3.
