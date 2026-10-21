# MUTATE — breaking the A22 checks

`a22_checks.py --mutate <NAME>` changes a **term** in the computation (never a boolean), reruns the same
checks, prints `K# FAIL ...` and exits **1**. Baseline `--mutate none` is 13/13 PASS, exit 0 (`a22.out`).

Each mutation is the physical alternative the corresponding check is supposed to exclude.

| mutation | what it changes | check(s) broken | baseline value | mutated value |
|---|---|---|---|---|
| `drop_clock` | removes the clock operator `P^i D_i ln N` from the quadratic Lagrangian | **K3**, **K10** | `lapse-eq residual 0`; `a_P = 2.420e-16` | residual `= p' + 2p/r` (the charge is gone) and `-Phi'`; `a_P = 0` |
| `gamma_zero` | sets `gamma = 0` (deletes the `(D.P)^2` gradient term) | **K3**, **K11** | identity `lap^2 psi + K rho/gamma = 0`; `lambda = 5.24e17 m` | identity `= 1` (no P equation left); `lambda = inf` |
| `theta_stress` | gives `theta` a nonzero background value (`theta = theta_bar + O(h)`) | **K5** | `d(theta^2)/dh|_0 = 0` | `= G_w != 0` |
| `alpha1_forced` | sets the measured `alpha_1(r)` to `1` (an `O(1)` preferred-frame response) | **K7** | `8.16e-14` (1 AU), `7.35e-11` (30 AU) | `1.000` at both radii |
| `frw_source` | adds a linear source `-K P` to the FRW Lagrangian | **K9** | `FRW eom residual 0`, source `0` | residual `= -K a^3` |
| `beta_forced` | adds a `mu^2/r^4` term to the `O(rho^2)` source list | **K8** | source exponents `{0, -2}` | exponents `{0, -2, -4}` |

## Captured mutated output (verbatim `K#` lines)

```
### drop_clock
K3   FAIL value=eq residuals=[Derivative(p(r), r) + 2*p(r)/r, 0, -Derivative(Phi(r), r)]  id(lap^2 psi + K rho/gamma)=0 thr=all 0
K10  FAIL value=a_P(mut=drop_clock)=0.000e+00  u_CMB/a0=0.0271 thr=0<a_P<B_E
A22 COMPLETE: 11/13 checks PASS.

### gamma_zero
K3   FAIL value=eq residuals=[0, 0, 0]  id(lap^2 psi + K rho/gamma)=1 thr=all 0
K11  FAIL value=gamma=K L*^2/2 exact; lambda=inf           thr=<1e30
A22 COMPLETE: 11/13 checks PASS.

### theta_stress
K5   FAIL value=theta_static=0 d(theta^2)/dh|0=G_w alpha1_lit=0 thr=0/0/0
A22 COMPLETE: 12/13 checks PASS.

### alpha1_forced
K7   FAIL value=|a1|(30AU)=1.000e+00 |a1|(1AU)=1.000e+00   thr=< 3e-04
A22 COMPLETE: 12/13 checks PASS.

### frw_source
K9   FAIL value=eom-res=-K*a(t)**3 source=0 m/H0=2.621e+08 thr=0 / 0 / >1
A22 COMPLETE: 12/13 checks PASS.

### beta_forced
K8   FAIL value=beta-1=0; src r-powers={'W=Kp^2/2': '0', 'gamma psi^2/2': '-2.00000000000000', 'p Phi_prime': '-2.00000000000000', 'forced 1/r^4': '-4.00000000000000'}; residual=4.41e-10 thr=< 1e-04
A22 COMPLETE: 12/13 checks PASS.
```

Exit status: `none` → 0; every listed mutation → 1.

## Why these are the right mutations

* `drop_clock` is the one operator A12 identified as the protector (`Pi`/`sigma` bookkeeping) and the only
  source of the charge in (4)/(7). Removing it removes the whole `O(rho)` P stress, so `a_P` must vanish —
  the check fails on the *value*, not on a flag.
* `gamma_zero` is the degenerate limit of the framework's own identity `gamma = K L*^2/2`; without it the
  charge identity (7) does not exist (`lambda → ∞`), which is exactly what K11 asserts must not happen.
* `theta_stress` is the only way `beta_ADM` could reach `alpha_1`: a nonzero background expansion. K5 is the
  statement that it is zero on the static branch — the load-bearing half of (F1).
* `alpha1_forced` and `beta_forced` are the two observational failure modes this lane is testing for: an
  `O(1)` preferred-frame response, and a Nordtvedt-scale `1/r^2` term. K7 and K8 must see them.
* `frw_source` is the "cosmic aether" alternative: any source term on FRW would give `P` a VEV. K9 asserts the
  source vanishes identically.
