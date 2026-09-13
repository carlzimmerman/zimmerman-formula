# General first-gradient York/QUMOND no-slip obstruction

For the complete isotropic first-gradient two-potential class

```text
L = -2 A(u) h^{ij} Phi_i Psi_j + a0^2 F(u),
u = h^{ij} Psi_i Psi_j/a0^2,
```

variation with respect to `Phi_i` gives `-2 A(u) Psi_i`.  Exact linear
Poisson response with the measured normalization requires `A(u)=1` for every
field value (a nonzero gradient component is enough to derive this directly).
The Hilbert trace-free variation on `Phi=Psi` has the independently derived
coefficient

```text
C_TF(u) = F'(u) - 2(A(u) + u A'(u)).
```

After the Poisson requirement this becomes `C_TF=F'(u)-2`.  Hence no-slip for
arbitrary anisotropic gradients requires `F'(u)=2` identically.  The exact
exponential QUMOND carrier instead requires

```text
F'(u) = nu_exp(sqrt(u)) = 1/(1-exp(-sqrt(u))),
```

which is nonconstant and equals `2` only at `sqrt(u)=log(2)`.  The action
class therefore cannot provide exact Poisson response, exact exponential
QUMOND flux, and no slip simultaneously.  This is stronger than the earlier
single-coefficient York check, but remains scoped to one metric, two static
potentials, locality, first spatial derivatives, and isotropic dependence on
`u`; it is not a universal theorem about every nonlocal or multi-metric model.

Reproduction:

```bash
python3 general_york_no_slip_no_go_2026.py       # exit 0
python3 -m unittest -v test_general_york_no_slip_no_go_2026.py  # 1 test, exit 0
python3 run_general_york_lean.py                 # exit 0
```
